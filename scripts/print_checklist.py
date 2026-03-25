# ====================================================================
# print_checklist.py — Print Your March 31 Payer Checklist
#
# WHAT IS THIS SCRIPT?
# Prints a formatted checklist of all payers in your database, along
# with the specific URL where you should look for their PA metrics.
#
# Some payers already have dedicated PA metrics pages. Others just
# have their homepage — you'll need to hunt around on March 31.
#
# HOW TO RUN:
#     python scripts/print_checklist.py
#
# This script ONLY READS from the database — it doesn't change anything.
# ====================================================================

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

from clearpath.database import get_connection
from clearpath.config import PAYER_TYPES


# ====================================================================
# KNOWN PA METRICS PAGES
#
# These are specific URLs where payers have already set up pages for
# PA metrics, transparency data, or CMS-0057-F compliance. We found
# these by searching each payer's website in March 2026.
#
# If a payer isn't in this dictionary, we'll just show their main
# website URL and you'll have to search manually.
#
# KEY INSIGHT: Most payers haven't set up dedicated pages yet.
# Expect a rush of new pages around March 31. When you find them,
# update this dictionary so future runs show the right URLs.
# ====================================================================
KNOWN_METRICS_PAGES = {
    # --- PAYERS WITH DEDICATED PA METRICS PAGES (confirmed) ---

    "Oscar Health": {
        "status": "PUBLISHED",
        "urls": [
            ("PA Statistics (Medical)", "https://www.hioscar.com/prior-authorization-statistics"),
            ("PA Statistics (Rx)", "https://www.hioscar.com/prior-authorization-statistics-prescriptions"),
            ("PA Turnaround Times", "https://www.hioscar.com/prior-authorization-turnaround-times"),
        ],
        "notes": "Most transparent payer found. Three separate pages with actual data.",
    },

    "Superior HealthPlan": {
        "status": "PARTIAL",
        "urls": [
            ("PA Info (Medicaid)", "https://www.superiorhealthplan.com/members/medicaid/resources/prior-authorization.html"),
            ("Medicare PA Times", "https://www.superiorhealthplan.com/newsroom/change-in-medicare-pa-response-time.html"),
        ],
        "notes": "Publishes approval/denial rate PDFs for CHIP and Ambetter.",
    },

    "Ambetter Health": {
        "status": "PARTIAL",
        "urls": [
            ("TX PA Requirements", "https://www.ambetterhealth.com/en/tx/provider-resources/manuals-and-forms/prior-authorization-requirements-for-health-insurance-marketplac/"),
        ],
        "notes": "2024 approval/denial rates available as downloadable PDF.",
    },

    # --- PAYERS WITH SOME DATA EMBEDDED IN OTHER PAGES ---

    "SCAN Health Plan": {
        "status": "EMBEDDED",
        "urls": [
            ("Provider Portal (has some stats)", "https://www.scanhealthplan.com/en/providers/joining-the-scan-network/prior-authorizations/scan-referral-intake-portal"),
        ],
        "notes": "Claims 87% of submissions didn't need PA. Denial rate <1%.",
    },

    "HCSC": {
        "status": "EMBEDDED",
        "urls": [
            ("AI PA Press Release (has metrics)", "https://www.hcsc.com/newsroom/news-releases/2023/artificial-intelligence-prior-authorization-process-helps-members-providers"),
        ],
        "notes": "80% speed approvals (behavioral health). Eliminated PA for ~1000 codes since 2018.",
    },

    # --- PAYERS WITH USEFUL (BUT NOT METRICS) PA PAGES ---

    "UnitedHealthcare": {
        "status": "NOT YET",
        "urls": [
            ("Provider PA Hub", "https://www.uhcprovider.com/en/prior-auth-advance-notification.html"),
        ],
        "notes": "12.8% MA denial rate, 85.2% appeal overturn. Metrics page expected by 3/31.",
    },

    "Elevance Health": {
        "status": "NOT YET",
        "urls": [
            ("PA Approach Page", "https://www.elevancehealth.com/our-approach-to-health/whole-health/prior-authorization"),
        ],
        "notes": "Claims majority approved in real-time. No AI for denials.",
    },

    "Florida Blue": {
        "status": "NOT YET",
        "urls": [
            ("PA Blog Post", "https://www.floridablue.com/blog/florida-blues-approach-to-prior-authorizations"),
        ],
        "notes": "96% Rx claims, 93% medical claims NOT subject to PA.",
    },

    "Molina Healthcare": {
        "status": "NOT YET",
        "urls": [
            ("CMS-0057 Bulletin (MI)", "https://www.molinahealthcare.com/providers/mi/medicaid/comm/-/media/2DCE855636704A3FA7808FA71DE64701.ashx"),
        ],
        "notes": "Bulletins confirm awareness of March 31 deadline.",
    },

    "Community Health Choice": {
        "status": "NOT YET",
        "urls": [
            ("Provider PA Info", "https://provider.communityhealthchoice.org/resources/prior-authorization-information/"),
        ],
        "notes": "References Texas Gold Card program (HB 3459).",
    },

    "Texas Children's Health Plan": {
        "status": "NOT YET",
        "urls": [
            ("Provider PA Info", "https://www.texaschildrenshealthplan.org/providers/provider-resources/prior-authorization-information"),
        ],
        "notes": "Houston-based. BCM teaching affiliate.",
    },

    # --- STATE MEDICAID PROGRAMS ---

    "MassHealth": {
        "status": "PAGE READY",
        "urls": [
            ("PA Metrics Page (no data yet)", "https://www.mass.gov/info-details/prior-authorization-process-changes-and-metrics"),
        ],
        "notes": "Dedicated metrics page exists but is not yet populated. Best state example.",
    },
}


