# ClearPath Health
## Prior Authorization Efficiency Benchmarking & Research Institute
### Comprehensive Project Plan, Constitution & Resource Guide — v2

**Working Name:** ClearPath Health

**Mission:** To use publicly mandated prior authorization data to identify system-wide inefficiencies, benchmark best practices, recognize industry leaders, and publish evidence-based recommendations that reduce waste for payers, administrative burden for physicians, and barriers to care for patients.

**Core Belief:** The prior authorization system wastes billions of dollars annually through process failures that harm every stakeholder — payers, providers, patients, and policymakers alike. Public data, rigorously analyzed and accessibly presented, is the fastest path to a system that works for everyone.

---

## Part 1: The Problem (Why Everyone Loses Today)

### What we know from the data

**Payers lose money:**
- 82% of PA denials are overturned on appeal when properly managed (CMS data) — meaning the initial denial was double-processing that produced the same outcome at higher cost
- PA adjudication costs the healthcare system ~$19.7 billion annually (industry estimates, 2024)
- Poor PA practices hurt Medicare Advantage Star ratings, which directly affect bonus payments
- UnitedHealthcare has already voluntarily cut PA volume by ~30% since 2023 because they identified the waste internally

**Physicians lose time:**
- Physicians spend an average of 16.4 hours/week on PA tasks — 853 hours/year per provider (AMA)
- The average practice submits 43 PA requests per week (AMA)
- 35% of practices have staff dedicated solely to PA (AMA 2023 survey)
- That staff time cost gets passed back into the system as higher healthcare costs

**Patients lose access:**
- 94% of physicians report care delays due to PA denials (AMA 2023)
- 78% say patients abandon treatment after PA denial (AMA 2023)
- Only ~11% of denials are actually appealed, despite the 82% overturn rate — a massive information gap
- National denial rates hover around 12% (Optum 2024 Revenue Cycle Denials Index)
- Medicare Advantage alone denied 3.2 million of ~50 million PA requests in one year (KFF 2023)

**The system loses trust:**
- PA is the #1 administrative complaint from physicians about insurance companies
- Patient satisfaction scores (CAHPS) are dragged down by PA friction
- Bipartisan congressional action is being driven by the scale of the problem
- CMS estimates $15 billion in savings over 10 years from its interoperability reforms alone

### The opportunity: data that didn't exist before

The CMS Interoperability and Prior Authorization Final Rule (CMS-0057-F) creates mandatory public reporting for the first time. Payers must now publish their PA data. But publishing data and making it *useful* are different things. Nobody is collecting this data across all payers, normalizing it, analyzing patterns, and publishing actionable insights.

That's what ClearPath Health does.

---

## Part 2: Verified Regulatory Foundation

### Source Rule
CMS Interoperability and Prior Authorization Final Rule (CMS-0057-F), finalized January 17, 2024.

### Impacted Payers
Medicare Advantage organizations, state Medicaid and CHIP fee-for-service programs, Medicaid managed care plans, CHIP managed care entities, and Qualified Health Plan issuers on the Federally Facilitated Exchanges.

### Timeline of Requirements

**Already in effect (January 1, 2026):**
- Payers must issue PA decisions within 72 hours (expedited) and 7 calendar days (standard)
- Payers must provide specific reasons for denied PA decisions
- Payers must begin collecting PA metrics for public reporting

**March 31, 2026 — First Public Reporting Deadline:**
- Payers must post CY2025 prior authorization metrics on their public-facing websites
- This is the data that ClearPath Health will collect and analyze

**The 8 required public metrics:**
1. A list of all items and services that require prior authorization (excluding drugs)
2. Percentage of standard PA requests approved
3. Percentage of standard PA requests denied
4. Percentage of standard PA requests approved after appeal
5. Percentage of PA requests where timeframe was extended, then approved
6. Percentage of expedited PA requests approved
7. Percentage of expedited PA requests denied
8. Average and median elapsed time between submission and decision (standard and expedited)

**Reporting levels:**
- MA organizations → contract level
- State Medicaid/CHIP FFS → state level
- Medicaid managed care plans/CHIP managed care entities → plan level
- QHP issuers on FFEs → issuer level

