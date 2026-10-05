# [agente GT19-elaborazione-matrici-pen]
import json
import zipfile
import csv
import os
import re
from pathlib import Path

def load_sezioni_torino():
    """Carica le sezioni di Torino e cintura da data/processed/sezioni_torino.json"""
    path = Path("data/processed/sezioni_torino.json")
    if not path.exists():
        raise FileNotFoundError("Eseguire prima scripts/05_prepara_sezioni.py")
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    # Estrarre codici sezione e mapping sezione->comune
    sezione_set = set()
    sezione_comune = {}
    for sezione in data.get("sezioni", []):
        codice = sezione.get("codice")
        comune = sezione.get("comune")
        if codice and comune:
            sezione_set.add(codice)
            sezione_comune[codice] = comune
    return sezione_set, sezione_comune

def get_comuni_dalle_sezioni(sezione_comune):
    """Ottiene l'insieme dei comuni dalle sezioni"""
    return set(sezione_comune.values())

def processa_matrice_2011(zip_path, sezione_set, output_data):
    """Elabora la matrice 2011 a livello di sezione"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            # Supponiamo che il file CSV sia l'unico .zip interno o il primo .csv
            csv_files = [f for f in zf.namelist() if f.lower().endswith('.csv')]
            if not csv_files:
                print(f"Nessun CSV trovato in {zip_path}")
                return
            with zf.open(csv_files[0]) as f:
                # Leggere l'intestazione per capire la struttura
                content = f.read().decode('utf-8-sig')
                reader = csv.DictReader(content.splitlines())
                # Normalizzare i nomi delle colonne (rimuovere spazi, maiuscole)
                fieldnames = [col.strip().lower().replace(' ', '_') for col in reader.fieldnames]
                # Cercare le colonne di origine e destinazione
                orig_col = next((col for col in fieldnames if 'origine' in col or 'origin' in col), None)
                dest_col = next((col for col in fieldnames if 'destinazione' in col or 'dest' in col or 'destination' in col), None)
                if not orig_col or not dest_col:
                    print(f"Colonne origine/destinazione non trovate in {zip_path}. Campi: {fieldnames}")
                    return
                # Elaborare le righe
                count_tot = 0
                count_filt = 0
                for row in reader:
                    count_tot += 1
                    # Normalizzare le chiavi della riga
                    row_norm = {k.strip().lower().replace(' ', '_'): v for k, v in row.items()}
                    orig = row_norm.get(orig_col, '').strip()
                    dest = row_norm.get(dest_col, '').strip()
                    if orig in sezione_set or dest in sezione_set:
                        count_filt += 1
                        # Mantenere tutti i campi utili
                        output_data["2011"].append(row_norm)
                print(f"2011: {count_tot} righe totali, {count_filt} filtrate per Torino/cintura")
    except Exception as e:
        print(f"Errore elaborando {zip_path}: {e}")

def processa_matrice_2021(zip_path, tipo, comuni_set, output_data):
    """Elabora la matrice 2021 a livello di comune (lavoro o studio)"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            csv_files = [f for f in zf.namelist() if f.lower().endswith('.csv')]
            if not csv_files:
                print(f"Nessun CSV trovato in {zip_path}")
                return
            with zf.open(csv_files[0]) as f:
                content = f.read().decode('utf-8-sig')
                reader = csv.DictReader(content.splitlines())
                fieldnames = [col.strip().lower().replace(' ', '_') for col in reader.fieldnames]
                orig_col = next((col for col in fieldnames if 'origine' in col or 'origin' in col), None)
                dest_col = next((col for col in fieldnames if 'destinazione' in col or 'dest' in col or 'destination' in col), None)
                val_col = next((col for col in fieldnames if 'numero' in col or 'valore' in col or 'persone' in col), None)
                if not orig_col or not dest_col or not val_col:
                    print(f"Colonne richieste non trovate in {zip_path}. Campi: {fieldnames}")
                    return
                count_tot = 0
                count_filt = 0
                for row in reader:
                    count_tot += 1
                    row_norm = {k.strip().lower().replace(' ', '_'): v for k, v in row.items()}
                    orig = row_norm.get(orig_col, '').strip()
                    dest = row_norm.get(dest_col, '').strip()
                    if orig in comuni_set or dest in comuni_set:
                        count_filt += 1
                        # Aggiungere tipo e normalizzare valore
                        row_norm["tipo"] = tipo
                        try:
                            val = int(row_norm.get(val_col, 0))
                        except:
                            val = 0
                        row_norm["numero_persone"] = val
                        output_data["2021"].append(row_norm)
                print(f"2021 {tipo}: {count_tot} righe totali, {count_filt} filtrate per Torino/cintura")
    except Exception as e:
        print(f"Errore elaborando {zip_path}: {e}")

