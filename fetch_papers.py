from __future__ import unicode_literals, print_function
import arxiv
from datetime import datetime, timedelta
from typing import List, Dict
from config import KEYWORDS, MAX_RESULTS

def fetch_recent_papers(keywords: List[str], days: int = 7) -> List[Dict[str, str]]:
    """
    Fetch recent papers from arXiv based on given keywords and time window.

    Args:
        keywords (List[str]): A list of keyword queries for arXiv.
        days (int): Number of days to look back from now.

    Returns:
        List[Dict[str, str]]: A list of dictionaries with paper info (title, link, abstract, date).
    """
    current_date = datetime.now()
    one_week_ago = current_date - timedelta(days=days)
    
    # Format dates for arXiv API
    start_date = '{d.year}{d.month:02d}{d.day:02d}'.format(d=one_week_ago)
    end_date = '{d.year}{d.month:02d}{d.day:02d}'.format(d=current_date)
    
    papers = []
    for kw in keywords:
        search_query = f"abs:{kw} AND submittedDate:[{start_date} TO {end_date}]"
        
        search = arxiv.Search(
            query=search_query,
            max_results=MAX_RESULTS,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        for result in search.results():
            paper_info = {
                "title": result.title,
                "link": result.entry_id,
                "abstract": result.summary,
                "date": '{d.year}{d.month:02d}{d.day:02d}'.format(d=result.published)
            }
            papers.append(paper_info)
    return papers

def print_papers(papers: List[Dict[str, str]]) -> None:
    """
    Print the papers in a readable format.

    Args:
        papers (List[Dict[str, str]]): The list of papers to print.
    """
    print("Here is the list of new papers:\n")
    for paper in papers:
        print(f"Title: {paper['title']}")
        print(f"Link: {paper['link']}")
        print(f"Date: {paper['date']}")
        print(f"Abstract: {paper['abstract']}\n")

if __name__ == "__main__":
    retrieved_papers = fetch_recent_papers(KEYWORDS)
    print_papers(retrieved_papers)
