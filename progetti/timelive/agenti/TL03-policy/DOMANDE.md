dominio per override: prefisso tabella (es. "spotify") o nome dominio formale? | opzioni: prefisso tabella / nome formale / entrambi | scelta: prefisso tabella | dove: privacy_policy.py _get_level_for_domain
formato "[omesso]" fisso o configurabile? | opzioni: fisso / configurabile via Policy | scelta: fisso | dove: privacy_policy.py redact_rows
integrazione in llm_bridge.py: chi istanzia Policy e dove si applica? | opzioni: in run_query / nel client LLM / esternamente | scelta: da decidere da Leo | dove: llm_bridge.py (non toccato)
load_policy: supportare anche file path oltre a dict? | opzioni: solo dict / dict + path / solo path | scelta: solo dict | dove: privacy_policy.py load_policy
