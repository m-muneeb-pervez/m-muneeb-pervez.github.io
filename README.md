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

## Analytics (GoatCounter)

Visit counts use [GoatCounter](https://www.goatcounter.com): free, no cookies, no consent banner. It is off until a site code is set.

1. Create a free account and pick a site code, for example `muneeb`.
2. Copy `.env.example` to `.env.production`, set `VITE_GOATCOUNTER_CODE=muneeb`, and rebuild. The code is public (it ships in the built JS), so committing `.env.production` is fine. On a host that builds for you (Netlify, Vercel, GitHub Actions), you can instead set `VITE_GOATCOUNTER_CODE` in the host's build environment.

It runs only in production builds, never on localhost, and respects Do Not Track. CV opens, email clicks, and outbound links are recorded as events. A short privacy note appears in the footer when analytics are active.

## Deploying

The site is published with GitHub Pages at https://m-muneeb-pervez.github.io/. Every push to `main` runs `.github/workflows/deploy.yml`, which builds the site and publishes `dist/`.

To enable analytics on the live site without touching code, add a repository variable named `GOATCOUNTER_CODE` (Settings, Secrets and variables, Actions, Variables) and re-run the workflow.

The build uses relative paths, so `dist/` also works on any other static host, at a domain root or a subpath.
