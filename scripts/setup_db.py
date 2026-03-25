# ====================================================================
# setup_db.py — Create the ClearPath Health Database
#
# WHAT IS THIS SCRIPT?
# This is a "script" — a Python file you run directly from the
# command line (terminal). It creates the database by reading the
# blueprint (schema.sql) and building all the tables.
#
# HOW TO RUN IT:
# Open your terminal, navigate to the project folder, and type:
#     python scripts/setup_db.py
#
# WHEN TO RUN IT:
# - Once, when you first set up the project on a new computer
# - If you ever delete the database and need to recreate it
# - It's safe to run multiple times (it won't delete existing data)
#
# WHAT IS A "SCRIPT" vs. A "MODULE"?
# - A MODULE (like config.py, database.py) is meant to be IMPORTED
#   by other code. It provides tools for other files to use.
# - A SCRIPT is meant to be RUN DIRECTLY by you. It does a specific
#   task and then stops. Scripts live in the scripts/ folder.
# ====================================================================

# ====================================================================
# IMPORTS
#
# "sys" is a built-in Python module that gives access to system-level
# things. We use it here to modify the "path" — the list of places
# Python looks when you say "import something."
#
# "Path" is from pathlib (explained in config.py) — it helps us
# work with file/folder locations.
# ====================================================================
import sys
from pathlib import Path

# ====================================================================
# PATH SETUP — WHY IS THIS NECESSARY?
#
# When you run "python scripts/setup_db.py" from the terminal,
# Python only knows about the scripts/ folder. It doesn't
# automatically know where src/clearpath/ is.
#
# These two lines tell Python: "Hey, also look in the 'src' folder
# when I say 'import'." Without this, "from clearpath import ..."
# would fail with "ModuleNotFoundError."
#
# This is only needed in scripts that you run directly. Files inside
# src/clearpath/ can find each other automatically.
# ====================================================================
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

# NOW we can import from our project.
# "from clearpath.database import initialize_database" means:
#   - Look in the "clearpath" package (folder)
#   - Find the "database" module (database.py)
#   - Grab the "initialize_database" function from it
from clearpath.database import initialize_database
from clearpath.config import DATABASE_PATH

# ====================================================================
# WHAT IS "if __name__ == '__main__'"?
#
# This is one of Python's most common (and confusing) patterns.
# Here's what it means:
#
# Every Python file has a hidden variable called __name__.
# - If you RUN the file directly (python setup_db.py), __name__
#   is set to the special string "__main__"
# - If another file IMPORTS this file, __name__ is set to the
#   file's actual name (like "setup_db")
#
# So "if __name__ == '__main__'" means: "Only run the code below
# if this file was run directly, NOT if it was imported."
#
# WHY? Because sometimes you want a file to work both ways:
# - As a script you can run: python setup_db.py
# - As a module other code can import from (without running the script)
#
# For this file, it just means: running it directly creates the DB.
# ====================================================================
if __name__ == "__main__":

    # print() displays text in the terminal so you can see what's happening.
    print("=" * 60)
    print("ClearPath Health — Database Setup")
    print("=" * 60)
    print()

    # Call the function that actually creates the tables.
    # This was defined in database.py — we imported it above.
    initialize_database()

    # Let the user know it worked, and show where the database file is.
    print(f"Database created successfully!")
    print(f"Location: {DATABASE_PATH}")
    print()
    print("The following tables were created:")
    print("  - payers              (insurance companies/plans)")
    print("  - metrics_reports     (annual PA metrics publications)")
    print("  - data_points         (individual metric values)")
    print("  - pa_requirements     (services requiring PA)")
    print("  - compliance_checks   (CMS rule compliance tracking)")
    print()
    print("You're ready to start collecting data!")
