id: GT01-sfondi
title: sfondi della mappa senza OpenStreetMap (bloccato da file://) + intensita' dello sfondo
project: gtt
tier: small
priority: 3
data_level: 0
repo: C:\Users\campe\Desktop\GTT
branch: GT01-sfondi
profile: profiles/gtt.md
allowed: [scripts/mappa_template.html]
checks: [html_js_check:scripts/mappa_template.html, py_compile:scripts/04_genera_mappa.py, git_unchanged:scripts/03_raccolta_continua.py;scripts/06_dati_live.py;scripts/supervisore.py;scripts/installa_sfondo.py, run_py:scripts/04_genera_mappa.py]
approval_before: leo
approved: yes
---
Problem: the backgrounds "chiara" and "osm" use tile.openstreetmap.org. OSM blocks pages opened from disk (file://, no Referer) with "app is not following the tile usage policy" (osm.wiki/Blocked). Leo sees that error; only the satellite (Esri) works, and he likes the satellite a lot.
Edit ONLY scripts/mappa_template.html (tile code is around the "tiles"/"CRED"/"basemap" parts):
1. Remove every tile.openstreetmap.org URL. New backgrounds, all keyless Esri ArcGIS Online tile services (same URL pattern as the existing satellite, .../MapServer/tile/{z}/{y}/{x}):
   - "chiara": Canvas/World_Light_Gray_Base (max zoom 16)
   - "stradale": World_Street_Map (max zoom 19)
   - "sat": World_Imagery (unchanged)
   - "nessuno": no tiles, plain light background
   Give each background a maxZoom. When the map zoom is above it, draw the max-zoom tile scaled up (overzoom) instead of requesting missing tiles. Keep the existing tile cache limits.
2. Default background = satellite.
3. New slider "Intensità sfondo" (0-100%, default 70%) under the background menu: it fades the background toward white (or dark, your choice, list it in Scelte) so data layers stay readable over the satellite. Do it with one overlay rect or globalAlpha per frame, not per tile.
4. Attribution: correct Esri credits for each background (keep "dati GTT, 5T, ISTAT, Comune di Torino").
5. If more than ~20 tiles fail and none loaded, show a small non-blocking notice "Sfondo non disponibile (connessione?)" and keep the data layers working.
Report agenti/GT01-sfondi/RAPPORTO.md (Italian): what changed, and exactly what Leo should click to test (each background, zoom 17-18 on "chiara", the slider).
