Goal: Refactor the core idea generation logic from the reference notebook into a modular, configurable script.
Budget: { gpu_type: "NONE", max_hours: 1, max_memory_GB: 8 }
Output:
- Core Deliverables: A Python script `src/idea_generator.py`.
- Verification Artifacts: A log message confirming that the self-test passed successfully.
Inputs:
- `/outputs/config.json` (from Task 1)
- `REFERENCE_MATERIAL`: `World_Model_Idea_Generation_Notebook_1.ipynb`
Guidelines:
- Create `src/idea_generator.py` and a corresponding `@stub.function` in `run.py` to run its self-test.
- **Instruction:** Extract the **exact** prompt templates for both the control ("generate a new research idea") and mashing ("given these two papers...") conditions directly from `World_Model_Idea_Generation_Notebook_1.ipynb`.
- Define two functions: `generate_control_idea(model_name)` and `generate_mashing_idea(model_name, paper1_text, paper2_text)`.
- Implement a `test_generator()` function. It should read the `llm_model_name` from `/outputs/config.json`, initialize the client with that model, call both generation functions with dummy data, and assert that the outputs are non-empty strings.
Additional Context: This task modularizes the core logic from the provided notebook. Adherence to the notebook's prompts is critical for hypothesis validity.