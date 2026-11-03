"""Offline transparent sentiment baseline for short comments."""
import argparse
import csv
import re
from pathlib import Path

POSITIVE = frozenset({'bon', 'bonne', 'excellent', 'super', 'rapide', 'merci', 'parfait', 'bien', 'good', 'great', 'fast', 'love', 'misaotra', 'tsara', 'mahafinaritra'})
NEGATIVE = frozenset({'mauvais', 'mauvaise', 'lent', 'lente', 'cher', 'chere', 'déçu', 'decu', 'nul', 'bad', 'slow', 'poor', 'hate', 'ratsy', 'lafo'})
NEGATIONS = frozenset({'pas', 'not', 'tsy', 'jamais', 'never'})
TOKEN_RE = re.compile(r"[^\W\d_]+", re.UNICODE)


def classify(text: str) -> tuple[str, int]:
    tokens = TOKEN_RE.findall(text.casefold())
    score = 0
    for i, token in enumerate(tokens):
        weight = int(token in POSITIVE) - int(token in NEGATIVE)
        if weight and any(t in NEGATIONS for t in tokens[max(0, i - 2):i]):
            weight *= -1
        score += weight
    return ('positive' if score > 0 else 'negative' if score < 0 else 'neutral', score)


def process_csv(source: Path, destination: Path, column: str = 'comment') -> int:
    if source.resolve() == destination.resolve():
        raise ValueError('Input and output must be different files')
    with source.open('r', encoding='utf-8-sig', newline='') as inp:
        reader = csv.DictReader(inp)
        if not reader.fieldnames or column not in reader.fieldnames:
            raise ValueError(f'Missing CSV column: {column}')
        if 'sentiment' in reader.fieldnames or 'score' in reader.fieldnames:
            raise ValueError('Input already contains sentiment or score column')
        with destination.open('w', encoding='utf-8', newline='') as out:
            writer = csv.DictWriter(out, fieldnames=[*reader.fieldnames, 'sentiment', 'score'])
            writer.writeheader()
            count = 0
            for row in reader:
                label, score = classify(row[column] or '')
                writer.writerow({**row, 'sentiment': label, 'score': score})
                count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description='Offline FR/EN/MG sentiment CSV baseline')
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--column', default='comment')
    args = parser.parse_args()
    print(f'Processed {process_csv(args.input, args.output, args.column)} rows')


if __name__ == '__main__':
    main()
