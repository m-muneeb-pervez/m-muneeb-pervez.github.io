import { existsSync } from 'node:fs'
import { defineConfig } from 'vite'

const builtOn = new Date().toLocaleDateString('en-GB', { month: 'long', year: 'numeric' })
const has = (file) => existsSync(new URL(`./public/${file}`, import.meta.url))

// Elements marked with an attribute (data-cv, data-photo) are kept only when the
// matching file exists in public/, so the site never links to a missing file.
function keepIf(html, attr, keep) {
  if (keep) return html.replace(new RegExp(` ${attr}(?=[\\s>])`, 'g'), '')
  return html
    .replace(new RegExp(`<(li|span|figure)\\b[^>]*\\b${attr}\\b[^>]*>[\\s\\S]*?<\\/\\1>`, 'g'), '')
    .replace(new RegExp(`<meta\\b[^>]*\\b${attr}\\b[^>]*>\\s*`, 'g'), '')
}

export default defineConfig({
  // Relative base so the build works from a domain root or a subpath (GitHub Pages).
  base: './',
  plugins: [
    {
      name: 'site-html',
      transformIndexHtml(html) {
        let out = keepIf(html, 'data-cv', has('Muneeb_Pervez_CV.pdf'))
        out = keepIf(out, 'data-photo', has('muneeb.jpg'))
        return out.replaceAll('{{BUILT_ON}}', builtOn)
      },
    },
  ],
})
