import csv
import json
from pathlib import Path
from classifier import train

ROOT = Path(__file__).resolve().parent


def load_examples(path=ROOT / "data" / "examples.csv"):
    with open(path, encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if not {"text", "label"}.issubset(reader.fieldnames or []):
            raise ValueError("CSV needs text and label columns")
        return [(row["text"], row["label"]) for row in reader]


if __name__ == "__main__":
    model = train(load_examples())
    (ROOT / "model.json").write_text(json.dumps(model,indent=2,ensure_ascii=False), encoding="utf-8")
    print(f"Trained demo model on {model['sample_count']} fictional samples")
