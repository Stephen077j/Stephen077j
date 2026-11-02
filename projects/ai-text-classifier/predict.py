import json
import sys
from pathlib import Path
from classifier import predict

ROOT=Path(__file__).resolve().parent


def load_model():
    with open(ROOT / "model.json",encoding="utf-8") as stream:
        return json.load(stream)


if __name__ == "__main__":
    if len(sys.argv)<2:
        raise SystemExit('Usage: python predict.py "example text"')
    print(json.dumps(predict(load_model()," ".join(sys.argv[1:])),ensure_ascii=False))
