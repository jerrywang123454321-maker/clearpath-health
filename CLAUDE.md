# CLAUDE.md — Project Rules for AI-Assisted Development
# =====================================================
# This file is automatically read by Claude Code at the start
# of every session. It tells Claude HOW to work on this project.
# Think of it as the "constitution" for AI development on ClearPath Health.
#
# JERRY: You can edit this file anytime to change how Claude behaves.
# If Claude ever does something you don't like, add a rule here.

## Project Overview
- **Project:** ClearPath Health — Prior Authorization Efficiency Benchmarking
- **Owner:** Jerry Wang (incoming MS1, Baylor College of Medicine Houston)
- **Language:** Python 3.11+
- **Database:** SQLite (will migrate to PostgreSQL when needed)
- **Status:** Pre-launch, building data collection and analysis infrastructure

## GOLDEN RULES (never break these)

1. **COMMIT EARLY AND OFTEN.** After every meaningful change, remind Jerry to commit.
   Never let more than ~30 minutes of work go uncommitted.

2. **MAX 200 LINES PER FILE.** If a file approaches 200 lines, split it into smaller
   modules. No exceptions. This prevents the "balloon" problem.

3. **ONE MODULE = ONE JOB.** Each .py file does exactly one thing. If you're tempted
   to add a second responsibility, make a new file instead.

4. **TEACHING-LEVEL COMMENTS.** Jerry is learning Python. Every file must include:
   - A top-of-file block explaining WHAT this file does and WHY it exists
   - Comments on every function explaining what it does in plain English
   - Line-level comments on anything that isn't obvious to a beginner
   - Explain Python concepts inline (what is a dict? what does "import" do? etc.)
   - Use analogies and real-world comparisons when helpful
   - When introducing a new concept for the FIRST time, explain it thoroughly.
     In later files, a brief reminder is fine.

5. **NO CLEVER CODE.** Write the simplest, most readable version. If there's a
   "Pythonic" one-liner and a 5-line version a beginner can read, use the 5-line version.
   Jerry can learn the shortcuts later.

6. **NEVER STORE SECRETS IN CODE.** API keys, passwords, etc. go in .env files
   (which are in .gitignore and never uploaded to GitHub).

## File Structure Rules

```
Med School Project/
├── CLAUDE.md              ← You are here (AI development rules)
├── README.md              ← Project description for GitHub visitors
├── pyproject.toml         ← Python project configuration
├── requirements.txt       ← List of Python libraries needed
├── .gitignore             ← Files git should never track
│
├── db/
│   └── schema.sql         ← Database table definitions (the blueprint)
│
├── src/clearpath/          ← ALL source code lives here
│   ├── __init__.py        ← Makes this folder a Python "package"
│   ├── config.py          ← Settings (database path, etc.)
│   ├── database.py        ← Database connection and setup
│   │
│   ├── collectors/        ← Code that COLLECTS data from payer websites
│   │   ├── __init__.py
│   │   ├── base.py        ← Shared collector logic
│   │   └── manual.py      ← Manual data entry tool
│   │
│   ├── analysis/          ← Code that ANALYZES collected data
│   │   ├── __init__.py
│   │   ├── benchmarks.py  ← Compare payers against each other
│   │   └── compliance.py  ← Check if payers followed CMS rules
│   │
│   └── reports/           ← Code that GENERATES reports and charts
│       ├── __init__.py
│       └── generator.py   ← Build the annual report
│
├── data/
│   ├── raw/               ← Unmodified data straight from payer websites
│   └── processed/         ← Cleaned and normalized data ready for analysis
│
├── tests/                 ← Automated tests (verify code works correctly)
│   └── __init__.py
│
└── scripts/               ← Utility scripts you run manually
    └── setup_db.py        ← Creates the database from schema.sql
```

## When adding a new file:
1. Decide which folder it belongs in based on what it DOES
2. Add it to the structure diagram above (keep this current!)
3. Start with the teaching-level header comment block
4. Keep it under 200 lines

## Code Style
- Use `snake_case` for variables and functions (like_this, not likeThis)
- Use `PascalCase` for classes (LikeThis)
- Use ALL_CAPS for constants (LIKE_THIS)
- Use type hints on function signatures (these help editors catch bugs)
- Use f-strings for string formatting (explained in code when first used)

## Git Practices
- Commit messages should be descriptive: "Add payer data model" not "update"
- One logical change per commit
- Always run tests before committing (once we have tests)
- Never force-push to main branch

## Dependencies
- Keep dependencies minimal — every library added is a future maintenance burden
- Core: sqlite3 (built-in), requests, beautifulsoup4, pandas
- Analysis: matplotlib, plotly
- Later: selenium (for JavaScript-heavy payer sites)
- Document WHY each dependency is needed in requirements.txt
