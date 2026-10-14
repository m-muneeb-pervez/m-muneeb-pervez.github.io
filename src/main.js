import '@fontsource-variable/newsreader/opsz.css'
import '@fontsource-variable/newsreader/opsz-italic.css'
import './style.css'
import { initAnalytics } from './analytics.js'

initAnalytics()

// Highlight the section currently in view in the side navigation.
const links = [...document.querySelectorAll('.toc a')]
const byId = new Map(links.map((a) => [a.getAttribute('href').slice(1), a]))

if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue
        links.forEach((a) => a.removeAttribute('aria-current'))
        byId.get(entry.target.id)?.setAttribute('aria-current', 'true')
      }
    },
    { rootMargin: '-20% 0px -70% 0px' },
  )
  document.querySelectorAll('main section[id]').forEach((s) => observer.observe(s))
}
