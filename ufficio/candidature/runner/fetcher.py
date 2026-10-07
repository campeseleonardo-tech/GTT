#!/usr/bin/env python3
"""
fetcher.py - legge una pagina di offerta (link) e le pagine "chi siamo" dell'azienda.
Nessun token Claude usato: e' solo Python sul tuo PC.

Prova da PowerShell:  python fetcher.py "https://..."
Non solleva mai eccezioni verso il chiamante: se qualcosa non va restituisce testo vuoto e il motivo.
"""
import gzip, json, re, sys
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0 Safari/537.36")
MIN_OFFER_CHARS = 600
MAX_OFFER_CHARS = 15000
MAX_PAGE_CHARS = 5000
ABOUT_RE = re.compile(r"(?i)\babout\b|über uns|ueber[-_ ]?uns|unternehmen|\bcompany\b|chi siamo|\bazienda\b|"
                      r"mission|vision|leitbild|\bwerte\b|\bvalues\b|who we are|wer wir sind|philosophie|"
                      r"unsere geschichte|our story|\bprofil\b|wir über|nosotros|qui sommes")
SKIP_EXT = re.compile(r"(?i)\.(pdf|jpg|jpeg|png|gif|svg|zip|docx?|xlsx?|pptx?|mp4)(\?|$)")
BLOCK_TAGS = {"p", "div", "br", "li", "ul", "ol", "h1", "h2", "h3", "h4", "h5", "h6", "tr", "section",
              "article", "table", "dd", "dt", "header", "main", "aside"}
SKIP_TAGS = {"script", "style", "noscript", "svg", "nav", "footer", "form", "iframe", "template"}


class _Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip, self.links, self._href, self._atext = [], 0, [], None, []
        self.title, self._in_title = "", False

    def handle_starttag(self, tag, attrs):
        if tag in SKIP_TAGS:
            self.skip += 1
        if tag == "title":
            self._in_title = True
        if tag == "a":
            self._href = dict(attrs).get("href")
            self._atext = []
        if tag in BLOCK_TAGS:
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in SKIP_TAGS and self.skip:
            self.skip -= 1
        if tag == "title":
            self._in_title = False
        if tag == "a" and self._href is not None:
            self.links.append((self._href, " ".join("".join(self._atext).split())))
            self._href = None
        if tag in BLOCK_TAGS:
            self.out.append("\n")

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._href is not None:
            self._atext.append(data)
        if not self.skip:
            self.out.append(data)


def html_to_text(html):
    p = _Text()
    try:
        p.feed(html)
    except Exception:
        pass
    lines, prev = [], None
    for raw in "".join(p.out).split("\n"):
        ln = " ".join(raw.split())
        if ln and ln != prev:
            lines.append(ln)
        prev = ln or prev
    return "\n".join(lines), p.links, " ".join(p.title.split())


def http_get(url, timeout=30):
    """Ritorna (html, errore)."""
    try:
        req = Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml",
                                    "Accept-Language": "de,en;q=0.8,it;q=0.6"})
        with urlopen(req, timeout=timeout) as r:
            raw = r.read(3_000_000)
            enc = (r.headers.get("Content-Encoding") or "").lower()
            if "gzip" in enc:
                raw = gzip.decompress(raw)
            ctype = r.headers.get("Content-Type") or ""
            if ctype and "html" not in ctype.lower() and "text" not in ctype.lower():
                return "", f"tipo di contenuto non testuale ({ctype})"
            m = re.search(r"charset=([\w-]+)", ctype) or re.search(rb"charset=[\"']?([\w-]+)", raw[:4000])
            cs = m.group(1) if m and isinstance(m.group(1), str) else (m.group(1).decode("ascii", "ignore") if m else "utf-8")
            try:
                return raw.decode(cs, errors="replace"), ""
            except LookupError:
                return raw.decode("utf-8", errors="replace"), ""
    except Exception as e:
        return "", f"{type(e).__name__}: {e}"


def _walk(o):
    if isinstance(o, dict):
        yield o
        for v in o.values():
            yield from _walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from _walk(v)


