import sqlite3, sys
from datetime import datetime, timezone

db = sys.argv[1] if len(sys.argv) > 1 else 'data/storico_backup.sqlite'
con = sqlite3.connect(db)
cur = con.cursor()

# Tabelle
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
print("Tabelle:")
tables = []
for r in cur.fetchall():
    tables.append(r[0])
    print("  -", r[0])

# Trova tabella di mezzi
mezzi_table = None
for nome in tables:
    cur.execute(f"PRAGMA table_info('{nome}')")
    cols = cur.fetchall()
    if any('linea' in c[1] or 'lat' in c[1] or 'long' in c[1] or 'letto' in c[1] for c in cols):
        mezzi_table = nome
        break

if mezzi_table:
    print(f"\nTavolo di mezzi trovato: {mezzi_table}")
    # Ultime posizioni
    cur.execute(f"SELECT COUNT(*), MIN(letto_utc), MAX(letto_utc) FROM {mezzi_table}")
    c, minu, maxu = cur.fetchone()
    print(f"\nTotale posizioni: {c}")
    print(f"Primo: {minu}")
    print(f"Ultimo: {maxu}")
    print(f"Ora UTC: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Cerca aggiornamenti piu recenti
    cur.execute(f"SELECT MAX(letto_utc), COUNT(DISTINCT strftime('%Y-%m-%d', letto_utc)) FROM {mezzi_table}")
    max_date, days = cur.fetchone()
    print(f"Data aggiornamento massimo: {max_date}")
    print(f"Giorni con dati: {days}")
    
    # ultimi minuti di aggiornamento
    cur.execute(f"SELECT COUNT(*) FROM {mezzi_table} WHERE letto_utc > datetime('now', '-10 minutes')")
    recent = cur.fetchone()[0]
    print(f"Posizioni nelle ultime 10 minuti: {recent}")
else:
    print("\nNessuna tabella di mezzi trovata!")
    # Lista colonne di tutti i dati
    for nome in tables:
        cur.execute(f"PRAGMA table_info('{nome}')")
        cols = cur.fetchall()
        print(f"\nColonne {nome}:")
        for c in cols:
            print(f"  {c[1]} ({c[2]})")