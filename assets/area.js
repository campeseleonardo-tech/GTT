/* Area che si espande: dove si arriva in N minuti, coi mezzi pubblici e in auto, partendo da Piazza Castello o da una zona di Torino.
   Due mappe di Torino fatte di quadratini (una per sezione di censimento): si colorano quando il tempo e' entro i minuti scelti.
   Un cursore e un ▶ fanno crescere le aree minuto per minuto fino a 60; sotto, le soglie 10, 20, 30, 45 con la quota di torinesi raggiunti.
   Nessun numero e' scritto qui: tutto arriva da data/area_tempi.js (scritto dallo script delle schede, da scripts/99_area_tempi.py).

   Uso:  contenitore.innerHTML = Area.html();     (il disegno parte da solo quando il contenitore compare nella pagina)
   Con «riduci movimento»: niente cursore ne' ▶, le 4 soglie affiancate e ferme. */
(function(){
  "use strict";
  var MAX_MIN = 60, SEC_TOTALI = 9;
  var ridotto = !!(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches);
  var contatore = 0, caricamento = null;

  var TESTI = {
    it: {partenza: "Partenza", castello: "Piazza Castello (una sezione di censimento per quadratino)", zone: "Zone di Torino (una zona per colore)",
         traffico: "Traffico in auto", scorrevole: "scorrevole (fattore ", pesante: "pesante (fattore ", minuti: "minuti", min: "min",
         mezzi: "Coi mezzi pubblici", auto: "In auto", mezziBreve: "mezzi", autoBreve: "auto", parti: "Parti", ferma: "Ferma", cursore: "Minuti di viaggio",
         soglie: "Quanti torinesi raggiungi", dentro: "entro ", ab: "dei torinesi",
         non: "senza collegamento entro 120 minuti: ", fonteCastello: "Partenza alle 7:45 di un feriale; auto di punta = tempo a flusso libero per il fattore, più 5 minuti per parcheggiare.",
         caricamentoKo: "Dati non disponibili.", puntoOrigine: "partenza",
         parlato: function(o, m, pm, pa){ return "Da " + o + ", entro " + m + " minuti: coi mezzi pubblici " + pm + "% dei torinesi, in auto " + pa + "%."; }},
    en: {partenza: "Start", castello: "Piazza Castello (one census section per square)", zone: "Zones of Turin (one zone per colour)",
         traffico: "Car traffic", scorrevole: "flowing (factor ", pesante: "heavy (factor ", minuti: "minutes", min: "min",
         mezzi: "By public transport", auto: "By car", mezziBreve: "transit", autoBreve: "car", parti: "Play", ferma: "Pause", cursore: "Travel minutes",
         soglie: "How many residents you reach", dentro: "within ", ab: "of residents",
         non: "no connection within 120 minutes: ", fonteCastello: "Departure at 7:45 on a weekday; rush-hour car = free-flow time times the factor, plus 5 minutes to park.",
         caricamentoKo: "Data not available.", puntoOrigine: "start",
         parlato: function(o, m, pm, pa){ return "From " + o + ", within " + m + " minutes: by public transport " + pm + "% of residents, by car " + pa + "%."; }}
  };
  function lingua(){ return (document.documentElement.lang || "it").slice(0, 2) === "en" ? "en" : "it"; }
  function T(){ return TESTI[lingua()]; }
  function n(v){ return window.Sito && Sito.formattaNumero ? Sito.formattaNumero(v) : String(v); }
  function pct(v){ return n(Math.round(v * 10) / 10); }
  function esc(s){ return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
  function css(nome, ripiego){ var v = getComputedStyle(document.documentElement).getPropertyValue(nome).trim(); return v || ripiego; }

  function stile(){
    if(document.getElementById("area-stile")) return;
    var s = document.createElement("style"); s.id = "area-stile";
    s.textContent = ".area{margin:8px 0}.area .area-comandi{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;margin:4px 0 8px}"
      + ".area label{font-size:14px;color:var(--muted,#4a5a7a)}.area select,.area button{font:inherit;font-size:14px;padding:5px 8px;border:1px solid var(--line,#c9d2e4);border-radius:8px;background:var(--card,#fff);color:var(--ink,#0b2559);max-width:100%}"
      + ".area button{font-weight:600;padding:5px 14px;cursor:pointer}.area button:focus-visible,.area select:focus-visible,.area input:focus-visible{outline:3px solid var(--oro,#c9a227);outline-offset:2px}"
      + ".area .area-giro{display:flex;align-items:center;gap:10px;margin:2px 0 8px}.area .area-giro input{flex:1;min-width:120px}"
      + ".area .area-minuti{font:700 22px/1 var(--font-titoli,inherit);min-width:3.4em;text-align:right}"
      + ".area .area-mappe{display:grid;grid-template-columns:1fr 1fr;gap:10px}.area .area-mappa h6{margin:0 0 4px;font:700 15px/1.2 var(--font-titoli,inherit);text-transform:uppercase;letter-spacing:.02em}"
      + ".area canvas{display:block;width:100%;height:auto;background:var(--sunk,#f7f8fc);border-radius:8px}"
      + ".area .area-quota{font:700 20px/1.1 var(--font-titoli,inherit);margin-top:4px}.area .area-quota small{font:400 13px var(--font-testi,inherit);color:var(--muted,#4a5a7a)}"
      + ".area table{border-collapse:collapse;width:100%;margin:10px 0 0;font-size:14px}.area th,.area td{padding:5px 8px;border-bottom:1px solid var(--line,#c9d2e4);text-align:right}"
      + ".area th:first-child,.area td:first-child{text-align:left}.area tr.attiva td,.area tr.attiva th{font-weight:700;background:var(--hover,#eaeef7)}"
      + ".area .area-fermo{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}.area .area-fermo .area-cella p{margin:2px 0 0;font-size:12.5px;line-height:1.25}"
      + ".area .area-cella .t{font:700 15px/1.2 var(--font-titoli,inherit)}"
      + ".area .area-nota{font-size:13px;color:var(--muted,#4a5a7a);margin:8px 0 0}"
      + ".area-mini{margin:0}.area-mini .area-mappe{gap:6px}.area-mini .area-mappa h6{font-size:12px;margin:0 0 2px}.area-mini .area-quota{font-size:15px;margin-top:2px}"
      + ".area-mini .area-quota small{font-size:11px}.area-mini .area-minuti{display:block;text-align:center;font-size:17px;margin-top:6px;min-width:0}"
      + "@media (max-width:480px){.area .area-fermo{grid-template-columns:repeat(2,1fr)}}";
    document.head.appendChild(s);
  }

  /* ---- dati: data/area_tempi.js, caricato la prima volta che serve ---- */
  function carica(poi, male){
    if(window.AREA_TEMPI) return poi(window.AREA_TEMPI);
    if(!caricamento){
      caricamento = new Promise(function(ok, ko){
        var s = document.createElement("script"); s.src = "data/area_tempi.js";
        s.onload = function(){ window.AREA_TEMPI ? ok(window.AREA_TEMPI) : ko(); }; s.onerror = ko; document.head.appendChild(s);
      });
    }
    caricamento.then(poi, male);
  }

  /* ---- geometria: stessa per tutte le mappe ---- */
  function geom(D){
    if(D._g) return D._g;
    var mx = 0, my = 0, N = D.x.length, i;
    for(i = 0; i < N; i++){ if(D.x[i] > mx) mx = D.x[i]; if(D.y[i] > my) my = D.y[i]; }
    var k = Math.cos(45.07 * Math.PI / 180), W = mx * k, H = my, tot = 0;
    for(i = 0; i < N; i++) tot += D.r[i];
    D._g = {mx: mx, my: my, k: k, W: W, H: H, tot: tot, N: N};
    return D._g;
  }

  /* tempi di ogni sezione per la partenza scelta: [mezzi, auto] (null = non raggiunta) */
  function tempi(D, s){
    var N = D.x.length, m = new Array(N), a = new Array(N), i;
    var chiave = s.traffico === "b" ? "b" : "a";
    if(s.origine === 0){
      for(i = 0; i < N; i++){ m[i] = D.c.m[i]; a[i] = D.c[chiave][i]; }
    } else {
      var z = s.origine - 1, tz = D.zm[z], az = (chiave === "b" ? D.zb : D.za)[z];
      for(i = 0; i < N; i++){ m[i] = tz[D.z[i]]; a[i] = az[D.z[i]]; }
    }
    return [m, a];
  }

  function quota(D, t, minuto){
    var g = geom(D), s = 0;
    for(var i = 0; i < g.N; i++) if(t[i] !== null && t[i] <= minuto) s += D.r[i];
    return 100 * s / g.tot;
  }

  function puntoOrigine(D, s){
    if(s.origine === 0) return {x: D.ox, y: D.oy};
    var z = s.origine - 1, sx = 0, sy = 0, c = 0;
    for(var i = 0; i < D.x.length; i++) if(D.z[i] === z){ sx += D.x[i]; sy += D.y[i]; c++; }
    return {x: sx / c, y: sy / c};
  }

  function disegna(cv, D, t, minuto, colore, s){
    var g = geom(D), w = cv.width, h = cv.height, ctx = cv.getContext("2d");
    var pad = 6, sc = Math.min((w - 2 * pad) / g.W, (h - 2 * pad) / g.H);
    var lato = Math.max(2, 0.95 * Math.sqrt((g.W * sc) * (g.H * sc) / g.N));
    ctx.clearRect(0, 0, w, h);
    var spento = css("--line", "#c9d2e4"), i, px, py;
    var ox = pad + (w - 2 * pad - g.W * sc) / 2, oy = pad + (h - 2 * pad - g.H * sc) / 2;
    ctx.globalAlpha = .55; ctx.fillStyle = spento;
    for(i = 0; i < g.N; i++){
      if(t[i] !== null && t[i] <= minuto) continue;
      px = ox + D.x[i] * g.k * sc; py = oy + (g.my - D.y[i]) * sc;
      ctx.fillRect(px - lato / 2, py - lato / 2, lato, lato);
    }
    ctx.globalAlpha = .95; ctx.fillStyle = colore;
    for(i = 0; i < g.N; i++){
      if(t[i] === null || t[i] > minuto) continue;
      px = ox + D.x[i] * g.k * sc; py = oy + (g.my - D.y[i]) * sc;
      ctx.fillRect(px - lato / 2, py - lato / 2, lato, lato);
    }
    ctx.globalAlpha = 1;
    var p = puntoOrigine(D, s);
    px = ox + p.x * g.k * sc; py = oy + (g.my - p.y) * sc;
    ctx.lineWidth = 2.2; ctx.strokeStyle = css("--ink", "#0b2559"); ctx.fillStyle = css("--card", "#fff");
    ctx.beginPath(); ctx.arc(px, py, Math.max(4, lato * 1.1), 0, 6.2832); ctx.fill(); ctx.stroke();
  }

  function dimensiona(cv, D, larghezzaCss){
    var g = geom(D), r = window.devicePixelRatio > 1 ? 2 : 1;
    var w = Math.max(120, Math.round(larghezzaCss * r));
    cv.width = w; cv.height = Math.round(w * g.H / g.W);
  }

  function nomeOrigine(D, s){ return s.origine === 0 ? "Piazza Castello" : D.zn[s.origine - 1]; }

  function costruisci(el, D){
    var t = T(), uid = "area" + (++contatore);
    var stato = el._stato || (el._stato = {origine: 0, traffico: "a", minuto: 30});
    var opz0 = '<optgroup label="' + esc(t.castello) + '"><option value="0"' + (stato.origine === 0 ? " selected" : "") + '>Piazza Castello</option></optgroup>';
    var opz1 = '<optgroup label="' + esc(t.zone) + '">' + D.zn.map(function(nome, i){ return '<option value="' + (i + 1) + '"' + (stato.origine === i + 1 ? " selected" : "") + '>' + esc(nome) + '</option>'; }).join("") + '</optgroup>';
    var fa = D.f[0], fb = D.f[1];
    var traf = '<label for="' + uid + 't">' + esc(t.traffico) + '</label><select id="' + uid + 't"><option value="a"' + (stato.traffico === "a" ? " selected" : "") + '>' + esc(t.scorrevole) + String(fa).replace(".", lingua() === "en" ? "." : ",") + ')</option>'
      + '<option value="b"' + (stato.traffico === "b" ? " selected" : "") + '>' + esc(t.pesante) + String(fb).replace(".", lingua() === "en" ? "." : ",") + ')</option></select>';
    var comandi = '<div class="area-comandi"><label for="' + uid + 'o">' + esc(t.partenza) + '</label><select id="' + uid + 'o">' + opz0 + opz1 + '</select>' + traf + '</div>';
    var giro = ridotto ? "" : '<div class="area-giro"><button type="button" class="area-play">' + esc(t.parti) + '</button>'
      + '<input type="range" min="0" max="' + MAX_MIN + '" step="1" value="' + stato.minuto + '" aria-label="' + esc(t.cursore) + '"><span class="area-minuti" aria-hidden="true"></span></div>';
    var corpo;
    if(ridotto){
      corpo = '<div class="area-fermo">' + D.soglie.map(function(m){
        return '<div class="area-cella"><div class="t">' + esc(t.dentro) + n(m) + ' ' + esc(t.min) + '</div><canvas data-m="' + m + '" data-k="m" aria-hidden="true"></canvas><canvas data-m="' + m + '" data-k="a" aria-hidden="true"></canvas><p></p></div>';
      }).join("") + '</div>';
    } else {
      corpo = '<div class="area-mappe"><div class="area-mappa"><h6>' + esc(t.mezzi) + '</h6><canvas data-k="m" role="img"></canvas><div class="area-quota" data-q="m"></div></div>'
        + '<div class="area-mappa"><h6>' + esc(t.auto) + '</h6><canvas data-k="a" role="img"></canvas><div class="area-quota" data-q="a"></div></div></div>';
    }
    el.innerHTML = comandi + giro + corpo + '<table><thead><tr><th>' + esc(t.soglie) + '</th><th>' + esc(t.mezzi) + '</th><th>' + esc(t.auto) + '</th></tr></thead><tbody></tbody></table>'
      + '<p class="area-parlato" aria-live="polite" style="position:absolute;left:-9999px"></p><p class="area-nota">' + esc(t.fonteCastello) + '</p>';

    var selO = el.querySelector("#" + uid + "o"), selT = el.querySelector("#" + uid + "t"), rng = el.querySelector("input[type=range]"), play = el.querySelector(".area-play");
    var cvs = Array.prototype.slice.call(el.querySelectorAll("canvas"));
    var T_ = null;

    function ridisegna(){
      T_ = tempi(D, stato);
      var m = stato.minuto, pm = quota(D, T_[0], m), pa = quota(D, T_[1], m);
      var cMezzi = css("--neu-blu", "#6f8fc7"), cAuto = css("--neu-arancio", "#c9a227");
      if(ridotto){
        cvs.forEach(function(cv){ var mm = +cv.getAttribute("data-m"); cv.setAttribute("aria-hidden", "true"); disegna(cv, D, cv.getAttribute("data-k") === "m" ? T_[0] : T_[1], mm, cv.getAttribute("data-k") === "m" ? cMezzi : cAuto, stato); });
        Array.prototype.forEach.call(el.querySelectorAll(".area-cella"), function(c, i){
          var mm = D.soglie[i]; c.querySelector("p").textContent = t.mezziBreve + " " + n(Math.round(quota(D, T_[0], mm))) + "% · " + t.autoBreve + " " + n(Math.round(quota(D, T_[1], mm))) + "%";
        });
      } else {
        cvs.forEach(function(cv){ var mezzi = cv.getAttribute("data-k") === "m"; disegna(cv, D, mezzi ? T_[0] : T_[1], m, mezzi ? cMezzi : cAuto, stato);
          cv.setAttribute("aria-label", (mezzi ? t.mezzi : t.auto) + ": " + n(Math.round(mezzi ? pm : pa)) + "% " + t.ab); });
        el.querySelector("[data-q=m]").innerHTML = pct(pm) + '% <small>' + esc(t.ab) + ' ' + esc(t.dentro) + n(m) + ' ' + esc(t.min) + '</small>';
        el.querySelector("[data-q=a]").innerHTML = pct(pa) + '% <small>' + esc(t.ab) + ' ' + esc(t.dentro) + n(m) + ' ' + esc(t.min) + '</small>';
        el.querySelector(".area-minuti").textContent = n(m) + " " + t.min;
      }
      var cb = stato.traffico === "a" ? "b" : "a";           // l'altro fattore: la tabella mostra la forbice
      var altro = tempi(D, {origine: stato.origine, traffico: cb})[1];
      el.querySelector("tbody").innerHTML = D.soglie.map(function(mm){
        var qq = quota(D, T_[0], mm), q1 = quota(D, T_[1], mm), q2 = quota(D, altro, mm);
        var lo = Math.min(q1, q2), hi = Math.max(q1, q2);
        var auto = Math.round(lo) === Math.round(hi) ? n(Math.round(lo)) + "%" : n(Math.round(lo)) + "–" + n(Math.round(hi)) + "%";
        return '<tr' + (ridotto ? "" : (mm === m ? ' class="attiva"' : "")) + '><td>' + esc(t.dentro) + n(mm) + ' ' + esc(t.min) + '</td><td>' + n(Math.round(qq)) + '%</td><td>' + auto + '</td></tr>';
      }).join("");
      el.querySelector(".area-parlato").textContent = t.parlato(nomeOrigine(D, stato), m, n(Math.round(pm)), n(Math.round(pa)));
    }
    function misura(){
      var colonne = ridotto ? (window.innerWidth <= 480 ? 2 : 4) : 2;
      var larg = (el.clientWidth || 600) / colonne - (ridotto ? 8 : 10);
      cvs.forEach(function(cv){ dimensiona(cv, D, larg); });
    }
    misura(); ridisegna();
    if(el._ro) el._ro.disconnect();
    if("ResizeObserver" in window){ var ult = el.clientWidth; el._ro = new ResizeObserver(function(){ if(Math.abs(el.clientWidth - ult) > 8){ ult = el.clientWidth; misura(); ridisegna(); } }); el._ro.observe(el); }

    selO.addEventListener("change", function(){ stato.origine = parseInt(selO.value, 10); ferma(); ridisegna(); });
    selT.addEventListener("change", function(){ stato.traffico = selT.value; ridisegna(); });
    if(rng){
      rng.addEventListener("input", function(){ ferma(); stato.minuto = parseInt(rng.value, 10); ridisegna(); });
      play.addEventListener("click", function(){ if(el._anim) ferma(); else via(); });
    }
    var id = 0;
    function ferma(){ el._anim = 0; id++; if(play) play.textContent = t.parti; }
    function via(){
      var mio = ++id; el._anim = mio; play.textContent = t.ferma;
      var t0 = null, da = stato.minuto >= MAX_MIN ? 0 : stato.minuto;
      function passo(ts){
        if(el._anim !== mio || !document.body.contains(el)) return;
        if(t0 === null) t0 = ts;
        var f = Math.min(1, (ts - t0) / 1000 / (SEC_TOTALI * (1 - da / MAX_MIN) + .01));
        stato.minuto = Math.round(da + f * (MAX_MIN - da)); rng.value = stato.minuto; ridisegna();
        if(f < 1) requestAnimationFrame(passo); else ferma();
      }
      requestAnimationFrame(passo);
    }
    el._ferma = ferma;
  }

  /* versione piccola (riquadri della home): senza comandi ne' tabella; le due mappe crescono da sole da 0 a 60 minuti, poi ricominciano
     (solo mentre si vedono). Con «riduci movimento» si vede ferma la situazione a 30 minuti. */
  function costruisciMini(el, D){
    var t = T(), cMezzi = css("--neu-blu", "#6f8fc7"), cAuto = css("--neu-arancio", "#c9a227");
    var stato = {origine: 0, traffico: "a", minuto: 30};
    el.innerHTML = '<div class="area-mappe"><div class="area-mappa"><h6>' + esc(t.mezzi) + '</h6><canvas data-k="m" aria-hidden="true"></canvas><div class="area-quota" data-q="m"></div></div>'
      + '<div class="area-mappa"><h6>' + esc(t.auto) + '</h6><canvas data-k="a" aria-hidden="true"></canvas><div class="area-quota" data-q="a"></div></div></div>'
      + '<span class="area-minuti" aria-hidden="true"></span>';
    var cvs = Array.prototype.slice.call(el.querySelectorAll("canvas")), T_ = tempi(D, stato);
    var larg = (el.clientWidth || 240) / 2 - 6;
    cvs.forEach(function(cv){ dimensiona(cv, D, larg); });
    function ridisegna(){
      var m = stato.minuto, pm = quota(D, T_[0], m), pa = quota(D, T_[1], m);
      cvs.forEach(function(cv){ var mezzi = cv.getAttribute("data-k") === "m"; disegna(cv, D, mezzi ? T_[0] : T_[1], m, mezzi ? cMezzi : cAuto, stato); });
      el.querySelector("[data-q=m]").innerHTML = n(Math.round(pm)) + '%';
      el.querySelector("[data-q=a]").innerHTML = n(Math.round(pa)) + '%';
      el.querySelector(".area-minuti").textContent = t.dentro + n(m) + " " + t.min;
    }
    ridisegna();
    el.setAttribute("role", "img");
    el.setAttribute("aria-label", t.parlato("Piazza Castello", 30, n(Math.round(quota(D, T_[0], 30))), n(Math.round(quota(D, T_[1], 30)))));
    if(ridotto) return;
    var giro = ++contatore, visibile = false;
    el._anim = giro;
    function corsa(){
      var t0 = null;
      function passo(ts){
        if(el._anim !== giro || !document.body.contains(el)) return;
        if(!visibile){ el._inattesa = true; return; }
        if(t0 === null) t0 = ts;
        var f = Math.min(1, (ts - t0) / 1000 / SEC_TOTALI);
        stato.minuto = Math.round(f * MAX_MIN); ridisegna();
        if(f < 1) requestAnimationFrame(passo);
        else setTimeout(function(){ if(el._anim === giro) corsa(); }, 2200);
      }
      requestAnimationFrame(passo);
    }
    stato.minuto = 0; ridisegna();
    if("IntersectionObserver" in window) new IntersectionObserver(function(v){
      visibile = v[0].isIntersecting;
      if(visibile && el._inattesa){ el._inattesa = false; corsa(); }
    }).observe(el); else visibile = true;
    el._inattesa = true;
    el._ferma = function(){ el._anim = 0; };
  }

  function avvia(el){
    if(el._pronto) return; el._pronto = true;
    stile();
    carica(function(D){
      var mini = el.hasAttribute("data-mini"), fa = mini ? costruisciMini : costruisci;
      fa(el, D);
      window.addEventListener("lingua", function(){ if(el._ferma) el._ferma(); if(document.body.contains(el)) fa(el, D); });
    }, function(){ el.textContent = T().caricamentoKo; });
  }

  function html(opz){ var mini = !!(opz && opz.compatto); return '<div class="area' + (mini ? " area-mini" : "") + '" data-area="1"' + (mini ? ' data-mini="1"' : "") + '></div>'; }

  function scansiona(radice){
    var els = (radice.querySelectorAll ? radice.querySelectorAll("[data-area]") : []);
    for(var i = 0; i < els.length; i++) avvia(els[i]);
    if(radice.matches && radice.matches("[data-area]")) avvia(radice);
  }
  function avviaTutto(){
    scansiona(document);
    new MutationObserver(function(muts){
      muts.forEach(function(m){ m.addedNodes.forEach(function(nd){ if(nd.nodeType === 1) scansiona(nd); }); });
    }).observe(document.body, {childList: true, subtree: true});
  }
  if(document.body) avviaTutto(); else document.addEventListener("DOMContentLoaded", avviaTutto);

  window.Area = {html: html, avvia: avvia};
})();
