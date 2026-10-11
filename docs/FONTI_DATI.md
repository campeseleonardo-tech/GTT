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

## ISTAT: stato all'8/10/2026

Tutto scaricato e verificato: pendolarismo 2021 (lavoro e studio, comune contro comune), matrici 2011 (110 zip
per provincia + nazionale con mezzo e orario), basi territoriali 2021 Piemonte, indicatori regionali 2021.
Dove stanno i file e cosa contengono: inventario ISTAT in `MEMORIA_PROGETTO.md`.

## OMI (Agenzia delle Entrate): SCARICATO l'8/10/2026

- Quotazioni immobiliari semestre 2025/2 e perimetri delle zone OMI, provincia di Torino (312 comuni).
- File in `data/raw/QIP1445919_CMPLRD98T08F335C/` (due CSV + `TO20252/` con i KML, uno per comune). Non toccare.
- Scaricati a mano da Leo dal servizio Forniture dati OMI / GeoPOI dell'Agenzia. In caso di uso: citare
  "Agenzia delle Entrate - OMI".
- Mancante (facoltativo): provincia di Asti, per coprire Moncucco Torinese (unico comune dell'area non coperto).
- In mappa dal 9/10: sezione 4 di `MEMORIA_PROGETTO.md`.

## Da scaricare a mano (eventuale, non urgente)

1. **Facoltativo** - OMI provincia di Asti (per Moncucco Torinese, vedi sopra).
2. **Facoltativo** - aperTO: incidenti 2011-2017 (ciclabili, zone blu, ZTL e fermate metro sono già nel catalogo).
   Catalogo: https://aperto.comune.torino.it/dataset/?q=mobilit%C3%A0

## Non pubbliche (richiedono una richiesta)

- Indagine IMQ 2022 (MTM, Agenzia Mobilità Piemontese): usati i dati aperti (`data/raw/IMQ2022_opendata_web/`).
  Richiesta di zone di campionamento e altre elaborazioni INVIATA da Leo; risposta attesa.
- Dati da telefonia mobile (TIM/Wind usati dall'agenzia, Vodafone usati con il Politecnico): non pubblici.
  Bozza in `richiesta_dati_telefonia.md`.

## Rete stradale (per R5)

- OpenStreetMap, estratto Geofabrik Nord-Ovest (8/10/2026), tagliato all'area Torino+cintura dallo script 17
  in `data/otp/rete/torino_cintura.osm.pbf`. L'estratto intero è stato cancellato: si riscarica da
  https://download.geofabrik.de/europe/italy/nord-ovest.html

## Non trovati

Bici e sharing (ToBike, monopattini, car sharing), posti liberi nei parcheggi, feed dei treni urbani (SFM),
dati orari ARPA (su aperTO ci sono solo medie annuali). Non vuol dire che non esistano.

## Dati storici di confronto

PUMS Torino 2008: pagina del geoportale (mappe PDF di flussi alle ore di punta 7:40-8:40 e 17-18, sosta, incidenti,
sensori 5T, offerta TPL in posti/ora). Non leggibile da programma senza digitalizzazione.
