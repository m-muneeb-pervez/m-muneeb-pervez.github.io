// Privacy-friendly visit counts via Umami (no cookies, no tracking across sites).
// Active only in production builds, never on localhost, and only when a website ID is set.

const websiteId = import.meta.env.VITE_UMAMI_WEBSITE_ID
// Umami Cloud by default. For a self-hosted Umami, set VITE_UMAMI_SRC to its script URL.
const src = import.meta.env.VITE_UMAMI_SRC || 'https://cloud.umami.is/script.js'
const note = document.getElementById('analytics-note')

function say(text) {
  if (!note) return
  note.textContent = text
  note.hidden = false
}

function isLocal() {
  return /^(localhost|127\.|0\.0\.0\.0|10\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.)|\.local$/.test(location.hostname)
}

function optedOut() {
  return (
    navigator.doNotTrack === '1' ||
    window.doNotTrack === '1' ||
    navigator.globalPrivacyControl === true
  )
}

function track(name, data) {
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
  if (!import.meta.env.PROD || !websiteId || isLocal()) return

  if (optedOut()) {
    say('Your browser asks not to be tracked, so this visit is not counted.')
    return
  }

  const script = document.createElement('script')
  script.defer = true
  script.src = src
  script.dataset.websiteId = websiteId
  script.dataset.doNotTrack = 'true'
  document.head.append(script)

  document.addEventListener('click', onClick)
  say('Visits are counted with Umami, which uses no cookies and does not follow you across sites.')
}
