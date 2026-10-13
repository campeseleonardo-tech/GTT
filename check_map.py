import re

html = open('mappa_torino.html', encoding='utf-8').read()

# Check themes
for name in ['vulnerabilita', 'vuln_servizi']:
    if '"id":"' + name + '"' in html:
        print('Tema ' + name + ': PRESENTE')
    else:
        print('Tema ' + name + ': ASSENTE')

# Check the vuln data in DATI
idx = html.find('"vuln"')
if idx > 0:
    print('vuln field found')
    print('Context:', html[idx:idx+120])
else:
    print('vuln field NOT found')

# Count occurrences of 'vulnerabilità mappa:' (debug output)
print(html.count('vulnerabilità mappa:'))
