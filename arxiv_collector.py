"""
ArXiv Collector: fetch and cache recent AI papers via the ArXiv API.
"""

import arxiv

def fetch_recent_papers(category: str, max_results: int):
    """Fetch recent papers for the given ArXiv category using the official API."""
    client = arxiv.Client(page_size=100, delay_seconds=3, num_retries=3)
    search = arxiv.Search(
        query=f"cat:{category}",
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )
    results = []
    for paper in client.results(search):
        results.append(paper)
    return results