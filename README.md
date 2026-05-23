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

## Public knowledge surface workflow

Use this site as the canonical public-facing research surface for work that is
ready to be explained publicly.

- Put stable public research entry points under `research/<slug>/`.
- Keep publication metadata in `_data/publications.yaml`.
- Add a `research_page` field to a publication when a paper belongs to a larger
  research surface.
- Keep the full manuscript authority in the relevant writing repository; this
  site should explain the work and link to the published or permitted public
  versions.
- Rebuild locally with the same Ruby 3.3 command above.

The plain `jekyll` command may fail on this machine if the system Ruby and
user gem path are mixed.

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
