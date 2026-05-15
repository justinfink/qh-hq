"""Named executives, customer leaders, and partners. Sourced from research dossiers.
All publicly available via LinkedIn, press releases, or org websites.
"""
from __future__ import annotations

# Format: (org_name, name, title, role_category, linkedin_url, notes)
CONTACTS: list[dict] = [
    # QH leadership
    {"org": "Qualified Health", "name": "Justin Norden, MD MBA MPhil", "title": "Co-founder & CEO",
     "role_category": "ceo",
     "linkedin": "https://www.linkedin.com/in/justin-norden",
     "notes": "Stanford MD/MBA. Adjunct Stanford Medicine. Prior: Trustworthy AI (acq Waymo), GSR Ventures partner, Apple Health."},
    {"org": "Qualified Health", "name": "Kedar Mate, MD", "title": "Co-founder & Chief Medical Officer",
     "role_category": "cmo",
     "linkedin": "https://www.linkedin.com/in/kedarmatemd",
     "notes": "Former President & CEO of Institute for Healthcare Improvement (IHI). Weill Cornell faculty."},
    {"org": "Qualified Health", "name": "Shantanu Phatakwala", "title": "Co-founder & Chief Commercial Officer",
     "role_category": "cco",
     "linkedin": None,
     "notes": "Prior: Haven Chief Data Science Officer; Evolent VP R&D; Resolution Health (acq Anthem)."},
    {"org": "Qualified Health", "name": "Beau Norgeot, PhD", "title": "Co-founder & Chief AI Officer",
     "role_category": "cto",
     "linkedin": None,
     "notes": "Prior: VP of AI at Elevance Health (NYSE: ELV). UCSF PhD, AI/ML & personalized medicine."},
    {"org": "Qualified Health", "name": "Nirav R. Shah, MD MPH", "title": "Co-founder",
     "role_category": "advisor",
     "linkedin": None,
     "notes": "Former COO Kaiser Permanente Southern California. Former NY State Health Commissioner. Stanford Medicine faculty."},
    {"org": "Qualified Health", "name": "Nicholas Chedid, MD MBA", "title": "Associate Chief Medical Officer",
     "role_category": "leadership",
     "linkedin": None, "notes": "Visible via UC Berkeley Haas recruiting."},
    {"org": "Qualified Health", "name": "Matthew Lungren, MD MPH", "title": "GM Technical Advisor / Office of CTO",
     "role_category": "advisor",
     "linkedin": None,
     "notes": "Formerly Chief Scientific Officer, Microsoft Health & Life Sciences."},

    # Customers — UTMB
    {"org": "University of Texas System", "name": "Peter McCaffrey, MD", "title": "Chief AI & Digital Officer, UTMB",
     "role_category": "caio",
     "linkedin": None,
     "notes": "Quoted: 'The ROI has already exceeded expectations.' UTMB anchor exec for QH."},

    # Customers — Mercy
    {"org": "Mercy", "name": "Byron Yount", "title": "Mercy Health (operations)",
     "role_category": "operations",
     "linkedin": None,
     "notes": "Quoted on QH partnership: 'AI allows us to simplify complex workflows, anticipate patient needs earlier.'"},

    # Prospects — Cleveland Clinic
    {"org": "Cleveland Clinic", "name": "Rohit Chandra", "title": "Chief Digital Officer",
     "role_category": "cdo",
     "linkedin": None, "notes": "Active deployment of Bayesian Health (sepsis) + Hippocratic AI agents."},

    # Prospects — Mayo
    {"org": "Mayo Clinic", "name": "John Halamka, MD MS", "title": "President, Mayo Clinic Platform",
     "role_category": "platform_president",
     "linkedin": None, "notes": "Mayo Clinic Platform President. Drives Mayo's external AI program. Abridge enterprise customer."},

    # Prospects — HCA
    {"org": "HCA Healthcare", "name": "Mike Schlosser", "title": "Chief Technology Officer",
     "role_category": "cto",
     "linkedin": None, "notes": "HCA CTO. Multi-vendor AI footprint (Commure ambient, Google MedLM ED pilot)."},
    {"org": "HCA Healthcare", "name": "Mangesh Patil", "title": "Chief AI Officer",
     "role_category": "caio",
     "linkedin": None, "notes": "HCA's first CAIO. Multi-EHR enterprise — fits QH multi-EHR thesis."},

    # Prospects — Kaiser
    {"org": "Kaiser Permanente", "name": "Daniel Yang, MD", "title": "VP, AI / Augmented Intelligence in Medicine",
     "role_category": "vp_ai",
     "linkedin": None, "notes": "Reports to CMO Andrew Bindman. Abridge enterprise deployment."},
    {"org": "Kaiser Permanente", "name": "Andrew Bindman, MD", "title": "Chief Medical Officer",
     "role_category": "cmo",
     "linkedin": None, "notes": "Kaiser CMO. Warm intro path via QH co-founder Nirav Shah (former Kaiser SoCal COO)."},

    # Prospects — Northwell
    {"org": "Northwell Health", "name": "Tom Manning", "title": "Chairman, Ascertain (Northwell AI venture)",
     "role_category": "ai_executive",
     "linkedin": None, "notes": "Aegis Ventures + Northwell collaboration. Active healthcare AI investor."},

    # Prospects — CommonSpirit
    {"org": "CommonSpirit Health", "name": "Daniel Barchi", "title": "Chief Information Officer",
     "role_category": "cio",
     "linkedin": None, "notes": "CommonSpirit CIO. Multi-EHR (Epic + Cerner) — highest-fit for QH multi-EHR thesis."},

    # Pharma — Pfizer
    {"org": "Pfizer", "name": "Lidia Fonseca", "title": "Chief Digital & Technology Officer",
     "role_category": "cdto",
     "linkedin": None, "notes": "Pfizer CDTO. Open to 30-min intro via DiMe contact."},
    {"org": "Pfizer", "name": "Berta Rodriguez-Hervas, PhD", "title": "Chief AI & Analytics Officer",
     "role_category": "caio",
     "linkedin": None, "notes": "Pfizer CAIO. Direct counterpart for governance discussions."},

    # Pharma — Lilly
    {"org": "Eli Lilly", "name": "Thomas Fuchs, PhD", "title": "Chief AI Officer",
     "role_category": "caio",
     "linkedin": None, "notes": "Lilly's first CAIO (appointed Oct 2024). High-priority pharma target."},

    # Pharma — AstraZeneca
    {"org": "AstraZeneca", "name": "Jim Weatherall, PhD", "title": "Chief Data Scientist",
     "role_category": "cds",
     "linkedin": None, "notes": "AstraZeneca clinical innovation flagged interest at HIMSS26."},

    # Partner — DiMe
    {"org": "Digital Medicine Society", "name": "Jennifer Goldsack", "title": "Co-founder & CEO",
     "role_category": "ceo",
     "linkedin": None, "notes": "Co-author of QH-DiMe AI Governance Toolkit announcement (4/15/2026)."},

    # Investor — NEA
    {"org": "New Enterprise Associates", "name": "Mohamad Makhzoumi", "title": "Co-CEO / Managing GP",
     "role_category": "investor",
     "linkedin": None, "notes": "Joined QH board on Series B."},

    # Competitor — Hippocratic
    {"org": "Hippocratic AI", "name": "Munjal Shah", "title": "Co-founder & CEO",
     "role_category": "ceo",
     "linkedin": None, "notes": "Polaris Safety Constellation Architecture is competitive framing vs QH."},
]

