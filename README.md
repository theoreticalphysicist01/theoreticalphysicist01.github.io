# Zeng-Zhao Li — Academic Website

A lightweight, framework-free academic homepage built with semantic HTML, CSS, and a small amount of vanilla JavaScript for navigation enhancement.

## Update the site

- Edit biography and research text in `index.html`.
- Add or update papers in `data/publications.json`, then run `python3 scripts/build_publications.py`. The script sorts and groups entries automatically; set `selected` to `true` to include an item on the homepage.
- Publication records are generated into semantic HTML, so the complete list remains readable and indexable without JavaScript.
- Add CV or ORCID links only after authoritative URLs are confirmed.

For an HTTP-based local preview matching GitHub Pages behavior, run:

```sh
python3 -m http.server 8000
```

Then visit `http://localhost:8000`.

## Deploy with GitHub Pages

1. Create a public GitHub repository named `theoreticalphysicist01.github.io`.
2. Push this folder to the repository's `main` branch.
3. In **Settings → Pages**, choose **Deploy from a branch**, then select `main` and `/ (root)`.
4. GitHub will publish the site at <https://theoreticalphysicist01.github.io/>. No build workflow is required.

If the GitHub username differs, rename the repository to `<github-username>.github.io` and update canonical/Open Graph URLs in both HTML files.
