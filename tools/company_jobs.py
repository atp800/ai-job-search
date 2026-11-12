"""Read configured employers' public job boards. Custom careers sites use the web workflow."""

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


SETTINGS = Path(__file__).resolve().parents[1] / ".claude/skills/job-scraper/companies.json"


def fetch_json(url):
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "ai-job-search"})
    with urlopen(request, timeout=20) as response:
        return json.load(response)


def required_text(row, field):
    value = row[field]
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Missing {field} in posting")
    return value


def read_board(entry, fetch=fetch_json):
    name = entry.get("name") if isinstance(entry, dict) else None
    url = entry.get("careers_url") if isinstance(entry, dict) else None
    report = {"company": name, "careers_url": url}
    try:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Missing company name")
        if not url:
            return {**report, "status": "resolve_url"}
        parsed = urlsplit(url)
        if parsed.scheme not in ("http", "https") or not parsed.hostname:
            raise ValueError("Expected a public careers URL")
        tenant = parsed.path.strip("/").split("/")[0]
        if not re.fullmatch(r"[a-zA-Z0-9_-]+", tenant):
            return {**report, "status": "check_web"}

        jobs = []
        if parsed.hostname in ("boards.greenhouse.io", "job-boards.greenhouse.io"):
            rows = fetch(f"https://boards-api.greenhouse.io/v1/boards/{tenant}/jobs")["jobs"]
            if not isinstance(rows, list):
                raise ValueError("Unexpected Greenhouse response")
            for row in rows:
                jobs.append({"title": required_text(row, "title"), "url": required_text(row, "absolute_url"),
                             "location": (row.get("location") or {}).get("name")})
        elif parsed.hostname in ("jobs.lever.co", "jobs.eu.lever.co"):
            host = "api.eu.lever.co" if parsed.hostname == "jobs.eu.lever.co" else "api.lever.co"
            seen = set()
            offset = 0
            while True:
                rows = fetch(f"https://{host}/v0/postings/{tenant}?mode=json&skip={offset}&limit=100")
                if not isinstance(rows, list):
                    raise ValueError("Unexpected Lever response")
                for row in rows:
                    link = required_text(row, "hostedUrl")
                    if link in seen:
                        raise ValueError("Overlapping Lever pages; verify on careers site")
                    seen.add(link)
                    jobs.append({"title": required_text(row, "text"), "url": link,
                                 "location": (row.get("categories") or {}).get("location"),
                                 "workplace_type": row.get("workplaceType")})
                if len(rows) < 100:
                    break
                offset += len(rows)
        else:
            return {**report, "status": "check_web"}
        return {**report, "status": "listed", "jobs": jobs}
    except (URLError, OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        return {**report, "status": "unavailable", "reason": str(exc)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--settings", type=Path, default=SETTINGS)
    args = parser.parse_args()
    try:
        companies = json.loads(args.settings.read_text(encoding="utf-8-sig"))
        if not isinstance(companies, list):
            raise ValueError("Expected an array of company settings")
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Could not read company settings: {exc}\n")
    sys.stdout.write(json.dumps([read_board(company) for company in companies]) + "\n")


if __name__ == "__main__":
    main()