# V0.2 executive coverage. Keep this in the existing contacts table so the
# CRM integration path can replace/enrich records without a schema migration.
CONTACTS.extend([
    # Customers: executive buying committee coverage
    {"org": "University of Texas System", "name": "John M. Zerwas, MD", "title": "Chancellor",
     "role_category": "ceo", "linkedin": None,
     "notes": "Chief executive of UT System; system-level sponsor for cross-institution expansion."},
    {"org": "University of Texas System", "name": "Jonathan Pruitt", "title": "Executive Vice Chancellor and Chief Operating Officer",
     "role_category": "coo", "linkedin": None,
     "notes": "System operations owner; relevant to scaling QH from flagship institutions to enterprise standard."},
    {"org": "University of Texas System", "name": "David L. Lakey, MD", "title": "Vice Chancellor for Health Affairs and Chief Medical Officer",
     "role_category": "cmo", "linkedin": None,
     "notes": "Health affairs executive; likely clinical governance sponsor across UT health institutions."},
    {"org": "Emory Healthcare", "name": "Joon S. Lee, MD", "title": "Executive Vice President for Health Affairs & CEO, Emory Healthcare",
     "role_category": "ceo", "linkedin": None,
     "notes": "Enterprise CEO; strategic sponsor for generative-AI transformation and margin/outcomes story."},
    {"org": "Emory Healthcare", "name": "Christopher L. Augostini", "title": "Executive Vice President & Enterprise Chief Operating Officer",
     "role_category": "coo", "linkedin": None,
     "notes": "Enterprise COO; operational owner for workflow redesign and deployment scale."},
    {"org": "Jefferson Health", "name": "Joseph G. Cacchione, MD", "title": "CEO, Jefferson Health and Thomas Jefferson University",
     "role_category": "ceo", "linkedin": None,
     "notes": "System CEO; fiscal-pressure context makes CFO-friendly ROI proof important."},
    {"org": "Mercy", "name": "Steve Mackin", "title": "President and CEO",
     "role_category": "ceo", "linkedin": None,
     "notes": "Enterprise CEO; public quote path through Mercy's QH workflow redesign relationship."},
    {"org": "Mercy", "name": "Brian Day", "title": "Chief Financial Officer",
     "role_category": "cfo", "linkedin": None,
     "notes": "CFO appointed effective 2026; strong persona for RCM and margin-growth motion."},
    {"org": "University of Rochester Medicine", "name": "David C. Linehan, MD", "title": "CEO, University of Rochester Medical Center",
     "role_category": "ceo", "linkedin": None,
     "notes": "Medical center CEO; academic-system sponsor for enterprise AI standardization."},
    {"org": "NYC Health + Hospitals", "name": "Mitchell Katz, MD", "title": "President and CEO",
     "role_category": "ceo", "linkedin": None,
     "notes": "Largest U.S. public health system CEO; public-sector AI governance and safety scrutiny."},
    {"org": "NYC Health + Hospitals", "name": "Marlene Zurack", "title": "Corporate Chief Financial Officer",
     "role_category": "cfo", "linkedin": None,
     "notes": "Finance executive for public-system ROI and budget gating."},

    # Existing prospects: CEO/CFO/CIO plus empowered AI/digital owners where public
    {"org": "Cleveland Clinic", "name": "Tomislav Mihaljevic, MD", "title": "CEO and President",
     "role_category": "ceo", "linkedin": None,
     "notes": "Enterprise CEO; anchor for board-level AI safety and international governance narrative."},
    {"org": "Mayo Clinic", "name": "Gianrico Farrugia, MD", "title": "President and CEO",
     "role_category": "ceo", "linkedin": None,
     "notes": "Enterprise CEO; Mayo Platform relationship makes QH partner-versus-competitor framing sensitive."},
    {"org": "Mayo Clinic", "name": "Dennis E. Dahlen", "title": "Chief Financial Officer",
     "role_category": "cfo", "linkedin": None,
     "notes": "Finance executive; relevant to outcomes-tracking and sustained margin-growth proof."},
    {"org": "HCA Healthcare", "name": "Sam Hazen", "title": "Chief Executive Officer",
     "role_category": "ceo", "linkedin": None,
     "notes": "Enterprise CEO; scale makes HCA the highest-impact for-profit prospect."},
    {"org": "HCA Healthcare", "name": "Mike Marks", "title": "Executive Vice President and Chief Financial Officer",
     "role_category": "cfo", "linkedin": None,
     "notes": "CFO buyer for RCM, margin, and enterprise efficiency cases."},
    {"org": "Kaiser Permanente", "name": "Greg A. Adams", "title": "Chair and CEO",
     "role_category": "ceo", "linkedin": None,
     "notes": "Enterprise CEO; integrated payer-provider model maps to provider and payer QH motions."},
    {"org": "CommonSpirit Health", "name": "Wright Lassiter III", "title": "CEO",
     "role_category": "ceo", "linkedin": None,
     "notes": "Enterprise CEO; Catholic-system motion can leverage Mercy reference."},
    {"org": "CommonSpirit Health", "name": "Michael P. Browning", "title": "System SEVP and Chief Financial Officer",
     "role_category": "cfo", "linkedin": None,
     "notes": "CFO effective 2026; target for financial-strategy and operational-efficiency framing."},
    {"org": "Northwell Health", "name": "John D'Angelo", "title": "President and CEO",
     "role_category": "ceo", "linkedin": None,
     "notes": "Enterprise CEO; leadership transition creates strategic refresh window."},
    {"org": "Northwell Health", "name": "Sophy Lu", "title": "Senior Vice President and Chief Information Officer",
     "role_category": "cio", "linkedin": None,
     "notes": "CIO buyer for enterprise data, digital, and governed AI deployment."},

    # V0.2 added prospects
    {"org": "Hackensack Meridian Health", "name": "Robert C. Garrett", "title": "Chief Executive Officer",
     "role_category": "ceo", "linkedin": None,
     "notes": "Enterprise CEO; target for Northeast reference expansion and governance narrative."},
    {"org": "Hackensack Meridian Health", "name": "Joel Klein, MD", "title": "Chief Digital & Information Officer",
     "role_category": "cio", "linkedin": None,
     "notes": "New CDIO signal opens 6-12 month vendor evaluation window."},
    {"org": "AdventHealth", "name": "David Banks", "title": "President and CEO",
     "role_category": "ceo", "linkedin": None,
     "notes": "Enterprise CEO; faith-based system similarity to Mercy/CommonSpirit."},
    {"org": "AdventHealth", "name": "Todd Goodman", "title": "Chief Financial Officer",
     "role_category": "cfo", "linkedin": None,
     "notes": "CFO effective 2026; margin and RCM ROI buyer."},
    {"org": "AdventHealth", "name": "Rob Purinton", "title": "Chief AI Officer",
     "role_category": "caio", "linkedin": None,
     "notes": "First CAIO signal; best executive opener for governed AI portfolio discussion."},
    {"org": "Advocate Health", "name": "Eugene A. Woods", "title": "Chief Executive Officer",
     "role_category": "ceo", "linkedin": None,
     "notes": "Enterprise CEO of a very large nonprofit IDN; strategic sponsor for AI portfolio control."},
    {"org": "Advocate Health", "name": "Rasu Shrestha, MD", "title": "Chief Innovation and Commercialization Officer",
     "role_category": "innovation", "linkedin": None,
     "notes": "Innovation executive; likely entry point for governed model marketplace and platform partnerships."},
    {"org": "Mass General Brigham", "name": "Anne Klibanski, MD", "title": "President and CEO",
     "role_category": "ceo", "linkedin": None,
     "notes": "Academic-system CEO; high-fit for governance credibility and research-backed validation."},
    {"org": "Mass General Brigham", "name": "Jane Moran", "title": "Chief Information and Digital Officer",
     "role_category": "cio", "linkedin": None,
     "notes": "Digital and information executive; buyer for enterprise AI control plane."},
    {"org": "Providence", "name": "Erik Wexler", "title": "President and CEO",
     "role_category": "ceo", "linkedin": None,
     "notes": "Enterprise CEO; large mission-driven West Coast system with digital transformation history."},
    {"org": "Providence", "name": "B.J. Moore", "title": "Executive Vice President and Chief Information Officer",
     "role_category": "cio", "linkedin": None,
     "notes": "CIO buyer for multi-state data, cloud, and AI governance."},
    {"org": "Trinity Health", "name": "Mike Slubowski", "title": "President and CEO",
     "role_category": "ceo", "linkedin": None,
     "notes": "Enterprise CEO; Catholic-system expansion target adjacent to Mercy/CommonSpirit."},
    {"org": "Trinity Health", "name": "Ben Carter", "title": "Executive Vice President and Chief Financial Officer",
     "role_category": "cfo", "linkedin": None,
     "notes": "Finance executive; target for operational efficiency and ROI proof."},
])