**January 1, 2027:**
- Prior Authorization FHIR API must be implemented
- API must identify which services require PA, documentation requirements, and support request/response with specific denial reasons
- Provider Access API and Payer-to-Payer API also required

### Political Context

The Trump administration suspended some granular reporting requirements (service-level breakdowns, health equity analyses by social risk factor, plan-level vs. contract-level detail for MA). However, the core 8 metrics and March 31, 2026 public reporting deadline remain in force.

This means: independent analysis and benchmarking is *more* valuable, not less. Where government pulled back, ClearPath Health fills the gap — not as an adversary, but as a resource that helps all stakeholders make sense of the data.

### Verify Everything — Primary Source Links

| What | URL |
|------|-----|
| CMS Final Rule fact sheet | https://www.cms.gov/newsroom/fact-sheets/cms-interoperability-prior-authorization-final-rule-cms-0057-f |
| CMS Final Rule press release | https://www.cms.gov/newsroom/press-releases/cms-finalizes-rule-expand-access-health-information-and-improve-prior-authorization-process |
| CMS Prior Auth API FAQ | https://www.cms.gov/priorities/burden-reduction/overview/interoperability/frequently-asked-questions/prior-authorization-api |
| CMS Metrics Reporting Template (PDF) | https://www.cms.gov/files/document/prior-authorization-metrics-reporting-overview-template.pdf |
| CMS-0057-F full rule text (PDF) | https://www.cms.gov/files/document/cms-0057-f.pdf |
| CMS rule overview page | https://www.cms.gov/cms-interoperability-and-prior-authorization-final-rule-cms-0057-f |
| Georgetown analysis of suspended rules | https://medicare.chir.georgetown.edu/cms-suspends-new-medicare-advantage-prior-authorization-transparency-rules-amid-public-concerns-about-care-denials/ |
| KFF prior auth analysis | https://www.kff.org/private-insurance/final-prior-authorization-rules-look-to-streamline-the-process-but-issues-remain/ |
| AMA prior auth transparency page | https://www.ama-assn.org/practice-management/prior-authorization/fixing-prior-auth-clear-what-s-required-and-when |
| MassHealth state implementation example | https://www.mass.gov/info-details/prior-authorization-process-changes-and-metrics |
| UHC PA reduction announcements | https://www.uhc.com/news-articles/newsroom/easing-prior-authorizations |
| UHC Gold Card Program details | https://www.uhcprovider.com/en/prior-auth-advance-notification/adv-notification-plan-reqs.html |

---

## Part 3: Value Proposition by Stakeholder

### For Payers: Competitive Benchmarking & Waste Identification

**What ClearPath gives them:**
- Independent benchmarking against peers (denial rates, turnaround times, appeal overturn rates)
- Identification of PA requirements that produce 90%+ approval rates — candidates for elimination that save processing costs
- Public recognition for efficiency improvements (annual "PA Efficiency Leaders" report)
- Data to support Gold Card-style programs by showing which PA codes have near-universal approval
- Evidence to present to their own boards that PA streamlining saves money

**Why they cooperate:**
- UnitedHealthcare already cut PA volume by ~30% voluntarily and promotes this publicly — they *want* recognition
- Better PA practices improve Star ratings (directly affects MA bonus payments)
- Payers who are early adopters of efficiency get positive press; laggards get compared unfavorably — but the comparison is constructive, not adversarial
- Voluntary data sharing beyond the CMS minimum earns them a deeper profile in the benchmark report

**The pitch to a payer executive:**
"We're building the independent benchmark for PA efficiency. Your competitors are being measured whether they participate or not — but payers who voluntarily share additional data get a more complete and favorable profile. UHC's Gold Card program is exactly the kind of innovation we highlight."

### For Physicians & Medical Associations: Evidence for Advocacy

**What ClearPath gives them:**
- Data-driven evidence replacing anecdotes: "Payer X takes 6.2 days average for standard PA decisions while Payer Y takes 2.1 days — here's what Y does differently"
- Identification of PA requirements that serve no gatekeeping purpose (95%+ approval = rubber stamp with paperwork)
- Payer-specific guides: which payers are easiest to work with, which have the most streamlined processes
- Evidence for contract negotiations with payers
- Research publications for academic physicians interested in health policy

