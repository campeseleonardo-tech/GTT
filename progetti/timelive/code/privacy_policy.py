"""
privacy_policy.py
================================================================================
PERSONAL DATA VAULT — Online/Offline Privacy Policy
================================================================================

Questo modulo definisce la policy di privacy per controllare quali dati
possono lasciare la macchina locale quando si usa un backend LLM cloud
(come ClaudeAPIClient o TogetherAIClient in llm_bridge.py).

LIVELLI:
- L0 (default): nulla lascia la macchina. Solo backend locali (Ollama).
- L1: la domanda dell'utente e le descrizioni delle tabelle (schema compatto
  o descrizioni complete da describe_table) possono essere inviate al cloud.
  I risultati delle query (righe reali con dati personali) NON lasciano la macchina.
- L2: oltre a L1, anche i risultati delle query possono lasciare la macchina,
  MA le colonne marcate come sensitive=True in ColumnSpec vengono redatte
  (sostituite con "[omesso]") prima dell'invio.

API PRINCIPALE:
- Policy(level, per_domain_overrides=None)
    - allows(kind) -> bool: kind in {"question", "table_descriptions", "query_results"}
    - redact_rows(columns, rows) -> list[dict]: columns è una lista di dict
      {"name": str, "sensitive": bool}, rows è una lista di dict {col: val}.
      Restituisce le righe con i valori delle colonne sensitive sostituiti.

- load_policy(config_dict) -> Policy:
    Legge una sezione "privacy" dal dizionario di configurazione.
    Formato JSON atteso:
    {
        "privacy": {
            "level": 0 | 1 | 2,              # obbligatorio se presente
            "per_domain_overrides": {        # opzionale
                "nome_dominio": 0 | 1 | 2
            }
        }
    }
    Se la sezione "privacy" manca o level manca, default = L0 (più sicuro).
    Se per_domain_overrides manca, nessun override per dominio.

Self-test sotto __main__ con dati sintetici.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


class Policy:
    """
    Policy di privacy per il Personal Data Vault.

    Controlla quali tipi di dati possono essere inviati a un backend cloud
    e applica la redazione delle colonne sensibili quando necessario.
    """

    # Livelli di policy
    L0 = 0  # nulla esce
    L1 = 1  # domanda + descrizioni tabelle
    L2 = 2  # domanda + descrizioni + risultati query (con redazione sensitive)

    _KINDS = ("question", "table_descriptions", "query_results")

    def __init__(
        self,
        level: int,
        per_domain_overrides: Optional[Dict[str, int]] = None
    ) -> None:
        """
        Inizializza la policy.

        Args:
            level: Livello globale (0, 1, 2).
            per_domain_overrides: Dizionario opzionale {dominio: livello}
                per sovrascrivere il livello per domini specifici.
                Il dominio corrisponde al prefisso della tabella (es. "chessdotcom",
                "spotify", "money", "instagram") prima del primo underscore.
        """
        if level not in (self.L0, self.L1, self.L2):
            raise ValueError(f"Livello policy non valido: {level}. Deve essere 0, 1 o 2.")

        self._level = level
        self._overrides = per_domain_overrides or {}

        # Valida gli override
        for domain, lvl in self._overrides.items():
            if lvl not in (self.L0, self.L1, self.L2):
                raise ValueError(
                    f"Override per dominio '{domain}': livello non valido {lvl}. "
                    f"Deve essere 0, 1 o 2."
                )

    @property
    def level(self) -> int:
        return self._level

    @property
    def per_domain_overrides(self) -> Dict[str, int]:
        return dict(self._overrides)

    def _get_level_for_domain(self, domain: Optional[str] = None) -> int:
        """Restituisce il livello effettivo per un dominio (con override se presente)."""
        if domain and domain in self._overrides:
            return self._overrides[domain]
        return self._level

    def allows(self, kind: str, domain: Optional[str] = None) -> bool:
        """
        Verifica se un tipo di dato può lasciare la macchina per il dominio dato.

        Args:
            kind: Uno di "question", "table_descriptions", "query_results".
            domain: Dominio opzionale (es. "spotify", "chessdotcom") per applicare
                override per dominio. Se None, usa il livello globale.

        Returns:
            True se il dato può essere inviato, False altrimenti.

        Raises:
            ValueError: se kind non è valido.
        """
        if kind not in self._KINDS:
            raise ValueError(
                f"Kind non valido: {kind!r}. Valori ammessi: {self._KINDS}"
            )

        level = self._get_level_for_domain(domain)

        if kind == "question":
            return level >= self.L1
        elif kind == "table_descriptions":
            return level >= self.L1
        elif kind == "query_results":
            return level >= self.L2

        return False  # non raggiunto

    def redact_rows(
        self,
        columns: List[Dict[str, Any]],
        rows: List[Dict[str, Any]],
        domain: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Redige le righe sostituendo i valori delle colonne sensitive con "[omesso]".

        La redazione viene applicata SOLO se il livello effettivo per il dominio
        è L2 (o superiore). A L0/L1 questa funzione non dovrebbe essere chiamata
        perché allows("query_results") sarebbe False, ma per sicurezza restituisce
        le righe non modificate se il livello non è L2.

        Args:
            columns: Lista di dizionari {"name": str, "sensitive": bool, ...}
                che descrivono le colonne (come da ColumnSpec di ingest_engine).
            rows: Lista di dizionari {nome_colonna: valore} rappresentanti le righe.
            domain: Dominio opzionale per applicare override per dominio.

        Returns:
            Nuova lista di righe con i valori delle colonne sensitive redatti
            (se level >= L2 per il dominio), altrimenti le righe originali.
        """
        level = self._get_level_for_domain(domain)

        # Se il livello non permette l'invio di risultati, non redigiamo
        # (il chiamante non dovrebbe inviare i dati comunque)
        if level < self.L2:
            return [dict(row) for row in rows]

        # Identifica i nomi delle colonne sensibili
        sensitive_names = {
            col["name"] for col in columns
            if col.get("sensitive") is True
        }

        if not sensitive_names:
            return [dict(row) for row in rows]

        redacted_rows = []
        for row in rows:
            new_row = dict(row)
            for col_name in sensitive_names:
                if col_name in new_row:
                    new_row[col_name] = "[omesso]"
            redacted_rows.append(new_row)

        return redacted_rows


