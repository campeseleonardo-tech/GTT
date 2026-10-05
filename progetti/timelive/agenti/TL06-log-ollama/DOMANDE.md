# DOMANDE per Leo

- Le misure prompt_eval vanno stampate anche nel CLI manuale? | opzioni: A (una riga in fondo alla stampa) / B (niente, solo nei dati) / C (riga nel CLI + nel report batch) | scelta: B | dove: code/llm_bridge.py (__main__) | perche: i numeri stanno già nei dati della risposta; stamparli a schermo è questione di gusto | cambia: A = ogni prova manuale mostra i numeri a video; B = a schermo non cambia niente; C = va modificato anche il file del report batch, che non ho potuto toccare ora