**The pitch to a medical association:**
"We turn the new CMS-mandated PA data into the evidence base your advocacy has been missing. Instead of '94% of physicians report delays' — which payers can dismiss as subjective — you can say 'Payer X denies cardiac imaging at 3x the rate of Payer Y with identical overturn rates on appeal, costing the system $X million in unnecessary processing.'"

### For Patients & Patient Advocates: Information & Empowerment

**What ClearPath gives them:**
- Plain-language guides: "Your insurer denied your request. Here's what the data says about your chances on appeal" (hint: very good)
- Payer comparison tools: if you're choosing a plan during open enrollment, see which payers have the fastest PA turnaround and highest approval rates
- Rights education: most patients don't know they can appeal, or that 82% of appeals succeed
- Closing the information gap that causes 89% of patients to *not* appeal valid denials

**The pitch to a patient advocacy org:**
"We help your members understand which plans actually approve care efficiently and what to do when they don't. Every data point we publish is grounded in the payers' own mandatory disclosures."

### For Policymakers: Evidence for Smarter Regulation

**What ClearPath gives them:**
- Compliance monitoring: which payers published on time, which formats are they using, is the data complete?
- Outcome measurement: are the CMS 2026 rules actually changing behavior? (Baseline data from first year enables future comparison)
- Evidence for future rulemaking: where are the biggest remaining inefficiencies?
- State-level analysis: how do Medicaid managed care PA practices vary by state?

**The pitch to a congressional staffer:**
"We're the independent data source for prior authorization system performance. When your member needs to cite PA statistics in a hearing or a bill, we have the payer-specific, publicly verifiable numbers."

---

## Part 4: Organizational Constitution

### Article I — Name and Purpose

**Section 1.** The name of this organization shall be ClearPath Health, a Texas nonprofit corporation.

**Section 2.** The purpose of this organization is exclusively charitable, scientific, and educational within the meaning of Section 501(c)(3) of the Internal Revenue Code. Specifically, the organization exists to:

(a) Collect and aggregate publicly available prior authorization data disclosed by health insurance payers pursuant to federal and state transparency mandates;

(b) Analyze such data to identify system-wide inefficiencies, benchmark best practices, and measure the impact of regulatory reforms on all stakeholders;

(c) Publish accessible, free public reports that help payers identify opportunities to reduce unnecessary PA processing costs, help physicians reduce administrative burden, help patients understand their rights and make informed plan choices, and help policymakers craft evidence-based regulations;

(d) Recognize and promote industry-leading PA practices that demonstrate alignment between cost efficiency, care quality, and patient access;

(e) Conduct and publish peer-reviewed research on prior authorization system performance, healthcare administrative waste, and evidence-based approaches to utilization management.

**Section 3.** The organization shall maintain a nonpartisan, multi-stakeholder approach. It shall not advocate for or against any individual payer, provider, or political candidate. Its publications shall present data accurately and in context, with constructive recommendations directed at system improvement.

**Section 4.** No part of the net earnings of the organization shall inure to the benefit of any director, officer, or private individual. The organization shall not participate in any political campaign on behalf of or in opposition to any candidate for public office.

**Section 5.** Upon dissolution, assets shall be distributed exclusively to organizations that qualify as exempt under Section 501(c)(3) of the Internal Revenue Code.

### Article II — Board of Directors

**Section 1.** The board shall consist of no fewer than three (3) and no more than nine (9) directors.

**Section 2.** The board should strive for multi-stakeholder representation, including individuals with experience in: clinical medicine, health insurance operations, health policy research, patient advocacy, data science, and/or health law.

**Section 3.** Directors shall serve two-year terms and may be reappointed.

**Section 4.** The board shall meet at least quarterly. Meetings may be held electronically.

**Section 5.** A majority of directors shall constitute a quorum.

### Article III — Officers

**Section 1.** Officers shall include a President, Secretary, and Treasurer. One person may hold multiple offices except President and Secretary simultaneously.

**Section 2.** Officers shall be elected by the board at the annual meeting and serve one-year terms.

### Article IV — Editorial Independence & Methodology Integrity

