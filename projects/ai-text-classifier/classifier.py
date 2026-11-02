import math
import re
from collections import Counter, defaultdict

TOKEN = re.compile(r"[^\W_]+", re.UNICODE)


def tokenize(text):
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    return TOKEN.findall(text.casefold())


def train(samples):
    samples = list(samples)
    if not samples:
        raise ValueError("at least one training sample is required")
    counts = defaultdict(Counter)
    totals = Counter()
    vocabulary = set()
    for text, label in samples:
        if not isinstance(label, str) or not label.strip():
            raise ValueError("labels must be nonempty strings")
        words = tokenize(text)
        totals[label] += 1
        counts[label].update(words)
        vocabulary.update(words)
    return {
        "labels": sorted(totals),
        "documents": dict(totals),
        "tokens": {label: dict(counts[label]) for label in sorted(totals)},
        "vocabulary_size": max(1, len(vocabulary)),
        "sample_count": len(samples),
    }


def predict(model, text):
    words = tokenize(text)
    labels = model["labels"]
    if not labels:
        raise ValueError("model has no labels")
    scores = {}
    for label in labels:
        prior = model["documents"][label] / model["sample_count"]
        counts = model["tokens"][label]
        denominator = sum(counts.values()) + model["vocabulary_size"]
        scores[label] = math.log(prior) + sum(
            math.log((counts.get(word, 0) + 1) / denominator) for word in words
        )
    top = max(scores.values())
    weights = {label: math.exp(score - top) for label, score in scores.items()}
    total = sum(weights.values())
    probabilities = {label: round(weight / total, 6) for label, weight in weights.items()}
    best = max(labels, key=lambda label: (scores[label], label))
    return {"label": best, "scores": probabilities}
