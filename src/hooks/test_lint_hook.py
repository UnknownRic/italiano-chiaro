import json, os, pathlib, subprocess, sys, tempfile
HERE = pathlib.Path(__file__).resolve().parent
HOOK = HERE / "lint_hook.py"
CLEAN = {"CLAUDE_CONFIG_DIR": "/inesistente/claude-config", "ITALIANO_CHIARO_LINT_EXCLUDE": ""}
SLOP = "Dovresti semplicemente utilizzare lo strumento robusto, rendendo il processo più facile per il team.\n"

def run(event, env=None):
    r = subprocess.run([sys.executable, str(HOOK)], input=json.dumps(event), capture_output=True, text=True,
                       encoding="utf-8", env={**os.environ, **CLEAN, **(env or {})})
    return r.returncode, r.stdout, r.stderr

def write(directory, name="note.md", text=SLOP):
    path = pathlib.Path(directory, name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return str(path)

def post(path, **event):
    return {"hook_event_name": "PostToolUse", "tool_name": "Write", "tool_input": {"file_path": path}, **event}

def symlink(link, target):
    """False dove il sistema non permette i link simbolici (Windows senza modalità sviluppatore)."""
    try:
        pathlib.Path(link).symlink_to(target)
        return True
    except OSError:
        return False

def test_post_tool_use_segnala_un_file_markdown_con_slop():
    with tempfile.TemporaryDirectory() as d:
        code, out, err = run(post(write(d)))
    assert code == 2 and "violazioni" in err, (code, err)

def test_post_tool_use_scrive_il_testo_e_la_riga():
    with tempfile.TemporaryDirectory() as d:
        code, out, err = run(post(write(d, text="# Titolo\n\nDovresti leggere il log. Non so perchè.\n")))
    assert code == 2, (code, err)
    assert "riga 3, conditional: Dovresti" in err, err
    assert "riga 3, spelling: perchè" in err, err

def test_post_tool_use_ignora_file_pulito_e_file_non_markdown():
    with tempfile.TemporaryDirectory() as d:
        assert run(post(write(d, text="Esegui la migrazione del database. Poi riavvia il servizio.\n")))[0] == 0
    assert run(post("/tmp/x.py"))[0] == 0

def test_post_tool_use_ignora_gli_avvisi():
    with tempfile.TemporaryDirectory() as d:
        assert run(post(write(d, text="Il percorso completo del file è nella guida.\n")))[0] == 0

def test_post_tool_use_salta_un_file_inglese():
    with tempfile.TemporaryDirectory() as d:
        text = "You should simply leverage the robust tool; it is seamless — really.\n"
        assert run(post(write(d, text=text)))[0] == 0

def test_post_tool_use_salta_la_cartella_di_configurazione_di_claude():
    with tempfile.TemporaryDirectory() as d:
        path = write(pathlib.Path(d, "projects", "repo", "memory"), "MEMORY.md")
        assert run(post(path))[0] == 2, "un file di memoria fuori dalla cartella di configurazione passa dal linter"
        assert run(post(path), env={"CLAUDE_CONFIG_DIR": d})[0] == 0

def test_post_tool_use_salta_una_cartella_dot_claude():
    with tempfile.TemporaryDirectory() as d:
        assert run(post(write(pathlib.Path(d, ".claude", "agent-memory", "reviewer"), "MEMORY.md")))[0] == 0

def test_post_tool_use_rispetta_i_glob_di_esclusione():
    with tempfile.TemporaryDirectory() as d:
        path = write(d)
        assert run(post(path))[0] == 2
        globs = os.pathsep.join(["~/nessun-file.md", f"{d}/*.md"])
        assert run(post(path), env={"ITALIANO_CHIARO_LINT_EXCLUDE": globs})[0] == 0

def test_post_tool_use_risolve_un_percorso_relativo_con_cwd():
    with tempfile.TemporaryDirectory() as d:
        write(d)
        assert run(post("note.md", cwd=d))[0] == 2

def test_post_tool_use_controlla_un_percorso_che_esce_da_dot_claude():
    with tempfile.TemporaryDirectory() as d:
        write(d)
        pathlib.Path(d, ".claude").mkdir()
        assert run(post(str(pathlib.Path(d, ".claude", "..", "note.md"))))[0] == 2

def test_post_tool_use_salta_un_link_verso_dot_claude():
    with tempfile.TemporaryDirectory() as d:
        link = pathlib.Path(d, "note.md")
        if symlink(link, write(pathlib.Path(d, ".claude"), "MEMORY.md")):
            assert run(post(str(link)))[0] == 0

def test_post_tool_use_salta_una_cartella_dot_claude_che_e_un_link():
    with tempfile.TemporaryDirectory() as d:
        write(pathlib.Path(d, "dotfiles"), "MEMORY.md")
        if symlink(pathlib.Path(d, ".claude"), pathlib.Path(d, "dotfiles")):
            assert run(post(str(pathlib.Path(d, ".claude", "MEMORY.md"))))[0] == 0

def test_stop_segnala_una_risposta_con_slop_e_non_blocca():
    reply = "Ottima domanda! " + "Questa è una frase robusta per il test. " * 7 + "Spero di esserti stato utile!"
    code, out, err = run({"hook_event_name": "Stop", "last_assistant_message": reply})
    assert code == 0 and "systemMessage" in out, (code, out)
    msg = json.loads(out)["systemMessage"]
    assert "apertura" in msg and "chiusura" in msg and "slop" in msg, msg

def test_stop_segnala_lineette_e_grassetto():
    code, out, err = run({"hook_event_name": "Stop", "last_assistant_message": "**Sì** — il disco è pieno e non c'è spazio per il log."})
    msg = json.loads(out)["systemMessage"]
    assert "lineette: 1" in msg and "grassetti: 1" in msg, msg

def test_stop_tace_su_una_risposta_buona():
    reply = "La build è fallita perché il disco era pieno. Libera 2 GB e riprova."
    code, out, err = run({"hook_event_name": "Stop", "last_assistant_message": reply})
    assert code == 0 and out.strip() == "", (code, out)

def test_stop_tace_su_una_risposta_inglese():
    reply = "Great question! This is a **robust** answer — I hope this helps."
    code, out, err = run({"hook_event_name": "Stop", "last_assistant_message": reply})
    assert code == 0 and out.strip() == "", (code, out)

def test_stdin_non_valido_esce_con_zero():
    r = subprocess.run([sys.executable, str(HOOK)], input="non json", capture_output=True, text=True)
    assert r.returncode == 0

if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok", name)
