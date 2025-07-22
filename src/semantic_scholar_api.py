import requests
import time
import json
from typing import Dict, List, Optional
from datetime import datetime

# Configuration
BASE_URL = "https://api.semanticscholar.org/graph/v1"
DEFAULT_TIMEOUT = 30
DEFAULT_RETRY_DELAY = 2.0
MAX_RETRIES = 3

def make_s2_api_call(endpoint: str, params: dict = None) -> Dict:
    """
    Make a raw API call to Semantic Scholar with retries and rate limiting.
    
    Args:
        endpoint: API endpoint (e.g., 'paper/search', 'paper/{paper_id}')
        params: Query parameters for the request
        
    Returns:
        Dict containing API response data
        
    Raises:
        Exception: If API call fails after retries
    """
    if params is None:
        params = {}
    
    url = f"{BASE_URL}/{endpoint}"
    headers = {"User-Agent": "paper-mashing-validator/1.0 (research use)"}
    
    print(f"[S2 API] Making request to: {endpoint}")
    print(f"[S2 API] Parameters: {params}")
    
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, params=params, headers=headers, timeout=DEFAULT_TIMEOUT)
            
            print(f"[S2 API] Response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"[S2 API] Success: Retrieved data with {len(data.get('data', [data]))} items")
                return data
            elif response.status_code == 429:
                print(f"[S2 API] Rate limited, waiting {DEFAULT_RETRY_DELAY * attempt}s...")
                time.sleep(DEFAULT_RETRY_DELAY * attempt)
            else:
                print(f"[S2 API] HTTP {response.status_code}: {response.text}")
                response.raise_for_status()
                
        except requests.exceptions.RequestException as e:
            print(f"[S2 API] Attempt {attempt}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(DEFAULT_RETRY_DELAY)
            else:
                raise Exception(f"API call failed after {MAX_RETRIES} attempts: {e}")
    
    # Rate limiting between requests
    time.sleep(0.1)  # 100ms to be respectful
    
def search_paper_by_title(title: str) -> Optional[Dict]:
    """
    Search for a paper by title and return the best match.
    
    Args:
        title: Paper title to search for
        
    Returns:
        Dict with paper metadata or None if not found
    """
    print(f"[S2 Search] Searching for paper: '{title[:60]}{'...' if len(title) > 60 else ''}'")
    
    if not title or not title.strip():
        print("[S2 Search] Empty title provided")
        return None
    
    try:
        params = {
            "query": title.strip(),
            "limit": 5,  # Get top 5 to find best match
            "fields": "paperId,title,year,publicationDate,authors,externalIds,publicationTypes,venue"
        }
        
        response_data = make_s2_api_call("paper/search", params)
        
        papers = response_data.get('data', [])
        if not papers:
            print(f"[S2 Search] No papers found for: '{title}'")
            return None
        
        # Find best match (exact or closest title match)
        best_match = None
        title_lower = title.lower().strip()
        
        for paper in papers:
            paper_title = paper.get('title', '').lower().strip()
            
            # Exact match
            if paper_title == title_lower:
                best_match = paper
                print(f"[S2 Search] Exact match found: {paper.get('paperId')}")
                break
            # First partial match as fallback
            elif not best_match and title_lower in paper_title:
                best_match = paper
                print(f"[S2 Search] Partial match found: {paper.get('paperId')}")
        
        if not best_match:
            best_match = papers[0]  # Take first result as fallback
            print(f"[S2 Search] Using first result: {best_match.get('paperId')}")
        
        print(f"[S2 Search] Selected: '{best_match.get('title', 'N/A')[:60]}...' (Year: {best_match.get('year', 'N/A')})")
        return best_match
        
    except Exception as e:
        print(f"[S2 Search] Error searching for '{title}': {e}")
        return None

def get_paper_references(paper_id: str) -> List[Dict]:
    """
    Get the list of papers that this paper references (cites).
    
    Args:
        paper_id: Semantic Scholar paper ID
        
    Returns:
        List of paper dictionaries with reference metadata
    """
    print(f"[S2 References] Getting references for paper: {paper_id}")
    
    if not paper_id or not paper_id.strip():
        print("[S2 References] Empty paper_id provided")
        return []
    
    try:
        params = {
            "fields": "paperId,title,year,publicationDate,authors,externalIds,venue",
            "limit": 100  # Get up to 100 references
        }
        
        endpoint = f"paper/{paper_id.strip()}/references"
        response_data = make_s2_api_call(endpoint, params)
        
        references_data = response_data.get('data', [])
        if not references_data:
            print(f"[S2 References] No references found for paper: {paper_id}")
            return []
        
        # Extract the actual paper data from the reference structure
        references = []
        for ref_item in references_data:
            cited_paper = ref_item.get('citedPaper', {})
            if cited_paper and cited_paper.get('paperId'):
                references.append(cited_paper)
        
        print(f"[S2 References] Found {len(references)} references for paper: {paper_id}")
        
        # Log some sample references
        for i, ref in enumerate(references[:3], 1):
            ref_title = ref.get('title', 'N/A')
            ref_year = ref.get('year', 'N/A')
            print(f"[S2 References]   {i}. '{ref_title[:50]}...' ({ref_year})")
        
        return references
        
    except Exception as e:
        print(f"[S2 References] Error getting references for '{paper_id}': {e}")
        return []

# Test functions
def test_search_known_paper():
    """Test searching for a well-known paper"""
    print("\n=== Testing search_paper_by_title ===")
    
    # Test with a famous paper
    test_title = "Attention Is All You Need"
    result = search_paper_by_title(test_title)
    
    if result:
        print(f"✓ Found paper: {result.get('title')}")
        print(f"  Paper ID: {result.get('paperId')}")
        print(f"  Year: {result.get('year')}")
        return result.get('paperId')
    else:
        print("✗ Failed to find paper")
        return None

def test_get_references(paper_id: str):
    """Test getting references for a paper"""
    print(f"\n=== Testing get_paper_references for {paper_id} ===")
    
    if not paper_id:
        print("No paper ID provided, skipping test")
        return
    
    references = get_paper_references(paper_id)
    
    if references:
        print(f"✓ Found {len(references)} references")
        # Show first few
        for i, ref in enumerate(references[:3], 1):
            print(f"  {i}. {ref.get('title', 'N/A')} ({ref.get('year', 'N/A')})")
    else:
        print("✗ No references found")

def test_api_error_handling():
    """Test error handling with invalid inputs"""
    print("\n=== Testing error handling ===")
    
    # Test empty title
    result = search_paper_by_title("")
    print(f"Empty title result: {result is None}")
    
    # Test invalid paper ID
    refs = get_paper_references("invalid_id_12345")
    print(f"Invalid ID references: {len(refs) == 0}")

if __name__ == '__main__':
    print("Testing Semantic Scholar API functions...")
    
    # Run tests
    paper_id = test_search_known_paper()
    test_get_references(paper_id)
    test_api_error_handling()
    
    print("\nTesting completed!")