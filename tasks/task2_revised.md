**Goal:** Curate a small, high-quality dataset of "future" papers and their "predecessor" references, ensuring the "future" papers were first published after the model knowledge cutoff.

**Budget:** { gpu_type: "NONE", max_hours: 2.0, max_memory_GB: 8 }

**Output:**
- Core Deliverable: A JSON file `/outputs/curated_dataset.json`.
- Code Deliverables: `src/openreview.py`, `src/arxiv.py`, `src/data_collection.py`.
- Verification Artifacts: A log file `/outputs/curation_log.md`.

**Reference Notebooks:**
- `tasks/OpenReview_Venue_Parser-2.ipynb`
- `tasks/arxiv_api.ipynb`

**Implementation Plan:**

1.  **Create `src/openreview.py`:**
    *   Adapt logic from `OpenReview_Venue_Parser-2.ipynb` to find and parse accepted papers from top-tier conferences (e.g., ICLR 2025).
    *   This module's primary function will be to return a list of candidate paper titles and authors.

2.  **Create `src/arxiv.py`:**
    *   Adapt logic from `arxiv_api.ipynb`.
    *   Create a core function `get_paper_details(title, authors)` that searches arXiv.
    *   **Crucially, this function must retrieve the submission date of the *first version* (v1) of the paper.**

3.  **Create `src/data_collection.py`:**
    *   This script will orchestrate the entire data curation workflow.

**Data Curation Steps (in `data_collection.py`):**

*   **Step 1: Get Candidate Papers from a Top Conference**
    *   Use `openreview.py` to fetch a list of accepted papers from a recent, top-tier 2025 conference.

*   **Step 2: Verify First Publication Date & Filter for "Future" Papers**
    *   For each candidate paper, use `arxiv.py` to find its record.
    *   **Filter out any paper where the first version was published on or before March 2025.**
    *   From the remaining valid papers, select 5-10 to create the "Future Set."

*   **Step 3: Find "Predecessor" Papers (Pre-June 2024)**
    *   For each paper in the "Future Set," use the Semantic Scholar API to get its references.
    *   Filter these references to keep only those published *before* June 2024.

*   **Step 4: Store the Final Dataset**
    *   Save the result to `/outputs/curated_dataset.json`.