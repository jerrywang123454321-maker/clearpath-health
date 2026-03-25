# ====================================================================
# seed_payers.py — Load the Top 20 MA Payer Watchlist into the Database
#
# WHAT IS THIS SCRIPT?
# This script adds the 20 largest Medicare Advantage organizations
# to our database so we know WHO to look for when CMS data drops
# on March 31, 2026. Think of it as building your "hit list" of
# payers to check.
#
# WHAT DOES "SEED" MEAN?
# "Seeding" a database means pre-loading it with starter data.
# Like planting seeds in a garden — you put the initial data in so
# the system has something to work with. In our case, the seeds are
# the names and info of the payers we want to track.
#
# HOW TO RUN IT:
#     python scripts/seed_payers.py
#
# It's safe to run multiple times — it checks if a payer already
# exists before adding it, so you won't get duplicates.
#
# DATA SOURCE:
# Enrollment numbers come from CMS enrollment data as reported by
# KFF, Becker's, and Mark Farrah Associates (2024-2025 data).
# ====================================================================

import sys
from pathlib import Path

# ====================================================================
# PATH SETUP
# Same trick as setup_db.py — tell Python where to find our code.
# (See setup_db.py for the detailed explanation of why this is needed.)
# ====================================================================
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

from clearpath.database import get_connection

# ====================================================================
# THE PAYER WATCHLIST
#
# This is a "list of tuples." Let me break that down:
#
# LIST = an ordered collection of items, wrapped in square brackets [].
#   Think of it like a numbered list on paper.
#
# TUPLE = a group of values bundled together, wrapped in parentheses ().
#   Think of it like one row in a spreadsheet — multiple columns of
#   data that belong together.
#
# So this is a list where each item is a tuple containing:
#   (name, payer_type, parent_organization, enrollment_size, website_url)
#
# The order of values in each tuple MUST match the order of columns
# in our INSERT statement below. If you mix them up, the wrong data
# goes into the wrong column.
# ====================================================================
PAYERS = [
    # (name, type, parent_org, enrollment, website)
    #
    # "MA" means Medicare Advantage — all 20 of these are MA plans.
    # These are ranked by enrollment size (biggest first).

    (
        "UnitedHealthcare",           # The largest MA insurer by far
        "MA",
        "UnitedHealth Group",         # Parent company
        9_900_000,                    # ~9.9 million members
        # In Python, underscores in numbers are ignored — they're
        # just visual separators to make big numbers readable.
        # 9_900_000 is the same as 9900000, just easier to read.
        "https://www.uhc.com",
    ),
    (
        "Humana",
        "MA",
        "Humana Inc.",
        5_700_000,
        "https://www.humana.com",
    ),
    (
        "Aetna",
        "MA",
        "CVS Health Corporation",     # CVS bought Aetna in 2018
        4_100_000,
        "https://www.aetna.com",
    ),
    (
        "Elevance Health",            # Formerly Anthem / Wellpoint
        "MA",
        "Elevance Health Inc.",
        2_200_000,
        "https://www.elevancehealth.com",
    ),
    (
        "Kaiser Permanente",
        "MA",
        "Kaiser Foundation Health Plan Inc.",
        1_900_000,
        "https://www.kaiserpermanente.org",
    ),
    (
        "Centene (Wellcare)",
        "MA",
        "Centene Corporation",
        1_100_000,
        "https://www.centene.com",
    ),
    (
        "HCSC",                       # Health Care Service Corporation
        "MA",
        "Health Care Service Corporation",
        925_000,
        "https://www.hcsc.com",
    ),
    (
        "Blue Cross Blue Shield of Michigan",
        "MA",
        "BCBSM",
        696_000,
        "https://www.bcbsm.com",
    ),
    (
        "Devoted Health",
        "MA",
        None,                         # None = no parent / independent
        470_000,                      # Fast-growing — doubled recently
        "https://www.devoted.com",
    ),
    (
        "SCAN Health Plan",
        "MA",
        "SCAN Group",                 # Nonprofit
        440_000,
        "https://www.scanhealthplan.com",
    ),
    (
        "Highmark Health",
        "MA",
        "Highmark Inc.",
        417_000,
        "https://www.highmark.com",
    ),
    (
        "Florida Blue",
        "MA",
        "GuideWell Mutual Holding Corp.",
        332_000,
        "https://www.floridablue.com",
    ),
    (
        "Alignment Healthcare",
        "MA",
        "Alignment Healthcare Inc.",
        277_000,
        "https://www.alignmenthealthcare.com",
    ),
    (
        "Molina Healthcare",
        "MA",
        "Molina Healthcare Inc.",
        213_000,
        "https://www.molinahealthcare.com",
    ),
    (
        "Clover Health",
        "MA",
        "Clover Health Investments",
        153_000,
        "https://www.cloverhealth.com",
    ),
    (
        "CareSource",
        "MA",
        None,                         # Nonprofit
        150_000,
        "https://www.caresource.com",
    ),
    (
        "Horizon BCBSNJ",
        "MA",
        "Horizon Blue Cross Blue Shield of NJ",
        130_000,
        "https://medicare.horizonblue.com",
    ),
    (
        "Independence Blue Cross",
        "MA",
        "Independence Health Group",
        120_000,
        "https://www.ibx.com",
    ),
    (
        "Tufts Health Plan",
        "MA",
        "Point32Health",
        100_000,
        "https://www.tuftsmedicarepreferred.org",
    ),
    (
        "Geisinger Health Plan",
        "MA",
        "Risant Health",              # Now a Kaiser subsidiary
        90_000,
        "https://www.geisinger.org",
    ),
]