def load_policy(config_dict: Dict[str, Any]) -> Policy:
    """
    Carica una Policy da un dizionario di configurazione.

    Cerca una sezione "privacy" nel dizionario. Formato atteso:

    {
        "privacy": {
            "level": 0 | 1 | 2,              # obbligatorio se sezione presente
            "per_domain_overrides": {        # opzionale
                "nome_dominio": 0 | 1 | 2
            }
        }
    }

    Esempio completo:
    {
        "privacy": {
            "level": 1,
            "per_domain_overrides": {
                "spotify": 2,
                "money": 0
            }
        }
    }

    Se la sezione "privacy" manca, o se "level" manca al suo interno,
    restituisce una Policy L0 (la più sicura).

    Args:
        config_dict: Dizionario di configurazione (es. caricato da config.json).

    Returns:
        Istanza di Policy configurata.
    """
    privacy_section = config_dict.get("privacy")

    if not privacy_section or not isinstance(privacy_section, dict):
        # Nessuna sezione privacy -> default sicuro L0
        return Policy(Policy.L0)

    level = privacy_section.get("level")
    if level is None or not isinstance(level, int):
        # level mancante o non intero -> default sicuro L0
        return Policy(Policy.L0)

    overrides = privacy_section.get("per_domain_overrides")
    if overrides is not None and not isinstance(overrides, dict):
        # overrides presente ma non è un dict -> ignoriamo gli override
        overrides = None

    return Policy(level, overrides)


# ==============================================================================
# SELF-TEST (solo dati sintetici)
# ==============================================================================

