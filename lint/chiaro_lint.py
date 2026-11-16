#!/usr/bin/env python3
"""Contatore deterministico di violazioni per Italiano Chiaro.

Conta le violazioni meccaniche che una regex può trovare: lunghezza delle
frasi, condizionale, modali deboli, "si" impersonale, gerundio dopo la
virgola, nominalizzazioni, "andare a", congiunzioni col congiuntivo,
abbreviazioni, slop, burocratese, condizione in coda, lineette, punto e
virgola, rotazione dei sinonimi, ortografia, titoli con troppe maiuscole.

Limite noto: è un passaggio di regex, non un parser. Conta meno del vero
(nessuna analisi grammaticale) e può sbagliare i confini delle frasi in un
markdown insolito. I numeri sono confrontabili tra due testi passati dalla
stessa versione. Non sono un verdetto di conformità.

Ogni risultato ha un livello: "errore" o "avviso". Solo gli errori entrano
in violations_total e fanno fallire --gate.

Deriva da evals/ste_lint.py di SimpleEnglish (AminBlg, MIT).

Uso:
  python3 chiaro_lint.py --type procedural file.md
  cat testo.md | python3 chiaro_lint.py --type descriptive -
  python3 chiaro_lint.py --self-test
"""
import json
import pathlib
import re
import sys
from collections import Counter

HERE = pathlib.Path(__file__).resolve().parent
I = re.I

CONDITIONAL = re.compile(r"\b(dovr|potr|sar|vorr|avr)(ei|esti|ebbe|emmo|este|ebbero)\b", I)
WEAK_MODAL = re.compile(r"\b(si\s+consiglia|si\s+raccomanda|si\s+suggerisce|è\s+consigliabile|è\s+opportuno|eventualmente)\b", I)
IMPERSONAL_SI = re.compile(
    r"\bsi\s+(deve|devono|può|possono|prega|invita)\b|\b(viene|vengono)\s+\w+(at|ut|it)[oaie]\b", I)
GERUND = re.compile(r",\s*(\w+(?:ando|endo))\b", I)
# shortcut: lista chiusa di parole in -ando/-endo che non sono gerundi, da allungare quando il linter dà un falso positivo
NOT_GERUND = {
    "quando", "comando", "tremendo", "stupendo", "orrendo", "dividendo", "addendo",
    "reverendo", "rimando", "bando", "blando", "intendo", "prendo", "mando", "rendo",
    "vendo", "attendo",
}
NOMINALIZATION = re.compile(
    r"\beffettu\w*\s+(?:(?:la|il|lo|le|gli|i|un|una|uno)\b|l'|un')"
    r"|\b(?:proced|provved)(?:i|e|o|ere|ete|iamo|ono|erà|uto)\s+(?:(?:a|al|allo|alla|alle|ai|agli)\b|all')", I)
ANDARE_A = re.compile(r"\b(va|vanno|vai|andiamo|andate|andrà|andremo)\s+a\s+\w+(are|ere|ire)\b", I)
SUBJ_CONJ = re.compile(r"\b(affinch[éè]|qualora|bench[éè]|sebbene|purch[éè]|laddove)\b", I)
ABBREVIATION = re.compile(r"\b(?:es\.|p\.\s?es\.|ecc\.|etc\b\.?|cfr\.|c\.d\.|i\.e\.|e\.g\.)|\be/o\b", I)
SPELLING = re.compile(r"\bE'(?=\s)|\b(?:perchè|poichè|affinchè|benchè|finchè|purchè|nè|sè|pò|qual'è)\b", I)
DASH = re.compile(r"—|(?<!\d)–(?!\d)|(?<= )--(?= )|(?<=[^\s\d]{2}) - (?=[^\s\d]{2})")
TRAILING_COND = re.compile(r"\s(se|quando)\s", I)
# Prima di "se": domanda indiretta ("verifica se"), concessiva ("anche se"), coordinata ("e se").
NOT_COND_BEFORE = re.compile(
    r"\b(verific\w*|controll\w*|chied\w*|sapere|sai|ved\w+|decid\w+|indic\w+|anche|come|a|da|di|e|ma|o)$", I)
