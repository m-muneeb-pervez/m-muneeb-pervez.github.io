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
