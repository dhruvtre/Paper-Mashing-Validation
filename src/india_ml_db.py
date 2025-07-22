import sqlite3
import json
from typing import List, Dict, Any
import os

class IndiaMLDBAccessor:
    """
    Accessor class for India ML tracker database files containing 
    conference paper data from ICML and ICLR 2025.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.icml_db_path = os.path.join(data_dir, "venues-icml-2025-v2.db")
        self.iclr_db_path = os.path.join(data_dir, "venues-iclr-2025-v3.db")
    
    def _connect_to_db(self, db_path: str) -> sqlite3.Connection:
        """Create a connection to the SQLite database."""
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file not found: {db_path}")
        return sqlite3.connect(db_path)
    
    def get_accepted_papers(self, conference: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve accepted papers from the specified conference database.
        
        Args:
            conference: Either 'icml' or 'iclr'
            limit: Maximum number of papers to retrieve
            
        Returns:
            List of dictionaries containing paper information
        """
        if conference.lower() == 'icml':
            db_path = self.icml_db_path
        elif conference.lower() == 'iclr':
            db_path = self.iclr_db_path
        else:
            raise ValueError("Conference must be either 'icml' or 'iclr'")
        
        conn = self._connect_to_db(db_path)
        cursor = conn.cursor()
        
        try:
            query = """
            SELECT p.title, p.raw_authors, p.id, p.pdf_url, p.accept_type
            FROM papers p
            WHERE p.status = 'accepted'
            LIMIT ?
            """
            
            cursor.execute(query, (limit,))
            rows = cursor.fetchall()
            
            papers = []
            for row in rows:
                title, raw_authors_json, paper_id, pdf_url, accept_type = row
                
                # Parse the JSON authors field
                authors = []
                if raw_authors_json:
                    try:
                        raw_authors = json.loads(raw_authors_json)
                        authors = [author.get('name', '') for author in raw_authors if isinstance(author, dict)]
                    except (json.JSONDecodeError, AttributeError):
                        # Fallback if JSON parsing fails
                        authors = []
                
                paper = {
                    'title': title,
                    'authors': authors,
                    'id': paper_id,
                    'pdf_url': pdf_url,
                    'accept_type': accept_type,
                    'conference': conference.upper()
                }
                papers.append(paper)
            
            return papers
            
        finally:
            conn.close()
    
    def get_paper_stats(self, conference: str) -> Dict[str, int]:
        """
        Get statistics about papers in the database.
        
        Args:
            conference: Either 'icml' or 'iclr'
            
        Returns:
            Dictionary with counts by status
        """
        if conference.lower() == 'icml':
            db_path = self.icml_db_path
        elif conference.lower() == 'iclr':
            db_path = self.iclr_db_path
        else:
            raise ValueError("Conference must be either 'icml' or 'iclr'")
        
        conn = self._connect_to_db(db_path)
        cursor = conn.cursor()
        
        try:
            query = """
            SELECT status, COUNT(*) as count
            FROM papers
            GROUP BY status
            """
            
            cursor.execute(query)
            rows = cursor.fetchall()
            
            stats = {status: count for status, count in rows}
            return stats
            
        finally:
            conn.close()

def get_all_accepted_papers(limit_per_conference: int = 50) -> List[Dict[str, Any]]:
    """
    Convenience function to get accepted papers from both ICML and ICLR.
    
    Args:
        limit_per_conference: Maximum papers to fetch from each conference
        
    Returns:
        Combined list of papers from both conferences
    """
    db_accessor = IndiaMLDBAccessor()
    all_papers = []
    
    for conference in ['icml', 'iclr']:
        try:
            papers = db_accessor.get_accepted_papers(conference, limit_per_conference)
            all_papers.extend(papers)
            print(f"Retrieved {len(papers)} accepted papers from {conference.upper()}")
        except FileNotFoundError:
            print(f"Warning: {conference.upper()} database not found, skipping...")
        except Exception as e:
            print(f"Error retrieving papers from {conference.upper()}: {e}")
    
    return all_papers

if __name__ == '__main__':
    # Example usage
    db_accessor = IndiaMLDBAccessor()
    
    # Get stats for both conferences
    for conference in ['icml', 'iclr']:
        try:
            stats = db_accessor.get_paper_stats(conference)
            print(f"\n{conference.upper()} 2025 Paper Statistics:")
            for status, count in stats.items():
                print(f"  {status}: {count}")
        except FileNotFoundError:
            print(f"{conference.upper()} database not found")
    
    # Get sample of accepted papers
    print("\n--- Sample Accepted Papers ---")
    accepted_papers = get_all_accepted_papers(limit_per_conference=3)
    
    for i, paper in enumerate(accepted_papers, 1):
        print(f"\n{i}. {paper['title']}")
        print(f"   Conference: {paper['conference']}")
        print(f"   Authors: {', '.join(paper['authors'][:3])}{'...' if len(paper['authors']) > 3 else ''}")