**Section 1.** All data collection methodologies, analysis code, and raw collected data shall be published openly and made freely available.

**Section 2.** No funder, partner, or data-sharing payer shall have editorial control or pre-publication review rights over ClearPath Health reports. Partners may be offered the opportunity to review data for factual accuracy before publication, but not to alter findings, conclusions, or recommendations.

**Section 3.** Any voluntary data shared by payers beyond CMS requirements shall be clearly labeled as voluntarily provided and distinguished from mandatory public disclosures.

### Article V — Conflict of Interest Policy

**Section 1.** Any director or officer with a financial or personal interest in a matter before the board must disclose the interest and recuse themselves from discussion and vote.

**Section 2.** The board shall document all conflict disclosures in meeting minutes.

**Section 3.** No director or officer shall simultaneously serve as an employee, consultant, or board member of an insurance company or healthcare payer while serving on the ClearPath Health board.

### Article VI — Amendments

These bylaws may be amended by a two-thirds vote of the board at any regular or special meeting, provided written notice of the proposed amendment is given at least 14 days in advance.

---

## Part 5: Nonprofit Formation (Texas)

### Formation Checklist & Costs

| Step | Action | Cost | Time |
|------|--------|------|------|
| 1 | Hold initial board meeting, adopt mission, appoint officers | $0 | Day 1 |
| 2 | Apply for EIN online (IRS) | $0 | Instant |
| 3 | File Certificate of Formation (Form 202) with Texas SOS | $25 | 2-5 days |
| 4 | Adopt bylaws (internal, not filed with state) | $0 | Day 1 |
| 5 | File Form 1023-EZ with IRS for 501(c)(3) status | $275 | 2-4 weeks |
| 6 | Apply for TX franchise tax exemption (Comptroller) | $0 | Varies |
| **Total** | | **$300** | **~1 month** |

### Key Formation Links

| What | URL |
|------|-----|
| Texas SOS nonprofit page | https://www.sos.state.tx.us/corp/nonprofit_org.shtml |
| Texas SOS Form 202 (Certificate of Formation) | https://www.sos.state.tx.us/corp/forms/202_boc.pdf |
| SOSDirect (online filing) | https://www.sos.state.tx.us/corp/sosda/index.shtml |
| IRS EIN application | https://www.irs.gov/businesses/small-businesses-self-employed/apply-for-an-employer-identification-number-ein-online |
| IRS Form 1023-EZ | https://www.irs.gov/forms-pubs/about-form-1023-ez |
| IRS exempt purposes guide | https://www.irs.gov/charities-non-profits/charitable-organizations/exempt-purposes-internal-revenue-code-section-501c3 |
| TX Comptroller franchise tax exemption | https://comptroller.texas.gov/taxes/exempt/ |

### Critical Formation Notes

- Texas requires minimum 3 directors
- The state Certificate of Formation template does NOT include IRS-required language — you must add a dissolution clause and purpose statement that meets 501(c)(3) requirements
- Texas has no state income tax; 501(c)(3)s are also exempt from franchise tax
- Form 1023-EZ is appropriate if you expect revenue under $50K/year for first 3 years (you will)

---

## Part 6: 90-Day Launch Plan

### Phase 1: Foundation (Days 1-14)

**Week 1: Legal setup**
- [ ] Recruit 2 additional board members (target profiles below)
- [ ] Apply for EIN online
- [ ] File Certificate of Formation with Texas SOS ($25)
- [ ] Hold initial board meeting, adopt bylaws and mission

**Week 2: Infrastructure**
- [ ] Open bank account
- [ ] File Form 1023-EZ ($275)
- [ ] Register domain (clearpath-health.org or similar)
- [ ] Set up GitHub organization (all code and data will be open source)
- [ ] Create organizational email

### Phase 2: Data Collection MVP (Days 15-45)

**Week 3-4: Build the collector**
- Compile master list of impacted payers by type and enrollment size
- Start with top 20 MA organizations by enrollment
- Manually locate their published CY2025 PA metrics on their websites
- Build collection pipeline:
  - Semi-automated web scraping (Python + BeautifulSoup/Selenium)
  - Manual collection backup spreadsheet for sites that resist scraping
  - Data normalization scripts (payers will use different formats)
  - Structured storage (PostgreSQL or SQLite)

