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


---

# Extended AI engineering reference / Référentiel IA avancé

> These categories expand the initial AI index. They are reference links, not downloaded dependencies or claims of compatibility.

## 1. Data engineering, datasets and labeling / Données

- Dataframes: [pandas](https://github.com/pandas-dev/pandas), [Polars](https://github.com/pola-rs/polars)
- Dataset loading and versioned datasets: [Hugging Face Datasets](https://github.com/huggingface/datasets), [DVC](https://github.com/iterative/dvc)
- Quality validation: [Great Expectations](https://github.com/great-expectations/great_expectations)
- Annotation: [Label Studio](https://github.com/HumanSignal/label-studio), [CVAT](https://github.com/cvat-ai/cvat)
- Data orchestration: [Apache Airflow](https://github.com/apache/airflow), [Prefect](https://github.com/PrefectHQ/prefect)
- Dataset basics: consent, licensing, train/validation/test splits, leakage prevention, deduplication, metadata, provenance.

## 2. Classical ML, AutoML and forecasting

- General ML: [scikit-learn](https://github.com/scikit-learn/scikit-learn), [XGBoost](https://github.com/dmlc/xgboost), [LightGBM](https://github.com/microsoft/LightGBM)
- Automatic modeling: [AutoGluon](https://github.com/autogluon/autogluon), [Optuna](https://github.com/optuna/optuna)
- Time series: [Darts](https://github.com/unit8co/darts), [sktime](https://github.com/sktime/sktime)
- Explainability: [SHAP](https://github.com/shap/shap), [LIME](https://github.com/marcotcr/lime)
- Evaluate out of time and against simple baselines. Accuracy alone is not enough for imbalanced classes.

## 3. Deep learning and training / Entraînement

- Training frameworks: [PyTorch](https://github.com/pytorch/pytorch), [TensorFlow](https://github.com/tensorflow/tensorflow), [JAX](https://github.com/jax-ml/jax)
- Higher-level training: [Lightning](https://github.com/Lightning-AI/pytorch-lightning), [Hugging Face Accelerate](https://github.com/huggingface/accelerate)
- Fine-tuning & adapters: [PEFT](https://github.com/huggingface/peft), [TRL](https://github.com/huggingface/trl)
- Distributed workloads: [Ray](https://github.com/ray-project/ray)
- Track seeds, data versions, hardware, memory, checkpoints, hyperparameters, reproducibility and licensing of training data.

## 4. Generative image, video, audio / Génération multimodale

- Diffusion workflows: [Diffusers](https://github.com/huggingface/diffusers), [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- Image generation interface: [InvokeAI](https://github.com/invoke-ai/InvokeAI)
- Speech synthesis: [Piper](https://github.com/rhasspy/piper), [Coqui TTS](https://github.com/coqui-ai/TTS)
- Audio tooling: [librosa](https://github.com/librosa/librosa), [Demucs](https://github.com/facebookresearch/demucs)
- Evaluate copyright, consent, identity/voice cloning implications, compute cost, watermarking and export rights.

## 5. Advanced vision, OCR and document AI

- Vision library and image processing: [OpenCV](https://github.com/opencv/opencv)
- Detection/segmentation: [Detectron2](https://github.com/facebookresearch/detectron2), [Segment Anything](https://github.com/facebookresearch/segment-anything)
- OCR / document extraction: [Tesseract](https://github.com/tesseract-ocr/tesseract), [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR), [docTR](https://github.com/mindee/doctr)
- Document ingestion: [Unstructured](https://github.com/Unstructured-IO/unstructured)
- Test scanning quality, language support, table extraction, layout and human review; OCR output may contain errors.

## 6. Search, databases and recommendations

- Vector search: [Qdrant](https://github.com/qdrant/qdrant), [Milvus](https://github.com/milvus-io/milvus), [FAISS](https://github.com/facebookresearch/faiss)
- Text + vector search: [OpenSearch](https://github.com/opensearch-project/OpenSearch)
- Recommendations: [RecBole](https://github.com/RUCAIBox/RecBole)
- Measure recall@k, latency, deduplication, tenant isolation, access-controlled retrieval and citation accuracy.

## 7. On-device, mobile and edge AI

- Model format and portability: [ONNX](https://github.com/onnx/onnx), [ONNX Runtime](https://github.com/microsoft/onnxruntime)
- Edge inference: [TensorFlow Lite](https://github.com/tensorflow/tensorflow), [ExecuTorch](https://github.com/pytorch/executorch)
- Apple devices: [MLX](https://github.com/ml-explore/mlx)
- In-browser ML: [Transformers.js](https://github.com/huggingface/transformers.js)
- Validate Android/Windows/macOS targets individually; RAM, quantization, model size, CPU/GPU/NPU, offline functionality and battery use are critical.

## 8. Robotics, reinforcement learning and simulation

- Reinforcement learning: [Stable-Baselines3](https://github.com/DLR-RM/stable-baselines3), [Gymnasium](https://github.com/Farama-Foundation/Gymnasium)
- Robotics foundations: [ROS 2](https://github.com/ros2/ros2), [MuJoCo](https://github.com/google-deepmind/mujoco)
- Prioritize simulation and safe physical-system controls before real-world actuator integration.

## 9. AI product backend, UI and agent protocols

- Python backend: [FastAPI](https://github.com/fastapi/fastapi)
- JS/TS orchestration: [Vercel AI SDK](https://github.com/vercel/ai)
- MCP protocol and examples: [Model Context Protocol](https://github.com/modelcontextprotocol)
- Agent workflow: [LangGraph](https://github.com/langchain-ai/langgraph)
- Build explicit tool allowlists and permission checks. Require user confirmation for destructive or external actions. Treat retrieved documents, website text and tool responses as untrusted instructions.

## 10. Serving, MLOps, LLMOps, reliability

- Model serving: [BentoML](https://github.com/bentoml/BentoML), [vLLM](https://github.com/vllm-project/vllm)
- Tracking and registry: [MLflow](https://github.com/mlflow/mlflow), [Weights & Biases](https://github.com/wandb/wandb)
- Monitoring/observability: [Evidently](https://github.com/evidentlyai/evidently), [Langfuse](https://github.com/langfuse/langfuse)
- Evaluation: [Ragas](https://github.com/explodinggradients/ragas), [DeepEval](https://github.com/confident-ai/deepeval)
- Production reading list: [Awesome Production Machine Learning](https://github.com/EthicalML/awesome-production-machine-learning), [Made With ML](https://github.com/GokuMohandas/Made-With-ML)
- Check security patching, model drift, logs with redaction, deployment rollback, reproducibility, telemetry privacy, cost/latency SLOs, and system ownership.

## 11. Responsible AI and security / Sécurité et gouvernance

- Adversarial prompt testing: [promptfoo](https://github.com/promptfoo/promptfoo), [garak](https://github.com/NVIDIA/garak)
- Privacy-preserving learning references: [Flower](https://github.com/adap/flower)
- Governance: model cards, dataset cards, usage policy, retention, provenance, red-team evaluation, incident response, review by humans when stakes are high.
- Never publish raw customer files, API keys, internal credentials or proprietary datasets in public repos.

## 12. Practical recipes / Recettes prêtes à adapter

| Use case | Suggested minimum stack | Acceptance tests |
|---|---|---|
| FR/MG/EN text classification | scikit-learn baseline -> Transformers as needed -> FastAPI | Per-language precision/recall, confusion matrix, held-out test |
| School document question answering | Authorized PDF parser -> embeddings -> vector store -> LLM | Source citations, access control, abstention when unsupported |
| Offline Android assistant | Small quantized ONNX/TFLite model -> local Flutter/native integration | Real device RAM/latency, no-cloud test, crash-free startup |
| Invoice document extraction | OCR -> schema validation -> human confirmation | Correct totals, no data leakage, malformed image handling |
| Image classification | PyTorch -> ONNX Runtime | Robustness on real images, model size, reproducibility |
| Sales forecast dashboard | pandas -> baseline forecast -> Streamlit | Time-based split, error metrics, downloadable report |
| Customer-support assistant | Knowledge base -> retrieval -> policy guardrails -> constrained tools | Refusal of unauthorized actions, fallback, traceability |
| Voice notes search | Consent -> Whisper -> indexing -> search UI | Word-error rate by language, secure audio retention |

## 13. Ready-to-reuse repository checklist / Checklist de dépôt IA

Each independent project should include:

```text
README.md                 # purpose, install, demo, limits (FR + EN)
LICENSE                   # select and verify allowed use
.gitignore                # exclude secrets, weights and local datasets
.env.example              # placeholders only
requirements.txt          # or pyproject.toml / package.json
src/                      # application code
tests/                    # unit, validation, adversarial regression tests
docs/ARCHITECTURE.md      # data flow, model, interfaces
docs/MODEL_CARD.md        # model/dataset licensing, evaluation, constraints
.github/workflows/ci.yml  # automated checks
```

No automatic fork or model download is implied by this guide. A project is only **ready** after dependencies, unit tests, security review and a real runtime demo are verified.

## 14. Selection by budget / Choisir selon ses moyens

- **Laptop CPU, no GPU:** scikit-learn, tiny OCR/classification, small quantized local LLM; expect limited performance.
- **Mobile offline:** ONNX Runtime / Lite, careful quantization, on-device profiling.
- **GPU available:** PyTorch training, diffusion, larger local models subject to VRAM.
- **Paid APIs permitted:** check provider pricing, data policies, rate limits and fallback.
- **Professional deployment:** budgeting for monitoring, storage, authentication and backups remains necessary even if the model is open-source.


## 15. Practical project delivery / Mise en œuvre pratique

For technology selection, project templates, model/dataset cards, security, deployment and a repository-by-repository roadmap, see **[AI Project Playbook](AI-PROJECT-PLAYBOOK.md)**.
