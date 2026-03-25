# ====================================================================
# COLLECTORS PACKAGE
#
# This folder contains all the code responsible for COLLECTING data
# from payer websites. Think of collectors as the "field researchers"
# of ClearPath Health — they go out to each payer's website, find the
# prior authorization metrics that CMS requires them to publish, and
# bring that data back in a structured format.
#
# Different payers publish their data in different ways (PDFs, HTML
# pages, spreadsheets), so we may need different collector strategies
# for different payers. That's why this is its own folder with
# multiple files inside it.
#
# Files in this folder:
#   base.py   — Shared logic that ALL collectors use
#   manual.py — A tool for manually entering data (for payers whose
#               websites can't be automatically scraped)
# ====================================================================