if __name__ == "__main__":
    import sys

    def _print_test(name: str, passed: bool) -> None:
        status = "PASS" if passed else "FAIL"
        print(f"{status}: {name}")
        if not passed:
            sys.exit(1)

    # Test 1: Policy L0 non permette nulla
    p0 = Policy(Policy.L0)
    _print_test("L0: allows question -> False", p0.allows("question") is False)
    _print_test("L0: allows table_descriptions -> False", p0.allows("table_descriptions") is False)
    _print_test("L0: allows query_results -> False", p0.allows("query_results") is False)

    # Test 2: Policy L1 permette question e table_descriptions, non query_results
    p1 = Policy(Policy.L1)
    _print_test("L1: allows question -> True", p1.allows("question") is True)
    _print_test("L1: allows table_descriptions -> True", p1.allows("table_descriptions") is True)
    _print_test("L1: allows query_results -> False", p1.allows("query_results") is False)

    # Test 3: Policy L2 permette tutto
    p2 = Policy(Policy.L2)
    _print_test("L2: allows question -> True", p2.allows("question") is True)
    _print_test("L2: allows table_descriptions -> True", p2.allows("table_descriptions") is True)
    _print_test("L2: allows query_results -> True", p2.allows("query_results") is True)

    # Test 4: Override per dominio
    p_override = Policy(Policy.L1, per_domain_overrides={"spotify": Policy.L2, "money": Policy.L0})
    _print_test("Override: spotify L2 -> allows query_results True", p_override.allows("query_results", "spotify") is True)
    _print_test("Override: money L0 -> allows question False", p_override.allows("question", "money") is False)
    _print_test("Override: dominio sconosciuto usa livello globale L1", p_override.allows("question", "chessdotcom") is True)
    _print_test("Override: dominio sconosciuto query_results False (globale L1)", p_override.allows("query_results", "chessdotcom") is False)

    # Test 5: redazione righe (L2)
    columns = [
        {"name": "user_id", "sensitive": True},
        {"name": "track_name", "sensitive": False},
        {"name": "artist", "sensitive": False},
        {"name": "email", "sensitive": True},
    ]
    rows = [
        {"user_id": "user123", "track_name": "Bohemian Rhapsody", "artist": "Queen", "email": "leo@example.com"},
        {"user_id": "user456", "track_name": "Imagine", "artist": "John Lennon", "email": "john@example.com"},
    ]

    redacted = p2.redact_rows(columns, rows, domain="spotify")
    expected_redacted = [
        {"user_id": "[omesso]", "track_name": "Bohemian Rhapsody", "artist": "Queen", "email": "[omesso]"},
        {"user_id": "[omesso]", "track_name": "Imagine", "artist": "John Lennon", "email": "[omesso]"},
    ]
    _print_test("L2: redact_rows redige colonne sensitive", redacted == expected_redacted)

    # Test 6: redazione righe (L1 - non redige perché livello insufficiente)
    redacted_l1 = p1.redact_rows(columns, rows, domain="spotify")
    _print_test("L1: redact_rows NON redige (livello < L2)", redacted_l1 == rows)

    # Test 7: redazione righe senza colonne sensitive
    columns_no_sensitive = [
        {"name": "track_name", "sensitive": False},
        {"name": "artist", "sensitive": False},
    ]
    rows_no_sensitive = [
        {"track_name": "Bohemian Rhapsody", "artist": "Queen"},
    ]
    redacted_none = p2.redact_rows(columns_no_sensitive, rows_no_sensitive)
    _print_test("Nessuna colonna sensitive: righe invariate", redacted_none == rows_no_sensitive)

    # Test 8: load_policy senza sezione privacy -> L0
    config_empty = {}
    p_from_empty = load_policy(config_empty)
    _print_test("load_policy: config vuoto -> L0", p_from_empty.level == Policy.L0)

    # Test 9: load_policy con sezione privacy ma senza level -> L0
    config_no_level = {"privacy": {"per_domain_overrides": {"spotify": 2}}}
    p_no_level = load_policy(config_no_level)
    _print_test("load_policy: privacy senza level -> L0", p_no_level.level == Policy.L0)

    # Test 10: load_policy con level valido
    config_valid = {"privacy": {"level": 2, "per_domain_overrides": {"money": 0}}}
    p_valid = load_policy(config_valid)
    _print_test("load_policy: level 2 + override money=0", p_valid.level == Policy.L2)
    _print_test("load_policy: override money L0 -> allows query_results False", p_valid.allows("query_results", "money") is False)
    _print_test("load_policy: override money L0 -> allows question False", p_valid.allows("question", "money") is False)

    # Test 11: allows con kind non valido solleva ValueError
    try:
        p2.allows("invalid_kind")
        _print_test("allows: kind invalido solleva ValueError", False)
    except ValueError:
        _print_test("allows: kind invalido solleva ValueError", True)

    # Test 12: costruttore con livello invalido solleva ValueError
    try:
        Policy(5)
        _print_test("Policy: livello invalido solleva ValueError", False)
    except ValueError:
        _print_test("Policy: livello invalido solleva ValueError", True)

    # Test 13: costruttore con override invalido solleva ValueError
    try:
        Policy(Policy.L1, {"spotify": 5})
        _print_test("Policy: override invalido solleva ValueError", False)
    except ValueError:
        _print_test("Policy: override invalido solleva ValueError", True)

    print("\nTutti i test superati!")
    sys.exit(0)
