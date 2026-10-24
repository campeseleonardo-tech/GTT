/* Gara bus contro auto: un bus e un'auto partono insieme da un luogo e corrono verso l'arrivo (di solito Piazza Castello).
   La durata e' proporzionale ai minuti veri (1 minuto vero = 0,15 secondi). Nessun numero e' scritto qui: tutto arriva dai dati.

   Due modi, stesso componente:
   - «giro» (schede dei risultati): nessun comando. Le corse vanno da sole una dopo l'altra, col nome del luogo sopra (nome lungo: «...», nome intero nel title),
     un'auto sola (auto_min: TomTom, parcheggio compreso); all'arrivo i minuti e il distacco. Con «riduci movimento» tutte le corse ferme, una sotto l'altra.
   - normale (pannello della mappa, compatto): una corsa, con la forbice fra due auto (auto_min e auto_max) e il pulsante «Riparti».

   Uso:
     contenitore.innerHTML = Gara.html({luoghi: [{nome, gruppo, arrivo, bus, auto_min, auto_max, giudizio}], giro: true});
   Il disegno parte da solo quando il contenitore compare nella pagina (MutationObserver), quindi basta inserire l'html. */
(function(){
  "use strict";
  var SEC_PER_MIN = 0.15, VIA = 8, FINE = 396, LARG_VEICOLO = 40;
  var ridotto = !!(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches);
  var contatore = 0;

  var TESTI = {
    it: {punto: "Punto", centro: "Piazza Castello", bus: "Bus", auto: "Auto, stima TomTom", autoLenta: "Auto, stima TomTom", autoVeloce: "Auto, stima sensori", autoLentaOra: "Auto, stima TomTom", autoVeloceOra: "Auto, stima sensori",
         min: "min", riparti: "Riparti", scegli: "Punto di partenza", prioritari: "Punti prioritari", interscambi: "Interscambi esistenti",
         da: "Da", autoSola: "Auto", parlato: function(l){ return "Da " + l.nome + " a " + (l.arrivo || "Piazza Castello") + (l.ora ? " alle " + l.ora : "") + ": bus " + n(l.bus) + " minuti; auto " + (forbice(l) ? n(l.auto_min) + " o " + n(l.auto_max) + " (due stime)" : n(l.auto_min) + " (stima TomTom)") + " minuti, parcheggio compreso." + (l.giudizio ? " " + l.giudizio + "." : ""); }},
    en: {punto: "Start", centro: "Piazza Castello", bus: "Bus", auto: "Car, TomTom estimate", autoLenta: "Car, TomTom estimate", autoVeloce: "Car, sensor estimate", autoLentaOra: "Car, TomTom estimate", autoVeloceOra: "Car, sensor estimate",
         min: "min", riparti: "Replay", scegli: "Starting point", prioritari: "Priority points", interscambi: "Existing park-and-ride",
         da: "From", autoSola: "Car", parlato: function(l){ return "From " + l.nome + " to " + (l.arrivo || "Piazza Castello") + (l.ora ? " at " + l.ora : "") + ": bus " + n(l.bus) + " minutes; car " + (forbice(l) ? n(l.auto_min) + " or " + n(l.auto_max) + " (two estimates)" : n(l.auto_min) + " (TomTom estimate)") + " minutes, parking included."; }}
  };
  TESTI.it.parlatoGiro = function(l){ return "Da " + l.nome + " a " + (l.arrivo || "Piazza Castello") + ": bus " + n(l.bus) + " minuti, auto " + n(l.auto_min) + " minuti, parcheggio compreso." + (l.giudizio ? " " + l.giudizio + "." : ""); };
  TESTI.en.parlatoGiro = function(l){ return "From " + l.nome + " to " + (l.arrivo || "Piazza Castello") + ": bus " + n(l.bus) + " minutes, car " + n(l.auto_min) + " minutes, parking included." + (l.giudizio ? " " + l.giudizio + "." : ""); };
  function lingua(){ return (document.documentElement.lang || "it").slice(0, 2) === "en" ? "en" : "it"; }
  function T(){ return TESTI[lingua()]; }
  function n(v){ return window.Sito && Sito.formattaNumero ? Sito.formattaNumero(Math.round(v)) : String(Math.round(v)); }
  function forbice(l){ return Math.round(l.auto_max) - Math.round(l.auto_min) >= 1; }
  function esc(s){ return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }

  /* icone semplici, 40 x 20, origine in alto a sinistra; il davanti e' a destra */
  var BUS = '<rect x="0" y="1" width="40" height="15" rx="3.5"/><rect x="4" y="4" width="7" height="5" rx="1" class="gv-vetro"/><rect x="13" y="4" width="7" height="5" rx="1" class="gv-vetro"/>'
          + '<rect x="22" y="4" width="7" height="5" rx="1" class="gv-vetro"/><rect x="31" y="4" width="6" height="8" rx="1" class="gv-vetro"/><circle cx="9" cy="17" r="3"/><circle cx="31" cy="17" r="3"/>';
  var AUTO = '<path d="M1 14V10.5c0-1.6 1-2.7 2.600-3L11 5.500c1.500-2.600 3.200-4 5.500-4h6c2.500 0 4.300 1.400 5.800 3.800L35 7.500c2.600.5 4 1.800 4 4V14z"/>'
           + '<path d="M13 6.500c1-1.800 2-2.700 3.600-2.700H21V7.500H12z" class="gv-vetro"/><path d="M23.500 3.800h1.400c1.300 0 2.300.8 3.200 2.200l.6 1.500h-5.200z" class="gv-vetro"/><circle cx="10" cy="15" r="3.200"/><circle cx="30" cy="15" r="3.200"/>';

  function stile(){
    if(document.getElementById("gara-stile")) return;
    var s = document.createElement("style"); s.id = "gara-stile";
    s.textContent = ".gara{margin:8px 0}.gara svg{display:block;width:100%;height:auto}"
      + ".gara .gara-testo{font-size:14px;margin:6px 0 0}.gara .gara-comandi{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:6px}"
      + ".gara select{font:inherit;font-size:14px;max-width:100%;padding:5px 8px;border:1px solid var(--line,#c9d1e3);border-radius:8px;background:var(--card,#fff);color:var(--ink,#1b2433)}"
      + ".gara button{font:inherit;font-size:14px;font-weight:600;padding:5px 14px;border:1px solid var(--line,#c9d1e3);border-radius:8px;background:var(--card,#fff);color:var(--ink,#1b2433);cursor:pointer}"
      + ".gara button:focus-visible,.gara select:focus-visible{outline:3px solid var(--oro,#e3bf55);outline-offset:2px}"
      + ".gara .gv{fill:var(--neu-blu,#6f8fc7)}.gara .gv.auto{fill:var(--neu-arancio,#c9a227)}.gara .gv.chiara{opacity:.5}.gara .gv-vetro{fill:var(--card,#fff);opacity:.85}"
      + ".gara .gara-strada{stroke:var(--line,#c9d1e3);stroke-width:1.5;stroke-dasharray:5 5}.gara .gara-arrivo{stroke:var(--vr-rosso,#a61e33);stroke-width:2}"
      + ".gara text{font-family:inherit;fill:var(--muted,#5b6578);font-size:13px}.gara text.gara-da{fill:var(--ink,#1b2433);font-weight:700;font-size:14px}"
      + ".gara-mini .gara-comandi,.gara-mini .gara-testo{display:none}"
      + ".gara text.gara-min{fill:var(--ink,#1b2433);font-size:15px;font-weight:700;opacity:0}"
      + ".gara .gara-compatto select{max-width:100%}.gara .barra-ferma{fill:var(--neu-blu,#6f8fc7)}.gara .barra-ferma.auto{fill:var(--neu-arancio,#c9a227)}";
    document.head.appendChild(s);
  }

  /* i veicoli da disegnare: bus, auto veloce, (auto lenta se la forbice c'e'); minuti per ognuno */
  function corsie(l){
    var t = T(), v = [{k: "bus", nome: t.bus, min: l.bus, forma: BUS}];
    if(forbice(l)){
      v.push({k: "auto", nome: l.ora ? t.autoVeloceOra : t.autoVeloce, min: l.auto_min, forma: AUTO});
      v.push({k: "auto chiara", nome: l.ora ? t.autoLentaOra : t.autoLenta, min: l.auto_max, forma: AUTO});
    } else v.push({k: "auto", nome: t.auto, min: l.auto_min, forma: AUTO});
    return v;
  }

  function disegna(el, dati, i) {
    var l = dati.luoghi[i];
    var t = T(), cs = corsie(l), H = 20 + cs.length * 36;
    var maxMin = Math.max.apply(null, cs.map(function(c){ return c.min; })), minMin = Math.min.apply(null, cs.map(function(c){ return c.min; }));
    var distacco = Math.round(maxMin) - Math.round(minMin);      // scritto all'arrivo, accanto al mezzo piu' lento
    var righe = cs.map(function(c, j){
      var y = 22 + j * 36;
      var scia = distacco >= 1 && c.min === maxMin ? '<tspan class="gara-distacco" x="' + (FINE + 8) + '" dy="15" style="font-size:13px;font-weight:700">+' + n(distacco) + ' ' + t.min + '</tspan>' : "";
      var base = '<text x="' + VIA + '" y="' + (y - 5) + '">' + esc(c.nome) + '</text><line class="gara-strada" x1="' + VIA + '" x2="' + FINE + '" y1="' + (y + 23) + '" y2="' + (y + 23) + '"/>';
      if(ridotto){
        var w = Math.max(6, c.min / maxMin * (FINE - VIA));
        return base + '<rect class="barra-ferma' + (c.k.indexOf("auto") === 0 ? " auto" : "") + '" x="' + VIA + '" y="' + (y + 3) + '" width="' + w.toFixed(1) + '" height="16" rx="3"' + (c.k.indexOf("chiara") > 0 ? ' opacity=".5"' : "") + '/>'
          + '<text class="gara-min" style="opacity:1" x="' + (FINE + 8) + '" y="' + (y + 16) + '">' + n(c.min) + ' ' + t.min + scia + '</text>';
      }
      return base + '<g class="gv ' + c.k + '" data-min="' + c.min + '" transform="translate(' + VIA + ' ' + (y + 1) + ')">' + c.forma + '</g>'
        + '<text class="gara-min" x="' + (FINE + 8) + '" y="' + (y + 16) + '">' + n(c.min) + ' ' + t.min + scia + '</text>';
    }).join("");
    // le due scritte in alto (partenza a sinistra, arrivo a destra) non devono toccarsi: stima 0,6 x corpo x caratteri
    var testoDa = t.da + " " + l.nome, arrivoTesto = l.arrivo || t.centro;
    var stimaDa = VIA + testoDa.length * .6 * 14, stimaArrivo = arrivoTesto.length * .6 * 12;
    var svg = '<svg viewBox="0 0 480 ' + H + '" role="img" aria-label="' + esc(t.parlato(l)) + '">'
      + '<line class="gara-arrivo" x1="' + (FINE + 2) + '" x2="' + (FINE + 2) + '" y1="8" y2="' + (H - 6) + '"/>'
      + '<text x="' + (FINE + 2) + '" y="' + 8 + '" text-anchor="end" dx="-4" style="font-size:12px">' + esc(l.arrivo || t.centro) + '</text>'
      + '<text x="' + VIA + '" y="8" class="gara-da"' + (stimaDa > FINE - 14 - stimaArrivo - 12 ? ' style="font-size:12px"' : '') + '>' + esc(testoDa) + '</text>' + righe + '</svg>';
    el.querySelector(".gara-svg").innerHTML = svg;
    el.querySelector(".gara-testo").textContent = t.parlato(l);
    if(!ridotto) corri(el, null);
  }

  function corri(el, fine){
    var carri = Array.prototype.slice.call(el.querySelectorAll(".gara-svg g.gv"));
    var etich = Array.prototype.slice.call(el.querySelectorAll(".gara-svg text.gara-min"));
    var id = ++contatore; el._corsa = id;
    var t0 = null;
    function y(g){ return g.getAttribute("transform").split(" ")[1].replace(")", ""); }
    function passo(ts){
      if(el._corsa !== id || !document.body.contains(el)) return;
      if(t0 === null) t0 = ts + 300;   // piccola pausa prima del via
      var sec = Math.max(0, (ts - t0) / 1000), finito = true;
      carri.forEach(function(g, j){
        var dur = parseFloat(g.getAttribute("data-min")) * SEC_PER_MIN, f = Math.min(1, sec / dur);
        g.setAttribute("transform", "translate(" + (VIA + f * (FINE - VIA - LARG_VEICOLO)).toFixed(1) + " " + y(g) + ")");
        etich[j].style.opacity = f >= 1 ? 1 : 0;
        if(f < 1) finito = false;
      });
      if(!finito) requestAnimationFrame(passo); else if(fine) fine();
    }
    requestAnimationFrame(passo);
  }

  /* ---------------- modo «giro» (schede): senza comandi, una corsa dopo l'altra ---------------- */
  var GA = {x0: VIA, fine: FINE, passo: 50, alto: 40};
  function taglia(testo, maxCar){ return testo.length > maxCar ? testo.slice(0, Math.max(1, maxCar - 1)).trim() + "…" : testo; }
  /* il disegno di un luogo: nome sopra (e arrivo a destra), due corsie (bus, auto) con il distacco all'arrivo, frase di esito sotto.
     statico = true (riduci movimento): i mezzi sono gia' all'arrivo e i minuti scritti */
  function svgGiro(l, statico){
    var t = T(), arrivo = l.arrivo || t.centro;
    var maxArrivo = 22, arrivoT = taglia(arrivo, maxArrivo);
    var spazio = Math.floor((FINE - VIA - arrivoT.length * 7.2 - 18) / 9.6);    // caratteri del nome a 17 px (circa 9,6 px l'uno)
    var nomeT = taglia(l.nome, Math.max(8, spazio));
    var cs = [{k: "bus", nome: t.bus, min: l.bus, forma: BUS}, {k: "auto", nome: t.autoSola, min: l.auto_min, forma: AUTO}];
    var maxMin = Math.max(cs[0].min, cs[1].min), distacco = Math.round(maxMin) - Math.round(Math.min(cs[0].min, cs[1].min));
    var H = 44 + cs.length * GA.passo + (l.giudizio ? 26 : 8);
    var righe = cs.map(function(c, j){
      var y = 50 + j * GA.passo;
      var scia = distacco >= 1 && c.min === maxMin ? '<tspan class="gara-distacco" x="' + (FINE + 8) + '" dy="16" style="font-size:13px;font-weight:700">+' + n(distacco) + ' ' + t.min + '</tspan>' : "";
      var base = '<text x="' + VIA + '" y="' + (y - 4) + '">' + esc(c.nome) + '</text><line class="gara-strada" x1="' + VIA + '" x2="' + FINE + '" y1="' + (y + 28) + '" y2="' + (y + 28) + '"/>';
      var tx = '<text class="gara-min" x="' + (FINE + 8) + '" y="' + (y + 18) + '"' + (statico ? ' style="opacity:1"' : "") + '>' + n(c.min) + ' ' + t.min + scia + '</text>';
      if(statico){
        var w = Math.max(6, c.min / maxMin * (FINE - VIA));
        return base + '<rect class="barra-ferma' + (c.k === "auto" ? " auto" : "") + '" x="' + VIA + '" y="' + (y + 4) + '" width="' + w.toFixed(1) + '" height="18" rx="3"/>' + tx;
      }
      return base + '<g class="gv ' + c.k + '" data-min="' + c.min + '" transform="translate(' + VIA + ' ' + (y + 2) + ')">' + c.forma + '</g>' + tx;
    }).join("");
    var esito = l.giudizio ? '<text class="gara-esito" x="' + VIA + '" y="' + (H - 8) + '" style="font-size:14px;fill:var(--ink,#1b2433);' + (statico ? "" : "opacity:0") + '">' + esc(l.giudizio.charAt(0).toUpperCase() + l.giudizio.slice(1)) + '</text>' : "";
    return '<svg viewBox="0 0 480 ' + H + '" role="img" aria-label="' + esc(t.parlatoGiro(l)) + '">'
      + '<line class="gara-arrivo" x1="' + (FINE + 2) + '" x2="' + (FINE + 2) + '" y1="28" y2="' + (H - 30) + '"/>'
      + '<text x="' + VIA + '" y="20" class="gara-da" style="font-size:17px">' + esc(nomeT) + (nomeT !== l.nome ? '<title>' + esc(l.nome) + '</title>' : "") + '</text>'
      + '<text x="' + (FINE + 2) + '" y="20" text-anchor="end" style="font-size:13px">' + esc(arrivoT) + (arrivoT !== arrivo ? '<title>' + esc(arrivo) + '</title>' : "") + '</text>'
      + righe + esito + '</svg>';
  }
  function avviaGiro(el, dati){
    stile();
    var luoghi = dati.luoghi;
    if(ridotto){
      el.innerHTML = luoghi.map(function(l){ return '<div class="gara-svg">' + svgGiro(l, true) + '</div>'; }).join("");
      return;
    }
    el.innerHTML = '<div class="gara-svg"></div>';
    var cont = el.querySelector(".gara-svg"), i = 0, visibile = true, attesa = false;
    function corsa(){
      cont.innerHTML = svgGiro(luoghi[i], false);
      var esito = cont.querySelector(".gara-esito");
      corri(el, function(){
        if(esito) esito.style.opacity = 1;
        setTimeout(prossima, 2200);
      });
    }
    function prossima(){
      if(!document.body.contains(el)) return;
      if(!visibile){ attesa = true; return; }
      i = (i + 1) % luoghi.length;
      corsa();
    }
    if("IntersectionObserver" in window) new IntersectionObserver(function(v){
      visibile = v[0].isIntersecting;
      if(visibile && attesa){ attesa = false; prossima(); }
    }).observe(el);
    corsa();
  }

  function html(dati){
    var base = (dati.luoghi || []).filter(function(l){ return typeof l.bus === "number" && typeof l.auto_min === "number"; });
    if(!base.length) return "";
    var d = {luoghi: base, scelto: Math.min(dati.scelto || 0, base.length - 1), compatto: !!dati.compatto, mini: !!dati.mini, giro: !!dati.giro};
    return '<div class="gara' + (d.compatto ? " gara-compatto" : "") + (d.mini ? " gara-mini" : "") + '" data-gara="' + esc(JSON.stringify(d)) + '"></div>';
  }

  function avvia(el){
    if(el._pronto) return; el._pronto = true;
    var dati; try { dati = JSON.parse(el.getAttribute("data-gara")); } catch(e){ return; }
    if(dati.giro){ avviaGiro(el, dati); return; }
    stile();
    var t = T();
    el.innerHTML = '<div class="gara-svg"></div><p class="gara-testo" aria-live="polite"></p>'
      + (dati.mini ? "" : '<div class="gara-comandi"><button type="button">' + esc(t.riparti) + '</button></div>');
    disegna(el, dati, 0);
    var bt = el.querySelector("button");
    if(bt) bt.addEventListener("click", function(){ disegna(el, dati, 0); });
  }

  function scansiona(radice){
    var els = (radice.querySelectorAll ? radice.querySelectorAll("[data-gara]") : []);
    for(var i = 0; i < els.length; i++) avvia(els[i]);
    if(radice.matches && radice.matches("[data-gara]")) avvia(radice);
  }
  function avviaTutto(){
    scansiona(document);
    new MutationObserver(function(muts){
      muts.forEach(function(m){ m.addedNodes.forEach(function(nd){ if(nd.nodeType === 1) scansiona(nd); }); });
    }).observe(document.body, {childList: true, subtree: true});
  }
  if(document.body) avviaTutto(); else document.addEventListener("DOMContentLoaded", avviaTutto);

  window.Gara = {html: html, avvia: avvia};
})();