**Week 5-6: First collection round**
- Collect published metrics from top 20 MA organizations
- Collect metrics from Texas Medicaid (your home state, first priority)
- Expand to other large state Medicaid programs
- Document compliance: who published on time, who hasn't, which formats are being used
- Note: CMS has published a recommended template — track who uses it vs. custom formats

### Phase 3: Analysis & First Report (Days 46-75)

**Week 7-8: Build analysis pipeline**
- Comparative analysis across payers:
  - Denial rate distributions
  - Turnaround time comparisons
  - Appeal overturn patterns
  - PA requirement volume by payer
- Efficiency identification:
  - Which payers have the fastest turnaround?
  - Which have the lowest denial rates? What might they be doing differently?
  - Where do high denial + high overturn rates suggest wasteful PA requirements?
- Compliance assessment:
  - Who published on time?
  - Whose data matches the CMS template?
  - What's missing or ambiguous?

**Week 9-10: Draft inaugural report**

**Report Title:** "The State of Prior Authorization Efficiency: What the First Year of Mandatory Data Reveals"

**Report Structure:**
1. Executive Summary (1 page, plain language, all stakeholders)
2. Why This Matters: The $19.7B waste problem and how data can fix it
3. Methodology: How we collected, what we measured, limitations
4. Industry Snapshot: aggregate findings across all collected payers
5. Efficiency Leaders: payers with best practices worth emulating
   - Fastest turnaround times
   - Lowest denial rates
   - Most streamlined PA requirement lists
   - Best Gold Card or provider-exemption programs
6. Opportunities for Improvement: patterns suggesting systemic waste
   - PA requirements with 90%+ approval rates (candidates for elimination)
   - Payers with high denial rates and high appeal overturn rates (double-processing waste)
   - Significant turnaround time variation for similar services
7. Compliance Report: who published, who didn't, format assessment
8. For Patients: plain-language guide to understanding your PA rights
9. Recommendations:
   - For payers: specific waste-reduction opportunities from the data
   - For physicians: how to use this data in contracting and advocacy
   - For policymakers: where the 2026 rules are working and where gaps remain
10. Methodology Appendix & Data Access (link to GitHub)

### Phase 4: Launch & Distribution (Days 76-90)

**Week 11: Soft launch**
- Publish report on website (free, open access)
- Publish all code and collected data on GitHub (open source)
- Send advance copies to key stakeholders for feedback

**Week 12-13: Distribution & relationship building**

*Academic:*
- Frame methodology for health policy journal submission (Health Affairs Blog, JAMA Health Forum)
- Connect with faculty advisor at medical school
- Present at any upcoming health policy events

*Industry — payers:*
- Send report to community benefit / government affairs teams at profiled payers
- Specifically highlight efficiency leaders with positive framing
- Invite payers to voluntarily share additional data for next year's deeper profile

*Physician community:*
- Share with AMA, state medical associations (Texas Medical Association first)
- Offer to present findings to medical society meetings

*Patient advocacy:*
- Share with disease-specific patient organizations (chronic conditions are most PA-impacted)
- Create shareable social media graphics from key patient-facing findings

*Policy:*
- Share with congressional offices working on PA legislation
- Share with CMS directly (they want to know if their rule is working)

