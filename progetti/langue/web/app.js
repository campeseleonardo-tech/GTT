/* Langue – logica del sito (nessuna libreria, nessuna rete).
   Struttura del file:
   1. funzioni pure (mescolare, scegliere, controllare l'ordine, progressi): testabili senza browser
   2. salvataggio nel browser (localStorage, sempre dentro try/catch)
   3. interfaccia (si costruisce solo con textContent, mai con innerHTML) */
'use strict';

/* ========== 1. FUNZIONI PURE ========== */

/** Livelli selezionabili nel filtro della home. */
const LIVELLI = ['A1', 'A2', 'tutti'];

/** Chiavi dei tre giochi (sono anche le chiavi dei dati in window.LANGUE_DATA). */
const GIOCHI = ['articoli', 'frasi', 'errori'];

/** Chiave per i debiti (errori da ripassare) in localStorage. */
const CHIAVE_DEBITI = 'langue_debiti_v1';

/** Massimo numero di debiti per gioco. */
const MAX_DEBITI_PER_GIOCO = 50;

/** Mescola una copia della lista (Fisher-Yates). `rng` è una funzione che dà un numero in [0,1). */
function mescola(lista, rng) {
  const casuale = rng || Math.random;
  const copia = lista.slice();
  for (let i = copia.length - 1; i > 0; i--) {
    const j = Math.floor(casuale() * (i + 1));
    const tmp = copia[i];
    copia[i] = copia[j];
    copia[j] = tmp;
  }
  return copia;
}

/** Sceglie un elemento a caso, evitando se possibile quello appena uscito (`escludi`). Lista vuota -> null. */
function scegliCasuale(lista, rng, escludi) {
  if (!lista || lista.length === 0) return null;
  const casuale = rng || Math.random;
  let candidati = lista.filter(function (x) { return x !== escludi; });
  if (candidati.length === 0) candidati = lista;
  return candidati[Math.floor(casuale() * candidati.length)];
}

/** Un record è usabile nel sito solo se non è "da_verificare". */
function eUsabile(record) {
  return !!record && record.stato !== 'da_verificare';
}

/** Tiene i record usabili del livello richiesto ("tutti" = nessun filtro sul livello). */
function filtraPerLivello(lista, livello) {
  return (lista || []).filter(function (r) {
    return eUsabile(r) && (livello === 'tutti' || r.livello === livello);
  });
}

/** Rende una frase confrontabile: spazi singoli, niente spazi ai bordi, maiuscole/minuscole ignorate.
    (Si ignora tutto il maiuscolo/minuscolo, non solo la prima lettera: i blocchi hanno una forma fissa,
    quindi "Ich" a metà frase deve valere come "ich" nelle frasi alternative.) */
function normalizzaFrase(testo) {
  return String(testo).normalize('NFC').trim().replace(/\s+/g, ' ').toLowerCase();
}

/** Controlla se i blocchi messi dal giocatore (lista di testi) formano la frase giusta
    o una delle `alternative` del record. Si confrontano le frasi complete. */
function controllaOrdine(blocchiScelti, record) {
  const costruita = normalizzaFrase(blocchiScelti.join(' '));
  const ammesse = [record.testo_de].concat(record.alternative || []);
  return ammesse.some(function (frase) { return normalizzaFrase(frase) === costruita; });
}

/** Dà un ordine mescolato degli indici 0..n-1 dei blocchi, diverso dall'ordine giusto
    (se i blocchi non sono tutti uguali). Restituisce una lista di indici. */
function ordineMescolato(blocchi, rng) {
  const indici = blocchi.map(function (_, i) { return i; });
  const originale = blocchi.join('\u0001');
  const comeTesto = function (ord) { return ord.map(function (i) { return blocchi[i]; }).join('\u0001'); };
  for (let tentativo = 0; tentativo < 20; tentativo++) {
    const prova = mescola(indici, rng);
    if (comeTesto(prova) !== originale) return prova;
  }
  // Ultima risorsa: rotazione di un posto (diversa dall'originale se i blocchi non sono tutti uguali).
  return indici.slice(1).concat(indici.slice(0, 1));
}

/** Una domanda di "Trova l'errore": le due frasi in ordine casuale. */
function opzioniErrore(record, rng) {
  const casuale = rng || Math.random;
  const opzioni = [
    { testo: record.frase_sbagliata, corretta: false },
    { testo: record.frase_corretta, corretta: true }
  ];
  return casuale() < 0.5 ? opzioni : [opzioni[1], opzioni[0]];
}

/** Contatori a zero. */
function nuovoProgresso() {
  const giochi = {};
  GIOCHI.forEach(function (g) { giochi[g] = { giusti: 0, sbagliati: 0, migliorSerie: 0 }; });
  return { versione: 1, livello: 'tutti', giochi: giochi };
}

/** Numero intero >= 0, altrimenti 0 (difesa contro dati rovinati nel localStorage). */
function interoSicuro(n) {
  return (typeof n === 'number' && isFinite(n) && n >= 0) ? Math.floor(n) : 0;
}

/** Costruisce un progresso valido partendo da un oggetto qualsiasi (letto dal browser). */
function sistemaProgresso(grezzo) {
  const p = nuovoProgresso();
  if (!grezzo || typeof grezzo !== 'object') return p;
  if (LIVELLI.indexOf(grezzo.livello) !== -1) p.livello = grezzo.livello;
  const g = grezzo.giochi && typeof grezzo.giochi === 'object' ? grezzo.giochi : {};
  GIOCHI.forEach(function (nome) {
    const v = g[nome] && typeof g[nome] === 'object' ? g[nome] : {};
    p.giochi[nome].giusti = interoSicuro(v.giusti);
    p.giochi[nome].sbagliati = interoSicuro(v.sbagliati);
    p.giochi[nome].migliorSerie = interoSicuro(v.migliorSerie);
  });
  return p;
}

