id: GT06-pannello
title: pannello piu' chiaro: riga "Quando", tema a discesa, legenda dentro il pannello, sezione Info
project: gtt
tier: medium
priority: 3
data_level: 0
repo: C:\Users\campe\Desktop\GTT
branch: GT06-pannello
depends_on: [GT05-pendolari]
profile: profiles/gtt.md
allowed: [scripts/mappa_template.html]
checks: [html_js_check:scripts/mappa_template.html, py_compile:scripts/04_genera_mappa.py, git_unchanged:scripts/03_raccolta_continua.py;scripts/06_dati_live.py;scripts/supervisore.py;scripts/installa_sfondo.py, run_py:scripts/04_genera_mappa.py]
approval_before: leo
approved: yes
---
Leo's feedback on the current map: the legend (#legenda, bottom-left) overlaps the side panel (#pannello); the theme buttons take too much space; the title "Offerta programmata: giorno e ora" is jargon he does not understand; data-update info is not useful while looking at the map.
Edit ONLY scripts/mappa_template.html. Keep every existing feature reachable and all existing element ids working (other code uses them). The THEMES table already contains Velocità (GT04) and Pendolari (GT05): keep them working.
1. "Quando" row at the TOP of the panel (right under the title): replace the h2 "Offerta programmata: giorno e ora" with h2 "Quando". Keep day buttons (#giorno: Feriale/Sabato/Domenica), the time slider (#ora, #oraTxt), "Adesso", play/pause and simulation speed, as compact as possible (ideally 2 lines). Under it one plain sentence that updates by itself: "La mappa mostra il servizio di un giorno feriale alle 23:27" (sabato/domenica accordingly).
2. Theme: replace the big buttons (#temi) with ONE dropdown <select> built from the THEMES table (same ids/labels, same behaviour, default Offerta). Keep #temaDesc under it. Future themes must appear automatically by adding a row to THEMES.
3. Legend inside the panel: move the legend content into the panel as its LAST block (h2 "Legenda"), so there is only one box on the left and nothing overlaps. Remove the separate floating #legenda box (or keep the element hidden but render its content inside the panel). aggiornaLegenda() must keep working (it rebuilds after every live update).
4. Remove the "PROGRAMMATO" tag where it is the only tag in a block (it repeats on every line and adds nothing); keep tags only where they distinguish MISURATO vs STIMATO/SIMULATO vs CENSIMENTO, and keep "dati scarsi".
5. "Info" section: move "Aggiornamento dati" (#stato) and "Dati raccolti" (#statoLive) into one collapsible section "Info sui dati" (a <details> element, CLOSED by default) near the bottom of the panel, above the legend. "Segnalazioni adesso" (#boxSegn) stays where it is with its current theme logic.
6. Panel order top to bottom: title, Quando, Tema (+ description), Sovrapposizioni, Sfondo e filtro, Segnalazioni (when visible), Info sui dati (closed), Legenda.
Report agenti/GT06-pannello/RAPPORTO.md (Italian): what moved where, choices, exact clicks for Leo to test (each theme in the dropdown incl. Velocità and Pendolari, Feriale/Sabato/Domenica + slider + sentence, Info opens/closes, legend changes with the theme, narrow window: no overlap).