ROTATION_SETS = [
    ("verifica", re.compile(r"\b(verific|controll(?!er)|accert|assicur|conferm|convalid)\w*", I)),
    # "settaggio" sta in burocratese.tsv, non qui: una parola, una segnalazione.
    ("configurazione", re.compile(r"\b(config|configurazion\w*|impostazion\w*)\b", I)),
]
LIMITS = {"procedural": 20, "descriptive": 25}
ERRORS = [
    "sentence_over_limit", "conditional", "weak_modal", "gerund_clause", "nominalization",
    "andare_a", "subjunctive_conjunction", "abbreviation", "slop_word", "bureaucratese",
    "trailing_condition", "em_dash", "semicolon", "spelling",
]
WARNINGS = ["impersonal_si", "synonym_rotation", "title_case", "slop_word", "bureaucratese"]


def load_tsv(name):
    """Righe "regex<TAB>sostituzione<TAB>livello" -> {livello: pattern}. Uno spazio vale \\s+."""
    rows = {"errore": [], "avviso": []}
    path = HERE / name
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            cols = line.split("\t")
            if len(cols) == 3 and not line.startswith("#"):
                rows[cols[2].strip()].append("(?:%s)" % cols[0].strip().replace(" ", r"\s+"))
    return {lvl: re.compile(r"\b(?:%s)\b" % "|".join(rx), I) for lvl, rx in rows.items() if rx}


TERM_LISTS = [("slop_word", load_tsv("slop_it.tsv")), ("bureaucratese", load_tsv("burocratese.tsv"))]


def blank(m):
    """Sostituisce un blocco e tiene gli a capo, così i numeri di riga restano giusti."""
    return "\n" * m.group(0).count("\n") or " "


def normalize(text):
    return text.replace("\r\n", "\n").replace("’", "'")


def strip_code(text):
    text = re.sub(r"\A---\n.*?\n---\n", blank, text, flags=re.S)  # frontmatter YAML
    text = re.sub(r"```.*?```", blank, text, flags=re.S)
    text = re.sub(r"`[^`\n]+`", " CODESPAN ", text)  # conta come una parola (IC-8.4)
    text = re.sub(r"^#+\s.*$", " ", text, flags=re.M)  # i titoli sono esenti
    text = re.sub(r"https?://\S+", " URL ", text)
    text = re.sub(r"^\s*\|[\s:|-]+\|\s*$", " ", text, flags=re.M)  # separatori di tabella
    text = re.sub(r"^\s*\|(.*)\|\s*$", lambda m: ". ".join(c.strip() for c in m.group(1).split("|") if c.strip()) + ". ", text, flags=re.M)
    return text


DOT = "․"  # segnaposto per il punto di un'abbreviazione
ABBR_ALWAYS = re.compile(r"\b(art|pag|dott|sig|n|p|cap|fig|cfr)\.(?=\s)", I)
ABBR_MID = re.compile(r"\b(es|ecc)\.(?=\s+[a-zà-ÿ0-9])", I)


def sentences(text):
    text = ABBR_ALWAYS.sub(lambda m: m.group(1) + DOT, text)
    text = ABBR_MID.sub(lambda m: m.group(1) + DOT, text)
    # Ogni voce di elenco diventa una frase a sé.
    text = re.sub(r"^\s*([-*]|\d+\.)\s+(.*?)([.!?:])?\s*$", lambda m: m.group(2) + (m.group(3) or ".") + " ", text, flags=re.M)
    parts = re.split(r"(?<=[.!?:])\s+", text)
    return [p.strip().replace(DOT, ".") for p in parts if len(p.strip().split()) >= 2]


