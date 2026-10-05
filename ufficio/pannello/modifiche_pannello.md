# Modifiche al pannello fatte dalla chat

Una voce per modifica applicata: richiesta, file, differenze. Le piu' vecchie vengono potate da sole.

## 2026-10-04 00:29 · [m1791066589] Nella finestra Registro modifiche, rendi ogni voce più chiara. Per ogni modifica mostra, oltre alla data, una spiegazione di 1-2 frasi concise ma esaustive in italiano semplice, senza gergo. La spiegazione deve dire: cosa è cambiato, in quale parte del pannello (o in quale progetto) e a cosa serve per Leonardo. Esempio: 'Aggiunto un elenco a discesa Mondo nella barra in alto: permette di scegliere tra la Mappa e il nuovo mondo Cyberpunk.' Per le voci già presenti, riscrivi i testi in questo stile partendo da ciò che è registrato. Per le voci future, fai in modo che il testo venga scritto così al momento della modifica. Se una voce è troppo tecnica, mostra la spiegazione semplice in evidenza e tieni il dettaglio tecnico in secondo piano, visibile solo cliccando.
**Cosa e' stato fatto:** Nel Registro modifiche ogni voce ora mostra, sotto la data e il nome, una spiegazione di 1-2 frasi in italiano semplice: cosa è cambiato, dove (Mappa aziende o scheda base del CV) e a cosa serve. Il dettaglio tecnico (prima/dopo, motivo) è in "Dettaglio tecnico", visibile solo cliccando. Non ho potuto provare il pannello né eseguire Python: ho ricontrollato la sintassi rileggendo il codice.

Le modifiche sono in `pannello.html` (`renderReg`) e `pannello_server.py` (nuova `spiega_reg`, usata da `get_registro`). Le spiegazioni vengono costruite al momento della lettura dai dati registrati, quindi valgono anche per le voci vecchie e per quelle future. Se una voce ha già un campo `spiegazione` scritto da chi la registra, viene usato quello.

Per le voci sulle offerte non ho visto i dati registrati, perché il modulo che le scrive non è tra questi file. Per quelle esiste solo un testo generico basato sul motivo registrato.
**File:** pannello.html, pannello_server.py (+28 -1)
```diff
--- prima/pannello.html
+++ dopo/pannello.html
@@ -829,5 +829,7 @@
       r.tipo==='mappa_nuova'?'<div style="font-size:13px;margin-top:4px">'+esc(r.dopo)+'</div>':
       '<div style="font-size:13px;margin-top:4px"><span class="label">'+esc(r.campo)+'</span><br><span class="muted">prima:</span> '+esc(r.prima==null?'(vuoto)':r.prima)+'<br><span class="muted">dopo:</span> '+esc(r.dopo)+'</div>';
-    c.innerHTML='<div class="label">'+esc((r.quando||'').replace('T',' ').slice(0,16))+' · '+esc(r.chi)+' · '+esc(tipo)+' · <b>'+esc(r.stato)+'</b></div><h4>'+esc(r.oggetto_nome||'')+'</h4>'+cosa+'<div class="muted" style="font-size:12px">'+esc(r.motivo||'')+'</div>';
+    c.innerHTML='<div class="label">'+esc((r.quando||'').replace('T',' ').slice(0,16))+' · '+esc(r.chi)+' · '+esc(tipo)+' · <b>'+esc(r.stato)+'</b></div><h4>'+esc(r.oggetto_nome||'')+'</h4>'+
+      (r.spiegazione?'<div style="font-size:14px;margin-top:4px">'+esc(r.spiegazione)+'</div>':'')+
+      '<details style="margin-top:4px"><summary class="muted" style="font-size:12px;cursor:pointer">Dettaglio tecnico</summary>'+cosa+'<div class="muted" style="font-size:12px">'+esc(r.motivo||'')+'</div></details>';
     if(r.stato==='attivo'){
       var row=document.createElement('div');row.className='chips';row.style.marginTop='8px';
--- prima/pannello_server.py
+++ dopo/pannello_server.py
@@ -921,4 +921,28 @@
 
 
+def spiega_reg(r, nome):
+    # spiegazione semplice di una voce del registro; se la voce ne ha gia' una scritta, vale quella
+    if r.get("spiegazione"):
+        return str(r["spiegazione"])
+
+    def corto(v):
+        v = " ".join(str(v).split())
+        return v if len(v) <= 80 else v[:77] + "..."
+    chi = "da te" if r.get("chi") == "lui" else "da un agente o dal programma"
+    if r["tipo"] == "mappa_nuova":
+        return ("Aggiunta l'azienda %s alla Mappa aziende, proposta %s: serve ad allargare l'elenco delle aziende dove cercare lavoro."
+                % (nome, chi))
+    if r["tipo"] == "mappa":
+        campi = {"status": "lo stato", "priority": "la priorità", "notes": "le note"}
+        campo = campi.get(r.get("campo"), "«%s»" % r.get("campo"))
+        prima = "vuoto" if r.get("prima") is None else corto(r["prima"])
+        return ("Cambiato %s dell'azienda %s nella Mappa aziende, %s: da «%s» a «%s». Serve a tenere aggiornato a che punto sei con questa azienda."
+                % (campo, nome, chi, prima, corto(r.get("dopo", ""))))
+    if r["tipo"] == "baseline":
+        return ("Aggiunta una riga nella sezione AUTO della tua scheda di base del CV, scritta %s: serve a far usare questo dato nelle candidature."
+                % chi)
+    return "Modifica a %s fatta %s%s." % (nome, chi, (": " + corto(r["motivo"])) if r.get("motivo") else "")
+
+
 def get_registro(cfg):
     for s in sources(cfg):
@@ -935,4 +959,5 @@
                     o = S.find_offer(st_, r["oggetto"])
                     d["oggetto_nome"] = S.label(o) if o else r["oggetto"]
+                d["spiegazione"] = spiega_reg(r, d["oggetto_nome"])
                 rows.append(d)
             return {"sorgente": s["id"], "righe": rows}
```