*Media:*
- Pitch to health policy journalists (KFF Health News, STAT News, Becker's)
- The "first independent analysis of new mandatory PA data" is a genuinely novel story

---

## Part 7: Technical Architecture

### MVP Stack

```
Data Collection:
├── Python scraping scripts (BeautifulSoup / Selenium)
├── Manual collection spreadsheet (backup)
├── CMS metrics template parser
└── Scheduled monitoring for new/updated postings

Data Storage:
├── SQLite → PostgreSQL (as volume grows)
├── Tables: payers, metrics_reports, data_points, compliance_checks, pa_requirements
├── GitHub repo for all code and raw data (open source)
└── Version-controlled data snapshots for reproducibility

Analysis:
├── Python (pandas, scipy for statistical comparisons)
├── Visualization (matplotlib, plotly)
├── Claude API for narrative generation and plain-language translation
└── Automated benchmarking and outlier detection

Output:
├── Static website (GitHub Pages — free)
├── Annual report (PDF + HTML)
├── Interactive payer comparison tool (Phase 2)
├── Patient-facing PA rights guide (Phase 2)
└── Researcher API (Phase 3)
```

### Core Data Model

```sql
-- Payers in the system
payers (
  id, name, type [MA|Medicaid|CHIP|QHP],
  parent_org, state, enrollment_size, website_url
)

-- Annual metrics reports (one per payer per year)
metrics_reports (
  id, payer_id, reporting_year, date_published,
  source_url, screenshot_path, compliant BOOL,
  format_used [CMS_template|custom|PDF|HTML],
  notes
)

-- Individual data points from each report
data_points (
  id, report_id,
  metric_type [std_approved|std_denied|std_appeal_approved|
               ext_approved|exp_approved|exp_denied|
               avg_time_std|median_time_std|
               avg_time_exp|median_time_exp],
  value NUMERIC,
  notes
)

-- PA requirement lists (what services each payer requires PA for)
pa_requirements (
  id, payer_id, effective_date,
  service_category, cpt_codes,
  source_url
)

-- Compliance tracking
compliance_checks (
  id, payer_id, check_date,
  published BOOL, on_time BOOL,
  format_compliant BOOL, data_complete BOOL,
  notes
)
```

---

## Part 8: Risk Mitigation (Updated for Win-Win Framing)

### Legal (Minimal Risk)

1. **Only use publicly mandated data.** Never solicit, receive, or handle PHI.
2. **Methodology transparency.** All code, data, and methods published openly. Errors can be caught and corrected quickly.
3. **Constructive language.** Report findings as benchmarking — "Payer X's published data shows faster turnaround than the industry average" — not accusations.
4. **Offer pre-publication factual review.** Let profiled payers check that you've correctly captured their data before publishing. This is standard practice in research and builds trust. They cannot change your analysis or conclusions.
5. **Legal advisor.** Have a health law attorney (ideally pro bono via medical school) review your first report.

### Reputational

1. **Multi-stakeholder board.** Having someone with payer experience on your board signals this isn't adversarial.
2. **Efficiency Leaders recognition.** Payers want to be on this list. It creates positive incentive to cooperate.
3. **Article IV of bylaws (Editorial Independence).** Protects credibility by ensuring no funder or partner has editorial control. You can be collaborative without being captured.

### Operational

1. **Design for a medical school schedule.** Annual data cycle (March 31 publish → May-June report) gives natural sprints with recovery time.
2. **Automate everything possible.** The scraper and analysis pipeline should run with minimal manual intervention after Year 1.
3. **Recruit MPH/health policy student collaborators.** They need capstone projects; you need hands.
4. **D&O insurance.** $500-1,500/year for small nonprofits. Get it once you publish your first report.

---

## Part 9: Funding Strategy

### Year 1: Bootstrap ($300-2,000)

- $300 formation costs (personal)
- Medical school innovation/community health grants ($500-2,000)
- No external fundraising needed

### Year 2+: Grant-Ready

**Health system improvement funders (perfect fit for win-win framing):**
- Robert Wood Johnson Foundation (health system efficiency)
- Arnold Ventures (healthcare transparency)
- Commonwealth Fund (health system performance measurement)
- Peterson Center on Healthcare (cost reduction and efficiency)
- AHIP Foundation (yes — the insurer trade group funds research on PA improvement)

**Academic/research funders:**
- AHRQ (Agency for Healthcare Research and Quality)
- State health foundations
- AMA Foundation medical student grants

**The win-win framing makes you fundable by both sides.** A watchdog can only take money from one side. A benchmarking institute can take money from health foundations, insurer associations, AND physician groups without compromising credibility — as long as editorial independence (Article IV) is ironclad.

---

## Part 10: Growth Roadmap

### Year 1: Prove the Concept
- Collect and analyze first round of mandatory CY2025 metrics
- Publish inaugural benchmarking report
- Establish credibility with 1-2 media citations or academic submissions
- Build relationships with 2-3 payers willing to share additional data voluntarily

### Year 2: Expand & Deepen
- Add Phase 2: plain-language patient tools (PA rights guides, payer comparison for open enrollment)
- Collect data from all 50 state Medicaid programs
- Build interactive public dashboard
- Launch annual "PA Efficiency Leaders" recognition
- Begin monitoring 2027 Prior Authorization API data
- Second annual report with year-over-year trend analysis

### Year 3: Become the Reference
- Annual "State of Prior Authorization" report becomes an anticipated industry publication
- Cited in congressional testimony, medical association policy documents, payer strategic plans
- Research partnerships with health services researchers
- Expand scope to monitor payer AI use in PA decisions (emerging area)
- Launch consulting arm: help smaller payers benchmark and improve (earned revenue)

---

## Part 11: Board Recruitment Strategy

### Ideal Initial Board (3 minimum, 5 ideal)

| Role | Why | Where to Find |
|------|-----|---------------|
| You (Founder/President) | Vision, medical credibility, tech capability | — |
| Health policy researcher | Methodology credibility, academic network, publication guidance | Medical school faculty, school of public health |
| Practicing physician | Real-world PA experience, clinical credibility, AMA connections | Medical school clinical faculty, state medical association |
| Data/tech person | Technical infrastructure, analysis quality | CS/data science grad student, tech professional interested in health |
| (Phase 2) Someone with payer experience | Industry credibility, ensures reports are fair and useful to payers | Former insurer medical director, healthcare consulting, AHIP network |

### Faculty Advisor Pitch (Updated for Win-Win)

"I'm an incoming MS1 building a nonprofit research institute that benchmarks prior authorization efficiency across payers using the new CMS-mandated transparency data. The first reporting deadline was March 31, 2026, and I'm building the data collection and analysis infrastructure now. The goal isn't adversarial — it's to identify system-wide waste that costs payers money, physicians time, and patients access, then publish constructive, evidence-based recommendations. I'd value your guidance on methodology and the opportunity to develop this into a publishable research project."

---

## Part 12: Annual Publication Calendar

| Month | Activity |
|-------|----------|
| January-February | Prepare collection infrastructure for upcoming data cycle |
| March | CMS reporting deadline (March 31). Begin data collection immediately. |
| April | Complete data collection across all tracked payers. Quality check. |
| May | Analysis and report drafting. Pre-publication factual review by profiled payers. |
| June | Publish annual benchmarking report. Media and distribution push. |
| July-August | Academic submission (journal article). Conference presentations. |
| September-October | Relationship building with payers for voluntary data sharing. Board planning. |
| November-December | Open enrollment patient tools. Year-end review. Prepare for next cycle. |

This calendar is deliberately designed around a medical school schedule — the heaviest work (April-June) falls during summer between MS1 and MS2.

---

## Part 13: How to Describe This to Different Audiences

**To a payer executive:**
"We're building the independent PA efficiency benchmark. We recognize leaders, identify waste that costs you money, and help the industry move toward best practices. UHC's Gold Card program is exactly the kind of innovation we highlight."

**To a physician:**
"We turn the new mandatory PA data into the evidence your advocacy needs. Not anecdotes — specific, payer-level, publicly verifiable data about who denies what, how fast they respond, and how often appeals succeed."

**To a patient:**
"We help you understand which health plans process your care requests fastest and what to do if your request is denied. Most people don't know that the vast majority of denials are overturned on appeal — we want to change that."

**To a journalist:**
"We're the first independent organization collecting and analyzing the new CMS-mandated prior authorization transparency data across all major payers. This data has never existed before in public. We can give you the numbers."

**To a faculty advisor:**
"This is a health services research project housed in a 501(c)(3), designed to produce peer-reviewed publications while creating a public good. The data pipeline and methodology are reproducible and open source."

**To a grant funder:**
"We reduce healthcare administrative waste by making mandatory transparency data actionable. Every unnecessary prior authorization we help eliminate saves payers processing costs, physicians time, and patients access to care."

---

*Document prepared March 24, 2026. All regulatory information verified against primary CMS sources. All links active at time of creation. This is v2, incorporating the multi-stakeholder win-win framing.*
