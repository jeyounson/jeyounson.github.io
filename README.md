# Jeyoun Son's Website

## Updates guide
Change one of the files in `_data`, unless you are changing the look of the website.

Test changes with:
```
/Users/jeyounson/.rubies/ruby-3.3.5/bin/ruby /Users/jeyounson/.gem/ruby/3.3.5/bin/jekyll build
```

For a local browser preview, serve the generated `_site/` directory:

```bash
cd _site
python3 -m http.server 4000
```

Push to the ML web directory:
```
rm -rf public_html
mkdir public_html
```
```
./__deploy.sh
```

More info on the [Media Lab wiki](http://wiki.media.mit.edu/view/Necsys/WebPagePersonal).

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
- Rebuild locally with the same Ruby 3.3 command above.

The plain `jekyll` command may fail on this machine if the system Ruby and
user gem path are mixed.

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

Before pushing citation-surface changes:

- rebuild locally with the Ruby 3.3 Jekyll command above
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