def trailing_cond(s):
    if re.match(r"(se|quando)\b", s, I):
        return False
    for m in TRAILING_COND.finditer(s):
        before = s[s.rfind("\n", 0, m.start()) + 1:m.start()]
        # Una virgola dopo la condizione vuol dire che il comando segue: "Poi, se X, fai Y."
        if len(before) >= 4 and "," not in s[m.end():] and not NOT_COND_BEFORE.search(before.rstrip(" ,")):
            return True
    return False


def title_case_hits(text):
    """Titoli con 2+ parole maiuscole oltre la prima. Le sigle (API, HTTP) non contano."""
    out = []
    raw = re.sub(r"```.*?```", blank, text, flags=re.S)
    for m in re.finditer(r"^#+\s+(.*)$", raw, flags=re.M):
        words = re.sub(r"`[^`]*`", " ", m.group(1)).split()[1:]
        if sum(1 for w in words if re.match(r"[A-ZÀ-Ý][a-zà-ÿ]", w)) >= 2:
            out.append({"category": "title_case", "level": "avviso", "text": m.group(1).strip(),
                        "line": raw.count("\n", 0, m.start()) + 1})
    return out


def lint_detail(text, text_type):
    """Ogni risultato con categoria, livello, testo trovato e numero di riga."""
    text = normalize(text)
    body = strip_code(text)
    limit = LIMITS[text_type]
    hits = title_case_hits(text)

    def add(category, start, snippet, level="errore"):
        snippet = snippet.strip()
        if len(snippet) > 80:
            snippet = snippet[:80] + "…"
        hits.append({"category": category, "level": level, "text": snippet,
                     "line": body.count("\n", 0, start) + 1})

    pos = 0
    for s in sentences(body):
        found = body.find(s, pos)
        pos = found if found != -1 else pos
        if len(s.split()) > limit:
            add("sentence_over_limit", pos, s)
        if text_type == "procedural" and trailing_cond(s):
            add("trailing_condition", pos, s)
        pos += max(len(s), 1)

    simple = [
        ("conditional", CONDITIONAL, "errore"), ("weak_modal", WEAK_MODAL, "errore"),
        ("impersonal_si", IMPERSONAL_SI, "avviso"), ("nominalization", NOMINALIZATION, "errore"),
        ("andare_a", ANDARE_A, "errore"), ("subjunctive_conjunction", SUBJ_CONJ, "errore"),
        ("abbreviation", ABBREVIATION, "errore"), ("spelling", SPELLING, "errore"),
        ("em_dash", DASH, "errore"), ("semicolon", re.compile(";"), "errore"),
    ]
    for category, rx, level in simple:
        for m in rx.finditer(body):
            add(category, m.start(), m.group(0), level)
    for m in GERUND.finditer(body):
        if m.group(1).lower() not in NOT_GERUND:
            add("gerund_clause", m.start(), m.group(0))
    for category, patterns in TERM_LISTS:
        for level, rx in patterns.items():
            for m in rx.finditer(body):
                add(category, m.start(), m.group(0), level)
    for name, rx in ROTATION_SETS:
        seen = {}
        for m in rx.finditer(body):
            seen.setdefault(m.group(1).lower()[:7], m)
        for m in list(seen.values())[1:]:
            add("synonym_rotation", m.start(), "%s (%s)" % (m.group(0), name), "avviso")

    return sorted(hits, key=lambda h: h["line"])


def lint(text, text_type):
    hits = lint_detail(text, text_type)
    sents = sentences(strip_code(normalize(text)))
    lengths = [len(s.split()) for s in sents]
    errors = Counter(h["category"] for h in hits if h["level"] == "errore")
    warns = Counter(h["category"] for h in hits if h["level"] == "avviso")
    words = max(1, len(strip_code(normalize(text)).split()))
    total = sum(errors.values())
    return {
        "type": text_type,
        "words": words,
        "sentences": len(sents),
        "mean_sentence_words": round(sum(lengths) / max(1, len(lengths)), 1),
        "longest_sentence_words": max(lengths, default=0),
        "violations": {c: errors.get(c, 0) for c in ERRORS},
        "violations_total": total,
        "violations_per_100w": round(100.0 * total / words, 2),
        "warnings": {c: warns.get(c, 0) for c in WARNINGS},
        "warnings_total": sum(warns.values()),
    }