def seed_payers():
    """
    Add all payers from the PAYERS list into the database.

    This function loops through each payer and adds it to the
    "payers" table — but ONLY if that payer isn't already there.
    That way you can run this script multiple times without
    creating duplicates.
    """

    # Open a connection to the database.
    # "with" ensures the connection is closed properly when done.
    with get_connection() as connection:

        # "cursor" is like a pointer that executes SQL commands.
        # Think of the connection as picking up the phone, and the
        # cursor as actually speaking into it.
        cursor = connection.cursor()

        # Keep track of how many we actually add (for the summary).
        added_count = 0
        skipped_count = 0

        # ============================================================
        # WHAT IS A "FOR LOOP"?
        #
        # A "for loop" repeats a block of code once for each item in
        # a list. It's like saying "for each payer in my list, do
        # the following..."
        #
        # The variable names in the parentheses (name, payer_type, etc.)
        # automatically get filled with the values from each tuple.
        # On the first loop, name="UnitedHealthcare", payer_type="MA", etc.
        # On the second loop, name="Humana", payer_type="MA", etc.
        # And so on for all 20 payers.
        # ============================================================
        for (name, payer_type, parent_org, enrollment, website) in PAYERS:

            # --- Check if this payer already exists ---
            # We search by name. If we find a match, skip it.
            #
            # "?" is a PLACEHOLDER. Instead of putting the payer name
            # directly in the SQL string (which is a security risk called
            # "SQL injection"), we use ? and pass the actual value
            # separately. The database safely substitutes it in.
            #
            # The (name,) at the end is a tuple with one item — the
            # comma after "name" is required because Python needs it
            # to distinguish a one-item tuple from just parentheses.
            # Weird, but that's how Python works.
            cursor.execute(
                "SELECT id FROM payers WHERE name = ?",
                (name,)
            )

            # fetchone() gets one result. If the payer exists, it
            # returns a row. If not, it returns None (Python's word
            # for "nothing").
            existing = cursor.fetchone()

            # "if existing is not None" means "if we found a match"
            if existing is not None:
                print(f"  SKIP: {name} (already in database)")
                skipped_count = skipped_count + 1
                # "continue" means "skip the rest of this loop iteration
                # and move on to the next payer in the list"
                continue

            # --- Add the payer to the database ---
            # INSERT INTO is the SQL command for adding a new row.
            # We list the column names, then the values to put in them.
            cursor.execute(
                """
                INSERT INTO payers (
                    name, payer_type, parent_organization,
                    enrollment_size, website_url
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (name, payer_type, parent_org, enrollment, website)
            )

            print(f"  ADDED: {name} ({enrollment:,} members)")
            #       The {:,} inside the f-string adds commas to numbers.
            #       So 9900000 displays as 9,900,000. Just for readability.

            added_count = added_count + 1

        # Save all changes to the database.
        # "commit" means "make these changes permanent."
        # Without commit, changes would be lost when the connection closes.
        connection.commit()

    # --- Print summary ---
    print()
    print(f"Done! Added {added_count} payers, skipped {skipped_count}.")
    print(f"Total payers in watchlist: {added_count + skipped_count}")


# ====================================================================
# Run the function when this script is executed directly.
# (See setup_db.py for the full explanation of this pattern.)
# ====================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("ClearPath Health — Seeding Payer Watchlist")
    print("=" * 60)
    print()
    print("Adding top 20 Medicare Advantage organizations...")
    print()

    seed_payers()

    print()
    print("These are the payers we'll check on March 31 when")
    print("CMS-mandated PA metrics are due to be published.")
