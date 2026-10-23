// generato da scripts/schede_risultati.py - non modificare a mano
window.SCHEDE_RISULTATI = [
 {
  "risultato": "1",
  "titolo": "Dove mancano i servizi a piedi",
  "tag": "STIMATO",
  "stato": "Fatto",
  "in_breve": "Torino è una città compatta, ma non tutti hanno scuola, medico, negozi, una fermata e un po' di verde a un quarto d'ora a piedi da casa.",
  "domanda": "Quanti residenti di Torino, nelle zone abitate, non hanno più servizi essenziali (scuole, salute, negozi e attività commerciali, fermate, verde) entro 15 minuti a piedi, e quanti ne recupererebbe qualche servizio nuovo?",
  "numero_chiave": {
   "valore": 362,
   "unita": "residenti",
   "testo": "di zone abitate di Torino senza 3 o più dei 5 servizi essenziali a 15 minuti a piedi (0% dei torinesi)"
  },
  "racconto": "Una delle domande da cui è partito il progetto: dove mancano i servizi? L'idea di riferimento è la \"città dei 15 minuti\", in cui le cose di tutti i giorni si raggiungono a piedi.",
  "risposta": [
   "362 residenti su 848.748 (0%) vivono in zone abitate (almeno 1.000 abitanti per km²) e non hanno 3 o più dei 5 servizi entro 15 minuti a piedi. Tutti e 5 mancano a 8 residenti.",
   "Altri 6.768 residenti vivono in zone poco abitate (parchi, collina): sono contati a parte, fuori dal titolo.",
   "Altri 389 residenti sono in zone dove il calcolo non raggiunge una fermata che c'è: contati a parte, da verificare.",
   "Contando anche le zone poco abitate, 10.919 residenti su 848.748 (1,3%) non hanno almeno uno dei 5 servizi entro 15 minuti a piedi.",
   "Il servizio che manca più spesso è salute: 9.104 residenti senza un servizio di questo tipo vicino.",
   "Pochi servizi nuovi messi nei punti giusti (al massimo 5 per gruppo) riporterebbero entro i 15 minuti 6.190 di questi casi, contati gruppo per gruppo."
  ],
  "grafici": [
   {
    "tipo": "barre",
    "titolo": "Residenti per numero di servizi mancanti (0-5), zone abitate",
    "unita": "residenti",
    "nota": "Zone abitate = almeno 1.000 abitanti per km². Le zone poco abitate (6.768 residenti) sono escluse. Servizi mancanti = zero entro 15 minuti a piedi.",
    "voci": [
     {
      "label": "0 mancanti",
      "valore": 834963
     },
     {
      "label": "1 mancanti",
      "valore": 5302
     },
     {
      "label": "2 mancanti",
      "valore": 964
     },
     {
      "label": "3 mancanti",
      "valore": 362,
      "tono": "rosso"
     },
     {
      "label": "4 mancanti",
      "valore": 0,
      "tono": "rosso"
     },
     {
      "label": "5 mancanti",
      "valore": 0,
      "tono": "rosso"
     }
    ]
   },
   {
    "tipo": "barre",
    "titolo": "Residenti di Torino senza il servizio entro 15 minuti a piedi",
    "unita": "residenti",
    "voci": [
     {
      "label": "salute",
      "valore": 9104,
      "tono": "rosso"
     },
     {
      "label": "scuole",
      "valore": 6060,
      "tono": "rosso"
     },
     {
      "label": "negozi e attività commerciali",
      "valore": 1697,
      "tono": "rosso"
     },
     {
      "label": "fermate",
      "valore": 1204,
      "tono": "rosso"
     },
     {
      "label": "verde",
      "valore": 104,
      "tono": "rosso"
     }
    ]
   },
   {
    "tipo": "barre",
    "titolo": "Residenti con pochissimi servizi di quel tipo vicini",
    "unita": "residenti",
    "nota": "\"Pochissimi\" = sotto il livello che ha il 10% dei residenti meno servito (soglia per gruppo).",
    "voci": [
     {
      "label": "salute",
      "valore": 86915
     },
     {
      "label": "scuole",
      "valore": 84147
     },
     {
      "label": "negozi e attività commerciali",
      "valore": 83353
     },
     {
      "label": "fermate",
      "valore": 3357
     },
     {
      "label": "verde",
      "valore": 11330
     }
    ]
   },
   {
    "tipo": "barre",
    "titolo": "Residenti senza il servizio: oggi e con i punti nuovi",
    "unita": "residenti",
    "nota": "Barra chiara = oggi, barra scura = con i punti nuovi.",
    "voci": [
     {
      "label": "salute (5 punti nuovi)",
      "valore": 1494,
      "prima": 5340,
      "tono": "rosso"
     },
     {
      "label": "scuole (5 punti nuovi)",
      "valore": 617,
      "prima": 2529,
      "tono": "rosso"
     },
     {
      "label": "negozi e attività commerciali (3 punti nuovi)",
      "valore": 0,
      "prima": 347,
      "tono": "rosso"
     },
     {
      "label": "fermate (1 punto nuovo)",
      "valore": 15,
      "prima": 100,
      "tono": "rosso"
     },
     {
      "label": "verde (0 punti nuovi)",
      "valore": 0,
      "prima": 0,
      "tono": "rosso"
     }
    ]
   }
  ],
  "metodo": [
   "Per ognuna delle 4.044 sezioni di censimento di Torino (centinaia di persone ciascuna) si contano i servizi raggiungibili camminando 15 minuti sulla rete stradale reale (OpenStreetMap), con il motore di percorsi R5.",
   "Cinque gruppi trattati separatamente, senza un indice unico: scuole, salute, negozi e attività commerciali (catalogo comunale), fermate del trasporto pubblico, verde.",
   "\"Senza\" = zero servizi di quel gruppo entro 15 minuti. I residenti vengono dal censimento ISTAT 2021.",
   "Per ogni sezione si contano quanti dei 5 gruppi mancano (0-5). Le sezioni con meno di 1.000 abitanti per km² (superficie e residenti del censimento) sono \"poco abitate\": in grigio e fuori dal titolo, che conta i residenti delle zone abitate con 3 o più servizi mancanti.",
   "Dove aggiungere un servizio: per ogni gruppo si cercano fino a 5 punti (raggruppando le zone scoperte entro 400 m) che riportano dentro i 15 minuti più residenti possibile, uno dopo l'altro."
  ],
  "criteri": [
   {
    "nome": "Zona poco abitata",
    "valore": "sotto 1.000 abitanti per km²",
    "perche": "parchi, collina e zone poco abitabili sono vuoti per natura: contarli come carenza falserebbe il titolo",
    "effetto": "500 ab/km²: 2.875 residenti poco abitati, 1.395 abitati con 3 o più servizi mancanti, 9.140 abitati con almeno 1; 1.000 ab/km²: 6.768 residenti poco abitati, 362 abitati con 3 o più servizi mancanti, 6.628 abitati con almeno 1; 2.000 ab/km²: 17.039 residenti poco abitati, 0 abitati con 3 o più servizi mancanti, 1.614 abitati con almeno 1"
   },
   {
    "nome": "Titolo",
    "valore": "residenti delle zone abitate con 3 o più dei 5 servizi mancanti",
    "perche": "guardare dove mancano più servizi insieme, non uno solo",
    "effetto": "\"tutti e 5 mancanti\": 8 residenti (non fa titolo)"
   },
   {
    "nome": "Cintura (a parte)",
    "valore": "servizio raggiungibile a piedi in 15 minuti o col mezzo pubblico entro 45 minuti alle 08:00 di un feriale (scuole, salute, negozi)",
    "perche": "fuori Torino si va in paese e non a piedi: la regola della città dei 15 minuti non vale",
    "effetto": "834 residenti di zone abitate con 3 o più servizi mancanti: non confrontabile con Torino (catalogo diverso)"
   }
  ],
  "parametri": [
   [
    "Tempo a piedi",
    "15 minuti"
   ],
   [
    "Velocità a piedi",
    "80 m al minuto (4,8 km/h)"
   ],
   [
    "Zona poco abitata",
    "sotto 1.000 ab/km² (prove con 500 e 2.000)"
   ],
   [
    "Sezioni di Torino",
    "4.044"
   ],
   [
    "Residenti",
    "848.748"
   ],
   [
    "Punti nuovi per gruppo",
    "fino a 5"
   ]
  ],
  "limiti": [
   "Zona \"da verificare\": nessuna fermata entro 15 minuti a piedi nel calcolo, ma una fermata GTT entro 300 m in linea d'aria (probabile errore del punto di partenza); esclusa dal titolo e dai punti nuovi.",
   "Solo Torino: in cintura il catalogo dei servizi non c'è, quindi lì \"zero\" vuol dire spesso \"manca il dato\", non \"manca il servizio\".",
   "Il gruppo \"negozi e attività commerciali\" usa tutte le attività commerciali del catalogo, senza distinguere la categoria.",
   "Si conta se un servizio c'è, non quanto è grande o se ha posto (una scuola piena conta come una vuota).",
   "Capienza di ospedali, presidi e scuole non nota: un ospedale grande e un ambulatorio contano uguale.",
   "Orario programmato: niente ritardi né affollamento. Le sezioni senza superficie contano come abitate.",
   "I punti nuovi sono posizioni ipotetiche: non tengono conto di costi, spazi liberi o permessi, e non si sommano tra gruppi."
  ],
  "in_english": [
   "Question: how many Turin residents in inhabited areas lack 3 or more essential services (schools, health, shops and commercial activities, stops, green space) within 15 minutes on foot, and how many would gain one with a few new services?",
   "362 residents out of 848,748 (0.0%) live in inhabited areas (at least 1,000 inhabitants per km²) and lack 3 or more of the 5 services within 15 minutes on foot; all 5 are missing for 8. A further 6,768 residents live in sparsely populated areas (parks, hills), counted separately. Sensitivity of the threshold: at 500 inhabitants/km² the sparsely populated zones hold 2,875 residents and those missing 3+ services 1,395; at 1,000 inhabitants/km² the sparsely populated zones hold 6,768 residents and those missing 3+ services 362; at 2,000 inhabitants/km² the sparsely populated zones hold 17,039 residents and those missing 3+ services 0.",
   "Counting those areas too, 10,919 residents out of 848,748 (1.3%) lack at least one of the 5 services within 15 minutes on foot. The most often missing one is health, with 9,104 residents without a nearby service of that kind.",
   "A further 389 residents live in areas where the calculation does not reach a stop that exists (counted separately, to be verified).",
   "Up to 5 new services per group, placed where they help most, would bring 6,190 of these cases within 15 minutes, counted group by group.",
   "Areas flagged for verification have no stop within 15 minutes on foot in the calculation but a stop within 300 m as the crow flies; they are excluded from the headline figure and from the new-service points.",
   "Limits: the map covers Turin and its surrounding belt; in the belt a service counts as missing only if it is out of reach both on foot (15 minutes) and by public transport (45 minutes, 8 am on a weekday), and the service data there (schools, health, shops from OpenStreetMap) is less complete."
  ],
  "mappa": {
   "id": "faseb",
   "tema": "Dove mancano i servizi",
   "nota": "Nella mappa, tema \"Dove mancano i servizi\": all'apertura quanti servizi mancano in ogni zona (0-5, zone poco abitate in grigio); nel menu un servizio alla volta, con i punti dove aggiungerne uno."
  },
  "fonti": [
   "docs/R1_servizi.md",
   "docs/rapporti/RAPPORTO_RISULTATO1.txt",
   "docs/rapporti/RAPPORTO_RISULTATO1_CANDIDATI.txt",
   "scripts/21_risultato1_vuoti.py",
   "scripts/22_risultato1_candidati.py"
  ],
  "generato": "2026-10-23T13:30:39+00:00",
  "avviso": [
   "Dati [STIMATO] — solo comune di Torino",
   "Distanze a piedi sulla rete stradale (15 min a 80 m/min) su 848.748 residenti (censimento 2021). Servizi dal catalogo comunale: la cintura non è confrontabile (manca il dato, non il servizio). I punti nuovi sono ipotesi di posizione, calcolate gruppo per gruppo: non si sommano tra gruppi e non tengono conto di costi o spazi disponibili."
  ],
  "scenari": [
   {
    "nome": "Oggi",
    "numeri": [
     {
      "label": "Residenti di zone abitate senza 3 o più servizi",
      "prima": null,
      "dopo": 362,
      "unita": "residenti"
     },
     {
      "label": "Quota dei residenti di Torino",
      "prima": null,
      "dopo": 0.0,
      "unita": "%"
     },
     {
      "label": "Tutti e 5 i servizi mancanti",
      "prima": null,
      "dopo": 8,
      "unita": "residenti"
     },
     {
      "label": "Residenti nelle zone poco abitate (a parte)",
      "prima": null,
      "dopo": 6768,
      "unita": "residenti"
     },
     {
      "label": "Residenti in zone da verificare (a parte)",
      "prima": null,
      "dopo": 389,
      "unita": "residenti"
     },
     {
      "label": "Residenti senza almeno un servizio essenziale",
      "prima": null,
      "dopo": 10919,
      "unita": "residenti"
     },
     {
      "label": "Quota dei residenti di Torino senza almeno un servizio",
      "prima": null,
      "dopo": 1.3,
      "unita": "%"
     },
     {
      "label": "Senza salute entro 15 min",
      "prima": null,
      "dopo": 9104,
      "unita": "residenti"
     },
     {
      "label": "Senza scuole entro 15 min",
      "prima": null,
      "dopo": 6060,
      "unita": "residenti"
     },
     {
      "label": "Senza negozi e attività commerciali entro 15 min",
      "prima": null,
      "dopo": 1697,
      "unita": "residenti"
     },
     {
      "label": "Senza fermate entro 15 min",
      "prima": null,
      "dopo": 1204,
      "unita": "residenti"
     },
     {
      "label": "Senza verde entro 15 min",
      "prima": null,
      "dopo": 104,
      "unita": "residenti"
     }
    ],
    "nota": "Il gruppo con più residenti scoperti è salute. Sensibilità della soglia: con 500 ab/km² le zone poco abitate sono 2.875 residenti e quelli con 3 o più servizi mancanti 1.395; con 1.000 ab/km² le zone poco abitate sono 6.768 residenti e quelli con 3 o più servizi mancanti 362; con 2.000 ab/km² le zone poco abitate sono 17.039 residenti e quelli con 3 o più servizi mancanti 0."
   },
   {
    "nome": "Con pochi servizi nuovi nei punti migliori",
    "numeri": [
     {
      "label": "Senza salute (5 punti nuovi)",
      "prima": 5340,
      "dopo": 1494,
      "unita": "residenti"
     },
     {
      "label": "Senza scuole (5 punti nuovi)",
      "prima": 2529,
      "dopo": 617,
      "unita": "residenti"
     },
     {
      "label": "Senza negozi e attività commerciali (3 punti nuovi)",
      "prima": 347,
      "dopo": 0,
      "unita": "residenti"
     },
     {
      "label": "Senza fermate (1 punto nuovo)",
      "prima": 100,
      "dopo": 15,
      "unita": "residenti"
     },
     {
      "label": "Senza verde (0 punti nuovi)",
      "prima": 0,
      "dopo": 0,
      "unita": "residenti"
     }
    ],
    "nota": "Fino a 5 punti per gruppo, scelti dove recuperano più residenti (raggruppamento 400 m)."
   }
  ],
  "forma": {
   "etichetta": "STIMATO",
   "titolo": "A 15 minuti quasi tutti hanno i servizi; a 5 minuti molti meno",
   "domanda": "Quanti torinesi hanno i servizi a 5, 10 e 15 minuti a piedi, e quanti vivono su una strada trafficata?",
   "numero": {
    "valore": 99.2,
    "unita": "%",
    "testo": "dei residenti delle zone abitate ha tutti e 5 i servizi a 15 minuti a piedi"
   },
   "principale": {
    "tipo": "pila100",
    "titolo": "Residenti per servizi raggiunti a piedi",
    "unita": "%",
    "nota": "Ogni barra è un tempo a piedi: 100% dei residenti delle zone abitate (almeno 1.000 abitanti per km²).",
    "righe": [
     {
      "label": "5 minuti",
      "voci": [
       {
        "label": "tutti e 5 i servizi",
        "valore": 68.3,
        "tono": "verde"
       },
       {
        "label": "4 servizi",
        "valore": 22.2,
        "tono": "giallo"
       },
       {
        "label": "3 o meno",
        "valore": 9.5,
        "tono": "rosso"
       }
      ]
     },
     {
      "label": "10 minuti",
      "voci": [
       {
        "label": "tutti e 5 i servizi",
        "valore": 96.8,
        "tono": "verde"
       },
       {
        "label": "4 servizi",
        "valore": 2.4,
        "tono": "giallo"
       },
       {
        "label": "3 o meno",
        "valore": 0.8,
        "tono": "rosso"
       }
      ]
     },
     {
      "label": "15 minuti",
      "voci": [
       {
        "label": "tutti e 5 i servizi",
        "valore": 99.2,
        "tono": "verde"
       },
       {
        "label": "4 servizi",
        "valore": 0.6,
        "tono": "giallo"
       },
       {
        "label": "3 o meno",
        "valore": 0.2,
        "tono": "rosso"
       }
      ]
     }
    ]
   },
   "punti": [
    "A 5 minuti solo il 68,3% dei residenti ha tutti e 5 i servizi; a 10 minuti il 96,8%.",
    "190.255 residenti (22,6%) vivono a meno di 100 m da una strada molto trafficata.",
    "I 362 residenti senza 3 o più servizi sono in 5 sezioni di collina: dove manca davvero tutto."
   ],
   "altri": [
    {
     "tipo": "barre",
     "titolo": "Residenti per distanza da una strada molto trafficata",
     "unita": "residenti",
     "nota": "Distanza dal centro della sezione. Strada molto trafficata: almeno 11.720 veicoli al giorno. Stima debole: il modello sbaglia del ±38% in metà dei casi.",
     "voci": [
      {
       "label": "esposti (meno di 100 m)",
       "valore": 190255,
       "tono": "rosso"
      },
      {
       "label": "vicini (100-250 m)",
       "valore": 259977,
       "tono": "giallo"
      },
      {
       "label": "lontani (oltre 250 m)",
       "valore": 391748,
       "tono": "verde"
      }
     ]
    },
    {
     "tipo": "barre",
     "titolo": "Residenti senza il servizio a 15 minuti a piedi",
     "unita": "residenti",
     "nota": "Solo zone abitate (almeno 1.000 abitanti per km²).",
     "voci": [
      {
       "label": "salute",
       "valore": 5340,
       "tono": "rosso"
      },
      {
       "label": "scuole",
       "valore": 2529,
       "tono": "rosso"
      },
      {
       "label": "negozi e attività commerciali",
       "valore": 347,
       "tono": "rosso"
      },
      {
       "label": "fermate",
       "valore": 100,
       "tono": "rosso"
      },
      {
       "label": "verde",
       "valore": 0,
       "tono": "rosso"
      }
     ]
    }
   ],
   "calcolo": [
    "Per ogni sezione di censimento si contano i servizi raggiungibili a piedi in 5, 10 e 15 minuti.",
    "I tipi di servizio sono cinque, contati separatamente: scuole, salute, negozi, fermate, verde.",
    "Si cammina sulla rete stradale reale (OpenStreetMap), a 80 m al minuto.",
    "Residenti dal censimento ISTAT 2021; le zone con meno di 1.000 abitanti per km² sono grigie e contate a parte.",
    "Si è esposti se il centro della sezione è a meno di 100 m da una strada molto trafficata."
   ],
   "criteri": [
    [
     "Tempi a piedi",
     "5, 10 e 15 minuti"
    ],
    [
     "Velocità a piedi",
     "80 m al minuto (4,8 km/h)"
    ],
    [
     "Zona poco abitata",
     "sotto 1.000 ab/km² (prove con 500 e 2.000)"
    ],
    [
     "Sezioni di Torino",
     "4.044"
    ],
    [
     "Residenti",
     "848.748"
    ],
    [
     "Punti nuovi per gruppo",
     "fino a 5"
    ],
    [
     "Strada molto trafficata",
     "almeno 11.720 veicoli al giorno"
    ],
    [
     "Esposto al traffico",
     "a meno di 100 m dalla strada"
    ]
   ],
   "limiti": [
    "Solo Torino: in cintura il catalogo dei servizi manca, quindi «zero» spesso vuol dire dato mancante.",
    "Si conta se un servizio c'è, non quanto è grande né se ha posto. Le fermate usano l'orario programmato: niente ritardi né affollamento.",
    "I punti nuovi sono ipotesi: non tengono conto di costi, spazi liberi o permessi.",
    "Il traffico è una stima e sostituisce rumore e smog, che non misuriamo."
   ],
   "english": [
    "Question: how many Turin residents lack schools, health, shops, stops or green space within 15 minutes on foot?",
    "Answer: 10,919 residents (1.3%) lack at least one of the 5 services; 362 in inhabited areas lack three or more.",
    "Limit: only Turin is covered, because the service catalogue is missing for the surrounding towns."
   ],
   "mappa": {
    "id": "faseb",
    "nota": "Nella mappa, tema \"Dove mancano i servizi\": all'apertura quanti servizi mancano in ogni zona (0-5, zone poco abitate in grigio); nel menu un servizio alla volta, con i punti dove aggiungerne uno."
   }
  },
  "forma_en": {
   "etichetta": "ESTIMATED",
   "titolo": "Within 15 minutes almost everyone has the services; within 5 minutes far fewer do",
   "domanda": "How many people in Turin have the services within 5, 10 and 15 minutes on foot, and how many live on a busy road?",
   "numero": {
    "valore": 99.2,
    "unita": "%",
    "testo": "of residents of inhabited areas have all 5 services within a 15-minute walk"
   },
   "principale": {
    "tipo": "pila100",
    "titolo": "Residents by services reached on foot",
    "unita": "%",
    "nota": "Each bar is a walking time: 100% of residents of inhabited areas (at least 1,000 inhabitants per km²).",
    "righe": [
     {
      "label": "5 minutes",
      "voci": [
       {
        "label": "all 5 services",
        "valore": 68.3,
        "tono": "verde"
       },
       {
        "label": "4 services",
        "valore": 22.2,
        "tono": "giallo"
       },
       {
        "label": "3 or fewer",
        "valore": 9.5,
        "tono": "rosso"
       }
      ]
     },
     {
      "label": "10 minutes",
      "voci": [
       {
        "label": "all 5 services",
        "valore": 96.8,
        "tono": "verde"
       },
       {
        "label": "4 services",
        "valore": 2.4,
        "tono": "giallo"
       },
       {
        "label": "3 or fewer",
        "valore": 0.8,
        "tono": "rosso"
       }
      ]
     },
     {
      "label": "15 minutes",
      "voci": [
       {
        "label": "all 5 services",
        "valore": 99.2,
        "tono": "verde"
       },
       {
        "label": "4 services",
        "valore": 0.6,
        "tono": "giallo"
       },
       {
        "label": "3 or fewer",
        "valore": 0.2,
        "tono": "rosso"
       }
      ]
     }
    ]
   },
   "punti": [
    "Within 5 minutes only 68.3% of residents have all 5 services; within 10 minutes 96.8%.",
    "190,255 residents (22.6%) live less than 100 m from a very busy road.",
    "The 362 residents without 3 or more services live in 5 hillside sections: where really everything is missing."
   ],
   "altri": [
    {
     "tipo": "barre",
     "titolo": "Residents by distance from a very busy road",
     "unita": "residents",
     "nota": "Distance from the centre of the census section. Very busy road: at least 11,720 vehicles a day. Weak estimate: the model is off by ±38% in half of the cases.",
     "voci": [
      {
       "label": "exposed (less than 100 m)",
       "valore": 190255,
       "tono": "rosso"
      },
      {
       "label": "close (100-250 m)",
       "valore": 259977,
       "tono": "giallo"
      },
      {
       "label": "far (over 250 m)",
       "valore": 391748,
       "tono": "verde"
      }
     ]
    },
    {
     "tipo": "barre",
     "titolo": "Residents without the service within a 15-minute walk",
     "unita": "residents",
     "nota": "Inhabited areas only (at least 1,000 inhabitants per km²).",
     "voci": [
      {
       "label": "health",
       "valore": 5340,
       "tono": "rosso"
      },
      {
       "label": "schools",
       "valore": 2529,
       "tono": "rosso"
      },
      {
       "label": "shops and commercial activities",
       "valore": 347,
       "tono": "rosso"
      },
      {
       "label": "public transport stops",
       "valore": 100,
       "tono": "rosso"
      },
      {
       "label": "green space",
       "valore": 0,
       "tono": "rosso"
      }
     ]
    }
   ],
   "calcolo": [
    "For each census section we count the services reachable on foot in 5, 10 and 15 minutes.",
    "There are five types of service, counted separately: schools, health, shops, stops, green space.",
    "Walking follows the real street network (OpenStreetMap), at 80 m per minute.",
    "Residents come from the ISTAT 2021 census; areas with fewer than 1,000 inhabitants per km² are shown in grey and counted separately.",
    "A section is exposed if its centre is less than 100 m from a very busy road."
   ],
   "criteri": [
    [
     "Walking times",
     "5, 10 and 15 minutes"
    ],
    [
     "Walking speed",
     "80 m per minute (4.8 km/h)"
    ],
    [
     "Sparsely inhabited area",
     "under 1,000 inh/km² (tested with 500 and 2,000)"
    ],
    [
     "Sections in Turin",
     "4,044"
    ],
    [
     "Residents",
     "848,748"
    ],
    [
     "New points per group",
     "up to 5"
    ],
    [
     "Very busy road",
     "at least 11,720 vehicles a day"
    ],
    [
     "Exposed to traffic",
     "less than 100 m from the road"
    ]
   ],
   "limiti": [
    "Turin only: the service catalogue is missing for the surrounding towns, so “zero” often means missing data.",
    "We count whether a service exists, not how big it is or whether it has room. Stops use the scheduled timetable: no delays and no crowding.",
    "New points are hypotheses: they ignore costs, free space and permits.",
    "Traffic is an estimate standing in for noise and smog, which we do not measure."
   ],
   "mappa": {
    "id": "faseb",
    "nota": "Nella mappa, tema \"Dove mancano i servizi\": all'apertura quanti servizi mancano in ogni zona (0-5, zone poco abitate in grigio); nel menu un servizio alla volta, con i punti dove aggiungerne uno."
   }
  },
  "numero_pubblico": 1,
  "_nome": "risultato1_riepilogo_mappa.json"
 },
 {
  "risultato": "4",
  "titolo": "Puntualità e attese",
  "tag": "MISURATO",
  "stato": "Fatto",
  "in_breve": "L'orario alla fermata promette un passaggio ogni tot minuti. Quanto spesso i mezzi GTT arrivano davvero in ritardo, o a coppie lasciando un buco?",
  "domanda": "Quanto spesso i mezzi GTT arrivano in ritardo, e quanto spesso sulle linee frequenti arrivano a grappolo o lasciano buchi? E quanto si aspetta davvero alla fermata, rispetto a quello che promette l'orario?",
  "numero_chiave": {
   "valore": 14.1,
   "unita": "%",
   "testo": "dei passaggi nei giorni feriali arriva con più di 5 minuti di ritardo"
  },
  "racconto": "Una delle direzioni del progetto: confrontare l'orario promesso con quello reale, usando le posizioni e i ritardi dei mezzi che il Raspberry Pi del progetto raccoglie ogni minuto.",
  "risposta": [
   "Nei giorni feriali il 14,1% dei passaggi arriva con più di 5 minuti di ritardo; il sabato il 16,8%.",
   "Sulle linee frequenti il 20,9% delle coppie di mezzi consecutivi arriva a grappolo o lascia un buco.",
   "Il problema più comune è l'anticipo: il 37,9% dei passaggi feriali arriva più di un minuto prima dell'orario.",
   "Il feed in tempo reale di GTT, che usavamo prima, dava il 5,4% in ritardo invece del 14,1%: smette di aggiornare la fermata all'orario previsto e così sottostima i ritardi.",
   "Oltre 10 minuti: 5,44% nei feriali. GTT dichiara il 2,3% per il 2025: il suo metodo non è pubblicato; noi misuriamo a ogni fermata con il GPS, su pochi giorni.",
   "Non è la stessa misura: GTT fa la media dell'anno intero, estate e sere comprese, su tutte le linee, con un metodo che non pubblica; noi misuriamo pochi giorni di ottobre, solo le linee urbane, dalle 5 a mezzanotte.",
   "Il ritardo cresce lungo la corsa: alla prima fermata è 3,92%, a metà corsa 5,24%, a ogni fermata 5,49%, fuori dalle ore di punta 5,30% (media della settimana).",
   "Tutte e due le misure dicono che i ritardi gravi sono una piccola parte dei passaggi: tra 2,3% e 5,5%.",
   "Tram e bus: in ritardo oltre 5 minuti il 14,4% dei passaggi dei tram e il 14% dei bus (feriale).",
   "Linee utili (quelle che toccano più zone affollate): in ritardo oltre 5 minuti il 15,5% dei passaggi, contro l'11,4% delle altre linee (feriale).",
   "Attesa: Nei giorni feriali, sulle linee frequenti, l'orario promette un'attesa media di 4,7 minuti; quella reale è tra 6,3 e 7,1 minuti.",
   "Sono da 1,6 a 2,4 minuti in più a ogni attesa: almeno il 34% oltre la promessa.",
   "La linea con più attesa in più è la 61 (3,2 minuti in più, stima bassa).",
   "Attesa alla fermata sulle linee frequenti (feriale): tram, promessa 4,5 min, in più 1,8-2,4 min; bus, promessa 5,6 min, in più 1,1-2,4 min."
  ],
  "grafici": [
   {
    "tipo": "pila",
    "titolo": "Come arrivano i mezzi nei giorni feriali",
    "unita": "%",
    "voci": [
     {
      "label": "in anticipo (oltre 1 min)",
      "valore": 37.9
     },
     {
      "label": "puntuali (da -1 a +5 min)",
      "valore": 48.0,
      "tono": "verde"
     },
     {
      "label": "in ritardo (oltre 5 min)",
      "valore": 14.1,
      "tono": "rosso"
     }
    ]
   },
   {
    "tipo": "barre",
    "titolo": "Passaggi in ritardo oltre 5 minuti, per fascia oraria (feriale)",
    "unita": "%",
    "voci": [
     {
      "label": "punta del mattino (7-9)",
      "valore": 12.3,
      "tono": "rosso"
     },
     {
      "label": "giorno (9-16)",
      "valore": 15.2,
      "tono": "rosso"
     },
     {
      "label": "punta della sera (16-19)",
      "valore": 16.8,
      "tono": "rosso"
     },
     {
      "label": "sera (19-24)",
      "valore": 15.6,
      "tono": "rosso"
     },
     {
      "label": "notte e primo mattino (fino alle 7, dati parziali)",
      "valore": 5.7,
      "tono": "rosso"
     }
    ]
   },
   {
    "tipo": "barre",
    "titolo": "Passaggi in ritardo oltre 5 minuti, per tipo di giorno",
    "unita": "%",
    "voci": [
     {
      "label": "feriale",
      "valore": 14.1,
      "tono": "rosso"
     },
     {
      "label": "sabato",
      "valore": 16.8,
      "tono": "rosso"
     },
     {
      "label": "domenica",
      "valore": 12.0,
      "tono": "rosso"
     }
    ]
   },
   {
    "tipo": "barre",
    "titolo": "Le 10 linee più in ritardo (feriale)",
    "unita": "%",
    "nota": "Solo linee ordinarie (nome di sole cifre) con almeno 2000 passaggi osservati. Clicca una linea per vederla nella mappa.",
    "voci": [
     {
      "label": "linea 17",
      "valore": 38.1,
      "link": "mappa_torino.html#tema=puntualita&linea=17&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 6",
      "valore": 36.7,
      "link": "mappa_torino.html#tema=puntualita&linea=6&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 19",
      "valore": 30.1,
      "link": "mappa_torino.html#tema=puntualita&linea=19&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 68",
      "valore": 26.9,
      "link": "mappa_torino.html#tema=puntualita&linea=68&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 33",
      "valore": 26.2,
      "link": "mappa_torino.html#tema=puntualita&linea=33&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 66",
      "valore": 25.9,
      "link": "mappa_torino.html#tema=puntualita&linea=66&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 61",
      "valore": 23.1,
      "link": "mappa_torino.html#tema=puntualita&linea=61&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 4",
      "valore": 22.7,
      "link": "mappa_torino.html#tema=puntualita&linea=4&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 72",
      "valore": 22.2,
      "link": "mappa_torino.html#tema=puntualita&linea=72&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 52",
      "valore": 19.7,
      "link": "mappa_torino.html#tema=puntualita&linea=52&ora=8",
      "tono": "rosso"
     }
    ]
   },
   {
    "tipo": "barre",
    "titolo": "Le 10 linee più irregolari (feriale): grappolo + buco",
    "unita": "%",
    "nota": "Solo linee frequenti (un mezzo ogni 15 minuti o meno) con almeno 100 coppie osservate. Clicca una linea per vederla nella mappa.",
    "voci": [
     {
      "label": "linea 14",
      "valore": 42.4,
      "link": "mappa_torino.html#tema=puntualita&linea=14&ora=8"
     },
     {
      "label": "linea 30",
      "valore": 41.7,
      "link": "mappa_torino.html#tema=puntualita&linea=30&ora=8"
     },
     {
      "label": "linea 4",
      "valore": 40.1,
      "link": "mappa_torino.html#tema=puntualita&linea=4&ora=8"
     },
     {
      "label": "linea 45",
      "valore": 31.5,
      "link": "mappa_torino.html#tema=puntualita&linea=45&ora=8"
     },
     {
      "label": "linea 17",
      "valore": 31.0,
      "link": "mappa_torino.html#tema=puntualita&linea=17&ora=8"
     },
     {
      "label": "linea 29",
      "valore": 28.8,
      "link": "mappa_torino.html#tema=puntualita&linea=29&ora=8"
     },
     {
      "label": "linea 61",
      "valore": 27.2,
      "link": "mappa_torino.html#tema=puntualita&linea=61&ora=8"
     },
     {
      "label": "linea 43",
      "valore": 27.0,
      "link": "mappa_torino.html#tema=puntualita&linea=43&ora=8"
     },
     {
      "label": "linea 68",
      "valore": 23.4,
      "link": "mappa_torino.html#tema=puntualita&linea=68&ora=8"
     },
     {
      "label": "linea 13",
      "valore": 23.1,
      "link": "mappa_torino.html#tema=puntualita&linea=13&ora=8"
     }
    ]
   },
   {
    "tipo": "barre",
    "titolo": "Noi e GTT: passaggi in ritardo oltre 10 minuti",
    "unita": "%",
    "nota": "Barre = media della settimana (feriale 5 : sabato 1 : domenica 1). Nei feriali: a ogni fermata 5,44%, alla prima fermata 3,86%, a metà corsa 5,29%, fuori punta 5,27%. GTT: anno 2025, tutte le linee, metodo non pubblicato.",
    "voci": [
     {
      "label": "GTT (2025, anno intero)",
      "valore": 2.3
     },
     {
      "label": "noi, a ogni fermata",
      "valore": 5.49,
      "tono": "rosso"
     },
     {
      "label": "noi, solo alla prima fermata",
      "valore": 3.92,
      "tono": "rosso"
     },
     {
      "label": "noi, solo a metà corsa",
      "valore": 5.24,
      "tono": "rosso"
     },
     {
      "label": "noi, fuori dalle ore di punta",
      "valore": 5.3,
      "tono": "rosso"
     }
    ]
   },
   {
    "tipo": "barre",
    "titolo": "Tram contro bus (feriale)",
    "unita": "%",
    "nota": "Tram: 195.848 passaggi; bus: 748.428.",
    "voci": [
     {
      "label": "tram: in ritardo oltre 5 min",
      "valore": 14.4,
      "tono": "rosso"
     },
     {
      "label": "bus: in ritardo oltre 5 min",
      "valore": 14.0,
      "tono": "rosso"
     },
     {
      "label": "tram: in ritardo oltre 10 min",
      "valore": 5.66,
      "tono": "rosso"
     },
     {
      "label": "bus: in ritardo oltre 10 min",
      "valore": 5.38,
      "tono": "rosso"
     },
     {
      "label": "tram: a grappolo o con un buco",
      "valore": 26.7
     },
     {
      "label": "bus: a grappolo o con un buco",
      "valore": 17.1
     }
    ]
   },
   {
    "tipo": "barre",
    "titolo": "Ritardo a fine corsa (feriale)",
    "unita": "min",
    "nota": "Ritardo mediano alle ultime 3 fermate della corsa, in minuti. Solo linee ordinarie con almeno 100 passaggi di fine corsa. I minuti ogni 10 km (ritardo diviso la lunghezza della corsa) sono nel rapporto: per km le linee corte vengono premiate. Clicca una linea per vederla nella mappa: la mappa si apre alle 8 di un feriale.",
    "voci": [
     {
      "label": "linea 19 (5,4 min ogni 10 km)",
      "valore": 3.2,
      "link": "mappa_torino.html#tema=puntualita&linea=19&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 4 (2,2 min ogni 10 km)",
      "valore": 3.2,
      "link": "mappa_torino.html#tema=puntualita&linea=4&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 17 (1,7 min ogni 10 km)",
      "valore": 2.9,
      "link": "mappa_torino.html#tema=puntualita&linea=17&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 6 (6,2 min ogni 10 km)",
      "valore": 2.6,
      "link": "mappa_torino.html#tema=puntualita&linea=6&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 33 (2 min ogni 10 km)",
      "valore": 2.3,
      "link": "mappa_torino.html#tema=puntualita&linea=33&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 68 (1,6 min ogni 10 km)",
      "valore": 1.8,
      "link": "mappa_torino.html#tema=puntualita&linea=68&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 44 (1,2 min ogni 10 km)",
      "valore": 1.6,
      "link": "mappa_torino.html#tema=puntualita&linea=44&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 60 (2,2 min ogni 10 km)",
      "valore": 1.5,
      "link": "mappa_torino.html#tema=puntualita&linea=60&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 132 (1,8 min ogni 10 km)",
      "valore": 1.5,
      "link": "mappa_torino.html#tema=puntualita&linea=132&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 61 (1,3 min ogni 10 km)",
      "valore": 1.4,
      "link": "mappa_torino.html#tema=puntualita&linea=61&ora=8",
      "tono": "rosso"
     }
    ]
   },
   {
    "tipo": "barre",
    "titolo": "Linee utili contro altre (feriale)",
    "unita": "%",
    "nota": "Linee utili = le 54 che toccano più delle zone dove arriva più gente per km² (Risultato 3). Passaggi: 623.308 sulle utili, 320.968 sulle altre.",
    "voci": [
     {
      "label": "linee utili: in ritardo oltre 5 min",
      "valore": 15.5,
      "tono": "rosso"
     },
     {
      "label": "altre linee: in ritardo oltre 5 min",
      "valore": 11.4,
      "tono": "rosso"
     },
     {
      "label": "linee utili: a grappolo o con un buco",
      "valore": 21.9
     },
     {
      "label": "altre linee: a grappolo o con un buco",
      "valore": 17.2
     }
    ]
   },
   {
    "tipo": "barre",
    "titolo": "Attesa media alla fermata per fascia oraria (feriale)",
    "unita": "min",
    "nota": "Barra chiara = attesa promessa, barra scura = attesa reale (stima bassa).",
    "voci": [
     {
      "label": "punta del mattino (7-9)",
      "valore": 5.85,
      "prima": 4.53
     },
     {
      "label": "giorno (9-16)",
      "valore": 5.26,
      "prima": 3.75
     },
     {
      "label": "punta della sera (16-19)",
      "valore": 6.54,
      "prima": 4.44
     },
     {
      "label": "sera (19-24)",
      "valore": 9.65,
      "prima": 8.2
     }
    ]
   },
   {
    "tipo": "barre",
    "titolo": "Minuti in più di attesa, per fascia oraria (feriale)",
    "unita": "min",
    "forbice": true,
    "nota": "Barra chiara = stima bassa, barra scura = stima alta.",
    "voci": [
     {
      "label": "punta del mattino (7-9)",
      "valore": 1.65,
      "prima": 1.31
     },
     {
      "label": "giorno (9-16)",
      "valore": 2.96,
      "prima": 1.51
     },
     {
      "label": "punta della sera (16-19)",
      "valore": 2.42,
      "prima": 2.1
     },
     {
      "label": "sera (19-24)",
      "valore": 1.58,
      "prima": 1.45
     }
    ]
   },
   {
    "tipo": "barre",
    "titolo": "Le 10 linee con più attesa in più (feriale, stima bassa)",
    "unita": "min",
    "nota": "Solo linee con almeno 30 intervalli osservati.",
    "voci": [
     {
      "label": "linea 61",
      "valore": 3.2
     },
     {
      "label": "linea 33",
      "valore": 2.2
     },
     {
      "label": "linea 4",
      "valore": 2.2
     },
     {
      "label": "linea 46",
      "valore": 1.9
     },
     {
      "label": "linea 15",
      "valore": 1.6
     },
     {
      "label": "linea 16 CD",
      "valore": 1.6
     },
     {
      "label": "linea 2",
      "valore": 1.4
     },
     {
      "label": "linea 62",
      "valore": 1.2
     },
     {
      "label": "linea 3",
      "valore": 1.2
     },
     {
      "label": "linea 56",
      "valore": 1.0
     }
    ]
   }
  ],
  "metodo": [
   "Il Raspberry Pi registra ogni minuto le posizioni GPS dei mezzi GTT.",
   "Per ogni corsa e fermata si prende l'istante in cui il GPS del mezzo passa a meno di 60 metri dalla fermata e lo si confronta con l'orario ufficiale (GTFS).",
   "Classi: in anticipo sotto -1 minuto, puntuale da -1 a +5, in ritardo oltre +5.",
   "Regolarità: per due mezzi consecutivi della stessa linea alla stessa fermata, \"grappolo\" se l'intervallo vero è meno della metà di quello previsto, \"buco\" se è più del doppio. Solo linee con un mezzo ogni 15 minuti o meno."
  ],
  "parametri": [
   [
    "Periodo",
    "2026-10-10 - 2026-10-20"
   ],
   [
    "Passaggi con GPS valido",
    "1.300.434 (78,3% di quelli programmati dalle corse viste)"
   ],
   [
    "Soglia ritardo",
    "5 min"
   ],
   [
    "Soglia anticipo",
    "-1 min"
   ],
   [
    "Distanza dalla fermata",
    "entro 60 m"
   ]
  ],
  "limiti": [
   "Pochi giorni (6 feriali, 2 sabati, 1 domeniche), e non tutti interi: sabato 10 dalle 15, lunedì 12 dalle 12, martedì 13 con buchi il pomeriggio e la sera, domenica 18 fino alle 9:30 (poi guasto del feed GTT). Ogni giorno conta con le ore che hanno dati.",
   "La raccolta si ferma a mezzanotte e riparte verso le 5: la notte non è misurata.",
   "Il GPS copre solo le linee urbane (circa 90): le extraurbane non ci sono mai. Anche sulle linee coperte alcune corse non sono mai viste dal GPS: se erano saltate davvero, la puntualità reale è peggiore e i buchi sono più di quelli contati.",
   "Il GPS c'è per circa il 78% dei passaggi delle corse viste; le corse mai viste dal GPS non si contano.",
   "Distanza di 60 metri dalla fermata: un mezzo fermo poco prima conta come arrivato poco dopo.",
   "Dice quanto spesso c'è ritardo, non quante persone aspettano né quanto erano pieni i mezzi.",
   "Arrivi misurati con il GPS dei mezzi (a meno di 60 metri dalla fermata); il vecchio feed GTT, controllato col GPS, dava una differenza tipica di 0,5 minuti.",
   "Solo le linee urbane viste dal GPS; niente extraurbane e niente notte.",
   "Le corse mancanti rendono il risultato una forbice, non un numero solo.",
   "Vale per chi arriva alla fermata senza guardare orario o app: è il caso tipico delle linee frequenti, non di quelle rare (per quelle conta la puntualità, risultato 4).",
   "Pochi giorni (gli stessi del risultato 4, non tutti interi): va rifatto con più settimane di dati. La domenica le linee frequenti sono poche: troppo pochi dati per dare un numero."
  ],
  "in_english": [
   "Question: how often do GTT vehicles arrive late, and how often do frequent lines bunch together or leave gaps?",
   "On weekdays 14.1% of departures arrive more than 5 minutes late; on Saturdays 16.8%. On frequent lines 20.9% of consecutive pairs of vehicles bunch together or leave a gap.",
   "The most common problem is early arrival: 37.9% of weekday departures arrive more than one minute before the timetable.",
   "Limits: only 6 weekdays, 2 Saturdays and 1 Sundays of data, some of them partial; the night is not measured.",
   "Arrivals are now measured with the vehicles' GPS; the GTT real-time feed we used before gave 5.4% late instead of 14.1% because it stops updating a stop at its scheduled time, so it underestimates delays.",
   "More than 10 minutes late: 5.44% of weekday departures. GTT reports 2.3% for 2025: its method is not published; we measure at every stop with GPS, over a few days.",
   "Why our number differs from GTT's 2.3% (more than 10 minutes late, 2025): GTT averages the whole year on all lines with an unpublished method; we measure a few October days on urban lines. At the first stop of the trip we get 3.92%, at every stop 5.49% (weekly average).",
   "Trams vs buses (weekdays): 14.4% of tram departures and 14.0% of bus departures are more than 5 minutes late.",
   "Delay at the end of the trip (median, last stops): highest on line 19 (3.2 minutes).",
   "Useful lines (touching the busiest zones per km2): 15.5% of departures more than 5 minutes late, other lines 11.4% (weekdays).",
   "On weekdays the timetable promises an average wait of 4.7 minutes; the real one is between 6.3 and 7.1 minutes. That is 1.6 to 2.4 minutes more per wait, at least 34% above the promise.",
   "Limits: only 6 weekdays of data so far; real arrivals are measured with the vehicles' GPS (within 60 metres of the stop); the night is not included.",
   "Waiting time on frequent lines (weekdays): trams promise 4.5 min, 1.8-2.4 min more in reality; buses 5.6 min, 1.1-2.4 min more."
  ],
  "mappa": {
   "id": "puntualita",
   "tema": "Puntualità delle linee",
   "nota": "Nella mappa, tema «Puntualità delle linee»: ogni linea colorata per ritardo nell'ora scelta con il cursore."
  },
  "fonti": [
   "docs/R4_puntualita.md",
   "docs/rapporti/RAPPORTO_RISULTATO4.txt",
   "scripts/27_risultato4_regolarita.py",
   "docs/rapporti/RAPPORTO_RISULTATO9_ATTESA.txt",
   "scripts/70_risultato9_attesa.py"
  ],
  "generato": "2026-10-23T13:30:39+00:00",
  "avviso": [
   "Dati [MISURATO] — pochi giorni",
   "Arrivi misurati con il GPS dei mezzi GTT raccolto dal Raspberry Pi, 2026-10-10 - 2026-10-20: il GPS c'è per il 78% dei passaggi programmati delle corse viste (prima si usava il feed GTT, che sottostima i ritardi: confronto nella scheda). Giorni non tutti interi e solo linee urbane viste dal GPS: vedi i limiti."
  ],
  "scenari": [
   {
    "nome": "Feriale (6 giorni, 944.276 passaggi)",
    "numeri": [
     {
      "label": "Passaggi in ritardo oltre 5 min",
      "prima": null,
      "dopo": 14.1,
      "unita": "%"
     },
     {
      "label": "Coppie di bus a grappolo o con un buco (linee frequenti)",
      "prima": null,
      "dopo": 20.9,
      "unita": "%"
     },
     {
      "label": "Ritardo mediano",
      "prima": null,
      "dopo": -0.1,
      "unita": "min"
     },
     {
      "label": "Passaggi in anticipo oltre 1 min",
      "prima": null,
      "dopo": 37.9,
      "unita": "%"
     },
     {
      "label": "Passaggi in ritardo oltre 10 min",
      "prima": null,
      "dopo": 5.44,
      "unita": "%"
     }
    ],
    "nota": "Molti passaggi risultano in anticipo perché l'orario ufficiale ha margini; un ritardo mediano negativo vuol dire 'di solito un po' prima'."
   },
   {
    "nome": "Sabato (2 giorni, 244.582 passaggi)",
    "numeri": [
     {
      "label": "Passaggi in ritardo oltre 5 min",
      "prima": null,
      "dopo": 16.8,
      "unita": "%"
     },
     {
      "label": "Coppie di bus a grappolo o con un buco (linee frequenti)",
      "prima": null,
      "dopo": 21.0,
      "unita": "%"
     },
     {
      "label": "Ritardo mediano",
      "prima": null,
      "dopo": 0.3,
      "unita": "min"
     },
     {
      "label": "Passaggi in anticipo oltre 1 min",
      "prima": null,
      "dopo": 34.3,
      "unita": "%"
     },
     {
      "label": "Passaggi in ritardo oltre 10 min",
      "prima": null,
      "dopo": 7.1,
      "unita": "%"
     }
    ]
   },
   {
    "nome": "Domenica (1 giorno, 111.576 passaggi)",
    "numeri": [
     {
      "label": "Passaggi in ritardo oltre 5 min",
      "prima": null,
      "dopo": 12.0,
      "unita": "%"
     },
     {
      "label": "Coppie di bus a grappolo o con un buco (linee frequenti)",
      "prima": null,
      "dopo": 18.5,
      "unita": "%"
     },
     {
      "label": "Ritardo mediano",
      "prima": null,
      "dopo": -0.1,
      "unita": "min"
     },
     {
      "label": "Passaggi in anticipo oltre 1 min",
      "prima": null,
      "dopo": 37.4,
      "unita": "%"
     },
     {
      "label": "Passaggi in ritardo oltre 10 min",
      "prima": null,
      "dopo": 4.11,
      "unita": "%"
     }
    ]
   },
   {
    "nome": "Feriale (6 giorni)",
    "numeri": [
     {
      "label": "Attesa media alla fermata, stima bassa",
      "prima": 4.73,
      "dopo": 6.35,
      "unita": "min"
     },
     {
      "label": "Attesa media alla fermata, stima alta",
      "prima": 4.73,
      "dopo": 7.14,
      "unita": "min"
     },
     {
      "label": "Corse programmate assenti dal GPS",
      "prima": null,
      "dopo": 13.3,
      "unita": "%"
     }
    ],
    "nota": "Prima = attesa promessa dall'orario, dopo = attesa reale stimata dai passaggi."
   },
   {
    "nome": "Sabato (2 giorni)",
    "numeri": [
     {
      "label": "Attesa media alla fermata, stima bassa",
      "prima": 4.75,
      "dopo": 6.88,
      "unita": "min"
     },
     {
      "label": "Attesa media alla fermata, stima alta",
      "prima": 4.75,
      "dopo": 6.98,
      "unita": "min"
     },
     {
      "label": "Corse programmate assenti dal GPS",
      "prima": null,
      "dopo": 7.8,
      "unita": "%"
     }
    ]
   }
  ],
  "forma": {
   "etichetta": "MISURATO",
   "titolo": "I ritardi gravi sono circa il 5% dei passaggi",
   "domanda": "Quanto spesso i mezzi GTT arrivano in ritardo o a coppie?",
   "numero": {
    "valore": 5.44,
    "unita": "%",
    "testo": "dei passaggi feriali arriva con oltre 10 minuti di ritardo"
   },
   "principale": {
    "tipo": "pila100",
    "titolo": "Come arrivano i mezzi",
    "unita": "%",
    "nota": "Ogni barra è un tipo di giorno: 100% dei passaggi.",
    "righe": [
     {
      "label": "feriale",
      "voci": [
       {
        "label": "in anticipo (oltre 1 minuto)",
        "valore": 37.9,
        "tono": "blu"
       },
       {
        "label": "puntuali",
        "valore": 48.0,
        "tono": "verde"
       },
       {
        "label": "ritardo da 5 a 10 minuti",
        "valore": 8.66,
        "tono": "giallo"
       },
       {
        "label": "ritardo oltre 10 minuti",
        "valore": 5.44,
        "tono": "rosso"
       }
      ]
     },
     {
      "label": "sabato",
      "voci": [
       {
        "label": "in anticipo (oltre 1 minuto)",
        "valore": 34.3,
        "tono": "blu"
       },
       {
        "label": "puntuali",
        "valore": 48.9,
        "tono": "verde"
       },
       {
        "label": "ritardo da 5 a 10 minuti",
        "valore": 9.7,
        "tono": "giallo"
       },
       {
        "label": "ritardo oltre 10 minuti",
        "valore": 7.1,
        "tono": "rosso"
       }
      ]
     },
     {
      "label": "domenica",
      "voci": [
       {
        "label": "in anticipo (oltre 1 minuto)",
        "valore": 37.4,
        "tono": "blu"
       },
       {
        "label": "puntuali",
        "valore": 50.6,
        "tono": "verde"
       },
       {
        "label": "ritardo da 5 a 10 minuti",
        "valore": 7.89,
        "tono": "giallo"
       },
       {
        "label": "ritardo oltre 10 minuti",
        "valore": 4.11,
        "tono": "rosso"
       }
      ]
     }
    ]
   },
   "punti": [
    "Oltre 10 minuti di ritardo: 5,4% dei passaggi a ogni fermata, 3,9% se si guarda solo la partenza.",
    "La linea più in ritardo è la 17: 38,1% dei passaggi feriali oltre 5 minuti.",
    "I tram arrivano più a grappolo dei bus: 26,7% delle coppie di mezzi contro 17,1% (feriale)."
   ],
   "altri": [
    {
     "tipo": "barre",
     "titolo": "Noi e GTT: passaggi in ritardo oltre 10 minuti",
     "unita": "%",
     "nota": "Barre = media della settimana (feriale 5 : sabato 1 : domenica 1). Nei feriali: a ogni fermata 5,44%, alla prima fermata 3,86%, a metà corsa 5,29%, fuori punta 5,27%. GTT: anno 2025, tutte le linee, metodo non pubblicato.",
     "voci": [
      {
       "label": "GTT (2025, anno intero)",
       "valore": 2.3
      },
      {
       "label": "noi, a ogni fermata",
       "valore": 5.49,
       "tono": "rosso"
      },
      {
       "label": "noi, solo alla prima fermata",
       "valore": 3.92,
       "tono": "rosso"
      },
      {
       "label": "noi, solo a metà corsa",
       "valore": 5.24,
       "tono": "rosso"
      },
      {
       "label": "noi, fuori dalle ore di punta",
       "valore": 5.3,
       "tono": "rosso"
      }
     ]
    },
    {
     "tipo": "linea",
     "titolo": "Ritardo oltre 5 minuti, per fascia oraria (feriale)",
     "unita": "%",
     "categorie": [
      "punta mattino (7-9)",
      "giorno (9-16)",
      "punta sera (16-19)",
      "sera (19-24)"
     ],
     "serie": [
      {
       "label": "passaggi in ritardo",
       "valori": [
        12.3,
        15.2,
        16.8,
        15.6
       ]
      }
     ]
    }
   ],
   "calcolo": [
    "Il Raspberry Pi registra ogni minuto la posizione GPS dei mezzi GTT.",
    "Il passaggio è l'istante in cui il GPS è a meno di 60 metri dalla fermata.",
    "Il ritardo è quell'istante meno l'orario ufficiale.",
    "In anticipo oltre 1 minuto; in ritardo oltre 5 minuti.",
    "Grappolo: due mezzi attaccati. Buco: intervallo doppio del previsto. Solo linee frequenti."
   ],
   "criteri": [
    [
     "Periodo",
     "2026-10-10 - 2026-10-20"
    ],
    [
     "Passaggi con GPS valido",
     "1.300.434 (78,3% di quelli programmati dalle corse viste)"
    ],
    [
     "Soglia ritardo",
     "5 min"
    ],
    [
     "Soglia anticipo",
     "-1 min"
    ],
    [
     "Distanza dalla fermata",
     "entro 60 m"
    ]
   ],
   "limiti": [
    "Pochi giorni: 6 feriali, 2 sabati e 1 domenica, non tutti interi.",
    "Solo le linee urbane viste dal GPS, dalle 5 a mezzanotte.",
    "Il GPS copre circa il 78% dei passaggi programmati; le corse mai viste non si contano.",
    "Contiamo quanto spesso c'è ritardo, non quante persone aspettano."
   ],
   "english": [
    "Question: how often are GTT vehicles late or bunched? Answer: 5.4% of weekday departures are more than 10 minutes late.",
    "GTT reports 2.3% for 2025. Counting only the first stop we get 3.9%; the rest is season and method.",
    "Limit: only 6 weekdays, 2 Saturdays and 1 Sunday of data, urban lines only, no night."
   ],
   "mappa": {
    "id": "puntualita",
    "nota": "Nella mappa, tema «Puntualità delle linee»: ogni linea colorata per ritardo nell'ora scelta con il cursore."
   },
   "unita": {
    "tipo": "quadratini",
    "totale": 100,
    "colorati": 14,
    "didascalia": "Su 100 passaggi feriali, circa 14 arrivano con più di 5 minuti di ritardo (14,1%); con più di 10 minuti circa 5."
   },
   "confronto": [
    "GTT dichiara il 2,3% oltre 10 minuti nel 2025: media dell'anno, tutte le linee, metodo non pubblicato.",
    "Noi misuriamo pochi giorni di ottobre sulle linee urbane: 5,5% a ogni fermata, 3,9% alla partenza.",
    "Anche contando come GTT alla partenza troviamo il 3,9%; il resto della differenza è stagione e metodo."
   ],
   "extra": {
    "titolo": "Quanto si aspetta alla fermata",
    "punto": "Sulle linee frequenti si aspettano da 1,6 a 2,4 minuti in più di quanto promette l'orario (feriale).",
    "grafico": {
     "tipo": "barre",
     "titolo": "Attesa media alla fermata, per fascia oraria (feriale)",
     "unita": "min",
     "nota": "Barra chiara = attesa promessa, barra scura = attesa reale (stima bassa).",
     "voci": [
      {
       "label": "punta del mattino (7-9)",
       "valore": 5.85,
       "prima": 4.53
      },
      {
       "label": "giorno (9-16)",
       "valore": 5.26,
       "prima": 3.75
      },
      {
       "label": "punta della sera (16-19)",
       "valore": 6.54,
       "prima": 4.44
      },
      {
       "label": "sera (19-24)",
       "valore": 9.65,
       "prima": 8.2
      }
     ]
    }
   }
  },
  "forma_en": {
   "etichetta": "MEASURED",
   "titolo": "Serious delays are about 5% of stop arrivals",
   "domanda": "How often are GTT vehicles late or bunched together?",
   "numero": {
    "valore": 5.44,
    "unita": "%",
    "testo": "of weekday arrivals are more than 10 minutes late"
   },
   "principale": {
    "tipo": "pila100",
    "titolo": "How vehicles arrive",
    "unita": "%",
    "nota": "Each bar is a type of day: 100% of arrivals.",
    "righe": [
     {
      "label": "weekday",
      "voci": [
       {
        "label": "early (more than 1 minute)",
        "valore": 37.9,
        "tono": "blu"
       },
       {
        "label": "on time",
        "valore": 48.0,
        "tono": "verde"
       },
       {
        "label": "5 to 10 minutes late",
        "valore": 8.66,
        "tono": "giallo"
       },
       {
        "label": "more than 10 minutes late",
        "valore": 5.44,
        "tono": "rosso"
       }
      ]
     },
     {
      "label": "Saturday",
      "voci": [
       {
        "label": "early (more than 1 minute)",
        "valore": 34.3,
        "tono": "blu"
       },
       {
        "label": "on time",
        "valore": 48.9,
        "tono": "verde"
       },
       {
        "label": "5 to 10 minutes late",
        "valore": 9.7,
        "tono": "giallo"
       },
       {
        "label": "more than 10 minutes late",
        "valore": 7.1,
        "tono": "rosso"
       }
      ]
     },
     {
      "label": "Sunday",
      "voci": [
       {
        "label": "early (more than 1 minute)",
        "valore": 37.4,
        "tono": "blu"
       },
       {
        "label": "on time",
        "valore": 50.6,
        "tono": "verde"
       },
       {
        "label": "5 to 10 minutes late",
        "valore": 7.89,
        "tono": "giallo"
       },
       {
        "label": "more than 10 minutes late",
        "valore": 4.11,
        "tono": "rosso"
       }
      ]
     }
    ]
   },
   "punti": [
    "More than 10 minutes late: 5.4% of arrivals at every stop, 3.9% if we look only at departure.",
    "The line with the most delays is line 17: 38.1% of weekday arrivals more than 5 minutes late.",
    "Trams bunch more than buses: 26.7% of vehicle pairs versus 17.1% (weekday)."
   ],
   "altri": [
    {
     "tipo": "barre",
     "titolo": "Us and GTT: arrivals more than 10 minutes late",
     "unita": "%",
     "nota": "Bars = weekly average (weekday 5 : Saturday 1 : Sunday 1). On weekdays: at every stop 5.44%, at the first stop 3.86%, mid-trip 5.29%, off-peak 5.27%. GTT: year 2025, all lines, method not published.",
     "voci": [
      {
       "label": "GTT (2025, whole year)",
       "valore": 2.3
      },
      {
       "label": "us, at every stop",
       "valore": 5.49,
       "tono": "rosso"
      },
      {
       "label": "us, first stop only",
       "valore": 3.92,
       "tono": "rosso"
      },
      {
       "label": "us, mid-trip only",
       "valore": 5.24,
       "tono": "rosso"
      },
      {
       "label": "us, outside peak hours",
       "valore": 5.3,
       "tono": "rosso"
      }
     ]
    },
    {
     "tipo": "linea",
     "titolo": "Delay over 5 minutes, by time of day (weekday)",
     "unita": "%",
     "categorie": [
      "morning peak (7-9)",
      "daytime (9-16)",
      "evening peak (16-19)",
      "evening (19-24)"
     ],
     "serie": [
      {
       "label": "late arrivals",
       "valori": [
        12.3,
        15.2,
        16.8,
        15.6
       ]
      }
     ]
    }
   ],
   "calcolo": [
    "A Raspberry Pi records the GPS position of GTT vehicles every minute.",
    "An arrival is the moment the GPS is less than 60 metres from the stop.",
    "The delay is that moment minus the official timetable.",
    "Early: more than 1 minute; late: more than 5 minutes.",
    "Bunching: two vehicles right behind each other. Gap: an interval twice the planned one. Frequent lines only."
   ],
   "criteri": [
    [
     "Period",
     "2026-10-10 - 2026-10-20"
    ],
    [
     "Arrivals with a valid GPS fix",
     "1,300,434 (78.3% of those scheduled for the trips seen)"
    ],
    [
     "Delay threshold",
     "5 min"
    ],
    [
     "Earliness threshold",
     "-1 min"
    ],
    [
     "Distance from the stop",
     "within 60 m"
    ]
   ],
   "limiti": [
    "Few days: 6 weekdays, 2 Saturdays and 1 Sunday, not all complete.",
    "Urban lines seen by the GPS only, from 5 a.m. to midnight.",
    "The GPS covers about 78% of scheduled arrivals; trips never seen are not counted.",
    "We count how often there is a delay, not how many people are waiting."
   ],
   "mappa": {
    "id": "puntualita",
    "nota": "Nella mappa, tema «Puntualità delle linee»: ogni linea colorata per ritardo nell'ora scelta con il cursore."
   },
   "unita": {
    "tipo": "quadratini",
    "totale": 100,
    "colorati": 14,
    "didascalia": "Out of 100 weekday arrivals, about 14 are more than 5 minutes late (14.1%); more than 10 minutes late, about 5."
   },
   "confronto": [
    "GTT reports 2.3% over 10 minutes in 2025: yearly average, all lines, method not published.",
    "We measure a few days in October on urban lines: 5.5% at every stop, 3.9% at departure.",
    "Even counting at departure like GTT, we find 3.9%; the rest of the difference is season and method."
   ],
   "extra": {
    "titolo": "How long you wait at the stop",
    "punto": "On frequent lines you wait 1.6 to 2.4 minutes more than the timetable promises (weekday).",
    "grafico": {
     "tipo": "barre",
     "titolo": "Average wait at the stop, by time of day (weekday)",
     "unita": "min",
     "nota": "Light bar = promised wait, dark bar = actual wait (low estimate).",
     "voci": [
      {
       "label": "morning peak (7-9)",
       "valore": 5.85,
       "prima": 4.53
      },
      {
       "label": "daytime (9-16)",
       "valore": 5.26,
       "prima": 3.75
      },
      {
       "label": "evening peak (16-19)",
       "valore": 6.54,
       "prima": 4.44
      },
      {
       "label": "evening (19-24)",
       "valore": 9.65,
       "prima": 8.2
      }
     ]
    }
   }
  },
  "numero_pubblico": 2,
  "_nome": "risultato4_riepilogo_mappa.json"
 },
 {
  "risultato": "6",
  "titolo": "Parcheggi per lasciare l'auto",
  "tag": "STIMATO / MISURATO (dati scarsi)",
  "stato": "Aggiornato al 23/10/2026",
  "in_breve": "Dove lasciare l'auto prima di entrare in città e proseguire con i mezzi pubblici: come funzionano gli interscambi che ci sono, e dove mancano posti per le auto che entrano ogni mattina.",
  "domanda": "Dove mancano posti per lasciare l'auto prima di entrare in città, vicino a una fermata importante, per le auto che ogni mattina entrano a Torino?",
  "numero_chiave": {
   "valore": 179,
   "unita": "fermate",
   "testo": "su 274 fermate importanti fuori dal centro non hanno abbastanza posti adatti entro 400 m a piedi per le auto in entrata che passano accanto"
  },
  "risposta": [
   "Gli interscambi che ci sono: nei giorni misurati Stura: sempre quasi pieno: 80% di notte, 91% di giorno; Caio Mario: il valore non cambia (1%): forse il contatore è fermo; Sofia: è più pieno di notte che di giorno: 52% di notte, 31% di giorno; Venchi Unica: sempre intorno al 55%; Fermi non trasmette il riempimento [MISURATO, DATI SCARSI]. Pieni di giorno: 1 su 5.",
   "Ogni mattina entrano a Torino circa 87.200 auto [STIMATO, indagine sugli spostamenti 2022]; oggi il 5,8% di chi arriva in auto prosegue con un mezzo pubblico.",
   "Delle 274 fermate importanti fuori dal centro, 179 non hanno abbastanza posti adatti entro 400 m a piedi per le auto da fermare (68 non ne hanno nessuno).",
   "I punti dove servirebbe di più un parcheggio (posti che mancano, ordine di grandezza): 1. Santa Rita (Santa Rita), 2. Metro Massaua (Parella), 3. Ponte Cavalieri Templari (Moncalieri)."
  ],
  "grafici": [
   {
    "tipo": "profilo",
    "titolo": "Stura (589 posti): sempre quasi pieno: 80% di notte, 91% di giorno",
    "unita": "",
    "nota": "[MISURATO] 7 giorni validi; linea piena feriale, tratteggiata weekend [DATI SCARSI].",
    "serie": [
     {
      "label": "giorno feriale",
      "valori": [
       0.797,
       0.797,
       0.797,
       0.797,
       0.797,
       0.799,
       0.803,
       0.827,
       0.872,
       0.897,
       0.917,
       0.918,
       0.918,
       0.914,
       0.908,
       0.902,
       0.893,
       0.875,
       0.844,
       0.812,
       0.802,
       0.8,
       0.8,
       0.798
      ]
     },
     {
      "label": "weekend",
      "valori": [
       0.795,
       0.795,
       0.795,
       0.795,
       0.795,
       0.796,
       0.796,
       0.798,
       0.799,
       0.799,
       0.799,
       0.8,
       0.798,
       0.8,
       0.801,
       0.801,
       0.8,
       0.799,
       0.799,
       0.799,
       0.797,
       0.796,
       0.795,
       0.795
      ],
      "tratteggio": true
     }
    ]
   },
   {
    "tipo": "profilo",
    "titolo": "Venchi Unica (437 posti): sempre intorno al 55%",
    "unita": "",
    "nota": "[MISURATO] 7 giorni validi; linea piena feriale, tratteggiata weekend [DATI SCARSI].",
    "serie": [
     {
      "label": "giorno feriale",
      "valori": [
       0.532,
       0.533,
       0.533,
       0.533,
       0.532,
       0.53,
       0.531,
       0.524,
       0.528,
       0.55,
       0.552,
       0.548,
       0.549,
       0.547,
       0.546,
       0.543,
       0.538,
       0.529,
       0.517,
       0.505,
       0.512,
       0.516,
       0.52,
       0.529
      ]
     },
     {
      "label": "weekend",
      "valori": [
       0.47,
       0.478,
       0.485,
       0.488,
       0.489,
       0.489,
       0.49,
       0.489,
       0.481,
       0.469,
       0.456,
       0.449,
       0.451,
       0.452,
       0.453,
       0.45,
       0.45,
       0.447,
       0.45,
       0.45,
       0.452,
       0.453,
       0.458,
       0.48
      ],
      "tratteggio": true
     }
    ]
   },
   {
    "tipo": "profilo",
    "titolo": "Caio Mario (418 posti): il valore non cambia (1%): forse il contatore è fermo",
    "unita": "",
    "nota": "[MISURATO] 7 giorni validi; linea piena feriale, tratteggiata weekend [DATI SCARSI].",
    "serie": [
     {
      "label": "giorno feriale",
      "valori": [
       0.017,
       0.01,
       0.01,
       0.01,
       0.01,
       0.01,
       0.009,
       0.009,
       0.009,
       0.009,
       0.009,
       0.009,
       0.009,
       0.009,
       0.01,
       0.011,
       0.011,
       0.011,
       0.01,
       0.011,
       0.012,
       0.012,
       0.013,
       0.013
      ]
     },
     {
      "label": "weekend",
      "valori": [
       0.025,
       0.017,
       0.017,
       0.017,
       0.017,
       0.017,
       0.017,
       0.016,
       0.018,
       0.019,
       0.019,
       0.021,
       0.021,
       0.022,
       0.021,
       0.024,
       0.024,
       0.027,
       0.029,
       0.03,
       0.034,
       0.033,
       0.033,
       0.035
      ],
      "tratteggio": true
     }
    ]
   },
   {
    "tipo": "profilo",
    "titolo": "Sofia (272 posti): è più pieno di notte che di giorno: 52% di notte, 31% di giorno",
    "unita": "",
    "nota": "[MISURATO] 7 giorni validi; linea piena feriale, tratteggiata weekend [DATI SCARSI].",
    "serie": [
     {
      "label": "giorno feriale",
      "valori": [
       0.521,
       0.522,
       0.522,
       0.523,
       0.524,
       0.515,
       0.494,
       0.447,
       0.406,
       0.365,
       0.311,
       0.295,
       0.302,
       0.31,
       0.311,
       0.313,
       0.31,
       0.342,
       0.379,
       0.42,
       0.453,
       0.47,
       0.493,
       0.505
      ]
     },
     {
      "label": "weekend",
      "valori": [
       0.507,
       0.51,
       0.512,
       0.514,
       0.516,
       0.513,
       0.504,
       0.489,
       0.471,
       0.44,
       0.403,
       0.385,
       0.394,
       0.396,
       0.396,
       0.393,
       0.394,
       0.395,
       0.407,
       0.416,
       0.43,
       0.436,
       0.446,
       0.495
      ],
      "tratteggio": true
     }
    ]
   },
   {
    "tipo": "pila",
    "titolo": "Fermate importanti e posti adatti",
    "unita": "fermate",
    "nota": "Posti adatti entro 400 m a piedi confrontati con le auto da fermare (auto che passano × 5,8%).",
    "voci": [
     {
      "label": "nessun parcheggio",
      "valore": 68,
      "tono": "rosso"
     },
     {
      "label": "posti insufficienti",
      "valore": 111,
      "tono": "arancio"
     },
     {
      "label": "posti sufficienti",
      "valore": 95,
      "tono": "verde"
     },
     {
      "label": "poche auto da fermare",
      "valore": 0
     }
    ]
   },
   {
    "tipo": "barre",
    "titolo": "I punti dove mancano più posti",
    "unita": "posti",
    "nota": "Posti che mancano = auto da fermare − posti adatti vicini [STIMATO, ordine di grandezza].",
    "voci": [
     {
      "label": "1. Santa Rita",
      "valore": 450,
      "tono": "rosso"
     },
     {
      "label": "2. Metro Massaua",
      "valore": 350,
      "tono": "rosso"
     },
     {
      "label": "3. Ponte Cavalieri Templari",
      "valore": 350,
      "tono": "rosso"
     },
     {
      "label": "4. Regina Margherita",
      "valore": 350,
      "tono": "rosso"
     },
     {
      "label": "5. Pasini",
      "valore": 250,
      "tono": "rosso"
     },
     {
      "label": "6. Leonardo Da Vinci",
      "valore": 200,
      "tono": "rosso"
     },
     {
      "label": "7. Drosso Cap",
      "valore": 200,
      "tono": "rosso"
     },
     {
      "label": "8. Stura Lazio",
      "valore": 200,
      "tono": "rosso"
     },
     {
      "label": "9. Marsè",
      "valore": 150,
      "tono": "rosso"
     },
     {
      "label": "10. Derna Est",
      "valore": 100,
      "tono": "rosso"
     }
    ]
   }
  ],
  "verifica": [
   {
    "nome": "Caio Mario",
    "fatto": "il valore non cambia (1%): forse il contatore è fermo [MISURATO]; auto in entrata sulla strada accanto: circa 3.900 [STIMATO]",
    "esito": "non si può dire: il contatore sembra fermo"
   },
   {
    "nome": "Fermi",
    "fatto": "non trasmette il riempimento; auto in entrata sulla strada accanto: circa 1.000 [STIMATO]",
    "esito": "non si può dire: non trasmette il riempimento"
   },
   {
    "nome": "Sofia",
    "fatto": "è più pieno di notte che di giorno: 52% di notte, 31% di giorno [MISURATO]; auto in entrata sulla strada accanto: circa 3.100 [STIMATO]",
    "esito": "da capire: accanto passano molte auto in entrata ma è poco usato (prezzo? posizione? collegamento?)"
   },
   {
    "nome": "Stura",
    "fatto": "sempre quasi pieno: 80% di notte, 91% di giorno [MISURATO]; auto in entrata sulla strada accanto: circa 7.600 [STIMATO]",
    "esito": "coerente: pieno, su una strada con molte auto in entrata"
   },
   {
    "nome": "Venchi Unica",
    "fatto": "sempre intorno al 55% [MISURATO]; auto in entrata sulla strada accanto: circa 7.100 [STIMATO]",
    "esito": "non si può dire: riempimento a metà"
   }
  ],
  "affidabilita": [
   {
    "voce": "Parcheggi trovati nei dati aperti",
    "valore": "5.205"
   },
   {
    "voce": "Aperti → fuori dal centro → con almeno 20 posti → adatti (non di destinazione)",
    "valore": "3.431 → 3.208 → 2.006 → 1.874"
   },
   {
    "voce": "Posti nei parcheggi adatti (dichiarati o stimati a 25 m² a posto)",
    "valore": "157.103"
   },
   {
    "voce": "Auto che entrano a Torino al mattino (solo conducenti)",
    "valore": "87.162 [STIMATO, IMQ 2022, 1039 interviste]"
   },
   {
    "voce": "Quota di chi già oggi lascia l'auto per un mezzo pubblico",
    "valore": "5,8% (64 interviste)"
   },
   {
    "voce": "Auto che passano accanto alle fermate",
    "valore": "modello del traffico (percorso più veloce, senza code): solo ordine di grandezza"
   },
   {
    "voce": "Quota di posti in mappa con riempimento misurato",
    "valore": "26,9%"
   },
   {
    "voce": "Giorni feriali di riempimento",
    "valore": "15/10, 16/10, 19/10, 20/10, 21/10"
   },
   {
    "voce": "Non sappiamo",
    "valore": "se i parcheggi senza misura (es. Fermi e i gratuiti) sono pieni; i parcheggi che non sono in OpenStreetMap; i treni"
   }
  ],
  "immagini": [],
  "metodo": [
   "Fermate importanti: fra i luoghi di fermata della Città metropolitana, quelle fuori dal centro, con metro, stazione o capolinea oppure almeno 10 corse all'ora nelle ore dei pendolari, e con almeno 1.000 auto in entrata che passano accanto (centro = i quartieri centrali). Regola fissa; il punteggio (importanza della strada, corse, auto, metro o stazione, pesi uguali) serve solo per l'ordine.",
   "Auto in entrata che passano accanto: le auto che entrano a Torino al mattino (indagine sugli spostamenti 2022) fatte «guidare» sul percorso più veloce della rete stradale; si legge la strada più trafficata entro 100 m.",
   "Auto da fermare = auto che passano × 5,8% (chi già oggi lascia l'auto per un mezzo pubblico).",
   "Posti adatti: parcheggi aperti fuori dal centro, con almeno 20 posti, non di ospedali, università o centri commerciali, entro 400 m a piedi (linea d'aria × 1,3); posti dichiarati o stimati con 25 m² a posto.",
   "Punti prioritari (fino a 20, almeno 50 posti mancanti, uno per asse d'ingresso, oltre 3 km dal centro): fermate senza posti bastanti raggruppate entro 1 km, in ordine di posti che mancano."
  ],
  "parametri": [
   [
    "Centro escluso",
    "i quartieri centrali (fermate e parcheggi)"
   ],
   [
    "Fermate importanti",
    "metro, stazione o capolinea o almeno 10 corse all'ora, e almeno 1.000 auto che passano (274 su 3.898)"
   ],
   [
    "Distanza",
    "400 m a piedi (linea d'aria × 1,3)"
   ],
   [
    "Auto da fermare",
    "auto che passano × 5,8%"
   ],
   [
    "Posti stimati",
    "25 m² a posto (±30%)"
   ],
   [
    "Giorni feriali di riempimento",
    "15/10, 16/10, 19/10, 20/10 e 21/10"
   ]
  ],
  "limiti": [
   "Auto che passano: modello del traffico (percorso più veloce, senza code), stima debole: solo ordine di grandezza. Le stesse auto passano davanti a più fermate dello stesso corso.",
   "Riempimento misurato su soli 5 giorni feriali e solo dove il 5T lo trasmette [DATI SCARSI]: Fermi e i parcheggi gratuiti non sono misurati.",
   "Quota di chi lascia l'auto: indagine sugli spostamenti 2022, poche interviste.",
   "Controllo con i sensori 5T del mattino: il modello mette le strade d'ingresso in un ordine simile solo in parte (ρ = 0,52 su 23 luoghi); sottostima gli ingressi da nord-ovest.",
   "Parcheggi da OpenStreetMap incompleti; posti spesso stimati dalla superficie (±30%).",
   "Distanza a piedi stimata (linea d'aria × 1,3). Treni non considerati."
  ],
  "criteri": [
   {
    "nome": "Fermate importanti",
    "valore": "fuori dal centro, con metro, stazione o capolinea oppure almeno 10 corse all'ora nelle ore dei pendolari, e almeno 1.000 auto in entrata che passano accanto (274 fermate)",
    "perche": "un parcheggio per lasciare l'auto serve dove passa un mezzo frequente e passano molte auto in entrata",
    "effetto": "con N 10, M 500: 347 fermate; con N 10, M 2.000: 201 fermate; con N 15, M 1.000: 136 fermate"
   },
   {
    "nome": "Centro escluso",
    "valore": "quartieri Q001-Q009 (Centro, San Salvario, Crocetta, San Paolo, Cenisia, San Donato, Aurora, Vanchiglia, Nizza Millefonti)",
    "perche": "un parcheggio per lasciare l'auto serve prima di entrare nella città densa, non a due passi dalla destinazione",
    "effetto": "vale sia per le fermate sia per i parcheggi"
   },
   {
    "nome": "Parcheggi contati",
    "valore": "solo quelli adatti: aperti, fuori dal centro, almeno 20 posti, non di ospedali, università o centri commerciali (1.874)",
    "perche": "i posti di chi arriva a destinazione non servono a chi vuole lasciare l'auto prima",
    "effetto": "contando anche i parcheggi di destinazione: 174 fermate senza posti bastanti (invece di 179)"
   },
   {
    "nome": "Distanza",
    "valore": "400 m a piedi (linea d'aria × 1.3)",
    "perche": "chi lascia l'auto accetta di solito una camminata di qualche minuto",
    "effetto": "a 300 m: 209 fermate senza posti bastanti; a 500 m: 147 (a 400 m: 179)"
   },
   {
    "nome": "Auto da fermare",
    "valore": "auto in entrata che passano accanto × 5,8% (chi già oggi lascia l'auto per un mezzo pubblico)",
    "perche": "i posti servono se ci sono auto da fermare: niente soglia fissa di posti",
    "effetto": "con metà quota: 135 fermate senza posti bastanti; con quota doppia: 212"
   },
   {
    "nome": "Poche auto da fermare",
    "valore": "meno di 20 auto da fermare al mattino",
    "perche": "lì un parcheggio per lasciare l'auto non serve",
    "effetto": "0 fermate importanti in questa classe"
   },
   {
    "nome": "Aree",
    "valore": "celle di circa 2 km²; Critica ≥ 60%, Scarsa 30-59%, Buona < 30%; almeno 5 fermate, se no «Pochi dati»",
    "perche": "con una o due fermate la percentuale è 0% o 100% per caso",
    "effetto": "soglie 50/25: Critica 14, Scarsa 4, Buona 2, Pochi dati 42; soglie 66/33: Critica 10, Scarsa 7, Buona 3, Pochi dati 42"
   },
   {
    "nome": "Punti prioritari",
    "valore": "fino a 20: fermate senza posti bastanti raggruppate entro 1 km, in ordine di posti che mancano (almeno 50); uno per asse d'ingresso (niente punti a meno di 2 km, né sulla stessa strada a meno di 5 km); almeno 3 km da Piazza Castello",
    "perche": "risponde a «dove metterne uno o ingrandirlo»; due punti sullo stesso asse contano le stesse auto; vicino al centro si risparmia poca strada",
    "effetto": "candidati: parcheggi adatti con almeno 100 posti entro 600 m a piedi; scartati 38 gruppi su 53"
   },
   {
    "nome": "Riempimento",
    "valore": "misurato dal 5T dove c'è (5 giorni feriali, ore 10-16); pieno ≥ 85%",
    "perche": "un parcheggio pieno non serve",
    "effetto": "colora i parcheggi e mostra i profili; non cambia le classi delle fermate"
   }
  ],
  "mappa": {
   "id": "interscambio",
   "tema": "Parcheggi per lasciare l'auto",
   "nota": "Due domande nella mappa, nel menu «Cosa vedere»: dove ci sono parcheggi e dove servirebbe di più un parcheggio."
  },
  "fonti": [
   "docs/R6_parcheggi.md",
   "docs/rapporti/RAPPORTO_R6_PARCHEGGI.txt",
   "docs/rapporti/RAPPORTO_R6_AUTO_PASSAGGIO.txt",
   "docs/rapporti/RAPPORTO_R6_FERMATE_IMPORTANTI.txt",
   "docs/rapporti/RAPPORTO_R6_PARCHEGGI_ADATTI.txt",
   "scripts/81_auto_di_passaggio.py",
   "scripts/82_parcheggi_adatti.py",
   "scripts/83_fermate_importanti.py",
   "scripts/84_risultato6_parcheggi.py",
   "data/processed/risultato6_v2/mappa_r6.json"
  ],
  "generato": "2026-10-23T13:30:39+00:00",
  "avviso": [
   "Come leggere i tag. ",
   "[MISURATO] = misura vera, fatta dai sensori del sistema 5T. [STIMATO] = calcolo nostro su dati veri, non una misura diretta. [DATI SCARSI] = pochi dati, da prendere con cautela."
  ],
  "in_english": [
   "Question: where are park-and-ride spaces missing for the cars that enter Turin every morning, next to an important public transport stop outside the city centre?",
   "Existing park-and-ride car parks of the City: 4 of 5 report their occupancy; full during the day: 1 (measured, only a few days of data).",
   "About 87,200 cars enter Turin every morning (2022 travel survey) and 5.8% of these drivers already continue by public transport. 179 of 274 important stops outside the centre lack enough suitable parking within 400 m on foot for the cars passing by.",
   "Important stops: outside the centre, with a metro, train station or terminus or at least 10 departures per hour at commuting times, and at least 1,000 cars entering the city passing by.",
   "Limits: car flows come from a simple traffic model (order of magnitude only); occupancy is measured on few days and only where the city's 5T system reports it; trains are not included.",
   "Check against the 5T morning sensors: the model ranks the entry roads in a similar order only in part (rho = 0.52 over 23 places); it underestimates the entries from the north-west."
  ],
  "scenari": [
   {
    "nome": "Oggi",
    "numeri": [
     {
      "label": "Fermate importanti fuori dal centro",
      "prima": null,
      "dopo": 274,
      "unita": "fermate"
     },
     {
      "label": "Senza posti bastanti",
      "prima": null,
      "dopo": 179,
      "unita": "fermate"
     },
     {
      "label": "Senza nessun parcheggio adatto",
      "prima": null,
      "dopo": 68,
      "unita": "fermate"
     }
    ],
    "nota": "Stime [STIMATO]: auto dal modello del traffico, posti da OpenStreetMap, Comune e 5T; riempimento da 5T [DATI SCARSI]."
   }
  ],
  "forma": {
   "etichetta": "STIMATO / MISURATO (dati scarsi)",
   "titolo": "Dai parcheggi di scambio il bus vale l'auto solo se in centro si perdono 21–28 minuti a parcheggiare",
   "domanda": "Dove mancano posti per lasciare l'auto, e quando il bus da lì verso il centro è veloce quanto l'auto?",
   "numero": {
    "valore": "21–28",
    "unita": "minuti",
    "testo": "persi in centro per parcheggiare: sotto questa soglia l'auto batte il bus (mediana dei 12 punti)"
   },
   "principale": {
    "tipo": "gara",
    "titolo": "La gara: bus e auto da un punto a Piazza Castello, alle 8 di un feriale",
    "nota": "Un minuto vero dura un attimo: più la corsa è lunga, più il mezzo arriva tardi. L'auto ha due tempi, parcheggio compreso: 1,2 (sensori, auto veloce) e 2,1 (Google, auto chiara e lenta).",
    "luoghi": [
     {
      "nome": "Santa Rita",
      "gruppo": "Punti prioritari",
      "bus": 36.0,
      "auto_min": 13.7,
      "auto_max": 20.2,
      "giudizio": "il bus non conviene"
     },
     {
      "nome": "Metro Massaua",
      "gruppo": "Punti prioritari",
      "bus": 25.0,
      "auto_min": 15.1,
      "auto_max": 22.7,
      "giudizio": "dipende dal traffico"
     },
     {
      "nome": "Ponte Cavalieri Templari",
      "gruppo": "Punti prioritari",
      "bus": 51.0,
      "auto_min": 18.2,
      "auto_max": 28.0,
      "giudizio": "il bus non conviene"
     },
     {
      "nome": "Regina Margherita",
      "gruppo": "Punti prioritari",
      "bus": 31.0,
      "auto_min": 11.6,
      "auto_max": 16.6,
      "giudizio": "il bus non conviene"
     },
     {
      "nome": "Pasini",
      "gruppo": "Punti prioritari",
      "bus": 28.0,
      "auto_min": 12.1,
      "auto_max": 17.4,
      "giudizio": "il bus non conviene"
     },
     {
      "nome": "Leonardo Da Vinci",
      "gruppo": "Punti prioritari",
      "bus": 59.0,
      "auto_min": 19.9,
      "auto_max": 31.1,
      "giudizio": "il bus non conviene"
     },
     {
      "nome": "Drosso Cap",
      "gruppo": "Punti prioritari",
      "bus": 43.0,
      "auto_min": 17.4,
      "auto_max": 26.7,
      "giudizio": "il bus non conviene"
     },
     {
      "nome": "Stura Lazio",
      "gruppo": "Punti prioritari",
      "bus": 37.0,
      "auto_min": 14.3,
      "auto_max": 21.3,
      "giudizio": "il bus non conviene"
     },
     {
      "nome": "Marsè",
      "gruppo": "Punti prioritari",
      "bus": 61.0,
      "auto_min": 23.2,
      "auto_max": 36.8,
      "giudizio": "il bus non conviene"
     },
     {
      "nome": "Derna Est",
      "gruppo": "Punti prioritari",
      "bus": 34.0,
      "auto_min": 13.8,
      "auto_max": 20.4,
      "giudizio": "il bus non conviene"
     },
     {
      "nome": "Ferrara",
      "gruppo": "Punti prioritari",
      "bus": 49.0,
      "auto_min": 19.9,
      "auto_max": 31.0,
      "giudizio": "il bus non conviene"
     },
     {
      "nome": "Zara",
      "gruppo": "Punti prioritari",
      "bus": 33.0,
      "auto_min": 11.9,
      "auto_max": 17.1,
      "giudizio": "il bus non conviene"
     },
     {
      "nome": "Stura",
      "gruppo": "Interscambi esistenti",
      "bus": 39.0,
      "auto_min": 17.3,
      "auto_max": 26.6,
      "giudizio": "dipende dal traffico"
     },
     {
      "nome": "Venchi Unica",
      "gruppo": "Interscambi esistenti",
      "bus": 28.0,
      "auto_min": 16.0,
      "auto_max": 24.2,
      "giudizio": "dipende dal traffico"
     },
     {
      "nome": "Caio Mario",
      "gruppo": "Interscambi esistenti",
      "bus": 38.0,
      "auto_min": 16.0,
      "auto_max": 24.3,
      "giudizio": "il bus non conviene"
     },
     {
      "nome": "Fermi",
      "gruppo": "Interscambi esistenti",
      "bus": 31.0,
      "auto_min": 18.6,
      "auto_max": 28.9,
      "giudizio": "dipende dal traffico"
     },
     {
      "nome": "Sofia",
      "gruppo": "Interscambi esistenti",
      "bus": 33.0,
      "auto_min": 13.3,
      "auto_max": 19.6,
      "giudizio": "il bus non conviene"
     }
    ],
    "scelto": 1
   },
   "punti": [
    "Interscambi esistenti: pieni Stura (17–27 minuti); poco usati Caio Mario (19–27 minuti), Sofia (18–25 minuti).",
    "179 fermate importanti su 274 non hanno posti bastanti a 400 metri a piedi.",
    "Il punto più promettente è Metro Massaua: bastano 7–15 minuti perché il bus pareggi l'auto."
   ],
   "altri": [
    {
     "tipo": "barre",
     "titolo": "Minuti per parcheggiare in centro oltre i quali il bus dal punto è veloce quanto l'auto",
     "unita": "minuti",
     "nota": "Verso Piazza Castello alle 8. Barra scura = auto lenta (fattore di Google), barra chiara = auto veloce (fattore dei sensori). Meno minuti = punto più promettente; 0 = il bus è già più veloce.",
     "voci": [
      {
       "label": "Metro Massaua",
       "valore": 7,
       "prima": 15,
       "testo": "7–15 min"
      },
      {
       "label": "Pasini",
       "valore": 16,
       "prima": 21,
       "testo": "16–21 min"
      },
      {
       "label": "Derna Est",
       "valore": 19,
       "prima": 25,
       "testo": "19–25 min"
      },
      {
       "label": "Regina Margherita",
       "valore": 19,
       "prima": 24,
       "testo": "19–24 min"
      },
      {
       "label": "Stura Lazio",
       "valore": 21,
       "prima": 28,
       "testo": "21–28 min"
      },
      {
       "label": "Santa Rita",
       "valore": 21,
       "prima": 27,
       "testo": "21–27 min"
      },
      {
       "label": "Zara",
       "valore": 21,
       "prima": 26,
       "testo": "21–26 min"
      },
      {
       "label": "Drosso Cap",
       "valore": 21,
       "prima": 31,
       "testo": "21–31 min"
      },
      {
       "label": "Ferrara",
       "valore": 23,
       "prima": 34,
       "testo": "23–34 min"
      },
      {
       "label": "Ponte Cavalieri Templari",
       "valore": 28,
       "prima": 38,
       "testo": "28–38 min"
      },
      {
       "label": "Marsè",
       "valore": 29,
       "prima": 43,
       "testo": "29–43 min"
      },
      {
       "label": "Leonardo Da Vinci",
       "valore": 33,
       "prima": 44,
       "testo": "33–44 min"
      }
     ]
    },
    {
     "tipo": "barre",
     "titolo": "I 12 punti d'ingresso, per bisogno di parcheggio",
     "unita": "posti",
     "nota": "Il bisogno è alto, medio o basso a terzi, in base ai posti che mancano. Le lunghezze sono un ordine di grandezza.",
     "voci": [
      {
       "label": "Santa Rita",
       "valore": 450,
       "tono": "rosso",
       "testo": "bisogno alto"
      },
      {
       "label": "Metro Massaua",
       "valore": 350,
       "tono": "rosso",
       "testo": "bisogno alto"
      },
      {
       "label": "Ponte Cavalieri Templari",
       "valore": 350,
       "tono": "rosso",
       "testo": "bisogno alto"
      },
      {
       "label": "Regina Margherita",
       "valore": 350,
       "tono": "rosso",
       "testo": "bisogno alto"
      },
      {
       "label": "Pasini",
       "valore": 250,
       "tono": "arancio",
       "testo": "bisogno medio"
      },
      {
       "label": "Leonardo Da Vinci",
       "valore": 200,
       "tono": "arancio",
       "testo": "bisogno medio"
      },
      {
       "label": "Drosso Cap",
       "valore": 200,
       "tono": "arancio",
       "testo": "bisogno medio"
      },
      {
       "label": "Stura Lazio",
       "valore": 200,
       "tono": "arancio",
       "testo": "bisogno medio"
      },
      {
       "label": "Marsè",
       "valore": 150,
       "tono": "giallo",
       "testo": "bisogno basso"
      },
      {
       "label": "Derna Est",
       "valore": 100,
       "tono": "giallo",
       "testo": "bisogno basso"
      },
      {
       "label": "Ferrara",
       "valore": 80,
       "tono": "giallo",
       "testo": "bisogno basso"
      },
      {
       "label": "Zara",
       "valore": 60,
       "tono": "giallo",
       "testo": "bisogno basso"
      }
     ]
    }
   ],
   "calcolo": [
    "Fermate importanti: fuori dal centro, con metro, stazione o capolinea, oppure 10 corse all'ora.",
    "Le auto in entrata vengono dall'indagine sugli spostamenti 2022, assegnate al percorso più veloce.",
    "Auto da fermare: auto che passano per il 5,8% che già oggi lascia l'auto. Posti: parcheggi adatti entro 400 metri.",
    "Punti prioritari: fermate senza posti bastanti raggruppate entro 1 km, uno per asse d'ingresso.",
    "Minuti di pareggio: tempo coi mezzi verso Piazza Castello alle 8, meno il tempo in auto senza parcheggio."
   ],
   "criteri": [
    [
     "Fermate importanti",
     "10 corse all'ora o metro, e 1.000 auto che passano"
    ],
    [
     "Distanza a piedi",
     "400 metri"
    ],
    [
     "Auto da fermare",
     "auto che passano × 5,8%"
    ],
    [
     "Bus contro auto",
     "verso Piazza Castello alle 8, auto con fattore 1,2 (sensori) e 2,1 (Google)"
    ]
   ],
   "limiti": [
    "I tempi coi mezzi sono solo GTT, senza treni. L'auto è stimata fra due fattori di punta, 1,2 e 2,1.",
    "Il costo del parcheggio in centro non è nel calcolo: pesa come minuti in più.",
    "Si guarda un solo punto per luogo e una sola destinazione, Piazza Castello.",
    "Le auto che passano vengono da un modello del traffico. I posti sono spesso stimati, con ±30%."
   ],
   "english": [
    "Question: when is the bus from a park-and-ride as fast as the car to the centre?",
    "Answer: park-and-ride pays off only if parking downtown costs at least 21–28 minutes (median of 12 priority points). Also, 179 of 274 important stops lack enough parking.",
    "Limit: bus times use GTT only, without trains; parking cost is not considered."
   ],
   "mappa": {
    "id": "interscambio",
    "nota": "Due domande nella mappa, nel menu «Cosa vedere»: dove ci sono parcheggi e dove servirebbe di più un parcheggio."
   },
   "unita": {
    "tipo": "pallini",
    "pallini": [
     {
      "label": "Santa Rita",
      "tono": "rosso"
     },
     {
      "label": "Metro Massaua",
      "tono": "giallo"
     },
     {
      "label": "Ponte Cavalieri Templari",
      "tono": "rosso"
     },
     {
      "label": "Regina Margherita",
      "tono": "rosso"
     },
     {
      "label": "Pasini",
      "tono": "rosso"
     },
     {
      "label": "Leonardo Da Vinci",
      "tono": "rosso"
     },
     {
      "label": "Drosso Cap",
      "tono": "rosso"
     },
     {
      "label": "Stura Lazio",
      "tono": "rosso"
     },
     {
      "label": "Marsè",
      "tono": "rosso"
     },
     {
      "label": "Derna Est",
      "tono": "rosso"
     },
     {
      "label": "Ferrara",
      "tono": "rosso"
     },
     {
      "label": "Zara",
      "tono": "rosso"
     }
    ],
    "didascalia": "Un pallino per punto prioritario: verde = il bus conviene (0), giallo = dipende (1), rosso = il bus non conviene (11)."
   },
   "extra": {
    "titolo": "Interscambi esistenti e bus verso il centro",
    "punto": "Gli interscambi esistenti sono poco pieni: di giorno solo 1 su 5 è pieno.",
    "grafico": {
     "tipo": "barre",
     "titolo": "Dagli interscambi esistenti a Piazza Castello, minuti coi mezzi pubblici",
     "unita": "minuti",
     "nota": "Alle 8 di un feriale. A destra il tempo in auto, parcheggio compreso, fra i due fattori di punta (1,2 e 2,1).",
     "voci": [
      {
       "label": "Stura",
       "valore": 39,
       "testo": "39 contro 17-27 in auto"
      },
      {
       "label": "Venchi Unica",
       "valore": 28,
       "testo": "28 contro 16-24 in auto"
      },
      {
       "label": "Caio Mario",
       "valore": 38,
       "testo": "38 contro 16-24 in auto"
      },
      {
       "label": "Fermi",
       "valore": 31,
       "testo": "31 contro 19-29 in auto"
      },
      {
       "label": "Sofia",
       "valore": 33,
       "testo": "33 contro 13-20 in auto"
      }
     ]
    }
   }
  },
  "forma_en": {
   "etichetta": "ESTIMATED / MEASURED (little data)",
   "titolo": "From park-and-ride lots the bus matches the car only if 21–28 minutes are lost parking downtown",
   "domanda": "Where is there too little room to leave the car, and when is the bus from there to the centre as fast as the car?",
   "numero": {
    "valore": "21–28",
    "unita": "minutes",
    "testo": "lost downtown looking for parking: below this threshold the car beats the bus (median of the 12 points)"
   },
   "principale": {
    "tipo": "gara",
    "titolo": "The race: bus and car from a point to Piazza Castello, at 8 a.m. on a weekday",
    "nota": "One real minute lasts a split second: the longer the trip, the later the vehicle arrives. The car has two times, parking included: 1.2 (sensors, fast car) and 2.1 (Google, faded slow car).",
    "luoghi": [
     {
      "nome": "Santa Rita",
      "gruppo": "Priority points",
      "bus": 36.0,
      "auto_min": 13.7,
      "auto_max": 20.2,
      "giudizio": "the bus does not pay off"
     },
     {
      "nome": "Metro Massaua",
      "gruppo": "Priority points",
      "bus": 25.0,
      "auto_min": 15.1,
      "auto_max": 22.7,
      "giudizio": "depends on traffic"
     },
     {
      "nome": "Ponte Cavalieri Templari",
      "gruppo": "Priority points",
      "bus": 51.0,
      "auto_min": 18.2,
      "auto_max": 28.0,
      "giudizio": "the bus does not pay off"
     },
     {
      "nome": "Regina Margherita",
      "gruppo": "Priority points",
      "bus": 31.0,
      "auto_min": 11.6,
      "auto_max": 16.6,
      "giudizio": "the bus does not pay off"
     },
     {
      "nome": "Pasini",
      "gruppo": "Priority points",
      "bus": 28.0,
      "auto_min": 12.1,
      "auto_max": 17.4,
      "giudizio": "the bus does not pay off"
     },
     {
      "nome": "Leonardo Da Vinci",
      "gruppo": "Priority points",
      "bus": 59.0,
      "auto_min": 19.9,
      "auto_max": 31.1,
      "giudizio": "the bus does not pay off"
     },
     {
      "nome": "Drosso Cap",
      "gruppo": "Priority points",
      "bus": 43.0,
      "auto_min": 17.4,
      "auto_max": 26.7,
      "giudizio": "the bus does not pay off"
     },
     {
      "nome": "Stura Lazio",
      "gruppo": "Priority points",
      "bus": 37.0,
      "auto_min": 14.3,
      "auto_max": 21.3,
      "giudizio": "the bus does not pay off"
     },
     {
      "nome": "Marsè",
      "gruppo": "Priority points",
      "bus": 61.0,
      "auto_min": 23.2,
      "auto_max": 36.8,
      "giudizio": "the bus does not pay off"
     },
     {
      "nome": "Derna Est",
      "gruppo": "Priority points",
      "bus": 34.0,
      "auto_min": 13.8,
      "auto_max": 20.4,
      "giudizio": "the bus does not pay off"
     },
     {
      "nome": "Ferrara",
      "gruppo": "Priority points",
      "bus": 49.0,
      "auto_min": 19.9,
      "auto_max": 31.0,
      "giudizio": "the bus does not pay off"
     },
     {
      "nome": "Zara",
      "gruppo": "Priority points",
      "bus": 33.0,
      "auto_min": 11.9,
      "auto_max": 17.1,
      "giudizio": "the bus does not pay off"
     },
     {
      "nome": "Stura",
      "gruppo": "Existing park-and-ride",
      "bus": 39.0,
      "auto_min": 17.3,
      "auto_max": 26.6,
      "giudizio": "depends on traffic"
     },
     {
      "nome": "Venchi Unica",
      "gruppo": "Existing park-and-ride",
      "bus": 28.0,
      "auto_min": 16.0,
      "auto_max": 24.2,
      "giudizio": "depends on traffic"
     },
     {
      "nome": "Caio Mario",
      "gruppo": "Existing park-and-ride",
      "bus": 38.0,
      "auto_min": 16.0,
      "auto_max": 24.3,
      "giudizio": "the bus does not pay off"
     },
     {
      "nome": "Fermi",
      "gruppo": "Existing park-and-ride",
      "bus": 31.0,
      "auto_min": 18.6,
      "auto_max": 28.9,
      "giudizio": "depends on traffic"
     },
     {
      "nome": "Sofia",
      "gruppo": "Existing park-and-ride",
      "bus": 33.0,
      "auto_min": 13.3,
      "auto_max": 19.6,
      "giudizio": "the bus does not pay off"
     }
    ],
    "scelto": 1
   },
   "punti": [
    "Existing park-and-ride lots: full Stura (17–27 minutes); little used Caio Mario (19–27 minutes), Sofia (18–25 minutes).",
    "179 important stops out of 274 do not have enough parking within 400 metres on foot.",
    "The most promising point is Metro Massaua: 7–15 minutes are enough for the bus to match the car."
   ],
   "altri": [
    {
     "tipo": "barre",
     "titolo": "Minutes spent parking downtown beyond which the bus from the point is as fast as the car",
     "unita": "minutes",
     "nota": "Towards Piazza Castello at 8 a.m. Dark bar = slow car (Google factor), light bar = fast car (sensor factor). Fewer minutes = more promising point; 0 = the bus is already faster.",
     "voci": [
      {
       "label": "Metro Massaua",
       "valore": 7,
       "prima": 15,
       "testo": "7–15 min"
      },
      {
       "label": "Pasini",
       "valore": 16,
       "prima": 21,
       "testo": "16–21 min"
      },
      {
       "label": "Derna Est",
       "valore": 19,
       "prima": 25,
       "testo": "19–25 min"
      },
      {
       "label": "Regina Margherita",
       "valore": 19,
       "prima": 24,
       "testo": "19–24 min"
      },
      {
       "label": "Stura Lazio",
       "valore": 21,
       "prima": 28,
       "testo": "21–28 min"
      },
      {
       "label": "Santa Rita",
       "valore": 21,
       "prima": 27,
       "testo": "21–27 min"
      },
      {
       "label": "Zara",
       "valore": 21,
       "prima": 26,
       "testo": "21–26 min"
      },
      {
       "label": "Drosso Cap",
       "valore": 21,
       "prima": 31,
       "testo": "21–31 min"
      },
      {
       "label": "Ferrara",
       "valore": 23,
       "prima": 34,
       "testo": "23–34 min"
      },
      {
       "label": "Ponte Cavalieri Templari",
       "valore": 28,
       "prima": 38,
       "testo": "28–38 min"
      },
      {
       "label": "Marsè",
       "valore": 29,
       "prima": 43,
       "testo": "29–43 min"
      },
      {
       "label": "Leonardo Da Vinci",
       "valore": 33,
       "prima": 44,
       "testo": "33–44 min"
      }
     ]
    },
    {
     "tipo": "barre",
     "titolo": "The 12 entry points, by need for parking",
     "unita": "spaces",
     "nota": "Need is high, medium or low by thirds, based on the missing spaces. Lengths are an order of magnitude.",
     "voci": [
      {
       "label": "Santa Rita",
       "valore": 450,
       "tono": "rosso",
       "testo": "high need"
      },
      {
       "label": "Metro Massaua",
       "valore": 350,
       "tono": "rosso",
       "testo": "high need"
      },
      {
       "label": "Ponte Cavalieri Templari",
       "valore": 350,
       "tono": "rosso",
       "testo": "high need"
      },
      {
       "label": "Regina Margherita",
       "valore": 350,
       "tono": "rosso",
       "testo": "high need"
      },
      {
       "label": "Pasini",
       "valore": 250,
       "tono": "arancio",
       "testo": "medium need"
      },
      {
       "label": "Leonardo Da Vinci",
       "valore": 200,
       "tono": "arancio",
       "testo": "medium need"
      },
      {
       "label": "Drosso Cap",
       "valore": 200,
       "tono": "arancio",
       "testo": "medium need"
      },
      {
       "label": "Stura Lazio",
       "valore": 200,
       "tono": "arancio",
       "testo": "medium need"
      },
      {
       "label": "Marsè",
       "valore": 150,
       "tono": "giallo",
       "testo": "low need"
      },
      {
       "label": "Derna Est",
       "valore": 100,
       "tono": "giallo",
       "testo": "low need"
      },
      {
       "label": "Ferrara",
       "valore": 80,
       "tono": "giallo",
       "testo": "low need"
      },
      {
       "label": "Zara",
       "valore": 60,
       "tono": "giallo",
       "testo": "low need"
      }
     ]
    }
   ],
   "calcolo": [
    "Important stops: outside the centre, with a metro, station or terminus, or 10 trips an hour.",
    "Cars entering come from the 2022 travel survey, assigned to the fastest route.",
    "Cars to stop: passing cars times the 5.8% who already leave the car today. Spaces: suitable car parks within 400 metres.",
    "Priority points: stops without enough parking, grouped within 1 km, one per entry axis.",
    "Break-even minutes: travel time by public transport to Piazza Castello at 8 a.m., minus travel time by car without parking."
   ],
   "criteri": [
    [
     "Important stops",
     "10 trips an hour or a metro, and 1,000 passing cars"
    ],
    [
     "Walking distance",
     "400 metres"
    ],
    [
     "Cars to stop",
     "passing cars × 5.8%"
    ],
    [
     "Bus versus car",
     "towards Piazza Castello at 8 a.m., car with factor 1.2 (sensors) and 2.1 (Google)"
    ]
   ],
   "limiti": [
    "Public transport times are GTT only, without trains. The car is estimated between two peak factors, 1.2 and 2.1.",
    "The cost of parking downtown is not in the calculation: it counts as extra minutes.",
    "We look at one point per place and a single destination, Piazza Castello.",
    "Passing cars come from a traffic model. Spaces are often estimated, with ±30%."
   ],
   "mappa": {
    "id": "interscambio",
    "nota": "Due domande nella mappa, nel menu «Cosa vedere»: dove ci sono parcheggi e dove servirebbe di più un parcheggio."
   },
   "unita": {
    "tipo": "pallini",
    "pallini": [
     {
      "label": "Santa Rita",
      "tono": "rosso"
     },
     {
      "label": "Metro Massaua",
      "tono": "giallo"
     },
     {
      "label": "Ponte Cavalieri Templari",
      "tono": "rosso"
     },
     {
      "label": "Regina Margherita",
      "tono": "rosso"
     },
     {
      "label": "Pasini",
      "tono": "rosso"
     },
     {
      "label": "Leonardo Da Vinci",
      "tono": "rosso"
     },
     {
      "label": "Drosso Cap",
      "tono": "rosso"
     },
     {
      "label": "Stura Lazio",
      "tono": "rosso"
     },
     {
      "label": "Marsè",
      "tono": "rosso"
     },
     {
      "label": "Derna Est",
      "tono": "rosso"
     },
     {
      "label": "Ferrara",
      "tono": "rosso"
     },
     {
      "label": "Zara",
      "tono": "rosso"
     }
    ],
    "didascalia": "One dot per priority point: green = the bus pays off (0), yellow = it depends (1), red = the bus does not pay off (11)."
   },
   "extra": {
    "titolo": "Existing park-and-ride lots and buses to the centre",
    "punto": "Existing park-and-ride lots are not very full: in the daytime only 1 of 5 is full.",
    "grafico": {
     "tipo": "barre",
     "titolo": "From existing park-and-ride lots to Piazza Castello, minutes by public transport",
     "unita": "minutes",
     "nota": "At 8 a.m. on a weekday. On the right, car time including parking, between the two peak factors (1.2 and 2.1).",
     "voci": [
      {
       "label": "Stura",
       "valore": 39,
       "testo": "39 versus 17-27 by car"
      },
      {
       "label": "Venchi Unica",
       "valore": 28,
       "testo": "28 versus 16-24 by car"
      },
      {
       "label": "Caio Mario",
       "valore": 38,
       "testo": "38 versus 16-24 by car"
      },
      {
       "label": "Fermi",
       "valore": 31,
       "testo": "31 versus 19-29 by car"
      },
      {
       "label": "Sofia",
       "valore": 33,
       "testo": "33 versus 13-20 by car"
      }
     ]
    }
   }
  },
  "numero_pubblico": 3,
  "_nome": "risultato6_riepilogo_mappa.json"
 },
 {
  "risultato": "8",
  "titolo": "Traffico sulle strade e trasporto pubblico",
  "tag": "STIMATO / MISURATO / PROGRAMMATO",
  "stato": "Fatto",
  "in_breve": "Quante auto passano sulle strade grandi di Torino? E dove c'è tanto traffico ma nessun bus, tram o metro comodo, così che l'auto resta l'unica scelta?",
  "domanda": "Sulle strade grandi di Torino, dove c'è molto traffico e poco trasporto pubblico vicino?",
  "numero_chiave": {
   "valore": 95.3,
   "unita": "%",
   "testo": "dei km di strade grandi di Torino hanno fermate frequenti a pochi passi (327,3 km su 343,3)"
  },
  "racconto": "Un primo calcolo trovava 23 strade \"con molto traffico e poco trasporto pubblico\". Ricontrollando, quasi tutte erano un errore di misura: i bus si cercavano lungo la strada per nome invece che per posizione delle fermate (Corso Cairoli risultava senza passaggi). Rifatto il calcolo, la lista si è quasi svuotata: è questa la risposta.",
  "risposta": [
   "Sulle 540 tratte di strade grandi di Torino (343,3 km), il 95,3% della lunghezza ha una fermata con almeno 4 passaggi all'ora entro 300 m, o la metro entro 600 m.",
   "Le tratte con molto traffico (oltre 11.720 veicoli al giorno) sono 180; quelle che hanno anche poco trasporto pubblico sono 5.",
   "In pratica è un solo caso: Corso Regina Margherita verso ovest, il tratto a scorrimento veloce (circa 34.000 veicoli al giorno, nessuna fermata frequente entro 300 m). In più un tratto di Corso Moncalieri, coperto solo per un quarto della lunghezza.",
   "I numeri di traffico sono stime: in metà dei casi l'errore è entro ±38%. Servono a ordinare le strade, non a contare i veicoli."
  ],
  "grafici": [
   {
    "tipo": "pila",
    "titolo": "Km di strade grandi di Torino: con o senza trasporto pubblico vicino",
    "unita": "km",
    "voci": [
     {
      "label": "con fermate frequenti vicine",
      "valore": 327.3,
      "tono": "verde"
     },
     {
      "label": "con poco trasporto pubblico",
      "valore": 16.0,
      "tono": "rosso"
     }
    ]
   },
   {
    "tipo": "barre",
    "titolo": "Strade con un sensore: la tratta più carica (veicoli al giorno, 6-21)",
    "unita": "veicoli/giorno",
    "nota": "Solo strade con almeno un sensore sullo stesso asse: senza, il modello mette in cima anche strade poco credibili. \"misurato\" = sensore sulla tratta; le altre sono stime. Corso Unione Sovietica è probabilmente sovrastimato: dove c'è il sensore il modello dava quasi il triplo del misurato.",
    "voci": [
     {
      "label": "Unità d'Italia (misurato)",
      "valore": 80946
     },
     {
      "label": "Regina Margherita",
      "valore": 56136
     },
     {
      "label": "Orbassano (misurato)",
      "valore": 50204
     },
     {
      "label": "Unione Sovietica",
      "valore": 47774
     },
     {
      "label": "Francia",
      "valore": 47616
     },
     {
      "label": "Giulio Cesare (misurato)",
      "valore": 33928
     },
     {
      "label": "Asse di Penetrazione Urbana di Corso Regina Margherita",
      "valore": 33529
     },
     {
      "label": "Giovanni Agnelli",
      "valore": 31640
     },
     {
      "label": "Strada di Settimo (misurato)",
      "valore": 29916
     },
     {
      "label": "Vercelli (misurato)",
      "valore": 26244
     }
    ]
   },
   {
    "tipo": "barre",
    "titolo": "Prova del modello sui 20 sensori: misurato e stimato",
    "unita": "veicoli/giorno",
    "nota": "Barra chiara = misurato dal sensore, barra scura = stima del modello senza usare quel sensore.",
    "voci": [
     {
      "label": "Corso Unità d'Italia",
      "valore": 60268,
      "prima": 80946
     },
     {
      "label": "Corso Trieste",
      "valore": 58375,
      "prima": 69134
     },
     {
      "label": "Corso Orbassano",
      "valore": 42058,
      "prima": 50204
     },
     {
      "label": "Corso Orbassano",
      "valore": 41245,
      "prima": 41346
     },
     {
      "label": "R24 Raccordo Torino-Aeroporto Caselle",
      "valore": 30159,
      "prima": 40092
     },
     {
      "label": "Corso Giulio Cesare",
      "valore": 24228,
      "prima": 33928
     },
     {
      "label": "Corso Francia",
      "valore": 40789,
      "prima": 30934
     },
     {
      "label": "Ponte Amedeo VIII",
      "valore": 20918,
      "prima": 29916
     },
     {
      "label": "Corso Giulio Cesare",
      "valore": 32592,
      "prima": 28846
     },
     {
      "label": "Corso Francia",
      "valore": 41574,
      "prima": 28698
     },
     {
      "label": "Corso Regina Margherita",
      "valore": 31008,
      "prima": 28438
     },
     {
      "label": "Corso Orbassano",
      "valore": 40010,
      "prima": 27262
     },
     {
      "label": "Corso Vercelli",
      "valore": 14077,
      "prima": 26244
     },
     {
      "label": "Corso Agnelli",
      "valore": 32947,
      "prima": 21104
     },
     {
      "label": "SP8 di Druento",
      "valore": 8236,
      "prima": 20889
     },
     {
      "label": "Corso Unione Sovietica",
      "valore": 52860,
      "prima": 19066
     },
     {
      "label": "Corso Sebastopoli",
      "valore": 34568,
      "prima": 17342
     },
     {
      "label": "Strada Di Settimo",
      "valore": 8267,
      "prima": 16888
     },
     {
      "label": "SP1 delle Valli di Lanzo",
      "valore": 7968,
      "prima": 15886
     },
     {
      "label": "Corso Allamano",
      "valore": 19177,
      "prima": 12636
     }
    ]
   },
   {
    "tipo": "barre",
    "titolo": "Errore della stima su ogni sensore (%)",
    "unita": "%",
    "nota": "Errore = |stimato − misurato| / misurato. Metà dei sensori sotto il valore tipico, gli altri sopra.",
    "voci": [
     {
      "label": "Corso Orbassano",
      "valore": 0,
      "tono": "rosso"
     },
     {
      "label": "Corso Regina Margherita",
      "valore": 9,
      "tono": "rosso"
     },
     {
      "label": "Corso Giulio Cesare",
      "valore": 13,
      "tono": "rosso"
     },
     {
      "label": "Corso Trieste",
      "valore": 16,
      "tono": "rosso"
     },
     {
      "label": "Corso Orbassano",
      "valore": 16,
      "tono": "rosso"
     },
     {
      "label": "R24 Raccordo Torino-Aeroporto Caselle",
      "valore": 25,
      "tono": "rosso"
     },
     {
      "label": "Corso Unità d'Italia",
      "valore": 26,
      "tono": "rosso"
     },
     {
      "label": "Corso Giulio Cesare",
      "valore": 29,
      "tono": "rosso"
     },
     {
      "label": "Ponte Amedeo VIII",
      "valore": 30,
      "tono": "rosso"
     },
     {
      "label": "Corso Francia",
      "valore": 32,
      "tono": "rosso"
     },
     {
      "label": "Corso Francia",
      "valore": 45,
      "tono": "rosso"
     },
     {
      "label": "Corso Vercelli",
      "valore": 46,
      "tono": "rosso"
     },
     {
      "label": "Corso Orbassano",
      "valore": 47,
      "tono": "rosso"
     },
     {
      "label": "SP1 delle Valli di Lanzo",
      "valore": 50,
      "tono": "rosso"
     },
     {
      "label": "Strada Di Settimo",
      "valore": 51,
      "tono": "rosso"
     },
     {
      "label": "Corso Allamano",
      "valore": 52,
      "tono": "rosso"
     },
     {
      "label": "Corso Agnelli",
      "valore": 56,
      "tono": "rosso"
     },
     {
      "label": "SP8 di Druento",
      "valore": 61,
      "tono": "rosso"
     },
     {
      "label": "Corso Sebastopoli",
      "valore": 99,
      "tono": "rosso"
     },
     {
      "label": "Corso Unione Sovietica",
      "valore": 177,
      "tono": "rosso"
     }
    ]
   }
  ],
  "metodo": [
   "Domanda: gli spostamenti in auto dell'indagine sugli spostamenti 2022 (residenti, giorno feriale), assegnati alla strada più veloce sulla rete di OpenStreetMap.",
   "Taratura su 20 punti di misura dei sensori 5T: un solo fattore per tutta la città, provato togliendo un sensore alla volta e stimandolo con gli altri.",
   "Strade come assi: un corso che cambia nome o comune resta la stessa strada, tagliata in tratte da 300 m a 1,5 km. Strade grandi = Torino, importanza alta o strade principali, almeno 300 m, senza tangenziale e raccordi.",
   "Trasporto pubblico per posizione delle fermate, mai per nome: una tratta è servita dove c'è una fermata con almeno 4 passaggi all'ora entro 300 m (orario ufficiale, mercoledì 14/10), o la metro entro 600 m. Poco trasporto pubblico = servita per metà della lunghezza o meno.",
   "Molto traffico = il terzo più alto delle tratte. Un modello più ricco (attrazioni, code, ZTL) è stato provato una volta e non ha migliorato l'ordine delle strade: si tiene quello semplice."
  ],
  "parametri": [
   [
    "Strade grandi di Torino",
    "540 tratte, 343,3 km"
   ],
   [
    "Errore tipico (metà dei casi)",
    "±38% (9 volte su 10 entro ±64%)"
   ],
   [
    "Ordine giusto delle strade (Spearman)",
    "0,60"
   ],
   [
    "Validato tra",
    "8.800 e 105.000 veicoli/giorno"
   ],
   [
    "Soglia 'molto traffico'",
    "11.720 veicoli/giorno"
   ],
   [
    "Confronto con chi conosce la città",
    "10 strade su 18 nella fascia giusta, 4 confronti su 7 (solo controllo)"
   ]
  ],
  "limiti": [
   "Stima debole: errore tipico ±38% e intervallo d'incertezza largo (da 26% a 50%). Alcune strade sono molto sbagliate (Corso Unione Sovietica, Corso Sebastopoli): buona per ordinare, non per contare.",
   "Solo 20 punti di misura, quasi tutti su corsi trafficati: sotto circa 9.000 veicoli al giorno la stima non è verificata.",
   "Solo i residenti tra 11 e 84 anni (indagine sugli spostamenti): mancano merci, turisti e chi viene da fuori. Il modello non sa fare le code: l'ora di punta non è verificata.",
   "Trasporto pubblico programmato: niente ritardi né affollamento. Il centro (ZTL, aree pedonali) non è stimato bene.",
   "Il valore è per i due versi: sulle poche vie a senso unico vero potrebbe essere il doppio del reale.",
   "Il tratto di Corso Moncalieri va controllato a mano: una fermata con 26 passaggi all'ora è a 40 m, ma copre solo un quarto della tratta."
  ],
  "in_english": [
   "Question: on Turin's major roads, where is there a lot of traffic and little public transport nearby?",
   "Of 540 road sections on Turin's major roads (343.3 km), 95.3% of the length has a frequent stop (at least 4 departures an hour) within 300 m, or the metro within 600 m. Heavy-traffic sections (over 11,720 vehicles a day): 180; of these, 5 also have little public transport.",
   "In practice this is one main case: Corso Regina Margherita westbound, a fast road with no frequent stop within 300 m, plus one stretch of Corso Moncalieri covered for only a quarter of its length.",
   "Limits: traffic figures are estimates with a typical error of ±38%; use them to rank the roads, not to count vehicles."
  ],
  "mappa": null,
  "fonti": [
   "docs/R8_traffico.md",
   "docs/rapporti/RAPPORTO_RISULTATO8_TRAFFICO_TP_V2.txt",
   "data/processed/risultato8_traffico_tp_v2.json"
  ],
  "generato": "2026-10-23T13:30:39+00:00",
  "avviso": [
   "Dati [STIMATO] (traffico) / [MISURATO] (sensori 5T) / [PROGRAMMATO] (orari GTT)",
   "Traffico stimato con un modello tarato su 20 sensori: errore tipico ±38%. Trasporto pubblico = fermate con almeno 4 passaggi all'ora entro 300 m o metro entro 600 m."
  ],
  "scenari": [
   {
    "nome": "Oggi",
    "numeri": [
     {
      "label": "Km di strade grandi di Torino",
      "prima": null,
      "dopo": 343.3,
      "unita": "km"
     },
     {
      "label": "Con fermate frequenti vicine",
      "prima": null,
      "dopo": 95.3,
      "unita": "%"
     },
     {
      "label": "Tratte con molto traffico",
      "prima": null,
      "dopo": 180,
      "unita": "tratte"
     },
     {
      "label": "Molto traffico e poco trasporto pubblico",
      "prima": null,
      "dopo": 5,
      "unita": "tratte"
     },
     {
      "label": "Errore tipico della stima",
      "prima": null,
      "dopo": 38,
      "unita": "%"
     }
    ],
    "nota": "Le 5 tratte sono quasi tutte su Corso Regina Margherita ovest; una su Corso Moncalieri."
   }
  ],
  "forma": {
   "etichetta": "STIMATO / MISURATO / PROGRAMMATO",
   "titolo": "Al mattino, coi mezzi pubblici si impiega da 2 a 3 volte il tempo dell'auto",
   "domanda": "Per quali spostamenti l'auto è molto più veloce dei mezzi pubblici, e quante auto li fanno?",
   "numero": {
    "valore": "2–3",
    "unita": "volte",
    "testo": "il tempo dell'auto: rapporto mediano, pesato per le auto del mattino (220.307 auto)"
   },
   "principale": {
    "tipo": "barre_gruppi",
    "titolo": "Auto del mattino per rapporto fra tempo coi mezzi pubblici e tempo in auto",
    "unita": "%",
    "max": 100,
    "nota": "Rapporto 2 = coi mezzi pubblici si impiega il doppio che in auto. Coppie Torino-Torino e Torino-cintura. Limite basso: auto lenta come su Google Maps (fattore 2,1); limite alto: auto veloce come misurano i sensori (fattore 1,2).",
    "gruppi": [
     {
      "label": "sotto 1,5",
      "voci": [
       {
        "label": "limite basso",
        "valore": 3.9,
        "tono": "verde",
        "testo": "3,9% (8.649 auto)"
       },
       {
        "label": "limite alto",
        "valore": 0.0,
        "tono": "verde",
        "testo": "0% (0 auto)"
       }
      ]
     },
     {
      "label": "1,5-2",
      "voci": [
       {
        "label": "limite basso",
        "valore": 54.6,
        "tono": "giallo",
        "testo": "54,6% (120.360 auto)"
       },
       {
        "label": "limite alto",
        "valore": 3.0,
        "tono": "giallo",
        "testo": "3% (6.661 auto)"
       }
      ]
     },
     {
      "label": "2-3",
      "voci": [
       {
        "label": "limite basso",
        "valore": 41.1,
        "tono": "arancio",
        "testo": "41,1% (90.508 auto)"
       },
       {
        "label": "limite alto",
        "valore": 52.2,
        "tono": "arancio",
        "testo": "52,2% (115.033 auto)"
       }
      ]
     },
     {
      "label": "oltre 3",
      "voci": [
       {
        "label": "limite basso",
        "valore": 0.4,
        "tono": "rosso",
        "testo": "0,4% (791 auto)"
       },
       {
        "label": "limite alto",
        "valore": 44.8,
        "tono": "rosso",
        "testo": "44,8% (98.612 auto)"
       }
      ]
     }
    ]
   },
   "punti": [
    "Le auto con rapporto oltre 2 sono il 41% con il fattore basso e il 97% con il fattore alto.",
    "Le 3 coppie peggiori: Torino, Madonna Del Pilone → Torino, Vanchiglia, Torino, Parella → Torino, San Paolo, Torino, Madonna Del Pilone → Torino, Centro.",
    "Google conferma i tempi coi mezzi pubblici sui percorsi di controllo: 31 contro 30-35 e 33 contro 30-35 minuti."
   ],
   "altri": [
    {
     "tipo": "dispersione",
     "titolo": "Tempo in auto e tempo coi mezzi pubblici, una coppia di zone per punto",
     "xlabel": "minuti in auto (ora di punta, fattore 2,1)",
     "ylabel": "minuti coi mezzi pubblici",
     "punti": [
      [
       12.7,
       20.6,
       1355.3
      ],
      [
       16.0,
       31.3,
       1341.8
      ],
      [
       10.6,
       19.2,
       1324.4
      ],
      [
       18.1,
       24.7,
       1277.0
      ],
      [
       12.0,
       18.7,
       1269.4
      ],
      [
       13.4,
       24.0,
       1208.2
      ],
      [
       23.2,
       43.0,
       1149.2
      ],
      [
       18.8,
       37.5,
       1107.8
      ],
      [
       47.5,
       80.1,
       1081.8
      ],
      [
       10.3,
       15.2,
       1038.1
      ],
      [
       16.8,
       33.2,
       969.9
      ],
      [
       18.7,
       30.6,
       968.1
      ],
      [
       10.6,
       15.2,
       957.2
      ],
      [
       27.2,
       44.5,
       940.7
      ],
      [
       12.6,
       20.2,
       938.8
      ],
      [
       17.0,
       33.5,
       928.7
      ],
      [
       19.1,
       38.2,
       916.7
      ],
      [
       35.6,
       63.4,
       910.0
      ],
      [
       15.7,
       30.4,
       900.6
      ],
      [
       15.5,
       35.2,
       894.4
      ],
      [
       11.8,
       22.4,
       893.3
      ],
      [
       13.0,
       23.8,
       889.9
      ],
      [
       22.8,
       39.3,
       888.0
      ],
      [
       18.3,
       27.5,
       818.9
      ],
      [
       22.1,
       42.3,
       796.7
      ],
      [
       18.0,
       35.2,
       795.1
      ],
      [
       10.3,
       18.9,
       789.0
      ],
      [
       19.7,
       31.2,
       779.1
      ],
      [
       15.1,
       30.4,
       762.5
      ],
      [
       22.8,
       50.0,
       753.4
      ],
      [
       15.8,
       31.2,
       751.2
      ],
      [
       14.3,
       24.3,
       737.2
      ],
      [
       31.1,
       81.4,
       718.7
      ],
      [
       11.4,
       18.1,
       714.6
      ],
      [
       16.9,
       35.2,
       714.1
      ],
      [
       13.8,
       24.0,
       706.6
      ],
      [
       35.5,
       63.5,
       702.1
      ],
      [
       11.8,
       22.6,
       698.0
      ],
      [
       19.2,
       29.7,
       696.9
      ],
      [
       30.9,
       50.3,
       690.4
      ],
      [
       38.0,
       72.7,
       687.3
      ],
      [
       13.2,
       23.2,
       685.0
      ],
      [
       22.2,
       25.5,
       672.4
      ],
      [
       15.4,
       29.2,
       671.0
      ],
      [
       11.6,
       22.8,
       666.8
      ],
      [
       37.3,
       72.4,
       659.4
      ],
      [
       25.8,
       51.0,
       644.0
      ],
      [
       17.0,
       32.7,
       627.3
      ],
      [
       10.1,
       16.0,
       622.4
      ],
      [
       11.8,
       22.2,
       620.3
      ],
      [
       12.5,
       27.2,
       615.4
      ],
      [
       19.7,
       37.0,
       614.3
      ],
      [
       14.9,
       34.5,
       614.1
      ],
      [
       12.6,
       23.4,
       607.7
      ],
      [
       13.7,
       27.2,
       606.6
      ],
      [
       16.9,
       34.0,
       601.6
      ],
      [
       15.6,
       30.4,
       592.7
      ],
      [
       17.2,
       36.0,
       589.8
      ],
      [
       17.6,
       34.1,
       582.5
      ],
      [
       26.8,
       50.2,
       580.1
      ],
      [
       17.1,
       24.1,
       574.5
      ],
      [
       15.0,
       29.9,
       570.6
      ],
      [
       24.9,
       55.1,
       568.2
      ],
      [
       14.5,
       24.6,
       562.6
      ],
      [
       34.0,
       85.7,
       543.7
      ],
      [
       14.5,
       24.1,
       543.0
      ],
      [
       17.1,
       39.2,
       540.9
      ],
      [
       10.8,
       21.6,
       540.3
      ],
      [
       15.8,
       30.9,
       539.8
      ],
      [
       16.4,
       30.7,
       527.7
      ],
      [
       33.6,
       68.8,
       520.3
      ],
      [
       33.4,
       71.6,
       519.9
      ],
      [
       15.0,
       29.4,
       519.7
      ],
      [
       12.9,
       24.9,
       517.1
      ],
      [
       26.5,
       56.9,
       515.6
      ],
      [
       36.0,
       71.2,
       514.3
      ],
      [
       18.3,
       39.6,
       512.4
      ],
      [
       29.2,
       62.2,
       504.1
      ],
      [
       15.2,
       26.9,
       503.9
      ],
      [
       16.9,
       32.7,
       498.7
      ],
      [
       15.4,
       28.9,
       496.3
      ],
      [
       10.3,
       15.5,
       494.3
      ],
      [
       21.4,
       47.1,
       490.1
      ],
      [
       19.0,
       38.7,
       489.2
      ],
      [
       11.3,
       23.2,
       488.9
      ],
      [
       40.9,
       74.0,
       488.2
      ],
      [
       12.0,
       22.0,
       481.0
      ],
      [
       17.9,
       38.2,
       478.8
      ],
      [
       27.1,
       54.9,
       478.7
      ],
      [
       24.3,
       47.5,
       476.8
      ],
      [
       23.4,
       45.8,
       467.9
      ],
      [
       12.9,
       26.2,
       466.7
      ],
      [
       17.3,
       27.7,
       462.0
      ],
      [
       13.0,
       26.3,
       459.7
      ],
      [
       47.0,
       77.7,
       458.7
      ],
      [
       22.3,
       26.0,
       458.5
      ],
      [
       19.2,
       37.2,
       456.6
      ],
      [
       14.2,
       22.8,
       456.0
      ],
      [
       31.3,
       57.1,
       454.7
      ],
      [
       10.7,
       20.3,
       452.9
      ],
      [
       29.9,
       54.0,
       452.3
      ],
      [
       39.6,
       85.9,
       449.8
      ],
      [
       17.4,
       31.6,
       448.6
      ],
      [
       46.5,
       92.7,
       448.4
      ],
      [
       32.3,
       71.8,
       445.5
      ],
      [
       16.5,
       35.8,
       443.8
      ],
      [
       25.1,
       46.5,
       442.8
      ],
      [
       19.9,
       40.2,
       439.9
      ],
      [
       23.0,
       55.3,
       438.4
      ],
      [
       11.0,
       21.4,
       437.5
      ],
      [
       30.8,
       61.8,
       431.9
      ],
      [
       35.6,
       58.3,
       431.8
      ],
      [
       14.3,
       32.3,
       431.4
      ],
      [
       32.5,
       68.6,
       428.4
      ],
      [
       19.6,
       37.4,
       428.4
      ],
      [
       42.1,
       81.3,
       426.2
      ],
      [
       17.7,
       35.8,
       423.2
      ],
      [
       19.5,
       41.3,
       422.6
      ],
      [
       11.7,
       18.2,
       421.9
      ],
      [
       25.2,
       47.6,
       421.1
      ],
      [
       10.7,
       19.0,
       419.2
      ],
      [
       22.6,
       53.4,
       411.0
      ],
      [
       42.8,
       73.5,
       410.3
      ],
      [
       28.5,
       53.8,
       410.0
      ],
      [
       25.3,
       32.7,
       409.6
      ],
      [
       26.6,
       53.5,
       409.5
      ],
      [
       30.2,
       51.2,
       404.3
      ],
      [
       27.6,
       46.1,
       403.5
      ],
      [
       23.6,
       54.5,
       402.7
      ],
      [
       30.5,
       61.2,
       399.0
      ],
      [
       11.5,
       24.9,
       398.4
      ],
      [
       35.5,
       64.3,
       396.9
      ],
      [
       12.9,
       28.4,
       396.9
      ],
      [
       29.2,
       59.6,
       395.5
      ],
      [
       16.1,
       32.4,
       391.8
      ],
      [
       26.8,
       51.1,
       389.9
      ],
      [
       24.9,
       46.5,
       389.6
      ],
      [
       48.3,
       103.8,
       386.9
      ],
      [
       18.2,
       28.0,
       386.6
      ],
      [
       13.7,
       28.2,
       384.3
      ],
      [
       17.8,
       27.5,
       383.2
      ],
      [
       25.6,
       81.4,
       383.2
      ],
      [
       31.0,
       62.3,
       382.4
      ],
      [
       23.2,
       56.5,
       382.0
      ],
      [
       19.7,
       54.1,
       379.4
      ],
      [
       18.9,
       38.4,
       377.6
      ],
      [
       14.8,
       31.4,
       377.4
      ],
      [
       15.4,
       24.3,
       376.5
      ],
      [
       15.4,
       36.7,
       369.2
      ],
      [
       17.8,
       30.6,
       368.7
      ],
      [
       20.0,
       37.1,
       367.3
      ],
      [
       24.7,
       43.4,
       366.6
      ],
      [
       34.1,
       79.1,
       365.7
      ],
      [
       13.1,
       19.3,
       365.5
      ],
      [
       33.9,
       74.5,
       363.3
      ],
      [
       14.1,
       28.2,
       362.7
      ],
      [
       10.5,
       20.9,
       356.4
      ],
      [
       13.5,
       21.4,
       355.0
      ],
      [
       19.0,
       39.1,
       353.0
      ],
      [
       23.3,
       52.3,
       352.5
      ],
      [
       15.6,
       17.1,
       352.1
      ],
      [
       28.6,
       50.6,
       350.1
      ],
      [
       17.6,
       37.0,
       348.3
      ],
      [
       20.9,
       44.8,
       347.8
      ],
      [
       42.3,
       71.4,
       346.3
      ],
      [
       31.7,
       71.2,
       346.1
      ],
      [
       29.7,
       63.5,
       345.7
      ],
      [
       17.6,
       32.0,
       340.6
      ],
      [
       18.5,
       41.8,
       340.0
      ],
      [
       26.0,
       50.6,
       339.6
      ],
      [
       44.6,
       83.0,
       338.3
      ],
      [
       18.7,
       45.7,
       336.5
      ],
      [
       25.7,
       54.3,
       336.5
      ],
      [
       40.2,
       79.4,
       335.5
      ],
      [
       29.5,
       52.0,
       335.0
      ],
      [
       31.2,
       60.6,
       333.8
      ],
      [
       43.3,
       87.7,
       333.6
      ],
      [
       39.0,
       74.5,
       333.5
      ],
      [
       18.9,
       31.4,
       332.2
      ],
      [
       37.6,
       82.7,
       331.5
      ],
      [
       29.4,
       47.6,
       331.5
      ],
      [
       28.9,
       64.4,
       330.5
      ],
      [
       27.0,
       52.4,
       329.9
      ],
      [
       28.6,
       43.5,
       329.1
      ],
      [
       34.3,
       65.5,
       328.2
      ],
      [
       28.7,
       54.2,
       328.0
      ],
      [
       25.4,
       54.2,
       326.5
      ],
      [
       42.6,
       67.1,
       323.5
      ],
      [
       12.5,
       24.0,
       322.3
      ],
      [
       10.2,
       19.2,
       322.1
      ],
      [
       31.9,
       64.3,
       321.4
      ],
      [
       17.1,
       34.1,
       318.2
      ],
      [
       27.6,
       47.8,
       317.7
      ],
      [
       34.1,
       80.6,
       311.9
      ],
      [
       48.1,
       94.0,
       310.7
      ],
      [
       13.5,
       26.4,
       309.9
      ],
      [
       32.7,
       60.2,
       307.1
      ],
      [
       35.0,
       69.8,
       306.3
      ],
      [
       12.8,
       25.1,
       305.1
      ],
      [
       19.6,
       35.8,
       304.4
      ],
      [
       26.1,
       53.0,
       304.2
      ],
      [
       22.6,
       52.3,
       303.6
      ],
      [
       33.0,
       62.6,
       303.4
      ],
      [
       40.1,
       77.0,
       302.8
      ],
      [
       31.1,
       68.8,
       302.3
      ],
      [
       39.2,
       72.2,
       300.8
      ],
      [
       13.5,
       19.0,
       299.5
      ],
      [
       19.7,
       48.9,
       299.2
      ],
      [
       24.7,
       56.4,
       298.9
      ],
      [
       24.2,
       47.2,
       298.6
      ],
      [
       28.9,
       54.3,
       297.1
      ],
      [
       23.4,
       54.1,
       296.5
      ],
      [
       23.8,
       57.7,
       296.0
      ],
      [
       41.6,
       86.8,
       295.0
      ],
      [
       36.6,
       70.0,
       294.0
      ],
      [
       14.4,
       33.8,
       292.7
      ],
      [
       42.5,
       85.7,
       291.8
      ],
      [
       24.7,
       46.0,
       290.8
      ],
      [
       11.0,
       21.3,
       290.5
      ],
      [
       26.7,
       60.2,
       289.4
      ],
      [
       29.1,
       52.7,
       288.9
      ],
      [
       34.9,
       74.6,
       288.6
      ],
      [
       15.3,
       35.0,
       284.7
      ],
      [
       18.5,
       38.6,
       283.1
      ],
      [
       9.9,
       18.9,
       282.6
      ],
      [
       17.8,
       42.7,
       282.2
      ],
      [
       20.9,
       42.2,
       281.8
      ],
      [
       18.3,
       38.3,
       281.7
      ],
      [
       23.6,
       57.4,
       280.3
      ],
      [
       27.4,
       56.7,
       278.1
      ],
      [
       12.4,
       24.5,
       274.9
      ],
      [
       37.5,
       83.0,
       274.4
      ],
      [
       32.3,
       68.0,
       273.4
      ],
      [
       18.3,
       34.6,
       273.2
      ],
      [
       29.0,
       46.0,
       272.4
      ],
      [
       46.6,
       76.5,
       271.8
      ],
      [
       42.3,
       79.0,
       271.3
      ],
      [
       34.9,
       61.4,
       271.0
      ],
      [
       16.0,
       31.8,
       270.6
      ],
      [
       13.1,
       24.6,
       270.2
      ],
      [
       29.9,
       44.1,
       270.1
      ],
      [
       46.1,
       98.2,
       269.7
      ],
      [
       31.8,
       62.1,
       269.7
      ],
      [
       42.2,
       83.6,
       268.9
      ],
      [
       15.6,
       17.1,
       268.5
      ],
      [
       29.2,
       55.2,
       267.8
      ],
      [
       23.9,
       37.0,
       264.3
      ],
      [
       25.9,
       60.4,
       263.3
      ],
      [
       23.6,
       51.4,
       262.3
      ],
      [
       21.1,
       42.2,
       261.5
      ],
      [
       27.4,
       49.4,
       261.2
      ],
      [
       17.4,
       34.8,
       260.2
      ],
      [
       11.5,
       17.5,
       259.7
      ],
      [
       13.2,
       29.1,
       258.2
      ],
      [
       46.9,
       79.4,
       257.3
      ],
      [
       22.2,
       46.5,
       256.8
      ],
      [
       36.2,
       75.8,
       255.1
      ],
      [
       44.8,
       78.2,
       254.4
      ],
      [
       49.9,
       103.2,
       253.6
      ],
      [
       49.4,
       89.0,
       253.1
      ],
      [
       9.2,
       15.8,
       252.2
      ],
      [
       30.1,
       49.4,
       251.6
      ],
      [
       14.6,
       29.9,
       251.5
      ],
      [
       23.7,
       56.6,
       250.1
      ],
      [
       24.4,
       37.3,
       248.3
      ],
      [
       31.0,
       48.8,
       247.4
      ],
      [
       18.6,
       34.8,
       244.8
      ],
      [
       14.4,
       28.9,
       243.9
      ],
      [
       23.7,
       44.1,
       243.6
      ],
      [
       30.3,
       55.0,
       243.6
      ],
      [
       15.0,
       29.2,
       243.6
      ],
      [
       21.9,
       41.8,
       243.0
      ],
      [
       37.0,
       77.9,
       242.3
      ],
      [
       25.3,
       43.4,
       242.2
      ],
      [
       30.5,
       61.5,
       241.4
      ],
      [
       14.9,
       30.4,
       241.0
      ],
      [
       47.3,
       91.5,
       240.6
      ],
      [
       17.3,
       39.4,
       240.0
      ],
      [
       33.3,
       65.0,
       238.3
      ],
      [
       36.4,
       72.1,
       236.1
      ],
      [
       17.2,
       24.2,
       235.8
      ],
      [
       27.6,
       46.3,
       234.9
      ],
      [
       31.0,
       52.5,
       234.7
      ],
      [
       25.7,
       46.3,
       234.6
      ],
      [
       21.1,
       46.7,
       233.6
      ],
      [
       30.9,
       67.6,
       233.3
      ],
      [
       19.8,
       43.3,
       231.7
      ],
      [
       26.0,
       61.4,
       231.5
      ],
      [
       53.4,
       99.5,
       230.9
      ],
      [
       23.5,
       48.0,
       228.8
      ],
      [
       11.4,
       25.4,
       228.3
      ],
      [
       19.9,
       41.6,
       228.1
      ],
      [
       25.2,
       62.8,
       227.0
      ],
      [
       32.4,
       79.2,
       226.3
      ],
      [
       16.8,
       36.1,
       225.6
      ],
      [
       31.4,
       59.0,
       225.4
      ],
      [
       21.2,
       52.0,
       225.1
      ],
      [
       35.0,
       64.8,
       224.1
      ],
      [
       12.3,
       24.1,
       223.2
      ],
      [
       40.6,
       94.3,
       222.3
      ],
      [
       15.4,
       32.1,
       222.1
      ],
      [
       37.2,
       70.7,
       221.0
      ],
      [
       12.6,
       25.9,
       220.4
      ],
      [
       14.8,
       24.2,
       219.8
      ],
      [
       14.4,
       22.4,
       218.7
      ],
      [
       25.8,
       52.8,
       218.3
      ],
      [
       33.1,
       75.5,
       217.8
      ],
      [
       40.1,
       68.5,
       217.1
      ],
      [
       16.3,
       30.8,
       216.9
      ],
      [
       41.4,
       104.0,
       216.3
      ],
      [
       39.8,
       61.0,
       215.9
      ],
      [
       31.3,
       71.9,
       215.8
      ],
      [
       48.9,
       96.9,
       215.6
      ],
      [
       29.4,
       53.9,
       215.3
      ],
      [
       28.0,
       67.0,
       214.1
      ],
      [
       24.2,
       51.6,
       214.0
      ],
      [
       12.8,
       26.0,
       213.2
      ],
      [
       34.4,
       72.4,
       212.7
      ],
      [
       43.2,
       78.5,
       212.0
      ],
      [
       34.0,
       93.1,
       211.8
      ],
      [
       38.7,
       63.9,
       211.3
      ],
      [
       24.0,
       50.2,
       211.2
      ],
      [
       29.2,
       61.1,
       210.7
      ],
      [
       29.3,
       57.8,
       209.8
      ],
      [
       23.6,
       43.2,
       209.0
      ],
      [
       21.5,
       51.2,
       208.2
      ],
      [
       51.1,
       102.7,
       208.1
      ],
      [
       34.2,
       61.3,
       207.6
      ],
      [
       50.0,
       86.5,
       207.5
      ],
      [
       15.6,
       30.0,
       206.7
      ],
      [
       43.4,
       82.2,
       206.4
      ],
      [
       25.5,
       44.2,
       206.2
      ],
      [
       20.9,
       50.9,
       206.2
      ],
      [
       22.3,
       44.3,
       206.1
      ],
      [
       38.8,
       66.5,
       206.0
      ],
      [
       26.5,
       55.3,
       205.9
      ],
      [
       42.7,
       96.3,
       205.6
      ],
      [
       30.1,
       56.6,
       205.0
      ],
      [
       26.0,
       41.6,
       204.7
      ],
      [
       33.9,
       75.6,
       204.3
      ],
      [
       33.3,
       56.6,
       204.3
      ],
      [
       41.5,
       78.0,
       204.0
      ],
      [
       39.9,
       77.3,
       203.9
      ],
      [
       24.0,
       57.1,
       203.8
      ],
      [
       35.0,
       91.5,
       203.7
      ],
      [
       25.5,
       43.6,
       203.5
      ],
      [
       20.5,
       42.6,
       203.4
      ],
      [
       39.1,
       74.0,
       203.4
      ],
      [
       23.6,
       46.8,
       203.2
      ],
      [
       47.6,
       84.4,
       202.3
      ],
      [
       31.7,
       67.5,
       201.9
      ],
      [
       33.9,
       58.4,
       201.7
      ],
      [
       26.3,
       54.3,
       201.5
      ],
      [
       14.7,
       26.2,
       201.5
      ],
      [
       14.7,
       27.0,
       201.2
      ],
      [
       21.7,
       42.8,
       200.7
      ],
      [
       34.5,
       61.8,
       200.5
      ],
      [
       39.1,
       82.2,
       200.3
      ],
      [
       34.4,
       85.6,
       199.7
      ],
      [
       15.0,
       27.0,
       199.4
      ],
      [
       14.3,
       30.9,
       199.3
      ],
      [
       31.7,
       55.4,
       198.8
      ],
      [
       33.3,
       56.4,
       197.7
      ],
      [
       38.3,
       77.4,
       197.7
      ],
      [
       25.7,
       48.8,
       196.4
      ],
      [
       31.4,
       69.6,
       195.7
      ],
      [
       35.9,
       67.0,
       195.6
      ],
      [
       14.9,
       33.0,
       195.3
      ],
      [
       16.9,
       42.0,
       194.7
      ],
      [
       12.1,
       26.4,
       194.6
      ],
      [
       39.2,
       76.1,
       194.1
      ],
      [
       16.9,
       34.1,
       193.8
      ],
      [
       43.2,
       100.1,
       193.0
      ],
      [
       25.1,
       45.7,
       192.7
      ],
      [
       51.8,
       98.6,
       192.4
      ],
      [
       15.8,
       32.5,
       192.2
      ],
      [
       40.7,
       81.0,
       191.6
      ],
      [
       20.0,
       41.7,
       191.5
      ],
      [
       32.5,
       58.7,
       190.6
      ],
      [
       41.1,
       88.2,
       190.5
      ],
      [
       29.4,
       61.8,
       190.5
      ],
      [
       37.2,
       78.3,
       190.5
      ],
      [
       36.5,
       84.6,
       190.2
      ],
      [
       14.8,
       33.7,
       190.2
      ],
      [
       34.1,
       57.8,
       189.6
      ],
      [
       19.1,
       42.1,
       189.4
      ],
      [
       54.6,
       108.3,
       188.8
      ],
      [
       24.1,
       52.8,
       188.6
      ],
      [
       22.4,
       44.8,
       188.5
      ],
      [
       46.8,
       84.5,
       187.6
      ],
      [
       54.8,
       86.5,
       187.3
      ],
      [
       32.4,
       63.9,
       186.9
      ],
      [
       29.6,
       57.4,
       186.9
      ],
      [
       35.2,
       64.1,
       186.9
      ],
      [
       16.0,
       37.8,
       186.8
      ],
      [
       39.0,
       74.2,
       186.4
      ],
      [
       55.7,
       97.4,
       186.4
      ],
      [
       36.3,
       84.8,
       186.2
      ],
      [
       40.9,
       81.6,
       185.9
      ],
      [
       20.7,
       40.7,
       185.7
      ],
      [
       25.1,
       45.0,
       185.5
      ],
      [
       16.7,
       39.8,
       185.4
      ],
      [
       18.1,
       31.4,
       185.1
      ],
      [
       28.6,
       54.9,
       184.5
      ],
      [
       52.0,
       92.0,
       184.1
      ],
      [
       40.5,
       85.6,
       183.3
      ],
      [
       49.0,
       87.8,
       183.3
      ],
      [
       14.4,
       29.6,
       183.2
      ],
      [
       42.7,
       83.0,
       183.0
      ],
      [
       27.0,
       68.7,
       182.4
      ],
      [
       32.2,
       66.2,
       182.4
      ],
      [
       47.3,
       90.8,
       181.8
      ],
      [
       39.5,
       77.4,
       181.2
      ],
      [
       28.8,
       64.3,
       181.2
      ],
      [
       30.7,
       69.0,
       181.1
      ],
      [
       27.1,
       57.4,
       180.8
      ],
      [
       25.2,
       65.9,
       179.9
      ],
      [
       26.7,
       48.9,
       179.7
      ],
      [
       21.8,
       35.5,
       179.6
      ],
      [
       43.8,
       92.6,
       179.5
      ],
      [
       26.8,
       59.6,
       179.5
      ],
      [
       20.4,
       46.4,
       179.5
      ],
      [
       41.7,
       91.4,
       179.2
      ],
      [
       22.1,
       54.4,
       178.4
      ],
      [
       35.2,
       64.8,
       177.9
      ],
      [
       37.5,
       61.2,
       177.9
      ],
      [
       21.4,
       47.4,
       177.4
      ],
      [
       34.1,
       51.0,
       177.3
      ],
      [
       36.2,
       112.9,
       177.0
      ],
      [
       12.8,
       29.5,
       176.7
      ],
      [
       52.6,
       94.5,
       176.2
      ],
      [
       43.3,
       88.2,
       176.0
      ],
      [
       13.2,
       21.1,
       175.3
      ],
      [
       21.1,
       44.9,
       175.0
      ],
      [
       26.6,
       57.0,
       174.5
      ],
      [
       13.0,
       26.6,
       173.9
      ],
      [
       13.5,
       31.4,
       173.6
      ],
      [
       32.4,
       69.0,
       173.5
      ],
      [
       29.8,
       60.7,
       173.4
      ],
      [
       26.1,
       56.0,
       173.2
      ],
      [
       16.9,
       26.6,
       173.1
      ],
      [
       28.3,
       63.1,
       173.1
      ],
      [
       28.7,
       54.3,
       173.0
      ],
      [
       33.3,
       67.0,
       173.0
      ],
      [
       16.9,
       40.7,
       173.0
      ],
      [
       49.3,
       99.5,
       173.0
      ],
      [
       21.3,
       42.6,
       172.3
      ],
      [
       37.2,
       93.0,
       172.0
      ],
      [
       34.0,
       62.5,
       171.6
      ],
      [
       45.7,
       113.8,
       171.3
      ],
      [
       48.7,
       89.9,
       171.3
      ],
      [
       41.0,
       77.7,
       171.2
      ],
      [
       18.3,
       24.7,
       171.0
      ],
      [
       54.5,
       99.0,
       170.7
      ],
      [
       20.0,
       46.9,
       170.0
      ],
      [
       23.5,
       50.3,
       169.8
      ],
      [
       17.6,
       40.7,
       169.6
      ],
      [
       31.3,
       77.5,
       169.4
      ],
      [
       16.3,
       33.8,
       169.2
      ],
      [
       36.1,
       93.1,
       168.9
      ],
      [
       16.4,
       35.8,
       168.6
      ],
      [
       28.6,
       68.6,
       168.1
      ],
      [
       29.1,
       86.0,
       168.1
      ],
      [
       10.4,
       18.2,
       167.9
      ],
      [
       15.2,
       33.7,
       167.5
      ],
      [
       39.8,
       62.8,
       167.2
      ],
      [
       40.5,
       87.9,
       166.7
      ],
      [
       34.6,
       73.5,
       166.7
      ],
      [
       21.2,
       35.6,
       166.1
      ],
      [
       45.9,
       92.3,
       165.5
      ],
      [
       56.4,
       112.0,
       165.4
      ],
      [
       34.0,
       98.0,
       165.4
      ],
      [
       15.8,
       33.8,
       164.6
      ],
      [
       13.7,
       33.0,
       163.9
      ],
      [
       20.8,
       46.1,
       163.8
      ],
      [
       12.2,
       23.3,
       163.6
      ],
      [
       31.9,
       72.8,
       163.5
      ],
      [
       25.6,
       50.7,
       163.3
      ],
      [
       32.6,
       69.8,
       163.0
      ],
      [
       40.8,
       78.5,
       162.2
      ],
      [
       32.0,
       68.0,
       161.5
      ],
      [
       33.3,
       64.2,
       161.5
      ],
      [
       31.7,
       71.0,
       161.5
      ],
      [
       25.0,
       54.7,
       161.4
      ],
      [
       46.1,
       87.0,
       160.9
      ],
      [
       24.2,
       55.1,
       160.0
      ],
      [
       26.1,
       39.7,
       159.7
      ],
      [
       27.5,
       53.4,
       159.5
      ],
      [
       28.2,
       51.4,
       159.4
      ],
      [
       31.3,
       72.3,
       159.3
      ],
      [
       33.5,
       53.0,
       158.2
      ],
      [
       47.5,
       82.8,
       158.2
      ],
      [
       31.2,
       57.2,
       157.9
      ],
      [
       17.8,
       33.0,
       157.8
      ],
      [
       31.3,
       70.6,
       157.5
      ],
      [
       21.2,
       45.2,
       157.3
      ],
      [
       15.2,
       30.2,
       157.3
      ],
      [
       42.2,
       95.0,
       156.5
      ],
      [
       28.5,
       41.1,
       155.8
      ],
      [
       34.7,
       74.4,
       155.6
      ],
      [
       31.3,
       50.9,
       155.4
      ],
      [
       31.5,
       54.8,
       155.2
      ],
      [
       40.2,
       92.7,
       155.1
      ],
      [
       30.6,
       83.6,
       154.9
      ],
      [
       20.9,
       37.8,
       154.5
      ],
      [
       49.0,
       90.2,
       154.5
      ],
      [
       31.9,
       64.6,
       154.1
      ],
      [
       19.1,
       44.6,
       153.6
      ],
      [
       28.3,
       51.8,
       152.4
      ],
      [
       12.5,
       26.6,
       152.3
      ],
      [
       28.7,
       53.8,
       152.3
      ],
      [
       44.4,
       90.8,
       151.5
      ],
      [
       31.1,
       59.0,
       151.3
      ],
      [
       25.1,
       67.8,
       151.2
      ],
      [
       22.0,
       60.4,
       150.6
      ],
      [
       20.7,
       46.1,
       150.2
      ],
      [
       18.0,
       40.1,
       149.8
      ],
      [
       23.5,
       48.5,
       148.6
      ],
      [
       27.9,
       66.8,
       148.5
      ],
      [
       14.4,
       31.5,
       148.2
      ],
      [
       34.3,
       63.6,
       147.4
      ],
      [
       18.1,
       34.0,
       147.2
      ],
      [
       22.4,
       48.2,
       146.3
      ],
      [
       20.0,
       28.6,
       146.1
      ],
      [
       14.7,
       30.9,
       145.2
      ],
      [
       24.0,
       49.4,
       145.0
      ],
      [
       46.5,
       88.6,
       144.6
      ],
      [
       25.7,
       50.1,
       143.8
      ],
      [
       27.9,
       52.5,
       143.2
      ],
      [
       54.2,
       100.8,
       142.8
      ],
      [
       17.5,
       34.2,
       142.2
      ],
      [
       29.5,
       57.7,
       142.1
      ],
      [
       24.7,
       51.0,
       142.1
      ],
      [
       17.6,
       37.6,
       141.5
      ],
      [
       21.7,
       45.2,
       141.1
      ],
      [
       22.4,
       44.0,
       140.8
      ],
      [
       36.9,
       71.0,
       140.6
      ],
      [
       20.9,
       35.3,
       140.1
      ],
      [
       40.2,
       87.5,
       139.1
      ],
      [
       27.8,
       63.6,
       139.1
      ],
      [
       22.8,
       51.9,
       136.6
      ],
      [
       21.6,
       50.3,
       136.6
      ],
      [
       43.3,
       99.4,
       135.8
      ],
      [
       39.9,
       69.8,
       135.1
      ],
      [
       42.8,
       111.8,
       132.9
      ],
      [
       29.8,
       86.0,
       132.9
      ],
      [
       37.4,
       60.8,
       131.1
      ],
      [
       28.3,
       59.3,
       130.6
      ],
      [
       25.2,
       56.8,
       130.3
      ],
      [
       20.2,
       46.1,
       129.1
      ],
      [
       35.0,
       92.4,
       128.8
      ],
      [
       25.0,
       62.7,
       128.8
      ],
      [
       16.9,
       27.2,
       125.9
      ],
      [
       33.9,
       67.2,
       125.8
      ],
      [
       47.1,
       81.4,
       125.8
      ],
      [
       34.9,
       112.6,
       124.6
      ],
      [
       30.8,
       67.6,
       122.4
      ],
      [
       54.8,
       104.8,
       122.4
      ],
      [
       34.5,
       61.3,
       122.0
      ],
      [
       36.2,
       61.1,
       121.7
      ],
      [
       25.8,
       54.6,
       120.0
      ],
      [
       24.5,
       57.8,
       119.6
      ],
      [
       45.0,
       94.6,
       118.8
      ],
      [
       32.2,
       52.6,
       118.8
      ],
      [
       46.9,
       98.0,
       118.6
      ],
      [
       15.1,
       36.6,
       117.9
      ],
      [
       52.6,
       99.4,
       117.8
      ],
      [
       26.0,
       54.6,
       115.5
      ],
      [
       38.5,
       72.6,
       115.5
      ],
      [
       26.3,
       61.6,
       115.5
      ],
      [
       20.0,
       38.8,
       115.5
      ],
      [
       18.1,
       39.2,
       115.5
      ],
      [
       37.6,
       58.2,
       114.2
      ],
      [
       25.5,
       66.4,
       113.9
      ],
      [
       20.3,
       39.5,
       113.4
      ],
      [
       32.3,
       69.0,
       113.4
      ],
      [
       32.5,
       64.6,
       113.4
      ],
      [
       29.5,
       56.5,
       113.4
      ],
      [
       27.9,
       64.4,
       113.4
      ],
      [
       18.9,
       43.1,
       113.4
      ],
      [
       20.5,
       40.0,
       112.0
      ],
      [
       33.0,
       75.6,
       112.0
      ],
      [
       48.2,
       98.4,
       112.0
      ],
      [
       46.5,
       96.2,
       112.0
      ],
      [
       26.2,
       39.3,
       112.0
      ],
      [
       42.8,
       98.4,
       112.0
      ],
      [
       19.8,
       41.0,
       112.0
      ],
      [
       51.0,
       101.9,
       112.0
      ],
      [
       17.4,
       33.4,
       112.0
      ],
      [
       17.4,
       33.8,
       112.0
      ],
      [
       24.4,
       62.0,
       111.0
      ],
      [
       21.3,
       39.8,
       111.0
      ],
      [
       31.5,
       55.8,
       110.8
      ],
      [
       42.0,
       78.2,
       110.3
      ],
      [
       32.8,
       63.8,
       110.3
      ],
      [
       40.4,
       63.4,
       110.1
      ],
      [
       20.0,
       46.2,
       109.2
      ],
      [
       44.2,
       93.8,
       109.2
      ],
      [
       14.0,
       30.2,
       109.2
      ],
      [
       13.9,
       31.4,
       109.2
      ]
     ],
     "linee": [
      {
       "k": 1.5,
       "label": "1,5 volte"
      },
      {
       "k": 2.0,
       "label": "il doppio"
      }
     ],
     "nota": "Ogni punto è una coppia di zone, grande quanto le auto del mattino. Sono le 600 coppie con più auto (83,2% delle auto). Sopra una linea il mezzo pubblico impiega più di quel multiplo dell'auto."
    },
    {
     "tipo": "barre",
     "titolo": "Le 15 coppie con più auto dove i mezzi pubblici impiegano più del doppio",
     "unita": "auto",
     "nota": "Auto del mattino su quella coppia (dalle 6 alle 10, giorno feriale), con il fattore basso 2,1. A destra i minuti coi mezzi contro quelli in auto.",
     "voci": [
      {
       "label": "Torino, Madonna Del Pilone → Torino, Vanchiglia",
       "valore": 894,
       "tono": "rosso",
       "testo": "894 auto: 35 contro 16 min"
      },
      {
       "label": "Torino, Parella → Torino, San Paolo",
       "valore": 763,
       "tono": "rosso",
       "testo": "763 auto: 30 contro 15 min"
      },
      {
       "label": "Torino, Madonna Del Pilone → Torino, Centro",
       "valore": 753,
       "tono": "rosso",
       "testo": "753 auto: 50 contro 23 min"
      },
      {
       "label": "Torino, Mirafiori Sud → Rivoli",
       "valore": 719,
       "tono": "rosso",
       "testo": "719 auto: 81 contro 31 min"
      },
      {
       "label": "Grugliasco → Torino, Pozzo Strada",
       "valore": 714,
       "tono": "rosso",
       "testo": "714 auto: 35 contro 17 min"
      },
      {
       "label": "Torino, Vanchiglia → Torino, Aurora",
       "valore": 615,
       "tono": "rosso",
       "testo": "615 auto: 27 contro 12 min"
      },
      {
       "label": "Torino, Barriera di Milano → Torino, Vanchiglia",
       "valore": 614,
       "tono": "rosso",
       "testo": "614 auto: 34 contro 15 min"
      },
      {
       "label": "Venaria Reale → Torino, Madonna di Campagna",
       "valore": 602,
       "tono": "rosso",
       "testo": "602 auto: 34 contro 17 min"
      },
      {
       "label": "Torino, Centro → Torino, Borgata Vittoria",
       "valore": 590,
       "tono": "rosso",
       "testo": "590 auto: 36 contro 17 min"
      },
      {
       "label": "Moncalieri → Torino, Mirafiori Sud",
       "valore": 568,
       "tono": "rosso",
       "testo": "568 auto: 55 contro 25 min"
      },
      {
       "label": "Settimo Torinese → Torino, Madonna Del Pilone",
       "valore": 544,
       "tono": "rosso",
       "testo": "544 auto: 86 contro 34 min"
      },
      {
       "label": "Torino, Borgata Vittoria → Torino, Centro",
       "valore": 541,
       "tono": "rosso",
       "testo": "541 auto: 39 contro 17 min"
      },
      {
       "label": "Torino, Madonna di Campagna → Torino, Borgata Vittoria",
       "valore": 540,
       "tono": "rosso",
       "testo": "540 auto: 22 contro 11 min"
      },
      {
       "label": "Beinasco → Torino, Centro",
       "valore": 520,
       "tono": "rosso",
       "testo": "520 auto: 69 contro 34 min"
      },
      {
       "label": "Torino, Mirafiori Nord → Moncalieri",
       "valore": 520,
       "tono": "rosso",
       "testo": "520 auto: 72 contro 33 min"
      }
     ]
    }
   ],
   "calcolo": [
    "Le zone sono quelle dell'indagine sugli spostamenti 2022 con punti di calcolo; ognuna ha fino a 5 punti.",
    "Mezzi pubblici: a piedi, bus, tram e metro, con partenza fra le 7:45 e le 8:15. Si prende la mediana.",
    "Auto: tempo a flusso libero per un fattore di punta, più 5 minuti. I fattori sono due: 2,1 da Google Maps e 1,2 dai sensori.",
    "Rapporto = tempo coi mezzi diviso tempo in auto. Le fasce sono fisse e decise prima di vedere i numeri.",
    "Le auto di una coppia sono i viaggi in auto dell'indagine, in partenza dalle 6 alle 10 di un feriale."
   ],
   "criteri": [
    [
     "Zone",
     "71 zone dell'indagine sugli spostamenti (23 di Torino), fino a 5 punti ciascuna"
    ],
    [
     "Mezzi pubblici",
     "partenza 07:45-8:15 di un feriale, mediana, cammino a 4,8 km/h, al massimo 120 minuti"
    ],
    [
     "Auto, limite alto",
     "tempo a flusso libero × 1,2 (sensori 5T) + 5 minuti"
    ],
    [
     "Auto, limite basso",
     "tempo a flusso libero × 2,1 (Google Maps, 6 percorsi) + 5 minuti"
    ],
    [
     "Fasce del rapporto",
     "sotto 1,5, 1,5-2, 2-3, oltre 3 (fissate prima dei numeri)"
    ]
   ],
   "limiti": [
    "Fuori Torino mancano treni e altre aziende: le coppie fra comuni della cintura non sono nel numero.",
    "La nostra rete stradale non conta semafori e incroci. I tempi in auto sono stimati fra il rallentamento misurato dai sensori e quello di Google Maps.",
    "Senza i treni metropolitani, dove ci sono, i mezzi pubblici risultano più lenti del vero. L'orario è quello programmato.",
    "L'indagine è un campione. I viaggi dentro una zona e 653 coppie senza collegamento (5.616 auto) non sono nel confronto."
   ],
   "english": [
    "Question: for which trips is the car much faster than public transport, and how many cars make them?",
    "Answer: in the morning public transport takes 2.0 to 2.9 times as long as the car (weighted median). For 41% to 97% of cars it takes more than twice as long.",
    "Limit: car times lie between the slowdown measured by sensors (1.2) and by Google Maps (2.1). Without metropolitan trains, public transport looks slower than it is."
   ],
   "extra": {
    "titolo": "Strade grandi e fermate vicine",
    "punto": "Il 95,3% dei km di strade grandi ha una fermata frequente vicina: la fermata c'è, ma non basta.",
    "grafico": {
     "tipo": "pila",
     "titolo": "Km di strade grandi di Torino: con o senza trasporto pubblico vicino",
     "unita": "km",
     "voci": [
      {
       "label": "con fermate frequenti vicine",
       "valore": 327.3,
       "tono": "verde"
      },
      {
       "label": "con poco trasporto pubblico",
       "valore": 16.0,
       "tono": "rosso"
      }
     ]
    }
   }
  },
  "forma_en": {
   "etichetta": "ESTIMATED / MEASURED / SCHEDULED",
   "titolo": "In the morning, public transport takes 2 to 3 times as long as the car",
   "domanda": "For which trips is the car much faster than public transport, and how many cars make them?",
   "numero": {
    "valore": "2–3",
    "unita": "times",
    "testo": "the car's travel time: median ratio, weighted by morning cars (220,307 cars)"
   },
   "principale": {
    "tipo": "barre_gruppi",
    "titolo": "Morning cars by ratio of public transport time to car time",
    "unita": "%",
    "max": 100,
    "nota": "Ratio 2 = public transport takes twice as long as the car. Turin–Turin and Turin–suburb pairs. Low limit: slow car as on Google Maps (factor 2.1); high limit: fast car as the sensors measure (factor 1.2).",
    "gruppi": [
     {
      "label": "under 1.5",
      "voci": [
       {
        "label": "low limit",
        "valore": 3.9,
        "tono": "verde",
        "testo": "3.9% (8,649 cars)"
       },
       {
        "label": "high limit",
        "valore": 0.0,
        "tono": "verde",
        "testo": "0% (0 cars)"
       }
      ]
     },
     {
      "label": "1.5-2",
      "voci": [
       {
        "label": "low limit",
        "valore": 54.6,
        "tono": "giallo",
        "testo": "54.6% (120,360 cars)"
       },
       {
        "label": "high limit",
        "valore": 3.0,
        "tono": "giallo",
        "testo": "3% (6,661 cars)"
       }
      ]
     },
     {
      "label": "2-3",
      "voci": [
       {
        "label": "low limit",
        "valore": 41.1,
        "tono": "arancio",
        "testo": "41.1% (90,508 cars)"
       },
       {
        "label": "high limit",
        "valore": 52.2,
        "tono": "arancio",
        "testo": "52.2% (115,033 cars)"
       }
      ]
     },
     {
      "label": "over 3",
      "voci": [
       {
        "label": "low limit",
        "valore": 0.4,
        "tono": "rosso",
        "testo": "0.4% (791 cars)"
       },
       {
        "label": "high limit",
        "valore": 44.8,
        "tono": "rosso",
        "testo": "44.8% (98,612 cars)"
       }
      ]
     }
    ]
   },
   "punti": [
    "Cars with a ratio above 2 are 41% with the low factor and 97% with the high factor.",
    "The 3 worst pairs: Torino, Madonna Del Pilone → Torino, Vanchiglia, Torino, Parella → Torino, San Paolo, Torino, Madonna Del Pilone → Torino, Centro.",
    "Google confirms the public transport times on the check routes: 31 versus 30-35 and 33 versus 30-35 minutes."
   ],
   "altri": [
    {
     "tipo": "dispersione",
     "titolo": "Car time and public transport time, one pair of zones per point",
     "xlabel": "minutes by car (peak hour, factor 2.1)",
     "ylabel": "minutes by public transport",
     "punti": [
      [
       12.7,
       20.6,
       1355.3
      ],
      [
       16.0,
       31.3,
       1341.8
      ],
      [
       10.6,
       19.2,
       1324.4
      ],
      [
       18.1,
       24.7,
       1277.0
      ],
      [
       12.0,
       18.7,
       1269.4
      ],
      [
       13.4,
       24.0,
       1208.2
      ],
      [
       23.2,
       43.0,
       1149.2
      ],
      [
       18.8,
       37.5,
       1107.8
      ],
      [
       47.5,
       80.1,
       1081.8
      ],
      [
       10.3,
       15.2,
       1038.1
      ],
      [
       16.8,
       33.2,
       969.9
      ],
      [
       18.7,
       30.6,
       968.1
      ],
      [
       10.6,
       15.2,
       957.2
      ],
      [
       27.2,
       44.5,
       940.7
      ],
      [
       12.6,
       20.2,
       938.8
      ],
      [
       17.0,
       33.5,
       928.7
      ],
      [
       19.1,
       38.2,
       916.7
      ],
      [
       35.6,
       63.4,
       910.0
      ],
      [
       15.7,
       30.4,
       900.6
      ],
      [
       15.5,
       35.2,
       894.4
      ],
      [
       11.8,
       22.4,
       893.3
      ],
      [
       13.0,
       23.8,
       889.9
      ],
      [
       22.8,
       39.3,
       888.0
      ],
      [
       18.3,
       27.5,
       818.9
      ],
      [
       22.1,
       42.3,
       796.7
      ],
      [
       18.0,
       35.2,
       795.1
      ],
      [
       10.3,
       18.9,
       789.0
      ],
      [
       19.7,
       31.2,
       779.1
      ],
      [
       15.1,
       30.4,
       762.5
      ],
      [
       22.8,
       50.0,
       753.4
      ],
      [
       15.8,
       31.2,
       751.2
      ],
      [
       14.3,
       24.3,
       737.2
      ],
      [
       31.1,
       81.4,
       718.7
      ],
      [
       11.4,
       18.1,
       714.6
      ],
      [
       16.9,
       35.2,
       714.1
      ],
      [
       13.8,
       24.0,
       706.6
      ],
      [
       35.5,
       63.5,
       702.1
      ],
      [
       11.8,
       22.6,
       698.0
      ],
      [
       19.2,
       29.7,
       696.9
      ],
      [
       30.9,
       50.3,
       690.4
      ],
      [
       38.0,
       72.7,
       687.3
      ],
      [
       13.2,
       23.2,
       685.0
      ],
      [
       22.2,
       25.5,
       672.4
      ],
      [
       15.4,
       29.2,
       671.0
      ],
      [
       11.6,
       22.8,
       666.8
      ],
      [
       37.3,
       72.4,
       659.4
      ],
      [
       25.8,
       51.0,
       644.0
      ],
      [
       17.0,
       32.7,
       627.3
      ],
      [
       10.1,
       16.0,
       622.4
      ],
      [
       11.8,
       22.2,
       620.3
      ],
      [
       12.5,
       27.2,
       615.4
      ],
      [
       19.7,
       37.0,
       614.3
      ],
      [
       14.9,
       34.5,
       614.1
      ],
      [
       12.6,
       23.4,
       607.7
      ],
      [
       13.7,
       27.2,
       606.6
      ],
      [
       16.9,
       34.0,
       601.6
      ],
      [
       15.6,
       30.4,
       592.7
      ],
      [
       17.2,
       36.0,
       589.8
      ],
      [
       17.6,
       34.1,
       582.5
      ],
      [
       26.8,
       50.2,
       580.1
      ],
      [
       17.1,
       24.1,
       574.5
      ],
      [
       15.0,
       29.9,
       570.6
      ],
      [
       24.9,
       55.1,
       568.2
      ],
      [
       14.5,
       24.6,
       562.6
      ],
      [
       34.0,
       85.7,
       543.7
      ],
      [
       14.5,
       24.1,
       543.0
      ],
      [
       17.1,
       39.2,
       540.9
      ],
      [
       10.8,
       21.6,
       540.3
      ],
      [
       15.8,
       30.9,
       539.8
      ],
      [
       16.4,
       30.7,
       527.7
      ],
      [
       33.6,
       68.8,
       520.3
      ],
      [
       33.4,
       71.6,
       519.9
      ],
      [
       15.0,
       29.4,
       519.7
      ],
      [
       12.9,
       24.9,
       517.1
      ],
      [
       26.5,
       56.9,
       515.6
      ],
      [
       36.0,
       71.2,
       514.3
      ],
      [
       18.3,
       39.6,
       512.4
      ],
      [
       29.2,
       62.2,
       504.1
      ],
      [
       15.2,
       26.9,
       503.9
      ],
      [
       16.9,
       32.7,
       498.7
      ],
      [
       15.4,
       28.9,
       496.3
      ],
      [
       10.3,
       15.5,
       494.3
      ],
      [
       21.4,
       47.1,
       490.1
      ],
      [
       19.0,
       38.7,
       489.2
      ],
      [
       11.3,
       23.2,
       488.9
      ],
      [
       40.9,
       74.0,
       488.2
      ],
      [
       12.0,
       22.0,
       481.0
      ],
      [
       17.9,
       38.2,
       478.8
      ],
      [
       27.1,
       54.9,
       478.7
      ],
      [
       24.3,
       47.5,
       476.8
      ],
      [
       23.4,
       45.8,
       467.9
      ],
      [
       12.9,
       26.2,
       466.7
      ],
      [
       17.3,
       27.7,
       462.0
      ],
      [
       13.0,
       26.3,
       459.7
      ],
      [
       47.0,
       77.7,
       458.7
      ],
      [
       22.3,
       26.0,
       458.5
      ],
      [
       19.2,
       37.2,
       456.6
      ],
      [
       14.2,
       22.8,
       456.0
      ],
      [
       31.3,
       57.1,
       454.7
      ],
      [
       10.7,
       20.3,
       452.9
      ],
      [
       29.9,
       54.0,
       452.3
      ],
      [
       39.6,
       85.9,
       449.8
      ],
      [
       17.4,
       31.6,
       448.6
      ],
      [
       46.5,
       92.7,
       448.4
      ],
      [
       32.3,
       71.8,
       445.5
      ],
      [
       16.5,
       35.8,
       443.8
      ],
      [
       25.1,
       46.5,
       442.8
      ],
      [
       19.9,
       40.2,
       439.9
      ],
      [
       23.0,
       55.3,
       438.4
      ],
      [
       11.0,
       21.4,
       437.5
      ],
      [
       30.8,
       61.8,
       431.9
      ],
      [
       35.6,
       58.3,
       431.8
      ],
      [
       14.3,
       32.3,
       431.4
      ],
      [
       32.5,
       68.6,
       428.4
      ],
      [
       19.6,
       37.4,
       428.4
      ],
      [
       42.1,
       81.3,
       426.2
      ],
      [
       17.7,
       35.8,
       423.2
      ],
      [
       19.5,
       41.3,
       422.6
      ],
      [
       11.7,
       18.2,
       421.9
      ],
      [
       25.2,
       47.6,
       421.1
      ],
      [
       10.7,
       19.0,
       419.2
      ],
      [
       22.6,
       53.4,
       411.0
      ],
      [
       42.8,
       73.5,
       410.3
      ],
      [
       28.5,
       53.8,
       410.0
      ],
      [
       25.3,
       32.7,
       409.6
      ],
      [
       26.6,
       53.5,
       409.5
      ],
      [
       30.2,
       51.2,
       404.3
      ],
      [
       27.6,
       46.1,
       403.5
      ],
      [
       23.6,
       54.5,
       402.7
      ],
      [
       30.5,
       61.2,
       399.0
      ],
      [
       11.5,
       24.9,
       398.4
      ],
      [
       35.5,
       64.3,
       396.9
      ],
      [
       12.9,
       28.4,
       396.9
      ],
      [
       29.2,
       59.6,
       395.5
      ],
      [
       16.1,
       32.4,
       391.8
      ],
      [
       26.8,
       51.1,
       389.9
      ],
      [
       24.9,
       46.5,
       389.6
      ],
      [
       48.3,
       103.8,
       386.9
      ],
      [
       18.2,
       28.0,
       386.6
      ],
      [
       13.7,
       28.2,
       384.3
      ],
      [
       17.8,
       27.5,
       383.2
      ],
      [
       25.6,
       81.4,
       383.2
      ],
      [
       31.0,
       62.3,
       382.4
      ],
      [
       23.2,
       56.5,
       382.0
      ],
      [
       19.7,
       54.1,
       379.4
      ],
      [
       18.9,
       38.4,
       377.6
      ],
      [
       14.8,
       31.4,
       377.4
      ],
      [
       15.4,
       24.3,
       376.5
      ],
      [
       15.4,
       36.7,
       369.2
      ],
      [
       17.8,
       30.6,
       368.7
      ],
      [
       20.0,
       37.1,
       367.3
      ],
      [
       24.7,
       43.4,
       366.6
      ],
      [
       34.1,
       79.1,
       365.7
      ],
      [
       13.1,
       19.3,
       365.5
      ],
      [
       33.9,
       74.5,
       363.3
      ],
      [
       14.1,
       28.2,
       362.7
      ],
      [
       10.5,
       20.9,
       356.4
      ],
      [
       13.5,
       21.4,
       355.0
      ],
      [
       19.0,
       39.1,
       353.0
      ],
      [
       23.3,
       52.3,
       352.5
      ],
      [
       15.6,
       17.1,
       352.1
      ],
      [
       28.6,
       50.6,
       350.1
      ],
      [
       17.6,
       37.0,
       348.3
      ],
      [
       20.9,
       44.8,
       347.8
      ],
      [
       42.3,
       71.4,
       346.3
      ],
      [
       31.7,
       71.2,
       346.1
      ],
      [
       29.7,
       63.5,
       345.7
      ],
      [
       17.6,
       32.0,
       340.6
      ],
      [
       18.5,
       41.8,
       340.0
      ],
      [
       26.0,
       50.6,
       339.6
      ],
      [
       44.6,
       83.0,
       338.3
      ],
      [
       18.7,
       45.7,
       336.5
      ],
      [
       25.7,
       54.3,
       336.5
      ],
      [
       40.2,
       79.4,
       335.5
      ],
      [
       29.5,
       52.0,
       335.0
      ],
      [
       31.2,
       60.6,
       333.8
      ],
      [
       43.3,
       87.7,
       333.6
      ],
      [
       39.0,
       74.5,
       333.5
      ],
      [
       18.9,
       31.4,
       332.2
      ],
      [
       37.6,
       82.7,
       331.5
      ],
      [
       29.4,
       47.6,
       331.5
      ],
      [
       28.9,
       64.4,
       330.5
      ],
      [
       27.0,
       52.4,
       329.9
      ],
      [
       28.6,
       43.5,
       329.1
      ],
      [
       34.3,
       65.5,
       328.2
      ],
      [
       28.7,
       54.2,
       328.0
      ],
      [
       25.4,
       54.2,
       326.5
      ],
      [
       42.6,
       67.1,
       323.5
      ],
      [
       12.5,
       24.0,
       322.3
      ],
      [
       10.2,
       19.2,
       322.1
      ],
      [
       31.9,
       64.3,
       321.4
      ],
      [
       17.1,
       34.1,
       318.2
      ],
      [
       27.6,
       47.8,
       317.7
      ],
      [
       34.1,
       80.6,
       311.9
      ],
      [
       48.1,
       94.0,
       310.7
      ],
      [
       13.5,
       26.4,
       309.9
      ],
      [
       32.7,
       60.2,
       307.1
      ],
      [
       35.0,
       69.8,
       306.3
      ],
      [
       12.8,
       25.1,
       305.1
      ],
      [
       19.6,
       35.8,
       304.4
      ],
      [
       26.1,
       53.0,
       304.2
      ],
      [
       22.6,
       52.3,
       303.6
      ],
      [
       33.0,
       62.6,
       303.4
      ],
      [
       40.1,
       77.0,
       302.8
      ],
      [
       31.1,
       68.8,
       302.3
      ],
      [
       39.2,
       72.2,
       300.8
      ],
      [
       13.5,
       19.0,
       299.5
      ],
      [
       19.7,
       48.9,
       299.2
      ],
      [
       24.7,
       56.4,
       298.9
      ],
      [
       24.2,
       47.2,
       298.6
      ],
      [
       28.9,
       54.3,
       297.1
      ],
      [
       23.4,
       54.1,
       296.5
      ],
      [
       23.8,
       57.7,
       296.0
      ],
      [
       41.6,
       86.8,
       295.0
      ],
      [
       36.6,
       70.0,
       294.0
      ],
      [
       14.4,
       33.8,
       292.7
      ],
      [
       42.5,
       85.7,
       291.8
      ],
      [
       24.7,
       46.0,
       290.8
      ],
      [
       11.0,
       21.3,
       290.5
      ],
      [
       26.7,
       60.2,
       289.4
      ],
      [
       29.1,
       52.7,
       288.9
      ],
      [
       34.9,
       74.6,
       288.6
      ],
      [
       15.3,
       35.0,
       284.7
      ],
      [
       18.5,
       38.6,
       283.1
      ],
      [
       9.9,
       18.9,
       282.6
      ],
      [
       17.8,
       42.7,
       282.2
      ],
      [
       20.9,
       42.2,
       281.8
      ],
      [
       18.3,
       38.3,
       281.7
      ],
      [
       23.6,
       57.4,
       280.3
      ],
      [
       27.4,
       56.7,
       278.1
      ],
      [
       12.4,
       24.5,
       274.9
      ],
      [
       37.5,
       83.0,
       274.4
      ],
      [
       32.3,
       68.0,
       273.4
      ],
      [
       18.3,
       34.6,
       273.2
      ],
      [
       29.0,
       46.0,
       272.4
      ],
      [
       46.6,
       76.5,
       271.8
      ],
      [
       42.3,
       79.0,
       271.3
      ],
      [
       34.9,
       61.4,
       271.0
      ],
      [
       16.0,
       31.8,
       270.6
      ],
      [
       13.1,
       24.6,
       270.2
      ],
      [
       29.9,
       44.1,
       270.1
      ],
      [
       46.1,
       98.2,
       269.7
      ],
      [
       31.8,
       62.1,
       269.7
      ],
      [
       42.2,
       83.6,
       268.9
      ],
      [
       15.6,
       17.1,
       268.5
      ],
      [
       29.2,
       55.2,
       267.8
      ],
      [
       23.9,
       37.0,
       264.3
      ],
      [
       25.9,
       60.4,
       263.3
      ],
      [
       23.6,
       51.4,
       262.3
      ],
      [
       21.1,
       42.2,
       261.5
      ],
      [
       27.4,
       49.4,
       261.2
      ],
      [
       17.4,
       34.8,
       260.2
      ],
      [
       11.5,
       17.5,
       259.7
      ],
      [
       13.2,
       29.1,
       258.2
      ],
      [
       46.9,
       79.4,
       257.3
      ],
      [
       22.2,
       46.5,
       256.8
      ],
      [
       36.2,
       75.8,
       255.1
      ],
      [
       44.8,
       78.2,
       254.4
      ],
      [
       49.9,
       103.2,
       253.6
      ],
      [
       49.4,
       89.0,
       253.1
      ],
      [
       9.2,
       15.8,
       252.2
      ],
      [
       30.1,
       49.4,
       251.6
      ],
      [
       14.6,
       29.9,
       251.5
      ],
      [
       23.7,
       56.6,
       250.1
      ],
      [
       24.4,
       37.3,
       248.3
      ],
      [
       31.0,
       48.8,
       247.4
      ],
      [
       18.6,
       34.8,
       244.8
      ],
      [
       14.4,
       28.9,
       243.9
      ],
      [
       23.7,
       44.1,
       243.6
      ],
      [
       30.3,
       55.0,
       243.6
      ],
      [
       15.0,
       29.2,
       243.6
      ],
      [
       21.9,
       41.8,
       243.0
      ],
      [
       37.0,
       77.9,
       242.3
      ],
      [
       25.3,
       43.4,
       242.2
      ],
      [
       30.5,
       61.5,
       241.4
      ],
      [
       14.9,
       30.4,
       241.0
      ],
      [
       47.3,
       91.5,
       240.6
      ],
      [
       17.3,
       39.4,
       240.0
      ],
      [
       33.3,
       65.0,
       238.3
      ],
      [
       36.4,
       72.1,
       236.1
      ],
      [
       17.2,
       24.2,
       235.8
      ],
      [
       27.6,
       46.3,
       234.9
      ],
      [
       31.0,
       52.5,
       234.7
      ],
      [
       25.7,
       46.3,
       234.6
      ],
      [
       21.1,
       46.7,
       233.6
      ],
      [
       30.9,
       67.6,
       233.3
      ],
      [
       19.8,
       43.3,
       231.7
      ],
      [
       26.0,
       61.4,
       231.5
      ],
      [
       53.4,
       99.5,
       230.9
      ],
      [
       23.5,
       48.0,
       228.8
      ],
      [
       11.4,
       25.4,
       228.3
      ],
      [
       19.9,
       41.6,
       228.1
      ],
      [
       25.2,
       62.8,
       227.0
      ],
      [
       32.4,
       79.2,
       226.3
      ],
      [
       16.8,
       36.1,
       225.6
      ],
      [
       31.4,
       59.0,
       225.4
      ],
      [
       21.2,
       52.0,
       225.1
      ],
      [
       35.0,
       64.8,
       224.1
      ],
      [
       12.3,
       24.1,
       223.2
      ],
      [
       40.6,
       94.3,
       222.3
      ],
      [
       15.4,
       32.1,
       222.1
      ],
      [
       37.2,
       70.7,
       221.0
      ],
      [
       12.6,
       25.9,
       220.4
      ],
      [
       14.8,
       24.2,
       219.8
      ],
      [
       14.4,
       22.4,
       218.7
      ],
      [
       25.8,
       52.8,
       218.3
      ],
      [
       33.1,
       75.5,
       217.8
      ],
      [
       40.1,
       68.5,
       217.1
      ],
      [
       16.3,
       30.8,
       216.9
      ],
      [
       41.4,
       104.0,
       216.3
      ],
      [
       39.8,
       61.0,
       215.9
      ],
      [
       31.3,
       71.9,
       215.8
      ],
      [
       48.9,
       96.9,
       215.6
      ],
      [
       29.4,
       53.9,
       215.3
      ],
      [
       28.0,
       67.0,
       214.1
      ],
      [
       24.2,
       51.6,
       214.0
      ],
      [
       12.8,
       26.0,
       213.2
      ],
      [
       34.4,
       72.4,
       212.7
      ],
      [
       43.2,
       78.5,
       212.0
      ],
      [
       34.0,
       93.1,
       211.8
      ],
      [
       38.7,
       63.9,
       211.3
      ],
      [
       24.0,
       50.2,
       211.2
      ],
      [
       29.2,
       61.1,
       210.7
      ],
      [
       29.3,
       57.8,
       209.8
      ],
      [
       23.6,
       43.2,
       209.0
      ],
      [
       21.5,
       51.2,
       208.2
      ],
      [
       51.1,
       102.7,
       208.1
      ],
      [
       34.2,
       61.3,
       207.6
      ],
      [
       50.0,
       86.5,
       207.5
      ],
      [
       15.6,
       30.0,
       206.7
      ],
      [
       43.4,
       82.2,
       206.4
      ],
      [
       25.5,
       44.2,
       206.2
      ],
      [
       20.9,
       50.9,
       206.2
      ],
      [
       22.3,
       44.3,
       206.1
      ],
      [
       38.8,
       66.5,
       206.0
      ],
      [
       26.5,
       55.3,
       205.9
      ],
      [
       42.7,
       96.3,
       205.6
      ],
      [
       30.1,
       56.6,
       205.0
      ],
      [
       26.0,
       41.6,
       204.7
      ],
      [
       33.9,
       75.6,
       204.3
      ],
      [
       33.3,
       56.6,
       204.3
      ],
      [
       41.5,
       78.0,
       204.0
      ],
      [
       39.9,
       77.3,
       203.9
      ],
      [
       24.0,
       57.1,
       203.8
      ],
      [
       35.0,
       91.5,
       203.7
      ],
      [
       25.5,
       43.6,
       203.5
      ],
      [
       20.5,
       42.6,
       203.4
      ],
      [
       39.1,
       74.0,
       203.4
      ],
      [
       23.6,
       46.8,
       203.2
      ],
      [
       47.6,
       84.4,
       202.3
      ],
      [
       31.7,
       67.5,
       201.9
      ],
      [
       33.9,
       58.4,
       201.7
      ],
      [
       26.3,
       54.3,
       201.5
      ],
      [
       14.7,
       26.2,
       201.5
      ],
      [
       14.7,
       27.0,
       201.2
      ],
      [
       21.7,
       42.8,
       200.7
      ],
      [
       34.5,
       61.8,
       200.5
      ],
      [
       39.1,
       82.2,
       200.3
      ],
      [
       34.4,
       85.6,
       199.7
      ],
      [
       15.0,
       27.0,
       199.4
      ],
      [
       14.3,
       30.9,
       199.3
      ],
      [
       31.7,
       55.4,
       198.8
      ],
      [
       33.3,
       56.4,
       197.7
      ],
      [
       38.3,
       77.4,
       197.7
      ],
      [
       25.7,
       48.8,
       196.4
      ],
      [
       31.4,
       69.6,
       195.7
      ],
      [
       35.9,
       67.0,
       195.6
      ],
      [
       14.9,
       33.0,
       195.3
      ],
      [
       16.9,
       42.0,
       194.7
      ],
      [
       12.1,
       26.4,
       194.6
      ],
      [
       39.2,
       76.1,
       194.1
      ],
      [
       16.9,
       34.1,
       193.8
      ],
      [
       43.2,
       100.1,
       193.0
      ],
      [
       25.1,
       45.7,
       192.7
      ],
      [
       51.8,
       98.6,
       192.4
      ],
      [
       15.8,
       32.5,
       192.2
      ],
      [
       40.7,
       81.0,
       191.6
      ],
      [
       20.0,
       41.7,
       191.5
      ],
      [
       32.5,
       58.7,
       190.6
      ],
      [
       41.1,
       88.2,
       190.5
      ],
      [
       29.4,
       61.8,
       190.5
      ],
      [
       37.2,
       78.3,
       190.5
      ],
      [
       36.5,
       84.6,
       190.2
      ],
      [
       14.8,
       33.7,
       190.2
      ],
      [
       34.1,
       57.8,
       189.6
      ],
      [
       19.1,
       42.1,
       189.4
      ],
      [
       54.6,
       108.3,
       188.8
      ],
      [
       24.1,
       52.8,
       188.6
      ],
      [
       22.4,
       44.8,
       188.5
      ],
      [
       46.8,
       84.5,
       187.6
      ],
      [
       54.8,
       86.5,
       187.3
      ],
      [
       32.4,
       63.9,
       186.9
      ],
      [
       29.6,
       57.4,
       186.9
      ],
      [
       35.2,
       64.1,
       186.9
      ],
      [
       16.0,
       37.8,
       186.8
      ],
      [
       39.0,
       74.2,
       186.4
      ],
      [
       55.7,
       97.4,
       186.4
      ],
      [
       36.3,
       84.8,
       186.2
      ],
      [
       40.9,
       81.6,
       185.9
      ],
      [
       20.7,
       40.7,
       185.7
      ],
      [
       25.1,
       45.0,
       185.5
      ],
      [
       16.7,
       39.8,
       185.4
      ],
      [
       18.1,
       31.4,
       185.1
      ],
      [
       28.6,
       54.9,
       184.5
      ],
      [
       52.0,
       92.0,
       184.1
      ],
      [
       40.5,
       85.6,
       183.3
      ],
      [
       49.0,
       87.8,
       183.3
      ],
      [
       14.4,
       29.6,
       183.2
      ],
      [
       42.7,
       83.0,
       183.0
      ],
      [
       27.0,
       68.7,
       182.4
      ],
      [
       32.2,
       66.2,
       182.4
      ],
      [
       47.3,
       90.8,
       181.8
      ],
      [
       39.5,
       77.4,
       181.2
      ],
      [
       28.8,
       64.3,
       181.2
      ],
      [
       30.7,
       69.0,
       181.1
      ],
      [
       27.1,
       57.4,
       180.8
      ],
      [
       25.2,
       65.9,
       179.9
      ],
      [
       26.7,
       48.9,
       179.7
      ],
      [
       21.8,
       35.5,
       179.6
      ],
      [
       43.8,
       92.6,
       179.5
      ],
      [
       26.8,
       59.6,
       179.5
      ],
      [
       20.4,
       46.4,
       179.5
      ],
      [
       41.7,
       91.4,
       179.2
      ],
      [
       22.1,
       54.4,
       178.4
      ],
      [
       35.2,
       64.8,
       177.9
      ],
      [
       37.5,
       61.2,
       177.9
      ],
      [
       21.4,
       47.4,
       177.4
      ],
      [
       34.1,
       51.0,
       177.3
      ],
      [
       36.2,
       112.9,
       177.0
      ],
      [
       12.8,
       29.5,
       176.7
      ],
      [
       52.6,
       94.5,
       176.2
      ],
      [
       43.3,
       88.2,
       176.0
      ],
      [
       13.2,
       21.1,
       175.3
      ],
      [
       21.1,
       44.9,
       175.0
      ],
      [
       26.6,
       57.0,
       174.5
      ],
      [
       13.0,
       26.6,
       173.9
      ],
      [
       13.5,
       31.4,
       173.6
      ],
      [
       32.4,
       69.0,
       173.5
      ],
      [
       29.8,
       60.7,
       173.4
      ],
      [
       26.1,
       56.0,
       173.2
      ],
      [
       16.9,
       26.6,
       173.1
      ],
      [
       28.3,
       63.1,
       173.1
      ],
      [
       28.7,
       54.3,
       173.0
      ],
      [
       33.3,
       67.0,
       173.0
      ],
      [
       16.9,
       40.7,
       173.0
      ],
      [
       49.3,
       99.5,
       173.0
      ],
      [
       21.3,
       42.6,
       172.3
      ],
      [
       37.2,
       93.0,
       172.0
      ],
      [
       34.0,
       62.5,
       171.6
      ],
      [
       45.7,
       113.8,
       171.3
      ],
      [
       48.7,
       89.9,
       171.3
      ],
      [
       41.0,
       77.7,
       171.2
      ],
      [
       18.3,
       24.7,
       171.0
      ],
      [
       54.5,
       99.0,
       170.7
      ],
      [
       20.0,
       46.9,
       170.0
      ],
      [
       23.5,
       50.3,
       169.8
      ],
      [
       17.6,
       40.7,
       169.6
      ],
      [
       31.3,
       77.5,
       169.4
      ],
      [
       16.3,
       33.8,
       169.2
      ],
      [
       36.1,
       93.1,
       168.9
      ],
      [
       16.4,
       35.8,
       168.6
      ],
      [
       28.6,
       68.6,
       168.1
      ],
      [
       29.1,
       86.0,
       168.1
      ],
      [
       10.4,
       18.2,
       167.9
      ],
      [
       15.2,
       33.7,
       167.5
      ],
      [
       39.8,
       62.8,
       167.2
      ],
      [
       40.5,
       87.9,
       166.7
      ],
      [
       34.6,
       73.5,
       166.7
      ],
      [
       21.2,
       35.6,
       166.1
      ],
      [
       45.9,
       92.3,
       165.5
      ],
      [
       56.4,
       112.0,
       165.4
      ],
      [
       34.0,
       98.0,
       165.4
      ],
      [
       15.8,
       33.8,
       164.6
      ],
      [
       13.7,
       33.0,
       163.9
      ],
      [
       20.8,
       46.1,
       163.8
      ],
      [
       12.2,
       23.3,
       163.6
      ],
      [
       31.9,
       72.8,
       163.5
      ],
      [
       25.6,
       50.7,
       163.3
      ],
      [
       32.6,
       69.8,
       163.0
      ],
      [
       40.8,
       78.5,
       162.2
      ],
      [
       32.0,
       68.0,
       161.5
      ],
      [
       33.3,
       64.2,
       161.5
      ],
      [
       31.7,
       71.0,
       161.5
      ],
      [
       25.0,
       54.7,
       161.4
      ],
      [
       46.1,
       87.0,
       160.9
      ],
      [
       24.2,
       55.1,
       160.0
      ],
      [
       26.1,
       39.7,
       159.7
      ],
      [
       27.5,
       53.4,
       159.5
      ],
      [
       28.2,
       51.4,
       159.4
      ],
      [
       31.3,
       72.3,
       159.3
      ],
      [
       33.5,
       53.0,
       158.2
      ],
      [
       47.5,
       82.8,
       158.2
      ],
      [
       31.2,
       57.2,
       157.9
      ],
      [
       17.8,
       33.0,
       157.8
      ],
      [
       31.3,
       70.6,
       157.5
      ],
      [
       21.2,
       45.2,
       157.3
      ],
      [
       15.2,
       30.2,
       157.3
      ],
      [
       42.2,
       95.0,
       156.5
      ],
      [
       28.5,
       41.1,
       155.8
      ],
      [
       34.7,
       74.4,
       155.6
      ],
      [
       31.3,
       50.9,
       155.4
      ],
      [
       31.5,
       54.8,
       155.2
      ],
      [
       40.2,
       92.7,
       155.1
      ],
      [
       30.6,
       83.6,
       154.9
      ],
      [
       20.9,
       37.8,
       154.5
      ],
      [
       49.0,
       90.2,
       154.5
      ],
      [
       31.9,
       64.6,
       154.1
      ],
      [
       19.1,
       44.6,
       153.6
      ],
      [
       28.3,
       51.8,
       152.4
      ],
      [
       12.5,
       26.6,
       152.3
      ],
      [
       28.7,
       53.8,
       152.3
      ],
      [
       44.4,
       90.8,
       151.5
      ],
      [
       31.1,
       59.0,
       151.3
      ],
      [
       25.1,
       67.8,
       151.2
      ],
      [
       22.0,
       60.4,
       150.6
      ],
      [
       20.7,
       46.1,
       150.2
      ],
      [
       18.0,
       40.1,
       149.8
      ],
      [
       23.5,
       48.5,
       148.6
      ],
      [
       27.9,
       66.8,
       148.5
      ],
      [
       14.4,
       31.5,
       148.2
      ],
      [
       34.3,
       63.6,
       147.4
      ],
      [
       18.1,
       34.0,
       147.2
      ],
      [
       22.4,
       48.2,
       146.3
      ],
      [
       20.0,
       28.6,
       146.1
      ],
      [
       14.7,
       30.9,
       145.2
      ],
      [
       24.0,
       49.4,
       145.0
      ],
      [
       46.5,
       88.6,
       144.6
      ],
      [
       25.7,
       50.1,
       143.8
      ],
      [
       27.9,
       52.5,
       143.2
      ],
      [
       54.2,
       100.8,
       142.8
      ],
      [
       17.5,
       34.2,
       142.2
      ],
      [
       29.5,
       57.7,
       142.1
      ],
      [
       24.7,
       51.0,
       142.1
      ],
      [
       17.6,
       37.6,
       141.5
      ],
      [
       21.7,
       45.2,
       141.1
      ],
      [
       22.4,
       44.0,
       140.8
      ],
      [
       36.9,
       71.0,
       140.6
      ],
      [
       20.9,
       35.3,
       140.1
      ],
      [
       40.2,
       87.5,
       139.1
      ],
      [
       27.8,
       63.6,
       139.1
      ],
      [
       22.8,
       51.9,
       136.6
      ],
      [
       21.6,
       50.3,
       136.6
      ],
      [
       43.3,
       99.4,
       135.8
      ],
      [
       39.9,
       69.8,
       135.1
      ],
      [
       42.8,
       111.8,
       132.9
      ],
      [
       29.8,
       86.0,
       132.9
      ],
      [
       37.4,
       60.8,
       131.1
      ],
      [
       28.3,
       59.3,
       130.6
      ],
      [
       25.2,
       56.8,
       130.3
      ],
      [
       20.2,
       46.1,
       129.1
      ],
      [
       35.0,
       92.4,
       128.8
      ],
      [
       25.0,
       62.7,
       128.8
      ],
      [
       16.9,
       27.2,
       125.9
      ],
      [
       33.9,
       67.2,
       125.8
      ],
      [
       47.1,
       81.4,
       125.8
      ],
      [
       34.9,
       112.6,
       124.6
      ],
      [
       30.8,
       67.6,
       122.4
      ],
      [
       54.8,
       104.8,
       122.4
      ],
      [
       34.5,
       61.3,
       122.0
      ],
      [
       36.2,
       61.1,
       121.7
      ],
      [
       25.8,
       54.6,
       120.0
      ],
      [
       24.5,
       57.8,
       119.6
      ],
      [
       45.0,
       94.6,
       118.8
      ],
      [
       32.2,
       52.6,
       118.8
      ],
      [
       46.9,
       98.0,
       118.6
      ],
      [
       15.1,
       36.6,
       117.9
      ],
      [
       52.6,
       99.4,
       117.8
      ],
      [
       26.0,
       54.6,
       115.5
      ],
      [
       38.5,
       72.6,
       115.5
      ],
      [
       26.3,
       61.6,
       115.5
      ],
      [
       20.0,
       38.8,
       115.5
      ],
      [
       18.1,
       39.2,
       115.5
      ],
      [
       37.6,
       58.2,
       114.2
      ],
      [
       25.5,
       66.4,
       113.9
      ],
      [
       20.3,
       39.5,
       113.4
      ],
      [
       32.3,
       69.0,
       113.4
      ],
      [
       32.5,
       64.6,
       113.4
      ],
      [
       29.5,
       56.5,
       113.4
      ],
      [
       27.9,
       64.4,
       113.4
      ],
      [
       18.9,
       43.1,
       113.4
      ],
      [
       20.5,
       40.0,
       112.0
      ],
      [
       33.0,
       75.6,
       112.0
      ],
      [
       48.2,
       98.4,
       112.0
      ],
      [
       46.5,
       96.2,
       112.0
      ],
      [
       26.2,
       39.3,
       112.0
      ],
      [
       42.8,
       98.4,
       112.0
      ],
      [
       19.8,
       41.0,
       112.0
      ],
      [
       51.0,
       101.9,
       112.0
      ],
      [
       17.4,
       33.4,
       112.0
      ],
      [
       17.4,
       33.8,
       112.0
      ],
      [
       24.4,
       62.0,
       111.0
      ],
      [
       21.3,
       39.8,
       111.0
      ],
      [
       31.5,
       55.8,
       110.8
      ],
      [
       42.0,
       78.2,
       110.3
      ],
      [
       32.8,
       63.8,
       110.3
      ],
      [
       40.4,
       63.4,
       110.1
      ],
      [
       20.0,
       46.2,
       109.2
      ],
      [
       44.2,
       93.8,
       109.2
      ],
      [
       14.0,
       30.2,
       109.2
      ],
      [
       13.9,
       31.4,
       109.2
      ]
     ],
     "linee": [
      {
       "k": 1.5,
       "label": "1.5 times"
      },
      {
       "k": 2.0,
       "label": "twice as long"
      }
     ],
     "nota": "Each point is a pair of zones, sized by morning cars. These are the 600 pairs with the most cars (83.2% of cars). Above a line, public transport takes more than that multiple of the car's time."
    },
    {
     "tipo": "barre",
     "titolo": "The 15 pairs with the most cars where public transport takes more than twice as long",
     "unita": "cars",
     "nota": "Morning cars on that pair (6 a.m. to 10 a.m., weekday), with the low factor 2.1. On the right, minutes by public transport versus by car.",
     "voci": [
      {
       "label": "Torino, Madonna Del Pilone → Torino, Vanchiglia",
       "valore": 894,
       "tono": "rosso",
       "testo": "894 cars: 35 versus 16 min"
      },
      {
       "label": "Torino, Parella → Torino, San Paolo",
       "valore": 763,
       "tono": "rosso",
       "testo": "763 cars: 30 versus 15 min"
      },
      {
       "label": "Torino, Madonna Del Pilone → Torino, Centro",
       "valore": 753,
       "tono": "rosso",
       "testo": "753 cars: 50 versus 23 min"
      },
      {
       "label": "Torino, Mirafiori Sud → Rivoli",
       "valore": 719,
       "tono": "rosso",
       "testo": "719 cars: 81 versus 31 min"
      },
      {
       "label": "Grugliasco → Torino, Pozzo Strada",
       "valore": 714,
       "tono": "rosso",
       "testo": "714 cars: 35 versus 17 min"
      },
      {
       "label": "Torino, Vanchiglia → Torino, Aurora",
       "valore": 615,
       "tono": "rosso",
       "testo": "615 cars: 27 versus 12 min"
      },
      {
       "label": "Torino, Barriera di Milano → Torino, Vanchiglia",
       "valore": 614,
       "tono": "rosso",
       "testo": "614 cars: 34 versus 15 min"
      },
      {
       "label": "Venaria Reale → Torino, Madonna di Campagna",
       "valore": 602,
       "tono": "rosso",
       "testo": "602 cars: 34 versus 17 min"
      },
      {
       "label": "Torino, Centro → Torino, Borgata Vittoria",
       "valore": 590,
       "tono": "rosso",
       "testo": "590 cars: 36 versus 17 min"
      },
      {
       "label": "Moncalieri → Torino, Mirafiori Sud",
       "valore": 568,
       "tono": "rosso",
       "testo": "568 cars: 55 versus 25 min"
      },
      {
       "label": "Settimo Torinese → Torino, Madonna Del Pilone",
       "valore": 544,
       "tono": "rosso",
       "testo": "544 cars: 86 versus 34 min"
      },
      {
       "label": "Torino, Borgata Vittoria → Torino, Centro",
       "valore": 541,
       "tono": "rosso",
       "testo": "541 cars: 39 versus 17 min"
      },
      {
       "label": "Torino, Madonna di Campagna → Torino, Borgata Vittoria",
       "valore": 540,
       "tono": "rosso",
       "testo": "540 cars: 22 versus 11 min"
      },
      {
       "label": "Beinasco → Torino, Centro",
       "valore": 520,
       "tono": "rosso",
       "testo": "520 cars: 69 versus 34 min"
      },
      {
       "label": "Torino, Mirafiori Nord → Moncalieri",
       "valore": 520,
       "tono": "rosso",
       "testo": "520 cars: 72 versus 33 min"
      }
     ]
    }
   ],
   "calcolo": [
    "Zones are those of the 2022 travel survey, with calculation points; each has up to 5 points.",
    "Public transport: on foot, bus, tram and metro, departing between 7:45 and 8:15. We take the median.",
    "Car: free-flow time times a peak factor, plus 5 minutes. There are two factors: 2.1 from Google Maps and 1.2 from the sensors.",
    "Ratio = public transport time divided by car time. The bands are fixed and chosen before seeing the numbers.",
    "The cars of a pair are the survey's car trips, departing between 6 and 10 a.m. on a weekday."
   ],
   "criteri": [
    [
     "Zones",
     "71 travel-survey zones (23 in Turin), up to 5 points each"
    ],
    [
     "Public transport",
     "departure 07:45-8:15 on a weekday, median, walking at 4.8 km/h, at most 120 minutes"
    ],
    [
     "Car, high limit",
     "free-flow time × 1.2 (5T sensors) + 5 minutes"
    ],
    [
     "Car, low limit",
     "free-flow time × 2.1 (Google Maps, 6 routes) + 5 minutes"
    ],
    [
     "Ratio bands",
     "under 1.5, 1.5-2, 2-3, over 3 (fixed before the numbers)"
    ]
   ],
   "limiti": [
    "Outside Turin, trains and other operators are missing: pairs between suburban towns are not in the number.",
    "Our road network ignores traffic lights and junctions. Car times are estimated between the slowdown measured by sensors and that of Google Maps.",
    "Without metropolitan trains, where they exist, public transport looks slower than it is. The timetable is the scheduled one.",
    "The survey is a sample. Trips within a zone and 653 pairs with no connection (5,616 cars) are not in the comparison."
   ],
   "extra": {
    "titolo": "Large roads and nearby stops",
    "punto": "95.3% of the km of large roads have a frequent stop nearby: the stop is there, but it is not enough.",
    "grafico": {
     "tipo": "pila",
     "titolo": "Km of large roads in Turin: with or without public transport nearby",
     "unita": "km",
     "voci": [
      {
       "label": "with frequent stops nearby",
       "valore": 327.3,
       "tono": "verde"
      },
      {
       "label": "with little public transport",
       "valore": 16.0,
       "tono": "rosso"
      }
     ]
    }
   }
  },
  "numero_pubblico": 4,
  "_nome": "risultato8_riepilogo_mappa.json"
 },
 {
  "risultato": "10",
  "titolo": "Case, servizi e fragilità",
  "tag": "STIMATO / CENSIMENTO",
  "stato": "Fatto",
  "in_breve": "Le case costano di più dove ci sono più servizi? E dove la fragilità sociale è alta e i servizi sono pochi?",
  "domanda": "Si paga per i servizi? E chi vive dove la fragilità è alta e i servizi sono pochi?",
  "numero_chiave": {
   "valore": 79598,
   "unita": "",
   "testo": "residenti in sezioni con fragilità alta e pochi servizi (9,5% dei residenti)"
  },
  "racconto": "",
  "risposta": [],
  "grafici": [],
  "metodo": [],
  "limiti": [],
  "parametri": [],
  "mappa": {
   "id": "vulnerabilita",
   "vista": "doppio",
   "nota": "Vista «Doppio svantaggio» nel tema Fragilità sociale."
  },
  "fonti": [
   "docs/rapporti/RAPPORTO_CASE_FRAGILITA_SERVIZI.txt",
   "data/processed/case_fragilita_servizi.json"
  ],
  "generato": "2026-10-23T13:30:39+00:00",
  "avviso": [
   "Dati [STIMATO] (servizi, indice) / [CENSIMENTO] (abitanti). Differenza fra zone, non effetto causale."
  ],
  "in_english": [],
  "scenari": [
   {
    "nome": "Oggi",
    "numeri": [
     {
      "label": "Residenti in sezioni con fragilità alta e pochi servizi",
      "prima": null,
      "dopo": 79598,
      "unita": "residenti"
     },
     {
      "label": "Quota dei residenti di Torino",
      "prima": null,
      "dopo": 9.5,
      "unita": "%"
     },
     {
      "label": "Zone in doppio svantaggio",
      "prima": null,
      "dopo": 5,
      "unita": "zone"
     },
     {
      "label": "Correlazione prezzo-servizi (Spearman)",
      "prima": null,
      "dopo": 0.614,
      "unita": ""
     }
    ],
    "nota": "Zone OMI di Torino; le sezioni si sommano nella zona, pesate per abitanti."
   }
  ],
  "forma": {
   "etichetta": "STIMATO / CENSIMENTO",
   "titolo": "Circa 1 torinese su 10 vive dove la fragilità è alta e i servizi sono pochi",
   "domanda": "Si paga per i servizi? E chi vive dove i servizi sono pochi e la fragilità è alta?",
   "numero": {
    "valore": 79598,
    "unita": "",
    "testo": "residenti in sezioni con fragilità alta e servizi bassi: il 9,5% dei torinesi"
   },
   "principale": {
    "tipo": "dispersione",
    "titolo": "Prezzo delle case e servizi a piedi, una zona OMI per punto (46 zone)",
    "xlabel": "punteggio «Tutti i servizi» a piedi, 0-100",
    "ylabel": "prezzo delle case, euro al m²",
    "passo_x": 20,
    "passo_y": 500,
    "xnome": "servizi",
    "ynome": "euro al m²",
    "punti": [
     [
      82.2,
      3650,
      1093,
      "Roma"
     ],
     [
      79.2,
      3425,
      10989,
      "Carlo Emanuele Ii"
     ],
     [
      77.4,
      2500,
      2584,
      "Solferino"
     ],
     [
      73.9,
      2600,
      4598,
      "Vinzaglio"
     ],
     [
      80.9,
      2600,
      11934,
      "Garibaldi"
     ],
     [
      87.3,
      2850,
      2369,
      "Castello"
     ],
     [
      79.0,
      2375,
      4397,
      "Rocca"
     ],
     [
      67.7,
      1950,
      7157,
      "San Salvario"
     ],
     [
      59.9,
      2700,
      5486,
      "Valentino"
     ],
     [
      23.5,
      2175,
      7729,
      "Michelotti"
     ],
     [
      35.0,
      2925,
      7445,
      "Crimea"
     ],
     [
      69.0,
      2675,
      894,
      "Duca D Aosta"
     ],
     [
      61.5,
      1500,
      13406,
      "Porta Palazzo - Maria Ausiliatrice"
     ],
     [
      73.7,
      2225,
      18276,
      "Vanchiglia - Borgo Rossini"
     ],
     [
      51.8,
      1625,
      20157,
      "Aurora"
     ],
     [
      62.3,
      2175,
      22925,
      "Dante"
     ],
     [
      29.8,
      2000,
      16461,
      "Vanchiglietta"
     ],
     [
      70.5,
      1700,
      10462,
      "Campidoglio - Martinetto"
     ],
     [
      73.3,
      2050,
      11167,
      "Adriano - Bernini - Rivoli"
     ],
     [
      72.5,
      2000,
      18643,
      "Cenisia"
     ],
     [
      64.1,
      2250,
      29291,
      "San Paolo"
     ],
     [
      66.5,
      2100,
      5190,
      "San Secondo"
     ],
     [
      59.6,
      2275,
      7970,
      "Galileo Ferraris"
     ],
     [
      63.8,
      2600,
      15343,
      "De Gasperi"
     ],
     [
      72.8,
      2600,
      1405,
      "Politecnico"
     ],
     [
      81.0,
      2350,
      14491,
      "Duchessa Jolanda"
     ],
     [
      64.6,
      2050,
      22334,
      "San Donato"
     ],
     [
      46.7,
      1550,
      71762,
      "Madonna Di Campagna"
     ],
     [
      44.5,
      1375,
      4322,
      "Spina 4 - Docks Dora"
     ],
     [
      9.5,
      1600,
      10584,
      "Barca - Bertolla"
     ],
     [
      37.8,
      1750,
      26802,
      "Nizza Millefonti"
     ],
     [
      52.8,
      1500,
      46558,
      "Filadelfia - Traiano"
     ],
     [
      62.4,
      1800,
      56890,
      "Santa Rita"
     ],
     [
      43.9,
      1425,
      40047,
      "Mirafiori Nord"
     ],
     [
      57.6,
      1050,
      48588,
      "Barriera Di Milano"
     ],
     [
      33.4,
      1045,
      28202,
      "Rebaudengo - Regio Parco"
     ],
     [
      15.4,
      1250,
      25756,
      "Corona Nord"
     ],
     [
      21.3,
      1300,
      31262,
      "Lucento - Vallette"
     ],
     [
      55.5,
      1925,
      31541,
      "Parella"
     ],
     [
      39.5,
      1675,
      32025,
      "Aeronautica - Lesna"
     ],
     [
      55.8,
      1925,
      36080,
      "Pozzo Strada"
     ],
     [
      25.6,
      1300,
      33481,
      "Mirafiori Sud"
     ],
     [
      40.2,
      2025,
      11318,
      "Spina 3 - Eurotorino"
     ],
     [
      5.7,
      2175,
      9568,
      "Collinare Villa Della Regina"
     ],
     [
      4.6,
      1875,
      3563,
      "Collinare Superga"
     ],
     [
      6.0,
      2000,
      5865,
      "Collinare Cavoretto"
     ]
    ],
    "retta": {
     "a": 1369.9,
     "b": 12.88,
     "label": "tendenza"
    },
    "nota": "Ogni punto è una zona, grande quanto i suoi abitanti. La linea è la tendenza: ogni 10 punti di servizi in più, 129 euro al m² in più."
   },
   "punti": [
    "Prezzo e servizi vanno insieme: correlazione di Spearman 0,61 su 46 zone (da 0,39 a 0,79).",
    "5 zone sono in doppio svantaggio: Mirafiori Sud, Lucento - Vallette, Rebaudengo - Regio Parco, Corona Nord, Barca - Bertolla. Ci abitano 129.285 persone.",
    "Vicino alla metro le case costano poco di più (+115 euro al m² in media, a pari distanza dal centro). Differenza fra zone, non effetto causale."
   ],
   "altri": [
    {
     "tipo": "barre",
     "titolo": "Residenti delle sezioni di Torino per condizione",
     "unita": "residenti",
     "nota": "Sezioni abitate di Torino, senza le zone quasi disabitate. Fragilità alta = indice sopra 57,7 su 100 (il 20% più alto); servizi bassi = punteggio fino a 34,4 su 100 (il 20% più basso).",
     "voci": [
      {
       "label": "fragilità alta e servizi bassi",
       "valore": 79598,
       "tono": "rosso",
       "testo": "79.598 (216 sezioni)"
      },
      {
       "label": "solo fragilità alta",
       "valore": 142406,
       "tono": "arancio",
       "testo": "142.406 (483 sezioni)"
      },
      {
       "label": "solo servizi bassi",
       "valore": 100600,
       "tono": "blu",
       "testo": "100.600 (489 sezioni)"
      },
      {
       "label": "nessuna delle due",
       "valore": 517053,
       "tono": "verde",
       "testo": "517.053 (2.332 sezioni)"
      }
     ]
    },
    {
     "tipo": "barre_diff",
     "titolo": "Quanto più costano le case vicino alla metro (con metro meno senza metro)",
     "unita": "€/m²",
     "nota": "Per fascia di distanza da Piazza Castello (2 km): prezzo medio delle zone con una fermata M1 entro 600 m meno quello delle zone senza, alla stessa distanza dal centro. Su ogni barra il numero di zone. Differenza fra zone, non effetto della metro.",
     "voci": [
      {
       "label": "0-2 km dal centro",
       "valore": 73,
       "testo": "(6 zone con metro, 8 senza)"
      },
      {
       "label": "2-4 km dal centro",
       "valore": 219,
       "testo": "(3 zone con metro, 16 senza)"
      },
      {
       "label": "4-6 km dal centro",
       "valore": 52,
       "testo": "(2 zone con metro, 10 senza)"
      },
      {
       "label": "6-8 km dal centro",
       "valore": null,
       "testo": "(0 zone con metro, 1 senza)"
      }
     ]
    }
   ],
   "calcolo": [
    "Unità: le 46 zone OMI di Torino con almeno 500 abitanti. Le sezioni si sommano nella zona, pesate per abitanti.",
    "Servizi: punteggio «Tutti i servizi» a piedi in 15 minuti. Fragilità: indice del censimento 2021 (lavoro, istruzione, case, anziani).",
    "Prezzo: centro della forbice OMI per le abitazioni civili. Tendenza: retta dei minimi quadrati.",
    "Doppio svantaggio = fragilità nel 20% più alto e servizi nel 20% più basso. Soglie fissate prima dei numeri: 49,8 e 33,4.",
    "Metro: zone con una fermata M1 entro 600 m dal centro, contro le altre alla stessa distanza da Piazza Castello."
   ],
   "criteri": [
    [
     "Zone",
     "46 zone OMI di Torino, almeno 500 abitanti"
    ],
    [
     "Fragilità alta",
     "indice sopra 57,7 su 100 (sezioni) / 49,8 (zone)"
    ],
    [
     "Servizi bassi",
     "punteggio fino a 34,4 su 100 (sezioni) / 33,4 (zone)"
    ],
    [
     "Metro vicina",
     "fermata M1 entro 600 m dal centro della zona"
    ],
    [
     "Fasce",
     "2 km da Piazza Castello"
    ]
   ],
   "limiti": [
    "I prezzi sono quotazioni OMI, non compravendite.",
    "C'è un solo semestre di quotazioni (2025/2).",
    "Le zone OMI sono grandi: dentro una zona i prezzi e i servizi cambiano molto.",
    "L'indice di fragilità non è il reddito: misura lavoro, istruzione, affollamento e anziani."
   ],
   "english": [
    "Question: do homes cost more where services are plentiful, and who lives where fragility is high and services are few?",
    "Answer: 1 Turin resident in 10 (79.598 people, 9.5%) lives where fragility is high and services are few. Price and services go together (Spearman 0.61 over 46 zones).",
    "Limit: price quotes, not sales; one semester; large zones. The metro price gap is between zones, not a causal effect."
   ],
   "mappa": {
    "id": "vulnerabilita",
    "nota": "Vista «Doppio svantaggio» nel tema Fragilità sociale.",
    "vista": "doppio"
   },
   "unita": {
    "tipo": "omini",
    "totale": 10,
    "colorati": 1,
    "didascalia": "Circa 1 torinese su 10 vive in sezioni con fragilità alta e servizi bassi (9,5% dei residenti)."
   }
  },
  "forma_en": {
   "etichetta": "ESTIMATED / CENSUS",
   "titolo": "About 1 Turin resident in 10 lives where fragility is high and services are few",
   "domanda": "Do people pay for services? And who lives where services are few and fragility is high?",
   "numero": {
    "valore": 79598,
    "unita": "",
    "testo": "residents in sections with high fragility and low services: 9.5% of Turin residents"
   },
   "principale": {
    "tipo": "dispersione",
    "titolo": "House prices and services on foot, one OMI zone per point (46 zones)",
    "xlabel": "“All services” score on foot, 0-100",
    "ylabel": "house price, euro per m²",
    "passo_x": 20,
    "passo_y": 500,
    "xnome": "servizi",
    "ynome": "euro al m²",
    "punti": [
     [
      82.2,
      3650,
      1093,
      "Roma"
     ],
     [
      79.2,
      3425,
      10989,
      "Carlo Emanuele Ii"
     ],
     [
      77.4,
      2500,
      2584,
      "Solferino"
     ],
     [
      73.9,
      2600,
      4598,
      "Vinzaglio"
     ],
     [
      80.9,
      2600,
      11934,
      "Garibaldi"
     ],
     [
      87.3,
      2850,
      2369,
      "Castello"
     ],
     [
      79.0,
      2375,
      4397,
      "Rocca"
     ],
     [
      67.7,
      1950,
      7157,
      "San Salvario"
     ],
     [
      59.9,
      2700,
      5486,
      "Valentino"
     ],
     [
      23.5,
      2175,
      7729,
      "Michelotti"
     ],
     [
      35.0,
      2925,
      7445,
      "Crimea"
     ],
     [
      69.0,
      2675,
      894,
      "Duca D Aosta"
     ],
     [
      61.5,
      1500,
      13406,
      "Porta Palazzo - Maria Ausiliatrice"
     ],
     [
      73.7,
      2225,
      18276,
      "Vanchiglia - Borgo Rossini"
     ],
     [
      51.8,
      1625,
      20157,
      "Aurora"
     ],
     [
      62.3,
      2175,
      22925,
      "Dante"
     ],
     [
      29.8,
      2000,
      16461,
      "Vanchiglietta"
     ],
     [
      70.5,
      1700,
      10462,
      "Campidoglio - Martinetto"
     ],
     [
      73.3,
      2050,
      11167,
      "Adriano - Bernini - Rivoli"
     ],
     [
      72.5,
      2000,
      18643,
      "Cenisia"
     ],
     [
      64.1,
      2250,
      29291,
      "San Paolo"
     ],
     [
      66.5,
      2100,
      5190,
      "San Secondo"
     ],
     [
      59.6,
      2275,
      7970,
      "Galileo Ferraris"
     ],
     [
      63.8,
      2600,
      15343,
      "De Gasperi"
     ],
     [
      72.8,
      2600,
      1405,
      "Politecnico"
     ],
     [
      81.0,
      2350,
      14491,
      "Duchessa Jolanda"
     ],
     [
      64.6,
      2050,
      22334,
      "San Donato"
     ],
     [
      46.7,
      1550,
      71762,
      "Madonna Di Campagna"
     ],
     [
      44.5,
      1375,
      4322,
      "Spina 4 - Docks Dora"
     ],
     [
      9.5,
      1600,
      10584,
      "Barca - Bertolla"
     ],
     [
      37.8,
      1750,
      26802,
      "Nizza Millefonti"
     ],
     [
      52.8,
      1500,
      46558,
      "Filadelfia - Traiano"
     ],
     [
      62.4,
      1800,
      56890,
      "Santa Rita"
     ],
     [
      43.9,
      1425,
      40047,
      "Mirafiori Nord"
     ],
     [
      57.6,
      1050,
      48588,
      "Barriera Di Milano"
     ],
     [
      33.4,
      1045,
      28202,
      "Rebaudengo - Regio Parco"
     ],
     [
      15.4,
      1250,
      25756,
      "Corona Nord"
     ],
     [
      21.3,
      1300,
      31262,
      "Lucento - Vallette"
     ],
     [
      55.5,
      1925,
      31541,
      "Parella"
     ],
     [
      39.5,
      1675,
      32025,
      "Aeronautica - Lesna"
     ],
     [
      55.8,
      1925,
      36080,
      "Pozzo Strada"
     ],
     [
      25.6,
      1300,
      33481,
      "Mirafiori Sud"
     ],
     [
      40.2,
      2025,
      11318,
      "Spina 3 - Eurotorino"
     ],
     [
      5.7,
      2175,
      9568,
      "Collinare Villa Della Regina"
     ],
     [
      4.6,
      1875,
      3563,
      "Collinare Superga"
     ],
     [
      6.0,
      2000,
      5865,
      "Collinare Cavoretto"
     ]
    ],
    "retta": {
     "a": 1369.9,
     "b": 12.88,
     "label": "trend"
    },
    "nota": "Each point is a zone, sized by its inhabitants. The line is the trend: for every 10 extra service points, 129 euro per m² more."
   },
   "punti": [
    "Price and services go together: Spearman correlation 0.61 over 46 zones (from 0.39 to 0.79).",
    "5 zones are in double disadvantage: Mirafiori Sud, Lucento - Vallette, Rebaudengo - Regio Parco, Corona Nord, Barca - Bertolla. 129,285 people live there.",
    "Near the metro homes cost a little more (+115 euro per m² on average, at the same distance from the centre). A difference between zones, not a causal effect."
   ],
   "altri": [
    {
     "tipo": "barre",
     "titolo": "Residents of Turin's census sections by condition",
     "unita": "residents",
     "nota": "Inhabited sections of Turin, without the almost uninhabited areas. High fragility = index above 57.7 out of 100 (the highest 20%); low services = score up to 34.4 out of 100 (the lowest 20%).",
     "voci": [
      {
       "label": "high fragility and low services",
       "valore": 79598,
       "tono": "rosso",
       "testo": "79,598 (216 sections)"
      },
      {
       "label": "high fragility only",
       "valore": 142406,
       "tono": "arancio",
       "testo": "142,406 (483 sections)"
      },
      {
       "label": "low services only",
       "valore": 100600,
       "tono": "blu",
       "testo": "100,600 (489 sections)"
      },
      {
       "label": "neither",
       "valore": 517053,
       "tono": "verde",
       "testo": "517,053 (2,332 sections)"
      }
     ]
    },
    {
     "tipo": "barre_diff",
     "titolo": "How much more homes cost near the metro (with metro minus without)",
     "unita": "€/m²",
     "nota": "By distance band from Piazza Castello (2 km): average price of zones with an M1 stop within 600 m minus that of zones without, at the same distance from the centre. The number of zones is shown on each bar. A difference between zones, not an effect of the metro.",
     "voci": [
      {
       "label": "0-2 km from the centre",
       "valore": 73,
       "testo": "(6 zones with metro, 8 without)"
      },
      {
       "label": "2-4 km from the centre",
       "valore": 219,
       "testo": "(3 zones with metro, 16 without)"
      },
      {
       "label": "4-6 km from the centre",
       "valore": 52,
       "testo": "(2 zones with metro, 10 without)"
      },
      {
       "label": "6-8 km from the centre",
       "valore": null,
       "testo": "(0 zones with metro, 1 without)"
      }
     ]
    }
   ],
   "calcolo": [
    "Unit: the 46 OMI zones of Turin with at least 500 inhabitants. Sections are added up within the zone, weighted by inhabitants.",
    "Services: “All services” score within a 15-minute walk. Fragility: 2021 census index (work, education, housing, older people).",
    "Price: middle of the OMI range for residential homes. Trend: least-squares line.",
    "Double disadvantage = fragility in the highest 20% and services in the lowest 20%. Thresholds fixed before the numbers: 49.8 and 33.4.",
    "Metro: zones with an M1 stop within 600 m of the centre, compared with the others at the same distance from Piazza Castello."
   ],
   "criteri": [
    [
     "Zones",
     "46 OMI zones of Turin, at least 500 inhabitants"
    ],
    [
     "High fragility",
     "index above 57.7 out of 100 (sections) / 49.8 (zones)"
    ],
    [
     "Low services",
     "score up to 34.4 out of 100 (sections) / 33.4 (zones)"
    ],
    [
     "Metro nearby",
     "M1 stop within 600 m of the zone centre"
    ],
    [
     "Bands",
     "2 km from Piazza Castello"
    ]
   ],
   "limiti": [
    "Prices are OMI quotations, not actual sales.",
    "There is only one semester of quotations (2025/2).",
    "OMI zones are large: prices and services vary a lot within a zone.",
    "The fragility index is not income: it measures work, education, crowding and older people."
   ],
   "mappa": {
    "id": "vulnerabilita",
    "nota": "Vista «Doppio svantaggio» nel tema Fragilità sociale.",
    "vista": "doppio"
   },
   "unita": {
    "tipo": "omini",
    "totale": 10,
    "colorati": 1,
    "didascalia": "About 1 in 10 Turin residents live in sections with high fragility and low services (9.5% of residents)."
   }
  },
  "numero_pubblico": 5,
  "_nome": "risultato10_riepilogo_mappa.json"
 }
];
