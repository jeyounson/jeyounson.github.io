#!/usr/bin/env python3
"""Generate ORCID-ready work files from a BibTeX export.

This script is designed for a lightweight GitHub Pages/Jekyll workflow:

1. Read a BibTeX export from Zotero/KCI
2. Normalize the metadata needed by ORCID
3. Write reviewable JSON files into the repository
4. Write manual-entry helper files for ORCID personal accounts
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


ENTRY_START_RE = re.compile(r"@(?P<kind>[A-Za-z]+)\s*\{\s*(?P<key>[^,]+)\s*,", re.MULTILINE)


@dataclass
class BibEntry:
    entry_type: str
    cite_key: str
    fields: Dict[str, str]


def _strip_wrapping(value: str) -> str:
    value = value.strip().rstrip(",").strip()
    if len(value) >= 2 and value[0] == "{" and value[-1] == "}":
        value = value[1:-1]
    if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
        value = value[1:-1]
    return value.strip()


def _find_matching_brace(text: str, start_index: int) -> int:
    depth = 0
    for index in range(start_index, len(text)):
        char = text[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return index
    raise ValueError(f"Unmatched brace starting at offset {start_index}")


def _parse_entry_body(body: str) -> Dict[str, str]:
    fields: Dict[str, str] = {}
    index = 0
    length = len(body)

    while index < length:
        while index < length and body[index] in " \t\r\n,":
            index += 1
        if index >= length:
            break

        key_start = index
        while index < length and body[index] not in "=":
            index += 1
        if index >= length:
            break

        raw_key = body[key_start:index].strip()
        index += 1
        while index < length and body[index].isspace():
            index += 1
        if index >= length:
            fields[raw_key] = ""
            break

        if body[index] == "{":
            value_start = index
            value_end = _find_matching_brace(body, index)
            raw_value = body[value_start : value_end + 1]
            index = value_end + 1
        elif body[index] == '"':
            value_start = index
            index += 1
            escaped = False
            while index < length:
                char = body[index]
                if char == '"' and not escaped:
                    break
                escaped = char == "\\" and not escaped
                if char != "\\":
                    escaped = False
                index += 1
            raw_value = body[value_start : index + 1]
            index += 1
        else:
            value_start = index
            while index < length and body[index] not in ",\n":
                index += 1
            raw_value = body[value_start:index]

        fields[raw_key] = _strip_wrapping(raw_value)

        while index < length and body[index] != ",":
            if not body[index].isspace():
                break
            index += 1
        if index < length and body[index] == ",":
            index += 1

    return fields


def parse_bibtex(text: str) -> List[BibEntry]:
    entries: List[BibEntry] = []
    search_start = 0

    while True:
        match = ENTRY_START_RE.search(text, search_start)
        if not match:
            break

        brace_start = text.find("{", match.start())
        brace_end = _find_matching_brace(text, brace_start)
        body = text[match.end() : brace_end]
        entries.append(
            BibEntry(
                entry_type=match.group("kind").lower(),
                cite_key=match.group("key").strip(),
                fields=_parse_entry_body(body),
            )
        )
        search_start = brace_end + 1

    return entries


def clean_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def split_keywords(value: str) -> List[str]:
    if not value:
        return []
    return [clean_space(item) for item in value.split(",") if clean_space(item)]


def field(entry: BibEntry, *names: str) -> str:
    for name in names:
        if name in entry.fields and entry.fields[name].strip():
            return clean_space(entry.fields[name])
    return ""


def map_work_type(entry_type: str) -> str:
    mapping = {
        "article": "journal-article",
        "inproceedings": "conference-paper",
        "conference": "conference-paper",
        "book": "book",
        "phdthesis": "dissertation-thesis",
        "mastersthesis": "dissertation-thesis",
        "techreport": "report",
    }
    return mapping.get(entry_type, "journal-article")


def build_external_ids(entry: BibEntry) -> List[dict]:
    external_ids: List[dict] = []
    doi = field(entry, "DOI", "doi")
    if doi:
        external_ids.append(
            {
                "external-id-type": "doi",
                "external-id-value": doi,
                "external-id-url": {"value": f"https://doi.org/{doi}"},
                "external-id-relationship": "self",
            }
        )

    unique_id = field(entry, "Unique-ID")
    url = field(entry, "Url", "URL", "url")
    if unique_id and url:
        external_ids.append(
            {
                "external-id-type": "source-work-id",
                "external-id-value": unique_id,
                "external-id-url": {"value": url},
                "external-id-relationship": "self",
            }
        )
    return external_ids


def normalize_entry(entry: BibEntry, default_author_name: str = "") -> dict:
    title = field(entry, "Title-English", "Title-Foreign", "Title")
    title_native = field(entry, "Title")
    journal = field(entry, "Journal-Foreign", "Journal", "Journal-Abbreviation")
    journal_native = field(entry, "Journal")
    url = field(entry, "Url", "URL", "url")
    year = field(entry, "Year", "year")
    month_day = field(entry, "Month-Day")
    volume = field(entry, "Volume")
    issue = field(entry, "Number")
    pages = field(entry, "Pages")
    doi = field(entry, "DOI", "doi")
    author = field(entry, "Author") or default_author_name
    language = field(entry, "Language")
    abstract = field(entry, "Abstract-English", "Abstract")
    abstract_native = field(entry, "Abstract")
    keywords = split_keywords(field(entry, "Keywords-English", "Keywords-Foreign", "Keyword"))
    keywords_native = split_keywords(field(entry, "Keyword"))

    normalized = {
        "cite_key": entry.cite_key,
        "source_entry_type": entry.entry_type,
        "title": title,
        "title_native": title_native,
        "journal": journal,
        "journal_native": journal_native,
        "year": year,
        "month_day": month_day,
        "volume": volume,
        "issue": issue,
        "pages": pages,
        "type": map_work_type(entry.entry_type),
        "url": url,
        "doi": doi,
        "author": author,
        "language": language,
        "abstract": abstract,
        "abstract_native": abstract_native,
        "keywords": keywords,
        "keywords_native": keywords_native,
        "external_ids": build_external_ids(entry),
    }
    return normalized


def validate_work(work: dict) -> List[str]:
    missing = []
    for key in ("title", "journal", "year"):
        if not work.get(key):
            missing.append(key)
    return missing


def build_orcid_work_payload(work: dict) -> dict:
    payload = {
        "title": {
            "title": {"value": work["title"]},
        },
        "type": work["type"],
        "journal-title": {"value": work["journal"]},
        "publication-date": {
            "year": {"value": str(work["year"])},
        },
        "url": {"value": work["url"]} if work.get("url") else None,
        "short-description": work.get("abstract") or None,
        "external-ids": {
            "external-id": work["external_ids"],
        }
        if work["external_ids"]
        else None,
    }

    if work.get("month_day"):
        month_match = re.search(r"([A-Za-z]+)\.\s+(\d{1,2})\.", work["month_day"])
        month_map = {
            "Jan": "01",
            "Feb": "02",
            "Mar": "03",
            "Apr": "04",
            "May": "05",
            "Jun": "06",
            "Jul": "07",
            "Aug": "08",
            "Sep": "09",
            "Oct": "10",
            "Nov": "11",
            "Dec": "12",
        }
        if month_match:
            month_name, day = month_match.groups()
            month_value = month_map.get(month_name[:3])
            if month_value:
                payload["publication-date"]["month"] = {"value": month_value}
                payload["publication-date"]["day"] = {"value": day.zfill(2)}

    if work.get("title_native") and work["title_native"] != work["title"]:
        payload["translated-title"] = {
            "value": work["title_native"],
            "language-code": "ko",
        }

    return {key: value for key, value in payload.items() if value not in (None, "", [])}


def load_entries(path: Path) -> List[BibEntry]:
    return parse_bibtex(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def escape_bibtex_value(value: str) -> str:
    text = value or ""
    text = text.replace("\\", "\\\\")
    return text.replace("{", "\\{").replace("}", "\\}")


def csv_escape(value: str) -> str:
    text = value or ""
    text = text.replace('"', '""')
    return f'"{text}"'


def write_manual_csv(path: Path, works: List[dict]) -> None:
    header = [
        "status",
        "cite_key",
        "title",
        "journal",
        "year",
        "month_day",
        "type",
        "doi",
        "url",
        "title_native",
        "journal_native",
        "keywords",
    ]
    lines = [",".join(header)]
    for work in works:
        row = [
            "",
            work["cite_key"],
            work["title"],
            work["journal"],
            work["year"],
            work["month_day"],
            work["type"],
            work["doi"],
            work["url"],
            work["title_native"],
            work["journal_native"],
            "; ".join(work["keywords"]),
        ]
        lines.append(",".join(csv_escape(value) for value in row))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_manual_entry_markdown(works: List[dict], issues: List[dict]) -> str:
    issues_by_key = {item["cite_key"]: item["missing"] for item in issues}
    lines = [
        "# ORCID Manual Entry Checklist",
        "",
        "Use these records when adding works manually in ORCID.",
        "Recommended ORCID form fields: title, journal title, publication date, URL, external IDs.",
        "",
    ]
    for index, work in enumerate(works, start=1):
        missing = issues_by_key.get(work["cite_key"], [])
        lines.append(f"## {index}. {work['title']}")
        lines.append("")
        lines.append(f"- Status: {'Needs metadata fix' if missing else 'Ready to enter'}")
        lines.append(f"- Cite key: `{work['cite_key']}`")
        lines.append(f"- Work type: `{work['type']}`")
        lines.append(f"- Title (English): {work['title'] or '[missing]'}")
        lines.append(f"- Title (Korean): {work['title_native'] or '[missing]'}")
        lines.append(f"- Journal: {work['journal'] or '[missing]'}")
        lines.append(f"- Journal (Korean): {work['journal_native'] or '[missing]'}")
        lines.append(f"- Publication year: {work['year'] or '[missing]'}")
        lines.append(f"- Publication date detail: {work['month_day'] or '[optional]'}")
        lines.append(f"- DOI: {work['doi'] or '[none]'}")
        lines.append(f"- URL: {work['url'] or '[none]'}")
        lines.append(f"- External IDs: {json.dumps(work['external_ids'], ensure_ascii=False)}")
        lines.append(f"- Keywords: {', '.join(work['keywords']) or '[none]'}")
        if missing:
            lines.append(f"- Missing ORCID minimum fields: {', '.join(missing)}")
        lines.append("")
    return "\n".join(lines)


def build_english_first_bib_entry(entry: BibEntry, english_author_name: str) -> str:
    work = normalize_entry(entry, default_author_name=english_author_name)
    preferred_author = english_author_name or field(entry, "Author")
    preferred_title = field(entry, "Title-English", "Title-Foreign", "Title")
    preferred_journal = field(entry, "Journal-Foreign", "Journal", "Journal-Abbreviation")
    preferred_keywords = field(entry, "Keywords-English", "Keywords-Foreign", "Keyword")
    preferred_abstract = field(entry, "Abstract-English", "Abstract")

    ordered_fields = [
        ("author", preferred_author),
        ("title", preferred_title),
        ("journal", preferred_journal),
        ("year", field(entry, "Year", "year")),
        ("volume", field(entry, "Volume")),
        ("number", field(entry, "Number")),
        ("pages", field(entry, "Pages")),
        ("month", field(entry, "Month-Day")),
        ("doi", field(entry, "DOI", "doi")),
        ("url", field(entry, "Url", "URL", "url")),
        ("keywords", preferred_keywords),
        ("abstract", preferred_abstract),
        ("language", "en"),
        ("title_native", work["title_native"]),
        ("journal_native", work["journal_native"]),
        ("source_work_id", field(entry, "Unique-ID")),
    ]

    lines = [f"@{entry.entry_type}{{{entry.cite_key},"]
    rendered = []
    for key, value in ordered_fields:
        if value:
            rendered.append(f"  {key} = {{{escape_bibtex_value(value)}}}")
    lines.append(",\n".join(rendered))
    lines.append("}")
    return "\n".join(lines)


def write_english_first_bib(path: Path, entries: List[BibEntry], english_author_name: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    blocks = [
        build_english_first_bib_entry(entry, english_author_name=english_author_name)
        for entry in entries
    ]
    path.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bib", type=Path, help="Path to the BibTeX file")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("orcid"),
        help="Directory for generated ORCID artifacts",
    )
    parser.add_argument(
        "--author-name",
        default="Jeyoun Son",
        help="Fallback author name when the BibTeX entry omits Author",
    )
    parser.add_argument(
        "--bib-author-name",
        default="Son, Jeyoun",
        help="English author name to use in the exported English-first BibTeX",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Only process the first N entries (0 means all)",
    )
    return parser


def summarize_missing_fields(works: Iterable[dict]) -> List[dict]:
    issues = []
    for work in works:
        missing = validate_work(work)
        if missing:
            issues.append({"cite_key": work["cite_key"], "missing": missing})
    return issues


def print_next_steps(out_dir: Path) -> None:
    print("")
    print("Personal-account workflow:")
    print("1. Open ORCID > Works > Add works > Add manually")
    print(f"2. Use {out_dir / 'works.manual-entry.md'} as the step-by-step checklist")
    print(f"3. Use {out_dir / 'works.manual-entry.csv'} to track what you already entered")
    print(f"4. Use {out_dir / 'works.orcid-payloads.json'} only as a structured reference")


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_argument_parser()
    args = parser.parse_args(argv)

    entries = load_entries(args.bib)
    if args.limit > 0:
        entries = entries[: args.limit]

    works = [normalize_entry(entry, default_author_name=args.author_name) for entry in entries]
    review_items = [
        {
            "cite_key": work["cite_key"],
            "title": work["title"],
            "journal": work["journal"],
            "year": work["year"],
            "doi": work["doi"],
            "url": work["url"],
            "type": work["type"],
        }
        for work in works
    ]
    api_payloads = [
        {
            "cite_key": work["cite_key"],
            "payload": build_orcid_work_payload(work),
        }
        for work in works
        if not validate_work(work)
    ]
    issues = summarize_missing_fields(works)

    write_json(args.out_dir / "works.review.json", review_items)
    write_json(args.out_dir / "works.full.json", works)
    write_json(args.out_dir / "works.orcid-payloads.json", api_payloads)
    write_json(args.out_dir / "works.validation.json", issues)
    write_manual_csv(args.out_dir / "works.manual-entry.csv", works)
    write_english_first_bib(args.out_dir / "works.english-first.bib", entries, args.bib_author_name)
    (args.out_dir / "works.manual-entry.md").write_text(
        build_manual_entry_markdown(works, issues) + "\n",
        encoding="utf-8",
    )

    print(f"Parsed {len(entries)} BibTeX entries from {args.bib}")
    print(f"Wrote review data to {args.out_dir / 'works.review.json'}")
    print(f"Wrote normalized data to {args.out_dir / 'works.full.json'}")
    print(f"Wrote ORCID payloads to {args.out_dir / 'works.orcid-payloads.json'}")
    print(f"Wrote validation issues to {args.out_dir / 'works.validation.json'}")
    print(f"Wrote manual checklist to {args.out_dir / 'works.manual-entry.md'}")
    print(f"Wrote manual tracking CSV to {args.out_dir / 'works.manual-entry.csv'}")
    print(f"Wrote English-first BibTeX to {args.out_dir / 'works.english-first.bib'}")

    if issues:
        print(f"{len(issues)} entries are missing required ORCID minimum fields.")

    print_next_steps(args.out_dir)

    return 0


if __name__ == "__main__":
    sys.exit(main())
