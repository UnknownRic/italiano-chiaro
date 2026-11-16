#!/usr/bin/env python3
"""Controlli di scrittura per gli hook di Claude Code. Sono avvisi: non bloccano mai.

PostToolUse (Write|Edit su un file .md): passa il file a lint/chiaro_lint.py.
Se trova errori, scrive su stderr il testo e la riga di ogni errore (al
massimo MAX_HOOK_HITS) ed esce con 2, così il modello li vede. Su PostToolUse
l'uscita 2 è un avviso: lo strumento ha già scritto il file. Il controllo
salta i file interni dell'agente, come i file di memoria nella cartella di
configurazione di Claude. Imposta ITALIANO_CHIARO_LINT_EXCLUDE per saltare
altri percorsi.

Stop: legge `last_assistant_message`, controlla il registro della risposta
(niente grassetto, niente lineette) e restituisce un systemMessage solo se
la risposta lo viola. Esce sempre con 0, così la sessione non va in ciclo.

I due controlli saltano il testo che non è italiano.

Deriva da src/hooks/lint_hook.py di SimpleEnglish (AminBlg, MIT).
"""
import fnmatch
import json
import os
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "lint"))

MAX_HOOK_HITS = 12
CLAUDE_DIR = ".claude"
OPENERS = re.compile(
    r"^\s*(certo[,!.]|certamente|ottima domanda|assolutamente|perfetto[,!.]|hai (assolutamente |perfettamente )?ragione)", re.I)
CLOSERS = re.compile(
    r"(spero (di esserti stato|di esserle stato|che (questo|ciò) ti sia) utile|fammi sapere|resto a disposizione|non esitare a)", re.I)
# Parole comuni in italiano e rare in inglese.
ITALIAN_WORDS = {
    "il", "che", "non", "per", "della", "del", "di", "è", "una", "sono", "con", "gli",
    "nel", "alla", "questo", "più", "anche", "perché", "dei", "delle",
}


def load_linter():
    try:
        import chiaro_lint  # noqa: WPS433
        return chiaro_lint
    except Exception:  # noqa: BLE001
        return None


def strip_code(text):
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    return re.sub(r"`[^`]*`", " ", text)


def is_italian(text):
    """True se almeno il 6% delle parole è nella lista. Un testo italiano supera il 15%."""
    # shortcut: conteggio di parole comuni, non un rilevatore di lingua. Passa a una libreria se servono testi misti.
    words = re.findall(r"[a-zà-ÿ]+", strip_code(text).lower())
    hits = sum(1 for w in words if w in ITALIAN_WORDS)
    return hits >= max(1, round(0.06 * len(words)))


def absolute(path, cwd=None):
    """Rende il percorso assoluto. Lo strumento può passarlo relativo alla cartella della sessione."""
    return pathlib.Path(cwd or ".", pathlib.Path(path).expanduser()).absolute()


def variants(path):
    """Il percorso come è scritto e con i link simbolici risolti. Un'esclusione vale per le due forme."""
    return {pathlib.Path(os.path.normpath(path)), path.resolve()}


def excluded(target):
    """True per i file interni dell'agente e per i percorsi esclusi dall'utente."""
    config_dirs = variants(absolute(os.environ.get("CLAUDE_CONFIG_DIR") or f"~/{CLAUDE_DIR}"))
    raw = os.environ.get("ITALIANO_CHIARO_LINT_EXCLUDE", "").split(os.pathsep)
    patterns = [os.path.expanduser(p) for p in raw if p]
    for form in variants(target):
        if CLAUDE_DIR in form.parts or any(form.is_relative_to(d) for d in config_dirs):
            return True
        if any(fnmatch.fnmatch(str(form), p) for p in patterns):
            return True
    return False


def post_tool_use(event):
    path = (event.get("tool_input") or {}).get("file_path") or ""
    if not path.endswith(".md"):
        return 0
    target = absolute(path, event.get("cwd"))
    if excluded(target):
        return 0
    lint = load_linter()
    if lint is None:
        return 0
    try:
        text = target.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return 0
    if not is_italian(text):
        return 0
    detail = [h for h in lint.lint_detail(text, "descriptive") if h["level"] == "errore"]
    if not detail:
        return 0
    lines = [f"italiano-chiaro: {target.name} ha {len(detail)} violazioni."]
    for h in detail[:MAX_HOOK_HITS]:
        lines.append(f"  riga {h['line']}, {h['category']}: {h['text']}")
    if len(detail) > MAX_HOOK_HITS:
        lines.append(f"  e altre {len(detail) - MAX_HOOK_HITS} violazioni.")
    lines.append("Correggi queste violazioni nel file che hai appena scritto, poi continua.")
    sys.stderr.write("\n".join(lines) + "\n")
    return 2


def stop(event):
    reply = event.get("last_assistant_message") or ""
    if not is_italian(reply):
        return 0
    problems = []
    lint = load_linter()
    if lint is not None:
        c = lint.reader_check(reply)["counts"]
        for key, label in (("em_dash", "lineette"), ("bold_spans", "grassetti")):
            if c[key]:
                problems.append(f"{label}: {c[key]}")
        slop = lint.lint(strip_code(reply), "descriptive")["violations"].get("slop_word", 0)
        if slop:
            problems.append(f"parole slop: {slop}")
    if OPENERS.search(reply):
        problems.append("apertura di cortesia")
    if CLOSERS.search(reply):
        problems.append("chiusura di cortesia")
    if problems:
        print(json.dumps({"systemMessage": "italiano-chiaro, controllo della risposta: " + ", ".join(problems) + "."},
                         ensure_ascii=False))
    return 0


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")  # la console di Windows non è UTF-8
    try:
        event = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    except Exception:  # noqa: BLE001
        return 0
    try:
        name = event.get("hook_event_name", "")
        if name == "PostToolUse":
            return post_tool_use(event)
        if name == "Stop":
            return stop(event)
    except Exception:  # noqa: BLE001  hook di avviso: un errore non deve mai bloccare la sessione
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
