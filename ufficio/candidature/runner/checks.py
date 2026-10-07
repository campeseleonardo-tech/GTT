# checks.py - controlli deterministici (nessun LLM) su CV_description e lettera.
# Uso diretto:  python checks.py cv  <file.txt> [offer.txt]
#               python checks.py letter <file.txt> [offer.txt]
import re, sys
from pathlib import Path

BASELINE_PATH = None   # impostato dal runner: percorso del documento baseline CV
HARD_MAX = 90          # righe di descrizione normali
TOLERATED = 92         # massimo assoluto tollerato
LONG_MIN, LONG_MAX = 172, 180   # righe "doppie" importanti
MAX_LONG_LINES = 4     # poche righe importanti

SECTION_RE = re.compile(r"^[A-ZÄÖÜ][A-ZÄÖÜ /&\-]{3,}$")        # intestazioni TUTTE MAIUSCOLE
DATE_RE = re.compile(r"\d{2}/\d{4}|\d{4}\s*[-–]\s*\d{4}")
CLIENTS = ["McLaren", "Ducati", "Pankl", "Harbinger", "AMG", "MANN+HUMMEL", "BMW", "Yamaha"]
FORBIDDEN_CV = [
    (r"von der Initiierung bis zum Abschluss", "Virtual Prototype 'start to finish'"),
    (r"from initiation to (completion|closure)", "Virtual Prototype 'start to finish'"),
    (r"dall'inizio alla fine", "Virtual Prototype 'start to finish'"),
    (r"07/2026", "data KTM vietata 07/2026"),
    (r"informell|informal|in nero|undeclared", "occupazione informale da non dichiarare"),
    (r"ISO ?9001|IATF", "QM formale non rivendicabile"),
    (r"\*\*|^#{1,6} |\t", "markdown/tab nel TXT"),
]
FORBIDDEN_LETTER = [
    (r"[–—]", "trattino lungo (vietato)"),
    (r"\?", "punto interrogativo (domande retoriche vietate)"),
    (r"\bhab\b|\bwohn\b|\berzähl\b", "verbo troncato"),
    (r"Über ein Gespräch würde ich mich freuen", "chiusura standard vietata"),
    (r"(?i)excited to apply|thrilled to apply|I am writing to apply", "formula standard vietata"),
    (r"(?i)ho letto l'offerta|mi ha incuriosit|I read your (job )?(ad|posting)|Ihre Stellenanzeige hat mich", "apertura 'ho letto l'offerta' vietata"),
    (r"Drei Jahre bei KTM|Three years at KTM|Tre anni in KTM", "apertura 'periodo + risultato' vietata"),
    (r"Verfügbar bin ich|Studiert habe ich", "inversione tedesca vietata"),
]


def has_client(c, text, offer_text):
    pat = r"(?<![A-Za-z])" + re.escape(c) + r"(?![A-Za-z])"
    return re.search(pat, text, re.I) and not re.search(pat, offer_text, re.I)


def read(p):
    return Path(p).read_text(encoding="utf-8-sig").replace("\r\n", "\n")


