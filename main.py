#!/usr/bin/env python3
"""
CLI entrypoint for the AI Paper Monitoring Agent.
"""

import argparse
import sys

from arxiv_collector import fetch_recent_papers
from content_analyzer import filter_and_score
from ranking_engine import rank_papers
from report_generator import generate_report

def main():
    parser = argparse.ArgumentParser(description='AI Paper Monitoring Agent')
    parser.add_argument('--run', action='store_true', help='Run full analysis')
    parser.add_argument('--test', action='store_true', help='Dry run for testing')
    parser.add_argument('--from-date', type=str, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--to-date', type=str, help='End date (YYYY-MM-DD)')
    parser.add_argument('--force-refresh', action='store_true', help='Ignore cache')
    args = parser.parse_args()

    if args.test:
        print('Running in test (dry-run) mode...')
        # TODO: implement dry-run
    elif args.run:
        print('Starting full analysis run...')
        # TODO: orchestrate pipeline steps
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()