# Muneeb Pervez, personal site

Static site built with Vite (vanilla JS, no framework). All content lives in `index.html`.

```
npm install
npm run dev       # local development
npm run build     # production build in dist/
npm run preview   # serve dist/ locally
```

## Editing

- Text: `index.html`. Publications are numbered `[1]`, `[2]`, `[3]` and cited from the text with `<a class="cite" href="#pub-N">`.
- Styles and colors: `src/style.css` (palette variables are at the top). The site is light by default, and dark mode is a toggle in the side column that remembers the visitor's choice.
- Photo: put a square image at `public/muneeb.jpg`. It appears in the side column and is used as the link preview image. Without the file, the site simply has no photo.
- CV: put the PDF at `public/Muneeb_Pervez_CV.pdf`. The CV links in the page appear only when that file exists, so the site never links to a missing file.

## Analytics (Umami)

Visit counts use [Umami](https://umami.is): no cookies, no tracking across sites, no consent banner.

**Status: off until a website ID is set.** The deploy workflow passes the repository variable `UMAMI_WEBSITE_ID` to the build, so once that variable exists every deployed build counts visits.

1. Create a free account at [cloud.umami.is](https://cloud.umami.is) and add a website with the domain `m-muneeb-pervez.github.io`.
2. Copy the Website ID (a UUID) from the website's settings.
3. In the GitHub repository, go to Settings, Secrets and variables, Actions, Variables, and add `UMAMI_WEBSITE_ID` with that ID. Then re-run the deploy workflow.

A build only includes the counter when an ID is present, so `npm run dev` and a plain local `npm run build` have it off. It also never runs on localhost. It skips browsers that identify as automated (a `webdriver` flag or a headless user agent), counts a visit only after the visitor scrolls, moves the mouse, touches the screen, or presses a key (a visitor who leaves without doing any of those is not counted; change the `INTERACTIONS` list in `src/analytics.js` to adjust), and is locked to the site's hostname with Umami's `data-domains` setting, so copies of the site on other hosts report nothing. **If the site moves to a custom domain, add it to `VITE_UMAMI_DOMAINS` (comma separated) or counting stops.** To leave your own browser out of the numbers, open the site, run `localStorage.setItem('umami.disabled', '1')` in the browser console, and repeat in each browser you use. CV opens, email clicks, and outbound links are recorded as events. A short privacy note appears in the footer when analytics are active.

- Turn analytics off: delete the `UMAMI_WEBSITE_ID` variable and re-run the deploy workflow.
- Test a local build with analytics: copy `.env.example` to `.env.production`, set `VITE_UMAMI_WEBSITE_ID`, and run `npm run build`.
- Self-hosted Umami: also set `VITE_UMAMI_SRC` to your instance's script URL.

## Deploying

The site is published with GitHub Pages at https://m-muneeb-pervez.github.io/. Every push to `main` runs `.github/workflows/deploy.yml`, which builds the site and publishes `dist/`.

The build uses relative paths, so `dist/` also works on any other static host, at a domain root or a subpath.

## Figures

The paper figures in the Publications section are SVGs. Each one exists twice in `public/`, as `NAME-light.svg` and `NAME-dark.svg`, painted on the exact page background so it blends in. The page shows one or the other depending on the dark-mode toggle (an image cannot read the page's theme, so two files are needed).

Run `python3 figures/build_figures.py` to regenerate all six. The script holds the palette (mirroring `src/style.css`) and draws every figure:

- `www-overview.svg`: the Web Conference study as one picture (who and what was studied, the two interventions, how they were tested, findings), drawn at the size it is shown (720 px wide).
- `icwsm-pipeline.svg`: the ICWSM detection pipeline.
- `safemas-overview.svg`: the whole safeMAS paper as one picture. If the paper's numbers change, edit them in `safemas()` in the script.

All three are drawn at 720 px wide, with text of at least 14 px. On phones each figure scrolls sideways inside its own box (`.fig-scroll` in `src/style.css`) instead of shrinking, and tapping it opens the full-size image.

If the site colors change, update the palette in the script and run it again.