def check_cv(path, offer_text="", lang=""):
    text = read(path)
    lines = text.split("\n")
    issues, warns = [], []

    # segnaposto
    for i, ln in enumerate(lines, 1):
        if "[[" in ln:
            issues.append(("PLACEHOLDER", i, ln.strip()[:120]))

    # sezioni WORK EXPERIENCE / EDUCATION -> righe di descrizione
    in_scope, sec = False, ""
    long_count = 0
    for i, ln in enumerate(lines, 1):
        s = ln.strip()
        if SECTION_RE.match(s) and "|" not in s:
            sec = s
            in_scope = s.startswith(("WORK EXPERIENCE", "EDUCATION"))
            continue
        if not in_scope or not s:
            continue
        nxt = ""
        for j in range(i, len(lines)):
            if lines[j].strip():
                nxt = lines[j].strip()
                break
        is_title = (" | " in s and DATE_RE.search(s)) or (" | " in nxt and DATE_RE.search(nxt))
        if is_title:
            continue
        n = len(s)
        if n <= HARD_MAX:
            continue
        if n <= TOLERATED:
            warns.append(("TOLLERATA", i, f"{n} car.: {s[:70]}..."))
        elif LONG_MIN <= n <= LONG_MAX:
            long_count += 1
        else:
            issues.append(("LUNGHEZZA", i, f"{n} car. (ammessi <=90, o 172-180): {s[:70]}..."))
    if long_count > MAX_LONG_LINES:
        warns.append(("RIGHE_LUNGHE", 0, f"{long_count} righe doppie (suggerito <= {MAX_LONG_LINES})"))

    # date KTM obbligatorie
    for pat, lab in [(r"03/2023\s*[-–]\s*09/2023", "KTM Intern 03/2023-09/2023"),
                     (r"09/2023\s*[-–]\s*06/2025", "KTM System Testing 09/2023-06/2025"),
                     (r"06/2025\s*[-–]\s*06/2026", "KTM Functional Dev 06/2025-06/2026")]:
        if not re.search(pat, text):
            issues.append(("DATE_KTM", 0, f"manca {lab}"))

    # contenuti obbligatori
    if not re.search(r"IPMA Level D", text):
        issues.append(("IPMA", 0, "manca IPMA Level D"))
    if not re.search(r"(?i)(franz|french|francese|fran[cç]ais|franc[eé]s).{0,40}A2", text):
        issues.append(("FRANCESE", 0, "manca francese base (A2) nelle lingue"))
    for kw in ["ABOUT ME", "WORK EXPERIENCE", "EDUCATION", "CERTIFICATIONS", "LANGUAGES", "TOOLS"]:
        if kw not in text:
            issues.append(("SEZIONE", 0, f"manca la sezione {kw}"))

    # lingua delle etichette (solo DE ed EN)
    head = "\n".join(lines[:10])
    if lang == "DE":
        if re.search(r"(?m)^\s*(Italian|English|Spanish|German|French)\s*:", text):
            issues.append(("LINGUA", 0, "nomi delle lingue in inglese in un CV tedesco (es. 'Italienisch: Muttersprache')"))
        if re.search(r"Austria\b", head):
            issues.append(("LINGUA", 0, "riga del luogo in inglese ('Austria' invece di 'Österreich')"))
    if lang == "EN" and re.search(r"(?m)^\s*(Italienisch|Englisch|Spanisch|Deutsch|Französisch)\s*:", text):
        issues.append(("LINGUA", 0, "nomi delle lingue in tedesco in un CV inglese"))

    # frasi negative sul gap nel CV (ABOUT ME compreso)
    NEG = r"nur Berührungspunkte|nur am Rand|bisher (nur|nicht|keine|kein)|noch (nicht|kein)|keine Erfahrung|no (professional )?experience|not yet|only seen|nur gesehen"
    m2 = re.search(r"ABOUT ME\n+(.+?)\n\s*\n", text, flags=re.S)
    if m2 and re.search(NEG, m2.group(1)):
        issues.append(("GAP_NEL_CV", 0, "frase negativa sul gap in ABOUT ME (va solo in lettera e analisi)"))

    # voci con meno di 3 righe di descrizione (dato mancante, non errore)
    for sec_name in ("WORK EXPERIENCE", "EDUCATION"):
        mm = re.search(r"(?m)^" + sec_name + r"\n(.*?)(?=^[A-Z][A-Z /&\-]{3,}$|\Z)", text, flags=re.S)
        if not mm:
            continue
        for block in re.split(r"\n\s*\n", mm.group(1).strip()):
            bl = [x for x in block.split("\n") if x.strip()]
            if len(bl) >= 2 and " | " in bl[1] and DATE_RE.search(bl[1]):
                n_desc = len(bl) - 2
                if n_desc < 3:
                    warns.append(("VOCE_CORTA", 0, f"{bl[0][:50]}: {n_desc} righe di descrizione (fatto mancante?)"))

    # About me ~400 caratteri
    m = re.search(r"ABOUT ME\n+(.+?)\n\s*\n", text, flags=re.S)
    if m:
        n = len(" ".join(m.group(1).split()))
        if not 300 <= n <= 480:
            warns.append(("ABOUT_ME", 0, f"{n} caratteri (circa 400 previsti)"))

    # titoli e nomi come in baseline (non si traducono)
    for must in ["Functional Development Engineer", "System Testing Engineer", "Intern R&D", "SEO Data Analyst",
                 "Event Manager", "Fluid Dynamics", "Thermal Management", "Aerodynamics",
                 "Master of Science in Engineering", "Innovation & Product Management",
                 "Business & Management", "FH Upper Austria", "Universita degli Studi di Torino",
                 "University Collaboration", "Heilbronn University", "SCRUM Certification"]:
        if _plain(must) not in _plain(text):
            issues.append(("TITOLO", 0, f"manca '{must}' scritto come in baseline (titoli e nomi non si traducono)"))

    # CV_description contiene SEMPRE tutte le voci (decide Leonardo cosa togliere)
    for must in ["Electrician (Seasonal)", "Pizzaiolo"]:
        if must not in text:
            issues.append(("VOCE_MANCANTE", 0, f"manca la voce '{must}': il CV_description le contiene tutte"))

    # regole di contenuto
    for pat, lab in FORBIDDEN_CV:
        for mm in re.finditer(pat, text, flags=re.M):
            line_no = text[:mm.start()].count("\n") + 1
            issues.append(("VIETATO", line_no, lab))
    for c in CLIENTS:
        if has_client(c, text, offer_text):
            warns.append(("CLIENTE", 0, f"nome cliente '{c}' nel testo (usare descrittore generico)"))
    return issues, warns