## 2026-10-04 00:31 · [m1791066699] Le modifiche alla Mappa aziende devono essere applicate automaticamente, senza che Leonardo debba confermare con un pulsante. Vale soprattutto per le modifiche che sono solo note (aggiungere o cambiare una nota su un'azienda), ma anche per le altre modifiche alla mappa. Resta tutto registrato nel Registro modifiche, con la spiegazione breve, così Leonardo può vedere cosa è cambiato. Le azioni su offerte, CV e lettere restano con conferma come ora.
**Cosa e' stato fatto:** Ho cambiato `pannello_server.py`: ora le modifiche alla Mappa aziende (note, stato, priorità e aziende nuove) si confermano da sole. Non c'è più il pulsante "Va bene" per queste modifiche, e il contatore delle cose da controllare non le include più. Leonardo le vede nel Registro modifiche con la spiegazione breve, e in `pannello.html` ho solo aggiornato il testo introduttivo di quella pagina. Offerte, CV e lettere restano con conferma.

Non ho potuto eseguire il codice, quindi non l'ho provato: la sintassi l'ho solo riletta. Una modifica alla mappa già confermata ha perso il pulsante "Annulla" nel Registro. Non so se la funzione `reg_undo` accetti di annullare voci già confermate, perché il modulo che la contiene non è tra i file che ho qui.
**File:** pannello.html, pannello_server.py (+16 -1)
```diff
--- prima/pannello.html
+++ dopo/pannello.html
@@ -820,5 +820,5 @@
   var rows=(ARCH.data.righe||[]);
   var intro=document.createElement('div');intro.className='sub';intro.style.cssText='margin-bottom:10px;color:var(--ink2)';
-  intro.textContent='Tutto quello che programma e agenti hanno cambiato da soli: note sulla mappa, aziende nuove, righe aggiunte alla baseline. "Annulla" rimette com\'era prima; "Va bene" la segna come controllata.';
+  intro.textContent='Tutto quello che programma e agenti hanno cambiato da soli: note sulla mappa, aziende nuove, righe aggiunte alla baseline. Le modifiche alla mappa si applicano da sole e restano qui scritte. "Annulla" rimette com\'era prima; "Va bene" la segna come controllata.';
   body.appendChild(intro);
   if(!rows.length){body.innerHTML+='<div class="empty">Nessuna modifica per ora.</div>';return;}
--- prima/pannello_server.py
+++ dopo/pannello_server.py
@@ -878,5 +878,18 @@
         c["nuova"] = False
     S.update(go)
+    auto_conferma_mappa(S)
     return {"ok": bool(res.get("ok")), "msg": "Salvato." if res.get("ok") else "Azienda non trovata."}
+
+
+def auto_conferma_mappa(S):
+    # le modifiche alla mappa si applicano da sole: restano nel registro, ma non aspettano la conferma
+    def go(st_):
+        for r in st_["registro"]:
+            if r["stato"] == "attivo" and r["tipo"] in ("mappa", "mappa_nuova"):
+                r["stato"] = "ok"
+                if r["tipo"] == "mappa_nuova" and r["oggetto"] in st_["mappa"]:
+                    st_["mappa"][r["oggetto"]]["nuova"] = False
+    if any(r["stato"] == "attivo" and r["tipo"] in ("mappa", "mappa_nuova") for r in S.load()["registro"]):
+        S.update(go)
 
 
@@ -916,4 +929,5 @@
         if is_cv(s):
             S = cv_mod(s)
+            auto_conferma_mappa(S)
             st_ = S.load()
             return {"sorgente": s["id"], "aziende": S.map_view(st_), "scout_b": bool(st_["impostazioni"].get("scout_b"))}
@@ -949,4 +963,5 @@
         if is_cv(s):
             S = cv_mod(s)
+            auto_conferma_mappa(S)
             st_ = S.load()
             names = {c["id"]: c.get("name") for c in st_["mappa"].values()}
```

