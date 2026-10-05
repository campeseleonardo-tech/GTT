id: M01-mercatino-studio
title: Mercatino (archiviato) - studio del documento finale per Giangio e Mercatino + domande per Leo
project: mercatino
tier: medium
priority: 3
data_level: 2
inputs: [C:\Users\campe\Desktop\Mercatino\compass_artifact_wf-24198c43-6ec4-59e6-b4d2-a2a41e04877b_text_markdown.md, C:\Users\campe\Desktop\Mercatino\mercatino_project.txt]
per_te: Studia come impostare il documento finale per Giangio e Mercatino e ti prepara le domande (non scrive il documento).
---
Context: Leo (Leonardo) explored becoming Mercatino's (mercatinousato.com, Italian network of ~180 second-hand shops) master franchisee/partner in Austria. He has ARCHIVED the project with this reason: "the only truly valid proof would be opening one shop and seeing whether it works; without that, continuing makes no sense for now". He still wants to close it well: a written document (Italian, max ~15 pages) for Giangio (his friend, son of the founder) and for Mercatino itself, so the market research is useful to someone.

THIS TASK IS ONLY A STUDY. Do NOT write the final document.
Read the two input files (market research on the Austrian second-hand market with comparison to Italy, and Leo's project notes).

Write ./outputs/STUDIO_DOCUMENTO.md in Italian, plain language:
1. Purpose and readers (Giangio; Mercatino management): what they would want to get out of it.
2. Proposed structure of the final document (sections, about how many pages each, max ~15 pages total), ending with the honest conclusion above (a pilot shop is the only real test) and what a pilot would need to measure.
3. For each section: which data already exists in the inputs (with the source and date written there), what is missing, outdated or not verifiable, and what would need checking on the web before sending (list it; you have no web access).
4. Confidentiality: what should NOT go into a document sent to Mercatino (e.g. Leo's personal budget, private notes, interview details promised as anonymous). Flag anything you are unsure about.
5. Tone and form suggestions (professional, short, data first).

Then write the questions for Leo in ./DECISIONS.md, first line exactly `STATUS: OPEN`: numbered, each with 2-3 options and your recommendation (e.g. depth, which data to include, whether to mention his budget, language, format PDF/Word, who receives it first). Only questions that really change the document.
Never invent data: if a number is not in the inputs, write "non presente".

If ./ANSWERS.md exists (Leo answered): update STUDIO_DOCUMENTO.md with his answers, add a section "Piano di scrittura" (what the writing task will do), write `STATUS: RESOLVED` as first line of DECISIONS.md and stop. Still do NOT write the final document: that will be a separate task Leo starts only if he decides to go on.
