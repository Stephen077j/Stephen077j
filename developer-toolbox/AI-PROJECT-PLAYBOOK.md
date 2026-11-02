# AI Project Playbook — guide opérationnel FR / EN

**Purpose:** choose a stack, start a lawful project, validate it, and ship it without repeatedly searching for the same guidance. This complements [AI.md](AI.md).

## Decision tree / Choisir vite

| Your constraint | Recommended first approach | Avoid initially |
|---|---|---|
| No GPU, low budget | scikit-learn, lightweight sentence embeddings, CPU-friendly quantized model | GPU-heavy image/video generation |
| Offline Android | ONNX Runtime or ExecuTorch + compact licensed model | Assuming desktop inference works unchanged on phone |
| User asks questions about documents | Retrieval pipeline + permissions + quotations/citations | Sending all documents to model context |
| Classification FR/MG/EN | Labeled corpus -> baseline TF-IDF + linear model -> per-language evaluation | Reporting only global accuracy |
| Business API | FastAPI + Pydantic + controlled model inference | Unauthenticated public inference endpoints |
| Agent with external actions | Allowlisted tools + approval + audit log | Unrestricted tool execution |
| Speech and vision | Test on consented representative inputs and actual target hardware | Assuming one model works for all accents or image types |

## Project types and exact starter requirements

### NLP / classification
Inputs: documented labels, license, language and data split. Baseline: scikit-learn TF-IDF + LogisticRegression or LinearSVC. Tests: label consistency, no train/test leakage, precision/recall/F1 by language. Model card required.

### Document assistant / RAG
Inputs: authorized documents. Flow: parse -> chunk -> embed -> index -> retrieve -> answer with verifiable source references. Tests: retrieval recall, factual groundedness, access-control between users, malicious instructions embedded in documents, missing-source behavior.

### Offline assistant / local LLM
List the exact model, weights license, quantization, runtime, RAM/VRAM, storage, OS. Benchmark first-token latency, response speed and representative prompts. Include offline failure recovery. Do not claim zero cost: hardware and electricity still matter.

### Computer vision / OCR
Record camera/input permission, image size, lighting, labels, precision/recall on a held-out set, false positives/negatives and human corrections. Do not store faces or sensitive images without necessity and authorization.

### Voice interface
Document microphone consent, languages/accent test set, word-error rate, latency, local recording retention and whether any transcription leaves the device.

### AI-powered web/mobile app
Use least-privilege credentials, authenticated endpoints, per-tenant separation, request-size limits, timeouts, budget caps, monitoring and human approvals for consequential actions.

## Templates to keep in every AI repository

```text
README.md
LICENSE
.env.example
.gitignore
requirements.txt or pyproject.toml
src/
tests/
docs/ARCHITECTURE.md
docs/MODEL_CARD.md
docs/DATASET_CARD.md
docs/SECURITY.md
docs/DEPLOYMENT.md
.github/workflows/ci.yml
```

### Model card essentials
Model name/version/source; intended and prohibited uses; data provenance; weights/code licenses; preprocessing; evaluation metrics by subgroup/language where appropriate; limitations; environmental/hardware requirements; human oversight.

### Dataset card essentials
Collection source, consent/rights, date, language, size, cleaning, label process and agreement, splits, known imbalance, retention/deletion and privacy classification. Do not publish nonpublic samples.

### Security checklist
- Separate instructions from retrieved documents; treat webpages and tool results as untrusted data.
- Keep API keys out of Git; use GitHub secret scanning and environment variables.
- Check direct and indirect prompt injection, unauthorized retrieval, model/tool supply chain, unsafe output handling, rate limits, cost amplification and excessive permissions.
- Log minimally and redact sensitive inputs. Preserve rollback and incident response plans.
- Run dependency and container scans; pin versions and patch regularly.

### Deployment checklist
- Define hosting target (local PC, Android, web, VPS), CPU/RAM/storage/GPU, concurrency and fallback.
- Add liveness/readiness checks, request tracing, model version, resource caps, observability and backups for persisted state.
- CI should run lint, unit tests, regression prompts and dependency checks; benchmark on real hardware before claiming performance.
- Stage -> verify -> deploy -> monitor -> rollback; do not deploy customer data to an unverified demo.

## Useful references / Liens de référence

- [OpenAI Evals](https://github.com/openai/evals): evaluation patterns.
- [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/): application security risk categories.
- [Hugging Face model cards](https://huggingface.co/docs/hub/model-cards): model documentation conventions.
- [Hugging Face dataset cards](https://huggingface.co/docs/hub/datasets-cards): dataset documentation conventions.
- [Cookiecutter](https://github.com/cookiecutter/cookiecutter): project skeleton generation.
- [pre-commit](https://github.com/pre-commit/pre-commit): repeatable local checks.
- [Ruff](https://github.com/astral-sh/ruff): Python lint/format.

## Roadmap for this account

1. Verify and fix CI on the six existing Python repositories.
2. Add reproducible minimal AI demos: text classifier, grounded document retrieval, offline inference.
3. Publish model and dataset cards **only** for models/datasets actually used, with measured results.
4. Add screenshots, releases and deployment instructions after real end-to-end testing.
5. Track a single issue per outstanding improvement and make purposeful PRs; don't create issues merely for contribution counts.

**Status:** this is documentation, not an installed AI environment, working training pipeline, or proof of measured performance.
