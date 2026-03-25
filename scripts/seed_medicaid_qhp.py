# ====================================================================
# seed_medicaid_qhp.py — Add Medicaid MCOs and QHP Issuers to Database
#
# WHAT IS THIS SCRIPT?
# This adds two more categories of payers to our watchlist:
#   1. Texas Medicaid managed care organizations (MCOs)
#   2. Top national QHP (ACA marketplace) issuers
#
# WHY SEPARATE FROM seed_payers.py?
# We keep scripts focused on one task (remember: one module = one job).
# seed_payers.py handles Medicare Advantage. This one handles the
# other payer categories. Both use the same database table.
#
# HOW TO RUN:
#     python scripts/seed_medicaid_qhp.py
#
# Safe to run multiple times — skips payers that already exist.
# ====================================================================

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

from clearpath.database import get_connection


# ====================================================================
# TEXAS MEDICAID MANAGED CARE ORGANIZATIONS
#
# Texas has ~4.6 million people in Medicaid managed care, split across
# programs: STAR (general), STAR+PLUS (adults with disabilities),
# STAR Kids (children with disabilities), and CHIP.
#
# These are the plans YOUR PATIENTS at Baylor Houston will be on.
# That makes this data personally relevant to your clinical training.
#
# Note: Several of these are children's hospital-based plans — unique
# to Texas and worth highlighting in your report.
# ====================================================================
TEXAS_MEDICAID = [
    # (name, type, parent_org, state, enrollment, website)
    (
        "Superior HealthPlan",
        "Medicaid",
        "Centene Corporation",
        "TX",
        1_100_000,      # Largest TX Medicaid MCO; also runs STAR Health (foster care)
        "https://www.superiorhealthplan.com",
    ),
    (
        "UnitedHealthcare Community Plan of Texas",
        "Medicaid",
        "UnitedHealth Group",
        "TX",
        800_000,
        "https://www.uhccommunityplan.com/tx",
    ),
    (
        "Aetna Better Health of Texas",
        "Medicaid",
        "CVS Health Corporation",
        "TX",
        600_000,
        "https://www.aetnabetterhealth.com/texas",
    ),
    (
        "Molina Healthcare of Texas",
        "Medicaid",
        "Molina Healthcare Inc.",
        "TX",
        500_000,
        "https://www.molinahealthcare.com/members/tx",
    ),
    (
        "Blue Cross Blue Shield of Texas (Medicaid)",
        "Medicaid",
        "Health Care Service Corporation",
        "TX",
        400_000,
        "https://www.bcbstx.com",
    ),
    (
        "WellPoint Texas",              # Formerly Amerigroup
        "Medicaid",
        "Elevance Health Inc.",
        "TX",
        400_000,
        "https://www.wellpoint.com",
    ),
    (
        "Texas Children's Health Plan",  # Houston-based! Your backyard.
        "Medicaid",
        "Texas Children's Hospital",
        "TX",
        400_000,
        "https://www.texaschildrenshealthplan.org",
    ),
    (
        "Community Health Choice",       # Also Houston-based
        "Medicaid",
        None,                            # Independent nonprofit
        "TX",
        350_000,
        "https://www.communityhealthchoice.org",
    ),
    (
        "Cook Children's Health Plan",
        "Medicaid",
        "Cook Children's Medical Center",
        "TX",
        150_000,
        "https://www.cookchp.org",
    ),
    (
        "Driscoll Children's Health Plan",
        "Medicaid",
        "Driscoll Children's Hospital",
        "TX",
        125_000,
        "https://www.driscollhealthplan.com",
    ),
    (
        "El Paso First Health Plans",
        "Medicaid",
        None,                            # County hospital district
        "TX",
        100_000,
        "https://www.epfirst.com",
    ),
    (
        "Community First Health Plans",  # San Antonio
        "Medicaid",
        "University Health",
        "TX",
        100_000,
        "https://www.cfhp.com",
    ),
    (
        "Parkland Community Health Plan",  # Dallas
        "Medicaid",
        "Parkland Health",
        "TX",
        100_000,
        "https://www.parklandhealthfirst.com",
    ),
]


