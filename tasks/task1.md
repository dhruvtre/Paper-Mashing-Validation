Goal: Create the complete project scaffolding and a central configuration file for the Modal application.
Budget: { gpu_type: "NONE", max_hours: 0.5, max_memory_GB: 4 }
Output:
- Core Deliverables: A `run.py` file, an empty `src` directory, and a `/outputs/config.json` file.
- Verification Artifacts: A directory structure matching the specification: `/project/run.py`, `/project/src/`, `/project/outputs/`. A log message confirming the `config.json` was written.
Inputs: None
Guidelines:
- Create a directory structure: `/project` with `run.py` and subdirectories `src` and `outputs`.
- The `run.py` file must initialize a `modal.Stub` named "paper-mashing-mvh".
- The `modal.Image` must be defined to include: `torch==2.4.0`, `torchvision==0.22.1`, `transformers==4.42.4`, `accelerate==0.31.0`, `sentence-transformers==5.0.0`, `scikit-learn==1.5.0`, `pandas==2.2.2`, `matplotlib==3.9.1`, `arxiv==2.1.0`, `requests==2.32.3`, `scipy==1.14.0`, `semanticscholar==0.8.1`, `beautifulsoup4==4.12.3`.
- The `run.py` file must define a `modal.SharedVolume` mounted at `/outputs`.
- Create a primary `@stub.function` that writes a configuration file to `/outputs/config.json`. This config file must contain:
  ```json
  {
    "knowledge_cutoff_date": "2023-01-01",
    "llm_model_name": "mistralai/Mistral-7B-Instruct-v0.3",
    "perplexity_model_name": "gpt2"
  }
  ```
Additional Context: This task establishes the foundational structure and configuration for all other tasks. The inclusion of `semanticscholar` and `beautifulsoup4` is for Task 2's primary and fallback strategies.