# Note sui file ISTAT scaricati (letti il 4/10/2026)

## Pendolarismo 2021 - lavoro e studio (matrix_pendoLAVORO_2021.zip, matrix_pendoSTUDIO_2021.zip)

- File di testo con colonne separate da tab: provincia e comune di residenza, provincia e comune di lavoro (o studio), numero di pendolari.
- Livello: **comune contro comune**. Non c'è il mezzo, non c'è l'orario, non ci sono zone dentro Torino.
- Si riferisce a chi si sposta almeno tre giorni a settimana tra residenza e luogo abituale di lavoro/studio, al 31/12/2021.
- Lavoro: 19.565.808 persone in Italia, 523.949 righe. Studio: 9.279.329 persone, 141.226 righe (il file studio è una stima con modelli statistici, non un conteggio diretto).
- Codici comune: formato ISTAT a 6 cifre. Torino = 001272. I nomi dei comuni stanno nella tabella ISTAT dei codici (link nei "leggimi").
- Torino, calcolato da me sui file:
  - lavoro: 212.249 residenti che lavorano a Torino; 71.297 residenti di Torino che lavorano altrove; 138.605 che entrano da altri comuni (303 comuni della provincia, 15 coprono metà dei flussi);
  - studio: 120.148 dentro Torino; 6.373 escono; 48.730 entrano.
- Il flusso "Torino verso Torino" è un solo numero: per vedere dove, dentro la città, serve la matrice 2011 a livello di sezione.

## Altri file

- `leggimi_file_matrix_pendo*.doc`: descrizione delle colonne dei due file qui sopra.
- `nota-tecnica-matrici-distanze-maggio2023.pdf`: nota sulla matrice dei tempi di viaggio tra comuni italiani (2021), con tempo effettivo e tempo senza traffico. Il file della matrice NON è stato scaricato: potrebbe servire per stimare i ritardi dovuti al traffico tra comune e comune.
- `Matrici-di-contiguita...Nota-metodologica.pdf` e `MatriciContiguita_Province_2019_2025.zip`: contiguità tra province e comuni. Per ora non servono.

## Ancora mancante

- Matrice 2011 a livello di sezione di censimento (con mezzo e fascia oraria): il download nella cartella GTT risultava incompleto (file .crdownload).
- Confini dei comuni e delle sezioni 2021 (per disegnare i flussi sulla mappa) e popolazione per sezione: file R01_21.zip delle basi territoriali.
