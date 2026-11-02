# AI Development Toolbox | Boîte à outils IA

A curated, practical **reference index** for adding artificial intelligence to Python, JS/TS and full-stack projects. FR / EN. This folder contains links, **not copies** of external projects. Verify every upstream license, model license, version and hardware requirement.

## Choose by task / Choisir selon le besoin

| Goal / Objectif | Reference GitHub repositories | First step / Démarrage |
|---|---|---|
| Local LLM without paid API / LLM local | [Ollama](https://github.com/ollama/ollama), [llama.cpp](https://github.com/ggml-org/llama.cpp) | Run a small model locally; check RAM, CPU/GPU and each model's license |
| Hugging Face models / Modèles et NLP | [Transformers](https://github.com/huggingface/transformers), [sentence-transformers](https://github.com/huggingface/sentence-transformers) | Start with a tiny embedding or classification example |
| Retrieval augmented generation / RAG documentaire | [LlamaIndex](https://github.com/run-llama/llama_index), [LangChain](https://github.com/langchain-ai/langchain), [Chroma](https://github.com/chroma-core/chroma) | Create ingestion -> chunking -> retrieval -> cited answer |
| Agents and tools / Agents et outils | [LangGraph](https://github.com/langchain-ai/langgraph), [AutoGen](https://github.com/microsoft/autogen) | Implement a limited, human-approved tool workflow |
| Computer vision / Vision | [OpenCV](https://github.com/opencv/opencv), [Ultralytics](https://github.com/ultralytics/ultralytics) | Test an offline demo on non-sensitive images; check model/code licenses |
| Speech-to-text / Audio | [faster-whisper](https://github.com/SYSTRAN/faster-whisper), [whisper.cpp](https://github.com/ggml-org/whisper.cpp) | Benchmark transcription on representative FR/MG/EN recordings with consent |
| Model serving / Serveur IA | [vLLM](https://github.com/vllm-project/vllm), [LiteLLM](https://github.com/BerriAI/litellm) | Separate serving, request limits and authentication |
| LLM UI / Interface IA | [Open WebUI](https://github.com/open-webui/open-webui) | Run locally and review its deployment/security instructions |
| Evaluate accuracy / Évaluer | [Ragas](https://github.com/explodinggradients/ragas), [DeepEval](https://github.com/confident-ai/deepeval), [promptfoo](https://github.com/promptfoo/promptfoo) | Build a small test dataset with known expected outputs |
| Experiments and tracking / Suivi | [MLflow](https://github.com/mlflow/mlflow), [Langfuse](https://github.com/langfuse/langfuse) | Log datasets, model versions, latency, cost and failures |
| Security / Sécurité | [garak](https://github.com/NVIDIA/garak), [OWASP GenAI Security](https://github.com/OWASP/www-project-top-10-for-large-language-model-applications) | Test prompt injection, leaked secrets and unsafe tool access |

## Practical reference architectures / Architectures réutilisables

### A. Offline assistant (no cloud model API required)
`Local UI -> Python API -> Ollama or llama.cpp -> response`. Add clear model selection, failure handling, rate limits and local resource monitoring. **Running locally can be free of API charges but needs sufficient hardware and electricity**.

### B. Document Q&A with sources
`Upload authorized files -> parse -> split -> embeddings -> vector index -> retrieve -> LLM -> cite retrieved passages`. Protect uploads, access boundaries, and private content; evaluate whether answers really come from source passages.

### C. AI classification API
`POST /predict -> validate -> load versioned model -> infer -> return class + confidence + model version`. Add golden test cases and drift monitoring. For multilingual projects, evaluate FR, MG and EN separately; do not assume equivalent accuracy.

### D. Responsible AI workflow
`User request -> permissions -> constrained tools -> human approval for high-impact actions -> event log -> final output`. Never allow arbitrary shell commands, database mutations or external messages based only on untrusted model output.

## Essential checklist / Liste avant mise en production

- [ ] Clear problem; baseline without AI if possible
- [ ] Dataset consent, provenance, permissions, retention and privacy
- [ ] Model and code licenses; commercially permitted usage
- [ ] Explicit evaluation set with diverse language/domain cases
- [ ] Test hallucinations, prompt injection, data leakage and misuse
- [ ] Credentials in environment variables or secret manager, never Git
- [ ] API authentication, per-user authorization and rate limiting
- [ ] Cost, GPU/RAM, timeouts, fallback paths and offline behavior
- [ ] Human review for consequential decisions or actions
- [ ] Version pinning, reproducible setup, tests and CI
- [ ] README: setup, supported languages, limitations and real benchmarks

## Development conventions

Use **small, testable examples** rather than copying entire frameworks into a repository. A fork is useful to contribute changes to an upstream project; a template is useful to start independent work; install a package when only one library is needed. A public GitHub repository is **not automatically licensed for copying**.

## Français : ordre de progression conseillé

1. Faire fonctionner un petit modèle local (Ollama) et comprendre ses limites matérielles.
2. Ajouter une API Python FastAPI avec tests (aucune donnée réelle dans le dépôt).
3. Ajouter la recherche documentaire RAG avec citations vérifiables.
4. Évaluer les réponses en français, malgache et anglais sur des exemples représentatifs.
5. Ajouter sécurité, journalisation, limites d'usage et documentation.
6. Construire ensuite des intégrations pour tes projets existants, seulement si leur valeur est claire.

**Note:** These are external references, not dependencies installed in your repositories. This index is not a claim that any model is available or tested on a particular device.
