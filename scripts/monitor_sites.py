# ====================================================================
# monitor_sites.py — Check Payer Websites for Changes
#
# WHAT IS THIS SCRIPT?
# Instead of manually visiting 43+ payer websites every day to see
# if they've posted their PA metrics, this script does it for you.
# It visits each URL, takes a "fingerprint" of the page, and compares
# it to the last time you checked. If something changed, it tells you.
#
# HOW TO RUN:
#     python scripts/monitor_sites.py
#
# FIRST RUN: Establishes a "baseline" — saves a fingerprint of each
#   page as it looks right now. No changes to report.
#
# SUBSEQUENT RUNS: Compares current fingerprint to the baseline.
#   If a page changed, it reports "CHANGED" so you know to go look.
#
# HOW TO ADD NEW URLs:
#   Edit data/monitor_urls.json — it's a simple list you can open
#   in any text editor. Add a new entry with payer name, URL, and notes.
# ====================================================================

import sys
import json
import time
from pathlib import Path
from datetime import datetime

# ====================================================================
# WHAT IS "hashlib"?
# hashlib creates "hashes" — unique fingerprints for any piece of data.
# If you give it a 10,000-word web page, it produces a short string
# like "a3f2b8c1d4e5...". If even ONE character on that page changes,
# the hash is COMPLETELY different.
#
# This is how we detect changes without storing entire web pages.
# We just store the short fingerprint and compare it next time.
# ====================================================================
import hashlib

# "requests" lets Python download web pages (installed via pip).
import requests

# BeautifulSoup reads HTML and lets us extract just the text content,
# ignoring the code/formatting that makes up the page structure.
from bs4 import BeautifulSoup

# ====================================================================
# PATH SETUP
# ====================================================================
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

# Where our files live
URLS_FILE = project_root / "data" / "monitor_urls.json"
HASHES_FILE = project_root / "data" / "monitor_hashes.json"
LOGS_DIR = project_root / "data" / "monitor_logs"

# How long to wait for a website to respond (in seconds).
# Some payer sites are slow. 15 seconds is generous but reasonable.
REQUEST_TIMEOUT = 15

# How long to wait between requests (in seconds).
# This is called "rate limiting" — we don't want to hit payer servers
# too fast. That could get us blocked, and it's also just rude.
DELAY_BETWEEN_REQUESTS = 2


