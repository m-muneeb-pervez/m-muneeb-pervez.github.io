import '@fontsource-variable/newsreader/opsz.css'
import '@fontsource-variable/newsreader/opsz-italic.css'
import './style.css'
import { initAnalytics } from './analytics.js'

initAnalytics()

// Theme: light by default, dark only when the visitor switches it on.
// The saved choice is applied before first paint by a small inline script in index.html.
const root = document.documentElement
const toggle = document.querySelector('.theme-toggle')

function setTheme(dark) {
  if (dark) root.dataset.theme = 'dark'
  else delete root.dataset.theme
  toggle?.setAttribute('aria-pressed', String(dark))
}

setTheme(root.dataset.theme === 'dark')

toggle?.addEventListener('click', () => {
  const dark = root.dataset.theme !== 'dark'
  setTheme(dark)
  try {
    localStorage.setItem('theme', dark ? 'dark' : 'light')
  } catch {
    // Storage can be blocked; the switch still works for this visit.
  }
})

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
