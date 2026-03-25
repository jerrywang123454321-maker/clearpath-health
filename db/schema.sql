-- ====================================================================
-- schema.sql — The DATABASE BLUEPRINT for ClearPath Health
--
-- WHAT IS A DATABASE?
-- A database is like a collection of spreadsheets (called "tables").
-- Each table stores one type of information. Tables can reference
-- each other — for example, a "metrics_reports" row can point to
-- which "payer" it belongs to.
--
-- WHAT IS SQL?
-- SQL (Structured Query Language) is the language for talking to
-- databases. This file contains SQL commands that CREATE the tables.
-- Think of it as building the empty filing cabinets before you start
-- putting files in them.
--
-- WHAT IS A "SCHEMA"?
-- A schema is the STRUCTURE of your database — what tables exist,
-- what columns each table has, and what type of data each column
-- holds. This file IS the schema.
--
-- HOW IS THIS USED?
-- The script "scripts/setup_db.py" reads this file and runs these
-- commands to create an actual database file (clearpath.db).
-- ====================================================================


-- ====================================================================
-- TABLE: payers
-- WHO are the insurance companies/plans we're tracking?
--
-- Each row = one payer (like UnitedHealthcare, Aetna, Texas Medicaid)
-- This is the "master list" of every payer in our system.
-- ====================================================================
CREATE TABLE IF NOT EXISTS payers (

    -- "id" is a unique number automatically assigned to each payer.
    -- It's how the database identifies this payer internally.
    -- "INTEGER PRIMARY KEY AUTOINCREMENT" means:
    --   INTEGER     = it's a whole number
    --   PRIMARY KEY = it's the unique identifier for this table
    --   AUTOINCREMENT = the database picks the next number automatically
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- The payer's official name (e.g., "UnitedHealthcare")
    -- "TEXT NOT NULL" means:
    --   TEXT     = it's a string of characters (words)
    --   NOT NULL = this field is REQUIRED (can't be left blank)
    name TEXT NOT NULL,

    -- What TYPE of payer are they? The CMS rule covers these types:
    --   MA      = Medicare Advantage (private plans for seniors)
    --   Medicaid = State Medicaid programs (coverage for low-income)
    --   CHIP    = Children's Health Insurance Program
    --   QHP     = Qualified Health Plan (marketplace/exchange plans)
    --
    -- "CHECK" is a rule that says the value MUST be one of these options.
    -- If you try to enter "banana" as a payer type, the database will
    -- refuse — it's like a dropdown menu in a form.
    payer_type TEXT NOT NULL CHECK(payer_type IN ('MA', 'Medicaid', 'CHIP', 'QHP')),

    -- The parent company (e.g., UnitedHealth Group owns UnitedHealthcare).
    -- This can be NULL (blank) because some payers don't have a parent.
    parent_organization TEXT,

    -- Which state the payer operates in.
    -- For national payers like UHC, this might be their HQ state or NULL.
    state TEXT,

    -- How many people are enrolled in this plan.
    -- Helps us prioritize which payers to analyze first (bigger = more impact).
    enrollment_size INTEGER,

    -- The URL of the payer's main website.
    website_url TEXT,

    -- When was this payer added to our database?
    -- "DEFAULT CURRENT_TIMESTAMP" means the database automatically fills
    -- in today's date and time when you add a new row.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- When was this payer's info last updated?
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ====================================================================
-- TABLE: metrics_reports
-- Each row = one payer's published PA metrics for one year.
--
-- Example: "UnitedHealthcare's CY2025 report, published March 30, 2026"
-- A payer publishes one report per year (starting CY2025).
-- ====================================================================
CREATE TABLE IF NOT EXISTS metrics_reports (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Which payer does this report belong to?
    -- "REFERENCES payers(id)" means this number MUST match an id
    -- that exists in the payers table. This creates a LINK between
    -- the two tables. It's called a "foreign key."
    --
    -- ANALOGY: It's like writing someone's phone number in your
    -- contacts — the number has to actually belong to a real person.
    payer_id INTEGER NOT NULL REFERENCES payers(id),

    -- Which calendar year does this data cover? (e.g., 2025)
    reporting_year INTEGER NOT NULL,

    -- When did the payer actually publish this report?
    date_published DATE,

    -- The URL where we found this report on the payer's website.
    -- Critical for verification — anyone can click this link and
    -- see the original source data.
    source_url TEXT,

    -- We save a screenshot of the page as proof, in case the payer
    -- later changes or removes their data.
    screenshot_path TEXT,

    -- Did this report meet CMS requirements? (TRUE/FALSE)
    -- "BOOLEAN" is really just 0 (false) or 1 (true) in SQLite.
    is_compliant BOOLEAN,

    -- What format did the payer use to publish?
    -- CMS provided a template, but payers might use their own format.
    format_used TEXT CHECK(format_used IN (
        'CMS_template',  -- Used the official CMS template (good!)
        'custom_html',   -- Made their own HTML web page
        'pdf',           -- Published as a PDF document
        'spreadsheet',   -- Published as Excel/CSV
        'other'          -- Something else
    )),

    -- Free-text notes about anything unusual with this report.
    notes TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- UNIQUE constraint: one report per payer per year.
    -- This prevents accidentally entering the same report twice.
    UNIQUE(payer_id, reporting_year)
);


-- ====================================================================
-- TABLE: data_points
-- The ACTUAL NUMBERS from each report.
--
-- Each row = one specific metric from one report.
-- Example: "UHC's CY2025 report: standard PA approval rate = 87.3%"
--
-- These are the 8 metrics CMS requires payers to publish
-- (see Part 2 of the project plan).
-- ====================================================================
CREATE TABLE IF NOT EXISTS data_points (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Which report does this number come from?
    report_id INTEGER NOT NULL REFERENCES metrics_reports(id),

    -- WHICH metric is this? Must be one of these standardized types.
    -- These correspond to the 8 CMS-required metrics:
    metric_type TEXT NOT NULL CHECK(metric_type IN (
        'std_approved_pct',      -- % of standard PA requests approved
        'std_denied_pct',        -- % of standard PA requests denied
        'std_appeal_approved_pct', -- % of standard denials approved on appeal
        'ext_approved_pct',      -- % approved after timeframe extension
        'exp_approved_pct',      -- % of expedited (urgent) requests approved
        'exp_denied_pct',        -- % of expedited requests denied
        'avg_time_std_days',     -- Average days to decide standard requests
        'median_time_std_days',  -- Median days to decide standard requests
        'avg_time_exp_hours',    -- Average hours to decide expedited requests
        'median_time_exp_hours'  -- Median hours to decide expedited requests
    )),

    -- The actual number (e.g., 87.3 for 87.3%, or 4.2 for 4.2 days)
    -- "REAL" means it can have decimal places (not just whole numbers).
    value REAL NOT NULL,

    -- Optional notes about this specific data point.
    notes TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- One metric type per report — can't have two "std_approved_pct"
    -- values for the same report.
    UNIQUE(report_id, metric_type)
);


-- ====================================================================
-- TABLE: pa_requirements
-- WHAT services does each payer require prior authorization for?
--
-- CMS metric #1 requires payers to publish a list of all items and
-- services that require PA (excluding drugs). This table stores those.
--
-- Example: "UHC requires PA for MRI of lumbar spine (CPT 72148)"
-- ====================================================================
CREATE TABLE IF NOT EXISTS pa_requirements (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Which payer has this requirement?
    payer_id INTEGER NOT NULL REFERENCES payers(id),

    -- When did this list take effect?
    effective_date DATE,

    -- A broad category for the service (e.g., "Imaging", "Surgery")
    service_category TEXT,

    -- A description of the specific service
    service_description TEXT,

    -- CPT codes (the medical billing codes for specific procedures).
    -- Stored as text because there might be multiple codes or ranges.
    cpt_codes TEXT,

    -- Where we found this list on the payer's website.
    source_url TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ====================================================================
-- TABLE: compliance_checks
-- Did the payer follow the CMS rules?
--
-- Each row = one compliance check for one payer on one date.
-- We check: did they publish? Was it on time? Is the data complete?
--
-- This feeds into the "Compliance Report" section of our annual report.
-- ====================================================================
CREATE TABLE IF NOT EXISTS compliance_checks (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    payer_id INTEGER NOT NULL REFERENCES payers(id),

    -- When did we perform this check?
    check_date DATE NOT NULL,

    -- Did the payer publish their metrics at all? (yes/no)
    published BOOLEAN NOT NULL DEFAULT 0,

    -- Did they publish by the March 31 deadline? (yes/no)
    on_time BOOLEAN NOT NULL DEFAULT 0,

    -- Did their publication format meet CMS requirements? (yes/no)
    format_compliant BOOLEAN NOT NULL DEFAULT 0,

    -- Did they include ALL 8 required metrics? (yes/no)
    data_complete BOOLEAN NOT NULL DEFAULT 0,

    -- Free-text notes about any issues found.
    notes TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