BOLD = re.compile(r"\*\*[^*\n]+\*\*")
HEADER = re.compile(r"^#{1,6}\s", re.M)
BULLET = re.compile(r"^\s*([-*+]|\d+[.)])\s", re.M)


def reader_check(text):
    """Quello che un lettore vede in una risposta in chat. "sentences" è un dato, non un limite."""
    text = normalize(text)
    prose = re.sub(r"```.*?```", " ", text, flags=re.S)
    prose = re.sub(r"`[^`\n]+`", " CODESPAN ", prose)
    prose_no_md = re.sub(r"^\s*(#{1,6}\s|[-*+]\s|\d+[.)]\s|\|)", "", prose, flags=re.M)
    prose_no_md = re.sub(r"^\s*[\s:|-]+$", "", prose_no_md, flags=re.M)
    sents = [p for p in re.split(r"(?<=[.!?])[\"')\]]*\s+|\n+", prose_no_md) if len(p.strip().split()) >= 2]
    counts = {
        "sentences": len(sents),
        "em_dash": len(DASH.findall(prose)),
        "bold_spans": len(BOLD.findall(prose)),
        "headers": len(HEADER.findall(prose)),
        "bullets": len(BULLET.findall(prose)),
    }
    visible = counts["em_dash"] + counts["bold_spans"] + counts["headers"] + counts["bullets"]
    return {"type": "reply", "words": max(1, len(prose_no_md.split())), "counts": counts, "visible_total": visible}


CLEAN_FIXTURE = """Il sistema riprova in automatico un caricamento fallito. Questo processo mantiene i dati corretti.

Se gli errori continuano, verifica che le credenziali siano corrette. Esegui il comando. Verifica se la porta è aperta. Poi, se la build non riesce, leggi il log all'art. 5 della guida. Se il problema continua, contatta l'assistenza."""

DIRTY_FIXTURE = """## Errori Di Connessione Frequenti

Sfruttando il nostro robusto meccanismo di retry, i caricamenti falliti vengono ritentati in automatico, garantendo che l'integrità dei dati sia mantenuta durante tutto il processo che è stato progettato per gestire anche le interruzioni di rete più difficili.
Dovresti controllare le credenziali; si consiglia anche di verificare le impostazioni, es. il timeout della config.
Si deve effettuare la verifica della porta e procedere all'installazione — poi andiamo a configurare il client.
Qualora il problema persista, al fine di risolverlo contatta l'assistenza e/o riavvia il servizio se serve.
Non so perchè il servizio è lento.
"""

CODE_FIXTURE = """Esegui il comando:

```
dovresti; controllare — e/o perchè
## Titolo Finto Nel Codice
```

Leggi la pagina https://example.com/dovrebbe;qualora e usa `dovrebbe; e/o`.
"""

# Solo le prime tre lineette uniscono due affermazioni.
DASH_FIXTURE = """Il deploy è fallito — il disco era pieno.
Il caricamento è fallito -- il token era scaduto.
Il tentativo è fallito - la porta era chiusa.
Non usare --force in produzione.
La finestra è di 5 - 10 minuti.
L'intervallo è 5–10 minuti, nella stagione 2024–2025.
Usa il flag `--config sqlpipe.yaml`.
"""