## 2026-10-05 15:02 · [m1791205297] In ufficio.html, quando si apre la vista del progetto con la chat, imposta il contenitore a larghezza piena (100% dello schermo) suddiviso tra dettagli del progetto e chat laterale, assegnando alla chat una quota più ampia (circa il 45% della larghezza totale, con testo e campo di input ben distesi) e il restante 55% ai dettagli del progetto.
**Cosa e' stato fatto:** Quando apri un progetto, la pagina ora si divide a tutto schermo: 55% ai dettagli del progetto e 45% alla chat laterale. Nella chat il testo è un po' più grande e il campo di scrittura più alto. Non l'ho aperta nel browser per provarla.

La modifica è tutta in `ufficio.html`: un blocco di stile nuovo e una riga che attiva la vista larga quando si apre un progetto. Chiudendo il progetto torna la chat stretta di prima.
**File:** ufficio.html (+4 -2)
```diff
--- prima/ufficio.html
+++ dopo/ufficio.html
@@ -53,5 +53,7 @@
 #chatOpen{position:fixed;right:16px;bottom:16px;z-index:25;display:none}
 /* chat v2 (05/10): con la chat aperta, le finestre (progetto, task...) si aprono A SINISTRA della chat, cosi' la chat del progetto resta visibile */
-@media(min-width:901px){main:not(.nochat)~.drawer{right:340px;width:min(680px,calc(100vw - 340px))}main:not(.nochat)~.drawer.wide{width:min(980px,calc(100vw - 340px))}main:not(.nochat)~.drawer.full{width:calc(100vw - 340px);padding:22px 20px}main:not(.nochat)~.drawer:not(.on){transform:translateX(calc(105% + 340px));visibility:hidden}}
+@media(min-width:901px){main:not(.nochat)~.drawer{right:340px;width:min(680px,calc(100vw - 340px))}main:not(.nochat)~.drawer.wide{width:min(980px,calc(100vw - 340px))}main:not(.nochat)~.drawer.full{width:calc(100vw - 340px);padding:22px 20px}main:not(.nochat)~.drawer:not(.on){transform:translateX(calc(105% + 340px));visibility:hidden}
+/* vista progetto: pagina a tutta larghezza, 55% dettagli e 45% chat */
+body.proj main:not(.nochat){grid-template-columns:1fr 45vw}body.proj main:not(.nochat)~.drawer,body.proj main:not(.nochat)~.drawer.wide,body.proj main:not(.nochat)~.drawer.full{right:45vw;width:55vw}body.proj main:not(.nochat)~.drawer:not(.on){transform:translateX(calc(105% + 45vw))}body.proj .chat .msgs{font-size:14px;padding:16px 20px}body.proj .chat textarea{height:72px}}
 .drawer{position:fixed;top:0;right:0;bottom:0;width:min(680px,96vw);background:var(--card);box-shadow:-10px 0 30px #0006;transform:translateX(105%);transition:.22s;z-index:20;overflow:auto;padding:20px}
 .drawer.on{transform:none}.drawer h2{color:var(--ink);text-transform:none;font-size:19px;letter-spacing:0;margin-bottom:4px}
@@ -780,5 +782,5 @@
   if(id){var pm=prj(id).motore||(S&&S.motori&&S.motori.predefinito)||'claude';mot.value=mot2(pm);}
   else{mot.value=MOTG;}
-  CHATP=id;CHAT=CHAT||{};CHAT.storia=[];$('hChat').innerHTML=id?'· '+esc(prj(id).nome||id):hlp('chat');
+  CHATP=id;document.body.classList.toggle('proj',!!id);CHAT=CHAT||{};CHAT.storia=[];$('hChat').innerHTML=id?'· '+esc(prj(id).nome||id):hlp('chat');
   $('chatIn').placeholder=id?'Chiedi sul progetto, o descrivi una task… (Invio per mandare)':'Chiedi, o descrivi una task da mettere in coda… (Invio per mandare)';loadChat();}
 function loadChat(){var pid=CHATP;return api('/api/chat'+(pid?'?progetto='+encodeURIComponent(pid):'')).then(function(c){if(pid!==CHATP)return;CHAT=c;drawChat();});}
```
