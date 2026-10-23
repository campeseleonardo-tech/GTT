# Piano — Raccolta sul Raspberry Pi: mettere a posto

Scritto il 23/10/2026 dall'analisi critica (`ANALISI_CRITICA.md`, sezione 5), con le prove. **Da discutere con Leo prima dei giri.**
Nessuno di questi passi tocca i file di L3 (`rifai_tutto.py`, `scripts/schede/r6.py`, `r8.py`, `assets/gara.js`, script 100, `docs/R6_parcheggi.md`, `docs/R8_traffico.md`):
si possono fare anche mentre L3 è aperto, tranne il passo 2b (script 27 e 70), da fare dopo che L3 è unito se L3 rilancia il R4.

## Cosa non va (verificato)

| # | Problema | Prova | Gravità |
|---|---|---|---|
| 1 | La copia giornaliera sostituisce quella vecchia senza controllare che lo storico sia cresciuto: se sul Pi il file si azzera, il PC copia un archivio vuoto ma «integro» e perde l'unica copia | `scripts/backup_da_leopi.py:110` (`os.replace` dopo il solo controllo di integrità e Pi = PC) | alta |
| 2 | Il GTFS non si archivia: lo script 27 (e il 70, il 97) usa un solo file fisso; quando GTT pubblica un orario nuovo (di solito a dicembre, comunque prima del 31/01/2027) le corse dei giorni nuovi non si abbinano più | `scripts/27_risultato4_regolarita.py:78`; già oggi 3.614 corse «fuori GTFS» su 51.455; nessuno script del Pi scarica il GTFS | alta |
| 3 | Sul Pi gli avvisi di spazio (oltre 10 GB) e il promemoria settimanale finiscono solo nel registro: fuori da Windows `finestra()` stampa e basta | `scripts/supervisore.py:86-90` | media |
| 4 | Crescita: 2,1 GB il 23/10, ~190 MB al giorno (quasi tutto il feed dei ritardi `trip_update_gtt`, che il R4 non usa più per i numeri, solo per il confronto) → ~10 GB a inizio dicembre, ~21 GB a fine gennaio. Copia intera ogni giorno (oggi ~10 min) e snapshot intero in `/tmp` sul Pi | memoria, sezione 3; `backup_da_leopi.py` | media |
| 5 | `/tmp` del Pi: nelle versioni recenti di Debian (quelle con Python 3.13) può stare in memoria; uno snapshot di vari GB lì fallisce | **da verificare** sul Pi: `df -h /tmp` | media (se vero, alta) |
| 6 | Se il PC resta spento (vacanze), nessuno si accorge che il Pi è fermo: il controllo parte dal PC | `RACCOLTA_GIORNALIERA.bat` | media |
| 7 | Feed degli avvisi GTT: il 23/10 alle 20:25 l'indirizzo `alerts.aspx` rispondeva con una pagina d'errore del server (HTML «Runtime Error»), non col feed. Gli errori vanno nella tabella `errori` ma il controllo giornaliero li mostra solo come informazione | prova mia con `curl`; `scripts/12_ritardi_gtt.py:488`; `controlla_leopi.py` | bassa (gli avvisi oggi non servono a nessun risultato) |
| 8 | Un solo posto per lo storico grezzo (Pi + una copia nella stessa casa) | — | media |

Verificato anche, con il feed dal vivo (23/10, 364 mezzi): GTT pubblica per ogni mezzo **solo** corsa (con orario e data di partenza), linea, posizione,
istante e numero del veicolo. **Niente affollamento** (campi `occupancy_status` e `occupancy_percentage` assenti), niente fermata corrente, niente
velocità (il campo `velocita` del database resta vuoto). Il raccoglitore quindi non sta buttando via dati utili.

## Passi proposti (in ordine)

| # | Passo | Dove | Lavoro | Rischio con L3 |
|---|---|---|---|---|
| 1 | **Copia che non perde dati**: prima di sostituire, righe di `mezzi_gtt` e `flussi_5t` nuove ≥ vecchie e data minima uguale; altrimenti si tiene la vecchia, la nuova va in `storico_backup_SOSPETTO.sqlite` e il `.bat` dà ALLARME. Rotazione: tenere anche `storico_backup_ieri.sqlite`. Opzione `--prova` con due database finti | CLOUD (script) → Leo lancia `RACCOLTA_GIORNALIERA.bat` una volta | piccolo | nessuno |
| 2a | **Archivio del GTFS sul Pi**: una volta al giorno scaricare `gtt_gtfs.zip`; se l'hash è nuovo salvarlo come `data/gtfs/gtt_gtfs_AAAAMMGG.zip` + riga in una tabella `gtfs_versioni` (data, hash, validità da `calendar`/`feed_info`) | CLOUD (03 o supervisore) → Leo `AGGIORNA_RACCOLTA_LEOPI.bat` | piccolo | nessuno |
| 2b | Script 27, 70 e 97: per ogni giorno il GTFS valido quel giorno (il più recente scaricato prima); con un solo GTFS i numeri restano identici (regola di prova) | CLOUD → PC | piccolo-medio | **dopo L3** (L3 può rilanciare il R4) |
| 3 | **Controllo giornaliero più completo** (`controlla_leopi.py`): spazio libero sul Pi (ALLARME sotto 5 GB), peso dello storico, spazio di `/tmp`, ultima versione del GTFS e giorni alla scadenza (ALLARME entro 14 giorni), errori del feed avvisi oltre 24 ore di fila (AVVISO). Soglie scritte in testa allo script | CLOUD → Leo | piccolo | nessuno |
| 4 | Snapshot non in `/tmp` ma in una cartella del disco del Pi (dopo la verifica del punto 5) | CLOUD | piccolo | nessuno |
| 5 | **Crescita**: scelta di Leo fra (a) feed dei ritardi ogni 5 minuti invece che ogni minuto (−80% circa della crescita; il confronto feed/GPS del R4 resta possibile), (b) tenerlo com'è e passare a uno storico per mese (i mesi chiusi si copiano una volta sola), (c) entrambi | Leo decide → CLOUD → Leo sul Pi | medio | nessuno |
| 6 | **Avviso dal Pi al telefono** se la raccolta si ferma: un servizio esterno gratuito di «battito» (es. healthchecks.io, il Pi lo chiama ogni ora; se non arriva, un'email) | Leo decide (servizio esterno) | piccolo | nessuno |
| 7 | **Copia fuori casa** dei mesi chiusi: uno zip mensile nella Release di GitHub (solo i riassunti sono già in git) o su un disco esterno | Leo decide | piccolo | nessuno |
| 8 | Hardware (facoltativo): storico su una chiavetta o un SSD USB invece della scheda SD (le schede SD si consumano con le scritture continue) | Leo | — | nessuno |

Cose che il Pi **non** deve raccogliere: meteo e qualità dell'aria si scaricano dopo, quando servono (archivio orario di Open-Meteo;
ARPA Piemonte dà i dati orari delle stazioni degli ultimi due anni in CSV). Vedi `PIANO_AMPLIAMENTO.md`.

## Domande per Leo
1. Crescita (passo 5): feed dei ritardi più rado, storico per mese, o tutti e due?
2. Va bene un servizio esterno per l'avviso al telefono (passo 6)?
3. Puoi lanciare `df -h /tmp` e `df -h /` sul Pi (o con `CONTROLLA_LEOPI.bat` se lo aggiungiamo) e dirmi i numeri?
