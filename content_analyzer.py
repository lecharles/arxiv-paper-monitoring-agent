"""
Content Analyzer: filter papers by keyword relevance and extract analysis metrics.
"""

from dataclasses import dataclass
from typing import List

@dataclass
class PaperAnalysis:
    """Data structure for storing analysis results for a single paper."""
    rank: int = 0
    title: str = ""
    date: str = ""             # Publication date (YYYY-MM-DD)
    description: str = ""
    relevance: str = ""
    use_cases: List[str] = None
    business_problems: str = ""
    business_applications: str = ""
    grade: int = 0
    justification: str = ""
    arxiv_id: str = ""
    url: str = ""
    score: int = 0

# Default AI keywords for filtering and scoring
AI_KEYWORDS = [
    # AI Agents
    'agent', 'multi-agent', 'autonomous agent', 'agent architecture',
    'agentic', 'agent-based', 'reasoning agent',
    # Prompt Engineering
    'prompt engineering', 'prompt design', 'prompt optimization',
    'in-context learning', 'few-shot', 'chain-of-thought', 'prompt tuning',
    # LLMs
    'large language model', 'llm', 'transformer', 'foundation model',
    'language model', 'gpt', 'bert', 'generative model',
    # Context Engineering
    'context length', 'context window', 'long context',
    'retrieval-augmented', 'rag', 'context engineering',
    # Additional areas
    'fine-tuning', 'rlhf', 'reinforcement learning from human feedback',
    'multimodal', 'vision-language', 'alignment', 'safety',
    'reasoning', 'planning', 'tool use', 'function calling',
    'evaluation', 'benchmark'
]

def is_relevant_paper(paper) -> bool:
    text = f"{paper.title} {paper.summary}".lower()
    return any(keyword.lower() in text for keyword in AI_KEYWORDS)

def calculate_relevance_score(paper) -> int:
    title_text = paper.title.lower()
    summary_text = paper.summary.lower()
    score = 0
    for keyword in AI_KEYWORDS:
        kw = keyword.lower()
        if kw in title_text:
            score += 3
        elif kw in summary_text:
            score += 1
    return score

def analyze_papers(papers) -> List[PaperAnalysis]:
    """Filter, score, and perform full analysis on a list of ArXiv papers."""
    analyses: List[PaperAnalysis] = []
    for paper in papers:
        if not is_relevant_paper(paper):
            continue

        score = calculate_relevance_score(paper)
        analysis = PaperAnalysis(
            title=paper.title,
            date=paper.published.date().isoformat(),
            description=_extract_description(paper.summary),
            relevance=_assess_relevance(paper),
            use_cases=_extract_use_cases(paper),
            business_problems=_identify_business_problems(paper),
            business_applications=_identify_business_applications(paper),
            grade=_calculate_grade(paper),
            justification=_grade_justification(paper, _calculate_grade(paper)),
            arxiv_id=paper.entry_id.split('/')[-1],
            url=paper.entry_id,
            score=score,
        )
        analyses.append(analysis)
    return analyses

def _extract_description(abstract: str) -> str:
    sentences = abstract.split('.')[:3]
    return '. '.join(s.strip() for s in sentences if s).strip() + '.'

def _assess_relevance(paper) -> str:
    text = f"{paper.title} {paper.summary}".lower()
    if any(w in text for w in ['agent', 'multi-agent', 'agentic']):
        return "Advances AI agent architectures and autonomous system design"
    if any(w in text for w in ['prompt', 'in-context', 'few-shot']):
        return "Improves prompt engineering techniques and model interaction"
    if any(w in text for w in ['context', 'memory', 'retrieval']):
        return "Enhances context handling and memory management in AI systems"
    if any(w in text for w in ['reasoning', 'planning', 'tool']):
        return "Develops advanced reasoning and planning capabilities"
    return "Contributes to foundational AI research and development"

def _extract_use_cases(paper) -> List[str]:
    text = f"{paper.title} {paper.summary}".lower()
    cases = []
    if 'dialogue' in text or 'conversation' in text:
        cases.append("Conversational AI and chatbot enhancement")
    if 'code' in text or 'programming' in text:
        cases.append("Automated code generation and software development")
    if 'planning' in text or 'decision' in text:
        cases.append("Decision support systems and strategic planning")
    if 'vision' in text or 'multimodal' in text:
        cases.append("Multimodal AI applications (vision + language)")
    if 'search' in text or 'retrieval' in text:
        cases.append("Enhanced search and information retrieval")
    # pad to at least 3 items
    defaults = ["Enterprise AI automation", "R&D acceleration", "Educational AI tutoring"]
    for d in defaults:
        if len(cases) >= 3:
            break
        if d not in cases:
            cases.append(d)
    return cases[:3]

def _identify_business_problems(paper) -> str:
    text = f"{paper.title} {paper.summary}".lower()
    if 'efficien' in text or 'optimiza' in text:
        return "Operational efficiency and process optimization challenges"
    if 'scale' in text or 'scalab' in text:
        return "Scalability issues in AI deployment"
    if 'cost' in text or 'resource' in text:
        return "High computational cost and resource constraints"
    return "Complex decision-making and automation requirements"

def _identify_business_applications(paper) -> str:
    text = f"{paper.title} {paper.summary}".lower()
    if 'customer' in text or 'service' in text:
        return "Customer service automation and personalization platforms"
    if 'analytics' in text or 'analysis' in text:
        return "Business intelligence and predictive analytics"
    if 'content' in text or 'generation' in text:
        return "Automated content creation and marketing"
    return "Enterprise AI integration and workflow automation"

def _calculate_grade(paper) -> int:
    text = f"{paper.title} {paper.summary}".lower()
    score = 5
    if any(w in text for w in ['novel', 'breakthrough', 'significant']):
        score += 2
    if any(w in text for w in ['efficient', 'scalable', 'practical']):
        score += 1
    if any(w in text for w in ['benchmark', 'evaluation', 'comparison']):
        score += 1
    if len(paper.authors) > 5:
        score += 1
    return min(10, max(1, score))

def _grade_justification(paper, grade: int) -> str:
    if grade >= 8:
        return "High-impact research with significant practical applications and novel contributions."
    if grade >= 6:
        return "Solid research contribution with clear practical value and rigorous methodology."
    return "Foundational research with potential long-term impact; may require additional development."