"""
Ranking Engine: multi-criteria scoring and selection of top papers.
"""

def rank_analyses(analyses, top_n: int):
    """Assign ranks and return the top_n analyses sorted by score descending."""
    sorted_list = sorted(analyses, key=lambda a: a.score, reverse=True)
    for idx, analysis in enumerate(sorted_list[:top_n], start=1):
        analysis.rank = idx
    return sorted_list[:top_n]