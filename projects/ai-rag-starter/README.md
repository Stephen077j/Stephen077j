# Retrieval starter — Python starter

Find evidence in authorized text with TF-IDF-like term overlap; cite source ids.

## Run / Exécuter

Python 3.10+ (standard library only):

```bash
cd projects/ai-rag-starter/
python main.py
python -m unittest discover -s tests -v
```

## Scope / Limites

This **small tested starter** is not a full production application, trained model or verified mobile build. No API charges, hidden credentials, sensitive user data or automatic downloads.

**Français :** exemple Python léger, réutilisable, avec tests. Il faut ajouter les modèles, dépendances, évaluations et contrôles de sécurité selon les besoins réels.

## Improved retrieval

This implementation ranks matching documents using a small TF-IDF-style weighted term-frequency score, caps input sizes, rejects duplicate source IDs, and returns deterministic cited excerpts. It **does not** generate answers or guarantee semantic retrieval. Always obtain and authorize source documents before indexing.
