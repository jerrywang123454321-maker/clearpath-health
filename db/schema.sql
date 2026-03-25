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


-- ####################################################################
-- ####################################################################
--
--   GRANULAR DATA TABLES (added March 2026)
--
--   The tables above capture the CMS-mandated SUMMARY metrics that
--   every payer must report. But real payer data is much richer —
--   breakdowns by service type, denial reasons, appeal outcomes,
--   diagnosis codes, and more.
--
--   The tables below store that granular detail. When a payer only
--   publishes summary data, these tables will have NULLs (blanks)
--   for that payer — and that's fine. NULL means "not disclosed."
--
--   DESIGN PRINCIPLE: Start granular. It's easier to have empty
--   columns than to add columns later and backfill old data.
--
-- ####################################################################
-- ####################################################################


-- ====================================================================
-- TABLE: source_files
-- WHERE did we get each piece of data? This is the EVIDENCE CHAIN.
--
-- Every report should have at least one source file — the PDF,
-- screenshot, or HTML page we pulled the data from. This proves
-- our numbers are real and lets anyone verify them.
--
-- ANALOGY: In science, you keep your lab notebook. In journalism,
-- you keep your recordings. In data research, you keep your sources.
-- ====================================================================
CREATE TABLE IF NOT EXISTS source_files (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Which report does this source file belong to?
    report_id INTEGER NOT NULL REFERENCES metrics_reports(id),

    -- Where is this file stored on our computer?
    -- Example: "data/raw/oscar_health_tx_2024_medical.pdf"
    file_path TEXT,

    -- The original URL where we downloaded/found this file.
    -- Example: "https://assets.ctfassets.net/plyq12u1bv8a/..."
    original_url TEXT,

    -- What type of file is it?
    -- No CHECK constraint here — new types may appear.
    -- Common values: "pdf", "html", "screenshot", "csv", "xlsx"
    file_type TEXT,

    -- When did we download or capture this file?
    download_date DATE,

    -- Any notes about the source (e.g., "page 3 of PDF has the table")
    notes TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ====================================================================
-- TABLE: service_level_stats
-- PA outcomes BROKEN DOWN BY SERVICE TYPE.
--
-- This is the granular version of data_points. Instead of just
-- "overall approval rate = 83.9%", this table stores:
--   "Imaging approval rate = 75.1%"
--   "Surgery approval rate = 98.0%"
--   "Therapy approval rate = 71.7%"
--   ... etc.
--
-- Not all payers break down their data this way. When they don't,
-- we still store a single row with service_category = "ALL" to
-- hold the aggregate numbers. This way the table works for both
-- detailed and summary-only payers.
--
-- REAL EXAMPLE (Superior HealthPlan CHIP 2024):
--   service_category = "Imaging"
--   domain = "medical"
--   total_requests = 1517
--   approved_count = 1139
--   denied_count = 378
--   approved_pct = 75.1
--   denied_pct = 24.9
-- ====================================================================
CREATE TABLE IF NOT EXISTS service_level_stats (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Which report does this data come from?
    report_id INTEGER NOT NULL REFERENCES metrics_reports(id),

    -- What category of service? Examples:
    --   "Imaging", "Surgery", "Therapy", "Behavioral Health",
    --   "DME/Medical Supplies", "Medication", "Diagnostic Test",
    --   "Home Health", "Genetic Testing", "ALL" (aggregate)
    --
    -- NO CHECK constraint — payers use different category names.
    -- We normalize them as best we can, but new ones will appear.
    service_category TEXT NOT NULL,

    -- Is this medical services or prescription drugs?
    -- Payers report these completely separately (different PDFs,
    -- different tables, different metrics). We need to distinguish.
    --   "medical" = procedures, imaging, DME, therapy, etc.
    --   "rx"      = prescription drug PA
    --   "all"     = combined (if payer doesn't separate them)
    domain TEXT NOT NULL DEFAULT 'medical',

    -- Was this for standard (routine) or expedited (urgent) requests?
    -- Some payers break this down, others don't.
    --   "standard"  = non-urgent, 7-day decision window
    --   "expedited" = urgent, 72-hour decision window
    --   "all"       = combined (most common in current data)
    urgency_type TEXT NOT NULL DEFAULT 'all',

    -- THE ACTUAL NUMBERS
    -- We store both counts AND percentages because:
    --   - Counts are ground truth (you can recompute percentages)
    --   - But some payers only give percentages (no raw counts)
    --   - So both can be NULL independently

    -- How many PA requests were submitted for this service type?
    total_requests INTEGER,

    -- How many were approved?
    approved_count INTEGER,

    -- How many were denied? (also called "adverse determinations")
    denied_count INTEGER,

    -- Approval and denial rates as percentages (e.g., 75.1 for 75.1%)
    approved_pct REAL,
    denied_pct REAL,

    -- Any notes specific to this row
    notes TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ====================================================================
-- TABLE: denial_reasons
-- WHY were PA requests denied?
--
-- Each row = one reason category for denials, linked to either:
--   - A specific service type (via service_stat_id), OR
--   - The report as a whole (via report_id, when no service breakdown)
--
-- REAL EXAMPLE (Oscar Health TX 2024, Medications):
--   reason_category = "medical_necessity"
--   denial_count = 549
--   denial_pct = 97.5  (of all medication denials)
--
-- REAL EXAMPLE (Superior CHIP 2024, Imaging):
--   reason_category = "non_covered_benefit"
--   denial_count = NULL  (they gave percentage only)
--   denial_pct = 3.6
--
-- Common reason categories we've seen so far:
--   "medical_necessity"      — doesn't meet clinical guidelines
--   "administrative"         — paperwork issue, not clinical
--   "experimental"           — treatment considered experimental
--   "non_covered_benefit"    — plan simply doesn't cover this
--   "quantity_limit"         — exceeds allowed amount (Rx)
--   "non_formulary"          — drug not on the approved drug list
--   "trial_failure_required" — must try cheaper drug first (step therapy)
-- ====================================================================
CREATE TABLE IF NOT EXISTS denial_reasons (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Link to a specific service breakdown row (preferred when available).
    -- Can be NULL if this reason applies to the report as a whole.
    service_stat_id INTEGER REFERENCES service_level_stats(id),

    -- Link to the report directly (used when no service breakdown exists).
    -- At least one of service_stat_id or report_id should be filled.
    report_id INTEGER REFERENCES metrics_reports(id),

    -- What was the reason for denial?
    -- NO CHECK constraint — new reasons will appear from different payers.
    -- We use standardized lowercase_with_underscores where possible.
    reason_category TEXT NOT NULL,

    -- How many denials had this reason?
    denial_count INTEGER,

    -- What percentage of denials had this reason?
    denial_pct REAL,

    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ====================================================================
-- TABLE: appeal_outcomes
-- What happened when denied requests were APPEALED?
--
-- This is critical data. If a payer denies 30% of requests but 50%
-- of appeals are overturned, that suggests the denials were wrong —
-- the payer is wasting everyone's time and money.
--
-- Two types of appeals:
--   "internal" — the payer reviews their own denial (first step)
--   "external_iro" — an Independent Review Organization reviews it
--                     (second step, like a court of appeals)
--
-- REAL EXAMPLE (Oscar Health TX Rx 2024):
--   appeal_type = "internal"
--   total_appeals = 1259
--   overturned_count = 624
--   upheld_count = 635
--   overturn_pct = 49.6  (basically a coin flip!)
-- ====================================================================
CREATE TABLE IF NOT EXISTS appeal_outcomes (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Link to a specific service breakdown row (when available)
    service_stat_id INTEGER REFERENCES service_level_stats(id),

    -- Link to the report directly (when no service breakdown)
    report_id INTEGER REFERENCES metrics_reports(id),

    -- What type of appeal was this?
    --   "internal"     — reviewed by the payer themselves
    --   "external_iro" — reviewed by an Independent Review Organization
    --   "all"          — combined (if payer doesn't separate them)
    appeal_type TEXT NOT NULL DEFAULT 'all',

    -- How many denials were appealed in total?
    total_appeals INTEGER,

    -- How many appeals resulted in the denial being OVERTURNED (approved)?
    overturned_count INTEGER,

    -- How many appeals were UPHELD (denial stands)?
    upheld_count INTEGER,

    -- Overturn rate as a percentage
    overturn_pct REAL,

    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ====================================================================
-- TABLE: diagnosis_pa_volume
-- Which DIAGNOSES (medical conditions) drive the most PA requests?
--
-- This tells us what conditions are most burdened by prior auth.
-- If "hypertension" (high blood pressure) is the #1 diagnosis
-- triggering PA, that's a common condition being gatekept — worth
-- investigating whether that PA requirement serves any purpose.
--
-- Uses ICD-10 codes — the international system for classifying
-- diseases. Every diagnosis has a code (e.g., I10 = hypertension).
-- You'll learn these in med school.
--
-- REAL EXAMPLE (Oscar Health TX Rx 2024):
--   icd10_code = "I10"
--   description = "Essential (primary) hypertension"
--   pct_of_total_volume = 1.60
--   rank = 2
-- ====================================================================
CREATE TABLE IF NOT EXISTS diagnosis_pa_volume (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Which report does this come from?
    report_id INTEGER NOT NULL REFERENCES metrics_reports(id),

    -- The ICD-10 diagnosis code (e.g., "I10", "E11.9", "F41.1")
    icd10_code TEXT,

    -- Human-readable description of the diagnosis
    description TEXT,

    -- What percentage of total PA volume was for this diagnosis?
    pct_of_total_volume REAL,

    -- Rank in the list (1 = most common, 2 = second most, etc.)
    rank INTEGER,

    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ====================================================================
-- TABLE: prescriber_stats
-- WHO is submitting PA requests?
--
-- Tracks the types of healthcare providers (MD, NP, DO, PA) and
-- their specialties (Family Practice, Cardiology, etc.) that submit
-- the most PA requests.
--
-- This data can reveal whether PA burden falls disproportionately
-- on primary care vs. specialists, or on physicians vs. mid-levels.
--
-- REAL EXAMPLE (Oscar Health TX Rx 2024):
--   prescriber_type = "MD"
--   specialty = NULL
--   rank = 1
--
--   prescriber_type = NULL
--   specialty = "Family Practice"
--   rank = 2
-- ====================================================================
CREATE TABLE IF NOT EXISTS prescriber_stats (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Which report does this come from?
    report_id INTEGER NOT NULL REFERENCES metrics_reports(id),

    -- Type of prescriber (e.g., "MD", "DO", "NP", "PA")
    -- Can be NULL if this row is about specialty instead
    prescriber_type TEXT,

    -- Medical specialty (e.g., "Family Practice", "Cardiology")
    -- Can be NULL if this row is about prescriber type instead
    specialty TEXT,

    -- What percentage of PA requests came from this type/specialty?
    pct_of_total REAL,

    -- Rank (1 = submits the most PA requests)
    rank INTEGER,

    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
