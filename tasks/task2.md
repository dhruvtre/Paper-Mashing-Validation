Goal: Create a data curation script to collect a set of "future" papers and their "predecessor" references, with robust fallbacks.
Budget: { gpu_type: "NONE", max_hours: 1.5, max_memory_GB: 8 }
Output:
- Core Deliverables: A JSON file `/outputs/future_predecessor_map.json`.
- Verification Artifacts: A log file `/outputs/data_curation.log` detailing the number of papers found and the methods used (e.g., "Semantic Scholar API", "Web Scrape Fallback").
Inputs:
- `/outputs/config.json` (from Task 1)
Guidelines:
- Create `src/data_curator.py` and a corresponding Modal function in `run.py`.
- Load the `knowledge_cutoff_date` from `/outputs/config.json`.
- **Primary Strategy (Semantic Scholar API):**
  1.  Use the `semanticscholar` library to find a set of ~200-300 papers from top AI conferences published *after* the `knowledge_cutoff_date`.
  2.  For each "future paper," retrieve its list of references.
  3.  Filter these references to keep only those published *before* the `knowledge_cutoff_date`.
- **Important: Acknowledge API Limitations.** The Semantic Scholar API has strict rate limits. Your script must handle potential API errors gracefully.
- **Fallback Strategy (Internet Search & Scraping):**
  1.  If the Semantic Scholar API fails or is rate-limited, the agent is authorized to use an alternative strategy. A recommended fallback is to use an internet search engine (e.g., via `requests` and `BeautifulSoup`) to query Google Scholar or similar academic search sites.
  2.  Example query: `site:arxiv.org "cites <future_paper_title>" after:<cutoff_date>`.
  3.  The agent should parse the search results to extract paper titles or arXiv IDs of citing papers.
  4.  The arXiv API can then be used as a reliable secondary source to fetch metadata (like publication dates) for these identified papers to verify they are valid predecessors.
- The final output `/outputs/future_predecessor_map.json` should have the format: `{"future_paper_id_1": ["predecessor_id_A", "predecessor_id_B", ...], "future_paper_id_2": [...]}`.
Additional Context: This task requires resourcefulness. The primary goal is to populate the dataset; the agent should prioritize the Semantic Scholar API but use other internet resources if necessary to achieve the goal.