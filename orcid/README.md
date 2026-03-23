# ORCID Manual-Entry Workflow

This repository generates ORCID-ready helper files from a Zotero/KCI BibTeX export.
The target workflow is a personal ORCID account that updates works manually.

## Quick start

Generate helper files from a BibTeX export:

```bash
python3 scripts/orcid_sync.py /path/to/KCI_bibtex.bib
```

This writes:

- `orcid/works.review.json`: compact review list
- `orcid/works.full.json`: normalized metadata
- `orcid/works.orcid-payloads.json`: structured ORCID-style payloads for reference
- `orcid/works.validation.json`: entries missing required ORCID fields
- `orcid/works.manual-entry.md`: step-by-step checklist for manual entry
- `orcid/works.manual-entry.csv`: tracking sheet with a blank `status` column
- `orcid/works.english-first.bib`: BibTeX rewritten to prefer English title, journal, keywords, abstract, and author name

## Notes

- Personal ORCID accounts cannot use the production write API by themselves; this workflow is intentionally designed around manual entry support.
- Use `orcid/works.manual-entry.md` while entering records in ORCID and mark completion in `orcid/works.manual-entry.csv`.
- If you want to upload a BibTeX file to another service but keep the display mostly in English, use `orcid/works.english-first.bib`.
- The website already stores your ORCID profile URL in `_data/main_info.yaml`; this workflow focuses on work metadata updates.
