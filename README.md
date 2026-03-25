# ClearPath Health

**Prior Authorization Efficiency Benchmarking & Research Institute**

ClearPath Health collects, analyzes, and publishes the first-ever cross-payer benchmarking of prior authorization (PA) efficiency using CMS-mandated transparency data.

## The Problem

Prior authorization costs the U.S. healthcare system ~$19.7 billion annually. 82% of PA denials are overturned on appeal — meaning billions are wasted on double-processing that produces the same outcome. Physicians spend 16+ hours/week on PA paperwork. 78% of patients abandon treatment after a denial.

## The Opportunity

The CMS Interoperability and Prior Authorization Final Rule (CMS-0057-F) requires payers to publicly report PA metrics starting March 31, 2026. ClearPath Health is the first independent organization to collect this data across all major payers, normalize it, and publish actionable analysis.

## What We Produce

- **Annual Benchmarking Report** — Cross-payer comparison of denial rates, turnaround times, and appeal outcomes
- **Efficiency Leaders Recognition** — Highlighting payers with best practices worth emulating
- **Compliance Monitoring** — Tracking which payers published on time with complete data
- **Patient Guides** — Plain-language resources about PA rights and appeal success rates

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/jerrywang123454321-maker/clearpath-health.git
cd clearpath-health

# 2. Create a virtual environment (keeps project libraries separate)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create the database
python scripts/setup_db.py
```

## Project Structure

```
├── src/clearpath/       # Source code
│   ├── config.py        # Project settings
│   ├── database.py      # Database connection
│   ├── collectors/      # Data collection from payer websites
│   ├── analysis/        # Data analysis and benchmarking
│   └── reports/         # Report generation
├── db/schema.sql        # Database table definitions
├── data/                # Raw and processed data
├── tests/               # Automated tests
└── scripts/             # Utility scripts
```

## Status

**Pre-launch.** Building data collection infrastructure ahead of the March 31, 2026 CMS reporting deadline.

## License

MIT — see [LICENSE](LICENSE) for details.