def jobposting_from_jsonld(html):
    """Molti siti di carriera inseriscono l'offerta come dati strutturati: e' il testo piu' pulito."""
    for m in re.finditer(r"(?is)<script[^>]+application/ld\+json[^>]*>(.*?)</script>", html):
        try:
            data = json.loads(m.group(1).strip())
        except Exception:
            continue
        for d in _walk(data):
            t = d.get("@type")
            if t == "JobPosting" or (isinstance(t, list) and "JobPosting" in t):
                desc = html_to_text(str(d.get("description", "")))[0]
                org = d.get("hiringOrganization") or {}
                org_name = org.get("name", "") if isinstance(org, dict) else str(org)
                org_url = (org.get("sameAs") or org.get("url") or "") if isinstance(org, dict) else ""
                loc = ""
                jl = d.get("jobLocation")
                if isinstance(jl, list) and jl:
                    jl = jl[0]
                if isinstance(jl, dict):
                    a = jl.get("address") or {}
                    if isinstance(a, dict):
                        loc = ", ".join(str(a.get(k, "")) for k in ("addressLocality", "addressRegion", "addressCountry") if a.get(k))
                head = [f"Titel: {d.get('title', '')}", f"Unternehmen: {org_name}", f"Ort: {loc}",
                        f"Anstellungsart: {d.get('employmentType', '')}"]
                body = "\n".join(x for x in head if x.split(": ", 1)[1].strip()) + "\n\n" + desc
                return body, org_url if isinstance(org_url, str) else ""
    return "", ""


def _root(host):
    parts = host.lower().split(".")
    return ".".join(parts[-2:]) if len(parts) >= 2 else host.lower()


def fetch_offer(url):
    """Ritorna dict: ok, text, title, error, links, html, org_url."""
    html, err = http_get(url)
    res = {"ok": False, "text": "", "title": "", "error": err, "links": [], "org_url": ""}
    if not html:
        return res
    page_text, links, title = html_to_text(html)
    ld_text, org_url = jobposting_from_jsonld(html)
    text = ld_text if len(ld_text) >= 500 else page_text
    res.update(text=text[:MAX_OFFER_CHARS], title=title, links=links, org_url=org_url)
    if len(text) < MIN_OFFER_CHARS:
        res["error"] = (f"testo troppo corto ({len(text)} caratteri): la pagina probabilmente si carica con "
                        f"JavaScript o richiede un login")
    else:
        res["ok"] = True
    return res


def fetch_company_context(offer_url, links, org_url=""):
    """Cerca 1-2 pagine 'chi siamo / mission' sullo stesso sito. Ritorna (testo, [url usati])."""
    host = urlparse(offer_url).netloc
    cands, seen = [], {offer_url.split("#")[0]}

    def add(u, score):
        u = u.split("#")[0]
        if not u.startswith("http") or SKIP_EXT.search(u) or u in seen:
            return
        seen.add(u)
        cands.append((score, u))

    for href, txt in links:
        if not href or href.startswith(("mailto:", "tel:", "javascript:", "#")):
            continue
        full = urljoin(offer_url, href)
        if _root(urlparse(full).netloc) != _root(host) and not (org_url and _root(urlparse(full).netloc) == _root(urlparse(org_url).netloc)):
            continue
        hit_txt = ABOUT_RE.search(txt or "")
        hit_href = ABOUT_RE.search(urlparse(full).path)
        if hit_txt or hit_href:
            add(full, 0 if hit_txt else 1)
    cands.sort(key=lambda x: x[0])
    base = f"{urlparse(offer_url).scheme}://{host}"
    roots = [base] + ([org_url.rstrip("/")] if org_url.startswith("http") else [])
    guesses = []
    for r in roots:
        for g in ("/about", "/about-us", "/ueber-uns", "/unternehmen", "/company", "/chi-siamo", "/mission"):
            guesses.append(r + g)
    pages, used = [], []
    for _, u in cands[:4]:
        h, e = http_get(u, timeout=20)
        if h:
            t = html_to_text(h)[0]
            if len(t) >= 400:
                pages.append((u, t[:MAX_PAGE_CHARS]))
                used.append(u)
        if len(pages) >= 2:
            break
    if not pages:
        for u in guesses[:6]:
            if u in seen:
                continue
            h, e = http_get(u, timeout=15)
            if h:
                t = html_to_text(h)[0]
                if len(t) >= 400:
                    pages.append((u, t[:MAX_PAGE_CHARS]))
                    used.append(u)
                    break
    if not pages:
        for r in roots[:2]:
            h, e = http_get(r, timeout=20)
            if h:
                t = html_to_text(h)[0]
                if len(t) >= 400:
                    pages.append((r, t[:3000]))
                    used.append(r)
                    break
    if not pages:
        return "NOT AVAILABLE (no readable company page found)", []
    return "\n\n".join(f"SOURCE: {u}\n{t}" for u, t in pages), used


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    o = fetch_offer(sys.argv[1])
    print("OK" if o["ok"] else "PROBLEMA", o["error"], "| titolo:", o["title"], "| caratteri:", len(o["text"]))
    print(o["text"][:600])
    if o["ok"]:
        ctx, used = fetch_company_context(sys.argv[1], o["links"], o["org_url"])
        print("\n--- pagine azienda:", used)
        print(ctx[:600])
