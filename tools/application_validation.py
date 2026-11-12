"""Record independent application checks and enforce the correction limit."""

import argparse
import json
from pathlib import Path
import sqlite3
import sys


DATABASE = Path(__file__).resolve().parents[1] / "documents/validation/checks.sqlite3"
MAX_CORRECTIONS = 5


def latest(db, application):
    row = db.execute(
        "SELECT revision, corrections, status, report FROM checks "
        "WHERE application = ? ORDER BY revision DESC LIMIT 1",
        (application,),
    ).fetchone()
    if row is None:
        return dict(revision=0, corrections=0, status="unchecked", report=None)
    revision, corrections, status, report = row
    return dict(revision=revision, corrections=corrections, status=status, report=json.loads(report))


def record(db, application, after, report):
    if not isinstance(report, dict):
        raise ValueError("Expected a JSON object")
    if "blocked" in report:
        raise ValueError("Inspection blocked; resolve the missing input before recording a verdict")
    files, findings = report.get("files"), report.get("findings")
    if not isinstance(files, list) or not files or not all(isinstance(f, str) and f.strip() for f in files):
        raise ValueError("List every inspected file in files")
    if not isinstance(findings, list):
        raise ValueError("Supply findings, using an empty list for a clean inspection")
    for finding in findings:
        if not isinstance(finding, dict) or finding.get("file") not in files:
            raise ValueError("Each finding must identify an inspected file")
        for key in ("location", "error", "evidence", "correction"):
            if not isinstance(finding.get(key), str) or not finding[key].strip():
                raise ValueError(f"Missing finding detail: {key}")

    # Serialize the read and append. A retry or concurrent review of the same
    # revision cannot consume another correction or undo a cancellation.
    with db:
        db.execute("BEGIN IMMEDIATE")
        previous = latest(db, application)
        if previous["status"] == "cancelled":
            raise ValueError("Application cancelled; see its recorded findings")
        if previous["revision"] != after:
            raise ValueError("Stale review revision; read status before proceeding")
        corrections = previous["corrections"] if previous["status"] == "amend" else 0
        if not findings:
            status = "passed"
        elif corrections == MAX_CORRECTIONS:
            status = "cancelled"
        else:
            corrections += 1
            status = "amend"
        db.execute(
            "INSERT INTO checks VALUES (?, ?, ?, ?, ?)",
            (application, after + 1, corrections, status, json.dumps(report, ensure_ascii=False)),
        )
        return latest(db, application)


def open_ledger(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.execute(
        "CREATE TABLE IF NOT EXISTS checks (application TEXT, revision INTEGER, "
        "corrections INTEGER, status TEXT, report TEXT, PRIMARY KEY (application, revision))"
    )
    return db


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("status", "record"))
    parser.add_argument("application", help="stable key for this posting")
    parser.add_argument("--after", type=int, help="revision seen before the independent inspection")
    parser.add_argument("--report", type=Path, help="validator JSON file (default: standard input)")
    args = parser.parse_args()
    if args.action == "record" and args.after is None:
        parser.error("record requires --after")
    db = open_ledger(DATABASE)
    try:
        if args.action == "status":
            result = latest(db, args.application)
        else:
            report = json.loads(args.report.read_text(encoding="utf-8-sig") if args.report else sys.stdin.read())
            result = record(db, args.application, args.after, report)
        print(json.dumps(result, ensure_ascii=True))
    except (ValueError, OSError, sqlite3.Error) as exc:
        parser.exit(1, f"Validation record error: {exc}\n")
    finally:
        db.close()


if __name__ == "__main__":
    main()
