# KINETONE — Sound Objects

A complete 12-page fictional electronic music instrument website, built with **28 original user-supplied photographs** and working browser audio experiences. Original design concept by pfxamd.

## Site

- Home and Instruments collection
- Dedicated PULSE / FORM / LOOP product pages
- **Play** — working 16-step 4-track drum sequencer, 25-key polyphonic synthesizer and local audio sampler
- Sessions — three original procedural audio performances
- Journal / Design Story / Sound Story / About / Support

All media and specifications are fictional product demonstrations. **No physical hardware is offered for sale.** Audio files and microphone recordings remain in browser memory and are never uploaded. Microphone use is optional.

## Run and test locally

Python 3.10 or newer. Node 18+ for syntax verification.

```sh
python tools/build.py
python tools/check.py
python tools/serve.py
```

Open `http://localhost:8073/KINETONE/`.

The site is an intentionally dependency-free, prerendered frontend. Web Audio APIs provide genuine sound generation, with accessible progressive enhancements and reduced-motion support. The browser's standard audio and media APIs are used, with no external runtime libraries or CDN requirements for functionality. Web fonts are an optional enhancement.

## Asset map

All 28 images are in `assets/img/` and duplicated as deployable media under `docs/assets/img/`. Filenames retain the original image number and descriptive usage. Photo series: 01–04 brand, 05–07 PULSE, 08–10 FORM, 11–13 LOOP, 14–19 details, 20–22 lifestyle, 23–24 stories, 25–26 sessions, 27–28 editorial. `tools/build.py` generates the 12 pages and copies media.

## Publish

Target repository: [pfxamd/KINETONE](https://github.com/pfxamd/KINETONE). Site: `https://pfxamd.github.io/KINETONE/`.

Use Git and GitHub CLI, authenticated with `gh auth login`.

On Windows: extract the complete package and double-click `publish-pages.bat`. On Linux/macOS: `bash publish-pages.sh`.

The publisher uploads all website source files **and the original 28 images** in one regular Git commit, then enables GitHub Pages (when possible) and publishes via `.github/workflows/pages.yml`.

## Source organization

- `tools/build.py` — static page generator
- `tools/check.py` — static routing, image, ID and syntax tests
- `tools/serve.py` — local static server with proper base path
- `assets/site.css`, `assets/site.js` — style and interactive runtime
- `assets/img/` — 28 numbered source photographs
- `docs/` — full static output served by GitHub Pages
- `.github/workflows/pages.yml` — GitHub Pages deployment

All images were supplied by the user for this fictional website. Pages are prerendered without server-side rendering or a database. Product demos work through pointer or keyboard activation. Sound begins only with a user action.
