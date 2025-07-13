# ArXiv Paper Monitoring Agent

Automate monitoring of ArXiv's AI category, filter and rank new research papers, and generate structured markdown analysis reports.

## Quick Start

1. **Clone repository**:
   ```bash
   git clone https://github.com/lecharles/arxiv-paper-monitoring-agent.git
   cd arxiv-paper-monitoring-agent
   ```

2. **Set up your environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure**:
   - Edit `config.yaml` to adjust parameters as needed.
   - Copy `.env.example` to `.env` and set `OPENAI_API_KEY` if using LLM analysis.

4. **Run a test**:
   ```bash
   python main.py --test
   ```

5. **Generate reports**:
   ```bash
   python main.py --run
   ```

Reports will be written to the `reports/` directory by default.
6. **Schedule automated runs**:
   ```bash
   python scheduler.py
   ```

## Usage

After cloning the repository and activating the virtual environment, you can run the agent and generate reports using these commands:

```bash
# Activate your venv (macOS/Linux)
source venv/bin/activate

# Dry‑run (test mode) without writing reports
python main.py --test

# Full run: fetch, analyze, and generate markdown report
python main.py --run

# Optional flags:
python main.py --from-date YYYY-MM-DD --to-date YYYY-MM-DD --force-refresh

# Schedule periodic monitoring (every 48 hours)
python scheduler.py
```

Generated markdown reports (including the new **Link** column for direct ArXiv URLs) will appear in the `reports/` directory as `ai_papers_analysis_YYYY-MM-DD.md`.