def load_urls():
    """
    Read the URL watchlist from data/monitor_urls.json.

    WHAT IS JSON?
    JSON (JavaScript Object Notation) is a file format for storing
    structured data. It looks a lot like Python dictionaries and lists.
    It's the most common format for data exchange on the web.

    json.load() reads a JSON file and converts it into Python objects
    (lists and dictionaries) that we can work with in code.
    """
    with open(URLS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_hashes():
    """
    Load previously saved page fingerprints from monitor_hashes.json.
    If the file doesn't exist yet (first run), return an empty dict.
    """
    if HASHES_FILE.exists():
        with open(HASHES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    # First run — no previous hashes exist yet.
    return {}


def save_hashes(hashes):
    """
    Save current page fingerprints to monitor_hashes.json.

    json.dump() converts Python objects into JSON format and writes
    them to a file. The "indent=2" makes the file human-readable
    (adds line breaks and spacing) instead of one giant line.
    """
    with open(HASHES_FILE, "w", encoding="utf-8") as f:
        json.dump(hashes, f, indent=2)


def get_page_fingerprint(url):
    """
    Download a web page and create a fingerprint (hash) of its content.

    IMPORTANT: We don't hash the raw HTML. Websites have timestamps,
    session IDs, tracking pixels, and ads that change on every page load.
    If we hashed the raw HTML, we'd get "CHANGED!" every single time
    even if the actual content didn't change. That would be useless.

    Instead, we:
    1. Download the raw HTML
    2. Use BeautifulSoup to extract ONLY the visible text
    3. Remove extra whitespace (formatting changes don't matter)
    4. Hash the cleaned text

    This way, we only detect REAL content changes — like a payer
    adding their PA metrics data to the page.

    Returns the hash string, or None if the page couldn't be loaded.
    """

    # ================================================================
    # WHAT IS try/except?
    #
    # Sometimes code fails — a website might be down, your internet
    # might cut out, or a URL might be wrong. Normally, an error
    # would CRASH the entire script. That's bad when you're checking
    # 43 URLs — you don't want #3 crashing to skip #4 through #43.
    #
    # "try/except" says: "TRY to run this code. If it fails, don't
    # crash — instead, run the EXCEPT block (which handles the error
    # gracefully) and keep going."
    #
    # ANALOGY: It's like saying "try to open this door. If it's
    # locked, don't stand there forever — just note it and move on
    # to the next door."
    # ================================================================
    try:
        # Send an HTTP GET request to the URL.
        # "GET" means "give me this page" (as opposed to "POST" which
        # sends data TO the server).
        # "timeout" means give up after this many seconds if no response.
        # "headers" tells the website what browser we're pretending to be.
        # Some sites block requests that don't look like a real browser.
        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT,
            headers={
                "User-Agent": "ClearPath Health Monitor/1.0 (research)"
            }
        )

        # "status_code" is a number the website sends back:
        #   200 = OK (page loaded successfully)
        #   404 = Not Found (page doesn't exist)
        #   403 = Forbidden (we're blocked)
        #   500 = Server Error (their problem, not ours)
        # We only care about 200 (success).
        if response.status_code != 200:
            return None, f"HTTP {response.status_code}"

        # Parse the HTML with BeautifulSoup.
        # "html.parser" is a built-in Python HTML parser.
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove elements that change on every page load and would
        # cause false positives. These are HTML tags for:
        #   script = JavaScript code
        #   style  = CSS styling
        #   nav    = navigation menus
        #   footer = page footers (often have timestamps)
        #   header = page headers (often have login status)
        for element in soup.find_all(["script", "style", "nav", "footer", "header"]):
            # .decompose() removes the element from the parsed HTML entirely.
            element.decompose()

        # Extract just the visible text from what remains.
        # .get_text() strips all HTML tags and returns plain text.
        # separator=" " puts a space between text from different elements.
        text = soup.get_text(separator=" ")

        # Clean up the text: replace multiple spaces/newlines with
        # single spaces. This way, formatting changes (extra line breaks,
        # different spacing) don't trigger false "CHANGED" alerts.
        # .split() breaks text into words, " ".join() puts them back
        # together with exactly one space between each word.
        clean_text = " ".join(text.split())

        # Create the hash (fingerprint) of the cleaned text.
        # sha256 is a hashing algorithm — it always produces a
        # 64-character string, no matter how long the input is.
        # .encode("utf-8") converts the text string to bytes
        # (hashlib needs bytes, not strings).
        # .hexdigest() returns the hash as a readable hex string.
        page_hash = hashlib.sha256(clean_text.encode("utf-8")).hexdigest()

        return page_hash, "OK"

    except requests.exceptions.Timeout:
        return None, "TIMEOUT"
    except requests.exceptions.ConnectionError:
        return None, "CONNECTION ERROR"
    except Exception as e:
        # "Exception as e" catches ANY error and stores it in
        # the variable "e" so we can print what went wrong.
        return None, f"ERROR: {str(e)[:50]}"


def run_monitor():
    """
    Main function: check all URLs and report changes.
    """

    # Load the URL list and previous hashes
    urls = load_urls()
    previous_hashes = load_hashes()
    is_first_run = len(previous_hashes) == 0

    # Prepare to collect results
    results = []
    changed_count = 0
    error_count = 0
    new_hashes = {}

    # Get today's date for the log file name
    today = datetime.now().strftime("%Y-%m-%d")

    print(f"Checking {len(urls)} URLs...")
    print()

    # Check each URL
    for i, entry in enumerate(urls):
        payer = entry["payer"]
        url = entry["url"]

        # Show progress (which site we're checking)
        print(f"  [{i + 1}/{len(urls)}] {payer}...", end=" ")

        # Get the current fingerprint
        current_hash, status = get_page_fingerprint(url)

        if current_hash is None:
            # Page couldn't be loaded
            print(f"FAILED ({status})")
            results.append(f"FAILED  | {payer} | {status} | {url}")
            error_count = error_count + 1
        elif is_first_run:
            # First run — just establishing baseline
            print("baseline saved")
            results.append(f"NEW     | {payer} | Baseline established | {url}")
            new_hashes[url] = current_hash
        elif url not in previous_hashes:
            # URL was added to the list since last run
            print("NEW URL — baseline saved")
            results.append(f"NEW     | {payer} | First check for this URL | {url}")
            new_hashes[url] = current_hash
        elif current_hash != previous_hashes[url]:
            # HASH CHANGED — the page content is different!
            print("*** CHANGED ***")
            results.append(f"CHANGED | {payer} | Content changed! Go check. | {url}")
            new_hashes[url] = current_hash
            changed_count = changed_count + 1
        else:
            # No change — same as last time
            print("no change")
            results.append(f"OK      | {payer} | No change | {url}")
            new_hashes[url] = current_hash

        # Wait between requests (rate limiting)
        if i < len(urls) - 1:
            time.sleep(DELAY_BETWEEN_REQUESTS)

    # Save updated hashes
    save_hashes(new_hashes)

    # --- Write log file ---
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOGS_DIR / f"monitor_{today}.log"

    # "a" mode = append (add to end of file, don't overwrite).
    # This way, if you run the monitor multiple times in one day,
    # all results go into the same day's log file.
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\n{'=' * 60}\n")
        f.write(f"Monitor run: {timestamp}\n")
        f.write(f"{'=' * 60}\n")
        for line in results:
            f.write(line + "\n")
        f.write(f"\nSummary: {changed_count} changed, "
                f"{error_count} errors, "
                f"{len(urls)} total\n")

    # --- Print summary ---
    print()
    print("=" * 60)
    if is_first_run:
        print(f"  FIRST RUN — baseline established for {len(urls)} URLs.")
        print("  Run again later to detect changes.")
    elif changed_count > 0:
        print(f"  {changed_count} SITE(S) CHANGED! Go check them.")
    else:
        print("  No changes detected.")
    if error_count > 0:
        print(f"  {error_count} site(s) couldn't be reached.")
    print(f"  Log saved: {log_path}")
    print("=" * 60)


if __name__ == "__main__":
    print()
    print("=" * 60)
    print("  ClearPath Health — Payer Website Monitor")
    print("=" * 60)
    print()

    run_monitor()
