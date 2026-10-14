import { existsSync } from 'node:fs'
import { defineConfig } from 'vite'

const builtOn = new Date().toLocaleDateString('en-GB', { month: 'long', year: 'numeric' })
const hasCv = existsSync(new URL('./public/Muneeb_Pervez_CV.pdf', import.meta.url))

export default defineConfig({
  // Relative base so the build works from a domain root or a subpath (GitHub Pages).
  base: './',
  plugins: [
    {
      name: 'site-html',
      transformIndexHtml(html) {
        // Elements marked data-cv are kept only when public/Muneeb_Pervez_CV.pdf exists,
        // so the site never links to a missing file.
        const withCv = hasCv
          ? html.replace(/ data-cv(?=[\s>])/g, '')
          : html.replace(/<(li|span)\b[^>]*\bdata-cv\b[^>]*>[\s\S]*?<\/\1>/g, '')
        return withCv.replaceAll('{{BUILT_ON}}', builtOn)
      },
    },
  ],
})
