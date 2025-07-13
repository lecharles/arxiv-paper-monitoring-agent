"""
Report Generator: format analysis results into structured markdown.
"""

import os
import datetime

from content_analyzer import PaperAnalysis

def generate_report(analyses, output_path: str) -> str:
    """Generate and save a markdown report of the analyses to the output directory."""
    date_str = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = f'ai_papers_analysis_{date_str}.md'
    os.makedirs(output_path, exist_ok=True)
    filepath = os.path.join(output_path, filename)

    # Header and executive summary
    report = [f'# AI Papers Analysis - {date_str}', '', '## Executive Summary', '',
              f'This report covers the top {len(analyses)} AI papers from ArXiv recent submissions.', '']

    # Top papers table
    report.append('## Top Papers')
    report.append('')
    report.append('| Rank | Title | Grade | Relevance |')
    report.append('|------|-------|-------|-----------|')
    for a in analyses:
        title_short = (a.title[:50] + '...') if len(a.title) > 50 else a.title
        report.append(f'| {a.rank} | {title_short} | {a.grade}/10 | {a.relevance} |')

    # Detailed analysis
    report.extend(['', '## Detailed Analysis', ''])
    for a in analyses:
        report.extend([
            f'### {a.rank}. {a.title}',
            f'**ArXiv ID**: [{a.arxiv_id}]({a.url})',
            '',
            f'- **Description**: {a.description}',
            f'- **Relevance**: {a.relevance}',
            '- **Top 3 Use Cases**:',
            f'  1. {a.use_cases[0]}',
            f'  2. {a.use_cases[1]}',
            f'  3. {a.use_cases[2]}',
            f'- **Business Problems Solved**: {a.business_problems}',
            f'- **Business Applications**: {a.business_applications}',
            f'- **Grade**: {a.grade}/10',
            f'- **Justification**: {a.justification}',
            '', '---', ''
        ])

    # Write to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))

    return filepath