# Fonti dati

Legenda: VERIFICATO = l'ho letto io; NON VERIFICATO = indicato da altre pagine, da controllare.

## Scaricate dallo script 01

| Fonte | Indirizzo | Stato |
|---|---|---|
| GTT orari programmati (GTFS) | https://www.gtt.to.it/open_data/gtt_gtfs.zip | indirizzo VERIFICATO su aperTO; contenuto e date NON VERIFICATI |
| GTT posizioni mezzi (GTFS-RT) | https://percorsieorari.gtt.to.it/das_gtfsrt/vehicle_position.aspx | indirizzo VERIFICATO; contenuto NON VERIFICATO |
| GTT ritardi corse (GTFS-RT) | https://percorsieorari.gtt.to.it/das_gtfsrt/trip_update.aspx | come sopra |
| GTT avvisi (GTFS-RT) | https://percorsieorari.gtt.to.it/das_gtfsrt/alerts.aspx | come sopra |
| 5T flussi di traffico | https://opendata.5t.torino.it/get_fdt | VERIFICATO (91 sensori, 5 minuti) |
| Zone statistiche Torino | http://geoportale.comune.torino.it/geodati/zip/zone_statistiche_csv.zip e ..._geo.zip | indirizzi VERIFICATI su aperTO; dati del 2011 |

Pagina di riferimento aperTO per GTT tempo reale: https://aperto.comune.torino.it/dataset/feed-gtfs-real-time-trasporti-gtt

## ISTAT: stato al 4/10/2026

- Pendolarismo 2021 lavoro e studio: SCARICATI dall'utente (file di testo, comune contro comune, nessun mezzo né orario). Vedi `docs/istat/NOTE_FILE_ISTAT.md`.
- Matrice 2011 a livello di sezione: download incompleto, da rifare/finire.
- Basi territoriali 2021 Piemonte (R01_21.zip): ancora da scaricare.

## Da scaricare a mano (non conosco l'indirizzo diretto, non lo invento)

1. **ISTAT pendolarismo 2011**: pagina https://www.istat.it/non-categorizzato/matrici-di-contiguita-distanza-e-pendolarismo/
   Serve il file "a livello di sezione di censimento" (circa 126 MB) e quello comunale (circa 34 MB), più le note
   metodologiche e il file dei codici comunali. Salvali in `data/raw/istat/`.
2. **ISTAT basi territoriali 2021**: pagina https://www.istat.it/notizia/basi-territoriali-e-variabili-censuarie/
   Serve il file del Piemonte (indicato come R01_21.zip). Salva in `data/raw/istat/`.
3. **ISTAT pendolarismo per lavoro 2021**: pagina https://www.istat.it/notizia/matrice-di-pendolarismo-per-lavoro/
   Si consulta nel browser dati ISTAT (esploradati.istat.it): da lì si può provare a esportare Torino. NON verificato che
   contenga mezzo e orario.
4. **Facoltativo** - aperTO: ciclabili, parcheggi blu, ZTL con varchi, fermate metro, incidenti 2011-2017.
   Catalogo: https://aperto.comune.torino.it/dataset/?q=mobilit%C3%A0

## Non pubbliche (richiedono una richiesta)

- Indagine IMQ 2022 (MTM, Agenzia Mobilità Piemontese): solo risultati aggregati pubblici. Bozza in `richiesta_MTM_IMQ.md`.
- Dati da telefonia mobile (TIM/Wind usati dall'agenzia, Vodafone usati con il Politecnico): non pubblici.
  Bozza in `richiesta_dati_telefonia.md`.

## Non trovati

Bici e sharing (ToBike, monopattini, car sharing), posti liberi nei parcheggi, feed dei treni urbani (SFM),
dati orari ARPA (su aperTO ci sono solo medie annuali). Non vuol dire che non esistano.

## Dati storici di confronto

PUMS Torino 2008: pagina del geoportale (mappe PDF di flussi alle ore di punta 7:40-8:40 e 17-18, sosta, incidenti,
sensori 5T, offerta TPL in posti/ora). Non leggibile da programma senza digitalizzazione.