def _plain(s):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)).lower()


def check_letter(path, offer_text="", lang=""):
    text = read(path)
    issues, warns = [], []
    for i, ln in enumerate(text.split("\n"), 1):
        if "[[" in ln:
            issues.append(("PLACEHOLDER", i, ln.strip()[:120]))
    for c in CLIENTS:
        if has_client(c, text, offer_text):
            warns.append(("CLIENTE", 0, f"nome cliente '{c}' (usare descrittore generico)"))
    if re.search(r"\+\s?43|\b660\s?\d{3}|(?i:telefon|handynummer|rufnummer|phone number|numero di telefono)|erreichen Sie mich unter", text):
        issues.append(("VIETATO", 0, "numero di telefono nella lettera (toglierlo)"))
    if re.search(r"@\w+\.\w+", text):
        issues.append(("VIETATO", 0, "indirizzo e-mail nel testo della lettera"))
    if re.search(r"(?i)vor dem Studium|before (my )?(studies|studying|university)|prima degli studi|prima dell'universit", text):
        issues.append(("VIETATO", 0, "lavoro stagionale 2014-2018 NON e' prima degli studi: scrivere 'ogni estate'"))
    if re.search(r"(?i)informell|informal|in nero", text):
        issues.append(("VIETATO", 0, "occupazione informale da non dichiarare"))
    for pat, lab in [(r"(?i)\barbeite\s+(seit\b|derzeit|aktuell|momentan|bei KTM)|seit (drei|3|zwei|vier) Jahren bei KTM|\bbin\s+(derzeit|aktuell|momentan)?\s*bei KTM|(?i:I (currently )?work (at|for) KTM)|(?i:lavoro (attualmente )?(in|da|per) KTM)", "tempo presente su KTM (e' finito a 06/2026: usare il passato)")]:
        for mm in re.finditer(pat, text):
            issues.append(("TEMPO", text[:mm.start()].count("\n") + 1, lab))
    # numeri e nomi propri devono stare nel baseline
    base = ""
    for cand in ([Path(BASELINE_PATH)] if BASELINE_PATH else []) + [Path(path).resolve().parents[2] / "context" / "CV_description_baseline.txt",
                 Path(path).resolve().parents[1] / "context" / "CV_description_baseline.txt"]:
        if cand.exists():
            base = cand.read_text(encoding="utf-8", errors="ignore"); break
    if base:
        offer_l = offer_text.lower()
        for num in set(re.findall(r"\b\d[\d.,]*\b", text)):
            if num not in base and num not in offer_text:
                warns.append(("NUMERO_NOME", 0, f"numero '{num}' non e' nel baseline: verificare"))
        for nm in ([] if lang == "DE" else set(re.findall(r"(?<![.!?]\s)(?<!^)\b[A-Z][\w+-]{3,}\b", text))):
            if nm.lower() not in base.lower() and nm.lower() not in offer_l:
                warns.append(("NUMERO_NOME", 0, f"nome '{nm}' non e' nel baseline ne' nell'offerta: verificare"))
    for pat, lab in [(r"(?i)\bStunden pro Woche\b|\bWochenstunden\b|\bVollzeit\b|\bTeilzeit\b|\bGehalt\b|\bSchicht(en|arbeit|dienst)?\b|\bNachtarbeit\b|hours per week|full-time|part-time|\bsalary\b|shift work|night shift", "IMPEGNO su ore/turni/stipendio: e' in baseline?")]:
        for mm in re.finditer(pat, text):
            warns.append(("REVISIONE", text[:mm.start()].count("\n") + 1, lab))
    words = len(text.split())
    if words < 140:
        warns.append(("LUNGHEZZA", 0, f"solo {words} parole"))
    if words > 320:
        warns.append(("LUNGHEZZA", 0, f"{words} parole (target 150-300)"))
    return issues, warns


def fmt(issues, warns):
    out = [f"  ERRORE  {k} r.{ln}: {msg}" for k, ln, msg in issues]
    out += [f"  avviso  {k} r.{ln}: {msg}" for k, ln, msg in warns]
    return "\n".join(out) if out else "  nessun problema"


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    kind, f = sys.argv[1], sys.argv[2]
    offer = read(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3] else ""
    lang = sys.argv[4] if len(sys.argv) > 4 else ""
    iss, wr = (check_cv if kind == "cv" else check_letter)(f, offer, lang)
    print(f"{f}\n{fmt(iss, wr)}")
    sys.exit(1 if iss else 0)
