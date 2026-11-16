#!/usr/bin/env python3
"""Controlla che i testi duplicati della repo siano allineati.

Esegui questo script prima di ogni push. La CI lo esegue a ogni push e pull request.

    python3 lint/check_numbers.py

Controlli:
- Il blocco delle regole è identico in prompts/prompt-di-sistema.md e in
  output-styles/italiano-chiaro.md, e SKILL.md contiene le stesse regole chiave.
- La versione coincide in SKILL.md, nei tre manifest e nel CHANGELOG.

Questa versione non pubblica metriche, quindi non c'è nessun numero da ricalcolare.
Deriva da evals/check_numbers.py di SimpleEnglish (AminBlg, MIT).
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
problems = []


def read(relative):
    return (ROOT / relative).read_text(encoding="utf-8").replace("\r\n", "\n")


def rule_block(text):
    """Il testo tra le prime due righe ---."""
    parts = re.split(r"^---[ \t]*$", text, flags=re.M)
    return parts[1].strip() if len(parts) >= 3 else text.strip()


def sync():
    prompt = rule_block(read("prompts/prompt-di-sistema.md"))
    style = re.sub(r"^---\n.*?\n---\n", "", read("output-styles/italiano-chiaro.md"), count=1, flags=re.S).strip()
    if prompt != style:
        problems.append("il blocco delle regole è diverso tra prompts/prompt-di-sistema.md e output-styles/italiano-chiaro.md")
    skill = read("skills/italiano-chiaro/SKILL.md")
    for phrase in ("Rispondi in prosa", "Niente lineette", "prima frase dà la risposta", "Prima la condizione",
                   "verifica che", "Non toccare", "solo al testo italiano"):
        for name, text in (("SKILL.md", skill), ("prompts/prompt-di-sistema.md", prompt)):
            if phrase.lower() not in text.lower():
                problems.append(f"in {name} manca la regola {phrase!r}")


def versions():
    v = {"SKILL.md": re.search(r'version: "([^"]+)"', read("skills/italiano-chiaro/SKILL.md")).group(1)}
    for f in (".claude-plugin/plugin.json", ".claude-plugin/marketplace.json", ".codex-plugin/plugin.json"):
        v[f] = re.search(r'"version":\s*"([^"]+)"', read(f)).group(1)
    v["CHANGELOG.md"] = re.search(r"^## ([0-9.]+)", read("CHANGELOG.md"), flags=re.M).group(1)
    if len(set(v.values())) != 1:
        problems.append(f"le versioni sono diverse: {v}")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sync()
    versions()
    if problems:
        print("DIFFERENZE")
        for p in problems:
            print(" -", p)
        return 1
    print("check_numbers OK: blocco delle regole e versioni sono allineati")
    return 0


if __name__ == "__main__":
    sys.exit(main())
