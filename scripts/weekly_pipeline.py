#!/usr/bin/env python3
"""
Weekly Content Pipeline

Automatisierter Workflow:
1. Nächstes Thema aus topics/queue.txt lesen
2. /research [Thema] via Claude CLI ausführen
3. /write [Thema] via Claude CLI ausführen
4. Artikel direkt auf WordPress veröffentlichen
5. Thema als erledigt markieren

Verwendung:
    python3 scripts/weekly_pipeline.py
    python3 scripts/weekly_pipeline.py --dry-run   # Kein WordPress-Upload
    python3 scripts/weekly_pipeline.py --topic "Brandschutzhelfer Kurs Mannheim"  # Thema überschreiben
"""

import argparse
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

# Repo-Root ermitteln (Elternverzeichnis dieses Scripts)
REPO_ROOT = Path(__file__).parent.parent.resolve()
QUEUE_FILE = REPO_ROOT / "topics" / "queue.txt"
PROCESSED_FILE = REPO_ROOT / "topics" / "processed.txt"
DRAFTS_DIR = REPO_ROOT / "drafts"
RESEARCH_DIR = REPO_ROOT / "research"


def log(msg: str):
    print(f"[weekly-pipeline] {msg}", flush=True)


def read_next_topic() -> str | None:
    """Liest das nächste offene Thema aus queue.txt."""
    if not QUEUE_FILE.exists():
        log(f"FEHLER: {QUEUE_FILE} nicht gefunden.")
        return None

    lines = QUEUE_FILE.read_text(encoding="utf-8").splitlines()
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            return stripped
    return None


def mark_topic_done(topic: str):
    """Verschiebt das Thema von queue.txt nach processed.txt."""
    lines = QUEUE_FILE.read_text(encoding="utf-8").splitlines()
    remaining = [l for l in lines if l.strip() != topic]
    QUEUE_FILE.write_text("\n".join(remaining) + "\n", encoding="utf-8")

    today = date.today().isoformat()
    with open(PROCESSED_FILE, "a", encoding="utf-8") as f:
        f.write(f"{today}: {topic}\n")

    log(f"Thema als erledigt markiert: '{topic}'")


def run_claude_command(prompt: str, timeout: int = 600) -> str:
    """Führt einen Claude-CLI-Befehl aus und gibt die Ausgabe zurück."""
    log(f"Führe Claude-Befehl aus: {prompt[:80]}...")

    result = subprocess.run(
        ["claude", "-p", prompt],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=timeout,
        env={**os.environ, "CLAUDE_CODE_HEADLESS": "1"},
    )

    if result.returncode != 0:
        log(f"Claude-Befehl fehlgeschlagen (Exit {result.returncode}):")
        log(result.stderr[:500] if result.stderr else "(keine Fehlerausgabe)")
        raise RuntimeError(f"Claude-Befehl fehlgeschlagen: {prompt[:60]}")

    return result.stdout


def find_latest_file(directory: Path, pattern: str = "*.md") -> Path | None:
    """Findet die zuletzt geänderte Datei in einem Verzeichnis."""
    files = list(directory.glob(pattern))
    if not files:
        return None
    return max(files, key=lambda f: f.stat().st_mtime)


def publish_to_wordpress(draft_file: Path, dry_run: bool = False) -> dict:
    """Veröffentlicht die Datei direkt auf WordPress."""
    publisher_script = REPO_ROOT / "data_sources" / "modules" / "wordpress_publisher.py"

    if dry_run:
        log(f"[DRY-RUN] Würde veröffentlichen: {draft_file.name}")
        return {"dry_run": True, "file": str(draft_file)}

    log(f"Veröffentliche auf WordPress: {draft_file.name}")

    env_file = REPO_ROOT / "data_sources" / "config" / ".env"
    env = {**os.environ}

    # .env laden falls vorhanden
    if env_file.exists():
        from dotenv import load_dotenv
        load_dotenv(env_file)
        env = {**os.environ}

    result = subprocess.run(
        [
            sys.executable,
            str(publisher_script),
            str(draft_file),
            "--type", "post",
            "--status", "publish",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=120,
        env=env,
    )

    if result.returncode != 0:
        log("WordPress-Veröffentlichung fehlgeschlagen:")
        log(result.stderr[:500] if result.stderr else result.stdout[:500])
        raise RuntimeError("WordPress-Upload fehlgeschlagen")

    log("WordPress-Veröffentlichung erfolgreich!")
    log(result.stdout)
    return {"success": True, "output": result.stdout}


def main():
    parser = argparse.ArgumentParser(description="Wöchentliche SEO-Content-Pipeline")
    parser.add_argument("--dry-run", action="store_true", help="Kein WordPress-Upload")
    parser.add_argument("--topic", help="Thema manuell überschreiben (überspringt Queue)")
    parser.add_argument(
        "--skip-research",
        action="store_true",
        help="Recherche überspringen, direkt schreiben",
    )
    args = parser.parse_args()

    log("=== Wöchentliche Content-Pipeline gestartet ===")

    # Thema bestimmen
    if args.topic:
        topic = args.topic
        log(f"Thema manuell gesetzt: '{topic}'")
        skip_queue_update = True
    else:
        topic = read_next_topic()
        skip_queue_update = False
        if not topic:
            log("Keine offenen Themen in topics/queue.txt – Pipeline beendet.")
            sys.exit(0)

    log(f"Thema dieser Woche: '{topic}'")

    # Schritt 1: Recherche
    if not args.skip_research:
        log("--- Schritt 1: Keyword-Recherche ---")
        research_prompt = f"/research {topic}"
        run_claude_command(research_prompt, timeout=600)
        log("Recherche abgeschlossen.")

        research_file = find_latest_file(RESEARCH_DIR)
        if research_file:
            log(f"Research-Brief: {research_file.name}")
    else:
        log("Recherche übersprungen (--skip-research).")

    # Schritt 2: Artikel schreiben
    log("--- Schritt 2: Artikel schreiben ---")
    write_prompt = f"/write {topic}"
    run_claude_command(write_prompt, timeout=900)
    log("Artikel geschrieben.")

    # Neueste Draft-Datei finden
    draft_file = find_latest_file(DRAFTS_DIR)
    if not draft_file:
        log("FEHLER: Keine Draft-Datei in drafts/ gefunden.")
        sys.exit(1)

    log(f"Artikel-Datei: {draft_file.name}")

    # Schritt 3: WordPress veröffentlichen
    log("--- Schritt 3: WordPress-Veröffentlichung ---")
    publish_to_wordpress(draft_file, dry_run=args.dry_run)

    # Thema als erledigt markieren
    if not skip_queue_update:
        mark_topic_done(topic)

    log("=== Pipeline erfolgreich abgeschlossen ===")
    log(f"Thema veröffentlicht: '{topic}'")


if __name__ == "__main__":
    main()
