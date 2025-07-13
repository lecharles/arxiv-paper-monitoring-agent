#!/usr/bin/env python3
"""
CLI entrypoint for the AI Paper Monitoring Agent.
"""

import os
import sys
import logging
import argparse

import yaml
from dotenv import load_dotenv

from arxiv_collector import fetch_recent_papers
from content_analyzer import analyze_papers
from ranking_engine import rank_analyses
from report_generator import generate_report

def run_pipeline(config: dict, test_mode: bool = False) -> str:
    """Execute the full analysis pipeline: fetch, analyze, rank, and generate report."""
    arxiv_cfg = config.get('arxiv', {})
    ranking_cfg = config.get('ranking', {})
    report_cfg = config.get('report', {})

    category = arxiv_cfg.get('category', 'cs.AI')
    max_results = arxiv_cfg.get('max_results', 100)
    top_n = ranking_cfg.get('top_n', 20)
    output_dir = report_cfg.get('output_dir', 'reports')

    logging.info('Fetching recent papers for category %s (max %d)', category, max_results)
    papers = fetch_recent_papers(category, max_results)
    logging.info('Retrieved %d papers', len(papers))

    analyses = analyze_papers(papers)
    logging.info('%d papers passed relevance filtering', len(analyses))

    ranked = rank_analyses(analyses, top_n)
    logging.info('Selected top %d papers', len(ranked))

    report_path = generate_report(ranked, output_dir)
    logging.info('Report generated at %s', report_path)
    if test_mode:
        print(report_path)
    return report_path

def main():
    parser = argparse.ArgumentParser(description='AI Paper Monitoring Agent')
    parser.add_argument('--run', action='store_true', help='Run full analysis')
    parser.add_argument('--test', action='store_true', help='Dry run for testing')
    args = parser.parse_args()

    # Load environment variables
    load_dotenv()
    # Load YAML configuration
    cfg_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    with open(cfg_path, 'r') as f:
        config = yaml.safe_load(f)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s'
    )

    if args.test:
        logging.info('Running in test (dry-run) mode')
        run_pipeline(config, test_mode=True)
    elif args.run:
        logging.info('Starting full analysis run')
        run_pipeline(config)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()