# ====================================================================
# TOP QHP (ACA MARKETPLACE) ISSUERS
#
# These are the plans people buy on healthcare.gov (or state exchanges).
# Record 24.3 million enrolled for 2025. Many are the same parent
# companies as MA, but operating under different brand names.
# ====================================================================
QHP_ISSUERS = [
    (
        "Ambetter Health",              # Largest marketplace insurer
        "QHP",
        "Centene Corporation",
        None,                           # National (29 states)
        5_800_000,
        "https://www.ambetterhealth.com",
    ),
    (
        "Oscar Health",
        "QHP",
        "Oscar Health Inc.",
        None,
        2_000_000,                      # Fast-growing startup insurer
        "https://www.hioscar.com",
    ),
    (
        "Molina Marketplace",
        "QHP",
        "Molina Healthcare Inc.",
        None,
        1_100_000,
        "https://www.molinahealthcare.com",
    ),
    (
        "Florida Blue (Marketplace)",
        "QHP",
        "GuideWell Mutual Holding Corp.",
        "FL",
        1_250_000,                      # FL is the largest ACA market
        "https://www.floridablue.com",
    ),
    (
        "Kaiser Permanente (Marketplace)",
        "QHP",
        "Kaiser Foundation Health Plan Inc.",
        None,
        1_000_000,
        "https://www.kaiserpermanente.org",
    ),
    (
        "Elevance Health (Marketplace)",
        "QHP",
        "Elevance Health Inc.",
        None,
        1_000_000,
        "https://www.anthem.com",
    ),
    (
        "UnitedHealthcare (Marketplace)",
        "QHP",
        "UnitedHealth Group",
        None,
        650_000,
        "https://www.uhc.com",
    ),
    (
        "CareSource (Marketplace)",
        "QHP",
        None,                           # Nonprofit
        None,
        500_000,
        "https://www.caresource.com",
    ),
    (
        "HCSC (Marketplace)",
        "QHP",
        "Health Care Service Corporation",
        None,
        500_000,
        "https://www.hcsc.com",
    ),
    (
        "BCBS of Texas (Marketplace)",
        "QHP",
        "Health Care Service Corporation",
        "TX",
        400_000,
        "https://www.bcbstx.com",
    ),
]


def seed_all():
    """
    Add all Medicaid and QHP payers to the database.
    Skips any that already exist (checked by name).
    """

    with get_connection() as connection:
        cursor = connection.cursor()
        added = 0
        skipped = 0

        # Combine both lists into one so we can loop through them all.
        # The "+" operator on lists joins them together:
        #   [1, 2] + [3, 4] = [1, 2, 3, 4]
        all_payers = TEXAS_MEDICAID + QHP_ISSUERS

        for (name, payer_type, parent_org, state, enrollment, website) in all_payers:

            # Check if already exists
            cursor.execute("SELECT id FROM payers WHERE name = ?", (name,))
            if cursor.fetchone() is not None:
                print(f"  SKIP: {name}")
                skipped = skipped + 1
                continue

            # Add to database
            cursor.execute(
                """
                INSERT INTO payers (
                    name, payer_type, parent_organization,
                    state, enrollment_size, website_url
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (name, payer_type, parent_org, state, enrollment, website),
            )
            print(f"  ADDED: {name} ({enrollment:,} members) [{payer_type}]")
            added = added + 1

        connection.commit()

    print()
    print(f"Done! Added {added}, skipped {skipped}.")


if __name__ == "__main__":
    print("=" * 60)
    print("ClearPath Health — Seeding Medicaid & QHP Payers")
    print("=" * 60)
    print()
    print("--- Texas Medicaid Managed Care Organizations ---")
    print()

    seed_all()

    print()
    print("Your database now covers Medicare Advantage, Texas")
    print("Medicaid, and ACA Marketplace payers.")
