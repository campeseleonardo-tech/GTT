/* La storia del progetto in sei tappe: testo a sinistra, disegno a destra che cambia a ogni paragrafo (su telefono il disegno sta sopra il testo).
   Lo stesso codice serve progetto.html e la parte «Il progetto» in fondo alla home: Progetto.monta(elemento) scrive i testi (italiano e inglese,
   con data-en) e i disegni nell'elemento e li fa seguire lo scorrimento. Tutti i numeri vengono da data/progetto.js e dalle schede
   (data/schede_risultati.js): qui non c'e' scritto nessun numero. Con «riduci movimento» i disegni sono fermi. Gli stili stanno in assets/progetto.css. */
(function(){
  "use strict";
  var MARKUP = `
  <div class="colfig"><div class="sticky" aria-hidden="true">
    <figure class="fig attiva" id="f1"><svg viewBox="0 0 400 300" preserveAspectRatio="xMidYMid meet"></svg><figcaption data-en="2020: an idea on paper. Today: data that arrive every minute.">2020: un'idea sulla carta. Oggi: dati che arrivano ogni minuto.</figcaption></figure>
    <figure class="fig" id="f2"><svg viewBox="0 0 400 420" preserveAspectRatio="xMidYMid meet"></svg><figcaption data-en="From the sensors to the pages you are reading.">Dai sensori alle pagine che stai leggendo.</figcaption></figure>
    <figure class="fig" id="f3"><svg viewBox="0 0 1000 963" preserveAspectRatio="xMidYMid meet"></svg><figcaption data-en="In red: the zones where high fragility and few services go together.">In rosso: le zone dove fragilità alta e pochi servizi coincidono.</figcaption></figure>
    <figure class="fig" id="f4"><svg viewBox="0 0 400 300" preserveAspectRatio="xMidYMid meet"></svg><figcaption data-en="Morning trips: public transport compared with the car (the car is 1).">Spostamenti del mattino: mezzi pubblici contro auto (l'auto è 1).</figcaption></figure>
    <figure class="fig" id="f5"><svg viewBox="0 0 400 300" preserveAspectRatio="xMidYMid meet"></svg><figcaption data-en="Share of bus and tram arrivals more than 5 minutes late, by source.">Quota di passaggi di bus e tram con oltre 5 minuti di ritardo, per fonte.</figcaption></figure>
    <figure class="fig" id="f6"><svg viewBox="0 0 400 300" preserveAspectRatio="xMidYMid meet"></svg><figcaption data-en="The levels of the Internet of Things: the last one is still missing.">I livelli dell'Internet delle cose: l'ultimo manca ancora.</figcaption></figure>
  </div></div>

  <div class="testi">
    <section data-fig="f1" id="promessa" aria-labelledby="h1p">
      <p class="num-parte" data-en="1 · The promise">1 · La promessa</p>
      <h2 id="h1p" data-en="In 2020 it was only a promise">Nel 2020 era solo una promessa</h2>
      <p data-en="In my bachelor's thesis I wrote that sensors and data would change our cities. It was reading and theory: no data, no proof.">Nella mia tesi triennale scrivevo che sensori e dati avrebbero cambiato le città. Era letteratura: nessun dato, nessuna prova.</p>
      <p data-en="Six years later I wanted to put it to the test. What do the real data of Turin say?">Sei anni dopo ho voluto metterla alla prova. Cosa dicono davvero i dati di Torino?</p>
    </section>

    <section data-fig="f2" id="sistema" aria-labelledby="h2p">
      <p class="num-parte" data-en="2 · The system">2 · Il sistema</p>
      <h2 id="h2p" data-en="A Raspberry Pi that reads Turin every minute">Un Raspberry Pi che legge Torino ogni minuto</h2>
      <p data-en="For <b><span data-n='sistema.giorni'></span></b> days a small computer at home has been collecting the position of buses and trams and the counts of <b><span data-n='sistema.sensori'></span></b> traffic sensors.">Da <b><span data-n="sistema.giorni"></span></b> giorni un piccolo computer di casa raccoglie la posizione di bus e tram e i conteggi di <b><span data-n="sistema.sensori"></span></b> sensori del traffico.</p>
      <p data-en="So far: <b><span data-n='sistema.passaggi'></span></b> bus and tram stop passages measured by GPS. My scripts turn all of it into the map and the results.">Finora: <b><span data-n="sistema.passaggi"></span></b> di passaggi di bus e tram alle fermate misurati col GPS. I miei script trasformano tutto nella mappa e nei risultati.</p>
    </section>

    <section data-fig="f3" id="chi" aria-labelledby="h3p">
      <p class="num-parte" data-en="3 · Who lives where">3 · Chi abita dove</p>
      <h2 id="h3p" data-en="Where fragility and few services go together">Dove fragilità e pochi servizi coincidono</h2>
      <p data-en="About <b>1 Turin resident in <span data-n='doppio.n_su'></span></b> (<b><span data-n='doppio.residenti'></span></b> people) lives where social fragility is high and services within walking distance are few. In this situation there are <span data-n='doppio.n_zone'></span> zones: <span data-n='doppio.nomi'></span>.">Circa <b>1 torinese su <span data-n="doppio.n_su"></span></b> (<b><span data-n="doppio.residenti"></span></b> persone) vive dove la fragilità sociale è alta e i servizi a piedi sono pochi. In questa situazione ci sono <span data-n="doppio.n_zone"></span> zone: <span data-n="doppio.nomi"></span>.</p>
      <p data-en="For me this is the strongest result, and it is not about technology: as my thesis said, urban problems are social problems.">Per me è il risultato più forte, e non riguarda la tecnologia: come diceva la tesi, i problemi urbani sono sociali.</p>
      <div class="link-riga"><a class="btn" href="risultati.html#p5" data-en="Result 5">Risultato 5</a><a class="btn" href="mappa_torino.html#tema=vulnerabilita&amp;vista=doppio" data-en="See it on the map">Vedi sulla mappa</a></div>
    </section>

    <section data-fig="f4" id="muoversi" aria-labelledby="h4p">
      <p class="num-parte" data-en="4 · Getting around">4 · Muoversi</p>
      <h2 id="h4p" data-en="Public transport takes <span data-n='muoversi.volte'></span> times as long as the car">Coi mezzi pubblici ci vuole <span data-n="muoversi.volte"></span> volte il tempo dell'auto</h2>
      <p data-en="In the morning, going from one zone of the metropolitan area to another takes <b><span data-n='muoversi.volte'></span> times</b> as long by public transport as by car (median, with the car time forecast by TomTom for typical weekday traffic).">Al mattino, andare da una zona all'altra dell'area metropolitana coi mezzi pubblici richiede <b><span data-n="muoversi.volte"></span> volte</b> il tempo dell'auto (mediana, con il tempo dell'auto previsto da TomTom per il traffico tipico di un feriale).</p>
      <p data-en="Park-and-ride lots work only where the bus is fast: for the bus to match the car you must lose <b><span data-n='muoversi.pareggio'></span> minutes</b> parking downtown.">Anche i parcheggi di scambio funzionano solo dove il bus è veloce: perché il bus pareggi l'auto bisogna perdere <b><span data-n="muoversi.pareggio"></span> minuti</b> a parcheggiare in centro.</p>
      <div class="link-riga"><a class="btn" href="risultati.html#p3" data-en="Result 3">Risultato 3</a><a class="btn" href="risultati.html#p4" data-en="Result 4">Risultato 4</a></div>
    </section>

    <section data-fig="f5" id="fiducia" aria-labelledby="h5p">
      <p class="num-parte" data-en="5 · How far to trust the data">5 · Quanto ci si può fidare dei dati</p>
      <h2 id="h5p" data-en="The data exist, but they must be checked">I dati ci sono, ma vanno controllati</h2>
      <p data-en="The official delay feed reported <b><span data-n='ritardi.feed'></span>%</b> of passages more than 5 minutes late. The GPS of the vehicles says <b><span data-n='ritardi.gps'></span>%</b>: the feed understated delays by <b><span data-n='ritardi.rapporto'></span> times</b>. So I redid everything with the GPS.">Il feed ufficiale dei ritardi segnava il <b><span data-n="ritardi.feed"></span>%</b> di passaggi con oltre 5 minuti di ritardo. Il GPS dei mezzi dice il <b><span data-n="ritardi.gps"></span>%</b>: il feed sottostimava i ritardi di <b><span data-n="ritardi.rapporto"></span> volte</b>. Ho rifatto tutto col GPS.</p>
      <p data-en="Other traps: a bus whose clock is three years ahead, a feed that stopped on the morning of 18 October, a parking counter that never changes. Every result states its limits.">Altri trabocchetti: un mezzo con l'orologio tre anni avanti, un feed fermo la mattina del 18 ottobre, un contatore di parcheggio che non cambia mai. Ogni risultato dichiara i suoi limiti.</p>
    </section>

    <section data-fig="f6" id="manca" aria-labelledby="h6p">
      <p class="num-parte" data-en="6 · What is missing, and who I am">6 · Cosa manca e chi sono</p>
      <h2 id="h6p" data-en="What is missing, and who I am">Cosa manca, e chi sono</h2>
      <p data-en="Missing: how many people actually ride, what the service costs, trains and other operators. It is the «business» level of the Internet of Things, and the next step.">Mancano: quante persone salgono davvero, quanto costa il servizio, i treni e le altre aziende. È il livello «business» dell'Internet delle cose, e il prossimo passo.</p>
      <p data-en="I am Leonardo Campese. This is a personal study and portfolio project, built only on open data.">Sono Leonardo Campese. Questo è un progetto personale di studio e di portfolio, costruito solo su dati aperti.</p>
      <div class="finale-bottoni"><a class="btn primario" href="risultati.html" data-en="Go to the results">Vai ai risultati</a><a class="btn" href="mappa_torino.html" data-en="Open the map">Apri la mappa</a><a class="btn" href="https://www.linkedin.com/in/leocampese/">LinkedIn</a></div>
    </section>
  </div>
`;

  function monta(scena){
    document.documentElement.classList.add("js");
    scena.innerHTML = MARKUP;
    if(window.Sito && Sito.traduci) Sito.traduci(scena);   // testi fissi nella lingua scelta (i numeri li scrive numeri(), dopo)
    var P = window.PROGETTO, S = Array.isArray(window.SCHEDE_RISULTATI) ? window.SCHEDE_RISULTATI : [];
    var T = Sito.T, num = Sito.formattaNumero, NS = "http://www.w3.org/2000/svg";
    function svg(id){ return document.querySelector("#" + id + " svg"); }
    function el(tag, att, testo){ var e = document.createElementNS(NS, tag); for(var k in att) e.setAttribute(k, att[k]); if(testo != null) e.textContent = testo; return e; }
    function scheda(n){ return S.filter(function(s){ return s && s.numero_pubblico === n && s.forma; })[0]; }
    function forma(s){ return (Sito.lingua() === "en" && s.forma_en) ? s.forma_en : s.forma; }
    function valoreScheda(n){ var s = scheda(n); return s ? String(forma(s).numero.valore) : null; }
    function pareggioScheda(){ var s = scheda(3), f = s && forma(s); return f && f.pareggio ? String(f.pareggio.tomtom) : null; }
    function elenco(v){ return v.length < 2 ? v.join("") : v.slice(0, -1).join(", ") + T(" e ", " and ") + v[v.length - 1]; }

    /* ---- numeri del testo: tutto arriva dai dati (data/progetto.js e le schede), niente scritto a mano ---- */
    function numeri(){
      var c = P && P.contatore, d = P && P.doppio, r = P && P.ritardi;
      var milioni = c && c.passaggi >= 1e6;
      var v = {
        "sistema.giorni": c && num(Sito.giorniRaccolta(c)),
        "sistema.sensori": P && num(P.sensori_5t),
        "sistema.passaggi": c && (milioni ? num(Math.round(c.passaggi / 1e5) / 10) + T(" milioni", " million") : num(c.passaggi)),
        "doppio.residenti": d && num(d.residenti), "doppio.n_su": d && num(d.n_su),
        "doppio.n_zone": d && (T(["", "una", "due", "tre", "quattro", "cinque", "sei"][d.n_zone] || String(d.n_zone), ["", "one", "two", "three", "four", "five", "six"][d.n_zone] || String(d.n_zone))),
        "doppio.nomi": P && elenco(P.zone.filter(function(z){ return z.doppio; }).map(function(z){ return z.nome; })),
        "muoversi.volte": valoreScheda(4), "muoversi.pareggio": pareggioScheda(),
        "ritardi.feed": r && num(r.feed_pct), "ritardi.gps": r && num(r.gps_pct), "ritardi.rapporto": r && num(r.rapporto)
      };
      document.querySelectorAll("[data-n]").forEach(function(e){ var x = v[e.getAttribute("data-n")]; e.textContent = (x == null || x === "") ? "…" : x; });
    }

    /* ---- disegni ---- */
    function f1(){
      var s = svg("f1"); s.innerHTML = "";
      var cols = 9, righe = 6, x0 = 30, y0 = 70, dx = 40, dy = 36, k = 0;
      s.appendChild(el("text", {x: 30, y: 36, "class": "d-titolo"}, "2020"));
      s.appendChild(el("text", {x: 370, y: 36, "class": "d-titolo", "text-anchor": "end"}, T("oggi", "today")));
      s.appendChild(el("text", {x: 30, y: 54, "class": "d-piccolo"}, T("la promessa", "the promise")));
      s.appendChild(el("text", {x: 370, y: 54, "class": "d-piccolo", "text-anchor": "end"}, T("la verifica", "the check")));
      for(var j = 0; j < righe; j++) for(var i = 0; i < cols; i++){
        var vera = i >= 5 || (i === 4 && j % 2 === 0), c = el("circle", {cx: x0 + i * dx, cy: y0 + j * dy, r: vera ? 7 : 6, "class": vera ? "d-acceso a-accendi" : "d-spento"});
        if(vera) c.style.animationDelay = (0.05 * ((i - 4) * righe + j) + 0.15) + "s";
        s.appendChild(c); k++;
      }
      s.appendChild(el("text", {x: 30, y: 296, "class": "d-piccolo"}, T("letteratura, nessun dato", "literature, no data")));
      s.appendChild(el("text", {x: 370, y: 296, "class": "d-piccolo", "text-anchor": "end"}, T("dati veri di Torino", "real data from Turin")));
    }

    function f2(){
      var s = svg("f2"); s.innerHTML = "";
      var c = P && P.contatore;
      var passi = [
        [T("Sensori e GPS", "Sensors and GPS"), T("bus e tram, " + (P ? P.sensori_5t : "") + " sensori del traffico", "buses and trams, " + (P ? P.sensori_5t : "") + " traffic sensors")],
        [T("Raspberry Pi", "Raspberry Pi"), T("legge Torino ogni minuto", "reads Turin every minute")],
        [T("Storico", "History"), c ? T(Sito.giorniRaccolta(c) + " giorni di dati", Sito.giorniRaccolta(c) + " days of data") : ""],
        [T("Script", "Scripts"), T("calcoli, controlli, risultati", "calculations, checks, results")],
        [T("Pagine", "Pages"), T("mappa e schede dei risultati", "map and result cards")]
      ];
      passi.forEach(function(p, i){
        var y = 12 + i * 82;
        s.appendChild(el("rect", {x: 40, y: y, width: 320, height: 56, rx: 10, "class": "d-scatola" + (i === 1 ? " acc" : "")}));
        s.appendChild(el("text", {x: 58, y: y + 25, "class": "d-titolo"}, p[0]));
        s.appendChild(el("text", {x: 58, y: y + 44, "class": "d-piccolo"}, p[1]));
        if(i < passi.length - 1){
          s.appendChild(el("line", {x1: 200, x2: 200, y1: y + 58, y2: y + 80, "class": "d-filo"}));
          var d = el("circle", {cx: 200, cy: y + 58, r: 5, "class": "d-punto a-scorri"}); d.style.animationDelay = (i * 0.35) + "s"; d.style.transform = "translateY(0)";
          s.appendChild(d);
        }
      });
    }

    function f3(){
      var s = svg("f3"); s.innerHTML = "";
      if(!P){ return; }
      var g = el("g", {}), i = 0;
      P.zone.forEach(function(z){ g.appendChild(el("path", {d: z.d, "class": "d-zona" + (z.doppio ? " doppio" : ""), style: z.doppio ? "transition-delay:" + (0.25 + 0.2 * (i++)) + "s" : ""})); });
      s.appendChild(g);
      s.appendChild(el("path", {d: P.contorno.d, "class": "d-contorno"}));
      var etic = el("g", {}); s.appendChild(etic);
      // etichette al centro del riquadro di ogni zona in doppio svantaggio (calcolate dopo che le forme sono in pagina)
      requestAnimationFrame(function(){
        var paths = g.querySelectorAll(".doppio"), k = 0, messe = [];
        P.zone.forEach(function(z){
          if(!z.doppio) return;
          var b = paths[k++].getBBox(), x = b.x + b.width / 2, y = b.y + b.height / 2;
          messe.forEach(function(m){ if(Math.abs(m.y - y) < 30 && Math.abs(m.x - x) < 190) y = m.y + 32; });   // etichette che si sovrappongono: la seconda scende
          messe.push({x: x, y: y});
          etic.appendChild(el("text", {x: x, y: y, "text-anchor": "middle", "class": "d-etichetta"}, z.nome));
        });
      });
    }

    function f4(){
      var s = svg("f4"); s.innerHTML = "";
      var v = valoreScheda(4), m = v && /^(\d+(?:[.,]\d+)?)$/.exec(v);
      if(!m){ s.appendChild(el("text", {x: 200, y: 150, "text-anchor": "middle", "class": "d-testo"}, v || "")); return; }
      var x = parseFloat(m[1].replace(",", ".")), W = 300, u = W / Math.max(x, 1) * 0.92;
      s.appendChild(el("text", {x: 30, y: 36, "class": "d-titolo"}, T("In auto", "By car")));
      s.appendChild(el("rect", {x: 30, y: 46, width: u, height: 30, rx: 5, "class": "d-oro a-cresci d-barra"}));
      s.appendChild(el("text", {x: 30 + u + 8, y: 67, "class": "d-grande"}, "1"));
      s.appendChild(el("text", {x: 30, y: 134, "class": "d-titolo"}, T("Coi mezzi pubblici", "By public transport")));
      s.appendChild(el("rect", {x: 30, y: 144, width: u * x, height: 30, rx: 5, "class": "d-blu a-cresci d-barra"}));
      s.appendChild(el("text", {x: 30, y: 214, "class": "d-grande"}, v + " " + T("volte", "times")));
      s.appendChild(el("text", {x: 30, y: 236, "class": "d-piccolo"}, T("il tempo dell'auto (previsto da TomTom, mediana)", "the car's time (forecast by TomTom, median)")));
      var q = pareggioScheda();
      if(q){ s.appendChild(el("text", {x: 30, y: 274, "class": "d-testo"}, T("Il bus pareggia l'auto se in centro si perdono ", "The bus matches the car if you lose ") + q + T(" minuti", " minutes downtown"))); }
    }

    function f5(){
      var s = svg("f5"); s.innerHTML = "";
      var r = P && P.ritardi; if(!r) return;
      var max = Math.max(r.gps_pct, r.feed_pct) * 1.15, H = 150, base = 200, w = 70;
      [[r.feed_pct, 90, T("Feed ufficiale", "Official feed"), "d-oro"], [r.gps_pct, 240, T("GPS dei mezzi", "Vehicle GPS"), "d-blu"]].forEach(function(b){
        var h = b[0] / max * H, bar = el("rect", {x: b[1], y: base - h, width: w, height: h, rx: 5, "class": b[3]});
        bar.setAttribute("class", b[3] + " a-su");
        s.appendChild(bar);
        s.appendChild(el("text", {x: b[1] + w / 2, y: base - h - 8, "text-anchor": "middle", "class": "d-grande"}, num(b[0]) + "%"));
        s.appendChild(el("text", {x: b[1] + w / 2, y: base + 20, "text-anchor": "middle", "class": "d-testo"}, b[2]));
      });
      s.appendChild(el("line", {x1: 30, x2: 370, y1: base, y2: base, stroke: "var(--line)", "stroke-width": 1.5}));
      s.appendChild(el("text", {x: 200, y: 30, "text-anchor": "middle", "class": "d-titolo"}, T("Oltre 5 minuti di ritardo", "More than 5 minutes late")));
      s.appendChild(el("text", {x: 200, y: 274, "text-anchor": "middle", "class": "d-piccolo"}, T("sottostimato di ", "understated by ") + num(r.rapporto) + T(" volte", " times")));
    }

    function f6(){
      var s = svg("f6"); s.innerHTML = "";
      var liv = [[T("Percezione", "Perception"), T("GPS dei bus, sensori 5T", "bus GPS, 5T sensors"), 1], [T("Rete", "Network"), T("feed aperti, letti ogni minuto", "open feeds, read every minute"), 1],
                 [T("Middleware", "Middleware"), "Raspberry Pi, SQLite", 1], [T("Applicazione", "Application"), T("mappa e schede", "map and cards"), 1],
                 [T("Business", "Business"), T("manca: costi, passeggeri, valore", "missing: costs, riders, value"), 0]];
      liv.forEach(function(l, i){
        var y = 14 + i * 56, w = 230 + (i * 30);
        var r = el("rect", {x: 30, y: y, width: Math.min(340, w), height: 44, rx: 8, "class": "d-livello " + (l[2] ? "fatto" : "manca") + (l[2] ? " a-cresci" : " a-batti")});
        if(l[2]) r.style.animationDelay = (i * 0.15) + "s";
        s.appendChild(r);
        s.appendChild(el("text", {x: 44, y: y + 19, "class": "d-testo", "font-weight": 700}, l[0]));
        s.appendChild(el("text", {x: 44, y: y + 36, "class": "d-piccolo"}, l[1]));
      });
    }

    function tutto(){ numeri(); f1(); f2(); f3(); f4(); f5(); f6(); }
    tutto();
    window.addEventListener("lingua", function(){ if(document.body.contains(scena)) tutto(); });

    /* ---- il disegno cambia con il paragrafo che sta al centro dello schermo ---- */
    var figure = scena.querySelectorAll(".fig"), sezioni = scena.querySelectorAll(".testi section");
    function mostra(id){ figure.forEach(function(f){ f.classList.toggle("attiva", f.id === id); }); }
    if("IntersectionObserver" in window){
      var io = new IntersectionObserver(function(voci){
        voci.forEach(function(v){ if(v.isIntersecting) mostra(v.target.getAttribute("data-fig")); });
      }, {rootMargin: "-42% 0px -48% 0px"});
      sezioni.forEach(function(s){ io.observe(s); });
    } else figure.forEach(function(f){ f.classList.add("attiva"); });
  }

  window.Progetto = {monta: monta};
})();
