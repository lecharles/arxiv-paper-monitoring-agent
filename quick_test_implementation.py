# AI Paper Agent - Quick Test Implementation
# This is a minimal working version for immediate testing

import arxiv
import re
import json
import datetime
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class PaperAnalysis:
    rank: int
    title: str
    description: str
    relevance: str
    use_cases: List[str]
    business_problems: str
    business_applications: str
    grade: int
    justification: str
    arxiv_id: str
    url: str

class AIArxivAgent:
    def __init__(self):
        self.client = arxiv.Client(page_size=100, delay_seconds=3, num_retries=3)
        
        # Keywords for filtering relevant papers
        self.ai_keywords = [
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
            'context length', 'context window', 'long context', 'retrieval-augmented',
            'rag', 'context engineering', 'memory', 'context management',
            
            # Additional relevant areas
            'fine-tuning', 'rlhf', 'reinforcement learning from human feedback',
            'multimodal', 'vision-language', 'alignment', 'safety',
            'reasoning', 'planning', 'tool use', 'function calling',
            'evaluation', 'benchmark'
        ]
    
    def fetch_recent_papers(self, max_results: int = 200) -> List[arxiv.Result]:
        """Fetch recent AI papers from ArXiv"""
        search = arxiv.Search(
            query="cat:cs.AI",  # AI category
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )
        
        papers = []
        for paper in self.client.results(search):
            papers.append(paper)
            
        return papers
    
    def is_relevant_paper(self, paper: arxiv.Result) -> bool:
        """Check if paper is relevant based on keywords"""
        text_to_check = f"{paper.title} {paper.summary}".lower()
        
        for keyword in self.ai_keywords:
            if keyword.lower() in text_to_check:
                return True
        return False
    
    def calculate_relevance_score(self, paper: arxiv.Result) -> float:
        """Calculate relevance score based on keyword matches"""
        text_to_check = f"{paper.title} {paper.summary}".lower()
        score = 0
        
        # Weight title matches higher
        for keyword in self.ai_keywords:
            if keyword.lower() in paper.title.lower():
                score += 3
            elif keyword.lower() in paper.summary.lower():
                score += 1
                
        return score
    
    def analyze_paper(self, paper: arxiv.Result, rank: int) -> PaperAnalysis:
        """Analyze a single paper and extract insights"""
        
        # Basic analysis (in real implementation, this could use LLM APIs)
        description = self.extract_description(paper.summary)
        relevance = self.assess_relevance(paper)
        use_cases = self.extract_use_cases(paper)
        business_problems = self.identify_business_problems(paper)
        business_applications = self.identify_business_applications(paper)
        grade = self.calculate_grade(paper)
        justification = self.grade_justification(paper, grade)
        
        return PaperAnalysis(
            rank=rank,
            title=paper.title,
            description=description,
            relevance=relevance,
            use_cases=use_cases,
            business_problems=business_problems,
            business_applications=business_applications,
            grade=grade,
            justification=justification,
            arxiv_id=paper.entry_id.split('/')[-1],
            url=paper.entry_id
        )
    
    def extract_description(self, abstract: str) -> str:
        """Extract key description from abstract"""
        sentences = abstract.split('.')[:3]  # First 3 sentences
        return '. '.join(sentences).strip() + '.'
    
    def assess_relevance(self, paper: arxiv.Result) -> str:
        """Assess why this paper is relevant"""
        text = f"{paper.title} {paper.summary}".lower()
        
        if any(word in text for word in ['agent', 'multi-agent', 'agentic']):
            return "Advances AI agent capabilities and autonomous system design"
        elif any(word in text for word in ['prompt', 'in-context', 'few-shot']):
            return "Improves prompt engineering techniques and model interaction methods"
        elif any(word in text for word in ['context', 'memory', 'retrieval']):
            return "Enhances context handling and memory management in AI systems"
        elif any(word in text for word in ['reasoning', 'planning', 'tool']):
            return "Develops advanced reasoning and planning capabilities"
        else:
            return "Contributes to fundamental AI research and development"
    
    def extract_use_cases(self, paper: arxiv.Result) -> List[str]:
        """Extract potential use cases"""
        text = f"{paper.title} {paper.summary}".lower()
        use_cases = []
        
        if 'conversation' in text or 'dialogue' in text:
            use_cases.append("Conversational AI and chatbot enhancement")
        if 'code' in text or 'programming' in text:
            use_cases.append("Automated code generation and software development")
        if 'reasoning' in text or 'planning' in text:
            use_cases.append("Decision support systems and strategic planning")
        if 'multimodal' in text or 'vision' in text:
            use_cases.append("Multimodal AI applications (vision + language)")
        if 'retrieval' in text or 'search' in text:
            use_cases.append("Enhanced search and information retrieval")
        
        # Ensure we have at least 3 use cases
        while len(use_cases) < 3:
            default_cases = [
                "Enterprise AI automation",
                "Research and development acceleration",
                "Educational AI tutoring systems"
            ]
            for case in default_cases:
                if case not in use_cases:
                    use_cases.append(case)
                    break
        
        return use_cases[:3]
    
    def identify_business_problems(self, paper: arxiv.Result) -> str:
        """Identify business problems this could solve"""
        text = f"{paper.title} {paper.summary}".lower()
        
        if 'efficiency' in text or 'optimization' in text:
            return "Operational efficiency and process optimization challenges"
        elif 'scaling' in text or 'scale' in text:
            return "Scalability issues in AI deployment and management"
        elif 'cost' in text or 'resource' in text:
            return "High computational costs and resource management"
        else:
            return "Complex decision-making and automation requirements"
    
    def identify_business_applications(self, paper: arxiv.Result) -> str:
        """Identify potential business applications"""
        text = f"{paper.title} {paper.summary}".lower()
        
        if 'customer' in text or 'service' in text:
            return "Customer service automation and personalization platforms"
        elif 'analysis' in text or 'analytics' in text:
            return "Business intelligence and predictive analytics tools"
        elif 'content' in text or 'generation' in text:
            return "Content creation and marketing automation systems"
        else:
            return "Enterprise AI platform integration and workflow automation"
    
    def calculate_grade(self, paper: arxiv.Result) -> int:
        """Calculate grade from 1-10"""
        score = 5  # Base score
        
        text = f"{paper.title} {paper.summary}".lower()
        
        # Positive indicators
        if any(word in text for word in ['novel', 'breakthrough', 'significant']):
            score += 2
        if any(word in text for word in ['efficient', 'scalable', 'practical']):
            score += 1
        if any(word in text for word in ['evaluation', 'benchmark', 'comparison']):
            score += 1
        if len(paper.authors) > 5:  # Large research team
            score += 1
            
        return min(10, max(1, score))
    
    def grade_justification(self, paper: arxiv.Result, grade: int) -> str:
        """Provide justification for the grade"""
        if grade >= 8:
            return "High-impact research with significant practical applications and novel methodological contributions. Strong potential for industry adoption."
        elif grade >= 6:
            return "Solid research contribution with clear practical value. Addresses important challenges in current AI development."
        else:
            return "Foundational research with potential long-term impact. May require further development for practical application."
    
    def generate_report(self, analyses: List[PaperAnalysis]) -> str:
        """Generate markdown report"""
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        report = f"""# AI Papers Analysis - {current_date}

## Executive Summary

This report analyzes the top {len(analyses)} most relevant AI papers from ArXiv's recent submissions. Key trends include:
- Continued advancement in AI agent architectures and autonomous systems
- Growing focus on prompt engineering and context optimization techniques  
- Enhanced reasoning and planning capabilities in large language models
- Practical applications in enterprise automation and decision support

## Top {len(analyses)} Papers

| Rank | Title | Grade | Key Innovation |
|------|-------|-------|----------------|
"""
        
        # Add table rows
        for analysis in analyses:
            title_short = analysis.title[:60] + "..." if len(analysis.title) > 60 else analysis.title
            report += f"| {analysis.rank} | {title_short} | {analysis.grade}/10 | {analysis.relevance[:50]}... |\n"
        
        report += "\n## Detailed Analysis\n\n"
        
        # Add detailed analysis for each paper
        for analysis in analyses:
            report += f"""### {analysis.rank}. {analysis.title}

**ArXiv ID**: [{analysis.arxiv_id}]({analysis.url})

- **Description**: {analysis.description}
- **Relevance**: {analysis.relevance}
- **Top 3 Use Cases**: 
  1. {analysis.use_cases[0]}
  2. {analysis.use_cases[1]}
  3. {analysis.use_cases[2]}
- **Business Problems Solved**: {analysis.business_problems}
- **Business Applications**: {analysis.business_applications}
- **Grade**: {analysis.grade}/10
- **Justification**: {analysis.justification}

---

"""
        
        return report
    
    def run_analysis(self, max_papers: int = 200, top_n: int = 20) -> str:
        """Run the complete analysis pipeline"""
        print("🔍 Fetching recent papers from ArXiv...")
        papers = self.fetch_recent_papers(max_papers)
        print(f"📄 Found {len(papers)} papers")
        
        print("🎯 Filtering relevant papers...")
        relevant_papers = [p for p in papers if self.is_relevant_paper(p)]
        print(f"✅ {len(relevant_papers)} relevant papers identified")
        
        print("📊 Calculating relevance scores...")
        scored_papers = [(p, self.calculate_relevance_score(p)) for p in relevant_papers]
        scored_papers.sort(key=lambda x: x[1], reverse=True)
        
        print(f"🏆 Analyzing top {top_n} papers...")
        top_papers = scored_papers[:top_n]
        
        analyses = []
        for i, (paper, score) in enumerate(top_papers, 1):
            analysis = self.analyze_paper(paper, i)
            analyses.append(analysis)
            print(f"  ✓ Analyzed paper {i}: {paper.title[:50]}...")
        
        print("📝 Generating report...")
        report = self.generate_report(analyses)
        
        # Save report
        filename = f"ai_papers_analysis_{datetime.datetime.now().strftime('%Y-%m-%d')}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"💾 Report saved as: {filename}")
        return report

def main():
    """Quick test function"""
    agent = AIArxivAgent()
    
    print("🤖 AI ArXiv Agent - Quick Test")
    print("=" * 50)
    
    try:
        # Run analysis with smaller numbers for quick testing
        report = agent.run_analysis(max_papers=50, top_n=10)
        
        print("\n✅ Analysis complete!")
        print("\n📋 Report Preview:")
        print("-" * 50)
        print(report[:1000] + "...")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

# Requirements for this script:
# pip install arxiv pandas python-dateutil