def self_test():
    clean = lint(CLEAN_FIXTURE, "procedural")
    assert clean["violations_total"] == 0 and clean["warnings_total"] == 0, lint_detail(CLEAN_FIXTURE, "procedural")
    dirty = lint(DIRTY_FIXTURE, "procedural")
    for category in ERRORS:
        assert dirty["violations"][category] >= 1, (category, dirty)
    for category in WARNINGS:
        assert dirty["warnings"][category] >= 1 or category == "bureaucratese", (category, dirty)
    assert dirty["violations"]["semicolon"] == 1, dirty
    code = lint(CODE_FIXTURE, "procedural")
    assert code["violations_total"] == 0 and code["warnings_total"] == 0, lint_detail(CODE_FIXTURE, "procedural")
    assert lint(DASH_FIXTURE, "procedural")["violations"]["em_dash"] == 3
    # Tutte le persone del condizionale, e nessun falso positivo sul passato remoto.
    assert lint("Potresti farlo. Sarebbero due. Vorremmo un test.", "descriptive")["violations"]["conditional"] == 3
    assert lint("Il carico crebbe molto.", "descriptive")["violations"]["conditional"] == 0
    # "Inoltre" non è "inoltrare", e "controller" non è "controllare".
    assert lint("Inoltre il controller verifica la coda.", "descriptive")["warnings_total"] == 0
    assert lint("Inoltre il controller verifica la coda.", "descriptive")["violations_total"] == 0
    # La condizione in coda vale solo nel testo procedurale.
    assert lint("Riavvia il servizio se serve.", "descriptive")["violations"]["trailing_condition"] == 0
    # Una cella di tabella è un'unità a sé, e il numero di riga resta giusto dopo un blocco di codice.
    cell = lint("| Colonna | Valore |\n|---|---|\n| Dovresti riavviare | ok |\n", "descriptive")["violations"]
    assert cell["conditional"] == 1 and cell["sentence_over_limit"] == 0, cell
    assert lint_detail("```\na\nb\n```\nÈ lento; riprova.\n", "descriptive")[0]["line"] == 5
    assert lint("---\nname: x\ndescription: dovresti; e/o\n---\nTesto pulito qui.\n", "descriptive")["violations_total"] == 0
    assert lint("a " * 30, "descriptive")["violations"]["sentence_over_limit"] == 1
    assert sentences("- Allenta i bulloni.\n- Poi continua") == ["Allenta i bulloni.", "Poi continua."]
    r = reader_check("**Sì** — è grave.\n\n## Perché\n- Il ritardo cresce.\n- Gli utenti aspettano.\n\nLeggi il log. Poi scala.")["counts"]
    assert (r["em_dash"], r["bold_spans"], r["headers"], r["bullets"]) == (1, 1, 1, 2), r
    assert reader_check("Sì. È grave perché il ritardo cresce.")["visible_total"] == 0
    print("self-test OK:", dirty["violations_total"], "errori e", dirty["warnings_total"],
          "avvisi nel testo sporco, 0 nel testo pulito")


USAGE = "uso: chiaro_lint.py [--type procedural|descriptive|reply] [--gate] [--detail] (FILE|-) | --self-test"


def main():
    args = sys.argv[1:]
    if "--self-test" in args:
        self_test()
        return 0
    flags = {f: f in args for f in ("--gate", "--detail")}
    args = [a for a in args if a not in flags]
    text_type = "descriptive"
    if "--type" in args:
        i = args.index("--type")
        if i + 1 >= len(args):
            sys.exit("manca il valore dopo --type\n" + USAGE)
        text_type = args[i + 1]
        del args[i:i + 2]
    if text_type != "reply" and text_type not in LIMITS:
        sys.exit("--type %r sconosciuto\n%s" % (text_type, USAGE))
    if len(args) != 1:
        sys.exit(USAGE)
    if args[0] == "-":
        text = sys.stdin.buffer.read().decode("utf-8")
    else:
        try:
            text = pathlib.Path(args[0]).read_text(encoding="utf-8")
        except OSError as err:
            sys.exit(str(err))
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # la console di Windows non è UTF-8
    report = reader_check(text) if text_type == "reply" else lint(text, text_type)
    if flags["--detail"] and text_type != "reply":
        report["detail"] = lint_detail(text, text_type)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    total = report["visible_total"] if text_type == "reply" else report["violations_total"]
    return 1 if flags["--gate"] and total else 0


if __name__ == "__main__":
    sys.exit(main())
