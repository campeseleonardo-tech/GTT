# Decisione richiesta: T20-esegui-b
(Scrivi la tua risposta in fondo, dopo l'ultima riga 'RISPOSTA:'. Poi sposta il file task da blocked/ a queue/.)

STATUS: OPEN
Il bottone "Ripasso" in home attualmente avvia il ripasso solo per 'articoli'. Il brief prevedeva `avviaRipasso(progresso.livello)` ma la funzione richiede un parametro gioco (articoli/frasi/errori). Due opzioni:
A) Lasciare come è (parte da articoli, utente clicca di nuovo per altri giochi)
B) Cambiare il bottone per aprire un piccolo sottomenu con i 3 giochi che hanno debiti > 0
C) Far ciclare automaticamente la sessione tra tutti i giochi con debiti (più complesso)

Raccomandazione: B (sottomenu) – più chiaro per l'utente, basso sforzo implementativo.
Leo deve decidere prima di chiudere il task.

RISPOSTA:
B
