import time
import requests
import feedparser
from datetime import datetime
from urllib.parse import quote

def make_search_query(title: str, authors: list[str]) -> str:
    """Builds an arXiv search query from title and authors."""
    query_parts = []
    
    # Process title
    if title:
        # Exact title search
        query_parts.append(f'ti:"{title}"')

    # Process authors
    if authors:
        # Search for each author
        author_query = " AND ".join([f'au:"{author}"' for author in authors])
        query_parts.append(f"({author_query})")

    return " AND ".join(query_parts)

def make_arxiv_call(search_query: str, max_results: int = 1, retries: int = 3, backoff: float = 3.0) -> str:
    """Makes an HTTP call to the arXiv API."""
    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": search_query,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "ascending" # Get the oldest version first
    }
    url = f"{base_url}?{'&'.join(f'{k}={quote(str(v))}' for k, v in params.items())}"
    
    headers = {"User-Agent": "arxiv-query-tool/1.0 (Python; research use)"}

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            time.sleep(backoff) # Respect rate limits
            return response.text
        except Exception as e:
            if attempt < retries:
                time.sleep(backoff)
            else:
                raise e

def parse_arxiv_feed(feed_text: str) -> dict | None:
    """Parses the arXiv feed and returns the first paper's details."""
    feed = feedparser.parse(feed_text)
    if not feed.entries:
        return None

    entry = feed.entries[0]
    
    # The 'published' field contains the date of the first version (v1)
    published_date_str = entry.published
    published_date = datetime.fromisoformat(published_date_str.replace('Z', '+00:00'))

    paper = {
        "id": entry.id.split('/')[-1],
        "title": entry.title.replace('\n', ' ').strip(),
        "summary": entry.summary.replace('\n', ' ').strip(),
        "authors": [author.name for author in entry.authors],
        "published_date": published_date,
        "pdf_url": entry.link.replace('http', 'https').replace('abs', 'pdf')
    }
    return paper

def get_paper_details(title: str, authors: list[str]) -> dict | None:
    """
    Queries arXiv for a paper by title and authors and returns its details,
    including the v1 publication date.
    """
    search_query = make_search_query(title, authors)
    if not search_query:
        return None

    try:
        raw_feed = make_arxiv_call(search_query)
        return parse_arxiv_feed(raw_feed)
    except Exception as e:
        print(f"An error occurred while fetching from arXiv: {e}")
        return None

if __name__ == '__main__':
    # Example usage:
    test_title = "Attention Is All You Need"
    test_authors = ["Ashish Vaswani", "Noam Shazeer"]
    
    print(f"Searching for paper with title: '{test_title}' and authors: {test_authors}")
    
    paper_details = get_paper_details(test_title, test_authors)
    
    if paper_details:
        print("\nSuccessfully found paper:")
        print(f"  ID: {paper_details['id']}")
        print(f"  Title: {paper_details['title']}")
        print(f"  Published Date (v1): {paper_details['published_date'].strftime('%Y-%m-%d')}")
        print(f"  Authors: {', '.join(paper_details['authors'])}")
    else:
        print("\nCould not find the specified paper on arXiv.")