/** Registra una risposta. `serie` = serie di risposte giuste di fila DOPO questa risposta. */
function registraRisposta(progresso, gioco, giusta, serie) {
  const c = progresso.giochi[gioco];
  if (giusta) c.giusti += 1; else c.sbagliati += 1;
  if (serie > c.migliorSerie) c.migliorSerie = serie;
  return progresso;
}

/* ========== DEBITI (RIPASSO DEGLI SBAGLI) ========== */

/** Struttura debito: { articoli: [{id, volte}], frasi: [{id, volte}], errori: [{id, volte}] } */
function nuovoDebito() {
  const d = {};
  GIOCHI.forEach(function (g) { d[g] = []; });
  return d;
}

/** Carica i debiti da localStorage; se manca o è corrotto, restituisce struttura vuota. */
function caricaDebiti(storage) {
  if (!storage) return nuovoDebito();
  try {
    const testo = storage.getItem(CHIAVE_DEBITI);
    if (!testo) return nuovoDebito();
    const grezzo = JSON.parse(testo);
    const d = nuovoDebito();
    GIOCHI.forEach(function (g) {
      const arr = Array.isArray(grezzo[g]) ? grezzo[g] : [];
      d[g] = arr
        .filter(function (x) { return x && typeof x.id === 'string' && typeof x.volte === 'number'; })
        .map(function (x) { return { id: x.id, volte: Math.max(1, interoSicuro(x.volte)) }; }) // [agente T22]
        .slice(0, MAX_DEBITI_PER_GIOCO);
    });
    return d;
  } catch (e) {
    return nuovoDebito();
  }
}

/** Salva i debiti in localStorage; restituisce true se riuscito. */
function salvaDebiti(storage, debito) {
  if (!storage) return false;
  try {
    storage.setItem(CHIAVE_DEBITI, JSON.stringify(debito));
    return true;
  } catch (e) {
    return false;
  }
}

/** Aggiunge un debito per (gioco, id). Incrementa `volte` se esiste, altrimenti lo inserisce in testa.
    Mantiene al massimo MAX_DEBITI_PER_GIOCO item per gioco (scarta i più vecchi in coda). */
function aggiungiDebito(debito, gioco, id) {
  const lista = debito[gioco];
  if (!lista) return;
  let trovato = false;
  for (let i = 0; i < lista.length; i++) {
    if (lista[i].id === id) {
      lista[i].volte += 1;
      // sposta in testa per priorità (più errori recenti/frequenti prima)
      const item = lista.splice(i, 1)[0];
      lista.unshift(item);
      trovato = true;
      break;
    }
  }
  if (!trovato) {
    lista.unshift({ id: id, volte: 1 });
  }
  // taglia se supera il limite
  if (lista.length > MAX_DEBITI_PER_GIOCO) {
    lista.length = MAX_DEBITI_PER_GIOCO;
  }
}

/** Rimuove un debito per (gioco, id) se presente. */
function rimuoviDebito(debito, gioco, id) {
  const lista = debito[gioco];
  if (!lista) return;
  const idx = lista.findIndex(function (x) { return x.id === id; });
  if (idx !== -1) lista.splice(idx, 1);
}

/** Restituisce l'array dei debiti per un gioco, ordinato per `volte` decrescente (già mantenuto). */
function getDebitiPerGioco(debito, gioco) {
  return (debito[gioco] || []).slice();
}

/** Totale debiti tra tutti i giochi. */
function totaleDebiti(debito) {
  let tot = 0;
  GIOCHI.forEach(function (g) { tot += (debito[g] || []).length; });
  return tot;
}

/** Totali per la home: risposte giuste, sbagliate, migliore serie tra i giochi. */
function riepilogo(progresso) {
  let giusti = 0, sbagliati = 0, migliorSerie = 0;
  GIOCHI.forEach(function (g) {
    const c = progresso.giochi[g];
    giusti += c.giusti;
    sbagliati += c.sbagliati;
    migliorSerie = Math.max(migliorSerie, c.migliorSerie);
  });
  return { giusti: giusti, sbagliati: sbagliati, migliorSerie: migliorSerie };
}

/* Per provare le funzioni pure con Node (non serve al sito). */
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    mescola, scegliCasuale, eUsabile, filtraPerLivello, normalizzaFrase, controllaOrdine,
    ordineMescolato, opzioniErrore, nuovoProgresso, sistemaProgresso, registraRisposta, riepilogo
  };
}

/* ========== 2. SALVATAGGIO NEL BROWSER ========== */

const CHIAVE_PROGRESSI = 'langue_progress_v1';

/** Dà il localStorage se è utilizzabile, altrimenti null (anche solo leggerlo può dare errore se è bloccato). */
function trovaStorage() {
  try {
    return window.localStorage || null;
  } catch (e) {
    return null;
  }
}

/** Legge i progressi salvati; in caso di problemi parte da zero. */
function caricaProgresso(storage) {
  if (!storage) return nuovoProgresso();
  try {
    const testo = storage.getItem(CHIAVE_PROGRESSI);
    return testo ? sistemaProgresso(JSON.parse(testo)) : nuovoProgresso();
  } catch (e) {
    return nuovoProgresso();
  }
}

/** Salva i progressi; restituisce true se è riuscito. */
function salvaProgresso(storage, progresso) {
  if (!storage) return false;
  try {
    storage.setItem(CHIAVE_PROGRESSI, JSON.stringify(progresso));
    return true;
  } catch (e) {
    return false;
  }
}

