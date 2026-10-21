@echo off
rem TRAFFICO_RILANCIA_SENSORI.bat - Risultato 8 (traffico), pacchetto I.
rem Dopo ogni scarico dei dati da leopi: ricalcola i numeri dei sensori, la
rem taratura e il prodotto finale del metodo C. NON rifa il calcolo pesante dei
rem percorsi (pacchetto D), che non dipende dai sensori e resta in cache.
rem Prerequisito: aver gia' fatto almeno una volta TRAFFICO_RICALCOLA_MODELLO.bat.
rem Doppio clic. Log in logs\traffico_rilancia_sensori.log
rem
rem Ordine dei passi (script numerati):
rem   26  velocita'/flusso tipico dai sensori (legge il database storico)
rem   33  flusso per sensore (misure diurne)          -> flusso_5t_sensori.json
rem   35  sensori da escludere                        -> sensori_esclusi.json
rem   36  abbinamento sensore <-> corridoio per posizione
rem   38b codici lcd1 condivisi (controllo)
rem   37  metodi A e B + prova "nascondi un sensore"  -> traffico_stimato_AB.json
rem   43  dal flusso sui tratti ai corridoi           -> corridoi_modello.json
rem   44  taratura e validazione del metodo C (i criteri di riuscita)
rem   45  prodotto finale + relazione                 -> traffico_stimato_finale.json
rem   50b valutazione V3 vs V0 (i sensori cambiano)    -> v3/valutazione_v3.json
rem   53  pubblicazione v2 (numeri assoluti/relativi/graduatoria) -> traffico_stimato_finale_v2.json
rem   54  incrocio traffico x trasporto pubblico       -> risultato8_traffico_tp.json
rem (l'offerta di bus/tram, script 51-52, e il modello V3, script 49-50, NON
rem  cambiano con lo scarico dei sensori: si rifanno solo se cambia il GTFS o la rete.)
rem (43 c'era anche nel pacchetto E: serve dopo il 37 perche' raccoglie il tratto
rem  piu' vicino a ogni sensore, e il 44 legge il suo output.)

cd /d "%~dp0.."
if not exist logs mkdir logs
set "LOG=logs\traffico_rilancia_sensori.log"

echo === %date% %time% === > "%LOG%"

call :passo scripts\26_velocita_5t.py
call :passo scripts\33_flusso_sensori.py
call :passo scripts\35_sensori_esclusi.py
call :passo scripts\36_abbinamento_posizione.py
call :passo scripts\38b_codici_condivisi.py
call :passo scripts\37_traffico_AB.py
call :passo scripts\43_segmenti_corridoi.py
call :passo scripts\44_taratura_validazione.py
call :passo scripts\45_prodotto_finale.py
call :passo scripts\50b_v3_valutazione.py
call :passo scripts\53_pubblicazione_traffico.py
call :passo scripts\54_incrocio_traffico_tp.py
rem --- FASE 5: la valutazione, le fasce, la pubblicazione e le verifiche cambiano
rem     con i sensori; gli assi, le corsie, la ZTL, il TP per posizione (60-61) e il
rem     modello V4 (62) NON dipendono dai sensori (si rifanno solo se cambia la rete
rem     o il GTFS, con i comandi di docs\R8_traffico.md). ---
call :passo scripts\63_v4_valutazione.py
call :passo scripts\65_affidabilita.py
call :passo scripts\66_pubblicazione_incrocio.py
call :passo scripts\67_verifiche_fase5.py

python -c "import json;d=json.load(open('data/processed/traffico_c/taratura_validazione.json',encoding='utf-8'));e=d['varianti'][d['variante_finale']];print('--- NUMERI CHIAVE ---');print('classe di esito :',d['classe_esito']);print('errore mediano   : %.1f%%'%(100*e['errore_mediano']),'(metodo A: 36.9%)');print('rho di Spearman  : %.3f'%e['rho_loo']);print('unita confrontate:',d['n'])" >> "%LOG%" 2>&1
python -c "import json;d=json.load(open('data/processed/traffico_c/traffico_stimato_finale.json',encoding='utf-8'));c=d['conteggi_fiducia'];print('corridoi con fiducia alta/media/bassa:',c['alta'],'/',c['media'],'/',c['bassa'])" >> "%LOG%" 2>&1
python -c "import json;d=json.load(open('data/processed/traffico_c/v3/valutazione_v3.json',encoding='utf-8'));print('--- FASE 4 ---');print('variante finale  :',d['variante_finale']);print('classe di esito  :',d['classe_esito']);print('errore mediano   : %.1f%%'%(100*d['errore_mediano']));print('rho di Spearman  : %.3f'%d['rho_loo']);print('unita confrontate:',d['n'])" >> "%LOG%" 2>&1
python -c "import json;d=json.load(open('data/processed/traffico_d/valutazione_fase5.json',encoding='utf-8'));print('--- FASE 5 ---');print('variante finale  :',d['variante_finale']);print('classe di esito  :',d['classe_esito']);print('errore mediano   : %.1f%%'%(100*d['errore_mediano']));print('rho di Spearman  : %.3f'%d['rho_loo']);print('unita confrontate:',d['n'])" >> "%LOG%" 2>&1
python -c "import json;d=json.load(open('data/processed/risultato8_traffico_tp_v2.json',encoding='utf-8'));print('universo Torino :',d['universo_torino']['n_tratte'],'tratte,',d['universo_torino']['km'],'km');print('da guardare     :',d['conteggi']['da_guardare'],'di cui robuste',d['conteggi']['robusti']);print('accordo Leo 18/7:',d['accordo_leo']['n_giuste_18'],'/',d['accordo_leo']['n_giusti_7'])" >> "%LOG%" 2>&1

type "%LOG%"
echo.
echo FATTO. I numeri chiave sono in fondo al log. Se la classe di esito e' cambiata
echo rispetto a C-DEBOLE, dillo a Leo/Claude.
pause
exit /b 0

:passo
echo. >> "%LOG%"
echo --- %~1 --- >> "%LOG%"
python "%~1" >> "%LOG%" 2>&1
if errorlevel 1 (
  echo ERRORE in %~1 - mi fermo, vedi il log. >> "%LOG%"
  type "%LOG%"
  pause
  exit /b 1
)
exit /b 0
