# ====================================================================
# config.py — Project Settings and Configuration
#
# WHAT IS THIS FILE?
# This file stores all the "settings" for the ClearPath Health project
# in one central place. Things like: where is the database file? What
# year of data are we collecting? What's the project root folder?
#
# WHY ONE FILE FOR SETTINGS?
# Imagine if your database path was written in 10 different files.
# If you ever moved the database, you'd have to find and change it
# in all 10 places. With this config file, you change it ONCE here,
# and every other file reads it from here.
#
# ANALOGY: This is like the "Settings" app on your phone. All your
# preferences live in one place, and every app checks there.
# ====================================================================

# ====================================================================
# WHAT IS "IMPORT"?
# Python doesn't come with every ability built in. "import" loads
# extra tools (called "modules" or "libraries") so Python can do
# more things. It's like downloading an app to your phone.
#
# "from X import Y" means: from the module named X, grab just the
# specific tool named Y. You don't need the whole module — just
# that one piece.
#
# "pathlib" is a built-in Python module (no need to install it)
# that helps work with file paths. "Path" is a tool inside it
# that represents a location on your computer (like a file or folder).
# ====================================================================
from pathlib import Path


# ====================================================================
# PROJECT PATHS
#
# These variables store the locations of important folders.
# Using Path objects instead of plain text strings means Python
# handles differences between Windows (\) and Mac/Linux (/)
# automatically — you never have to worry about slash direction.
# ====================================================================

# __file__ is a special Python variable that contains the path to
# THIS file (config.py). We use it to figure out where the project
# root is, relative to where this file sits.
#
# .resolve() turns a relative path into an absolute one
#   (e.g., "../data" becomes "C:/Users/jerry/Med School Project/data")
#
# .parent gets the folder CONTAINING this file:
#   - First .parent = src/clearpath/ (the folder config.py is in)
#   - Second .parent = src/ (one level up)
#   - Third .parent = Med School Project/ (the project root!)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Now we can define every other path relative to the project root.
# The "/" operator on Path objects joins path segments together.
# So PROJECT_ROOT / "data" / "raw" becomes something like:
#   "C:/Users/jerry/Med School Project/data/raw"
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
DB_DIR = PROJECT_ROOT / "db"

# Where the SQLite database file will live.
# This file gets CREATED when you run scripts/setup_db.py.
# It's in .gitignore so it won't be uploaded to GitHub
# (because it might contain real data).
DATABASE_PATH = DB_DIR / "clearpath.db"

# Where the schema.sql file is (the blueprint for the database).
SCHEMA_PATH = DB_DIR / "schema.sql"


# ====================================================================
# DATA COLLECTION SETTINGS
# ====================================================================

# Which year of data are we currently collecting?
# CMS requires payers to report Calendar Year data.
# The first reporting year is 2025 (reported by March 31, 2026).
CURRENT_REPORTING_YEAR = 2025

# The CMS deadline for payers to publish their metrics.
# March 31 of the year AFTER the reporting year.
CMS_REPORTING_DEADLINE = "2026-03-31"


# ====================================================================
# PAYER TYPES
#
# These are the categories of payers covered by the CMS rule.
# We define them here as a "dictionary" (dict) so we can use the
# short codes in the database but display the full names to humans.
#
# WHAT IS A DICTIONARY (dict)?
# A dict is a collection of key-value pairs. Think of it like a
# real dictionary: you look up a WORD (the key) and get its
# DEFINITION (the value).
#
# In Python, dicts use curly braces {} and colons:
#   { key: value, another_key: another_value }
# ====================================================================
PAYER_TYPES = {
    "MA": "Medicare Advantage",
    "Medicaid": "Medicaid / CHIP Fee-for-Service",
    "CHIP": "Children's Health Insurance Program",
    "QHP": "Qualified Health Plan (Marketplace)",
}

# The 8 metrics CMS requires payers to report, with human-readable names.
# This dict maps our database codes to plain English descriptions.
METRIC_TYPES = {
    "std_approved_pct": "Standard PA Requests Approved (%)",
    "std_denied_pct": "Standard PA Requests Denied (%)",
    "std_appeal_approved_pct": "Standard Denials Approved on Appeal (%)",
    "ext_approved_pct": "Approved After Timeframe Extension (%)",
    "exp_approved_pct": "Expedited PA Requests Approved (%)",
    "exp_denied_pct": "Expedited PA Requests Denied (%)",
    "avg_time_std_days": "Average Decision Time — Standard (Days)",
    "median_time_std_days": "Median Decision Time — Standard (Days)",
    "avg_time_exp_hours": "Average Decision Time — Expedited (Hours)",
    "median_time_exp_hours": "Median Decision Time — Expedited (Hours)",
}
