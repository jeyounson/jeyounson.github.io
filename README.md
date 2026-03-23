# Jeyoun Son's Website

## Updates guide
Change one of the files in `_data`, unless you are changing the look of the website.

Test changes with:
```
jekyll serve
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