/* ========== 3. INTERFACCIA ========== */

if (typeof document !== 'undefined') {
  avviaSito();
}

function avviaSito() {
  const grezzi = window.LANGUE_DATA || {};
  const dati = {
    articoli: Array.isArray(grezzi.articoli) ? grezzi.articoli : [],
    frasi: Array.isArray(grezzi.frasi) ? grezzi.frasi : [],
    errori: Array.isArray(grezzi.errori) ? grezzi.errori : []
  };
  const storage = trovaStorage();
  let progresso = caricaProgresso(storage);
  let debito = caricaDebiti(storage);

  const vistaHome = document.getElementById('vista-home');
  const vistaGioco = document.getElementById('vista-gioco');
  const titoloGioco = document.getElementById('titolo-gioco');
  const area = document.getElementById('area-gioco');
  const avvisoDati = document.getElementById('avviso-dati');
  const avvisoSalvataggio = document.getElementById('avviso-salvataggio');

  const ARTICOLI = ['der', 'die', 'das'];

  /* --- piccoli aiuti per costruire la pagina senza innerHTML --- */

  /** Crea un elemento. opz: classe, testo, attr (oggetto), al (funzione per il click), lingua. */
  function el(tag, opz, figli) {
    const n = document.createElement(tag);
    const o = opz || {};
    if (o.classe) n.className = o.classe;
    if (o.testo !== undefined) n.textContent = o.testo;
    if (o.attr) Object.keys(o.attr).forEach(function (k) { n.setAttribute(k, o.attr[k]); });
    if (o.lingua) n.setAttribute('lang', o.lingua);
    if (o.al) n.addEventListener('click', o.al);
    (figli || []).forEach(function (f) { n.appendChild(f); });
    return n;
  }

  function bottone(testo, classe, al, attr) {
    const a = { type: 'button' };
    if (attr) Object.keys(attr).forEach(function (k) { a[k] = attr[k]; });
    return el('button', { classe: 'btn ' + (classe || ''), testo: testo, al: al, attr: a });
  }

  function svuota(nodo) {
    while (nodo.firstChild) nodo.removeChild(nodo.firstChild);
  }

  function salva() {
    // [agente T22] avviso corretto anche se il salvataggio dei debiti fallisce
    const okProgressi = salvaProgresso(storage, progresso);
    const okDebiti = salvaDebiti(storage, debito);
    avvisoSalvataggio.hidden = okProgressi && okDebiti;
  }

  /* --- home --- */

  /** Record disponibili per un gioco con il livello scelto. */
  function disponibili(gioco) {
    let lista = filtraPerLivello(dati[gioco], progresso.livello);
    if (gioco === 'articoli') {
      lista = lista.filter(function (r) { return ARTICOLI.indexOf(r.articolo) !== -1 && r.parola; });
    } else if (gioco === 'frasi') {
      lista = lista.filter(function (r) { return Array.isArray(r.blocchi) && r.blocchi.length > 1; });
    } else {
      lista = lista.filter(function (r) { return r.frase_sbagliata && r.frase_corretta; });
    }
    return lista;
  }

  /** Trova un record per id in un array di dati. */
  function trovaRecordPerId(lista, id) {
    for (let i = 0; i < lista.length; i++) {
      if (lista[i].id === id) return lista[i];
    }
    return null;
  }

  function aggiornaHome() {
    // filtro livello
    document.querySelectorAll('input[name="livello"]').forEach(function (r) {
      r.checked = (r.value === progresso.livello);
    });
    // schede dei giochi + statistiche
    const etichette = { articoli: 'parole', frasi: 'frasi', errori: 'errori' };
    GIOCHI.forEach(function (g) {
      const n = disponibili(g).length;
      const btn = document.getElementById('gioca-' + g);
      document.getElementById('conta-' + g).textContent =
        n === 0 ? 'Nessun contenuto per questo livello' : n + ' ' + etichette[g] + ' disponibili';
      btn.disabled = (n === 0);
      const c = progresso.giochi[g];
      document.getElementById('stat-' + g).textContent =
        'Giuste: ' + c.giusti + ' · Sbagliate: ' + c.sbagliati + ' · Serie migliore: ' + c.migliorSerie;
    });
    // scheda Ripasso
    const totDebiti = totaleDebiti(debito);
    const btnRipasso = document.getElementById('gioca-ripasso');
    if (btnRipasso) {
      document.getElementById('conta-ripasso').textContent =
        totDebiti === 0 ? 'Nessun errore da ripassare' : totDebiti + ' errori da ripassare';
      btnRipasso.disabled = (totDebiti === 0);
      // stat per ripasso: quanti debiti per gioco
      const dettagli = GIOCHI.map(function (g) {
        const n = (debito[g] || []).length;
        return n > 0 ? g + ': ' + n : null;
      }).filter(Boolean).join(' · ');
      document.getElementById('stat-ripasso').textContent = dettagli || '—';
    }
    // contatori nel sottomenu ripasso
    GIOCHI.forEach(function (g) {
      const n = (debito[g] || []).length;
      const elConteggio = document.getElementById('conta-ripasso-' + g);
      if (elConteggio) {
        elConteggio.textContent = n === 0 ? 'nessun debito' : n + ' error' + (n === 1 ? 'e' : 'i') + ' da ripassare';
      }
      const btn = document.getElementById('ripasso-' + g);
      if (btn) btn.disabled = (n === 0);
    });
    const tot = riepilogo(progresso);
    const risposte = tot.giusti + tot.sbagliati;
    document.getElementById('riepilogo').textContent = risposte === 0
      ? 'Non hai ancora risposto a nulla: scegli un gioco e inizia!'
      : 'Risposte giuste: ' + tot.giusti + ' su ' + risposte + ' (' + Math.round(100 * tot.giusti / risposte) +
        '%) · Serie migliore: ' + tot.migliorSerie;
    const nessunDato = GIOCHI.every(function (g) { return dati[g].length === 0; });
    avvisoDati.hidden = !nessunDato;
  }

  function mostraHome() {
    vistaGioco.hidden = true;
    vistaHome.hidden = false;
    svuota(area);
    aggiornaHome();
    document.title = 'Langue – impara il tedesco';
    document.getElementById('titolo-home').focus();
  }

  function mostraGioco(titolo) {
    vistaHome.hidden = true;
    vistaGioco.hidden = false;
    titoloGioco.textContent = titolo;
    document.title = titolo + ' – Langue';
    svuota(area);
  }

  /* --- parte comune a tutti i giochi: barra della serie, corpo, messaggio, tasto Avanti --- */

  function creaSessione(gioco, alProssimo) {
    const sessione = { serie: 0 };
    const barra = el('p', { classe: 'barra-serie' });
    const corpo = el('div', { classe: 'corpo' });
    const messaggio = el('div', { classe: 'messaggio', attr: { role: 'status', 'aria-live': 'polite' } });
    const avanti = bottone('Avanti →', 'primario', alProssimo);
    avanti.hidden = true;
    const azioni = el('div', { classe: 'azioni' }, [avanti]);
    area.appendChild(barra);
    area.appendChild(corpo);
    area.appendChild(messaggio);
    area.appendChild(azioni);

    function aggiornaBarra() {
      barra.textContent = 'Serie: ' + sessione.serie + ' · Record: ' + progresso.giochi[gioco].migliorSerie;
    }
    aggiornaBarra();

    sessione.corpo = corpo;
    sessione.azioni = azioni;
    sessione.avanti = avanti;

    /** Prepara una nuova domanda: toglie messaggio e tasto Avanti. */
    sessione.nuovaDomanda = function () {
      svuota(messaggio);
      messaggio.className = 'messaggio';
      avanti.hidden = true;
    };
    /** Registra la risposta (giusta/sbagliata) e aggiorna serie e contatori. */
    sessione.registra = function (giusta) {
      sessione.serie = giusta ? sessione.serie + 1 : 0;
      registraRisposta(progresso, gioco, giusta, sessione.serie);
      salva();
      aggiornaBarra();
    };
    /** Mostra un messaggio: `tipo` = 'ok' | 'ko' | 'info'; `righe` = lista di {testo, lingua}. */
    sessione.messaggio = function (tipo, righe) {
      svuota(messaggio);
      messaggio.className = 'messaggio ' + tipo;
      righe.forEach(function (r) {
        messaggio.appendChild(el('p', { testo: r.testo, lingua: r.lingua, classe: r.classe }));
      });
    };
    /** Domanda conclusa: mostra Avanti e ci porta il focus. */
    sessione.mostraAvanti = function () {
      avanti.hidden = false;
      avanti.focus();
    };
    return sessione;
  }

  /* --- Gioco 1: Der, die o das? --- */

  function giocoArticoli() {
    const pool = disponibili('articoli');
    mostraGioco('Der, die o das?');
    let corrente = null;
    const sessione = creaSessione('articoli', prossima);

    function prossima() {
      corrente = scegliCasuale(pool, null, corrente);
      sessione.nuovaDomanda();
      svuota(sessione.corpo);
      sessione.corpo.appendChild(el('p', { classe: 'istruzione', testo: 'Qual è l’articolo di questa parola?' }));
      sessione.corpo.appendChild(el('p', { classe: 'parola-grande', testo: corrente.parola, lingua: 'de' }));
      const riga = el('div', { classe: 'tre-bottoni', attr: { role: 'group', 'aria-label': 'Articolo' } });
      ARTICOLI.forEach(function (art) {
        riga.appendChild(bottone(art, 'articolo', function () { rispondi(art, riga); }, { lang: 'de' }));
      });
      sessione.corpo.appendChild(riga);
      riga.firstChild.focus();
    }

    function rispondi(scelto, riga) {
      const giusta = (scelto === corrente.articolo);
      riga.querySelectorAll('button').forEach(function (b) {
        b.disabled = true;
        if (b.textContent === corrente.articolo) {
          b.classList.add('giusto');
          b.textContent = '✓ ' + b.textContent;
        } else if (b.textContent === scelto) {
          b.classList.add('sbagliato');
          b.textContent = '✗ ' + b.textContent;
        }
      });
      sessione.registra(giusta);
      if (!giusta) {
        aggiungiDebito(debito, 'articoli', corrente.id);
        salva();
        aggiornaHome();
      }
      sessione.messaggio(giusta ? 'ok' : 'ko', [
        { testo: giusta ? 'Giusto!' : 'Non proprio.', classe: 'esito' },
        { testo: corrente.articolo + ' ' + corrente.parola, lingua: 'de', classe: 'de-grande' },
        { testo: 'In italiano: ' + corrente.traduzione_it }
      ]);
      sessione.mostraAvanti();
    }

    prossima();
  }

  /* --- Gioco 2: Rimetti in ordine --- */

  function giocoFrasi() {
    const pool = disponibili('frasi');
    mostraGioco('Rimetti in ordine');
    let corrente = null;
    let ordine = [];       // indici dei blocchi nell'ordine mescolato
    let scelti = [];       // indici dei blocchi scelti, nell'ordine in cui li ha messi il giocatore
    let chiusa = false;    // domanda conclusa (giusta o soluzione mostrata)
    let registrata = false; // la prima verifica conta una sola volta
    const sessione = creaSessione('frasi', prossima);

    function prossima() {
      corrente = scegliCasuale(pool, null, corrente);
      ordine = ordineMescolato(corrente.blocchi);
      scelti = [];
      chiusa = false;
      registrata = false;
      sessione.nuovaDomanda();
      disegna(null);
    }

    /** Ridisegna la domanda. `focus` = indice del blocco a cui dare il focus, 'controlla' o null. */
    function disegna(focus) {
      const corpo = sessione.corpo;
      svuota(corpo);
      corpo.appendChild(el('p', { classe: 'istruzione', testo: 'Tocca i blocchi nell’ordine giusto per formare la frase.' }));
      corpo.appendChild(el('p', { classe: 'suggerimento', testo: 'Suggerimento: ' + corrente.traduzione_it }));

      // frase costruita finora (toccando un blocco lo si toglie)
      const costruita = el('div', { classe: 'costruita', attr: { role: 'group', 'aria-label': 'La tua frase' } });
      if (scelti.length === 0) {
        costruita.appendChild(el('span', { classe: 'segnaposto', testo: 'La tua frase comparirà qui' }));
      }
      scelti.forEach(function (i) {
        costruita.appendChild(bottone(corrente.blocchi[i], 'blocco scelto', function () { togli(i); },
          { lang: 'de', 'data-i': String(i), 'aria-label': corrente.blocchi[i] + ' (tocca per toglierlo)' }));
      });
      corpo.appendChild(costruita);

      // blocchi ancora da usare
      const rimasti = el('div', { classe: 'rimasti', attr: { role: 'group', 'aria-label': 'Blocchi disponibili' } });
      ordine.forEach(function (i) {
        if (scelti.indexOf(i) === -1) {
          rimasti.appendChild(bottone(corrente.blocchi[i], 'blocco', function () { metti(i); },
            { lang: 'de', 'data-i': String(i) }));
        }
      });
      corpo.appendChild(rimasti);

      if (chiusa) {
        costruita.querySelectorAll('button').forEach(function (b) { b.disabled = true; });
        return;
      }

      const azioni = el('div', { classe: 'azioni' });
      const controlla = bottone('Controlla', 'primario', controllaClick, { id: 'btn-controlla' });
      azioni.appendChild(controlla);
      azioni.appendChild(bottone('Ricomincia', '', function () { scelti = []; sessione.messaggio('info', []); disegna(null); }));
      azioni.appendChild(bottone('Mostra la soluzione', '', mostraSoluzione));
      corpo.appendChild(azioni);

      if (focus === 'controlla') {
        controlla.focus();
      } else if (focus !== null && focus !== undefined) {
        const b = corpo.querySelector('button[data-i="' + focus + '"]');
        if (b) b.focus();
      }
    }

    function metti(i) {
      if (chiusa) return;
      scelti.push(i);
      // dopo aver scelto, il focus passa al prossimo blocco libero (o a "Controlla")
      const prossimo = ordine.find(function (k) { return scelti.indexOf(k) === -1; });
      disegna(prossimo === undefined ? 'controlla' : prossimo);
    }

    function togli(i) {
      if (chiusa) return;
      scelti = scelti.filter(function (k) { return k !== i; });
      disegna(i);
    }

    function controllaClick() {
      if (scelti.length < corrente.blocchi.length) {
        sessione.messaggio('info', [{ testo: 'Usa tutti i blocchi prima di controllare.' }]);
        return;
      }
      const testi = scelti.map(function (i) { return corrente.blocchi[i]; });
      if (controllaOrdine(testi, corrente)) {
        if (!registrata) sessione.registra(true);
        registrata = true;
        chiusa = true;
        sessione.messaggio('ok', [
          { testo: 'Giusto!', classe: 'esito' },
          { testo: testi.join(' '), lingua: 'de', classe: 'de-grande' },
          { testo: corrente.traduzione_it }
        ]);
        disegna(null);
        sessione.mostraAvanti();
      } else {
        if (!registrata) {
          sessione.registra(false);
          aggiungiDebito(debito, 'frasi', corrente.id);
          salva();
          aggiornaHome();
        }
        registrata = true;
        sessione.messaggio('ko', [{ testo: 'Non è ancora giusto: riprova, oppure guarda la soluzione.', classe: 'esito' }]);
      }
    }

    function mostraSoluzione() {
      if (!registrata) {
        sessione.registra(false);
        aggiungiDebito(debito, 'frasi', corrente.id);
        salva();
        aggiornaHome();
      }
      registrata = true;
      chiusa = true;
      sessione.messaggio('info', [
        { testo: 'Una soluzione possibile:' },
        { testo: corrente.testo_de, lingua: 'de', classe: 'de-grande' },
        { testo: corrente.traduzione_it }
      ]);
      disegna(null);
      sessione.mostraAvanti();
    }

    prossima();
  }

  /* --- Gioco 3: Trova l'errore --- */

  function giocoErrori() {
    const pool = disponibili('errori');
    mostraGioco('Trova l’errore');
    let corrente = null;
    const sessione = creaSessione('errori', prossima);

    function prossima() {
      corrente = scegliCasuale(pool, null, corrente);
      sessione.nuovaDomanda();
      svuota(sessione.corpo);
      sessione.corpo.appendChild(el('p', { classe: 'istruzione', testo: 'Quale frase è scritta correttamente?' }));
      const gruppo = el('div', { classe: 'due-opzioni', attr: { role: 'group', 'aria-label': 'Le due frasi' } });
      opzioniErrore(corrente).forEach(function (op) {
        const b = bottone(op.testo, 'opzione', function () { rispondi(op, gruppo); }, { lang: 'de' });
        b._corretta = op.corretta;
        gruppo.appendChild(b);
      });
      sessione.corpo.appendChild(gruppo);
      gruppo.firstChild.focus();
    }

    function rispondi(scelta, gruppo) {
      gruppo.querySelectorAll('button').forEach(function (b) {
        b.disabled = true;
        if (b._corretta) {
          b.classList.add('giusto');
          b.textContent = '✓ ' + b.textContent;
        } else if (b.textContent === scelta.testo) {
          b.classList.add('sbagliato');
          b.textContent = '✗ ' + b.textContent;
        }
      });
      sessione.registra(scelta.corretta);
      if (!scelta.corretta) {
        aggiungiDebito(debito, 'errori', corrente.id);
        salva();
        aggiornaHome();
      }
      sessione.messaggio(scelta.corretta ? 'ok' : 'ko', [
        { testo: scelta.corretta ? 'Giusto!' : 'Non proprio.', classe: 'esito' },
        { testo: 'Frase corretta: ' + corrente.frase_corretta, lingua: 'de', classe: 'de-grande' },
        { testo: corrente.spiegazione_it }
      ]);
      sessione.mostraAvanti();
    }

    prossima();
  }

  /* --- Gioco 4: Ripasso degli sbagli --- */

  /** Crea una sessione di ripasso per un gioco specifico. */
  function creaSessioneRipasso(gioco, alProssimo) {
    const debitiGioco = getDebitiPerGioco(debito, gioco);
    const sessione = { serie: 0, debitiRimasti: debitiGioco.slice() };
    const barra = el('p', { classe: 'barra-serie' });
    const corpo = el('div', { classe: 'corpo' });
    const messaggio = el('div', { classe: 'messaggio', attr: { role: 'status', 'aria-live': 'polite' } });
    const avanti = bottone('Avanti →', 'primario', function () {
      // Se il debito corrente è ancora in testa (risposta sbagliata), spostalo in coda
      if (sessione.debitiRimasti.length > 0) {
        const corrente = sessione.debitiRimasti[0];
        // Verifica se il debito corrente è stato rimosso (risposta giusta)
        // Se è ancora lì, significa che la risposta era sbagliata -> ruota
        const ancoraPresente = sessione.debitiRimasti.some(function (d) { return d.id === corrente.id; });
        if (ancoraPresente) {
          sessione.debitiRimasti.push(sessione.debitiRimasti.shift());
        }
      }
      alProssimo();
    });
    avanti.hidden = true;
    const azioni = el('div', { classe: 'azioni' }, [avanti]);
    area.appendChild(barra);
    area.appendChild(corpo);
    area.appendChild(messaggio);
    area.appendChild(azioni);

    function aggiornaBarra() {
      barra.textContent = 'Ripasso — Serie: ' + sessione.serie + ' · Rimasti: ' + sessione.debitiRimasti.length;
    }
    aggiornaBarra();

    sessione.corpo = corpo;
    sessione.azioni = azioni;
    sessione.avanti = avanti;
    sessione.gioco = gioco;

    sessione.nuovaDomanda = function () {
      svuota(messaggio);
      messaggio.className = 'messaggio';
      avanti.hidden = true;
    };

    sessione.registra = function (giusta) {
      sessione.serie = giusta ? sessione.serie + 1 : 0;
      registraRisposta(progresso, gioco, giusta, sessione.serie);
      salva();
      aggiornaBarra();
    };

    sessione.messaggio = function (tipo, righe) {
      svuota(messaggio);
      messaggio.className = 'messaggio ' + tipo;
      righe.forEach(function (r) {
        messaggio.appendChild(el('p', { testo: r.testo, lingua: r.lingua, classe: r.classe }));
      });
    };

    sessione.mostraAvanti = function () {
      avanti.hidden = false;
      avanti.focus();
    };

    sessione.rimuoviDebitoCorrente = function (id) {
      rimuoviDebito(debito, gioco, id);
      salva();
      aggiornaHome();
      // rimuovi anche dalla lista locale
      sessione.debitiRimasti = sessione.debitiRimasti.filter(function (d) { return d.id !== id; });
      aggiornaBarra(); // [agente T22]
    };

    return sessione;
  }

  /** Avvia la sessione di ripasso per un gioco. */
  function avviaRipasso(gioco) {
    const debitiGioco = getDebitiPerGioco(debito, gioco);
    if (debitiGioco.length === 0) {
      sessioneVuotaRipasso(gioco);
      return;
    }
    const titoli = { articoli: 'Ripasso — Articoli', frasi: 'Ripasso — Frasi', errori: 'Ripasso — Errori' };
    mostraGioco(titoli[gioco] || 'Ripasso');

    const sessioneRipasso = creaSessioneRipasso(gioco, prossimaRipasso);

    function prossimaRipasso() {
      if (sessioneRipasso.debitiRimasti.length === 0) {
        // tutti i debiti processati, torna alla home
        mostraHome();
        return;
      }
      const debitoItem = sessioneRipasso.debitiRimasti[0];
      const record = trovaRecordPerId(dati[gioco], debitoItem.id);
      if (!record) {
        // record non trovato (es. rimosso dai dati), salta e rimuovi dal debito
        sessioneRipasso.rimuoviDebitoCorrente(debitoItem.id);
        prossimaRipasso();
        return;
      }
      sessioneRipasso.nuovaDomanda();
      disegnaDomandaRipasso(gioco, record, sessioneRipasso);
    }

    prossimaRipasso();
  }

  /** Disegna una domanda di ripasso usando i renderer dei giochi normali. */
  function disegnaDomandaRipasso(gioco, record, sessione) {
    const corpo = sessione.corpo;
    svuota(corpo);

    if (gioco === 'articoli') {
      corpo.appendChild(el('p', { classe: 'istruzione', testo: 'Ripasso: qual è l’articolo di questa parola?' }));
      corpo.appendChild(el('p', { classe: 'parola-grande', testo: record.parola, lingua: 'de' }));
      const riga = el('div', { classe: 'tre-bottoni', attr: { role: 'group', 'aria-label': 'Articolo' } });
      ARTICOLI.forEach(function (art) {
        riga.appendChild(bottone(art, 'articolo', function () { rispondiRipassoArticoli(art, riga, record, sessione); }, { lang: 'de' }));
      });
      corpo.appendChild(riga);
      riga.firstChild.focus();
    } else if (gioco === 'frasi') {
      // riutilizza la logica di giocoFrasi ma con record fisso
      let ordine = ordineMescolato(record.blocchi);
      let scelti = [];
      let chiusa = false;
      let registrata = false;

      function ridisegna(focus) {
        svuota(corpo);
        corpo.appendChild(el('p', { classe: 'istruzione', testo: 'Ripasso: tocca i blocchi nell’ordine giusto per formare la frase.' }));
        corpo.appendChild(el('p', { classe: 'suggerimento', testo: 'Suggerimento: ' + record.traduzione_it }));

        const costruita = el('div', { classe: 'costruita', attr: { role: 'group', 'aria-label': 'La tua frase' } });
        if (scelti.length === 0) {
          costruita.appendChild(el('span', { classe: 'segnaposto', testo: 'La tua frase comparirà qui' }));
        }
        scelti.forEach(function (i) {
          costruita.appendChild(bottone(record.blocchi[i], 'blocco scelto', function () { togliRipasso(i); },
            { lang: 'de', 'data-i': String(i), 'aria-label': record.blocchi[i] + ' (tocca per toglierlo)' }));
        });
        corpo.appendChild(costruita);

        const rimasti = el('div', { classe: 'rimasti', attr: { role: 'group', 'aria-label': 'Blocchi disponibili' } });
        ordine.forEach(function (i) {
          if (scelti.indexOf(i) === -1) {
            rimasti.appendChild(bottone(record.blocchi[i], 'blocco', function () { mettiRipasso(i); },
              { lang: 'de', 'data-i': String(i) }));
          }
        });
        corpo.appendChild(rimasti);

        if (chiusa) {
          costruita.querySelectorAll('button').forEach(function (b) { b.disabled = true; });
          return;
        }

        const azioni = el('div', { classe: 'azioni' });
        const controlla = bottone('Controlla', 'primario', function () { controllaClickRipasso(); }, { id: 'btn-controlla' });
        azioni.appendChild(controlla);
        azioni.appendChild(bottone('Ricomincia', '', function () { scelti = []; sessione.messaggio('info', []); ridisegna(null); }));
        azioni.appendChild(bottone('Mostra la soluzione', '', function () { mostraSoluzioneRipasso(); }));
        corpo.appendChild(azioni);

        if (focus === 'controlla') {
          controlla.focus();
        } else if (focus !== null && focus !== undefined) {
          const b = corpo.querySelector('button[data-i="' + focus + '"]');
          if (b) b.focus();
        }
      }

      function mettiRipasso(i) {
        if (chiusa) return;
        scelti.push(i);
        const prossimo = ordine.find(function (k) { return scelti.indexOf(k) === -1; });
        ridisegna(prossimo === undefined ? 'controlla' : prossimo);
      }

      function togliRipasso(i) {
        if (chiusa) return;
        scelti = scelti.filter(function (k) { return k !== i; });
        ridisegna(i);
      }

      function controllaClickRipasso() {
        if (scelti.length < record.blocchi.length) {
          sessione.messaggio('info', [{ testo: 'Usa tutti i blocchi prima di controllare.' }]);
          return;
        }
        const testi = scelti.map(function (i) { return record.blocchi[i]; });
        if (controllaOrdine(testi, record)) {
          if (!registrata) {
            sessione.registra(true);
            sessione.rimuoviDebitoCorrente(record.id);
          }
          registrata = true;
          chiusa = true;
          sessione.messaggio('ok', [
            { testo: 'Giusto!', classe: 'esito' },
            { testo: testi.join(' '), lingua: 'de', classe: 'de-grande' },
            { testo: record.traduzione_it }
          ]);
          ridisegna(null);
          sessione.mostraAvanti();
        } else {
          if (!registrata) {
            sessione.registra(false);
            // il debito rimane, volte già incrementato durante il gioco normale
          }
          registrata = true;
          sessione.messaggio('ko', [{ testo: 'Non è ancora giusto: riprova, oppure guarda la soluzione.', classe: 'esito' }]);
        }
      }

      function mostraSoluzioneRipasso() {
        if (!registrata) {
          sessione.registra(false);
          // chi ha guardato la soluzione in ripasso non rimuove il debito
        }
        registrata = true;
        chiusa = true;
        sessione.messaggio('info', [
          { testo: 'Una soluzione possibile:' },
          { testo: record.testo_de, lingua: 'de', classe: 'de-grande' },
          { testo: record.traduzione_it }
        ]);
        ridisegna(null);
        sessione.mostraAvanti();
      }

      ridisegna(null);
    } else if (gioco === 'errori') {
      corpo.appendChild(el('p', { classe: 'istruzione', testo: 'Ripasso: quale frase è scritta correttamente?' }));
      const gruppo = el('div', { classe: 'due-opzioni', attr: { role: 'group', 'aria-label': 'Le due frasi' } });
      opzioniErrore(record).forEach(function (op) {
        const b = bottone(op.testo, 'opzione', function () { rispondiRipassoErrori(op, gruppo, record, sessione); }, { lang: 'de' });
        b._corretta = op.corretta;
        gruppo.appendChild(b);
      });
      corpo.appendChild(gruppo);
      gruppo.firstChild.focus();
    }
  }

  function rispondiRipassoArticoli(scelto, riga, record, sessione) {
    const giusta = (scelto === record.articolo);
    riga.querySelectorAll('button').forEach(function (b) {
      b.disabled = true;
      if (b.textContent === record.articolo) {
        b.classList.add('giusto');
        b.textContent = '✓ ' + b.textContent;
      } else if (b.textContent === scelto) {
        b.classList.add('sbagliato');
        b.textContent = '✗ ' + b.textContent;
      }
    });
    sessione.registra(giusta);
    if (giusta) {
      sessione.rimuoviDebitoCorrente(record.id);
    }
    sessione.messaggio(giusta ? 'ok' : 'ko', [
      { testo: giusta ? 'Giusto!' : 'Non proprio.', classe: 'esito' },
      { testo: record.articolo + ' ' + record.parola, lingua: 'de', classe: 'de-grande' },
      { testo: 'In italiano: ' + record.traduzione_it }
    ]);
    sessione.mostraAvanti();
  }

  function rispondiRipassoErrori(scelta, gruppo, record, sessione) {
    gruppo.querySelectorAll('button').forEach(function (b) {
      b.disabled = true;
      if (b._corretta) {
        b.classList.add('giusto');
        b.textContent = '✓ ' + b.textContent;
      } else if (b.textContent === scelta.testo) {
        b.classList.add('sbagliato');
        b.textContent = '✗ ' + b.textContent;
      }
    });
    sessione.registra(scelta.corretta);
    if (scelta.corretta) {
      sessione.rimuoviDebitoCorrente(record.id);
    }
    sessione.messaggio(scelta.corretta ? 'ok' : 'ko', [
      { testo: scelta.corretta ? 'Giusto!' : 'Non proprio.', classe: 'esito' },
      { testo: 'Frase corretta: ' + record.frase_corretta, lingua: 'de', classe: 'de-grande' },
      { testo: record.spiegazione_it }
    ]);
    sessione.mostraAvanti();
  }

  /** Mostra messaggio quando non ci sono debiti per un gioco. */
  function sessioneVuotaRipasso(gioco) {
    const titoli = { articoli: 'Ripasso — Articoli', frasi: 'Ripasso — Frasi', errori: 'Ripasso — Errori' };
    mostraGioco(titoli[gioco] || 'Ripasso');
    svuota(area);
    area.appendChild(el('p', { classe: 'istruzione', testo: 'Nessun errore da ripassare per questo gioco.' }));
    area.appendChild(el('p', { testo: 'Bravo! Torna alla home per scegliere un altro gioco.' }));
    area.appendChild(bottone('Torna alla home', 'primario', mostraHome));
  }

  /* --- collegamenti dei pulsanti della home --- */

  document.getElementById('gioca-articoli').addEventListener('click', giocoArticoli);
  document.getElementById('gioca-frasi').addEventListener('click', giocoFrasi);
  document.getElementById('gioca-errori').addEventListener('click', giocoErrori);
  document.getElementById('gioca-ripasso').addEventListener('click', apriSottomenuRipasso);
  document.getElementById('torna-home').addEventListener('click', mostraHome);

  document.getElementById('ripasso-articoli').addEventListener('click', function () { avviaRipasso('articoli'); chiudiSottomenuRipasso(); });
  document.getElementById('ripasso-frasi').addEventListener('click', function () { avviaRipasso('frasi'); chiudiSottomenuRipasso(); });
  document.getElementById('ripasso-errori').addEventListener('click', function () { avviaRipasso('errori'); chiudiSottomenuRipasso(); });
  document.getElementById('chiudi-sottomenu-ripasso').addEventListener('click', chiudiSottomenuRipasso);

  document.querySelectorAll('input[name="livello"]').forEach(function (r) {
    r.addEventListener('change', function () {
      if (LIVELLI.indexOf(r.value) === -1) return;
      progresso.livello = r.value;
      salva();
      aggiornaHome();
    });
  });

  document.getElementById('azzera').addEventListener('click', function () {
    let conferma = false;
    try {
      conferma = window.confirm('Vuoi azzerare tutti i progressi salvati in questo browser?');
    } catch (e) {
      conferma = false;
    }
    if (!conferma) return;
    const livello = progresso.livello;
    progresso = nuovoProgresso();
    progresso.livello = livello;
    salva();
    aggiornaHome();
  });

  // all'avvio: se il salvataggio non funziona, lo si dice una volta sola
  avvisoSalvataggio.hidden = (storage !== null) && salvaProgresso(storage, progresso);
  aggiornaHome();

  function apriSottomenuRipasso() {
    document.getElementById('sottomenu-ripasso').hidden = false;
    document.getElementById('gioca-ripasso').setAttribute('aria-expanded', 'true');
    // [agente T22] mette il focus sulla prima voce abilitata
    const prima = ['ripasso-articoli', 'ripasso-frasi', 'ripasso-errori']
      .map(function (id) { return document.getElementById(id); })
      .find(function (b) { return b && !b.disabled; });
    if (prima) prima.focus();
  }

  function chiudiSottomenuRipasso() {
    document.getElementById('sottomenu-ripasso').hidden = true;
    document.getElementById('gioca-ripasso').removeAttribute('aria-expanded');
    document.getElementById('gioca-ripasso').focus();
  }
}
