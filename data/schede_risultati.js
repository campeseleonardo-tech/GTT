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
  "generato": "2026-10-24T00:36:03+00:00",
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
   "tipo_dato": "Tipo di dato: calcolato da dati veri, non misurato direttamente.",
   "titolo": "Torino, città dei 15 minuti: quasi tutti hanno i servizi a 15 minuti a piedi",
   "domanda": "Quanti torinesi hanno i servizi a 5, 10 e 15 minuti a piedi, e quanti vivono su una strada trafficata?",
   "numero": {
    "valore": 99.2,
    "unita": "%",
    "testo": "dei residenti delle zone abitate ha tutti e 5 i servizi a 15 minuti a piedi",
    "breve": "dei residenti ha i servizi a 15 minuti"
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
    "A 5 minuti solo ~68% dei residenti ha tutti e 5 i servizi; a 10 minuti ~97%.",
    "~222 mila residenti (~26%) vivono a meno di 100 m da una strada molto trafficata.",
    "I 362 residenti senza 3 o più servizi sono in 5 sezioni di collina: dove manca davvero tutto."
   ],
   "altri": [
    {
     "tipo": "barre",
     "titolo": "Residenti per distanza da una strada molto trafficata",
     "unita": "residenti",
     "nota": "Distanza dal centro della sezione. Strada molto trafficata: almeno 10.677 veicoli al giorno.",
     "voci": [
      {
       "label": "esposti (meno di 100 m)",
       "valore": 222179,
       "tono": "rosso"
      },
      {
       "label": "vicini (100-250 m)",
       "valore": 265471,
       "tono": "giallo"
      },
      {
       "label": "lontani (oltre 250 m)",
       "valore": 354330,
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
    "Si è esposti se il centro della sezione è a meno di 100 m da una strada molto trafficata.",
    "Il traffico viene da un modello tarato sui sensori, che sbaglia del ±28% in metà dei casi."
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
     "almeno 10.677 veicoli al giorno"
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
    "Il traffico è un modello e sostituisce rumore e smog, che non sono misurati."
   ],
   "mappa": {
    "id": "faseb",
    "nota": "Nella mappa, tema \"Dove mancano i servizi\": all'apertura quanti servizi mancano in ogni zona (0-5, zone poco abitate in grigio); nel menu un servizio alla volta, con i punti dove aggiungerne uno."
   },
   "anima": {
    "tipo": "cerchi",
    "voci": [
     {
      "min": 5,
      "pct": 68.3,
      "testo": "tutti e 5 i servizi a 5 minuti a piedi"
     },
     {
      "min": 10,
      "pct": 96.8,
      "testo": "tutti e 5 i servizi a 10 minuti a piedi"
     },
     {
      "min": 15,
      "pct": 99.2,
      "testo": "tutti e 5 i servizi a 15 minuti a piedi"
     }
    ],
    "didascalia": "Residenti delle zone abitate che hanno scuole, salute, negozi, fermate e verde a 5, 10 e 15 minuti da casa a piedi."
   }
  },
  "forma_en": {
   "tipo_dato": "Type of data: calculated from real data, not measured directly.",
   "titolo": "Turin, a 15-minute city: almost everyone has the services within a 15-minute walk",
   "domanda": "How many people in Turin have the services within 5, 10 and 15 minutes on foot, and how many live on a busy road?",
   "numero": {
    "valore": 99.2,
    "unita": "%",
    "testo": "of residents of inhabited areas have all 5 services within a 15-minute walk",
    "breve": "of residents have the services within 15 minutes"
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
    "Within 5 minutes only ~68% of residents have all 5 services; within 10 minutes ~97%.",
    "~222 thousand residents (~26%) live less than 100 m from a very busy road.",
    "The 362 residents without 3 or more services live in 5 hillside sections: where really everything is missing."
   ],
   "altri": [
    {
     "tipo": "barre",
     "titolo": "Residents by distance from a very busy road",
     "unita": "residents",
     "nota": "Distance from the centre of the section. Very busy road: at least 10,677 vehicles a day.",
     "voci": [
      {
       "label": "exposed (less than 100 m)",
       "valore": 222179,
       "tono": "rosso"
      },
      {
       "label": "close (100-250 m)",
       "valore": 265471,
       "tono": "giallo"
      },
      {
       "label": "far (over 250 m)",
       "valore": 354330,
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
    "A section is exposed if its centre is less than 100 m from a very busy road.",
    "Traffic comes from a model calibrated on the sensors, which is off by ±28% in half of the cases."
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
     "at least 10,677 vehicles a day"
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
    "Traffic comes from a model and stands in for noise and smog, which are not measured."
   ],
   "mappa": {
    "id": "faseb",
    "nota": "Nella mappa, tema \"Dove mancano i servizi\": all'apertura quanti servizi mancano in ogni zona (0-5, zone poco abitate in grigio); nel menu un servizio alla volta, con i punti dove aggiungerne uno."
   },
   "anima": {
    "tipo": "cerchi",
    "voci": [
     {
      "min": 5,
      "pct": 68.3,
      "testo": "all 5 services within 5 minutes on foot"
     },
     {
      "min": 10,
      "pct": 96.8,
      "testo": "all 5 services within 10 minutes on foot"
     },
     {
      "min": 15,
      "pct": 99.2,
      "testo": "all 5 services within 15 minutes on foot"
     }
    ],
    "didascalia": "Residents of inhabited areas with schools, health care, shops, stops and green space within 5, 10 and 15 minutes' walk from home."
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
   "valore": 16.0,
   "unita": "%",
   "testo": "dei passaggi nei giorni feriali arriva con più di 5 minuti di ritardo"
  },
  "racconto": "Una delle direzioni del progetto: confrontare l'orario promesso con quello reale, usando le posizioni e i ritardi dei mezzi che il Raspberry Pi del progetto raccoglie ogni minuto.",
  "risposta": [
   "Nei giorni feriali il 16% dei passaggi arriva con più di 5 minuti di ritardo; il sabato il 16,9%.",
   "Sulle linee frequenti il 21,6% delle coppie di mezzi consecutivi arriva a grappolo o lascia un buco.",
   "Il problema più comune è l'anticipo: il 35,4% dei passaggi feriali arriva più di un minuto prima dell'orario.",
   "Il feed in tempo reale di GTT, usato in precedenza, dava il 6,2% in ritardo invece del 16%: smette di aggiornare la fermata all'orario previsto e così sottostima i ritardi.",
   "Oltre 10 minuti: 6,41% nei feriali. GTT dichiara il 2,3% per il 2025: il suo metodo non è pubblicato; qui si misura a ogni fermata con il GPS, su pochi giorni.",
   "Non è la stessa misura: GTT fa la media dell'anno intero, estate e sere comprese, su tutte le linee, con un metodo che non pubblica; il GPS misura pochi giorni di ottobre, solo le linee urbane, dalle 5 a mezzanotte.",
   "Il ritardo cresce lungo la corsa: alla prima fermata è 5,28%, a metà corsa 5,86%, a ogni fermata 6,18%, escluse le fasce 7-9 e 16-19 5,79% (media della settimana).",
   "Tutte e due le misure dicono che i ritardi gravi sono una piccola parte dei passaggi: tra 2,3% e 6,2%.",
   "Tram e bus: in ritardo oltre 5 minuti il 15,4% dei passaggi dei tram e il 16,2% dei bus (feriale).",
   "Linee utili (quelle che toccano più zone affollate): in ritardo oltre 5 minuti il 17,5% dei passaggi, contro il 13,2% delle altre linee (feriale).",
   "Attesa: Nei giorni feriali, sulle linee frequenti, l'orario promette un'attesa media di 4,8 minuti; quella reale è tra 6,4 e 6,5 minuti.",
   "Sono da 1,6 a 1,7 minuti in più a ogni attesa: almeno il 33% oltre la promessa.",
   "La linea con più attesa in più è la 61 (3,2 minuti in più, stima bassa).",
   "Attesa alla fermata sulle linee frequenti (feriale): tram, promessa 4,5 min, in più 1,7-1,7 min; bus, promessa 5,7 min, in più 1,1-2 min."
  ],
  "grafici": [
   {
    "tipo": "pila",
    "titolo": "Come arrivano i mezzi nei giorni feriali",
    "unita": "%",
    "voci": [
     {
      "label": "in anticipo (oltre 1 min)",
      "valore": 35.4
     },
     {
      "label": "puntuali (da -1 a +5 min)",
      "valore": 48.6,
      "tono": "verde"
     },
     {
      "label": "in ritardo (oltre 5 min)",
      "valore": 16.0,
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
      "label": "mattino (7-9)",
      "valore": 15.5,
      "tono": "rosso"
     },
     {
      "label": "giorno (9-16)",
      "valore": 16.3,
      "tono": "rosso"
     },
     {
      "label": "sera (16-19)",
      "valore": 20.4,
      "tono": "rosso"
     },
     {
      "label": "tarda sera (19-24)",
      "valore": 18.2,
      "tono": "rosso"
     },
     {
      "label": "notte e primo mattino (fino alle 7, dati parziali)",
      "valore": 5.9,
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
      "valore": 16.0,
      "tono": "rosso"
     },
     {
      "label": "sabato",
      "valore": 16.9,
      "tono": "rosso"
     },
     {
      "label": "domenica",
      "valore": 12.1,
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
      "valore": 41.4,
      "link": "mappa_torino.html#tema=puntualita&linea=17&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 6",
      "valore": 39.6,
      "link": "mappa_torino.html#tema=puntualita&linea=6&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 19",
      "valore": 36.7,
      "link": "mappa_torino.html#tema=puntualita&linea=19&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 68",
      "valore": 30.6,
      "link": "mappa_torino.html#tema=puntualita&linea=68&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 66",
      "valore": 28.8,
      "link": "mappa_torino.html#tema=puntualita&linea=66&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 33",
      "valore": 26.2,
      "link": "mappa_torino.html#tema=puntualita&linea=33&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 4",
      "valore": 24.4,
      "link": "mappa_torino.html#tema=puntualita&linea=4&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 72",
      "valore": 23.7,
      "link": "mappa_torino.html#tema=puntualita&linea=72&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 52",
      "valore": 23.1,
      "link": "mappa_torino.html#tema=puntualita&linea=52&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 61",
      "valore": 23.1,
      "link": "mappa_torino.html#tema=puntualita&linea=61&ora=8",
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
      "valore": 47.1,
      "link": "mappa_torino.html#tema=puntualita&linea=14&ora=8"
     },
     {
      "label": "linea 4",
      "valore": 40.7,
      "link": "mappa_torino.html#tema=puntualita&linea=4&ora=8"
     },
     {
      "label": "linea 45",
      "valore": 38.6,
      "link": "mappa_torino.html#tema=puntualita&linea=45&ora=8"
     },
     {
      "label": "linea 43",
      "valore": 33.6,
      "link": "mappa_torino.html#tema=puntualita&linea=43&ora=8"
     },
     {
      "label": "linea 17",
      "valore": 31.4,
      "link": "mappa_torino.html#tema=puntualita&linea=17&ora=8"
     },
     {
      "label": "linea 30",
      "valore": 31.2,
      "link": "mappa_torino.html#tema=puntualita&linea=30&ora=8"
     },
     {
      "label": "linea 12",
      "valore": 27.8,
      "link": "mappa_torino.html#tema=puntualita&linea=12&ora=8"
     },
     {
      "label": "linea 68",
      "valore": 25.8,
      "link": "mappa_torino.html#tema=puntualita&linea=68&ora=8"
     },
     {
      "label": "linea 29",
      "valore": 25.5,
      "link": "mappa_torino.html#tema=puntualita&linea=29&ora=8"
     },
     {
      "label": "linea 63",
      "valore": 25.0,
      "link": "mappa_torino.html#tema=puntualita&linea=63&ora=8"
     }
    ]
   },
   {
    "tipo": "barre",
    "titolo": "GPS e dato ufficiale GTT: passaggi con oltre 10 minuti di ritardo",
    "unita": "%",
    "nota": "Il GPS è la media della settimana, in quattro modi di contare. GTT è l'anno 2025, tutte le linee, con un metodo non pubblicato.",
    "voci": [
     {
      "label": "GTT (2025, anno intero)",
      "valore": 2
     },
     {
      "label": "GPS, a ogni fermata",
      "valore": 6,
      "tono": "rosso"
     },
     {
      "label": "GPS, solo alla prima fermata",
      "valore": 5,
      "tono": "rosso"
     },
     {
      "label": "GPS, solo a metà corsa",
      "valore": 6,
      "tono": "rosso"
     },
     {
      "label": "GPS, escluse le fasce 7-9 e 16-19",
      "valore": 6,
      "tono": "rosso"
     }
    ]
   },
   {
    "tipo": "barre",
    "titolo": "Tram contro bus (feriale)",
    "unita": "%",
    "nota": "Tram: 263.231 passaggi; bus: 987.202.",
    "voci": [
     {
      "label": "tram: in ritardo oltre 5 min",
      "valore": 15.4,
      "tono": "rosso"
     },
     {
      "label": "bus: in ritardo oltre 5 min",
      "valore": 16.2,
      "tono": "rosso"
     },
     {
      "label": "tram: in ritardo oltre 10 min",
      "valore": 6.2,
      "tono": "rosso"
     },
     {
      "label": "bus: in ritardo oltre 10 min",
      "valore": 6.47,
      "tono": "rosso"
     },
     {
      "label": "tram: a grappolo o con un buco",
      "valore": 26.8
     },
     {
      "label": "bus: a grappolo o con un buco",
      "valore": 18.3
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
      "label": "linea 19 (6,8 min ogni 10 km)",
      "valore": 4.1,
      "link": "mappa_torino.html#tema=puntualita&linea=19&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 17 (2,2 min ogni 10 km)",
      "valore": 3.7,
      "link": "mappa_torino.html#tema=puntualita&linea=17&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 4 (2,4 min ogni 10 km)",
      "valore": 3.4,
      "link": "mappa_torino.html#tema=puntualita&linea=4&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 6 (7,3 min ogni 10 km)",
      "valore": 3.2,
      "link": "mappa_torino.html#tema=puntualita&linea=6&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 68 (2,2 min ogni 10 km)",
      "valore": 2.4,
      "link": "mappa_torino.html#tema=puntualita&linea=68&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 33 (1,9 min ogni 10 km)",
      "valore": 2.1,
      "link": "mappa_torino.html#tema=puntualita&linea=33&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 72 (1,8 min ogni 10 km)",
      "valore": 2.0,
      "link": "mappa_torino.html#tema=puntualita&linea=72&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 60 (2,9 min ogni 10 km)",
      "valore": 1.8,
      "link": "mappa_torino.html#tema=puntualita&linea=60&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 132 (2,2 min ogni 10 km)",
      "valore": 1.8,
      "link": "mappa_torino.html#tema=puntualita&linea=132&ora=8",
      "tono": "rosso"
     },
     {
      "label": "linea 42 (2,2 min ogni 10 km)",
      "valore": 1.7,
      "link": "mappa_torino.html#tema=puntualita&linea=42&ora=8",
      "tono": "rosso"
     }
    ]
   },
   {
    "tipo": "barre",
    "titolo": "Linee utili contro altre (feriale)",
    "unita": "%",
    "nota": "Linee utili = le 54 che toccano più delle zone dove arriva più gente per km² (Risultato 3). Passaggi: 821.441 sulle utili, 428.992 sulle altre.",
    "voci": [
     {
      "label": "linee utili: in ritardo oltre 5 min",
      "valore": 17.5,
      "tono": "rosso"
     },
     {
      "label": "altre linee: in ritardo oltre 5 min",
      "valore": 13.2,
      "tono": "rosso"
     },
     {
      "label": "linee utili: a grappolo o con un buco",
      "valore": 22.9
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
      "label": "mattino (7-9)",
      "valore": 5.84,
      "prima": 4.53
     },
     {
      "label": "giorno (9-16)",
      "valore": 5.32,
      "prima": 3.88
     },
     {
      "label": "sera (16-19)",
      "valore": 6.54,
      "prima": 4.41
     },
     {
      "label": "tarda sera (19-24)",
      "valore": 9.96,
      "prima": 8.21
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
      "label": "mattino (7-9)",
      "valore": 1.65,
      "prima": 1.31
     },
     {
      "label": "giorno (9-16)",
      "valore": 1.7,
      "prima": 1.44
     },
     {
      "label": "sera (16-19)",
      "valore": 1.98,
      "prima": 2.12
     },
     {
      "label": "tarda sera (19-24)",
      "valore": 1.7,
      "prima": 1.74
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
      "label": "linea 56",
      "valore": 1.6
     },
     {
      "label": "linea 16 CD",
      "valore": 1.6
     },
     {
      "label": "linea 15",
      "valore": 1.4
     },
     {
      "label": "linea 2",
      "valore": 1.4
     },
     {
      "label": "linea 3",
      "valore": 1.2
     },
     {
      "label": "linea 55",
      "valore": 1.2
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
    "2026-10-10 - 2026-10-22"
   ],
   [
    "Passaggi con GPS valido",
    "1.606.548 (79,8% di quelli programmati dalle corse viste)"
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
   "Pochi giorni (7 feriali, 2 sabati, 1 domeniche), e non tutti interi: sabato 10 dalle 15, lunedì 12 dalle 12, martedì 13 con buchi il pomeriggio e la sera, domenica 18 fino alle 9:30 (poi guasto del feed GTT). Ogni giorno conta con le ore che hanno dati.",
   "La raccolta si ferma a mezzanotte e riparte verso le 5: la notte non è misurata.",
   "Il GPS copre solo le linee urbane (circa 90): le extraurbane non ci sono mai. Anche sulle linee coperte alcune corse non sono mai viste dal GPS: se erano saltate davvero, la puntualità reale è peggiore e i buchi sono più di quelli contati.",
   "Il GPS c'è per circa il 80% dei passaggi delle corse viste; le corse mai viste dal GPS non si contano.",
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
   "On weekdays 16.0% of departures arrive more than 5 minutes late; on Saturdays 16.9%. On frequent lines 21.6% of consecutive pairs of vehicles bunch together or leave a gap.",
   "The most common problem is early arrival: 35.4% of weekday departures arrive more than one minute before the timetable.",
   "Limits: only 7 weekdays, 2 Saturdays and 1 Sundays of data, some of them partial; the night is not measured.",
   "Arrivals are now measured with the vehicles' GPS; the GTT real-time feed we used before gave 6.2% late instead of 16.0% because it stops updating a stop at its scheduled time, so it underestimates delays.",
   "More than 10 minutes late: 6.41% of weekday departures. GTT reports 2.3% for 2025: its method is not published; we measure at every stop with GPS, over a few days.",
   "Why our number differs from GTT's 2.3% (more than 10 minutes late, 2025): GTT averages the whole year on all lines with an unpublished method; we measure a few October days on urban lines. At the first stop of the trip we get 5.28%, at every stop 6.18% (weekly average).",
   "Trams vs buses (weekdays): 15.4% of tram departures and 16.2% of bus departures are more than 5 minutes late.",
   "Delay at the end of the trip (median, last stops): highest on line 19 (4.1 minutes).",
   "Useful lines (touching the busiest zones per km2): 17.5% of departures more than 5 minutes late, other lines 13.2% (weekdays).",
   "On weekdays the timetable promises an average wait of 4.8 minutes; the real one is between 6.4 and 6.5 minutes. That is 1.6 to 1.7 minutes more per wait, at least 33% above the promise.",
   "Limits: only 7 weekdays of data so far; real arrivals are measured with the vehicles' GPS (within 60 metres of the stop); the night is not included.",
   "Waiting time on frequent lines (weekdays): trams promise 4.5 min, 1.7-1.7 min more in reality; buses 5.7 min, 1.1-2.0 min more."
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
  "generato": "2026-10-24T00:36:03+00:00",
  "avviso": [
   "Dati [MISURATO] — pochi giorni",
   "Arrivi misurati con il GPS dei mezzi GTT raccolto dal Raspberry Pi, 2026-10-10 - 2026-10-22: il GPS c'è per il 80% dei passaggi programmati delle corse viste (prima si usava il feed GTT, che sottostima i ritardi: confronto nella scheda). Giorni non tutti interi e solo linee urbane viste dal GPS: vedi i limiti."
  ],
  "scenari": [
   {
    "nome": "Feriale (7 giorni, 1.250.433 passaggi)",
    "numeri": [
     {
      "label": "Passaggi in ritardo oltre 5 min",
      "prima": null,
      "dopo": 16.0,
      "unita": "%"
     },
     {
      "label": "Coppie di bus a grappolo o con un buco (linee frequenti)",
      "prima": null,
      "dopo": 21.6,
      "unita": "%"
     },
     {
      "label": "Ritardo mediano",
      "prima": null,
      "dopo": 0.1,
      "unita": "min"
     },
     {
      "label": "Passaggi in anticipo oltre 1 min",
      "prima": null,
      "dopo": 35.4,
      "unita": "%"
     },
     {
      "label": "Passaggi in ritardo oltre 10 min",
      "prima": null,
      "dopo": 6.41,
      "unita": "%"
     }
    ],
    "nota": "Molti passaggi risultano in anticipo perché l'orario ufficiale ha margini; un ritardo mediano negativo vuol dire 'di solito un po' prima'."
   },
   {
    "nome": "Sabato (2 giorni, 244.547 passaggi)",
    "numeri": [
     {
      "label": "Passaggi in ritardo oltre 5 min",
      "prima": null,
      "dopo": 16.9,
      "unita": "%"
     },
     {
      "label": "Coppie di bus a grappolo o con un buco (linee frequenti)",
      "prima": null,
      "dopo": 20.8,
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
      "dopo": 33.7,
      "unita": "%"
     },
     {
      "label": "Passaggi in ritardo oltre 10 min",
      "prima": null,
      "dopo": 7.12,
      "unita": "%"
     }
    ]
   },
   {
    "nome": "Domenica (1 giorno, 111.568 passaggi)",
    "numeri": [
     {
      "label": "Passaggi in ritardo oltre 5 min",
      "prima": null,
      "dopo": 12.1,
      "unita": "%"
     },
     {
      "label": "Coppie di bus a grappolo o con un buco (linee frequenti)",
      "prima": null,
      "dopo": 18.4,
      "unita": "%"
     },
     {
      "label": "Ritardo mediano",
      "prima": null,
      "dopo": -0.0,
      "unita": "min"
     },
     {
      "label": "Passaggi in anticipo oltre 1 min",
      "prima": null,
      "dopo": 36.7,
      "unita": "%"
     },
     {
      "label": "Passaggi in ritardo oltre 10 min",
      "prima": null,
      "dopo": 4.12,
      "unita": "%"
     }
    ]
   },
   {
    "nome": "Feriale (7 giorni)",
    "numeri": [
     {
      "label": "Attesa media alla fermata, stima bassa",
      "prima": 4.78,
      "dopo": 6.36,
      "unita": "min"
     },
     {
      "label": "Attesa media alla fermata, stima alta",
      "prima": 4.78,
      "dopo": 6.52,
      "unita": "min"
     },
     {
      "label": "Corse programmate assenti dal GPS",
      "prima": null,
      "dopo": 7.7,
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
      "dopo": 6.86,
      "unita": "min"
     },
     {
      "label": "Attesa media alla fermata, stima alta",
      "prima": 4.75,
      "dopo": 6.97,
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
   "tipo_dato": "Tipo di dato: misurato, con la posizione GPS dei mezzi.",
   "titolo": "Circa il 6% dei passaggi arriva con più di 10 minuti di ritardo",
   "domanda": "Quanto spesso i mezzi GTT arrivano in ritardo o a coppie?",
   "numero": {
    "valore": 6.41,
    "unita": "%",
    "testo": "dei passaggi feriali arriva con oltre 10 minuti di ritardo",
    "breve": "dei passaggi in ritardo di oltre 10 minuti"
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
        "valore": 35.4,
        "tono": "blu"
       },
       {
        "label": "puntuali",
        "valore": 48.6,
        "tono": "verde"
       },
       {
        "label": "ritardo da 5 a 10 minuti",
        "valore": 9.59,
        "tono": "giallo"
       },
       {
        "label": "ritardo oltre 10 minuti",
        "valore": 6.41,
        "tono": "rosso"
       }
      ]
     },
     {
      "label": "sabato",
      "voci": [
       {
        "label": "in anticipo (oltre 1 minuto)",
        "valore": 33.7,
        "tono": "blu"
       },
       {
        "label": "puntuali",
        "valore": 49.4,
        "tono": "verde"
       },
       {
        "label": "ritardo da 5 a 10 minuti",
        "valore": 9.78,
        "tono": "giallo"
       },
       {
        "label": "ritardo oltre 10 minuti",
        "valore": 7.12,
        "tono": "rosso"
       }
      ]
     },
     {
      "label": "domenica",
      "voci": [
       {
        "label": "in anticipo (oltre 1 minuto)",
        "valore": 36.7,
        "tono": "blu"
       },
       {
        "label": "puntuali",
        "valore": 51.2,
        "tono": "verde"
       },
       {
        "label": "ritardo da 5 a 10 minuti",
        "valore": 7.98,
        "tono": "giallo"
       },
       {
        "label": "ritardo oltre 10 minuti",
        "valore": 4.12,
        "tono": "rosso"
       }
      ]
     }
    ]
   },
   "punti": [
    "Guardando solo la partenza dal capolinea, i passaggi con oltre 10 minuti di ritardo sono ~5%.",
    "La linea più in ritardo è la 17: ~41% dei passaggi feriali oltre 5 minuti.",
    "I tram arrivano a grappolo più dei bus: ~27% delle coppie di mezzi contro ~18%."
   ],
   "altri": [
    {
     "tipo": "barre",
     "titolo": "GPS e dato ufficiale GTT: passaggi con oltre 10 minuti di ritardo",
     "unita": "%",
     "nota": "Il GPS è la media della settimana, in quattro modi di contare. GTT è l'anno 2025, tutte le linee, con un metodo non pubblicato.",
     "voci": [
      {
       "label": "GTT (2025, anno intero)",
       "valore": 2
      },
      {
       "label": "GPS, a ogni fermata",
       "valore": 6,
       "tono": "rosso"
      },
      {
       "label": "GPS, solo alla prima fermata",
       "valore": 5,
       "tono": "rosso"
      },
      {
       "label": "GPS, solo a metà corsa",
       "valore": 6,
       "tono": "rosso"
      },
      {
       "label": "GPS, escluse le fasce 7-9 e 16-19",
       "valore": 6,
       "tono": "rosso"
      }
     ]
    },
    {
     "tipo": "linea",
     "titolo": "Ritardo oltre 5 minuti, per fascia oraria (feriale)",
     "unita": "%",
     "categorie": [
      "mattino (7-9)",
      "giorno (9-16)",
      "sera (16-19)",
      "tarda sera (19-24)"
     ],
     "serie": [
      {
       "label": "passaggi in ritardo",
       "valori": [
        16,
        16,
        20,
        18
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
     "2026-10-10 - 2026-10-22"
    ],
    [
     "Passaggi con GPS valido",
     "1.606.548 (79,8% di quelli programmati dalle corse viste)"
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
    ],
    [
     "Periodo dei dati",
     "dal 10/10/2026 al 22/10/2026"
    ]
   ],
   "limiti": [
    "Pochi giorni: 7 feriali, 2 sabati e 1 domenica, non tutti interi.",
    "Solo le linee urbane viste dal GPS, dalle 5 a mezzanotte.",
    "Il GPS copre circa il 80% dei passaggi programmati; le corse mai viste non si contano.",
    "Si conta quanto spesso c'è ritardo, non quante persone aspettano."
   ],
   "mappa": {
    "id": "puntualita",
    "nota": "Nella mappa, tema «Puntualità delle linee»: ogni linea colorata per ritardo nell'ora scelta con il cursore."
   },
   "anima": {
    "tipo": "quadratini",
    "totale": 100,
    "oltre5": 16.0,
    "oltre10": 6.41,
    "testo_tutto": "su 100 passaggi in un feriale arrivano con oltre 5 minuti di ritardo",
    "fasi": [
     {
      "label": "su 100 al mattino (7-9)",
      "valore": 15.5
     },
     {
      "label": "su 100 di giorno (9-16)",
      "valore": 16.3
     },
     {
      "label": "su 100 alla sera (16-19)",
      "valore": 20.4
     },
     {
      "label": "su 100 a tarda sera (19-24)",
      "valore": 18.2
     }
    ],
    "legenda5": "oltre 5 minuti",
    "legenda10": "oltre 10 minuti",
    "didascalia": "Su 100 passaggi feriali, circa 16 arrivano con più di 5 minuti di ritardo (16%); con più di 10 minuti circa 6. Poi il giorno, fascia per fascia."
   },
   "confronto": [
    "GTT dichiara il 2,3% oltre 10 minuti nel 2025: media dell'anno, tutte le linee, metodo non pubblicato.",
    "Il GPS misura pochi giorni di ottobre sulle linee urbane: 6,2% a ogni fermata, 5,3% alla partenza.",
    "Anche contando come GTT alla partenza si trova il 5,3%; il resto della differenza è stagione e metodo.",
    "Il grafico mostra la media della settimana (feriale 5 : sabato 1 : domenica 1).",
    "Solo feriali: 6,41% a ogni fermata, 5,48% alla prima, 6,15% a metà corsa, 5,96% senza le fasce 7-9 e 16-19."
   ],
   "extra": {
    "titolo": "Quanto si aspetta alla fermata",
    "punto": "Sulle linee frequenti si aspetta ~1 minuto e mezzo in più di quanto promette l'orario.",
    "grafico": {
     "tipo": "barre",
     "titolo": "Quanto si aspetta in più di quanto dice l'orario",
     "unita": "min",
     "nota": "Ogni barra è una fascia del giorno feriale: i minuti di attesa in più rispetto all'orario. A destra l'attesa reale contro quella promessa.",
     "voci": [
      {
       "label": "mattino (7-9)",
       "valore": 1.3,
       "tono": "rosso",
       "testo": "~6 min invece di ~5"
      },
      {
       "label": "giorno (9-16)",
       "valore": 1.4,
       "tono": "rosso",
       "testo": "~5 min invece di ~4"
      },
      {
       "label": "sera (16-19)",
       "valore": 2.1,
       "tono": "rosso",
       "testo": "~7 min invece di ~4"
      },
      {
       "label": "tarda sera (19-24)",
       "valore": 1.7,
       "tono": "rosso",
       "testo": "~10 min invece di ~8"
      }
     ]
    }
   },
   "chiave": {
    "valore": "~6",
    "unita": "%",
    "testo": "dei passaggi arriva con oltre 10 minuti di ritardo"
   }
  },
  "forma_en": {
   "tipo_dato": "Type of data: measured, with the GPS position of the vehicles.",
   "titolo": "About 6% of stop passages are more than 10 minutes late",
   "domanda": "How often are GTT vehicles late or bunched together?",
   "numero": {
    "valore": 6.41,
    "unita": "%",
    "testo": "of weekday arrivals are more than 10 minutes late",
    "breve": "of arrivals more than 10 minutes late"
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
        "valore": 35.4,
        "tono": "blu"
       },
       {
        "label": "on time",
        "valore": 48.6,
        "tono": "verde"
       },
       {
        "label": "5 to 10 minutes late",
        "valore": 9.59,
        "tono": "giallo"
       },
       {
        "label": "more than 10 minutes late",
        "valore": 6.41,
        "tono": "rosso"
       }
      ]
     },
     {
      "label": "Saturday",
      "voci": [
       {
        "label": "early (more than 1 minute)",
        "valore": 33.7,
        "tono": "blu"
       },
       {
        "label": "on time",
        "valore": 49.4,
        "tono": "verde"
       },
       {
        "label": "5 to 10 minutes late",
        "valore": 9.78,
        "tono": "giallo"
       },
       {
        "label": "more than 10 minutes late",
        "valore": 7.12,
        "tono": "rosso"
       }
      ]
     },
     {
      "label": "Sunday",
      "voci": [
       {
        "label": "early (more than 1 minute)",
        "valore": 36.7,
        "tono": "blu"
       },
       {
        "label": "on time",
        "valore": 51.2,
        "tono": "verde"
       },
       {
        "label": "5 to 10 minutes late",
        "valore": 7.98,
        "tono": "giallo"
       },
       {
        "label": "more than 10 minutes late",
        "valore": 4.12,
        "tono": "rosso"
       }
      ]
     }
    ]
   },
   "punti": [
    "Counting only the departure from the terminus, arrivals more than 10 minutes late are ~5%.",
    "The most delayed line is 17: ~41% of weekday arrivals are more than 5 minutes late.",
    "Trams bunch together more than buses: ~27% of pairs of vehicles against ~18%."
   ],
   "altri": [
    {
     "tipo": "barre",
     "titolo": "GPS and official GTT figure: arrivals more than 10 minutes late",
     "unita": "%",
     "nota": "GPS is the weekly average, counted in four ways. GTT is the year 2025, all lines, with an unpublished method.",
     "voci": [
      {
       "label": "GTT (2025, whole year)",
       "valore": 2
      },
      {
       "label": "GPS, at every stop",
       "valore": 6,
       "tono": "rosso"
      },
      {
       "label": "GPS, first stop only",
       "valore": 5,
       "tono": "rosso"
      },
      {
       "label": "GPS, mid-trip only",
       "valore": 6,
       "tono": "rosso"
      },
      {
       "label": "GPS, excluding 7-9 and 16-19",
       "valore": 6,
       "tono": "rosso"
      }
     ]
    },
    {
     "tipo": "linea",
     "titolo": "Delay over 5 minutes, by time of day (weekday)",
     "unita": "%",
     "categorie": [
      "morning (7-9)",
      "daytime (9-16)",
      "evening (16-19)",
      "late evening (19-24)"
     ],
     "serie": [
      {
       "label": "late arrivals",
       "valori": [
        16,
        16,
        20,
        18
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
     "2026-10-10 - 2026-10-22"
    ],
    [
     "Arrivals with a valid GPS fix",
     "1,606,548 (79.8% of those scheduled for the trips seen)"
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
    ],
    [
     "Data period",
     "from 10/10/2,026 to 22/10/2,026"
    ]
   ],
   "limiti": [
    "Few days: 7 weekdays, 2 Saturdays and 1 Sunday, not all complete.",
    "Urban lines seen by the GPS only, from 5 a.m. to midnight.",
    "The GPS covers about 80% of scheduled arrivals; trips never seen are not counted.",
    "The figure counts how often there is a delay, not how many people are waiting."
   ],
   "mappa": {
    "id": "puntualita",
    "nota": "Nella mappa, tema «Puntualità delle linee»: ogni linea colorata per ritardo nell'ora scelta con il cursore."
   },
   "anima": {
    "tipo": "quadratini",
    "totale": 100,
    "oltre5": 16.0,
    "oltre10": 6.41,
    "testo_tutto": "in 100 weekday stop passages are more than 5 minutes late",
    "fasi": [
     {
      "label": "out of 100 in the morning (7-9)",
      "valore": 15.5
     },
     {
      "label": "in 100 during the day (9-16)",
      "valore": 16.3
     },
     {
      "label": "out of 100 in the evening (16-19)",
      "valore": 20.4
     },
     {
      "label": "out of 100 in the late evening (19-24)",
      "valore": 18.2
     }
    ],
    "legenda5": "over 5 minutes",
    "legenda10": "over 10 minutes",
    "didascalia": "Out of 100 weekday stop passages, about 16 are more than 5 minutes late (16%); about 6 more than 10 minutes. Then the day, time band by time band."
   },
   "confronto": [
    "GTT reports 2.3% over 10 minutes in 2025: yearly average, all lines, method not published.",
    "The GPS measures a few days of October on urban lines: 6.2% at every stop, 5.3% at departure.",
    "Even counting at departure like GTT, the figure is 5.3%; the rest of the difference is season and method.",
    "The chart shows the weekly average (weekday 5 : Saturday 1 : Sunday 1).",
    "Weekdays only: 6.41% at every stop, 5.48% at the first, 6.15% mid-trip, 5.96% without the 7-9 and 16-19 bands."
   ],
   "extra": {
    "titolo": "How long you wait at the stop",
    "punto": "On frequent lines the wait is ~1 and a half minutes longer than the timetable promises.",
    "grafico": {
     "tipo": "barre",
     "titolo": "How much longer the wait is than the timetable says",
     "unita": "min",
     "nota": "Each bar is a part of the weekday: the extra minutes of waiting compared with the timetable. On the right, the real wait against the promised one.",
     "voci": [
      {
       "label": "morning (7-9)",
       "valore": 1.3,
       "tono": "rosso",
       "testo": "~6 min instead of ~5"
      },
      {
       "label": "daytime (9-16)",
       "valore": 1.4,
       "tono": "rosso",
       "testo": "~5 min instead of ~4"
      },
      {
       "label": "evening (16-19)",
       "valore": 2.1,
       "tono": "rosso",
       "testo": "~7 min instead of ~4"
      },
      {
       "label": "late evening (19-24)",
       "valore": 1.7,
       "tono": "rosso",
       "testo": "~10 min instead of ~8"
      }
     ]
    }
   },
   "chiave": {
    "valore": "~6",
    "unita": "%",
    "testo": "of arrivals are more than 10 minutes late"
   }
  },
  "numero_pubblico": 2,
  "_nome": "risultato4_riepilogo_mappa.json"
 },
 {
  "risultato": "6",
  "titolo": "Parcheggi per lasciare l'auto",
  "tag": "STIMATO / MISURATO (dati scarsi)",
  "stato": "Aggiornato al 24/10/2026",
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
    "nota": "[MISURATO] 8 giorni validi; linea piena feriale, tratteggiata weekend [DATI SCARSI].",
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
       0.804,
       0.829,
       0.877,
       0.903,
       0.919,
       0.921,
       0.921,
       0.916,
       0.91,
       0.904,
       0.894,
       0.877,
       0.846,
       0.813,
       0.802,
       0.801,
       0.801,
       0.8
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
    "nota": "[MISURATO] 8 giorni validi; linea piena feriale, tratteggiata weekend [DATI SCARSI].",
    "serie": [
     {
      "label": "giorno feriale",
      "valori": [
       0.537,
       0.538,
       0.538,
       0.538,
       0.537,
       0.535,
       0.537,
       0.53,
       0.535,
       0.555,
       0.556,
       0.552,
       0.553,
       0.552,
       0.551,
       0.548,
       0.542,
       0.533,
       0.52,
       0.507,
       0.515,
       0.521,
       0.525,
       0.532
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
    "nota": "[MISURATO] 8 giorni validi; linea piena feriale, tratteggiata weekend [DATI SCARSI].",
    "serie": [
     {
      "label": "giorno feriale",
      "valori": [
       0.016,
       0.011,
       0.01,
       0.011,
       0.011,
       0.01,
       0.01,
       0.009,
       0.009,
       0.009,
       0.01,
       0.01,
       0.009,
       0.009,
       0.01,
       0.011,
       0.011,
       0.011,
       0.01,
       0.012,
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
    "nota": "[MISURATO] 8 giorni validi; linea piena feriale, tratteggiata weekend [DATI SCARSI].",
    "serie": [
     {
      "label": "giorno feriale",
      "valori": [
       0.516,
       0.517,
       0.519,
       0.519,
       0.519,
       0.51,
       0.488,
       0.44,
       0.4,
       0.36,
       0.31,
       0.292,
       0.3,
       0.308,
       0.309,
       0.31,
       0.31,
       0.338,
       0.378,
       0.42,
       0.449,
       0.465,
       0.487,
       0.5
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
    "valore": "15/10, 16/10, 19/10, 20/10, 21/10, 22/10"
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
    "15/10, 16/10, 19/10, 20/10, 21/10 e 22/10"
   ]
  ],
  "limiti": [
   "Auto che passano: modello del traffico (percorso più veloce, senza code), stima debole: solo ordine di grandezza. Le stesse auto passano davanti a più fermate dello stesso corso.",
   "Riempimento misurato su soli 6 giorni feriali e solo dove il 5T lo trasmette [DATI SCARSI]: Fermi e i parcheggi gratuiti non sono misurati.",
   "Quota di chi lascia l'auto: indagine sugli spostamenti 2022, poche interviste.",
   "Controllo con i sensori 5T del mattino: il modello mette le strade d'ingresso in un ordine simile solo in parte (ρ = 0,46 su 24 luoghi); sottostima gli ingressi da nord-ovest.",
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
    "valore": "misurato dal 5T dove c'è (6 giorni feriali, ore 10-16); pieno ≥ 85%",
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
  "generato": "2026-10-24T00:36:03+00:00",
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
   "Check against the 5T morning sensors: the model ranks the entry roads in a similar order only in part (rho = 0.46 over 24 places); it underestimates the entries from the north-west."
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
   "tipo_dato": "Tipo di dato: calcolato da dati veri e in parte misurato, su pochi giorni di dati.",
   "titolo": "2 fermate importanti su 3 non hanno abbastanza posti per lasciare l'auto",
   "domanda": "Chi arriva in auto da fuori trova dove lasciarla vicino a una fermata importante, per proseguire coi mezzi?",
   "numero": {
    "valore": 179,
    "unita": "",
    "testo": "fermate importanti su 274 non hanno posti bastanti a 400 metri a piedi",
    "breve": "fermate importanti senza posti per l'auto"
   },
   "principale": {
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
   },
   "punti": [
    "68 fermate importanti non hanno nessun parcheggio vicino, 111 troppo pochi.",
    "Il primo dei 12 punti d'ingresso dove servono posti è Santa Rita: ne mancano ~450.",
    "In 8 punti su 12, lasciata l'auto, il bus arriva in centro in al più 1,5 volte il tempo dell'auto."
   ],
   "altri": [
    {
     "tipo": "gara",
     "titolo": "La gara: bus e auto verso Piazza Castello, alle 8 di un feriale",
     "nota": "Bus e auto partono insieme da ogni parcheggio, uno dopo l'altro. L'auto ha il tempo previsto da TomTom, parcheggio compreso.",
     "luoghi": [
      {
       "nome": "Santa Rita",
       "gruppo": "Punti prioritari",
       "bus": 36.0,
       "auto_min": 26.8,
       "auto_max": 26.8,
       "giudizio": "il bus conviene"
      },
      {
       "nome": "Metro Massaua",
       "gruppo": "Punti prioritari",
       "bus": 25.0,
       "auto_min": 26.9,
       "auto_max": 26.9,
       "giudizio": "il bus conviene"
      },
      {
       "nome": "Ponte Cavalieri Templari",
       "gruppo": "Punti prioritari",
       "bus": 51.0,
       "auto_min": 26.6,
       "auto_max": 26.6,
       "giudizio": "il bus non conviene"
      },
      {
       "nome": "Regina Margherita",
       "gruppo": "Punti prioritari",
       "bus": 31.0,
       "auto_min": 27.7,
       "auto_max": 27.7,
       "giudizio": "il bus conviene"
      },
      {
       "nome": "Pasini",
       "gruppo": "Punti prioritari",
       "bus": 28.0,
       "auto_min": 20.4,
       "auto_max": 20.4,
       "giudizio": "il bus conviene"
      },
      {
       "nome": "Leonardo Da Vinci",
       "gruppo": "Punti prioritari",
       "bus": 59.0,
       "auto_min": 38.5,
       "auto_max": 38.5,
       "giudizio": "il bus non conviene"
      },
      {
       "nome": "Drosso Cap",
       "gruppo": "Punti prioritari",
       "bus": 43.0,
       "auto_min": 31.3,
       "auto_max": 31.3,
       "giudizio": "il bus conviene"
      },
      {
       "nome": "Stura Lazio",
       "gruppo": "Punti prioritari",
       "bus": 37.0,
       "auto_min": 26.9,
       "auto_max": 26.9,
       "giudizio": "il bus conviene"
      },
      {
       "nome": "Marsè",
       "gruppo": "Punti prioritari",
       "bus": 61.0,
       "auto_min": 33.5,
       "auto_max": 33.5,
       "giudizio": "il bus non conviene"
      },
      {
       "nome": "Derna Est",
       "gruppo": "Punti prioritari",
       "bus": 34.0,
       "auto_min": 23.7,
       "auto_max": 23.7,
       "giudizio": "il bus conviene"
      },
      {
       "nome": "Ferrara",
       "gruppo": "Punti prioritari",
       "bus": 49.0,
       "auto_min": 34.8,
       "auto_max": 34.8,
       "giudizio": "il bus conviene"
      },
      {
       "nome": "Zara",
       "gruppo": "Punti prioritari",
       "bus": 33.0,
       "auto_min": 18.8,
       "auto_max": 18.8,
       "giudizio": "il bus non conviene"
      },
      {
       "nome": "Stura",
       "gruppo": "Interscambi esistenti",
       "bus": 39.0,
       "auto_min": 30.2,
       "auto_max": 30.2,
       "giudizio": "il bus conviene"
      },
      {
       "nome": "Venchi Unica",
       "gruppo": "Interscambi esistenti",
       "bus": 28.0,
       "auto_min": 28.8,
       "auto_max": 28.8,
       "giudizio": "il bus conviene"
      },
      {
       "nome": "Caio Mario",
       "gruppo": "Interscambi esistenti",
       "bus": 38.0,
       "auto_min": 30.1,
       "auto_max": 30.1,
       "giudizio": "il bus conviene"
      },
      {
       "nome": "Fermi",
       "gruppo": "Interscambi esistenti",
       "bus": 31.0,
       "auto_min": 36.6,
       "auto_max": 36.6,
       "giudizio": "il bus conviene"
      },
      {
       "nome": "Sofia",
       "gruppo": "Interscambi esistenti",
       "bus": 33.0,
       "auto_min": 21.8,
       "auto_max": 21.8,
       "giudizio": "il bus non conviene"
      }
     ],
     "scelto": 0
    },
    {
     "tipo": "barre",
     "titolo": "I parcheggi di scambio che ci sono già: quanto sono pieni e quanto ci mette il bus al centro",
     "unita": "minuti",
     "nota": "Barra = minuti coi mezzi pubblici fino a Piazza Castello alle 8. A destra il tempo in auto, parcheggio compreso (TomTom), e quanto è pieno il parcheggio di giorno.",
     "voci": [
      {
       "label": "Stura",
       "valore": 39,
       "testo": "39 contro 30 in auto · pieno di giorno"
      },
      {
       "label": "Venchi Unica",
       "valore": 28,
       "testo": "28 contro 29 in auto · a metà"
      },
      {
       "label": "Caio Mario",
       "valore": 38,
       "testo": "38 contro 30 in auto · con posti liberi"
      },
      {
       "label": "Fermi",
       "valore": 31,
       "testo": "31 contro 37 in auto · riempimento non noto"
      },
      {
       "label": "Sofia",
       "valore": 33,
       "testo": "33 contro 22 in auto · con posti liberi"
      }
     ]
    }
   ],
   "calcolo": [
    "Fermate importanti: fuori dal centro, con metro, stazione o capolinea, oppure 10 corse all'ora.",
    "Le auto in entrata vengono dall'indagine sugli spostamenti 2022, assegnate al percorso più veloce.",
    "Auto da fermare: auto che passano per il 5,8% che già oggi lascia l'auto. Posti: parcheggi adatti entro 400 metri.",
    "Punti prioritari: fermate senza posti bastanti raggruppate entro 1 km, uno per asse d'ingresso.",
    "Bus contro auto: minuti coi mezzi verso Piazza Castello alle 8, contro l'auto. Auto: tempo a flusso libero per il fattore TomTom del percorso, più 5 minuti. Dati di traffico: TomTom.",
    "Pareggio: con 16 minuti persi a parcheggiare in centro, l'auto impiega quanto il bus (mediana dei 12 punti, TomTom).",
    "Dei punti dove il bus conviene, 5 su 8 sono vicini alla soglia: un'auto il 10% più veloce cambia classe.",
    "Con la stima dei sensori del traffico, più favorevole all'auto (fattore 1,2), il pareggio sale a 28 minuti."
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
     "Periodo del riempimento dei parcheggi",
     "dal 15/10/2026 al 22/10/2026"
    ],
    [
     "Bus contro auto",
     "verso Piazza Castello alle 8; auto: fattore TomTom del percorso (mediana 2,6) + 5 minuti; stima più favorevole all'auto: sensori 5T, fattore 1,2"
    ]
   ],
   "limiti": [
    "Le auto che passano vengono da un modello del traffico. I posti sono spesso stimati: quelli che mancano sono un ordine di grandezza. Con metà o doppio di chi lascia l'auto, le fermate senza posti bastanti vanno da 135 a 212 su 274.",
    "I tempi coi mezzi sono solo GTT, senza treni. La stima dei sensori non conta semafori e incroci: è la più favorevole all'auto.",
    "Tempi in auto previsti da TomTom su traffico tipico di un feriale di novembre, non misurati in un giorno preciso. Si usa un solo servizio.",
    "Il costo del parcheggio non è nel calcolo: pesa come minuti in più. Si guarda un solo punto per luogo e una sola destinazione."
   ],
   "mappa": {
    "id": "interscambio",
    "nota": "Due domande nella mappa, nel menu «Cosa vedere»: dove ci sono parcheggi e dove servirebbe di più un parcheggio."
   },
   "anima": {
    "tipo": "fermate",
    "contorno": {
     "d": "M879 130l-33 35l-2 -35l22 -12l13 12zM452 11l123 41l18 -10l2 11l11 14l35 -6l42 -20l3 -17l6 -5l25 -3l34 9l-9 37l9 34l48 23l13 3l-8 28l46 93l43 29l-7 39l-27 21l-21 13l28 44l18 20l30 12l64 3l-8 11l3 8l10 6l12 -1l5 4l-90 145l-79 95l-39 49l-51 48l-40 17l-37 36l-129 15l-120 41l-18 59l-73 6l-70 -8l-19 1l-59 -16l-11 5l-87 -31l-14 -16l8 -25l8 -1l36 8l35 -80l-30 11l-67 -45l-44 -39l-10 -14l13 -18l32 -4l128 80l25 -39l45 -134l-1 -15l-33 5l-57 -11l9 -32l9 -4l6 -11l-20 -24l-25 -6l61 -129l13 -59l-19 -21l-12 -51l13 -8l30 2l12 -4l1 -39l122 13l40 -5l0 -15l-7 -11l-3 -50l9 -10l12 -31l-6 -29l2 -15l38 -36l7 -2l8 11z",
     "vb": [
      -297,
      -606,
      1582,
      1730
     ]
    },
    "punti": [
     [
      186,
      477,
      0,
      365
     ],
     [
      216,
      475,
      1,
      335
     ],
     [
      123,
      481,
      1,
      427
     ],
     [
      687,
      138,
      0,
      387
     ],
     [
      261,
      473,
      2,
      290
     ],
     [
      295,
      471,
      2,
      257
     ],
     [
      690,
      150,
      0,
      377
     ],
     [
      692,
      135,
      0,
      392
     ],
     [
      445,
      255,
      1,
      267
     ],
     [
      455,
      252,
      1,
      266
     ],
     [
      442,
      258,
      1,
      265
     ],
     [
      426,
      895,
      1,
      414
     ],
     [
      546,
      301,
      1,
      199
     ],
     [
      479,
      1008,
      0,
      513
     ],
     [
      369,
      154,
      0,
      390
     ],
     [
      342,
      1065,
      0,
      602
     ],
     [
      339,
      1063,
      0,
      601
     ],
     [
      393,
      817,
      0,
      354
     ],
     [
      574,
      300,
      1,
      201
     ],
     [
      576,
      299,
      1,
      203
     ],
     [
      476,
      1024,
      1,
      529
     ],
     [
      69,
      465,
      0,
      482
     ],
     [
      1237,
      976,
      0,
      836
     ],
     [
      401,
      839,
      0,
      370
     ],
     [
      241,
      917,
      1,
      519
     ],
     [
      346,
      682,
      2,
      273
     ],
     [
      257,
      746,
      2,
      383
     ],
     [
      680,
      145,
      0,
      378
     ],
     [
      356,
      671,
      2,
      259
     ],
     [
      268,
      738,
      1,
      369
     ],
     [
      175,
      791,
      1,
      475
     ],
     [
      221,
      475,
      1,
      330
     ],
     [
      290,
      854,
      1,
      439
     ],
     [
      136,
      480,
      1,
      414
     ],
     [
      185,
      787,
      2,
      464
     ],
     [
      259,
      896,
      1,
      491
     ],
     [
      245,
      754,
      1,
      397
     ],
     [
      264,
      887,
      2,
      481
     ],
     [
      279,
      871,
      2,
      459
     ],
     [
      248,
      754,
      1,
      395
     ],
     [
      592,
      599,
      2,
      108
     ],
     [
      270,
      882,
      2,
      474
     ],
     [
      204,
      782,
      2,
      446
     ],
     [
      253,
      900,
      1,
      498
     ],
     [
      200,
      782,
      2,
      449
     ],
     [
      236,
      762,
      1,
      409
     ],
     [
      240,
      648,
      1,
      344
     ],
     [
      727,
      514,
      1,
      178
     ],
     [
      299,
      840,
      1,
      423
     ],
     [
      233,
      762,
      1,
      411
     ],
     [
      743,
      510,
      1,
      193
     ],
     [
      325,
      699,
      1,
      300
     ],
     [
      311,
      828,
      1,
      406
     ],
     [
      269,
      652,
      1,
      319
     ],
     [
      375,
      748,
      0,
      304
     ],
     [
      337,
      685,
      2,
      282
     ],
     [
      10,
      488,
      1,
      540
     ],
     [
      784,
      403,
      1,
      253
     ],
     [
      390,
      729,
      0,
      279
     ],
     [
      345,
      687,
      2,
      277
     ],
     [
      334,
      799,
      0,
      369
     ],
     [
      313,
      825,
      0,
      402
     ],
     [
      353,
      776,
      1,
      339
     ],
     [
      331,
      804,
      0,
      375
     ],
     [
      293,
      721,
      1,
      339
     ],
     [
      706,
      332,
      0,
      229
     ],
     [
      1049,
      -566,
      0,
      1177
     ],
     [
      349,
      780,
      1,
      345
     ],
     [
      207,
      476,
      0,
      344
     ],
     [
      47,
      638,
      2,
      522
     ],
     [
      414,
      698,
      1,
      240
     ],
     [
      320,
      816,
      0,
      391
     ],
     [
      779,
      426,
      1,
      241
     ],
     [
      273,
      876,
      2,
      467
     ],
     [
      794,
      390,
      1,
      268
     ],
     [
      159,
      480,
      1,
      392
     ],
     [
      156,
      478,
      1,
      395
     ],
     [
      -57,
      492,
      2,
      607
     ],
     [
      260,
      901,
      1,
      495
     ],
     [
      647,
      229,
      2,
      288
     ],
     [
      672,
      177,
      1,
      345
     ],
     [
      632,
      261,
      0,
      253
     ],
     [
      663,
      197,
      0,
      323
     ],
     [
      223,
      647,
      1,
      359
     ],
     [
      256,
      650,
      1,
      330
     ],
     [
      268,
      650,
      1,
      319
     ],
     [
      399,
      717,
      2,
      264
     ],
     [
      856,
      357,
      1,
      338
     ],
     [
      507,
      999,
      1,
      501
     ],
     [
      722,
      316,
      0,
      252
     ],
     [
      674,
      534,
      2,
      129
     ],
     [
      95,
      482,
      1,
      455
     ],
     [
      553,
      300,
      1,
      200
     ],
     [
      432,
      675,
      2,
      211
     ],
     [
      607,
      268,
      0,
      239
     ],
     [
      324,
      812,
      0,
      385
     ],
     [
      393,
      348,
      2,
      219
     ],
     [
      380,
      377,
      2,
      210
     ],
     [
      936,
      265,
      0,
      452
     ],
     [
      429,
      679,
      2,
      216
     ],
     [
      778,
      469,
      2,
      230
     ],
     [
      532,
      729,
      1,
      230
     ],
     [
      315,
      828,
      1,
      403
     ],
     [
      927,
      309,
      1,
      423
     ],
     [
      516,
      367,
      1,
      137
     ],
     [
      -23,
      490,
      1,
      573
     ],
     [
      367,
      758,
      0,
      316
     ],
     [
      -19,
      489,
      1,
      569
     ],
     [
      620,
      561,
      1,
      93
     ],
     [
      404,
      716,
      2,
      261
     ],
     [
      510,
      359,
      1,
      147
     ],
     [
      294,
      841,
      1,
      426
     ],
     [
      365,
      760,
      0,
      319
     ],
     [
      287,
      718,
      1,
      342
     ],
     [
      750,
      286,
      2,
      293
     ],
     [
      292,
      602,
      2,
      277
     ],
     [
      284,
      660,
      1,
      310
     ],
     [
      333,
      473,
      1,
      219
     ],
     [
      307,
      515,
      1,
      243
     ],
     [
      337,
      464,
      1,
      216
     ],
     [
      281,
      656,
      1,
      311
     ],
     [
      402,
      713,
      2,
      259
     ],
     [
      -175,
      500,
      0,
      725
     ],
     [
      296,
      666,
      1,
      303
     ],
     [
      766,
      244,
      0,
      335
     ],
     [
      711,
      333,
      0,
      232
     ],
     [
      623,
      282,
      0,
      230
     ],
     [
      303,
      824,
      1,
      407
     ],
     [
      621,
      286,
      0,
      225
     ],
     [
      630,
      276,
      1,
      238
     ],
     [
      700,
      342,
      0,
      218
     ],
     [
      600,
      330,
      1,
      177
     ],
     [
      324,
      679,
      2,
      288
     ],
     [
      -178,
      498,
      0,
      728
     ],
     [
      -150,
      496,
      0,
      700
     ],
     [
      289,
      679,
      2,
      316
     ],
     [
      283,
      501,
      2,
      267
     ],
     [
      513,
      356,
      0,
      149
     ],
     [
      99,
      818,
      0,
      552
     ],
     [
      111,
      814,
      0,
      540
     ],
     [
      288,
      700,
      1,
      330
     ],
     [
      482,
      999,
      0,
      504
     ],
     [
      591,
      352,
      1,
      154
     ],
     [
      -257,
      504,
      0,
      807
     ],
     [
      103,
      818,
      0,
      549
     ],
     [
      122,
      811,
      2,
      529
     ],
     [
      444,
      252,
      1,
      270
     ],
     [
      555,
      262,
      2,
      238
     ],
     [
      -95,
      495,
      1,
      645
     ],
     [
      725,
      1084,
      2,
      610
     ],
     [
      588,
      358,
      2,
      147
     ],
     [
      533,
      260,
      2,
      241
     ],
     [
      428,
      266,
      1,
      264
     ],
     [
      688,
      357,
      0,
      199
     ],
     [
      422,
      290,
      2,
      246
     ],
     [
      284,
      56,
      0,
      518
     ],
     [
      312,
      806,
      0,
      388
     ],
     [
      411,
      310,
      2,
      235
     ],
     [
      539,
      366,
      0,
      134
     ],
     [
      -99,
      493,
      1,
      649
     ],
     [
      421,
      287,
      2,
      249
     ],
     [
      718,
      322,
      0,
      245
     ],
     [
      431,
      264,
      1,
      264
     ],
     [
      381,
      668,
      0,
      238
     ],
     [
      691,
      355,
      0,
      202
     ],
     [
      493,
      994,
      0,
      497
     ],
     [
      315,
      803,
      0,
      383
     ],
     [
      530,
      262,
      2,
      239
     ],
     [
      371,
      396,
      2,
      207
     ],
     [
      313,
      674,
      2,
      294
     ],
     [
      434,
      249,
      1,
      277
     ],
     [
      51,
      460,
      0,
      501
     ],
     [
      311,
      671,
      2,
      294
     ],
     [
      299,
      665,
      1,
      300
     ],
     [
      -221,
      501,
      0,
      771
     ],
     [
      302,
      546,
      2,
      252
     ],
     [
      -196,
      499,
      0,
      746
     ],
     [
      609,
      312,
      1,
      197
     ],
     [
      984,
      257,
      0,
      497
     ],
     [
      290,
      632,
      1,
      292
     ],
     [
      709,
      325,
      0,
      236
     ],
     [
      748,
      294,
      2,
      286
     ],
     [
      -224,
      503,
      0,
      774
     ],
     [
      788,
      288,
      2,
      319
     ],
     [
      813,
      284,
      2,
      340
     ],
     [
      360,
      719,
      0,
      290
     ],
     [
      575,
      378,
      1,
      125
     ],
     [
      619,
      304,
      0,
      208
     ],
     [
      598,
      335,
      1,
      172
     ],
     [
      611,
      307,
      1,
      202
     ],
     [
      1029,
      199,
      0,
      566
     ],
     [
      593,
      391,
      1,
      117
     ],
     [
      436,
      261,
      1,
      265
     ],
     [
      310,
      510,
      1,
      240
     ],
     [
      580,
      375,
      1,
      129
     ],
     [
      345,
      249,
      0,
      324
     ],
     [
      -151,
      501,
      0,
      701
     ],
     [
      576,
      384,
      2,
      119
     ],
     [
      265,
      645,
      1,
      320
     ],
     [
      287,
      774,
      0,
      380
     ],
     [
      766,
      291,
      2,
      301
     ],
     [
      600,
      270,
      2,
      235
     ],
     [
      293,
      571,
      2,
      267
     ],
     [
      614,
      410,
      0,
      110
     ],
     [
      651,
      387,
      0,
      152
     ],
     [
      428,
      675,
      1,
      213
     ],
     [
      296,
      566,
      2,
      262
     ],
     [
      677,
      370,
      1,
      182
     ],
     [
      247,
      761,
      1,
      400
     ],
     [
      667,
      377,
      1,
      170
     ],
     [
      266,
      628,
      2,
      312
     ],
     [
      626,
      435,
      1,
      100
     ],
     [
      423,
      214,
      1,
      313
     ],
     [
      442,
      891,
      1,
      406
     ],
     [
      412,
      205,
      0,
      326
     ],
     [
      522,
      365,
      0,
      138
     ],
     [
      391,
      714,
      1,
      267
     ],
     [
      411,
      953,
      0,
      474
     ],
     [
      562,
      371,
      0,
      130
     ],
     [
      442,
      692,
      0,
      220
     ],
     [
      -41,
      324,
      0,
      617
     ],
     [
      -16,
      321,
      1,
      594
     ],
     [
      387,
      177,
      2,
      362
     ],
     [
      374,
      946,
      0,
      479
     ],
     [
      423,
      230,
      2,
      298
     ],
     [
      234,
      551,
      2,
      320
     ],
     [
      403,
      980,
      1,
      502
     ],
     [
      419,
      201,
      0,
      326
     ],
     [
      353,
      1052,
      0,
      586
     ],
     [
      263,
      687,
      1,
      343
     ],
     [
      425,
      901,
      1,
      420
     ],
     [
      423,
      903,
      1,
      423
     ],
     [
      -93,
      327,
      0,
      666
     ],
     [
      -124,
      288,
      0,
      707
     ],
     [
      422,
      661,
      1,
      206
     ],
     [
      434,
      209,
      1,
      313
     ],
     [
      303,
      789,
      0,
      380
     ],
     [
      193,
      653,
      1,
      388
     ],
     [
      231,
      549,
      2,
      323
     ],
     [
      293,
      784,
      0,
      383
     ],
     [
      410,
      200,
      0,
      331
     ],
     [
      297,
      784,
      0,
      380
     ],
     [
      308,
      789,
      0,
      377
     ],
     [
      320,
      696,
      1,
      302
     ],
     [
      -160,
      269,
      0,
      747
     ],
     [
      507,
      348,
      0,
      158
     ],
     [
      379,
      833,
      2,
      374
     ],
     [
      373,
      852,
      2,
      394
     ],
     [
      381,
      837,
      2,
      377
     ],
     [
      486,
      262,
      1,
      246
     ],
     [
      518,
      255,
      2,
      247
     ],
     [
      362,
      908,
      1,
      449
     ],
     [
      153,
      527,
      0,
      398
     ],
     [
      69,
      552,
      0,
      484
     ],
     [
      92,
      552,
      1,
      461
     ],
     [
      50,
      547,
      0,
      502
     ],
     [
      338,
      167,
      1,
      395
     ],
     [
      1245,
      953,
      0,
      830
     ],
     [
      124,
      549,
      1,
      429
     ],
     [
      89,
      470,
      0,
      462
     ],
     [
      527,
      286,
      2,
      215
     ],
     [
      15,
      539,
      0,
      536
     ],
     [
      296,
      93,
      1,
      480
     ],
     [
      890,
      96,
      0,
      528
     ],
     [
      295,
      548,
      2,
      259
     ],
     [
      288,
      548,
      2,
      266
     ],
     [
      274,
      549,
      2,
      280
     ],
     [
      279,
      549,
      2,
      275
     ],
     [
      251,
      550,
      1,
      303
     ],
     [
      485,
      321,
      0,
      190
     ],
     [
      258,
      551,
      1,
      296
     ],
     [
      225,
      548,
      2,
      329
     ],
     [
      454,
      1043,
      0,
      551
     ],
     [
      64,
      463,
      0,
      487
     ]
    ],
    "prioritari": [
     [
      331,
      683
     ],
     [
      219,
      475
     ],
     [
      492,
      1012
     ],
     [
      381,
      374
     ],
     [
      778,
      469
     ],
     [
      47,
      638
     ],
     [
      262,
      891
     ],
     [
      755,
      291
     ],
     [
      725,
      1084
     ],
     [
      615,
      273
     ],
     [
      122,
      811
     ],
     [
      532,
      729
     ]
    ],
    "legenda": [
     {
      "label": "posti bastanti",
      "n": 95,
      "tono": "verde"
     },
     {
      "label": "pochi posti",
      "n": 111,
      "tono": "giallo"
     },
     {
      "label": "nessun parcheggio",
      "n": 68,
      "tono": "rosso"
     }
    ],
    "didascalia": "Ogni punto è una fermata importante, in Torino e in cintura; la linea è il confine di Torino. I cerchi neri sono i 12 punti dove servirebbero di più nuovi posti."
   },
   "pareggio": {
    "tomtom": 16,
    "sensori": 28
   }
  },
  "forma_en": {
   "tipo_dato": "Type of data: calculated from real data and partly measured, over few days of data.",
   "titolo": "2 in 3 important stops lack enough spaces to leave the car",
   "domanda": "Can people driving in from outside find a place to leave the car near an important stop, and continue by public transport?",
   "numero": {
    "valore": 179,
    "unita": "",
    "testo": "important stops out of 274 lack enough parking within 400 metres on foot",
    "breve": "important stops without parking spaces"
   },
   "principale": {
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
   },
   "punti": [
    "68 important stops have no car park nearby, 111 have too few.",
    "The first of the 12 entry points where spaces are needed is Santa Rita: ~450 are missing.",
    "In 8 points out of 12, once the car is left, the bus reaches the centre in at most 1.5 times the car's time."
   ],
   "altri": [
    {
     "tipo": "gara",
     "titolo": "The race: bus and car to Piazza Castello, at 8 a.m. on a weekday",
     "nota": "Bus and car leave together from each car park, one after the other. The car has the time forecast by TomTom, parking included.",
     "luoghi": [
      {
       "nome": "Santa Rita",
       "gruppo": "Priority points",
       "bus": 36.0,
       "auto_min": 26.8,
       "auto_max": 26.8,
       "giudizio": "the bus pays off"
      },
      {
       "nome": "Metro Massaua",
       "gruppo": "Priority points",
       "bus": 25.0,
       "auto_min": 26.9,
       "auto_max": 26.9,
       "giudizio": "the bus pays off"
      },
      {
       "nome": "Ponte Cavalieri Templari",
       "gruppo": "Priority points",
       "bus": 51.0,
       "auto_min": 26.6,
       "auto_max": 26.6,
       "giudizio": "the bus does not pay off"
      },
      {
       "nome": "Regina Margherita",
       "gruppo": "Priority points",
       "bus": 31.0,
       "auto_min": 27.7,
       "auto_max": 27.7,
       "giudizio": "the bus pays off"
      },
      {
       "nome": "Pasini",
       "gruppo": "Priority points",
       "bus": 28.0,
       "auto_min": 20.4,
       "auto_max": 20.4,
       "giudizio": "the bus pays off"
      },
      {
       "nome": "Leonardo Da Vinci",
       "gruppo": "Priority points",
       "bus": 59.0,
       "auto_min": 38.5,
       "auto_max": 38.5,
       "giudizio": "the bus does not pay off"
      },
      {
       "nome": "Drosso Cap",
       "gruppo": "Priority points",
       "bus": 43.0,
       "auto_min": 31.3,
       "auto_max": 31.3,
       "giudizio": "the bus pays off"
      },
      {
       "nome": "Stura Lazio",
       "gruppo": "Priority points",
       "bus": 37.0,
       "auto_min": 26.9,
       "auto_max": 26.9,
       "giudizio": "the bus pays off"
      },
      {
       "nome": "Marsè",
       "gruppo": "Priority points",
       "bus": 61.0,
       "auto_min": 33.5,
       "auto_max": 33.5,
       "giudizio": "the bus does not pay off"
      },
      {
       "nome": "Derna Est",
       "gruppo": "Priority points",
       "bus": 34.0,
       "auto_min": 23.7,
       "auto_max": 23.7,
       "giudizio": "the bus pays off"
      },
      {
       "nome": "Ferrara",
       "gruppo": "Priority points",
       "bus": 49.0,
       "auto_min": 34.8,
       "auto_max": 34.8,
       "giudizio": "the bus pays off"
      },
      {
       "nome": "Zara",
       "gruppo": "Priority points",
       "bus": 33.0,
       "auto_min": 18.8,
       "auto_max": 18.8,
       "giudizio": "the bus does not pay off"
      },
      {
       "nome": "Stura",
       "gruppo": "Existing park-and-ride",
       "bus": 39.0,
       "auto_min": 30.2,
       "auto_max": 30.2,
       "giudizio": "the bus pays off"
      },
      {
       "nome": "Venchi Unica",
       "gruppo": "Existing park-and-ride",
       "bus": 28.0,
       "auto_min": 28.8,
       "auto_max": 28.8,
       "giudizio": "the bus pays off"
      },
      {
       "nome": "Caio Mario",
       "gruppo": "Existing park-and-ride",
       "bus": 38.0,
       "auto_min": 30.1,
       "auto_max": 30.1,
       "giudizio": "the bus pays off"
      },
      {
       "nome": "Fermi",
       "gruppo": "Existing park-and-ride",
       "bus": 31.0,
       "auto_min": 36.6,
       "auto_max": 36.6,
       "giudizio": "the bus pays off"
      },
      {
       "nome": "Sofia",
       "gruppo": "Existing park-and-ride",
       "bus": 33.0,
       "auto_min": 21.8,
       "auto_max": 21.8,
       "giudizio": "the bus does not pay off"
      }
     ],
     "scelto": 0
    },
    {
     "tipo": "barre",
     "titolo": "Existing park-and-ride sites: how full they are and how long the bus takes to the centre",
     "unita": "minutes",
     "nota": "Bar = minutes by public transport to Piazza Castello at 8 a.m. On the right, the car time with parking included (TomTom), and how full the car park is during the day.",
     "voci": [
      {
       "label": "Stura",
       "valore": 39,
       "testo": "39 against 30 by car · full during the day"
      },
      {
       "label": "Venchi Unica",
       "valore": 28,
       "testo": "28 against 29 by car · half full"
      },
      {
       "label": "Caio Mario",
       "valore": 38,
       "testo": "38 against 30 by car · with free spaces"
      },
      {
       "label": "Fermi",
       "valore": 31,
       "testo": "31 against 37 by car · occupancy unknown"
      },
      {
       "label": "Sofia",
       "valore": 33,
       "testo": "33 against 22 by car · with free spaces"
      }
     ]
    }
   ],
   "calcolo": [
    "Important stops: outside the centre, with a metro, station or terminus, or 10 trips an hour.",
    "Cars entering come from the 2022 travel survey, assigned to the fastest route.",
    "Cars to stop: passing cars times the 5.8% who already leave the car today. Spaces: suitable car parks within 400 metres.",
    "Priority points: stops without enough parking, grouped within 1 km, one per entry axis.",
    "Bus versus car: minutes by public transport to Piazza Castello at 8, versus the car. Car: free-flow time times the TomTom factor of the route, plus 5 minutes. Traffic data: TomTom.",
    "Break-even: with 16 minutes lost parking downtown, the car takes as long as the bus (median of the 12 points, TomTom).",
    "Of the points where the bus pays off, 5 out of 8 are close to the threshold: a car 10% faster changes the class.",
    "With the traffic-sensor estimate, more favourable to the car (factor 1.2), the break-even rises to 28 minutes."
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
     "Car park occupancy period",
     "from 15/10/2,026 to 22/10/2,026"
    ],
    [
     "Bus versus car",
     "to Piazza Castello at 8; car: TomTom factor of the route (median 2.6) + 5 minutes; estimate most favourable to the car: 5T sensors, factor 1.2"
    ]
   ],
   "limiti": [
    "Passing cars come from a traffic model. Spaces are often estimated: the missing ones are an order of magnitude. With half or double the drivers who leave the car, stops without enough spaces go from 135 to 212 out of 274.",
    "Public transport times are GTT only, without trains. The sensor estimate ignores traffic lights and junctions: it is the most favourable to the car.",
    "Car times forecast by TomTom for typical traffic on a November weekday, not measured on a specific day. A single service is used.",
    "The cost of parking is not in the calculation: it weighs as extra minutes. One point per place and one destination only."
   ],
   "mappa": {
    "id": "interscambio",
    "nota": "Due domande nella mappa, nel menu «Cosa vedere»: dove ci sono parcheggi e dove servirebbe di più un parcheggio."
   },
   "anima": {
    "tipo": "fermate",
    "contorno": {
     "d": "M879 130l-33 35l-2 -35l22 -12l13 12zM452 11l123 41l18 -10l2 11l11 14l35 -6l42 -20l3 -17l6 -5l25 -3l34 9l-9 37l9 34l48 23l13 3l-8 28l46 93l43 29l-7 39l-27 21l-21 13l28 44l18 20l30 12l64 3l-8 11l3 8l10 6l12 -1l5 4l-90 145l-79 95l-39 49l-51 48l-40 17l-37 36l-129 15l-120 41l-18 59l-73 6l-70 -8l-19 1l-59 -16l-11 5l-87 -31l-14 -16l8 -25l8 -1l36 8l35 -80l-30 11l-67 -45l-44 -39l-10 -14l13 -18l32 -4l128 80l25 -39l45 -134l-1 -15l-33 5l-57 -11l9 -32l9 -4l6 -11l-20 -24l-25 -6l61 -129l13 -59l-19 -21l-12 -51l13 -8l30 2l12 -4l1 -39l122 13l40 -5l0 -15l-7 -11l-3 -50l9 -10l12 -31l-6 -29l2 -15l38 -36l7 -2l8 11z",
     "vb": [
      -297,
      -606,
      1582,
      1730
     ]
    },
    "punti": [
     [
      186,
      477,
      0,
      365
     ],
     [
      216,
      475,
      1,
      335
     ],
     [
      123,
      481,
      1,
      427
     ],
     [
      687,
      138,
      0,
      387
     ],
     [
      261,
      473,
      2,
      290
     ],
     [
      295,
      471,
      2,
      257
     ],
     [
      690,
      150,
      0,
      377
     ],
     [
      692,
      135,
      0,
      392
     ],
     [
      445,
      255,
      1,
      267
     ],
     [
      455,
      252,
      1,
      266
     ],
     [
      442,
      258,
      1,
      265
     ],
     [
      426,
      895,
      1,
      414
     ],
     [
      546,
      301,
      1,
      199
     ],
     [
      479,
      1008,
      0,
      513
     ],
     [
      369,
      154,
      0,
      390
     ],
     [
      342,
      1065,
      0,
      602
     ],
     [
      339,
      1063,
      0,
      601
     ],
     [
      393,
      817,
      0,
      354
     ],
     [
      574,
      300,
      1,
      201
     ],
     [
      576,
      299,
      1,
      203
     ],
     [
      476,
      1024,
      1,
      529
     ],
     [
      69,
      465,
      0,
      482
     ],
     [
      1237,
      976,
      0,
      836
     ],
     [
      401,
      839,
      0,
      370
     ],
     [
      241,
      917,
      1,
      519
     ],
     [
      346,
      682,
      2,
      273
     ],
     [
      257,
      746,
      2,
      383
     ],
     [
      680,
      145,
      0,
      378
     ],
     [
      356,
      671,
      2,
      259
     ],
     [
      268,
      738,
      1,
      369
     ],
     [
      175,
      791,
      1,
      475
     ],
     [
      221,
      475,
      1,
      330
     ],
     [
      290,
      854,
      1,
      439
     ],
     [
      136,
      480,
      1,
      414
     ],
     [
      185,
      787,
      2,
      464
     ],
     [
      259,
      896,
      1,
      491
     ],
     [
      245,
      754,
      1,
      397
     ],
     [
      264,
      887,
      2,
      481
     ],
     [
      279,
      871,
      2,
      459
     ],
     [
      248,
      754,
      1,
      395
     ],
     [
      592,
      599,
      2,
      108
     ],
     [
      270,
      882,
      2,
      474
     ],
     [
      204,
      782,
      2,
      446
     ],
     [
      253,
      900,
      1,
      498
     ],
     [
      200,
      782,
      2,
      449
     ],
     [
      236,
      762,
      1,
      409
     ],
     [
      240,
      648,
      1,
      344
     ],
     [
      727,
      514,
      1,
      178
     ],
     [
      299,
      840,
      1,
      423
     ],
     [
      233,
      762,
      1,
      411
     ],
     [
      743,
      510,
      1,
      193
     ],
     [
      325,
      699,
      1,
      300
     ],
     [
      311,
      828,
      1,
      406
     ],
     [
      269,
      652,
      1,
      319
     ],
     [
      375,
      748,
      0,
      304
     ],
     [
      337,
      685,
      2,
      282
     ],
     [
      10,
      488,
      1,
      540
     ],
     [
      784,
      403,
      1,
      253
     ],
     [
      390,
      729,
      0,
      279
     ],
     [
      345,
      687,
      2,
      277
     ],
     [
      334,
      799,
      0,
      369
     ],
     [
      313,
      825,
      0,
      402
     ],
     [
      353,
      776,
      1,
      339
     ],
     [
      331,
      804,
      0,
      375
     ],
     [
      293,
      721,
      1,
      339
     ],
     [
      706,
      332,
      0,
      229
     ],
     [
      1049,
      -566,
      0,
      1177
     ],
     [
      349,
      780,
      1,
      345
     ],
     [
      207,
      476,
      0,
      344
     ],
     [
      47,
      638,
      2,
      522
     ],
     [
      414,
      698,
      1,
      240
     ],
     [
      320,
      816,
      0,
      391
     ],
     [
      779,
      426,
      1,
      241
     ],
     [
      273,
      876,
      2,
      467
     ],
     [
      794,
      390,
      1,
      268
     ],
     [
      159,
      480,
      1,
      392
     ],
     [
      156,
      478,
      1,
      395
     ],
     [
      -57,
      492,
      2,
      607
     ],
     [
      260,
      901,
      1,
      495
     ],
     [
      647,
      229,
      2,
      288
     ],
     [
      672,
      177,
      1,
      345
     ],
     [
      632,
      261,
      0,
      253
     ],
     [
      663,
      197,
      0,
      323
     ],
     [
      223,
      647,
      1,
      359
     ],
     [
      256,
      650,
      1,
      330
     ],
     [
      268,
      650,
      1,
      319
     ],
     [
      399,
      717,
      2,
      264
     ],
     [
      856,
      357,
      1,
      338
     ],
     [
      507,
      999,
      1,
      501
     ],
     [
      722,
      316,
      0,
      252
     ],
     [
      674,
      534,
      2,
      129
     ],
     [
      95,
      482,
      1,
      455
     ],
     [
      553,
      300,
      1,
      200
     ],
     [
      432,
      675,
      2,
      211
     ],
     [
      607,
      268,
      0,
      239
     ],
     [
      324,
      812,
      0,
      385
     ],
     [
      393,
      348,
      2,
      219
     ],
     [
      380,
      377,
      2,
      210
     ],
     [
      936,
      265,
      0,
      452
     ],
     [
      429,
      679,
      2,
      216
     ],
     [
      778,
      469,
      2,
      230
     ],
     [
      532,
      729,
      1,
      230
     ],
     [
      315,
      828,
      1,
      403
     ],
     [
      927,
      309,
      1,
      423
     ],
     [
      516,
      367,
      1,
      137
     ],
     [
      -23,
      490,
      1,
      573
     ],
     [
      367,
      758,
      0,
      316
     ],
     [
      -19,
      489,
      1,
      569
     ],
     [
      620,
      561,
      1,
      93
     ],
     [
      404,
      716,
      2,
      261
     ],
     [
      510,
      359,
      1,
      147
     ],
     [
      294,
      841,
      1,
      426
     ],
     [
      365,
      760,
      0,
      319
     ],
     [
      287,
      718,
      1,
      342
     ],
     [
      750,
      286,
      2,
      293
     ],
     [
      292,
      602,
      2,
      277
     ],
     [
      284,
      660,
      1,
      310
     ],
     [
      333,
      473,
      1,
      219
     ],
     [
      307,
      515,
      1,
      243
     ],
     [
      337,
      464,
      1,
      216
     ],
     [
      281,
      656,
      1,
      311
     ],
     [
      402,
      713,
      2,
      259
     ],
     [
      -175,
      500,
      0,
      725
     ],
     [
      296,
      666,
      1,
      303
     ],
     [
      766,
      244,
      0,
      335
     ],
     [
      711,
      333,
      0,
      232
     ],
     [
      623,
      282,
      0,
      230
     ],
     [
      303,
      824,
      1,
      407
     ],
     [
      621,
      286,
      0,
      225
     ],
     [
      630,
      276,
      1,
      238
     ],
     [
      700,
      342,
      0,
      218
     ],
     [
      600,
      330,
      1,
      177
     ],
     [
      324,
      679,
      2,
      288
     ],
     [
      -178,
      498,
      0,
      728
     ],
     [
      -150,
      496,
      0,
      700
     ],
     [
      289,
      679,
      2,
      316
     ],
     [
      283,
      501,
      2,
      267
     ],
     [
      513,
      356,
      0,
      149
     ],
     [
      99,
      818,
      0,
      552
     ],
     [
      111,
      814,
      0,
      540
     ],
     [
      288,
      700,
      1,
      330
     ],
     [
      482,
      999,
      0,
      504
     ],
     [
      591,
      352,
      1,
      154
     ],
     [
      -257,
      504,
      0,
      807
     ],
     [
      103,
      818,
      0,
      549
     ],
     [
      122,
      811,
      2,
      529
     ],
     [
      444,
      252,
      1,
      270
     ],
     [
      555,
      262,
      2,
      238
     ],
     [
      -95,
      495,
      1,
      645
     ],
     [
      725,
      1084,
      2,
      610
     ],
     [
      588,
      358,
      2,
      147
     ],
     [
      533,
      260,
      2,
      241
     ],
     [
      428,
      266,
      1,
      264
     ],
     [
      688,
      357,
      0,
      199
     ],
     [
      422,
      290,
      2,
      246
     ],
     [
      284,
      56,
      0,
      518
     ],
     [
      312,
      806,
      0,
      388
     ],
     [
      411,
      310,
      2,
      235
     ],
     [
      539,
      366,
      0,
      134
     ],
     [
      -99,
      493,
      1,
      649
     ],
     [
      421,
      287,
      2,
      249
     ],
     [
      718,
      322,
      0,
      245
     ],
     [
      431,
      264,
      1,
      264
     ],
     [
      381,
      668,
      0,
      238
     ],
     [
      691,
      355,
      0,
      202
     ],
     [
      493,
      994,
      0,
      497
     ],
     [
      315,
      803,
      0,
      383
     ],
     [
      530,
      262,
      2,
      239
     ],
     [
      371,
      396,
      2,
      207
     ],
     [
      313,
      674,
      2,
      294
     ],
     [
      434,
      249,
      1,
      277
     ],
     [
      51,
      460,
      0,
      501
     ],
     [
      311,
      671,
      2,
      294
     ],
     [
      299,
      665,
      1,
      300
     ],
     [
      -221,
      501,
      0,
      771
     ],
     [
      302,
      546,
      2,
      252
     ],
     [
      -196,
      499,
      0,
      746
     ],
     [
      609,
      312,
      1,
      197
     ],
     [
      984,
      257,
      0,
      497
     ],
     [
      290,
      632,
      1,
      292
     ],
     [
      709,
      325,
      0,
      236
     ],
     [
      748,
      294,
      2,
      286
     ],
     [
      -224,
      503,
      0,
      774
     ],
     [
      788,
      288,
      2,
      319
     ],
     [
      813,
      284,
      2,
      340
     ],
     [
      360,
      719,
      0,
      290
     ],
     [
      575,
      378,
      1,
      125
     ],
     [
      619,
      304,
      0,
      208
     ],
     [
      598,
      335,
      1,
      172
     ],
     [
      611,
      307,
      1,
      202
     ],
     [
      1029,
      199,
      0,
      566
     ],
     [
      593,
      391,
      1,
      117
     ],
     [
      436,
      261,
      1,
      265
     ],
     [
      310,
      510,
      1,
      240
     ],
     [
      580,
      375,
      1,
      129
     ],
     [
      345,
      249,
      0,
      324
     ],
     [
      -151,
      501,
      0,
      701
     ],
     [
      576,
      384,
      2,
      119
     ],
     [
      265,
      645,
      1,
      320
     ],
     [
      287,
      774,
      0,
      380
     ],
     [
      766,
      291,
      2,
      301
     ],
     [
      600,
      270,
      2,
      235
     ],
     [
      293,
      571,
      2,
      267
     ],
     [
      614,
      410,
      0,
      110
     ],
     [
      651,
      387,
      0,
      152
     ],
     [
      428,
      675,
      1,
      213
     ],
     [
      296,
      566,
      2,
      262
     ],
     [
      677,
      370,
      1,
      182
     ],
     [
      247,
      761,
      1,
      400
     ],
     [
      667,
      377,
      1,
      170
     ],
     [
      266,
      628,
      2,
      312
     ],
     [
      626,
      435,
      1,
      100
     ],
     [
      423,
      214,
      1,
      313
     ],
     [
      442,
      891,
      1,
      406
     ],
     [
      412,
      205,
      0,
      326
     ],
     [
      522,
      365,
      0,
      138
     ],
     [
      391,
      714,
      1,
      267
     ],
     [
      411,
      953,
      0,
      474
     ],
     [
      562,
      371,
      0,
      130
     ],
     [
      442,
      692,
      0,
      220
     ],
     [
      -41,
      324,
      0,
      617
     ],
     [
      -16,
      321,
      1,
      594
     ],
     [
      387,
      177,
      2,
      362
     ],
     [
      374,
      946,
      0,
      479
     ],
     [
      423,
      230,
      2,
      298
     ],
     [
      234,
      551,
      2,
      320
     ],
     [
      403,
      980,
      1,
      502
     ],
     [
      419,
      201,
      0,
      326
     ],
     [
      353,
      1052,
      0,
      586
     ],
     [
      263,
      687,
      1,
      343
     ],
     [
      425,
      901,
      1,
      420
     ],
     [
      423,
      903,
      1,
      423
     ],
     [
      -93,
      327,
      0,
      666
     ],
     [
      -124,
      288,
      0,
      707
     ],
     [
      422,
      661,
      1,
      206
     ],
     [
      434,
      209,
      1,
      313
     ],
     [
      303,
      789,
      0,
      380
     ],
     [
      193,
      653,
      1,
      388
     ],
     [
      231,
      549,
      2,
      323
     ],
     [
      293,
      784,
      0,
      383
     ],
     [
      410,
      200,
      0,
      331
     ],
     [
      297,
      784,
      0,
      380
     ],
     [
      308,
      789,
      0,
      377
     ],
     [
      320,
      696,
      1,
      302
     ],
     [
      -160,
      269,
      0,
      747
     ],
     [
      507,
      348,
      0,
      158
     ],
     [
      379,
      833,
      2,
      374
     ],
     [
      373,
      852,
      2,
      394
     ],
     [
      381,
      837,
      2,
      377
     ],
     [
      486,
      262,
      1,
      246
     ],
     [
      518,
      255,
      2,
      247
     ],
     [
      362,
      908,
      1,
      449
     ],
     [
      153,
      527,
      0,
      398
     ],
     [
      69,
      552,
      0,
      484
     ],
     [
      92,
      552,
      1,
      461
     ],
     [
      50,
      547,
      0,
      502
     ],
     [
      338,
      167,
      1,
      395
     ],
     [
      1245,
      953,
      0,
      830
     ],
     [
      124,
      549,
      1,
      429
     ],
     [
      89,
      470,
      0,
      462
     ],
     [
      527,
      286,
      2,
      215
     ],
     [
      15,
      539,
      0,
      536
     ],
     [
      296,
      93,
      1,
      480
     ],
     [
      890,
      96,
      0,
      528
     ],
     [
      295,
      548,
      2,
      259
     ],
     [
      288,
      548,
      2,
      266
     ],
     [
      274,
      549,
      2,
      280
     ],
     [
      279,
      549,
      2,
      275
     ],
     [
      251,
      550,
      1,
      303
     ],
     [
      485,
      321,
      0,
      190
     ],
     [
      258,
      551,
      1,
      296
     ],
     [
      225,
      548,
      2,
      329
     ],
     [
      454,
      1043,
      0,
      551
     ],
     [
      64,
      463,
      0,
      487
     ]
    ],
    "prioritari": [
     [
      331,
      683
     ],
     [
      219,
      475
     ],
     [
      492,
      1012
     ],
     [
      381,
      374
     ],
     [
      778,
      469
     ],
     [
      47,
      638
     ],
     [
      262,
      891
     ],
     [
      755,
      291
     ],
     [
      725,
      1084
     ],
     [
      615,
      273
     ],
     [
      122,
      811
     ],
     [
      532,
      729
     ]
    ],
    "legenda": [
     {
      "label": "enough spaces",
      "n": 95,
      "tono": "verde"
     },
     {
      "label": "few spaces",
      "n": 111,
      "tono": "giallo"
     },
     {
      "label": "no car park",
      "n": 68,
      "tono": "rosso"
     }
    ],
    "didascalia": "Each dot is an important stop, in Turin and the surrounding towns; the line is the city boundary. The black circles are the 12 points where new spaces are most needed."
   },
   "pareggio": {
    "tomtom": 16,
    "sensori": 28
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
   "valore": 95.6,
   "unita": "%",
   "testo": "dei km di strade grandi di Torino hanno fermate frequenti a pochi passi (356,3 km su 372,7)"
  },
  "racconto": "Un primo calcolo trovava 23 strade \"con molto traffico e poco trasporto pubblico\". Ricontrollando, quasi tutte erano un errore di misura: i bus si cercavano lungo la strada per nome invece che per posizione delle fermate (Corso Cairoli risultava senza passaggi). Rifatto il calcolo, la lista si è quasi svuotata: è questa la risposta.",
  "risposta": [
   "Sulle 611 tratte di strade grandi di Torino (372,7 km), il 95,6% della lunghezza ha una fermata con almeno 4 passaggi all'ora entro 300 m, o la metro entro 600 m.",
   "Le tratte con molto traffico (oltre 10.677 veicoli al giorno) sono 204; quelle che hanno anche poco trasporto pubblico sono 5.",
   "In pratica è un solo caso: Corso Regina Margherita verso ovest, il tratto a scorrimento veloce (circa 32.000 veicoli al giorno, nessuna fermata frequente entro 300 m). In più un tratto di Casale, coperto solo per 25% della lunghezza.",
   "I numeri di traffico sono stime: in metà dei casi l'errore è entro ±28%. Servono a ordinare le strade, non a contare i veicoli."
  ],
  "grafici": [
   {
    "tipo": "pila",
    "titolo": "Km di strade grandi di Torino: con o senza trasporto pubblico vicino",
    "unita": "km",
    "voci": [
     {
      "label": "con fermate frequenti vicine",
      "valore": 356.3,
      "tono": "verde"
     },
     {
      "label": "con poco trasporto pubblico",
      "valore": 16.4,
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
      "label": "Unità d'Italia",
      "valore": 52296
     },
     {
      "label": "Orbassano (misurato)",
      "valore": 50322
     },
     {
      "label": "Regina Margherita",
      "valore": 48739
     },
     {
      "label": "Unione Sovietica",
      "valore": 48567
     },
     {
      "label": "Francia",
      "valore": 39243
     },
     {
      "label": "Giulio Cesare",
      "valore": 37396
     },
     {
      "label": "Giovanni Agnelli",
      "valore": 34034
     },
     {
      "label": "Asse di Penetrazione Urbana di Corso Regina Margherita",
      "valore": 31205
     },
     {
      "label": "Strada di Settimo (misurato)",
      "valore": 29926
     },
     {
      "label": "Quattro Novembre",
      "valore": 25977
     }
    ]
   },
   {
    "tipo": "barre",
    "titolo": "Prova del modello sui 22 sensori: misurato e stimato",
    "unita": "veicoli/giorno",
    "nota": "Barra chiara = misurato dal sensore, barra scura = stima del modello senza usare quel sensore.",
    "voci": [
     {
      "label": "Corso Unità d'Italia",
      "valore": 54449,
      "prima": 81956
     },
     {
      "label": "Corso Trieste",
      "valore": 49617,
      "prima": 65424
     },
     {
      "label": "Corso Orbassano",
      "valore": 49916,
      "prima": 50322
     },
     {
      "label": "Corso Unità d'Italia",
      "valore": 48344,
      "prima": 47616
     },
     {
      "label": "Corso Orbassano",
      "valore": 46751,
      "prima": 41326
     },
     {
      "label": "R24 Raccordo Torino-Aeroporto Caselle",
      "valore": 27103,
      "prima": 39810
     },
     {
      "label": "Corso Giulio Cesare",
      "valore": 24579,
      "prima": 34548
     },
     {
      "label": "Corso Francia",
      "valore": 38311,
      "prima": 30938
     },
     {
      "label": "Ponte Amedeo VIII",
      "valore": 26625,
      "prima": 29926
     },
     {
      "label": "Corso Giulio Cesare",
      "valore": 36474,
      "prima": 29270
     },
     {
      "label": "Corso Francia",
      "valore": 39197,
      "prima": 28414
     },
     {
      "label": "Corso Regina Margherita",
      "valore": 30585,
      "prima": 28412
     },
     {
      "label": "Corso Orbassano",
      "valore": 44057,
      "prima": 27024
     },
     {
      "label": "Corso Vercelli",
      "valore": 9941,
      "prima": 25470
     },
     {
      "label": "Corso Agnelli",
      "valore": 31592,
      "prima": 22014
     },
     {
      "label": "SP8 di Druento",
      "valore": 10514,
      "prima": 20611
     },
     {
      "label": "Corso Regina Margherita",
      "valore": 25497,
      "prima": 19954
     },
     {
      "label": "Corso Unione Sovietica",
      "valore": 53830,
      "prima": 19202
     },
     {
      "label": "Corso Sebastopoli",
      "valore": 28273,
      "prima": 17424
     },
     {
      "label": "Strada Di Settimo",
      "valore": 12280,
      "prima": 16856
     },
     {
      "label": "SP1 delle Valli di Lanzo",
      "valore": 6438,
      "prima": 15097
     },
     {
      "label": "Corso Allamano",
      "valore": 11620,
      "prima": 12820
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
      "valore": 1,
      "tono": "rosso"
     },
     {
      "label": "Corso Unità d'Italia",
      "valore": 2,
      "tono": "rosso"
     },
     {
      "label": "Corso Regina Margherita",
      "valore": 8,
      "tono": "rosso"
     },
     {
      "label": "Corso Allamano",
      "valore": 9,
      "tono": "rosso"
     },
     {
      "label": "Ponte Amedeo VIII",
      "valore": 11,
      "tono": "rosso"
     },
     {
      "label": "Corso Orbassano",
      "valore": 13,
      "tono": "rosso"
     },
     {
      "label": "Corso Francia",
      "valore": 24,
      "tono": "rosso"
     },
     {
      "label": "Corso Trieste",
      "valore": 24,
      "tono": "rosso"
     },
     {
      "label": "Corso Giulio Cesare",
      "valore": 25,
      "tono": "rosso"
     },
     {
      "label": "Strada Di Settimo",
      "valore": 27,
      "tono": "rosso"
     },
     {
      "label": "Corso Regina Margherita",
      "valore": 28,
      "tono": "rosso"
     },
     {
      "label": "Corso Giulio Cesare",
      "valore": 29,
      "tono": "rosso"
     },
     {
      "label": "R24 Raccordo Torino-Aeroporto Caselle",
      "valore": 32,
      "tono": "rosso"
     },
     {
      "label": "Corso Unità d'Italia",
      "valore": 34,
      "tono": "rosso"
     },
     {
      "label": "Corso Francia",
      "valore": 38,
      "tono": "rosso"
     },
     {
      "label": "Corso Agnelli",
      "valore": 44,
      "tono": "rosso"
     },
     {
      "label": "SP8 di Druento",
      "valore": 49,
      "tono": "rosso"
     },
     {
      "label": "SP1 delle Valli di Lanzo",
      "valore": 57,
      "tono": "rosso"
     },
     {
      "label": "Corso Vercelli",
      "valore": 61,
      "tono": "rosso"
     },
     {
      "label": "Corso Sebastopoli",
      "valore": 62,
      "tono": "rosso"
     },
     {
      "label": "Corso Orbassano",
      "valore": 63,
      "tono": "rosso"
     },
     {
      "label": "Corso Unione Sovietica",
      "valore": 180,
      "tono": "rosso"
     }
    ]
   }
  ],
  "metodo": [
   "Domanda: gli spostamenti in auto dell'indagine sugli spostamenti 2022 (residenti, giorno feriale), assegnati alla strada più veloce sulla rete di OpenStreetMap.",
   "Taratura su 22 punti di misura dei sensori 5T: un solo fattore per tutta la città, provato togliendo un sensore alla volta e stimandolo con gli altri.",
   "Strade come assi: un corso che cambia nome o comune resta la stessa strada, tagliata in tratte da 300 m a 1,5 km. Strade grandi = Torino, importanza alta o strade principali, almeno 300 m, senza tangenziale e raccordi.",
   "Trasporto pubblico per posizione delle fermate, mai per nome: una tratta è servita dove c'è una fermata con almeno 4 passaggi all'ora entro 300 m (orario ufficiale, mercoledì 14/10), o la metro entro 600 m. Poco trasporto pubblico = servita per metà della lunghezza o meno.",
   "Molto traffico = il terzo più alto delle tratte. Il modello è quello più ricco (attrazioni, code, ZTL): con i sensori di ottobre sbaglia meno di quello semplice (errore tipico 28% contro 38%), secondo una regola fissata prima."
  ],
  "parametri": [
   [
    "Strade grandi di Torino",
    "611 tratte, 372,7 km"
   ],
   [
    "Errore tipico (metà dei casi)",
    "±28% (9 volte su 10 entro ±62%)"
   ],
   [
    "Ordine giusto delle strade (Spearman)",
    "0,64"
   ],
   [
    "Validato tra",
    "9.000 e 107.000 veicoli/giorno"
   ],
   [
    "Soglia 'molto traffico'",
    "10.677 veicoli/giorno"
   ],
   [
    "Confronto con chi conosce la città",
    "11 strade su 18 nella fascia giusta, 5 confronti su 7 (solo controllo)"
   ]
  ],
  "limiti": [
   "Stima debole: errore tipico ±28% e intervallo d'incertezza largo (da 24% a 38%). Alcune strade sono molto sbagliate (Corso Unione Sovietica, Corso Sebastopoli): buona per ordinare, non per contare.",
   "Solo 22 punti di misura, quasi tutti su corsi trafficati: sotto circa 9.000 veicoli al giorno la stima non è verificata.",
   "Solo i residenti tra 11 e 84 anni (indagine sugli spostamenti): mancano merci, turisti e chi viene da fuori. Il modello non sa fare le code: l'ora di punta non è verificata.",
   "Trasporto pubblico programmato: niente ritardi né affollamento. Il centro (ZTL, aree pedonali) non è stimato bene.",
   "Il valore è per i due versi: sulle poche vie a senso unico vero potrebbe essere il doppio del reale.",
   "Il tratto di Corso Moncalieri va controllato a mano: una fermata con 26 passaggi all'ora è a 40 m, ma copre solo un quarto della tratta."
  ],
  "in_english": [
   "Question: on Turin's major roads, where is there a lot of traffic and little public transport nearby?",
   "Of 611 road sections on Turin's major roads (372.7 km), 95.6% of the length has a frequent stop (at least 4 departures an hour) within 300 m, or the metro within 600 m. Heavy-traffic sections (over 10,677 vehicles a day): 204; of these, 5 also have little public transport.",
   "In practice this is one main case: Corso Regina Margherita westbound, a fast road with no frequent stop within 300 m, plus one stretch of Corso Moncalieri covered for only a quarter of its length.",
   "Limits: traffic figures are estimates with a typical error of ±28%; use them to rank the roads, not to count vehicles."
  ],
  "mappa": {
   "id": "imq",
   "tema": "Spostamenti",
   "nota": "Nella mappa, tema «Spostamenti»: quanti spostamenti partono da ogni zona e dove vanno (indagine 2022, feriale)."
  },
  "fonti": [
   "docs/R8_traffico.md",
   "docs/rapporti/RAPPORTO_RISULTATO8_TRAFFICO_TP_V2.txt",
   "data/processed/risultato8_traffico_tp_v2.json"
  ],
  "generato": "2026-10-24T00:36:03+00:00",
  "avviso": [
   "Dati [STIMATO] (traffico) / [MISURATO] (sensori 5T) / [PROGRAMMATO] (orari GTT)",
   "Traffico stimato con un modello tarato su 22 sensori: errore tipico ±28%. Trasporto pubblico = fermate con almeno 4 passaggi all'ora entro 300 m o metro entro 600 m."
  ],
  "scenari": [
   {
    "nome": "Oggi",
    "numeri": [
     {
      "label": "Km di strade grandi di Torino",
      "prima": null,
      "dopo": 372.7,
      "unita": "km"
     },
     {
      "label": "Con fermate frequenti vicine",
      "prima": null,
      "dopo": 95.6,
      "unita": "%"
     },
     {
      "label": "Tratte con molto traffico",
      "prima": null,
      "dopo": 204,
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
      "dopo": 28,
      "unita": "%"
     }
    ],
    "nota": "Le 5 tratte sono quasi tutte su Corso Regina Margherita ovest; una su Corso Moncalieri."
   }
  ],
  "forma": {
   "tipo_dato": "Tipo di dato: calcolato da dati veri, con tempi in auto di TomTom, misure dei sensori e orari ufficiali dei mezzi.",
   "titolo": "Al mattino, coi mezzi pubblici si impiega 1,9 volte il tempo dell'auto",
   "domanda": "Al mattino, quanto ci si mette in più coi mezzi pubblici che in auto?",
   "numero": {
    "valore": "1,9",
    "unita": "volte",
    "testo": "il tempo dell'auto, per un viaggio tipico del mattino",
    "breve": "il tempo dell'auto, coi mezzi pubblici"
   },
   "principale": {
    "tipo": "barre",
    "titolo": "Auto del mattino, per quante volte i mezzi pubblici impiegano più dell'auto",
    "unita": "%",
    "max": 100,
    "nota": "Ogni barra è una fascia: coi mezzi pubblici si impiega quel multiplo del tempo in auto (TomTom). Coppie Torino-Torino e Torino-cintura.",
    "voci": [
     {
      "label": "meno di 1,5 volte",
      "valore": 13,
      "tono": "verde",
      "testo": "13% (28.510 auto)"
     },
     {
      "label": "da 1,5 a 2 volte",
      "valore": 52,
      "tono": "giallo",
      "testo": "52% (113.791 auto)"
     },
     {
      "label": "da 2 a 3 volte",
      "valore": 33,
      "tono": "arancio",
      "testo": "33% (73.728 auto)"
     },
     {
      "label": "oltre 3 volte",
      "valore": 2,
      "tono": "rosso",
      "testo": "2% (4.278 auto)"
     }
    ]
   },
   "punti": [
    "Per il ~35% delle auto del mattino i mezzi pubblici impiegano più del doppio.",
    "Nelle 4 ore del giorno il tempo coi mezzi va da 1,9 a 2,3 volte quello dell'auto.",
    "Un tragitto frequente tipico: Barriera di Milano → Falchera, ~24 minuti coi mezzi contro ~12 in auto."
   ],
   "altri": [
    {
     "tipo": "linea",
     "titolo": "Quante volte il tempo dell'auto, ora per ora",
     "unita": "volte",
     "nota": "Rapporto fra il tempo coi mezzi e il tempo in auto (TomTom), pesato per le auto del mattino, alle 4 ore del giorno.",
     "categorie": [
      "8:00",
      "13:00",
      "17:30",
      "21:00"
     ],
     "serie": [
      {
       "label": "rapporto",
       "valori": [
        1.9,
        2.1,
        1.9,
        2.3
       ]
      }
     ]
    },
    {
     "tipo": "gara",
     "titolo": "I viaggi in auto più frequenti del mattino: bus contro auto",
     "luoghi": [
      {
       "nome": "Crocetta",
       "arrivo": "Centro",
       "bus": 20.6,
       "auto_min": 15.8,
       "auto_max": 15.8,
       "giudizio": "coi mezzi 1,3 volte il tempo dell'auto"
      },
      {
       "nome": "San Paolo",
       "arrivo": "Centro",
       "bus": 31.3,
       "auto_min": 16.2,
       "auto_max": 16.2,
       "giudizio": "coi mezzi 1,9 volte il tempo dell'auto"
      },
      {
       "nome": "Mirafiori Nord",
       "arrivo": "Santa Rita",
       "bus": 19.2,
       "auto_min": 15.4,
       "auto_max": 15.4,
       "giudizio": "coi mezzi 1,2 volte il tempo dell'auto"
      },
      {
       "nome": "Parella",
       "arrivo": "Centro",
       "bus": 24.7,
       "auto_min": 16.0,
       "auto_max": 16.0,
       "giudizio": "coi mezzi 1,5 volte il tempo dell'auto"
      },
      {
       "nome": "San Donato",
       "arrivo": "Centro",
       "bus": 18.7,
       "auto_min": 12.2,
       "auto_max": 12.2,
       "giudizio": "coi mezzi 1,5 volte il tempo dell'auto"
      },
      {
       "nome": "Barriera di Milano",
       "arrivo": "Falchera",
       "bus": 24.0,
       "auto_min": 11.7,
       "auto_max": 11.7,
       "giudizio": "coi mezzi 2 volte il tempo dell'auto"
      }
     ],
     "scelto": 0,
     "nota": "Bus e auto partono insieme, uno dopo l'altro, per i 6 viaggi in auto più frequenti del mattino. L'auto ha il tempo previsto da TomTom, parcheggio compreso."
    },
    {
     "tipo": "dispersione",
     "titolo": "Tempo in auto e tempo coi mezzi pubblici, una coppia di zone per punto",
     "xlabel": "minuti in auto (mattino, TomTom)",
     "ylabel": "minuti coi mezzi pubblici",
     "punti": [
      [
       15.8,
       20.6,
       1355.3
      ],
      [
       16.2,
       31.3,
       1341.8
      ],
      [
       15.4,
       19.2,
       1324.4
      ],
      [
       16.0,
       24.7,
       1277.0
      ],
      [
       12.2,
       18.7,
       1269.4
      ],
      [
       11.7,
       24.0,
       1208.2
      ],
      [
       26.4,
       43.0,
       1149.2
      ],
      [
       21.6,
       37.5,
       1107.8
      ],
      [
       47.1,
       80.1,
       1081.8
      ],
      [
       9.1,
       15.2,
       1038.1
      ],
      [
       19.8,
       33.2,
       969.9
      ],
      [
       19.7,
       30.6,
       968.1
      ],
      [
       8.7,
       15.2,
       957.2
      ],
      [
       33.8,
       44.5,
       940.7
      ],
      [
       14.1,
       20.2,
       938.8
      ],
      [
       12.6,
       33.5,
       928.7
      ],
      [
       25.0,
       38.2,
       916.7
      ],
      [
       37.0,
       63.4,
       910.0
      ],
      [
       22.5,
       30.4,
       900.6
      ],
      [
       19.5,
       35.2,
       894.4
      ],
      [
       11.4,
       22.4,
       893.3
      ],
      [
       10.0,
       23.8,
       889.9
      ],
      [
       24.4,
       39.3,
       888.0
      ],
      [
       19.1,
       27.5,
       818.9
      ],
      [
       25.6,
       42.3,
       796.7
      ],
      [
       20.2,
       35.2,
       795.1
      ],
      [
       14.4,
       18.9,
       789.0
      ],
      [
       27.8,
       31.2,
       779.1
      ],
      [
       15.1,
       30.4,
       762.5
      ],
      [
       34.0,
       50.0,
       753.4
      ],
      [
       18.3,
       31.2,
       751.2
      ],
      [
       15.9,
       24.3,
       737.2
      ],
      [
       23.7,
       81.4,
       718.7
      ],
      [
       8.0,
       18.1,
       714.6
      ],
      [
       13.8,
       35.2,
       714.1
      ],
      [
       15.9,
       24.0,
       706.6
      ],
      [
       41.7,
       63.5,
       702.1
      ],
      [
       14.8,
       22.6,
       698.0
      ],
      [
       22.9,
       29.7,
       696.9
      ],
      [
       34.9,
       50.3,
       690.4
      ],
      [
       33.6,
       72.7,
       687.3
      ],
      [
       15.3,
       23.2,
       685.0
      ],
      [
       24.5,
       25.5,
       672.4
      ],
      [
       19.8,
       29.2,
       671.0
      ],
      [
       15.9,
       22.8,
       666.8
      ],
      [
       37.4,
       72.4,
       659.4
      ],
      [
       24.2,
       51.0,
       644.0
      ],
      [
       21.4,
       32.7,
       627.3
      ],
      [
       8.7,
       16.0,
       622.4
      ],
      [
       14.4,
       22.2,
       620.3
      ],
      [
       16.4,
       27.2,
       615.4
      ],
      [
       16.4,
       37.0,
       614.3
      ],
      [
       17.6,
       34.5,
       614.1
      ],
      [
       14.6,
       23.4,
       607.7
      ],
      [
       15.4,
       27.2,
       606.6
      ],
      [
       22.7,
       34.0,
       601.6
      ],
      [
       17.6,
       30.4,
       592.7
      ],
      [
       19.6,
       36.0,
       589.8
      ],
      [
       15.8,
       34.1,
       582.5
      ],
      [
       24.6,
       50.2,
       580.1
      ],
      [
       17.1,
       24.1,
       574.5
      ],
      [
       17.1,
       29.9,
       570.6
      ],
      [
       25.2,
       55.1,
       568.2
      ],
      [
       16.4,
       24.6,
       562.6
      ],
      [
       32.0,
       85.7,
       543.7
      ],
      [
       16.6,
       24.1,
       543.0
      ],
      [
       20.5,
       39.2,
       540.9
      ],
      [
       15.8,
       21.6,
       540.3
      ],
      [
       14.6,
       30.9,
       539.8
      ],
      [
       19.5,
       30.7,
       527.7
      ],
      [
       37.0,
       68.8,
       520.3
      ],
      [
       35.6,
       71.6,
       519.9
      ],
      [
       15.1,
       29.4,
       519.7
      ],
      [
       14.9,
       24.9,
       517.1
      ],
      [
       33.7,
       56.9,
       515.6
      ],
      [
       36.0,
       71.2,
       514.3
      ],
      [
       19.8,
       39.6,
       512.4
      ],
      [
       35.6,
       62.2,
       504.1
      ],
      [
       17.1,
       26.9,
       503.9
      ],
      [
       20.0,
       32.7,
       498.7
      ],
      [
       15.5,
       28.9,
       496.3
      ],
      [
       9.4,
       15.5,
       494.3
      ],
      [
       21.1,
       47.1,
       490.1
      ],
      [
       21.3,
       38.7,
       489.2
      ],
      [
       13.9,
       23.2,
       488.9
      ],
      [
       40.9,
       74.0,
       488.2
      ],
      [
       13.4,
       22.0,
       481.0
      ],
      [
       23.0,
       38.2,
       478.8
      ],
      [
       21.7,
       54.9,
       478.7
      ],
      [
       26.4,
       47.5,
       476.8
      ],
      [
       25.1,
       45.8,
       467.9
      ],
      [
       15.0,
       26.2,
       466.7
      ],
      [
       23.2,
       27.7,
       462.0
      ],
      [
       14.9,
       26.3,
       459.7
      ],
      [
       50.0,
       77.7,
       458.7
      ],
      [
       26.0,
       26.0,
       458.5
      ],
      [
       19.4,
       37.2,
       456.6
      ],
      [
       14.0,
       22.8,
       456.0
      ],
      [
       33.3,
       57.1,
       454.7
      ],
      [
       10.3,
       20.3,
       452.9
      ],
      [
       28.9,
       54.0,
       452.3
      ],
      [
       45.2,
       85.9,
       449.8
      ],
      [
       15.8,
       31.6,
       448.6
      ],
      [
       40.8,
       92.7,
       448.4
      ],
      [
       34.4,
       71.8,
       445.5
      ],
      [
       22.8,
       35.8,
       443.8
      ],
      [
       27.2,
       46.5,
       442.8
      ],
      [
       22.5,
       40.2,
       439.9
      ],
      [
       29.2,
       55.3,
       438.4
      ],
      [
       13.9,
       21.4,
       437.5
      ],
      [
       33.7,
       61.8,
       431.9
      ],
      [
       25.5,
       58.3,
       431.8
      ],
      [
       18.1,
       32.3,
       431.4
      ],
      [
       33.2,
       68.6,
       428.4
      ],
      [
       22.0,
       37.4,
       428.4
      ],
      [
       34.3,
       81.3,
       426.2
      ],
      [
       17.7,
       35.8,
       423.2
      ],
      [
       22.8,
       41.3,
       422.6
      ],
      [
       11.7,
       18.2,
       421.9
      ],
      [
       25.9,
       47.6,
       421.1
      ],
      [
       15.7,
       19.0,
       419.2
      ],
      [
       30.8,
       53.4,
       411.0
      ],
      [
       42.7,
       73.5,
       410.3
      ],
      [
       20.1,
       53.8,
       410.0
      ],
      [
       29.9,
       32.7,
       409.6
      ],
      [
       23.5,
       53.5,
       409.5
      ],
      [
       32.7,
       51.2,
       404.3
      ],
      [
       33.6,
       46.1,
       403.5
      ],
      [
       36.1,
       54.5,
       402.7
      ],
      [
       34.2,
       61.2,
       399.0
      ],
      [
       13.8,
       24.9,
       398.4
      ],
      [
       31.3,
       64.3,
       396.9
      ],
      [
       14.5,
       28.4,
       396.9
      ],
      [
       27.5,
       59.6,
       395.5
      ],
      [
       17.9,
       32.4,
       391.8
      ],
      [
       35.6,
       51.1,
       389.9
      ],
      [
       21.3,
       46.5,
       389.6
      ],
      [
       41.5,
       103.8,
       386.9
      ],
      [
       17.5,
       28.0,
       386.6
      ],
      [
       16.6,
       28.2,
       384.3
      ],
      [
       18.1,
       27.5,
       383.2
      ],
      [
       23.0,
       81.4,
       383.2
      ],
      [
       30.3,
       62.3,
       382.4
      ],
      [
       26.8,
       56.5,
       382.0
      ],
      [
       26.2,
       54.1,
       379.4
      ],
      [
       20.5,
       38.4,
       377.6
      ],
      [
       12.6,
       31.4,
       377.4
      ],
      [
       18.0,
       24.3,
       376.5
      ],
      [
       18.2,
       36.7,
       369.2
      ],
      [
       21.5,
       30.6,
       368.7
      ],
      [
       20.2,
       37.1,
       367.3
      ],
      [
       18.9,
       43.4,
       366.6
      ],
      [
       28.6,
       79.1,
       365.7
      ],
      [
       20.7,
       19.3,
       365.5
      ],
      [
       27.3,
       74.5,
       363.3
      ],
      [
       17.2,
       28.2,
       362.7
      ],
      [
       15.2,
       20.9,
       356.4
      ],
      [
       15.7,
       21.4,
       355.0
      ],
      [
       23.8,
       39.1,
       353.0
      ],
      [
       24.5,
       52.3,
       352.5
      ],
      [
       11.1,
       17.1,
       352.1
      ],
      [
       27.7,
       50.6,
       350.1
      ],
      [
       15.2,
       37.0,
       348.3
      ],
      [
       24.8,
       44.8,
       347.8
      ],
      [
       40.4,
       71.4,
       346.3
      ],
      [
       29.9,
       71.2,
       346.1
      ],
      [
       20.7,
       63.5,
       345.7
      ],
      [
       25.3,
       32.0,
       340.6
      ],
      [
       13.4,
       41.8,
       340.0
      ],
      [
       27.5,
       50.6,
       339.6
      ],
      [
       41.6,
       83.0,
       338.3
      ],
      [
       24.2,
       45.7,
       336.5
      ],
      [
       27.5,
       54.3,
       336.5
      ],
      [
       40.2,
       79.4,
       335.5
      ],
      [
       23.9,
       52.0,
       335.0
      ],
      [
       30.3,
       60.6,
       333.8
      ],
      [
       32.0,
       87.7,
       333.6
      ],
      [
       40.4,
       74.5,
       333.5
      ],
      [
       18.1,
       31.4,
       332.2
      ],
      [
       37.0,
       82.7,
       331.5
      ],
      [
       32.9,
       47.6,
       331.5
      ],
      [
       24.5,
       64.4,
       330.5
      ],
      [
       27.5,
       52.4,
       329.9
      ],
      [
       35.1,
       43.5,
       329.1
      ],
      [
       43.6,
       65.5,
       328.2
      ],
      [
       28.1,
       54.2,
       328.0
      ],
      [
       26.0,
       54.2,
       326.5
      ],
      [
       37.6,
       67.1,
       323.5
      ],
      [
       14.5,
       24.0,
       322.3
      ],
      [
       12.0,
       19.2,
       322.1
      ],
      [
       39.6,
       64.3,
       321.4
      ],
      [
       20.8,
       34.1,
       318.2
      ],
      [
       25.8,
       47.8,
       317.7
      ],
      [
       32.7,
       80.6,
       311.9
      ],
      [
       34.9,
       94.0,
       310.7
      ],
      [
       16.4,
       26.4,
       309.9
      ],
      [
       29.0,
       60.2,
       307.1
      ],
      [
       34.6,
       69.8,
       306.3
      ],
      [
       12.1,
       25.1,
       305.1
      ],
      [
       14.6,
       35.8,
       304.4
      ],
      [
       23.1,
       53.0,
       304.2
      ],
      [
       28.6,
       52.3,
       303.6
      ],
      [
       40.9,
       62.6,
       303.4
      ],
      [
       36.9,
       77.0,
       302.8
      ],
      [
       40.7,
       68.8,
       302.3
      ],
      [
       38.5,
       72.2,
       300.8
      ],
      [
       18.9,
       19.0,
       299.5
      ],
      [
       27.3,
       48.9,
       299.2
      ],
      [
       32.1,
       56.4,
       298.9
      ],
      [
       24.6,
       47.2,
       298.6
      ],
      [
       27.4,
       54.3,
       297.1
      ],
      [
       22.6,
       54.1,
       296.5
      ],
      [
       34.2,
       57.7,
       296.0
      ],
      [
       41.1,
       86.8,
       295.0
      ],
      [
       42.3,
       70.0,
       294.0
      ],
      [
       18.1,
       33.8,
       292.7
      ],
      [
       43.5,
       85.7,
       291.8
      ],
      [
       21.4,
       46.0,
       290.8
      ],
      [
       13.6,
       21.3,
       290.5
      ],
      [
       34.5,
       60.2,
       289.4
      ],
      [
       30.0,
       52.7,
       288.9
      ],
      [
       40.2,
       74.6,
       288.6
      ],
      [
       20.2,
       35.0,
       284.7
      ],
      [
       21.5,
       38.6,
       283.1
      ],
      [
       11.4,
       18.9,
       282.6
      ],
      [
       24.2,
       42.7,
       282.2
      ],
      [
       23.4,
       42.2,
       281.8
      ],
      [
       19.5,
       38.3,
       281.7
      ],
      [
       23.4,
       57.4,
       280.3
      ],
      [
       24.7,
       56.7,
       278.1
      ],
      [
       17.4,
       24.5,
       274.9
      ],
      [
       36.9,
       83.0,
       274.4
      ],
      [
       33.1,
       68.0,
       273.4
      ],
      [
       18.1,
       34.6,
       273.2
      ],
      [
       34.9,
       46.0,
       272.4
      ],
      [
       45.6,
       76.5,
       271.8
      ],
      [
       39.1,
       79.0,
       271.3
      ],
      [
       24.8,
       61.4,
       271.0
      ],
      [
       17.4,
       31.8,
       270.6
      ],
      [
       12.7,
       24.6,
       270.2
      ],
      [
       24.7,
       44.1,
       270.1
      ],
      [
       37.1,
       98.2,
       269.7
      ],
      [
       23.9,
       62.1,
       269.7
      ],
      [
       37.9,
       83.6,
       268.9
      ],
      [
       12.6,
       17.1,
       268.5
      ],
      [
       26.5,
       55.2,
       267.8
      ],
      [
       26.2,
       37.0,
       264.3
      ],
      [
       30.2,
       60.4,
       263.3
      ],
      [
       24.7,
       51.4,
       262.3
      ],
      [
       24.7,
       42.2,
       261.5
      ],
      [
       27.5,
       49.4,
       261.2
      ],
      [
       16.5,
       34.8,
       260.2
      ],
      [
       8.6,
       17.5,
       259.7
      ],
      [
       14.7,
       29.1,
       258.2
      ],
      [
       46.1,
       79.4,
       257.3
      ],
      [
       26.8,
       46.5,
       256.8
      ],
      [
       32.1,
       75.8,
       255.1
      ],
      [
       44.6,
       78.2,
       254.4
      ],
      [
       46.1,
       103.2,
       253.6
      ],
      [
       49.8,
       89.0,
       253.1
      ],
      [
       14.3,
       15.8,
       252.2
      ],
      [
       28.3,
       49.4,
       251.6
      ],
      [
       21.5,
       29.9,
       251.5
      ],
      [
       26.4,
       56.6,
       250.1
      ],
      [
       26.2,
       37.3,
       248.3
      ],
      [
       31.8,
       48.8,
       247.4
      ],
      [
       17.8,
       34.8,
       244.8
      ],
      [
       16.7,
       28.9,
       243.9
      ],
      [
       26.6,
       44.1,
       243.6
      ],
      [
       27.1,
       55.0,
       243.6
      ],
      [
       20.2,
       29.2,
       243.6
      ],
      [
       25.1,
       41.8,
       243.0
      ],
      [
       31.5,
       77.9,
       242.3
      ],
      [
       30.3,
       43.4,
       242.2
      ],
      [
       32.2,
       61.5,
       241.4
      ],
      [
       19.1,
       30.4,
       241.0
      ],
      [
       34.4,
       91.5,
       240.6
      ],
      [
       19.6,
       39.4,
       240.0
      ],
      [
       32.0,
       65.0,
       238.3
      ],
      [
       35.5,
       72.1,
       236.1
      ],
      [
       17.2,
       24.2,
       235.8
      ],
      [
       23.2,
       46.3,
       234.9
      ],
      [
       27.3,
       52.5,
       234.7
      ],
      [
       28.2,
       46.3,
       234.6
      ],
      [
       25.5,
       46.7,
       233.6
      ],
      [
       27.8,
       67.6,
       233.3
      ],
      [
       19.9,
       43.3,
       231.7
      ],
      [
       29.4,
       61.4,
       231.5
      ],
      [
       52.7,
       99.5,
       230.9
      ],
      [
       29.6,
       48.0,
       228.8
      ],
      [
       13.9,
       25.4,
       228.3
      ],
      [
       23.2,
       41.6,
       228.1
      ],
      [
       22.2,
       62.8,
       227.0
      ],
      [
       27.2,
       79.2,
       226.3
      ],
      [
       24.3,
       36.1,
       225.6
      ],
      [
       31.2,
       59.0,
       225.4
      ],
      [
       26.8,
       52.0,
       225.1
      ],
      [
       30.7,
       64.8,
       224.1
      ],
      [
       14.9,
       24.1,
       223.2
      ],
      [
       39.9,
       94.3,
       222.3
      ],
      [
       16.1,
       32.1,
       222.1
      ],
      [
       41.2,
       70.7,
       221.0
      ],
      [
       12.5,
       25.9,
       220.4
      ],
      [
       18.8,
       24.2,
       219.8
      ],
      [
       14.9,
       22.4,
       218.7
      ],
      [
       33.9,
       52.8,
       218.3
      ],
      [
       26.7,
       75.5,
       217.8
      ],
      [
       40.9,
       68.5,
       217.1
      ],
      [
       17.4,
       30.8,
       216.9
      ],
      [
       33.4,
       104.0,
       216.3
      ],
      [
       36.2,
       61.0,
       215.9
      ],
      [
       27.1,
       71.9,
       215.8
      ],
      [
       47.2,
       96.9,
       215.6
      ],
      [
       21.8,
       53.9,
       215.3
      ],
      [
       37.1,
       67.0,
       214.1
      ],
      [
       26.8,
       51.6,
       214.0
      ],
      [
       18.3,
       26.0,
       213.2
      ],
      [
       33.3,
       72.4,
       212.7
      ],
      [
       42.8,
       78.5,
       212.0
      ],
      [
       32.4,
       93.1,
       211.8
      ],
      [
       38.9,
       63.9,
       211.3
      ],
      [
       22.7,
       50.2,
       211.2
      ],
      [
       27.0,
       61.1,
       210.7
      ],
      [
       24.4,
       57.8,
       209.8
      ],
      [
       20.9,
       43.2,
       209.0
      ],
      [
       25.7,
       51.2,
       208.2
      ],
      [
       45.2,
       102.7,
       208.1
      ],
      [
       31.4,
       61.3,
       207.6
      ],
      [
       42.5,
       86.5,
       207.5
      ],
      [
       16.6,
       30.0,
       206.7
      ],
      [
       43.7,
       82.2,
       206.4
      ],
      [
       22.1,
       44.2,
       206.2
      ],
      [
       27.1,
       50.9,
       206.2
      ],
      [
       26.4,
       44.3,
       206.1
      ],
      [
       35.9,
       66.5,
       206.0
      ],
      [
       20.7,
       55.3,
       205.9
      ],
      [
       34.4,
       96.3,
       205.6
      ],
      [
       35.6,
       56.6,
       205.0
      ],
      [
       21.6,
       41.6,
       204.7
      ],
      [
       28.6,
       75.6,
       204.3
      ],
      [
       36.8,
       56.6,
       204.3
      ],
      [
       42.0,
       78.0,
       204.0
      ],
      [
       43.4,
       77.3,
       203.9
      ],
      [
       31.4,
       57.1,
       203.8
      ],
      [
       23.9,
       91.5,
       203.7
      ],
      [
       21.9,
       43.6,
       203.5
      ],
      [
       23.4,
       42.6,
       203.4
      ],
      [
       47.2,
       74.0,
       203.4
      ],
      [
       27.7,
       46.8,
       203.2
      ],
      [
       47.6,
       84.4,
       202.3
      ],
      [
       29.8,
       67.5,
       201.9
      ],
      [
       37.2,
       58.4,
       201.7
      ],
      [
       29.8,
       54.3,
       201.5
      ],
      [
       21.9,
       26.2,
       201.5
      ],
      [
       22.3,
       27.0,
       201.2
      ],
      [
       17.8,
       42.8,
       200.7
      ],
      [
       27.7,
       61.8,
       200.5
      ],
      [
       37.5,
       82.2,
       200.3
      ],
      [
       25.9,
       85.6,
       199.7
      ],
      [
       15.7,
       27.0,
       199.4
      ],
      [
       14.3,
       30.9,
       199.3
      ],
      [
       28.6,
       55.4,
       198.8
      ],
      [
       38.3,
       56.4,
       197.7
      ],
      [
       33.1,
       77.4,
       197.7
      ],
      [
       31.3,
       48.8,
       196.4
      ],
      [
       41.6,
       69.6,
       195.7
      ],
      [
       32.2,
       67.0,
       195.6
      ],
      [
       18.9,
       33.0,
       195.3
      ],
      [
       15.7,
       42.0,
       194.7
      ],
      [
       17.4,
       26.4,
       194.6
      ],
      [
       37.1,
       76.1,
       194.1
      ],
      [
       19.7,
       34.1,
       193.8
      ],
      [
       36.8,
       100.1,
       193.0
      ],
      [
       26.1,
       45.7,
       192.7
      ],
      [
       50.2,
       98.6,
       192.4
      ],
      [
       19.7,
       32.5,
       192.2
      ],
      [
       37.5,
       81.0,
       191.6
      ],
      [
       24.3,
       41.7,
       191.5
      ],
      [
       32.3,
       58.7,
       190.6
      ],
      [
       37.5,
       88.2,
       190.5
      ],
      [
       23.3,
       61.8,
       190.5
      ],
      [
       29.1,
       78.3,
       190.5
      ],
      [
       33.2,
       84.6,
       190.2
      ],
      [
       18.2,
       33.7,
       190.2
      ],
      [
       34.2,
       57.8,
       189.6
      ],
      [
       21.1,
       42.1,
       189.4
      ],
      [
       40.9,
       108.3,
       188.8
      ],
      [
       30.0,
       52.8,
       188.6
      ],
      [
       26.4,
       44.8,
       188.5
      ],
      [
       44.1,
       84.5,
       187.6
      ],
      [
       50.6,
       86.5,
       187.3
      ],
      [
       35.0,
       63.9,
       186.9
      ],
      [
       33.6,
       57.4,
       186.9
      ],
      [
       29.2,
       64.1,
       186.9
      ],
      [
       20.9,
       37.8,
       186.8
      ],
      [
       36.5,
       74.2,
       186.4
      ],
      [
       51.1,
       97.4,
       186.4
      ],
      [
       50.5,
       84.8,
       186.2
      ],
      [
       43.9,
       81.6,
       185.9
      ],
      [
       29.6,
       40.7,
       185.7
      ],
      [
       26.8,
       45.0,
       185.5
      ],
      [
       14.7,
       39.8,
       185.4
      ],
      [
       22.0,
       31.4,
       185.1
      ],
      [
       28.7,
       54.9,
       184.5
      ],
      [
       44.6,
       92.0,
       184.1
      ],
      [
       54.5,
       85.6,
       183.3
      ],
      [
       44.4,
       87.8,
       183.3
      ],
      [
       16.2,
       29.6,
       183.2
      ],
      [
       39.8,
       83.0,
       183.0
      ],
      [
       36.0,
       68.7,
       182.4
      ],
      [
       35.0,
       66.2,
       182.4
      ],
      [
       43.9,
       90.8,
       181.8
      ],
      [
       45.1,
       77.4,
       181.2
      ],
      [
       26.2,
       64.3,
       181.2
      ],
      [
       35.2,
       69.0,
       181.1
      ],
      [
       27.6,
       57.4,
       180.8
      ],
      [
       20.2,
       65.9,
       179.9
      ],
      [
       31.0,
       48.9,
       179.7
      ],
      [
       25.5,
       35.5,
       179.6
      ],
      [
       37.7,
       92.6,
       179.5
      ],
      [
       20.3,
       59.6,
       179.5
      ],
      [
       24.9,
       46.4,
       179.5
      ],
      [
       38.4,
       91.4,
       179.2
      ],
      [
       22.7,
       54.4,
       178.4
      ],
      [
       33.2,
       64.8,
       177.9
      ],
      [
       32.5,
       61.2,
       177.9
      ],
      [
       27.7,
       47.4,
       177.4
      ],
      [
       34.8,
       51.0,
       177.3
      ],
      [
       31.6,
       112.9,
       177.0
      ],
      [
       14.1,
       29.5,
       176.7
      ],
      [
       50.3,
       94.5,
       176.2
      ],
      [
       36.7,
       88.2,
       176.0
      ],
      [
       14.2,
       21.1,
       175.3
      ],
      [
       25.5,
       44.9,
       175.0
      ],
      [
       19.5,
       57.0,
       174.5
      ],
      [
       14.8,
       26.6,
       173.9
      ],
      [
       16.3,
       31.4,
       173.6
      ],
      [
       33.5,
       69.0,
       173.5
      ],
      [
       28.5,
       60.7,
       173.4
      ],
      [
       32.5,
       56.0,
       173.2
      ],
      [
       24.1,
       26.6,
       173.1
      ],
      [
       38.7,
       63.1,
       173.1
      ],
      [
       35.9,
       54.3,
       173.0
      ],
      [
       26.7,
       67.0,
       173.0
      ],
      [
       14.3,
       40.7,
       173.0
      ],
      [
       49.9,
       99.5,
       173.0
      ],
      [
       24.3,
       42.6,
       172.3
      ],
      [
       36.8,
       93.0,
       172.0
      ],
      [
       45.6,
       62.5,
       171.6
      ],
      [
       41.0,
       113.8,
       171.3
      ],
      [
       45.8,
       89.9,
       171.3
      ],
      [
       41.2,
       77.7,
       171.2
      ],
      [
       16.7,
       24.7,
       171.0
      ],
      [
       53.8,
       99.0,
       170.7
      ],
      [
       18.9,
       46.9,
       170.0
      ],
      [
       23.8,
       50.3,
       169.8
      ],
      [
       16.6,
       40.7,
       169.6
      ],
      [
       22.8,
       77.5,
       169.4
      ],
      [
       19.5,
       33.8,
       169.2
      ],
      [
       27.1,
       93.1,
       168.9
      ],
      [
       22.3,
       35.8,
       168.6
      ],
      [
       40.1,
       68.6,
       168.1
      ],
      [
       25.3,
       86.0,
       168.1
      ],
      [
       15.3,
       18.2,
       167.9
      ],
      [
       18.5,
       33.7,
       167.5
      ],
      [
       33.5,
       62.8,
       167.2
      ],
      [
       45.6,
       87.9,
       166.7
      ],
      [
       37.4,
       73.5,
       166.7
      ],
      [
       26.8,
       35.6,
       166.1
      ],
      [
       49.7,
       92.3,
       165.5
      ],
      [
       42.2,
       112.0,
       165.4
      ],
      [
       32.3,
       98.0,
       165.4
      ],
      [
       19.0,
       33.8,
       164.6
      ],
      [
       14.1,
       33.0,
       163.9
      ],
      [
       20.2,
       46.1,
       163.8
      ],
      [
       12.3,
       23.3,
       163.6
      ],
      [
       30.9,
       72.8,
       163.5
      ],
      [
       25.1,
       50.7,
       163.3
      ],
      [
       35.3,
       69.8,
       163.0
      ],
      [
       34.0,
       78.5,
       162.2
      ],
      [
       28.6,
       68.0,
       161.5
      ],
      [
       25.5,
       64.2,
       161.5
      ],
      [
       29.5,
       71.0,
       161.5
      ],
      [
       22.2,
       54.7,
       161.4
      ],
      [
       37.1,
       87.0,
       160.9
      ],
      [
       31.4,
       55.1,
       160.0
      ],
      [
       30.9,
       39.7,
       159.7
      ],
      [
       21.7,
       53.4,
       159.5
      ],
      [
       30.2,
       51.4,
       159.4
      ],
      [
       29.4,
       72.3,
       159.3
      ],
      [
       34.8,
       53.0,
       158.2
      ],
      [
       36.6,
       82.8,
       158.2
      ],
      [
       41.7,
       57.2,
       157.9
      ],
      [
       17.1,
       33.0,
       157.8
      ],
      [
       31.8,
       70.6,
       157.5
      ],
      [
       26.5,
       45.2,
       157.3
      ],
      [
       18.2,
       30.2,
       157.3
      ],
      [
       44.8,
       95.0,
       156.5
      ],
      [
       31.9,
       41.1,
       155.8
      ],
      [
       33.7,
       74.4,
       155.6
      ],
      [
       27.1,
       50.9,
       155.4
      ],
      [
       38.1,
       54.8,
       155.2
      ],
      [
       29.8,
       92.7,
       155.1
      ],
      [
       28.6,
       83.6,
       154.9
      ],
      [
       28.9,
       37.8,
       154.5
      ],
      [
       42.7,
       90.2,
       154.5
      ],
      [
       37.3,
       64.6,
       154.1
      ],
      [
       21.6,
       44.6,
       153.6
      ],
      [
       31.0,
       51.8,
       152.4
      ],
      [
       17.0,
       26.6,
       152.3
      ],
      [
       20.0,
       53.8,
       152.3
      ],
      [
       38.8,
       90.8,
       151.5
      ],
      [
       25.9,
       59.0,
       151.3
      ],
      [
       30.1,
       67.8,
       151.2
      ],
      [
       26.7,
       60.4,
       150.6
      ],
      [
       30.1,
       46.1,
       150.2
      ],
      [
       21.8,
       40.1,
       149.8
      ],
      [
       30.4,
       48.5,
       148.6
      ],
      [
       41.2,
       66.8,
       148.5
      ],
      [
       18.1,
       31.5,
       148.2
      ],
      [
       32.2,
       63.6,
       147.4
      ],
      [
       20.4,
       34.0,
       147.2
      ],
      [
       25.8,
       48.2,
       146.3
      ],
      [
       24.6,
       28.6,
       146.1
      ],
      [
       12.7,
       30.9,
       145.2
      ],
      [
       24.8,
       49.4,
       145.0
      ],
      [
       34.7,
       88.6,
       144.6
      ],
      [
       31.0,
       50.1,
       143.8
      ],
      [
       31.3,
       52.5,
       143.2
      ],
      [
       43.9,
       100.8,
       142.8
      ],
      [
       17.4,
       34.2,
       142.2
      ],
      [
       27.8,
       57.7,
       142.1
      ],
      [
       29.4,
       51.0,
       142.1
      ],
      [
       23.0,
       37.6,
       141.5
      ],
      [
       24.4,
       45.2,
       141.1
      ],
      [
       30.1,
       44.0,
       140.8
      ],
      [
       31.1,
       71.0,
       140.6
      ],
      [
       23.2,
       35.3,
       140.1
      ],
      [
       44.8,
       87.5,
       139.1
      ],
      [
       32.8,
       63.6,
       139.1
      ],
      [
       29.7,
       51.9,
       136.6
      ],
      [
       25.5,
       50.3,
       136.6
      ],
      [
       37.8,
       99.4,
       135.8
      ],
      [
       42.8,
       69.8,
       135.1
      ],
      [
       39.8,
       111.8,
       132.9
      ],
      [
       28.3,
       86.0,
       132.9
      ],
      [
       30.6,
       60.8,
       131.1
      ],
      [
       27.7,
       59.3,
       130.6
      ],
      [
       15.2,
       56.8,
       130.3
      ],
      [
       19.9,
       46.1,
       129.1
      ],
      [
       26.0,
       92.4,
       128.8
      ],
      [
       22.5,
       62.7,
       128.8
      ],
      [
       24.0,
       27.2,
       125.9
      ],
      [
       32.8,
       67.2,
       125.8
      ],
      [
       49.0,
       81.4,
       125.8
      ],
      [
       30.5,
       112.6,
       124.6
      ],
      [
       40.7,
       67.6,
       122.4
      ],
      [
       57.6,
       104.8,
       122.4
      ],
      [
       33.9,
       61.3,
       122.0
      ],
      [
       37.8,
       61.1,
       121.7
      ],
      [
       29.0,
       54.6,
       120.0
      ],
      [
       31.9,
       57.8,
       119.6
      ],
      [
       43.5,
       94.6,
       118.8
      ],
      [
       37.3,
       52.6,
       118.8
      ],
      [
       37.3,
       98.0,
       118.6
      ],
      [
       16.2,
       36.6,
       117.9
      ],
      [
       52.1,
       99.4,
       117.8
      ],
      [
       27.3,
       54.6,
       115.5
      ],
      [
       36.9,
       72.6,
       115.5
      ],
      [
       29.3,
       61.6,
       115.5
      ],
      [
       15.0,
       38.8,
       115.5
      ],
      [
       17.8,
       39.2,
       115.5
      ],
      [
       28.4,
       58.2,
       114.2
      ],
      [
       27.5,
       66.4,
       113.9
      ],
      [
       28.8,
       39.5,
       113.4
      ],
      [
       31.4,
       69.0,
       113.4
      ],
      [
       37.3,
       64.6,
       113.4
      ],
      [
       27.4,
       56.5,
       113.4
      ],
      [
       37.0,
       64.4,
       113.4
      ],
      [
       20.6,
       43.1,
       113.4
      ],
      [
       20.2,
       40.0,
       112.0
      ],
      [
       25.5,
       75.6,
       112.0
      ],
      [
       38.7,
       98.4,
       112.0
      ],
      [
       44.5,
       96.2,
       112.0
      ],
      [
       30.3,
       39.3,
       112.0
      ],
      [
       34.7,
       98.4,
       112.0
      ],
      [
       17.5,
       41.0,
       112.0
      ],
      [
       47.5,
       101.9,
       112.0
      ],
      [
       25.0,
       33.4,
       112.0
      ],
      [
       24.6,
       33.8,
       112.0
      ],
      [
       23.1,
       62.0,
       111.0
      ],
      [
       21.5,
       39.8,
       111.0
      ],
      [
       24.3,
       55.8,
       110.8
      ],
      [
       40.3,
       78.2,
       110.3
      ],
      [
       30.0,
       63.8,
       110.3
      ],
      [
       25.9,
       63.4,
       110.1
      ],
      [
       24.4,
       46.2,
       109.2
      ],
      [
       36.6,
       93.8,
       109.2
      ],
      [
       17.5,
       30.2,
       109.2
      ],
      [
       13.6,
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
     "nota": "Ogni punto è una coppia di zone, grande quanto le auto del mattino; sopra una linea i mezzi pubblici impiegano più di quel multiplo del tempo in auto."
    },
    {
     "tipo": "barre",
     "titolo": "I tragitti dove coi mezzi pubblici si impiega più del doppio dell'auto",
     "unita": "auto",
     "nota": "Ogni barra è il numero di auto del mattino su quel tragitto. A destra i minuti coi mezzi contro quelli in auto.",
     "voci": [
      {
       "label": "Barriera di Milano → Falchera",
       "valore": 1208,
       "tono": "rosso",
       "testo": "24 contro 12 min · 1.208 auto"
      },
      {
       "label": "Pozzo Strada → Grugliasco",
       "valore": 929,
       "tono": "rosso",
       "testo": "34 contro 13 min · 929 auto"
      },
      {
       "label": "Falchera → Barriera di Milano",
       "valore": 890,
       "tono": "rosso",
       "testo": "24 contro 10 min · 890 auto"
      },
      {
       "label": "Parella → San Paolo",
       "valore": 763,
       "tono": "rosso",
       "testo": "30 contro 15 min · 763 auto"
      },
      {
       "label": "Parella → Cenisia",
       "valore": 715,
       "tono": "rosso",
       "testo": "18 contro 8 min · 715 auto"
      },
      {
       "label": "Grugliasco → Pozzo Strada",
       "valore": 714,
       "tono": "rosso",
       "testo": "35 contro 14 min · 714 auto"
      },
      {
       "label": "Mirafiori Nord → Grugliasco",
       "valore": 583,
       "tono": "rosso",
       "testo": "34 contro 16 min · 583 auto"
      },
      {
       "label": "Parella → Madonna di Campagna",
       "valore": 540,
       "tono": "rosso",
       "testo": "31 contro 15 min · 540 auto"
      },
      {
       "label": "Vanchiglia → Madonna Del Pilone",
       "valore": 369,
       "tono": "rosso",
       "testo": "37 contro 18 min · 369 auto"
      },
      {
       "label": "Grugliasco → Mirafiori Nord",
       "valore": 348,
       "tono": "rosso",
       "testo": "37 contro 15 min · 348 auto"
      },
      {
       "label": "Cenisia → Parella",
       "valore": 260,
       "tono": "rosso",
       "testo": "18 contro 9 min · 260 auto"
      },
      {
       "label": "Borgata Vittoria → Aurora",
       "valore": 177,
       "tono": "rosso",
       "testo": "30 contro 14 min · 177 auto"
      }
     ]
    }
   ],
   "calcolo": [
    "Le zone sono quelle dell'indagine sugli spostamenti 2022 con punti di calcolo; ognuna ha fino a 5 punti.",
    "Mezzi pubblici: a piedi, bus, tram e metro, con partenza fra le 7:45 e le 8:15. Si prende la mediana.",
    "Auto: tempo a flusso libero per il fattore TomTom della coppia, più 5 minuti. Le coppie non chieste a TomTom prendono la mediana della loro fascia. Dati di traffico: TomTom.",
    "Con i sensori del traffico la stima è più favorevole all'auto: fattore 1,2, senza semafori e incroci. Il rapporto mediano diventa 2,9 e il 97% delle auto ha rapporto oltre 2.",
    "Rapporto = tempo coi mezzi diviso tempo in auto, in fasce fisse. Le auto di una coppia sono i viaggi in auto dell'indagine, dalle 6 alle 10 di un feriale.",
    "Il numero grande vale per il 47% delle auto del mattino (220.307). Mancano i viaggi dentro una zona e fra comuni della cintura.",
    "Su percorsi noti Google conferma i tempi coi mezzi: 31 contro 30-35 e 33 contro 30-35 minuti.",
    "Il grafico a punti mostra le 600 coppie con più auto (83,2% delle auto). L'elenco dei tragitti usa solo coppie con almeno 30 interviste."
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
     "Auto, stima TomTom",
     "tempo a flusso libero × fattore TomTom della coppia (mediana 2,2) + 5 minuti"
    ],
    [
     "Auto, stima più favorevole all'auto",
     "tempo a flusso libero × 1,2 (sensori 5T, non contano semafori e incroci) + 5 minuti"
    ],
    [
     "Periodo dei sensori",
     "dal 09/10/2026 al 22/10/2026"
    ],
    [
     "Fasce del rapporto",
     "sotto 1,5, 1,5-2, 2-3, oltre 3"
    ]
   ],
   "limiti": [
    "Fuori Torino mancano treni e altre aziende: le coppie fra comuni della cintura non sono nel numero. Senza i treni metropolitani, dove ci sono, i mezzi pubblici risultano più lenti del vero. L'orario è quello programmato.",
    "La stima dei sensori non conta semafori e incroci: è la più favorevole all'auto.",
    "Tempi in auto previsti da TomTom su traffico tipico di un feriale di novembre, non misurati in un giorno preciso. Si usa un solo servizio.",
    "L'indagine è un campione. I viaggi dentro una zona e 653 coppie senza collegamento (5.616 auto) non sono nel confronto."
   ],
   "mappa": {
    "id": "imq",
    "nota": "Nella mappa, tema «Spostamenti»: quanti spostamenti partono da ogni zona e dove vanno (indagine 2022, feriale)."
   },
   "chiave": {
    "valore": "1,9",
    "unita": "volte",
    "testo": "il tempo dell'auto coi mezzi pubblici, al mattino"
   },
   "anima": {
    "tipo": "area",
    "didascalia": "Da Piazza Castello, alle 7:45 di un feriale. In 30 minuti si raggiungono ~42% dei torinesi coi mezzi pubblici e ~90% in auto (TomTom, parcheggio compreso)."
   }
  },
  "forma_en": {
   "tipo_dato": "Type of data: calculated from real data, with car times from TomTom, sensor measurements and the official timetables of the vehicles.",
   "titolo": "In the morning, public transport takes 1.9 times as long as the car",
   "domanda": "In the morning, how much longer does it take by public transport than by car?",
   "numero": {
    "valore": "1.9",
    "unita": "times",
    "testo": "the car's travel time, for a typical morning trip",
    "breve": "the car's time, by public transport"
   },
   "principale": {
    "tipo": "barre",
    "titolo": "Morning cars, by how many times public transport takes longer than the car",
    "unita": "%",
    "max": 100,
    "nota": "Each bar is a band: public transport takes that multiple of the car's travel time (TomTom). Turin-Turin and Turin-belt pairs.",
    "voci": [
     {
      "label": "less than 1.5 times",
      "valore": 13,
      "tono": "verde",
      "testo": "13% (28,510 cars)"
     },
     {
      "label": "1.5 to 2 times",
      "valore": 52,
      "tono": "giallo",
      "testo": "52% (113,791 cars)"
     },
     {
      "label": "2 to 3 times",
      "valore": 33,
      "tono": "arancio",
      "testo": "33% (73,728 cars)"
     },
     {
      "label": "more than 3 times",
      "valore": 2,
      "tono": "rosso",
      "testo": "2% (4,278 cars)"
     }
    ]
   },
   "punti": [
    "For ~35% of morning cars, public transport takes more than twice as long.",
    "Across the 4 times of the day, public transport time goes from 1.9 to 2.3 times the car's.",
    "A typical frequent trip: Barriera di Milano → Falchera, ~24 minutes by public transport against ~12 by car."
   ],
   "altri": [
    {
     "tipo": "linea",
     "titolo": "How many times the car time, hour by hour",
     "unita": "times",
     "nota": "Ratio between public transport time and car time (TomTom), weighted by morning cars, at 4 times of the day.",
     "categorie": [
      "8:00",
      "13:00",
      "17:30",
      "21:00"
     ],
     "serie": [
      {
       "label": "ratio",
       "valori": [
        1.9,
        2.1,
        1.9,
        2.3
       ]
      }
     ]
    },
    {
     "tipo": "gara",
     "titolo": "The most frequent morning car trips: bus versus car",
     "luoghi": [
      {
       "nome": "Crocetta",
       "arrivo": "Centro",
       "bus": 20.6,
       "auto_min": 15.8,
       "auto_max": 15.8,
       "giudizio": "by public transport 1.3 times the car's time"
      },
      {
       "nome": "San Paolo",
       "arrivo": "Centro",
       "bus": 31.3,
       "auto_min": 16.2,
       "auto_max": 16.2,
       "giudizio": "by public transport 1.9 times the car's time"
      },
      {
       "nome": "Mirafiori Nord",
       "arrivo": "Santa Rita",
       "bus": 19.2,
       "auto_min": 15.4,
       "auto_max": 15.4,
       "giudizio": "by public transport 1.2 times the car's time"
      },
      {
       "nome": "Parella",
       "arrivo": "Centro",
       "bus": 24.7,
       "auto_min": 16.0,
       "auto_max": 16.0,
       "giudizio": "by public transport 1.5 times the car's time"
      },
      {
       "nome": "San Donato",
       "arrivo": "Centro",
       "bus": 18.7,
       "auto_min": 12.2,
       "auto_max": 12.2,
       "giudizio": "by public transport 1.5 times the car's time"
      },
      {
       "nome": "Barriera di Milano",
       "arrivo": "Falchera",
       "bus": 24.0,
       "auto_min": 11.7,
       "auto_max": 11.7,
       "giudizio": "by public transport 2 times the car's time"
      }
     ],
     "scelto": 0,
     "nota": "Bus and car leave together, one trip after the other, for the 6 most frequent morning car trips. The car has the time forecast by TomTom, parking included."
    },
    {
     "tipo": "dispersione",
     "titolo": "Car time and public transport time, one pair of zones per point",
     "xlabel": "minutes by car (morning, TomTom)",
     "ylabel": "minutes by public transport",
     "punti": [
      [
       15.8,
       20.6,
       1355.3
      ],
      [
       16.2,
       31.3,
       1341.8
      ],
      [
       15.4,
       19.2,
       1324.4
      ],
      [
       16.0,
       24.7,
       1277.0
      ],
      [
       12.2,
       18.7,
       1269.4
      ],
      [
       11.7,
       24.0,
       1208.2
      ],
      [
       26.4,
       43.0,
       1149.2
      ],
      [
       21.6,
       37.5,
       1107.8
      ],
      [
       47.1,
       80.1,
       1081.8
      ],
      [
       9.1,
       15.2,
       1038.1
      ],
      [
       19.8,
       33.2,
       969.9
      ],
      [
       19.7,
       30.6,
       968.1
      ],
      [
       8.7,
       15.2,
       957.2
      ],
      [
       33.8,
       44.5,
       940.7
      ],
      [
       14.1,
       20.2,
       938.8
      ],
      [
       12.6,
       33.5,
       928.7
      ],
      [
       25.0,
       38.2,
       916.7
      ],
      [
       37.0,
       63.4,
       910.0
      ],
      [
       22.5,
       30.4,
       900.6
      ],
      [
       19.5,
       35.2,
       894.4
      ],
      [
       11.4,
       22.4,
       893.3
      ],
      [
       10.0,
       23.8,
       889.9
      ],
      [
       24.4,
       39.3,
       888.0
      ],
      [
       19.1,
       27.5,
       818.9
      ],
      [
       25.6,
       42.3,
       796.7
      ],
      [
       20.2,
       35.2,
       795.1
      ],
      [
       14.4,
       18.9,
       789.0
      ],
      [
       27.8,
       31.2,
       779.1
      ],
      [
       15.1,
       30.4,
       762.5
      ],
      [
       34.0,
       50.0,
       753.4
      ],
      [
       18.3,
       31.2,
       751.2
      ],
      [
       15.9,
       24.3,
       737.2
      ],
      [
       23.7,
       81.4,
       718.7
      ],
      [
       8.0,
       18.1,
       714.6
      ],
      [
       13.8,
       35.2,
       714.1
      ],
      [
       15.9,
       24.0,
       706.6
      ],
      [
       41.7,
       63.5,
       702.1
      ],
      [
       14.8,
       22.6,
       698.0
      ],
      [
       22.9,
       29.7,
       696.9
      ],
      [
       34.9,
       50.3,
       690.4
      ],
      [
       33.6,
       72.7,
       687.3
      ],
      [
       15.3,
       23.2,
       685.0
      ],
      [
       24.5,
       25.5,
       672.4
      ],
      [
       19.8,
       29.2,
       671.0
      ],
      [
       15.9,
       22.8,
       666.8
      ],
      [
       37.4,
       72.4,
       659.4
      ],
      [
       24.2,
       51.0,
       644.0
      ],
      [
       21.4,
       32.7,
       627.3
      ],
      [
       8.7,
       16.0,
       622.4
      ],
      [
       14.4,
       22.2,
       620.3
      ],
      [
       16.4,
       27.2,
       615.4
      ],
      [
       16.4,
       37.0,
       614.3
      ],
      [
       17.6,
       34.5,
       614.1
      ],
      [
       14.6,
       23.4,
       607.7
      ],
      [
       15.4,
       27.2,
       606.6
      ],
      [
       22.7,
       34.0,
       601.6
      ],
      [
       17.6,
       30.4,
       592.7
      ],
      [
       19.6,
       36.0,
       589.8
      ],
      [
       15.8,
       34.1,
       582.5
      ],
      [
       24.6,
       50.2,
       580.1
      ],
      [
       17.1,
       24.1,
       574.5
      ],
      [
       17.1,
       29.9,
       570.6
      ],
      [
       25.2,
       55.1,
       568.2
      ],
      [
       16.4,
       24.6,
       562.6
      ],
      [
       32.0,
       85.7,
       543.7
      ],
      [
       16.6,
       24.1,
       543.0
      ],
      [
       20.5,
       39.2,
       540.9
      ],
      [
       15.8,
       21.6,
       540.3
      ],
      [
       14.6,
       30.9,
       539.8
      ],
      [
       19.5,
       30.7,
       527.7
      ],
      [
       37.0,
       68.8,
       520.3
      ],
      [
       35.6,
       71.6,
       519.9
      ],
      [
       15.1,
       29.4,
       519.7
      ],
      [
       14.9,
       24.9,
       517.1
      ],
      [
       33.7,
       56.9,
       515.6
      ],
      [
       36.0,
       71.2,
       514.3
      ],
      [
       19.8,
       39.6,
       512.4
      ],
      [
       35.6,
       62.2,
       504.1
      ],
      [
       17.1,
       26.9,
       503.9
      ],
      [
       20.0,
       32.7,
       498.7
      ],
      [
       15.5,
       28.9,
       496.3
      ],
      [
       9.4,
       15.5,
       494.3
      ],
      [
       21.1,
       47.1,
       490.1
      ],
      [
       21.3,
       38.7,
       489.2
      ],
      [
       13.9,
       23.2,
       488.9
      ],
      [
       40.9,
       74.0,
       488.2
      ],
      [
       13.4,
       22.0,
       481.0
      ],
      [
       23.0,
       38.2,
       478.8
      ],
      [
       21.7,
       54.9,
       478.7
      ],
      [
       26.4,
       47.5,
       476.8
      ],
      [
       25.1,
       45.8,
       467.9
      ],
      [
       15.0,
       26.2,
       466.7
      ],
      [
       23.2,
       27.7,
       462.0
      ],
      [
       14.9,
       26.3,
       459.7
      ],
      [
       50.0,
       77.7,
       458.7
      ],
      [
       26.0,
       26.0,
       458.5
      ],
      [
       19.4,
       37.2,
       456.6
      ],
      [
       14.0,
       22.8,
       456.0
      ],
      [
       33.3,
       57.1,
       454.7
      ],
      [
       10.3,
       20.3,
       452.9
      ],
      [
       28.9,
       54.0,
       452.3
      ],
      [
       45.2,
       85.9,
       449.8
      ],
      [
       15.8,
       31.6,
       448.6
      ],
      [
       40.8,
       92.7,
       448.4
      ],
      [
       34.4,
       71.8,
       445.5
      ],
      [
       22.8,
       35.8,
       443.8
      ],
      [
       27.2,
       46.5,
       442.8
      ],
      [
       22.5,
       40.2,
       439.9
      ],
      [
       29.2,
       55.3,
       438.4
      ],
      [
       13.9,
       21.4,
       437.5
      ],
      [
       33.7,
       61.8,
       431.9
      ],
      [
       25.5,
       58.3,
       431.8
      ],
      [
       18.1,
       32.3,
       431.4
      ],
      [
       33.2,
       68.6,
       428.4
      ],
      [
       22.0,
       37.4,
       428.4
      ],
      [
       34.3,
       81.3,
       426.2
      ],
      [
       17.7,
       35.8,
       423.2
      ],
      [
       22.8,
       41.3,
       422.6
      ],
      [
       11.7,
       18.2,
       421.9
      ],
      [
       25.9,
       47.6,
       421.1
      ],
      [
       15.7,
       19.0,
       419.2
      ],
      [
       30.8,
       53.4,
       411.0
      ],
      [
       42.7,
       73.5,
       410.3
      ],
      [
       20.1,
       53.8,
       410.0
      ],
      [
       29.9,
       32.7,
       409.6
      ],
      [
       23.5,
       53.5,
       409.5
      ],
      [
       32.7,
       51.2,
       404.3
      ],
      [
       33.6,
       46.1,
       403.5
      ],
      [
       36.1,
       54.5,
       402.7
      ],
      [
       34.2,
       61.2,
       399.0
      ],
      [
       13.8,
       24.9,
       398.4
      ],
      [
       31.3,
       64.3,
       396.9
      ],
      [
       14.5,
       28.4,
       396.9
      ],
      [
       27.5,
       59.6,
       395.5
      ],
      [
       17.9,
       32.4,
       391.8
      ],
      [
       35.6,
       51.1,
       389.9
      ],
      [
       21.3,
       46.5,
       389.6
      ],
      [
       41.5,
       103.8,
       386.9
      ],
      [
       17.5,
       28.0,
       386.6
      ],
      [
       16.6,
       28.2,
       384.3
      ],
      [
       18.1,
       27.5,
       383.2
      ],
      [
       23.0,
       81.4,
       383.2
      ],
      [
       30.3,
       62.3,
       382.4
      ],
      [
       26.8,
       56.5,
       382.0
      ],
      [
       26.2,
       54.1,
       379.4
      ],
      [
       20.5,
       38.4,
       377.6
      ],
      [
       12.6,
       31.4,
       377.4
      ],
      [
       18.0,
       24.3,
       376.5
      ],
      [
       18.2,
       36.7,
       369.2
      ],
      [
       21.5,
       30.6,
       368.7
      ],
      [
       20.2,
       37.1,
       367.3
      ],
      [
       18.9,
       43.4,
       366.6
      ],
      [
       28.6,
       79.1,
       365.7
      ],
      [
       20.7,
       19.3,
       365.5
      ],
      [
       27.3,
       74.5,
       363.3
      ],
      [
       17.2,
       28.2,
       362.7
      ],
      [
       15.2,
       20.9,
       356.4
      ],
      [
       15.7,
       21.4,
       355.0
      ],
      [
       23.8,
       39.1,
       353.0
      ],
      [
       24.5,
       52.3,
       352.5
      ],
      [
       11.1,
       17.1,
       352.1
      ],
      [
       27.7,
       50.6,
       350.1
      ],
      [
       15.2,
       37.0,
       348.3
      ],
      [
       24.8,
       44.8,
       347.8
      ],
      [
       40.4,
       71.4,
       346.3
      ],
      [
       29.9,
       71.2,
       346.1
      ],
      [
       20.7,
       63.5,
       345.7
      ],
      [
       25.3,
       32.0,
       340.6
      ],
      [
       13.4,
       41.8,
       340.0
      ],
      [
       27.5,
       50.6,
       339.6
      ],
      [
       41.6,
       83.0,
       338.3
      ],
      [
       24.2,
       45.7,
       336.5
      ],
      [
       27.5,
       54.3,
       336.5
      ],
      [
       40.2,
       79.4,
       335.5
      ],
      [
       23.9,
       52.0,
       335.0
      ],
      [
       30.3,
       60.6,
       333.8
      ],
      [
       32.0,
       87.7,
       333.6
      ],
      [
       40.4,
       74.5,
       333.5
      ],
      [
       18.1,
       31.4,
       332.2
      ],
      [
       37.0,
       82.7,
       331.5
      ],
      [
       32.9,
       47.6,
       331.5
      ],
      [
       24.5,
       64.4,
       330.5
      ],
      [
       27.5,
       52.4,
       329.9
      ],
      [
       35.1,
       43.5,
       329.1
      ],
      [
       43.6,
       65.5,
       328.2
      ],
      [
       28.1,
       54.2,
       328.0
      ],
      [
       26.0,
       54.2,
       326.5
      ],
      [
       37.6,
       67.1,
       323.5
      ],
      [
       14.5,
       24.0,
       322.3
      ],
      [
       12.0,
       19.2,
       322.1
      ],
      [
       39.6,
       64.3,
       321.4
      ],
      [
       20.8,
       34.1,
       318.2
      ],
      [
       25.8,
       47.8,
       317.7
      ],
      [
       32.7,
       80.6,
       311.9
      ],
      [
       34.9,
       94.0,
       310.7
      ],
      [
       16.4,
       26.4,
       309.9
      ],
      [
       29.0,
       60.2,
       307.1
      ],
      [
       34.6,
       69.8,
       306.3
      ],
      [
       12.1,
       25.1,
       305.1
      ],
      [
       14.6,
       35.8,
       304.4
      ],
      [
       23.1,
       53.0,
       304.2
      ],
      [
       28.6,
       52.3,
       303.6
      ],
      [
       40.9,
       62.6,
       303.4
      ],
      [
       36.9,
       77.0,
       302.8
      ],
      [
       40.7,
       68.8,
       302.3
      ],
      [
       38.5,
       72.2,
       300.8
      ],
      [
       18.9,
       19.0,
       299.5
      ],
      [
       27.3,
       48.9,
       299.2
      ],
      [
       32.1,
       56.4,
       298.9
      ],
      [
       24.6,
       47.2,
       298.6
      ],
      [
       27.4,
       54.3,
       297.1
      ],
      [
       22.6,
       54.1,
       296.5
      ],
      [
       34.2,
       57.7,
       296.0
      ],
      [
       41.1,
       86.8,
       295.0
      ],
      [
       42.3,
       70.0,
       294.0
      ],
      [
       18.1,
       33.8,
       292.7
      ],
      [
       43.5,
       85.7,
       291.8
      ],
      [
       21.4,
       46.0,
       290.8
      ],
      [
       13.6,
       21.3,
       290.5
      ],
      [
       34.5,
       60.2,
       289.4
      ],
      [
       30.0,
       52.7,
       288.9
      ],
      [
       40.2,
       74.6,
       288.6
      ],
      [
       20.2,
       35.0,
       284.7
      ],
      [
       21.5,
       38.6,
       283.1
      ],
      [
       11.4,
       18.9,
       282.6
      ],
      [
       24.2,
       42.7,
       282.2
      ],
      [
       23.4,
       42.2,
       281.8
      ],
      [
       19.5,
       38.3,
       281.7
      ],
      [
       23.4,
       57.4,
       280.3
      ],
      [
       24.7,
       56.7,
       278.1
      ],
      [
       17.4,
       24.5,
       274.9
      ],
      [
       36.9,
       83.0,
       274.4
      ],
      [
       33.1,
       68.0,
       273.4
      ],
      [
       18.1,
       34.6,
       273.2
      ],
      [
       34.9,
       46.0,
       272.4
      ],
      [
       45.6,
       76.5,
       271.8
      ],
      [
       39.1,
       79.0,
       271.3
      ],
      [
       24.8,
       61.4,
       271.0
      ],
      [
       17.4,
       31.8,
       270.6
      ],
      [
       12.7,
       24.6,
       270.2
      ],
      [
       24.7,
       44.1,
       270.1
      ],
      [
       37.1,
       98.2,
       269.7
      ],
      [
       23.9,
       62.1,
       269.7
      ],
      [
       37.9,
       83.6,
       268.9
      ],
      [
       12.6,
       17.1,
       268.5
      ],
      [
       26.5,
       55.2,
       267.8
      ],
      [
       26.2,
       37.0,
       264.3
      ],
      [
       30.2,
       60.4,
       263.3
      ],
      [
       24.7,
       51.4,
       262.3
      ],
      [
       24.7,
       42.2,
       261.5
      ],
      [
       27.5,
       49.4,
       261.2
      ],
      [
       16.5,
       34.8,
       260.2
      ],
      [
       8.6,
       17.5,
       259.7
      ],
      [
       14.7,
       29.1,
       258.2
      ],
      [
       46.1,
       79.4,
       257.3
      ],
      [
       26.8,
       46.5,
       256.8
      ],
      [
       32.1,
       75.8,
       255.1
      ],
      [
       44.6,
       78.2,
       254.4
      ],
      [
       46.1,
       103.2,
       253.6
      ],
      [
       49.8,
       89.0,
       253.1
      ],
      [
       14.3,
       15.8,
       252.2
      ],
      [
       28.3,
       49.4,
       251.6
      ],
      [
       21.5,
       29.9,
       251.5
      ],
      [
       26.4,
       56.6,
       250.1
      ],
      [
       26.2,
       37.3,
       248.3
      ],
      [
       31.8,
       48.8,
       247.4
      ],
      [
       17.8,
       34.8,
       244.8
      ],
      [
       16.7,
       28.9,
       243.9
      ],
      [
       26.6,
       44.1,
       243.6
      ],
      [
       27.1,
       55.0,
       243.6
      ],
      [
       20.2,
       29.2,
       243.6
      ],
      [
       25.1,
       41.8,
       243.0
      ],
      [
       31.5,
       77.9,
       242.3
      ],
      [
       30.3,
       43.4,
       242.2
      ],
      [
       32.2,
       61.5,
       241.4
      ],
      [
       19.1,
       30.4,
       241.0
      ],
      [
       34.4,
       91.5,
       240.6
      ],
      [
       19.6,
       39.4,
       240.0
      ],
      [
       32.0,
       65.0,
       238.3
      ],
      [
       35.5,
       72.1,
       236.1
      ],
      [
       17.2,
       24.2,
       235.8
      ],
      [
       23.2,
       46.3,
       234.9
      ],
      [
       27.3,
       52.5,
       234.7
      ],
      [
       28.2,
       46.3,
       234.6
      ],
      [
       25.5,
       46.7,
       233.6
      ],
      [
       27.8,
       67.6,
       233.3
      ],
      [
       19.9,
       43.3,
       231.7
      ],
      [
       29.4,
       61.4,
       231.5
      ],
      [
       52.7,
       99.5,
       230.9
      ],
      [
       29.6,
       48.0,
       228.8
      ],
      [
       13.9,
       25.4,
       228.3
      ],
      [
       23.2,
       41.6,
       228.1
      ],
      [
       22.2,
       62.8,
       227.0
      ],
      [
       27.2,
       79.2,
       226.3
      ],
      [
       24.3,
       36.1,
       225.6
      ],
      [
       31.2,
       59.0,
       225.4
      ],
      [
       26.8,
       52.0,
       225.1
      ],
      [
       30.7,
       64.8,
       224.1
      ],
      [
       14.9,
       24.1,
       223.2
      ],
      [
       39.9,
       94.3,
       222.3
      ],
      [
       16.1,
       32.1,
       222.1
      ],
      [
       41.2,
       70.7,
       221.0
      ],
      [
       12.5,
       25.9,
       220.4
      ],
      [
       18.8,
       24.2,
       219.8
      ],
      [
       14.9,
       22.4,
       218.7
      ],
      [
       33.9,
       52.8,
       218.3
      ],
      [
       26.7,
       75.5,
       217.8
      ],
      [
       40.9,
       68.5,
       217.1
      ],
      [
       17.4,
       30.8,
       216.9
      ],
      [
       33.4,
       104.0,
       216.3
      ],
      [
       36.2,
       61.0,
       215.9
      ],
      [
       27.1,
       71.9,
       215.8
      ],
      [
       47.2,
       96.9,
       215.6
      ],
      [
       21.8,
       53.9,
       215.3
      ],
      [
       37.1,
       67.0,
       214.1
      ],
      [
       26.8,
       51.6,
       214.0
      ],
      [
       18.3,
       26.0,
       213.2
      ],
      [
       33.3,
       72.4,
       212.7
      ],
      [
       42.8,
       78.5,
       212.0
      ],
      [
       32.4,
       93.1,
       211.8
      ],
      [
       38.9,
       63.9,
       211.3
      ],
      [
       22.7,
       50.2,
       211.2
      ],
      [
       27.0,
       61.1,
       210.7
      ],
      [
       24.4,
       57.8,
       209.8
      ],
      [
       20.9,
       43.2,
       209.0
      ],
      [
       25.7,
       51.2,
       208.2
      ],
      [
       45.2,
       102.7,
       208.1
      ],
      [
       31.4,
       61.3,
       207.6
      ],
      [
       42.5,
       86.5,
       207.5
      ],
      [
       16.6,
       30.0,
       206.7
      ],
      [
       43.7,
       82.2,
       206.4
      ],
      [
       22.1,
       44.2,
       206.2
      ],
      [
       27.1,
       50.9,
       206.2
      ],
      [
       26.4,
       44.3,
       206.1
      ],
      [
       35.9,
       66.5,
       206.0
      ],
      [
       20.7,
       55.3,
       205.9
      ],
      [
       34.4,
       96.3,
       205.6
      ],
      [
       35.6,
       56.6,
       205.0
      ],
      [
       21.6,
       41.6,
       204.7
      ],
      [
       28.6,
       75.6,
       204.3
      ],
      [
       36.8,
       56.6,
       204.3
      ],
      [
       42.0,
       78.0,
       204.0
      ],
      [
       43.4,
       77.3,
       203.9
      ],
      [
       31.4,
       57.1,
       203.8
      ],
      [
       23.9,
       91.5,
       203.7
      ],
      [
       21.9,
       43.6,
       203.5
      ],
      [
       23.4,
       42.6,
       203.4
      ],
      [
       47.2,
       74.0,
       203.4
      ],
      [
       27.7,
       46.8,
       203.2
      ],
      [
       47.6,
       84.4,
       202.3
      ],
      [
       29.8,
       67.5,
       201.9
      ],
      [
       37.2,
       58.4,
       201.7
      ],
      [
       29.8,
       54.3,
       201.5
      ],
      [
       21.9,
       26.2,
       201.5
      ],
      [
       22.3,
       27.0,
       201.2
      ],
      [
       17.8,
       42.8,
       200.7
      ],
      [
       27.7,
       61.8,
       200.5
      ],
      [
       37.5,
       82.2,
       200.3
      ],
      [
       25.9,
       85.6,
       199.7
      ],
      [
       15.7,
       27.0,
       199.4
      ],
      [
       14.3,
       30.9,
       199.3
      ],
      [
       28.6,
       55.4,
       198.8
      ],
      [
       38.3,
       56.4,
       197.7
      ],
      [
       33.1,
       77.4,
       197.7
      ],
      [
       31.3,
       48.8,
       196.4
      ],
      [
       41.6,
       69.6,
       195.7
      ],
      [
       32.2,
       67.0,
       195.6
      ],
      [
       18.9,
       33.0,
       195.3
      ],
      [
       15.7,
       42.0,
       194.7
      ],
      [
       17.4,
       26.4,
       194.6
      ],
      [
       37.1,
       76.1,
       194.1
      ],
      [
       19.7,
       34.1,
       193.8
      ],
      [
       36.8,
       100.1,
       193.0
      ],
      [
       26.1,
       45.7,
       192.7
      ],
      [
       50.2,
       98.6,
       192.4
      ],
      [
       19.7,
       32.5,
       192.2
      ],
      [
       37.5,
       81.0,
       191.6
      ],
      [
       24.3,
       41.7,
       191.5
      ],
      [
       32.3,
       58.7,
       190.6
      ],
      [
       37.5,
       88.2,
       190.5
      ],
      [
       23.3,
       61.8,
       190.5
      ],
      [
       29.1,
       78.3,
       190.5
      ],
      [
       33.2,
       84.6,
       190.2
      ],
      [
       18.2,
       33.7,
       190.2
      ],
      [
       34.2,
       57.8,
       189.6
      ],
      [
       21.1,
       42.1,
       189.4
      ],
      [
       40.9,
       108.3,
       188.8
      ],
      [
       30.0,
       52.8,
       188.6
      ],
      [
       26.4,
       44.8,
       188.5
      ],
      [
       44.1,
       84.5,
       187.6
      ],
      [
       50.6,
       86.5,
       187.3
      ],
      [
       35.0,
       63.9,
       186.9
      ],
      [
       33.6,
       57.4,
       186.9
      ],
      [
       29.2,
       64.1,
       186.9
      ],
      [
       20.9,
       37.8,
       186.8
      ],
      [
       36.5,
       74.2,
       186.4
      ],
      [
       51.1,
       97.4,
       186.4
      ],
      [
       50.5,
       84.8,
       186.2
      ],
      [
       43.9,
       81.6,
       185.9
      ],
      [
       29.6,
       40.7,
       185.7
      ],
      [
       26.8,
       45.0,
       185.5
      ],
      [
       14.7,
       39.8,
       185.4
      ],
      [
       22.0,
       31.4,
       185.1
      ],
      [
       28.7,
       54.9,
       184.5
      ],
      [
       44.6,
       92.0,
       184.1
      ],
      [
       54.5,
       85.6,
       183.3
      ],
      [
       44.4,
       87.8,
       183.3
      ],
      [
       16.2,
       29.6,
       183.2
      ],
      [
       39.8,
       83.0,
       183.0
      ],
      [
       36.0,
       68.7,
       182.4
      ],
      [
       35.0,
       66.2,
       182.4
      ],
      [
       43.9,
       90.8,
       181.8
      ],
      [
       45.1,
       77.4,
       181.2
      ],
      [
       26.2,
       64.3,
       181.2
      ],
      [
       35.2,
       69.0,
       181.1
      ],
      [
       27.6,
       57.4,
       180.8
      ],
      [
       20.2,
       65.9,
       179.9
      ],
      [
       31.0,
       48.9,
       179.7
      ],
      [
       25.5,
       35.5,
       179.6
      ],
      [
       37.7,
       92.6,
       179.5
      ],
      [
       20.3,
       59.6,
       179.5
      ],
      [
       24.9,
       46.4,
       179.5
      ],
      [
       38.4,
       91.4,
       179.2
      ],
      [
       22.7,
       54.4,
       178.4
      ],
      [
       33.2,
       64.8,
       177.9
      ],
      [
       32.5,
       61.2,
       177.9
      ],
      [
       27.7,
       47.4,
       177.4
      ],
      [
       34.8,
       51.0,
       177.3
      ],
      [
       31.6,
       112.9,
       177.0
      ],
      [
       14.1,
       29.5,
       176.7
      ],
      [
       50.3,
       94.5,
       176.2
      ],
      [
       36.7,
       88.2,
       176.0
      ],
      [
       14.2,
       21.1,
       175.3
      ],
      [
       25.5,
       44.9,
       175.0
      ],
      [
       19.5,
       57.0,
       174.5
      ],
      [
       14.8,
       26.6,
       173.9
      ],
      [
       16.3,
       31.4,
       173.6
      ],
      [
       33.5,
       69.0,
       173.5
      ],
      [
       28.5,
       60.7,
       173.4
      ],
      [
       32.5,
       56.0,
       173.2
      ],
      [
       24.1,
       26.6,
       173.1
      ],
      [
       38.7,
       63.1,
       173.1
      ],
      [
       35.9,
       54.3,
       173.0
      ],
      [
       26.7,
       67.0,
       173.0
      ],
      [
       14.3,
       40.7,
       173.0
      ],
      [
       49.9,
       99.5,
       173.0
      ],
      [
       24.3,
       42.6,
       172.3
      ],
      [
       36.8,
       93.0,
       172.0
      ],
      [
       45.6,
       62.5,
       171.6
      ],
      [
       41.0,
       113.8,
       171.3
      ],
      [
       45.8,
       89.9,
       171.3
      ],
      [
       41.2,
       77.7,
       171.2
      ],
      [
       16.7,
       24.7,
       171.0
      ],
      [
       53.8,
       99.0,
       170.7
      ],
      [
       18.9,
       46.9,
       170.0
      ],
      [
       23.8,
       50.3,
       169.8
      ],
      [
       16.6,
       40.7,
       169.6
      ],
      [
       22.8,
       77.5,
       169.4
      ],
      [
       19.5,
       33.8,
       169.2
      ],
      [
       27.1,
       93.1,
       168.9
      ],
      [
       22.3,
       35.8,
       168.6
      ],
      [
       40.1,
       68.6,
       168.1
      ],
      [
       25.3,
       86.0,
       168.1
      ],
      [
       15.3,
       18.2,
       167.9
      ],
      [
       18.5,
       33.7,
       167.5
      ],
      [
       33.5,
       62.8,
       167.2
      ],
      [
       45.6,
       87.9,
       166.7
      ],
      [
       37.4,
       73.5,
       166.7
      ],
      [
       26.8,
       35.6,
       166.1
      ],
      [
       49.7,
       92.3,
       165.5
      ],
      [
       42.2,
       112.0,
       165.4
      ],
      [
       32.3,
       98.0,
       165.4
      ],
      [
       19.0,
       33.8,
       164.6
      ],
      [
       14.1,
       33.0,
       163.9
      ],
      [
       20.2,
       46.1,
       163.8
      ],
      [
       12.3,
       23.3,
       163.6
      ],
      [
       30.9,
       72.8,
       163.5
      ],
      [
       25.1,
       50.7,
       163.3
      ],
      [
       35.3,
       69.8,
       163.0
      ],
      [
       34.0,
       78.5,
       162.2
      ],
      [
       28.6,
       68.0,
       161.5
      ],
      [
       25.5,
       64.2,
       161.5
      ],
      [
       29.5,
       71.0,
       161.5
      ],
      [
       22.2,
       54.7,
       161.4
      ],
      [
       37.1,
       87.0,
       160.9
      ],
      [
       31.4,
       55.1,
       160.0
      ],
      [
       30.9,
       39.7,
       159.7
      ],
      [
       21.7,
       53.4,
       159.5
      ],
      [
       30.2,
       51.4,
       159.4
      ],
      [
       29.4,
       72.3,
       159.3
      ],
      [
       34.8,
       53.0,
       158.2
      ],
      [
       36.6,
       82.8,
       158.2
      ],
      [
       41.7,
       57.2,
       157.9
      ],
      [
       17.1,
       33.0,
       157.8
      ],
      [
       31.8,
       70.6,
       157.5
      ],
      [
       26.5,
       45.2,
       157.3
      ],
      [
       18.2,
       30.2,
       157.3
      ],
      [
       44.8,
       95.0,
       156.5
      ],
      [
       31.9,
       41.1,
       155.8
      ],
      [
       33.7,
       74.4,
       155.6
      ],
      [
       27.1,
       50.9,
       155.4
      ],
      [
       38.1,
       54.8,
       155.2
      ],
      [
       29.8,
       92.7,
       155.1
      ],
      [
       28.6,
       83.6,
       154.9
      ],
      [
       28.9,
       37.8,
       154.5
      ],
      [
       42.7,
       90.2,
       154.5
      ],
      [
       37.3,
       64.6,
       154.1
      ],
      [
       21.6,
       44.6,
       153.6
      ],
      [
       31.0,
       51.8,
       152.4
      ],
      [
       17.0,
       26.6,
       152.3
      ],
      [
       20.0,
       53.8,
       152.3
      ],
      [
       38.8,
       90.8,
       151.5
      ],
      [
       25.9,
       59.0,
       151.3
      ],
      [
       30.1,
       67.8,
       151.2
      ],
      [
       26.7,
       60.4,
       150.6
      ],
      [
       30.1,
       46.1,
       150.2
      ],
      [
       21.8,
       40.1,
       149.8
      ],
      [
       30.4,
       48.5,
       148.6
      ],
      [
       41.2,
       66.8,
       148.5
      ],
      [
       18.1,
       31.5,
       148.2
      ],
      [
       32.2,
       63.6,
       147.4
      ],
      [
       20.4,
       34.0,
       147.2
      ],
      [
       25.8,
       48.2,
       146.3
      ],
      [
       24.6,
       28.6,
       146.1
      ],
      [
       12.7,
       30.9,
       145.2
      ],
      [
       24.8,
       49.4,
       145.0
      ],
      [
       34.7,
       88.6,
       144.6
      ],
      [
       31.0,
       50.1,
       143.8
      ],
      [
       31.3,
       52.5,
       143.2
      ],
      [
       43.9,
       100.8,
       142.8
      ],
      [
       17.4,
       34.2,
       142.2
      ],
      [
       27.8,
       57.7,
       142.1
      ],
      [
       29.4,
       51.0,
       142.1
      ],
      [
       23.0,
       37.6,
       141.5
      ],
      [
       24.4,
       45.2,
       141.1
      ],
      [
       30.1,
       44.0,
       140.8
      ],
      [
       31.1,
       71.0,
       140.6
      ],
      [
       23.2,
       35.3,
       140.1
      ],
      [
       44.8,
       87.5,
       139.1
      ],
      [
       32.8,
       63.6,
       139.1
      ],
      [
       29.7,
       51.9,
       136.6
      ],
      [
       25.5,
       50.3,
       136.6
      ],
      [
       37.8,
       99.4,
       135.8
      ],
      [
       42.8,
       69.8,
       135.1
      ],
      [
       39.8,
       111.8,
       132.9
      ],
      [
       28.3,
       86.0,
       132.9
      ],
      [
       30.6,
       60.8,
       131.1
      ],
      [
       27.7,
       59.3,
       130.6
      ],
      [
       15.2,
       56.8,
       130.3
      ],
      [
       19.9,
       46.1,
       129.1
      ],
      [
       26.0,
       92.4,
       128.8
      ],
      [
       22.5,
       62.7,
       128.8
      ],
      [
       24.0,
       27.2,
       125.9
      ],
      [
       32.8,
       67.2,
       125.8
      ],
      [
       49.0,
       81.4,
       125.8
      ],
      [
       30.5,
       112.6,
       124.6
      ],
      [
       40.7,
       67.6,
       122.4
      ],
      [
       57.6,
       104.8,
       122.4
      ],
      [
       33.9,
       61.3,
       122.0
      ],
      [
       37.8,
       61.1,
       121.7
      ],
      [
       29.0,
       54.6,
       120.0
      ],
      [
       31.9,
       57.8,
       119.6
      ],
      [
       43.5,
       94.6,
       118.8
      ],
      [
       37.3,
       52.6,
       118.8
      ],
      [
       37.3,
       98.0,
       118.6
      ],
      [
       16.2,
       36.6,
       117.9
      ],
      [
       52.1,
       99.4,
       117.8
      ],
      [
       27.3,
       54.6,
       115.5
      ],
      [
       36.9,
       72.6,
       115.5
      ],
      [
       29.3,
       61.6,
       115.5
      ],
      [
       15.0,
       38.8,
       115.5
      ],
      [
       17.8,
       39.2,
       115.5
      ],
      [
       28.4,
       58.2,
       114.2
      ],
      [
       27.5,
       66.4,
       113.9
      ],
      [
       28.8,
       39.5,
       113.4
      ],
      [
       31.4,
       69.0,
       113.4
      ],
      [
       37.3,
       64.6,
       113.4
      ],
      [
       27.4,
       56.5,
       113.4
      ],
      [
       37.0,
       64.4,
       113.4
      ],
      [
       20.6,
       43.1,
       113.4
      ],
      [
       20.2,
       40.0,
       112.0
      ],
      [
       25.5,
       75.6,
       112.0
      ],
      [
       38.7,
       98.4,
       112.0
      ],
      [
       44.5,
       96.2,
       112.0
      ],
      [
       30.3,
       39.3,
       112.0
      ],
      [
       34.7,
       98.4,
       112.0
      ],
      [
       17.5,
       41.0,
       112.0
      ],
      [
       47.5,
       101.9,
       112.0
      ],
      [
       25.0,
       33.4,
       112.0
      ],
      [
       24.6,
       33.8,
       112.0
      ],
      [
       23.1,
       62.0,
       111.0
      ],
      [
       21.5,
       39.8,
       111.0
      ],
      [
       24.3,
       55.8,
       110.8
      ],
      [
       40.3,
       78.2,
       110.3
      ],
      [
       30.0,
       63.8,
       110.3
      ],
      [
       25.9,
       63.4,
       110.1
      ],
      [
       24.4,
       46.2,
       109.2
      ],
      [
       36.6,
       93.8,
       109.2
      ],
      [
       17.5,
       30.2,
       109.2
      ],
      [
       13.6,
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
     "nota": "Each point is a pair of zones, sized by the morning cars; above a line public transport takes more than that multiple of the car's time."
    },
    {
     "tipo": "barre",
     "titolo": "Trips where public transport takes more than twice as long as the car",
     "unita": "cars",
     "nota": "Each bar is the number of morning cars on that trip. On the right, minutes by public transport against minutes by car.",
     "voci": [
      {
       "label": "Barriera di Milano → Falchera",
       "valore": 1208,
       "tono": "rosso",
       "testo": "24 against 12 min · 1,208 cars"
      },
      {
       "label": "Pozzo Strada → Grugliasco",
       "valore": 929,
       "tono": "rosso",
       "testo": "34 against 13 min · 929 cars"
      },
      {
       "label": "Falchera → Barriera di Milano",
       "valore": 890,
       "tono": "rosso",
       "testo": "24 against 10 min · 890 cars"
      },
      {
       "label": "Parella → San Paolo",
       "valore": 763,
       "tono": "rosso",
       "testo": "30 against 15 min · 763 cars"
      },
      {
       "label": "Parella → Cenisia",
       "valore": 715,
       "tono": "rosso",
       "testo": "18 against 8 min · 715 cars"
      },
      {
       "label": "Grugliasco → Pozzo Strada",
       "valore": 714,
       "tono": "rosso",
       "testo": "35 against 14 min · 714 cars"
      },
      {
       "label": "Mirafiori Nord → Grugliasco",
       "valore": 583,
       "tono": "rosso",
       "testo": "34 against 16 min · 583 cars"
      },
      {
       "label": "Parella → Madonna di Campagna",
       "valore": 540,
       "tono": "rosso",
       "testo": "31 against 15 min · 540 cars"
      },
      {
       "label": "Vanchiglia → Madonna Del Pilone",
       "valore": 369,
       "tono": "rosso",
       "testo": "37 against 18 min · 369 cars"
      },
      {
       "label": "Grugliasco → Mirafiori Nord",
       "valore": 348,
       "tono": "rosso",
       "testo": "37 against 15 min · 348 cars"
      },
      {
       "label": "Cenisia → Parella",
       "valore": 260,
       "tono": "rosso",
       "testo": "18 against 9 min · 260 cars"
      },
      {
       "label": "Borgata Vittoria → Aurora",
       "valore": 177,
       "tono": "rosso",
       "testo": "30 against 14 min · 177 cars"
      }
     ]
    }
   ],
   "calcolo": [
    "Zones are those of the 2022 travel survey, with calculation points; each has up to 5 points.",
    "Public transport: on foot, bus, tram and metro, departing between 7:45 and 8:15. We take the median.",
    "Car: free-flow time times the TomTom factor of the pair, plus 5 minutes. Pairs not asked to TomTom take the median of their band. Traffic data: TomTom.",
    "With the traffic sensors the estimate is more favourable to the car: factor 1.2, without traffic lights and junctions. The median ratio becomes 2.9 and 97% of cars have a ratio above 2.",
    "Ratio = public transport time divided by car time, in fixed bands. The cars of a pair are the survey's car trips, leaving between 6 and 10 a.m. on a weekday.",
    "The big number holds for 47% of morning cars (220,307). Trips within a single zone and between towns of the belt are missing.",
    "On known routes Google confirms the public transport times: 31 against 30-35 and 33 against 30-35 minutes.",
    "The scatter chart shows the 600 pairs with the most cars (83.2% of cars). The list of trips uses only pairs with at least 30 interviews."
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
     "Car, TomTom estimate",
     "free-flow time × TomTom factor of the pair (median 2.2) + 5 minutes"
    ],
    [
     "Car, estimate most favourable to the car",
     "free-flow time × 1.2 (5T sensors, they do not count traffic lights and junctions) + 5 minutes"
    ],
    [
     "Sensor period",
     "from 09/10/2,026 to 22/10/2,026"
    ],
    [
     "Ratio bands",
     "under 1.5, 1.5-2, 2-3, over 3"
    ]
   ],
   "limiti": [
    "Outside Turin, trains and other operators are missing: pairs between suburban towns are not in the number. Without metropolitan trains, where they exist, public transport looks slower than it is. The timetable is the scheduled one.",
    "The sensor estimate ignores traffic lights and junctions: it is the most favourable to the car.",
    "Car times forecast by TomTom for typical traffic on a November weekday, not measured on a specific day. A single service is used.",
    "The survey is a sample. Trips within a zone and 653 pairs with no connection (5,616 cars) are not in the comparison."
   ],
   "mappa": {
    "id": "imq",
    "nota": "Nella mappa, tema «Spostamenti»: quanti spostamenti partono da ogni zona e dove vanno (indagine 2022, feriale)."
   },
   "chiave": {
    "valore": "1.9",
    "unita": "times",
    "testo": "the car's time by public transport, in the morning"
   },
   "anima": {
    "tipo": "area",
    "didascalia": "From Piazza Castello, at 7:45 a.m. on a weekday. In 30 minutes you reach ~42% of Turin residents by public transport and ~90% by car (TomTom, parking included)."
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
  "generato": "2026-10-24T00:36:03+00:00",
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
   "tipo_dato": "Tipo di dato: calcolato da dati veri, con gli abitanti del censimento 2021.",
   "titolo": "Circa 1 torinese su 10 vive in una zona con più difficoltà sociali e pochi servizi",
   "domanda": "Si paga per i servizi? E chi vive dove i servizi sono pochi e la fragilità è alta?",
   "numero": {
    "valore": 79598,
    "unita": "",
    "testo": "residenti in zone con più difficoltà sociali e servizi bassi: il 9,5% dei residenti delle zone abitate. È 1,7 volte quanto ci si aspetterebbe per caso.",
    "breve": "residenti con pochi servizi e più difficoltà"
   },
   "principale": {
    "tipo": "dispersione",
    "titolo": "Fragilità sociale e servizi a piedi, una zona OMI per punto (46 zone)",
    "xlabel": "indice di fragilità sociale, 0-100",
    "ylabel": "punteggio «Tutti i servizi» a piedi, 0-100",
    "passo_x": 10,
    "passo_y": 20,
    "xnome": "fragilità",
    "ynome": "servizi",
    "punti": [
     [
      31.7,
      82.2,
      1093,
      "Roma"
     ],
     [
      24.6,
      79.2,
      10989,
      "Carlo Emanuele Ii"
     ],
     [
      31.5,
      77.4,
      2584,
      "Solferino"
     ],
     [
      29.0,
      73.9,
      4598,
      "Vinzaglio"
     ],
     [
      27.6,
      80.9,
      11934,
      "Garibaldi"
     ],
     [
      36.9,
      87.3,
      2369,
      "Castello"
     ],
     [
      32.0,
      79.0,
      4397,
      "Rocca"
     ],
     [
      33.3,
      67.7,
      7157,
      "San Salvario"
     ],
     [
      31.7,
      59.9,
      5486,
      "Valentino"
     ],
     [
      34.2,
      23.5,
      7729,
      "Michelotti"
     ],
     [
      35.5,
      35.0,
      7445,
      "Crimea"
     ],
     [
      39.1,
      69.0,
      894,
      "Duca D Aosta"
     ],
     [
      44.3,
      61.5,
      13406,
      "Porta Palazzo - Maria Ausiliatrice"
     ],
     [
      34.0,
      73.7,
      18276,
      "Vanchiglia - Borgo Rossini"
     ],
     [
      54.3,
      51.8,
      20157,
      "Aurora"
     ],
     [
      31.7,
      62.3,
      22925,
      "Dante"
     ],
     [
      42.8,
      29.8,
      16461,
      "Vanchiglietta"
     ],
     [
      37.3,
      70.5,
      10462,
      "Campidoglio - Martinetto"
     ],
     [
      27.4,
      73.3,
      11167,
      "Adriano - Bernini - Rivoli"
     ],
     [
      36.1,
      72.5,
      18643,
      "Cenisia"
     ],
     [
      38.7,
      64.1,
      29291,
      "San Paolo"
     ],
     [
      28.9,
      66.5,
      5190,
      "San Secondo"
     ],
     [
      35.3,
      59.6,
      7970,
      "Galileo Ferraris"
     ],
     [
      28.9,
      63.8,
      15343,
      "De Gasperi"
     ],
     [
      34.1,
      72.8,
      1405,
      "Politecnico"
     ],
     [
      30.2,
      81.0,
      14491,
      "Duchessa Jolanda"
     ],
     [
      41.3,
      64.6,
      22334,
      "San Donato"
     ],
     [
      56.5,
      46.7,
      71762,
      "Madonna Di Campagna"
     ],
     [
      47.8,
      44.5,
      4322,
      "Spina 4 - Docks Dora"
     ],
     [
      58.5,
      9.5,
      10584,
      "Barca - Bertolla"
     ],
     [
      44.3,
      37.8,
      26802,
      "Nizza Millefonti"
     ],
     [
      49.8,
      52.8,
      46558,
      "Filadelfia - Traiano"
     ],
     [
      40.9,
      62.4,
      56890,
      "Santa Rita"
     ],
     [
      54.5,
      43.9,
      40047,
      "Mirafiori Nord"
     ],
     [
      62.1,
      57.6,
      48588,
      "Barriera Di Milano"
     ],
     [
      64.9,
      33.4,
      28202,
      "Rebaudengo - Regio Parco"
     ],
     [
      63.1,
      15.4,
      25756,
      "Corona Nord"
     ],
     [
      65.9,
      21.3,
      31262,
      "Lucento - Vallette"
     ],
     [
      40.2,
      55.5,
      31541,
      "Parella"
     ],
     [
      47.6,
      39.5,
      32025,
      "Aeronautica - Lesna"
     ],
     [
      40.3,
      55.8,
      36080,
      "Pozzo Strada"
     ],
     [
      63.0,
      25.6,
      33481,
      "Mirafiori Sud"
     ],
     [
      36.9,
      40.2,
      11318,
      "Spina 3 - Eurotorino"
     ],
     [
      48.1,
      5.7,
      9568,
      "Collinare Villa Della Regina"
     ],
     [
      45.3,
      4.6,
      3563,
      "Collinare Superga"
     ],
     [
      40.7,
      6.0,
      5865,
      "Collinare Cavoretto"
     ]
    ],
    "retta": {
     "a": 107.82,
     "b": -1.323,
     "label": "tendenza"
    },
    "nota": "Ogni punto è una zona, grande quanto i suoi abitanti. La linea è la tendenza: più la fragilità è alta, meno servizi. Il legame regge anche a parità di distanza dal centro: correlazione −0,48 (da −0,66 a −0,23)."
   },
   "punti": [
    "A parità di distanza dal centro il legame prezzo-servizi quasi sparisce: correlazione 0,21 su 46 zone (da −0,12 a 0,52).",
    "5 zone sono in doppio svantaggio: Mirafiori Sud, Lucento - Vallette, Rebaudengo - Regio Parco, Corona Nord, Barca - Bertolla. Ci abitano ~129 mila persone.",
    "A parità di distanza dal centro reggono fragilità-servizi (−0,48) e prezzo-fragilità (−0,69)."
   ],
   "altri": [
    {
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
     "nota": "Ogni punto è una zona, grande quanto i suoi abitanti. A parità di distanza dal centro il legame quasi sparisce (0,21): la linea mostra soprattutto l'effetto della distanza dal centro."
    },
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
    }
   ],
   "calcolo": [
    "Unità: le 46 zone OMI di Torino con almeno 500 abitanti. Le sezioni si sommano nella zona, pesate per abitanti.",
    "Servizi: punteggio «Tutti i servizi» a piedi in 15 minuti. Fragilità: indice del censimento 2021 (lavoro, istruzione, case, anziani).",
    "Prezzo: centro della forbice OMI per le abitazioni civili. Tendenza: retta dei minimi quadrati.",
    "Doppio svantaggio = fragilità nel 20% più alto e servizi nel 20% più basso. Soglie fissate prima dei numeri: 49,8 e 33,4.",
    "Legami a parità di distanza dal centro: correlazione parziale sui ranghi, con intervallo al 95% per ricampionamento. Regge solo se l'intervallo non contiene lo zero."
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
     "Legami a parità di distanza",
     "correlazione parziale sui ranghi, intervallo al 95%; distanza dal centro della zona a Piazza Castello"
    ]
   ],
   "limiti": [
    "I prezzi sono quotazioni OMI, non compravendite.",
    "C'è un solo semestre di quotazioni (2025/2).",
    "Le zone OMI sono grandi: dentro una zona i prezzi e i servizi cambiano molto.",
    "L'indice di fragilità non è il reddito: misura lavoro, istruzione, affollamento e anziani."
   ],
   "mappa": {
    "id": "vulnerabilita",
    "nota": "Vista «Doppio svantaggio» nel tema Fragilità sociale.",
    "vista": "doppio"
   },
   "anima": {
    "tipo": "omini",
    "totale": 10,
    "colorati": 1,
    "didascalia": "Circa 1 torinese su 10 vive dove l'indice di fragilità sociale è alto e i servizi sono pochi (9,5% dei residenti delle zone abitate)."
   },
   "chiave": {
    "valore": "~1",
    "unita": "torinese su 10",
    "testo": "vive dove i servizi sono pochi e le difficoltà sociali alte"
   }
  },
  "forma_en": {
   "tipo_dato": "Type of data: calculated from real data, with the residents of the 2021 census.",
   "titolo": "About 1 Turin resident in 10 lives in an area with more social difficulties and few services",
   "domanda": "Do people pay for services? And who lives where services are few and fragility is high?",
   "numero": {
    "valore": 79598,
    "unita": "",
    "testo": "residents in zones with more social difficulty and few services: 9.5% of residents of inhabited zones. That is 1.7 times what you would expect by chance.",
    "breve": "residents with few services and more difficulties"
   },
   "principale": {
    "tipo": "dispersione",
    "titolo": "Social fragility and services on foot, one OMI zone per dot (46 zones)",
    "xlabel": "social fragility index, 0-100",
    "ylabel": "“All services” score on foot, 0-100",
    "passo_x": 10,
    "passo_y": 20,
    "xnome": "fragilità",
    "ynome": "servizi",
    "punti": [
     [
      31.7,
      82.2,
      1093,
      "Roma"
     ],
     [
      24.6,
      79.2,
      10989,
      "Carlo Emanuele Ii"
     ],
     [
      31.5,
      77.4,
      2584,
      "Solferino"
     ],
     [
      29.0,
      73.9,
      4598,
      "Vinzaglio"
     ],
     [
      27.6,
      80.9,
      11934,
      "Garibaldi"
     ],
     [
      36.9,
      87.3,
      2369,
      "Castello"
     ],
     [
      32.0,
      79.0,
      4397,
      "Rocca"
     ],
     [
      33.3,
      67.7,
      7157,
      "San Salvario"
     ],
     [
      31.7,
      59.9,
      5486,
      "Valentino"
     ],
     [
      34.2,
      23.5,
      7729,
      "Michelotti"
     ],
     [
      35.5,
      35.0,
      7445,
      "Crimea"
     ],
     [
      39.1,
      69.0,
      894,
      "Duca D Aosta"
     ],
     [
      44.3,
      61.5,
      13406,
      "Porta Palazzo - Maria Ausiliatrice"
     ],
     [
      34.0,
      73.7,
      18276,
      "Vanchiglia - Borgo Rossini"
     ],
     [
      54.3,
      51.8,
      20157,
      "Aurora"
     ],
     [
      31.7,
      62.3,
      22925,
      "Dante"
     ],
     [
      42.8,
      29.8,
      16461,
      "Vanchiglietta"
     ],
     [
      37.3,
      70.5,
      10462,
      "Campidoglio - Martinetto"
     ],
     [
      27.4,
      73.3,
      11167,
      "Adriano - Bernini - Rivoli"
     ],
     [
      36.1,
      72.5,
      18643,
      "Cenisia"
     ],
     [
      38.7,
      64.1,
      29291,
      "San Paolo"
     ],
     [
      28.9,
      66.5,
      5190,
      "San Secondo"
     ],
     [
      35.3,
      59.6,
      7970,
      "Galileo Ferraris"
     ],
     [
      28.9,
      63.8,
      15343,
      "De Gasperi"
     ],
     [
      34.1,
      72.8,
      1405,
      "Politecnico"
     ],
     [
      30.2,
      81.0,
      14491,
      "Duchessa Jolanda"
     ],
     [
      41.3,
      64.6,
      22334,
      "San Donato"
     ],
     [
      56.5,
      46.7,
      71762,
      "Madonna Di Campagna"
     ],
     [
      47.8,
      44.5,
      4322,
      "Spina 4 - Docks Dora"
     ],
     [
      58.5,
      9.5,
      10584,
      "Barca - Bertolla"
     ],
     [
      44.3,
      37.8,
      26802,
      "Nizza Millefonti"
     ],
     [
      49.8,
      52.8,
      46558,
      "Filadelfia - Traiano"
     ],
     [
      40.9,
      62.4,
      56890,
      "Santa Rita"
     ],
     [
      54.5,
      43.9,
      40047,
      "Mirafiori Nord"
     ],
     [
      62.1,
      57.6,
      48588,
      "Barriera Di Milano"
     ],
     [
      64.9,
      33.4,
      28202,
      "Rebaudengo - Regio Parco"
     ],
     [
      63.1,
      15.4,
      25756,
      "Corona Nord"
     ],
     [
      65.9,
      21.3,
      31262,
      "Lucento - Vallette"
     ],
     [
      40.2,
      55.5,
      31541,
      "Parella"
     ],
     [
      47.6,
      39.5,
      32025,
      "Aeronautica - Lesna"
     ],
     [
      40.3,
      55.8,
      36080,
      "Pozzo Strada"
     ],
     [
      63.0,
      25.6,
      33481,
      "Mirafiori Sud"
     ],
     [
      36.9,
      40.2,
      11318,
      "Spina 3 - Eurotorino"
     ],
     [
      48.1,
      5.7,
      9568,
      "Collinare Villa Della Regina"
     ],
     [
      45.3,
      4.6,
      3563,
      "Collinare Superga"
     ],
     [
      40.7,
      6.0,
      5865,
      "Collinare Cavoretto"
     ]
    ],
    "retta": {
     "a": 107.82,
     "b": -1.323,
     "label": "trend"
    },
    "nota": "Each dot is a zone, sized by its residents. The line is the trend: the higher the fragility, the fewer the services. The link holds even at equal distance from the centre: correlation −0.48 (from −0.66 to −0.23)."
   },
   "punti": [
    "At equal distance from the centre the price-services link nearly disappears: correlation 0.21 over 46 zones (from −0.12 to 0.52).",
    "5 zones are in double disadvantage: Mirafiori Sud, Lucento - Vallette, Rebaudengo - Regio Parco, Corona Nord, Barca - Bertolla. ~129 thousand people live there.",
    "At equal distance from the centre, fragility-services (−0.48) and price-fragility (−0.69) hold."
   ],
   "altri": [
    {
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
     "nota": "Each dot is a zone, sized by its residents. At equal distance from the centre the link nearly disappears (0.21): the line mostly shows the effect of distance from the centre."
    },
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
    }
   ],
   "calcolo": [
    "Unit: the 46 OMI zones of Turin with at least 500 inhabitants. Sections are added up within the zone, weighted by inhabitants.",
    "Services: “All services” score within a 15-minute walk. Fragility: 2021 census index (work, education, housing, older people).",
    "Price: middle of the OMI range for residential homes. Trend: least-squares line.",
    "Double disadvantage = fragility in the highest 20% and services in the lowest 20%. Thresholds fixed before the numbers: 49.8 and 33.4.",
    "Links at equal distance from the centre: partial rank correlation, with a 95% interval by resampling. It holds only if the interval does not contain zero."
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
     "Links at equal distance",
     "partial rank correlation, 95% interval; distance from the centre of the zone to Piazza Castello"
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
   "anima": {
    "tipo": "omini",
    "totale": 10,
    "colorati": 1,
    "didascalia": "About 1 Turin resident in 10 lives where the social fragility index is high and services are few (9.5% of residents of inhabited areas)."
   },
   "chiave": {
    "valore": "~1",
    "unita": "Turin resident in 10",
    "testo": "lives where services are few and social difficulties high"
   }
  },
  "numero_pubblico": 5,
  "_nome": "risultato10_riepilogo_mappa.json"
 }
];
window.SCHEDE_PERIODO = {"da": "2026-10-09", "a": "2026-10-22"};
