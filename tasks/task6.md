Goal: Create a reusable module for generating text embeddings.
Budget: { gpu_type: "NONE", max_hours: 0.5, max_memory_GB: 16 }
Output:
- Core Deliverables: A Python script `src/embedder.py`.
- Verification Artifacts: A log message confirming the self-test passed, showing the shape of the output embeddings.
Inputs: None
Guidelines:
- Create `src/embedder.py` and a `@stub.function` in `run.py` to run its self-test.
- The script should load a pre-trained `sentence-transformers` model, `all-MiniLM-L6-v2`.
- Define `get_embeddings(texts: list[str])` which returns embeddings as a NumPy array.
- Implement a `test_embedder()` function that embeds two sample sentences and asserts the output shape is `(2, 384)`.
Additional Context: This shared module will be used by the similarity evaluation task.