def print_checklist():
    """
    Query all payers from the database and print a formatted checklist
    grouped by payer type, with known metrics URLs where available.
    """

    with get_connection() as connection:
        cursor = connection.cursor()

        # Get all payers, sorted by type then by enrollment (biggest first).
        # "ORDER BY" tells SQL how to sort the results.
        # "DESC" means descending (biggest number first).
        cursor.execute("""
            SELECT name, payer_type, parent_organization,
                   enrollment_size, website_url
            FROM payers
            ORDER BY payer_type, enrollment_size DESC
        """)

        # fetchall() gets ALL results as a list (unlike fetchone which
        # gets just one). Each result is a Row object where you can
        # access columns by name.
        all_payers = cursor.fetchall()

    # ================================================================
    # GROUP PAYERS BY TYPE
    #
    # We want to print them in sections (MA, Medicaid, QHP).
    # We'll loop through and track when the type changes.
    #
    # "current_type" keeps track of which section we're in.
    # When it changes, we print a new section header.
    # ================================================================
    current_type = None
    payer_number = 0

    for payer in all_payers:
        # Access columns by name (thanks to row_factory in database.py)
        name = payer["name"]
        payer_type = payer["payer_type"]
        parent = payer["parent_organization"]
        enrollment = payer["enrollment_size"]
        website = payer["website_url"]

        # Print section header when type changes
        if payer_type != current_type:
            current_type = payer_type
            # PAYER_TYPES is the dictionary from config.py that maps
            # short codes to full names (e.g., "MA" -> "Medicare Advantage")
            full_type_name = PAYER_TYPES.get(payer_type, payer_type)
            print()
            print("=" * 70)
            print(f"  {full_type_name}")
            print("=" * 70)

        payer_number = payer_number + 1

        # Print the payer's basic info
        print()
        # "[ ]" is an empty checkbox — you can print this out and
        # physically check them off, or just track in your head.
        print(f"  [ ] #{payer_number}: {name}")
        if parent:
            print(f"       Parent: {parent}")
        if enrollment:
            print(f"       Enrollment: {enrollment:,}")
        print(f"       Website: {website}")

        # Check if we have known metrics page info for this payer
        known = KNOWN_METRICS_PAGES.get(name)
        if known:
            status = known["status"]
            print(f"       >>> STATUS: {status}")
            for label, url in known["urls"]:
                print(f"       >>> {label}: {url}")
            if known.get("notes"):
                print(f"       >>> Note: {known['notes']}")
        else:
            print(f"       >>> STATUS: NOT YET — check website on March 31")

    # Print summary
    print()
    print("=" * 70)
    print(f"  TOTAL: {payer_number} payers to check")
    print()
    print("  STATUS KEY:")
    print("    PUBLISHED  = PA metrics data is live and accessible")
    print("    PARTIAL    = Some data available (PDFs, partial stats)")
    print("    EMBEDDED   = Metrics buried in other pages/press releases")
    print("    PAGE READY = Dedicated page exists but no data yet")
    print("    NOT YET    = No metrics page found; check after March 31")
    print("=" * 70)


if __name__ == "__main__":
    print()
    print("=" * 70)
    print("  CLEARPATH HEALTH — March 31, 2026 Collection Checklist")
    print("  CMS-0057-F PA Metrics Reporting Deadline")
    print("=" * 70)
    print()
    print("  Instructions:")
    print("  1. Visit each payer's website/URL listed below")
    print("  2. Look for CY2025 prior authorization metrics")
    print("  3. Note the FORMAT (PDF, HTML, spreadsheet, etc.)")
    print("  4. Save/screenshot the page as evidence")
    print("  5. If no metrics found, note that too (compliance data!)")

    print_checklist()
