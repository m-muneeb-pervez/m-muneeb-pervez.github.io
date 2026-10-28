// Privacy-friendly visit counts via Umami (no cookies, no tracking across sites).
// Active only in production builds, never on localhost, and only when a website ID is set.
// A visit is counted only after the visitor interacts with the page (scroll, mouse move, touch,
// key press), which leaves out scanners and bots that load the page and leave. Automated
// browsers are skipped, and Umami only reports from the allowed domain.

const websiteId = import.meta.env.VITE_UMAMI_WEBSITE_ID
// Umami Cloud by default. For a self-hosted Umami, set VITE_UMAMI_SRC to its script URL.
const src = import.meta.env.VITE_UMAMI_SRC || 'https://cloud.umami.is/script.js'
// Hostnames (comma separated) the counter may report from. Copies of the site served from any
// other host are ignored. Add a custom domain here when the site moves to one.
const domains = import.meta.env.VITE_UMAMI_DOMAINS || 'm-muneeb-pervez.github.io'
const note = document.getElementById('analytics-note')

// Events that show a person is using the page. Listed in one place so they are easy to change.
const INTERACTIONS = ['pointermove', 'pointerdown', 'touchstart', 'keydown', 'wheel', 'scroll']

function say(text) {
  if (!note) return
  note.textContent = text
  note.hidden = false
}

function isLocal() {
  return /^(localhost|127\.|0\.0\.0\.0|10\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.)|\.local$/.test(location.hostname)
}

// Browsers driven by automation (scrapers, scanners, test runners) announce themselves.
function looksAutomated() {
  return navigator.webdriver === true || /headless|phantomjs|puppeteer|playwright/i.test(navigator.userAgent)
}

let interacted = false
let scriptReady = false
let pageviewSent = false

// Sends the pageview once the visitor has interacted and Umami's script has loaded.
function flush() {
  if (pageviewSent || !interacted || !scriptReady) return
  pageviewSent = true
  window.umami?.track?.()
}

function onInteract() {
  interacted = true
  INTERACTIONS.forEach((type) => window.removeEventListener(type, onInteract, true))
  flush()
}

function track(name, data) {
  onInteract() // a click is an interaction too, so the pageview always goes out before the event
  window.umami?.track?.(name, data)
}

function onClick(e) {
  const a = e.target.closest('a[href]')
  if (!a) return
  const url = new URL(a.href, location.href)
  if (url.pathname.endsWith('.pdf')) return track('cv-open')
  if (url.protocol === 'mailto:') return track('email-click')
  if (url.origin !== location.origin) return track('outbound-link', { host: url.hostname })
}

export function initAnalytics() {
  if (!import.meta.env.PROD || !websiteId || isLocal() || looksAutomated()) return

  const script = document.createElement('script')
  script.defer = true
  script.src = src
  script.dataset.websiteId = websiteId
  script.dataset.domains = domains
  script.dataset.autoTrack = 'false' // no automatic pageview; the gate above sends it
  script.addEventListener('load', () => {
    scriptReady = true
    flush()
  })
  document.head.append(script)

  INTERACTIONS.forEach((type) => window.addEventListener(type, onInteract, { capture: true, passive: true }))
  document.addEventListener('click', onClick)
  say('Visits are counted with Umami, which uses no cookies and does not follow you across sites.')
}