def main():
    # Percorsi
    docs_dir = Path("docs")
    data_processed_dir = Path("data/processed")
    data_processed_dir.mkdir(parents=True, exist_ok=True)
    
    # Caricare riferimento sezioni Torino
    try:
        sezione_set, sezione_comune = load_sezioni_torino()
        comuni_set = get_comuni_dalle_sezioni(sezione_comune)
        print(f"Caricate {len(sezione_set)} sezioni e {len(comuni_set)} comuni di riferimento")
    except Exception as e:
        print(f"Impossibile caricare riferimento sezioni: {e}")
        return
    
    # Preparare struttura output
    output_data = {
        "2011": [],
        "2021": []
    }
    
    # Elaborare matrice 2011
    zip_2011 = docs_dir / "matrici-pendolarismo-sezione-censimento-2011.zip"
    if zip_2011.exists():
        processa_matrice_2011(zip_2011, sezione_set, output_data)
    else:
        print(f"File non trovato: {zip_2011}")
    
    # Elaborare matrici 2021 (lavoro e studio)
    # Cerchiamo file con nomi tipici
    possibili_2021 = [
        ("pendolarismo-2021-lavoro.zip", "lavoro"),
        ("pendolarismo-2021-studio.zip", "studio"),
        ("matrice-pendolarismo-lavoro-2021.zip", "lavoro"),
        ("matrice-pendolarismo-studio-2021.zip", "studio")
    ]
    for zip_nome, tipo in possibili_2021:
        zip_path = docs_dir / zip_nome
        if zip_path.exists():
            processa_matrice_2021(zip_path, tipo, comuni_set, output_data)
        else:
            # Prova varianti senza hyphen
            alt_nome = zip_nome.replace("-", "_")
            zip_path_alt = docs_dir / alt_nome
            if zip_path_alt.exists():
                processa_matrice_2021(zip_path_alt, tipo, comuni_set, output_data)
    
    # Salvare risultato compatto
    output_file = data_processed_dir / "pendolarismo_torino_cintura.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    # Statistiche
    n2011 = len(output_data["2011"])
    n2021 = len(output_data["2021"])
    print(f"\nSalvato {output_file}")
    print(f"Record 2011: {n2011}")
    print(f"Record 2021: {n2021}")
    print(f"Totale: {n2011 + n2021}")

def _parse_hour(value):
    """Estrae l'ora (int) da una stringa di fascia oraria."""
    if not value:
        return None
    # Cerca il primo numero intero presente nella stringa
    m = re.search(r'(\d{1,2})', str(value))
    if m:
        try:
            return int(m.group(1))
        except:
            return None
    return None

def _slot_from_hour(hour):
    """Restituisce la fascia oraria corrispondente all'ora."""
    if hour is None:
        return None
    if 6 <= hour < 9:
        return "mattina"
    if 9 <= hour < 14:
        return "mezzogiorno"
    if 14 <= hour < 19:
        return "pomeriggio"
    if 19 <= hour < 22:
        return "sera"
    # notte: 22-24 o 0-6
    if hour >= 22 or hour < 6:
        return "notte"
    return None

def _aggregate_2011_by_fascia(rows):
    """Raggruppa i dati 2011 per fascia, origine, destinazione."""
    fasce = {}
    for row in rows:
        # Trova la colonna con il numero di persone
        val = None
        for key in ("numero_persone", "persone", "numero", "valore"):
            if key in row:
                try:
                    val = int(row.get(key, 0))
                except:
                    val = 0
                break
        if val is None:
            val = 0
        # Trova la colonna con la fascia oraria
        fas_f = None
        for key in ("fascia_oraria", "fascia", "orario", "orari"):
            if key in row:
                fas_f = row[key]
                break
        hour = _parse_hour(fas_f)
        slot = _slot_from_hour(hour)
        if slot is None:
            continue
        orig = row.get("origine", "").strip()
        dest = row.get("destinazione", "").strip()
        if not orig or not dest:
            continue
        fasce.setdefault(slot, {}).setdefault(orig, {}).setdefault(dest, 0)
        fasce[slot][orig][dest] += val
    return fasce

def _distribute_2021_to_fasce(rows_2021, fasce_2011):
    """Distribuisce i valori 2021 sui fasce usando le proporzioni della matrice 2011."""
    for row in rows_2021:
        val = row.get("numero_persone", 0)
        orig = row.get("origine", "").strip()
        dest = row.get("destinazione", "").strip()
        if not orig or not dest:
            continue
        # Totale 2011 per questo origine-destinazione
        total_2011 = sum(
            fasce_2011[slot].get(orig, {}).get(dest, 0) for slot in fasce_2011
        )
        if total_2011 > 0:
            for slot in fasce_2011:
                part = fasce_2011[slot].get(orig, {}).get(dest, 0) / total_2011
                add = int(round(val * part))
                if add:
                    fasce_2011[slot].setdefault(orig, {}).setdefault(dest, 0)
                    fasce_2011[slot][orig][dest] += add
        else:
            # Distribuzione uniforme se non ci sono dati 2011
            uniform = int(round(val / 5))
            for slot in ("mattina", "mezzogiorno", "pomeriggio", "sera", "notte"):
                fasce_2011.setdefault(slot, {}).setdefault(orig, {}).setdefault(dest, 0)
                fasce_2011[slot][orig][dest] += uniform
    return fasce_2011

def main_fasce():
    """Genera le matrici origine-destinazione per le 5 fasce orarie."""
    data_processed_dir = Path("data/processed")
    input_file = data_processed_dir / "pendolarismo_torino_cintura.json"
    if not input_file.exists():
        print("File di input non trovato, esegui prima main()")
        return
    with open(input_file, encoding="utf-8") as f:
        data = json.load(f)
    # Aggregazione 2011
    fasce = _aggregate_2011_by_fascia(data.get("2011", []))
    # Distribuzione 2021
    fasce = _distribute_2021_to_fasce(data.get("2021", []), fasce)
    # Salvataggio risultato
    out_file = data_processed_dir / "od_per_fascia.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(fasce, f, ensure_ascii=False, indent=2)
    print(f"Salvato OD per fascia in {out_file}")

if __name__ == "__main__":
    main()
