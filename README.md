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