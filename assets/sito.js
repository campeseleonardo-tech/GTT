/* Funzioni comuni delle pagine del sito (home, risultati): numeri in italiano, numeri che salgono, data dei dati nel piè di pagina. */
"use strict";
(function(){
  function esc(s){ return String(s==null?"":s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }

  /* numero in stile italiano: punto delle migliaia anche sotto 10.000, al massimo una cifra decimale */
  function formattaNumero(n){
    if(typeof n !== "number" || !Number.isFinite(n)) return esc(String(n));
    if(Number.isInteger(n)) return (n < 0 ? "−" : "") + String(Math.abs(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    return n.toLocaleString("it-IT", {maximumFractionDigits:1});
  }

  var ridotto = !!(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches);

  /* il numero sale da 0 al valore in circa 1,5 secondi, piano piano verso la fine, UNA volta sola, quando l'elemento appare.
     L'elemento ha già il testo finale (data-valore = il numero, data-suffisso = "%" o vuoto): senza animazione resta quello. */
  function contaSu(el){
    if(!el || el.dataset.fatto) return;
    var fine = parseFloat(el.dataset.valore);
    if(!Number.isFinite(fine) || ridotto || !window.requestAnimationFrame){ el.dataset.fatto = "1"; return; }
    var suff = el.dataset.suffisso || "", testoFinale = el.textContent, t0 = null, DUR = 1500;
    var intero = Number.isInteger(fine);
    el.dataset.fatto = "1";
    function passo(t){
      if(t0 === null) t0 = t;
      var x = Math.min(1, (t - t0) / DUR), v = fine * (1 - Math.pow(1 - x, 5));   // rallenta molto verso la fine
      el.textContent = (x >= 1 ? testoFinale : formattaNumero(intero ? Math.round(v) : Math.round(v * 10) / 10) + suff);
      if(x < 1) requestAnimationFrame(passo);
    }
    el.textContent = formattaNumero(0) + suff;
    requestAnimationFrame(passo);
  }
  function osserva(radice){
    var els = (radice || document).querySelectorAll("[data-valore]");
    if(!("IntersectionObserver" in window)){ return; }
    var io = new IntersectionObserver(function(voci){
      voci.forEach(function(v){ if(v.isIntersecting){ io.unobserve(v.target); contaSu(v.target); } });
    }, {threshold:.3});
    els.forEach(function(e){ if(!e.dataset.fatto) io.observe(e); });
  }

  /* «dati aggiornati al …»: la data più recente fra le schede */
  function dataAggiornamento(){
    var el = document.getElementById("datiAggiornati");
    var s = Array.isArray(window.SCHEDE_RISULTATI) ? window.SCHEDE_RISULTATI : [];
    var d = s.map(function(x){ return x && x.generato; }).filter(Boolean).sort().pop();
    if(el && d){
      var m = /^(\d{4})-(\d{2})-(\d{2})/.exec(d);
      if(m) el.textContent = "Dati aggiornati al " + m[3] + "/" + m[2] + "/" + m[1] + ".";
    }
  }

  window.Sito = {esc: esc, formattaNumero: formattaNumero, contaSu: contaSu, osserva: osserva, dataAggiornamento: dataAggiornamento, ridotto: ridotto};
})();
