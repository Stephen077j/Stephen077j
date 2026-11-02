# AI Text Classifier Starter — FR / EN

A **working, dependency-light machine learning starter** for intent classification with Python. It trains a multinomial Naive Bayes model from a local, tiny **fictional** example dataset. It includes unit tests and an optional JSON HTTP API using the Python standard library.

> Demonstration only. The example corpus is too small for real-world or multilingual quality claims. Never put customer texts or sensitive datasets in the public repository.

## Start / Démarrage

Python 3.10+; no pip install required.

```bash
cd projects/ai-text-classifier
python train.py
python predict.py "I want to track my order"
python -m unittest discover -s tests -v
python api.py
```

Send a JSON request locally:

```bash
curl -X POST http://127.0.0.1:8765/predict -H "Content-Type: application/json" -d '{"text":"I want to track my order"}'
```

## What it does / Fonctionnement

- Train a reproducible text classifier on the fictional CSV in `data/examples.csv`.
- Tokenize words, count word frequencies and use Laplace smoothing.
- Predict a class and return scores normalized to sum to one.
- Run a local-only HTTP endpoint and refuse oversized/invalid requests.
- No model weights downloaded; no GPU or third-party API charges.
- `train.py` emits a reproducible JSON model to `model.json` (generated locally and ignored by Git).

## Limits / Limites

This is a starter for code reuse, **not a measured model**: no separate held-out dataset, no performance benchmark and no guarantee for Malagasy, French or English outside the supplied examples. For production, replace data with consented, audited data, add splits, precision/recall/F1 per language, authentication, persistence, security review and real evaluation.

## License and security

See the repository LICENSE if you plan to copy code elsewhere. No secret keys or private data. Bind API on localhost only. Model files are data and should not be loaded from untrusted sources without review.

## Français

Démonstration de classification automatique de messages par Python, sans API payante. Les données sont fictives et les tests vérifient seulement le comportement du logiciel, **pas sa précision réelle**.
