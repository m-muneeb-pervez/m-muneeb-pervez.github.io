// Privacy-respecting visit counts via GoatCounter (no cookies, no personal data).
// Active only in production builds, and only when VITE_GOATCOUNTER_CODE is set.

const code = import.meta.env.VITE_GOATCOUNTER_CODE
const note = document.getElementById('analytics-note')

function say(text) {
  if (!note) return
  note.textContent = text
  note.hidden = false
}

function optedOut() {
  return (
    navigator.doNotTrack === '1' ||
    window.doNotTrack === '1' ||
    navigator.globalPrivacyControl === true
  )
}

function count(path, title) {
  window.goatcounter?.count?.({ path, title, event: true })
}

function onClick(e) {
  const a = e.target.closest('a[href]')
  if (!a) return
  const url = new URL(a.href, location.href)
  if (url.pathname.endsWith('.pdf')) return count('cv-open', 'CV opened')
  if (url.protocol === 'mailto:') return count('email-click', 'Email link clicked')
  if (url.origin !== location.origin) return count(`outbound/${url.hostname}`, `Link to ${url.hostname}`)
}

export function initAnalytics() {
  if (!import.meta.env.PROD || !code) return

  if (optedOut()) {
    say('Your browser asks not to be tracked, so this visit is not counted.')
    return
  }

  const endpoint = `https://${code}.goatcounter.com/count`
  window.goatcounter = { endpoint }

  const script = document.createElement('script')
  script.async = true
  script.src = 'https://gc.zgo.at/count.js'
  script.dataset.goatcounter = endpoint
  document.head.append(script)

  document.addEventListener('click', onClick)
  say('Visits are counted with GoatCounter, which sets no cookies and stores no personal data.')
}
