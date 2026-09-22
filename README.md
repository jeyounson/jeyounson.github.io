# Jeyoun Son's Website

## Updates guide
Change one of the files in `_data`, unless you are changing the look of the website.

Test changes using the installed Ruby 3.4 runtime and repository-local dependencies:
```
export PATH="/opt/homebrew/opt/ruby@3.4/bin:$PATH"
export BUNDLE_PATH=vendor/bundle
bundle install --frozen
bundle exec jekyll build
bundle exec ruby scripts/validate_site.rb
```

For a local browser preview, serve the generated `_site/` directory:

```bash
cd _site
python3 -m http.server 4000
```

Production uses GitHub Pages, publishing `master` at `https://www.jeyounson.com`. Preserve the root `CNAME`. Publish only with user approval, use the workspace push-with-closeout wrapper, and verify the exact GitHub Pages build and HTTPS pages after pushing. The old MIT deployment script is not this site's deployment path.

The [2026-09-22 repair plan](docs/site-ecosystem-repair-2026-09-22.ko.md) defines the public website/DeepWrite boundaries. Education links live in `_data/destinations.yml`; do not duplicate course materials or change authenticated course operations here.

## ORCID workflow

This repo includes a lightweight BibTeX-to-ORCID helper for personal ORCID accounts:

```bash
python3 scripts/orcid_sync.py /path/to/KCI_bibtex.bib
```

It generates reviewable JSON, a manual-entry checklist, and a tracking CSV under `orcid/`.

See [`orcid/README.md`](/Users/jeyounson/jeyounson.github.io/orcid/README.md) for details.

## Research page workflow

Use this site as the canonical public-facing research page for work that is
ready to be described publicly.

- Put stable public research entry points under `research/<slug>/`.
- Keep publication metadata in `_data/publications.yaml`.
- Add a `research_page` field to a publication when a paper belongs to a larger
  research page.
- Keep the full manuscript authority in the relevant writing repository; this
  site should explain the work and link to the published or permitted public
  versions.
- Rebuild locally with the Bundler/Jekyll command above.

The plain `jekyll` command may fail if system Ruby and user gem paths are mixed. Use the Ruby 3.4 runtime and repository-local `BUNDLE_PATH` above, preserving `Gemfile.lock`.

## Publication citation discoverability default

For every publicly posted article, English translation, accepted manuscript,
or publication-related HTML/PDF page, treat citation discoverability as part of
the publication task, not as later SEO polish.

A general research page is not enough. The concrete publication page should
carry the machine-readable and human-readable citation context that lets
scholars, search engines, and AI systems recognize the page as an authoritative
entry point for the work.

Minimum default for a publication page:

- stable canonical URL
- visible `Publication and Citation` box near the top of the page
- suggested citation for the public English access edition, when one exists
- version-of-record citation, DOI, and journal/KCI link where available
- clear version note for an English translation, author manuscript, HTML
  reading version, or PDF
- `citation_*` metadata for title, author, date, journal, volume, issue,
  pages, DOI, language, and PDF URL where available
- `description`, `keywords`, Open Graph article metadata, and `rel="canonical"`
- JSON-LD `ScholarlyArticle` data, including author ORCID when available
- PDF alternate link when a public PDF is permitted
- inclusion in `sitemap.xml`
- `_data/publications.yaml` links that point to the concrete public page, with
  labels such as `English translation`, `HTML`, `PDF`, or `DOI`

Boundary rule: do not imply that an English translation or local HTML copy is
the version of record unless it actually is. The public page should make the
formal citation target explicit and should expose only materials that may be
publicly posted.

English access-edition rule: for Korean-language scholarship whose likely
international readers have limited access to Korean, do not frame the English
translation as something to cite only in the narrow case of discussing
translation wording. Make the translation as complete, stable, and
edition-like as possible, and invite citation to the English access edition for
ordinary international scholarly discussion. The recommended citation should
still identify the Korean version of record and DOI, so that generous English
citation does not erase the formal publication record. Use a non-defensive
control clause rather than self-undermining language: say that the
author-prepared English access edition is not the journal's version of record
and that the Korean version controls for definitive wording, pagination, formal
indexing, and Korean-language legal scholarship.

KCI-wide backlog rule: do not treat this as a one-off rule for the current
`legal-acts-agents-en` page. All major KCI-published articles should eventually
receive at least a publication-specific citation shell, and the high-priority
articles should receive full English access editions or Korean-English parallel
editions. The homepage publication section intentionally does not maintain a
`Selected` subset; use the full publication inventory, topic/category filters,
research pages, and the workspace KCI audit plan as the curation and
completeness baseline.

Before pushing citation-surface changes:

- rebuild locally with the Bundler/Jekyll command above
- validate any manually added JSON-LD
- preview the page in a local browser
- after pushing, verify that the GitHub Pages build completed

**Stanford links**
- Use fetch!
- [Basic WWW for Individual Users](https://uit.stanford.edu/service/web/centralhosting/howto_user)
- [AFS File Transfer](https://uit.stanford.edu/service/afs/file-transfer/macintosh)


## External Libraries
- Framework: [Jekyll](http://jekyllrb.com/)
- CSS
  - [Skeleton](getskeleton.com)
  - Tabs: [Skeleton Tabs](https://github.com/nathancahill/skeleton-tabs)
  - Experience: [Timeline](https://codepen.io/NilsWe/pen/FemfK)
  - Icons: [Font Awesome](http://fontawesome.io/)
- JS
  - [Jquery (3.1.1)](https://jquery.com/)
