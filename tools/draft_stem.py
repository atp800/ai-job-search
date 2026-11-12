"""Build a safe, repeatable draft filename stem for a resolved vacancy."""

import argparse
import hashlib
import re


def draft_stem(company, role, vacancy_key):
    if not all(value.strip() for value in (company, role, vacancy_key)):
        raise ValueError("Company, role and a resolved vacancy key are required")
    parts = [
        re.sub(r"[^a-z0-9]+", "_", value.casefold()).strip("_")[:40] or "job"
        for value in (company, role)
    ]
    digest = hashlib.sha256(vacancy_key.strip().encode("utf-8")).hexdigest()[:20]
    return "_".join([*parts, digest])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("company", "role", "vacancy_key"):
        parser.add_argument(name)
    args = parser.parse_args()
    print(draft_stem(args.company, args.role, args.vacancy_key))
