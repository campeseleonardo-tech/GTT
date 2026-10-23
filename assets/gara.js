/* Gara bus contro auto: un bus e un'auto partono insieme da un punto e corrono verso Piazza Castello.
   La durata e' proporzionale ai minuti veri (1 minuto vero = 0,15 secondi). L'auto ha una forbice: due auto, una col fattore
   di punta dei sensori (veloce) e una col fattore di Google (lenta, chiara). Nessun numero e' scritto qui: tutto arriva dai dati.

   Un luogo puo' avere anche «ore»: [{ora: "8:00", bus, auto_min, auto_max, giudizio}, ...]: la gara le corre una dopo l'altra (l'ora e' scritta sopra la corsa
   e nella frase per il lettore di schermo); con «mini» e con «riduci movimento» si vede solo la prima.

   Uso (scheda dei risultati e pannello della mappa, stesso componente):
     contenitore.innerHTML = Gara.html({luoghi: [{nome, gruppo, bus, auto_min, auto_max, giudizio}], scelto: 0, compatto: false});
   Il disegno parte da solo quando il contenitore compare nella pagina (MutationObserver), quindi basta inserire l'html.
   Con «riduci movimento» al posto della corsa ci sono barre ferme con i minuti. */
(function(){
  "use strict";
  var SEC_PER_MIN = 0.15, VIA = 8, FINE = 396, LARG_VEICOLO = 40;
  var ridotto = !!(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches);
  var contatore = 0;

  var TESTI = {
    it: {punto: "Punto", centro: "Piazza Castello", bus: "Bus", auto: "Auto", autoLenta: "Auto, ora di punta lenta", autoVeloce: "Auto, ora di punta veloce", autoLentaOra: "Auto, traffico pesante", autoVeloceOra: "Auto, traffico scorrevole",
         min: "min", riparti: "Riparti", scegli: "Punto di partenza", prioritari: "Punti prioritari", interscambi: "Interscambi esistenti",
         da: "Da", parlato: function(l){ return "Da " + l.nome + " a " + (l.arrivo || "Piazza Castello") + (l.ora ? " alle " + l.ora : "") + ": bus " + n(l.bus) + " minuti; auto " + (forbice(l) ? "da " + n(l.auto_min) + " a " + n(l.auto_max) : n(l.auto_min)) + " minuti, parcheggio compreso." + (l.giudizio ? " " + l.giudizio + "." : ""); }},
    en: {punto: "Start", centro: "Piazza Castello", bus: "Bus", auto: "Car", autoLenta: "Car, slow rush hour", autoVeloce: "Car, fast rush hour", autoLentaOra: "Car, heavy traffic", autoVeloceOra: "Car, light traffic",
         min: "min", riparti: "Replay", scegli: "Starting point", prioritari: "Priority points", interscambi: "Existing park-and-ride",
         da: "From", parlato: function(l){ return "From " + l.nome + " to " + (l.arrivo || "Piazza Castello") + (l.ora ? " at " + l.ora : "") + ": bus " + n(l.bus) + " minutes; car " + (forbice(l) ? n(l.auto_min) + " to " + n(l.auto_max) : n(l.auto_min)) + " minutes, parking included."; }}
  };
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

  function disegna(el, dati, i, fine, k){
    var l0 = dati.luoghi[i], k0 = k || 0, ore = (!dati.mini && !ridotto && l0.ore && l0.ore.length > 1) ? l0.ore : null;
    var l = l0;
    if(l0.ore && l0.ore.length){   // un'ora alla volta: i campi dell'ora coprono quelli del luogo
      l = {}; Object.keys(l0).forEach(function(q){ l[q] = l0[q]; });
      var o = l0.ore[Math.min(k0, l0.ore.length - 1)]; Object.keys(o).forEach(function(q){ l[q] = o[q]; });
    }
    var t = T(), cs = corsie(l), H = 20 + cs.length * 36;
    var maxMin = Math.max.apply(null, cs.map(function(c){ return c.min; }));
    var righe = cs.map(function(c, j){
      var y = 22 + j * 36;
      var base = '<text x="' + VIA + '" y="' + (y - 5) + '">' + esc(c.nome) + '</text><line class="gara-strada" x1="' + VIA + '" x2="' + FINE + '" y1="' + (y + 23) + '" y2="' + (y + 23) + '"/>';
      if(ridotto){
        var w = Math.max(6, c.min / maxMin * (FINE - VIA));
        return base + '<rect class="barra-ferma' + (c.k.indexOf("auto") === 0 ? " auto" : "") + '" x="' + VIA + '" y="' + (y + 3) + '" width="' + w.toFixed(1) + '" height="16" rx="3"' + (c.k.indexOf("chiara") > 0 ? ' opacity=".5"' : "") + '/>'
          + '<text class="gara-min" style="opacity:1" x="' + (FINE + 8) + '" y="' + (y + 16) + '">' + n(c.min) + ' ' + t.min + '</text>';
      }
      return base + '<g class="gv ' + c.k + '" data-min="' + c.min + '" transform="translate(' + VIA + ' ' + (y + 1) + ')">' + c.forma + '</g>'
        + '<text class="gara-min" x="' + (FINE + 8) + '" y="' + (y + 16) + '">' + n(c.min) + ' ' + t.min + '</text>';
    }).join("");
    var svg = '<svg viewBox="0 0 480 ' + H + '" role="img" aria-label="' + esc(t.parlato(l)) + '">'
      + '<line class="gara-arrivo" x1="' + (FINE + 2) + '" x2="' + (FINE + 2) + '" y1="8" y2="' + (H - 6) + '"/>'
      + '<text x="' + (FINE + 2) + '" y="' + 8 + '" text-anchor="end" dx="-4" style="font-size:12px">' + esc(l.arrivo || t.centro) + '</text>'
      + '<text x="' + VIA + '" y="8" class="gara-da">' + esc(t.da + " " + l.nome + (l.ora && l0.ore.length > 1 ? " · " + l.ora : "")) + '</text>' + righe + '</svg>';
    el.querySelector(".gara-svg").innerHTML = svg;
    el.querySelector(".gara-testo").textContent = t.parlato(l);
    // ore: finita la corsa di un'ora, dopo una pausa parte quella dell'ora dopo; l'ultima chiama fine
    var dopo = fine;
    if(ore && k0 + 1 < ore.length) dopo = function(){
      var mio = el._corsa;
      setTimeout(function(){ if(el._corsa === mio && document.body.contains(el)) disegna(el, dati, i, fine, k0 + 1); }, 1100);
    };
    if(!ridotto) corri(el, dopo); else if(fine) fine();
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

  function html(dati){
    var base = (dati.luoghi || []).filter(function(l){ return typeof l.bus === "number" && typeof l.auto_min === "number"; });
    if(!base.length) return "";
    var d = {luoghi: base, scelto: Math.min(dati.scelto || 0, base.length - 1), compatto: !!dati.compatto, mini: !!dati.mini, giro: !!dati.giro && base.length > 1};
    return '<div class="gara' + (d.compatto ? " gara-compatto" : "") + (d.mini ? " gara-mini" : "") + '" data-gara="' + esc(JSON.stringify(d)) + '"></div>';
  }

  function avvia(el){
    if(el._pronto) return; el._pronto = true;
    var dati; try { dati = JSON.parse(el.getAttribute("data-gara")); } catch(e){ return; }
    stile();
    var t = T(), uid = "gara" + (++contatore), sel = "";
    if(!dati.compatto && dati.luoghi.length > 1){
      var gruppi = [];
      dati.luoghi.forEach(function(l, i){ var g = l.gruppo || ""; var o = gruppi.filter(function(x){ return x.g === g; })[0]; if(!o){ o = {g: g, voci: []}; gruppi.push(o); } o.voci.push([i, l.nome]); });
      sel = '<label for="' + uid + '" class="visually-hidden" style="position:absolute;left:-9999px">' + esc(t.scegli) + '</label><select id="' + uid + '">'
        + gruppi.map(function(o){ var op = o.voci.map(function(v){ return '<option value="' + v[0] + '"' + (v[0] === dati.scelto ? " selected" : "") + '>' + esc(v[1]) + '</option>'; }).join("");
            return o.g ? '<optgroup label="' + esc(o.g) + '">' + op + '</optgroup>' : op; }).join("") + '</select>';
    }
    el.innerHTML = '<div class="gara-svg"></div><p class="gara-testo" aria-live="polite"></p>'
      + (dati.mini ? "" : '<div class="gara-comandi">' + sel + '<button type="button">' + esc(t.riparti) + '</button></div>');
    var corrente = dati.scelto, s = el.querySelector("select"), giro = dati.giro && !ridotto, visibile = true;
    // giro: finita una corsa, dopo una pausa parte quella del luogo dopo (solo mentre la gara si vede); scegliere un luogo ferma il giro
    function prossima(){
      if(!giro) return;
      setTimeout(function(){
        if(!giro || !document.body.contains(el)) return;
        if(!visibile){ el._attesa = true; return; }
        corrente = (corrente + 1) % dati.luoghi.length;
        if(s) s.value = String(corrente);
        disegna(el, dati, corrente, prossima);
      }, 2200);
    }
    if("IntersectionObserver" in window) new IntersectionObserver(function(v){
      visibile = v[0].isIntersecting;
      if(visibile && el._attesa){ el._attesa = false; prossima(); }
    }).observe(el);
    disegna(el, dati, corrente, prossima);
    if(s) s.addEventListener("change", function(){ giro = false; corrente = parseInt(s.value, 10); disegna(el, dati, corrente); });
    var bt = el.querySelector("button");
    if(bt) bt.addEventListener("click", function(){ disegna(el, dati, corrente, giro ? prossima : null); });
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
