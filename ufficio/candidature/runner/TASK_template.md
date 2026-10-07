# TASK (unattended run: nobody is available to answer questions, never ask)

Work only inside this folder. The reference documents named below are read-only: never write to them. Read no other files.

Files:
- offer.txt                              the job posting (the only new input)
- company_context.txt                    text of the company's own pages (about / mission), may say NOT AVAILABLE
- {{FW}}        process and CV rules (includes the unattended-mode section)
- {{CVB}}    FACTS, single source of truth for facts

## Efficiency (this matters: each turn costs credits)
- Read offer.txt, company_context.txt and the two main context files (framework, baseline; company-specific facts are in section 7 of the baseline) in ONE turn, using parallel Read calls.
- Think and draft everything, then write ALL output files in ONE turn, using parallel Write calls.
- Aim for about 5-6 turns in total. Do not re-read files and do not re-open a file you just wrote.

## What to do
Prepare Analysis.md, CV_description.txt and meta.json for the offer, following the framework exactly,
including MODALITÀ NON PRESIDIATA. The cover letter is written later in a separate step: do NOT write it now.
In Analysis.md add a section "FIT CON L'AZIENDA": from company_context.txt note the company's mission,
objectives and scope in 3-5 lines and say which real facts of Leonardo connect to them (never invent company
facts that are not in company_context.txt; if it says NOT AVAILABLE, write that). Use the baseline for everything and ask Leonardo only through
OPEN QUESTIONS in the analysis, and only if a fact is truly missing.
Also add a short section "SUGGERIMENTI" (max 6 lines, Italian): things that could help Leonardo get in, found by
cross-checking company, offer and his earlier applications. Earlier applications you may READ (never change, never
copy text from them): {{ARC}} (history) and {{OUTD}} (prepared applications). Glance at no more than 2 files, only if
one is in a similar sector or role; say which file is worth comparing and why. Other ideas welcome (a contact angle,
a point to check on the company site, a small proactive idea). If nothing useful, write "nessuno".
The baseline may end with a section "AUTO-ADDED FACTS": lines tagged [AUTO ...] are facts Leonardo gave in earlier
answers; treat them as baseline facts, but if one conflicts with the rest of the baseline put it in DA VERIFICARE.
Rules this run has often broken, check each before writing:
1. Facts only from the baseline. If you doubt a detail, leave it out. Anything you would list in
   DA VERIFICARE as inferred or not in the baseline must NOT appear in CV or letter.
2. Never state hours, shifts, salary, notice period or workload as Leonardo's commitment. Exception in the
   baseline: working-time preference, only if the offer itself talks about hours or part-time.
4. Entries with too few facts stay at 2 lines. Never pad with generic or inferred sentences.
5. No negative gap sentence in the CV (not even in ABOUT ME). The gap goes in the analysis (and in the letter if useful).
6. Language: the content is in the offer's language, section headings stay in English capitals,
   location line and language names/levels are in the offer's language (no mix).
7. Titles and names stay EXACTLY as in the baseline, in every language: role titles and subtitles (e.g.
   "System Testing Engineer | Thermal Management"), degree names, "FH Upper Austria", "Heilbronn University",
   "University Collaboration", "SCRUM Certification". Translate only description lines.
8. Use the offer's own keywords wherever the baseline supports them (e.g. "Testautomatisierung",
   "Testfälle", "Scrum") in role lines and TOOLS: the ATS searches for them.
9. KTM ended in 06/2026: always past tense about KTM ("habe drei Jahre bei KTM gearbeitet"), never
   "arbeite bei KTM" or "seit drei Jahren bei KTM". Present tense only for what is true now.
11. When a sentence mixes an unsupported detail and a real one, delete only the unsupported detail and keep
    the real fact (e.g. keep "Events mit rund 1.000 Gästen"). Skills only in the baseline's words: never
    invent a story such as "hardware I had not known before".
12. Do not claim results were handed to suppliers unless the baseline says so (customers, colleagues).
13. Never claim a tool, method or experience the baseline does not state ("only seen" stays "only seen").
    Never write that something happened "before the studies": the seasonal electrician work 2014-2018
    overlaps the Bachelor (from 09/2017); say "every summer".

## Outputs (exactly these paths)
- out/cv/CV_description.txt
- out/analysis/Analysis.md       in Italian, structure from the framework (fit, salary vs usual ask, gaps,
                                 ATS risks, choices, OPEN QUESTIONS, DA VERIFICARE). About one page.
- out/meta.json                  {"company": "...", "role": "...", "lang": "DE", "location": "...",
                                  "questions": ["..."]}
                                 questions = facts that are truly missing from the baseline and needed for this
                                 offer, one short Italian question each, [] if none. Never ask what the
                                 baseline already says.
                                 company = employer in few words, no client, no legal form ("ACP", not
                                 "ACP doIT GmbH Kunde IQS"). lang = DE, EN, IT or ES (language of the offer).

## CV_description.txt layout (plain text, no bullets, no markdown, no tables, UTF-8)
Dates MM/YYYY - MM/YYYY with a plain hyphen. Exactly this order:

LEONARDO CAMPESE
(blank line)
LinkedIn / Phone / Email lines from the baseline, then one line, in the offer's language:
Salzburg, <Austria> | available immediately | relocation possible. No birth date.
ABOUT ME            paragraph of about 400 characters
WORK EXPERIENCE     ALL work entries of the baseline, always: 3 KTM roles, SEO Data Analyst, Event Manager,
                    Electrician (Seasonal), Pizzaiolo (student job; dates line "During the Master's studies"
                    as in the baseline). Leonardo cuts later. Entries separated by one blank line; each entry =
                    role line "Title | Subtitle", then "Company | MM/YYYY - MM/YYYY", then description lines
EDUCATION           same entry layout (MSc, BSc, university collaboration)
CERTIFICATIONS      IPMA Level D always, plus the Scrum certificate
LANGUAGES           Italian native, English C1, Spanish C1, German C1, French A2 (names in the offer's language)
TOOLS / DIGITAL SKILLS
ADDITIONAL          only if the offer asks for extras (application-form fields, in plain text)

Hard checks (a script verifies them right after you finish and repairs failures, so DO NOT spend effort
counting characters):
- Description lines in WORK EXPERIENCE and EDUCATION: each on its own line, one idea per line, written
  to be about 75-88 characters including spaces, never over 90. At most 4 important lines may be 172-180
  characters. Never 91-171. Just write short, compact lines; do not count or recount them.
- 3 description lines per entry by default; 4 or more only for entries central to this offer;
  2 if facts are missing.
- The three KTM roles, SEO Data Analyst (Internship / Praktikum), Event Manager, Electrician, Pizzaiolo and
  IPMA Level D always appear. KTM dates exactly as in the framework.

## Finish
Reply with the single word DONE. Do not summarise.
