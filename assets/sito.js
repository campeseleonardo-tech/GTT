/* Funzioni comuni delle pagine del sito: lingua IT/EN, numeri, numeri che salgono, data dei dati nel piè di pagina. */
"use strict";
(function(){
  function esc(s){ return String(s==null?"":s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }

  /* ---- lingua: italiano (default) o inglese; si ricorda la scelta; ?lang=en la forza; senza scelta segue il browser */
  var lang = "it";
  function leggiLingua(){
    var q = /[?&]lang=(it|en)\b/.exec(location.search);
    if(q) return q[1];
    try { var s = localStorage.getItem("tm_lingua"); if(s === "it" || s === "en") return s; } catch(e){}
    var n = (navigator.language || "it").toLowerCase();
    return n.indexOf("it") === 0 ? "it" : "en";
  }
  function T(it, en){ return lang === "en" ? en : it; }
  /* testi fissi della pagina: l'elemento ha l'italiano dentro e l'inglese in data-en */
  function traduciStatico(radice){
    var r = radice || document;      // con «radice» solo i testi di quel pezzo di pagina (per i pezzi scritti dal codice, es. le tappe del progetto)
    if(!radice) document.documentElement.lang = lang;
    r.querySelectorAll("[data-en]").forEach(function(el){
      if(el.dataset.it === undefined) el.dataset.it = el.innerHTML;
      el.innerHTML = lang === "en" ? el.dataset.en : el.dataset.it;
    });
    r.querySelectorAll("[data-en-label]").forEach(function(el){
      if(el.dataset.itLabel === undefined) el.dataset.itLabel = el.getAttribute("aria-label") || "";
      el.setAttribute("aria-label", lang === "en" ? el.dataset.enLabel : el.dataset.itLabel);
    });
    if(radice) return;
    document.querySelectorAll(".lingua button").forEach(function(b){ b.setAttribute("aria-pressed", b.dataset.l === lang ? "true" : "false"); });
    var tit = document.querySelector("title");
    if(tit){ if(tit.dataset.it === undefined) tit.dataset.it = tit.textContent; if(tit.dataset.en) tit.textContent = lang === "en" ? tit.dataset.en : tit.dataset.it; }
  }
  function impostaLingua(l){
    if(l !== "it" && l !== "en" || l === lang) return;
    lang = l;
    try { localStorage.setItem("tm_lingua", l); } catch(e){}
    traduciStatico();
    dataAggiornamento();
    window.dispatchEvent(new Event("lingua"));
  }
  lang = leggiLingua();

  /* numero: italiano (1.234,5) o inglese (1,234.5), al massimo una cifra decimale */
  function formattaNumero(n){
    if(typeof n !== "number" || !Number.isFinite(n)) return esc(String(n));
    var mig = lang === "en" ? "," : ".";
    if(Number.isInteger(n)) return (n < 0 ? "−" : "") + String(Math.abs(n)).replace(/\B(?=(\d{3})+(?!\d))/g, mig);
    return n.toLocaleString(lang === "en" ? "en-GB" : "it-IT", {maximumFractionDigits:1});
  }

  var ridotto = !!(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches);

  /* il numero sale da 0 al valore in circa 2,6 secondi, partendo e arrivando piano, UNA volta sola, quando l'elemento appare.
     Durante la corsa solo numeri interi, senza virgola né %: il testo finale (decimali, %) compare solo all'arrivo.
     L'elemento ha già il testo finale: data-valore = il numero, oppure data-forbice = "21,28" (due numeri che salgono insieme).
     La larghezza resta quella del testo finale, così niente intorno si sposta. Senza animazione resta il testo finale. */
  function contaSu(el){
    if(!el || el.dataset.fatto) return;
    var fb = (el.dataset.forbice || "").split(",").map(parseFloat).filter(Number.isFinite);
    var fine = fb.length === 2 ? fb : [parseFloat(el.dataset.valore)];
    el.dataset.fatto = "1";
    if(!Number.isFinite(fine[0]) || ridotto || !window.requestAnimationFrame) return;
    var testoFinale = el.textContent, t0 = null, DUR = 2600, ultimo = "";
    el.style.display = "inline-block";
    el.style.minWidth = el.getBoundingClientRect().width + "px";
    function morbido(x){ return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; }
    function testo(f){ return fine.map(function(v){ return formattaNumero(Math.floor(v * f)); }).join("–"); }
    function passo(t){
      if(t0 === null) t0 = t;
      var x = Math.min(1, (t - t0) / DUR), s = x >= 1 ? testoFinale : testo(morbido(x));
      if(s !== ultimo){ el.textContent = s; ultimo = s; }
      if(x < 1) requestAnimationFrame(passo);
    }
    el.textContent = testo(0);
    requestAnimationFrame(passo);
  }
  function osserva(radice){
    var els = (radice || document).querySelectorAll("[data-valore],[data-forbice]");
    if(!("IntersectionObserver" in window)){ return; }
    var io = new IntersectionObserver(function(voci){
      voci.forEach(function(v){ if(v.isIntersecting){ io.unobserve(v.target); contaSu(v.target); } });
    }, {threshold:.3});
    els.forEach(function(e){ if(!e.dataset.fatto) io.observe(e); });
  }

  /* «Dati dal 09/10 al 22/10/2026»: il periodo fisso dei dati (comuni.PERIODO, scritto da scripts/schede_risultati.py in data/schede_risultati.js) */
  function dataAggiornamento(){
    var el = document.getElementById("datiAggiornati");
    var p = window.SCHEDE_PERIODO;
    if(!el || !p) return;
    var da = /^(\d{4})-(\d{2})-(\d{2})$/.exec(p.da || ""), a = /^(\d{4})-(\d{2})-(\d{2})$/.exec(p.a || "");
    if(da && a) el.textContent = T("Dati dal ", "Data from ") + da[3] + "/" + da[2] + T(" al ", " to ") + a[3] + "/" + a[2] + "/" + a[1] + ".";
  }

  /* giorni dalla raccolta: dal primo giorno (INIZIO_RACCOLTA, nel contatore dei dati) a oggi; la stessa regola per home e progetto */
  function giorniRaccolta(c){
    var m = c && /^(\d{4})-(\d{2})-(\d{2})$/.exec(c.inizio_raccolta || c.dal || "");
    if(!m) return null;
    var oggi = new Date(), d0 = new Date(+m[1], +m[2] - 1, +m[3]);
    return Math.max(1, Math.floor((new Date(oggi.getFullYear(), oggi.getMonth(), oggi.getDate()) - d0) / 864e5) + 1);
  }

  function avvia(){
    document.querySelectorAll(".lingua button").forEach(function(b){ b.addEventListener("click", function(){ impostaLingua(b.dataset.l); }); });
    traduciStatico();
  }
  window.Sito = {esc: esc, formattaNumero: formattaNumero, contaSu: contaSu, osserva: osserva, dataAggiornamento: dataAggiornamento, giorniRaccolta: giorniRaccolta, ridotto: ridotto,
                 T: T, traduci: traduciStatico, lingua: function(){ return lang; }, impostaLingua: impostaLingua, avvia: avvia};
})();
