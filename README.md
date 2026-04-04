# KEKWClips

A single-file browser tool for monitoring Kick.com live streams in real time. Detects KEKW emote spikes in chat, logs highlights with clip thumbnails and links, and tracks detailed session statistics across multiple monitoring sessions.

**No install. No server. No dependencies.** Open `index.html` in Chrome or Edge and go.

🔗 **Live:** [itsavibecode.github.io/kewkchat](https://itsavibecode.github.io/kewkchat)  
📁 **Repo:** [github.com/itsavibecode/kewkchat](https://github.com/itsavibecode/kewkchat)

---

## Quick Start

1. Download `index.html`
2. Open in Chrome or Edge
3. Type a Kick streamer's username → **CONNECT**

---

## Features

### Spike Detection
- Configurable **Min KEKWs**, **Window (sec)**, and **Cooldown (sec)**
- Click **✓ APPLY SETTINGS** to apply without reconnecting
- Live KEKW rate bar graph (last 60 seconds, 1 count per message)
- Window counter shows real-time accumulation: `window: 4/10`
- `🧪 TEST SPIKE` button to verify the highlight log is working

### Highlight Log
| Column | Description |
|---|---|
| VOD TIME | Timestamp relative to stream start |
| KEKWs | Exact count, purple scaled light→dark by intensity |
| VIEWERS | Viewer count at spike |
| ΔVIEW | Viewer change since previous spike (dark red bubble ≥15k) |
| UNIQ | Unique chatters in the rolling 60s window |
| WALL TIME | Real clock time |
| TOP SPAMMERS | Purple tag bubbles, darker = more KEKWs |
| HOT WORDS | Top 5 chat words at spike moment |
| FRAME / CLIP | Thumbnail + clip title, clipper username, link |

- **💰 dono bubble** — appears under HOT WORDS if a tip was recorded around the spike. Hover for tipper name, amount, and time.
- **📎 Clip filter** — toggle to show only spikes that have clips attached
- **All-time record rows** highlighted with purple left border

### Clip Finding
Kicks's clip creation API is blocked by CORS from local files. Instead, KEKWClips searches for clips **already created by viewers** near each spike:

1. Spike fires at T+0
2. Countdown shows `🔍 10s`, `🔍 9s`… in the clip cell
3. **First search at T+10s** — checks Kick's clips API for clips within ±30s of spike
4. If not found → countdown resets, **second search at T+30s**
5. If not found → **third search at T+60s**
6. After all attempts → shows `No clip found`
7. Each clip can be used by at most **2 spikes** (deduplication)
8. Clip thumbnail shown in the frame column; falls back to stream thumbnail

### Header Bar
Stream Duration · Viewers · Unique Chatters/min · Date/Time · Total KEKWs · Spikes · All Time High · Stream Title · Category

**Monitoring section** (upper right): monitoring duration above "MONITORING ●", streamer name

**📷 Screenshot button** — exports a 5:7 PNG with:
- Stream info, streamer name, category
- "Stats based on monitored duration of: Xhr Ym Zs"
- Full-session KEKW rate bar graph with spike markers
- 6-stat grid (stream duration, viewers, KEKWs, spikes, ATH, unique chatters)
- Top 3 KEKW leaderboard
- Top 5 word cloud bubbles
- Timestamped footer with monitoring start/end and timezone

### Right-Side Panels
Each panel has a **📷 camera icon** to export a 3:2 (840×560) color-accurate PNG.

| Panel | Description |
|---|---|
| 🔴 KickSupport Watch | Logs KickSupport messages with VOD time, viewers, wall clock. Sound alert. |
| ✅ Verified Watchers | Verified Kick partners in chat. Excludes bots. Auto-expanding. |
| CX Detector | Fires when 10+ distinct users send CX in a rolling window. Shows `X/10` pending count. |
| 💰 Pocket Watcher | Tips + gifted subs leaderboards from KickBot messages. KPP estimate. |
| 🅵 F Detector | Groups F-spam into events (red theme) with start/end VOD + wall time. |
| 🔇 Muted Detector | Same as F Detector for "muted" messages (blue theme). |
| 🚨 Spammer Detector | Flags users repeating 5+ word messages 3+ times. Skips emote messages. |

### Sidebar (Collapsible Panels)
- **📡 Channel** — username input, OAuth token (masked), favourites as tag bubbles
- **⚡ Spike Detection** — threshold, window, cooldown, Apply button
- **🎮 Monitor Controls** — Connect, Clear Log, Session History, Test Spike
- **🏆 KEKW Leaderboard** — overall session leaderboard
- **☁️ Word Cloud** — top chat words, emotes/emoji filtered out

### Session History
Click **📊 Session History** to open the overlay. Sessions are grouped by streamer. Each card shows:
- Stream title + category
- ATH spike, total KEKWs, spike count
- Duration, peak viewers
- Tips total (USD), gifted subs total, KPP estimate
- Connect time + disconnect time
- Comparison bar (this session vs all sessions)
- Click to expand full spike log

### Pocket Watcher — KPP
**Kick Projected Payout** estimates hourly revenue using: `$10 per 100 average viewers per hour`.  
Samples viewer count every 30 seconds. Shows avg viewers, KPP/hr, and running total.

### Auto-Reconnect
On disconnect: red centre-screen overlay with descending tone alert. Auto-retries at 10s → 15s → 20s → … → 60s. Overlay auto-dismisses on successful reconnect. Retry count shown.

---

## Getting Your OAuth Token (Optional)

The token is not required for monitoring or clip finding. It's kept for future use.

1. Open [kick.com](https://kick.com) and log in
2. Press `F12` → Network tab
3. Filter by `api/v2`
4. Click any request → Headers → copy value after `Bearer `

> **Note:** "Login with Kick" via OAuth requires a registered app with a server redirect URI — not possible from a local HTML file.

---

## Limitations

| Issue | Status |
|---|---|
| Clip creation | Blocked by CORS. Viewer clip search is used instead. |
| Exact frame capture | Stream thumbnail has ~30s delay. Clip thumbnail used when found. |
| Verified streamer detection | Best-effort — reads `identity.badges[].type` from WebSocket payload |
| Captions/transcripts | No public Kick API. Future enhancement. |
| Login with Kick | Requires server-side redirect URI. Not feasible from local HTML. |

---

## Changelog

### v0.25
- **Fixed:** Screenshot export crashed with `Cannot access 'gridTop' before initialization` (TDZ bug from v0.23 bar graph insertion)
- Panel export (📷) doubled to 840×560px
- Panel export now reads computed CSS colors from DOM — usernames, counts, labels match their live colors
- Updated README

### v0.24
- `index.html` — renamed from `kekw-detector.html` for GitHub Pages compatibility
- `404.html` — custom 404 page with animated KEKW, links back to index
- **Clip thumbnail** — tries multiple proxy strategies + falls back to direct `img.src` + derives thumbnail from clip ID pattern
- **Countdown fix** — shows `🔍 Ns` ticking down, then `🔍 searching… (N/3)`, then `No clip found` on exhaustion
- **Reconnect fix** — disconnect overlay auto-dismisses when WebSocket reconnects
- **HOT WORDS column** — top 5 chat words at each spike captured and shown as purple tags
- **💰 dono bubble** — gold bubble in HOT WORDS if tips were recorded around the spike; hover tooltip shows tipper details
- **📎 Clip filter** — toggle in log bar to show only entries with clips
- **Panel 📷 export** — all 9 panels (Verified Watchers, KickSupport, CX, Pocket Watcher, F, Muted, Spammer, Leaderboard, Word Cloud)
- `hasClip` flag set on spike objects when clip is found, used by filter

### v0.23
- Multi-attempt clip search: T+10s, T+30s, T+60s
- Clip accept window expanded: 30s before spike to 90s after spike
- Live countdown in clip cell while searching
- KEKW rate bar graph added to screenshot export (full session, with spike markers)
- Canvas height expanded to 980px for bar graph

### v0.22
- Clip deduplication — `clipUsageCount` Map ensures same clip used at most twice
- Top 5 word cloud bubbles added to screenshot export (purple pills with frequency)
- Canvas expanded to 860px

### v0.21
- Proxy list expanded to 5 options, shuffled randomly to prevent rate limiting when multiple tabs open
- Screenshot version number corrected
- Screenshot footer condensed: one-line start→end format with timezone

### v0.20
- Panel renames: "Pocket Watcher", "Verified Watchers"
- Sound ON by default at load
- F Detector = red theme, Muted Detector = blue theme (CSS ID overrides for badge specificity)
- Frame + Clip merged into single column with thumbnail, title, clipper name
- Screenshot: "Stats based on monitored duration of:" label above stats grid
- Screenshot: detailed timestamp footer (captured, start, end, timezone)

### v0.19
- OAuth modal `display:none` by default (was rendering inline, breaking layout)
- Close button + backdrop click work correctly
- Tooltips render at `<body>` level — no longer clipped by `overflow:hidden` containers
- Session history records connect/disconnect wall times
- Screenshot: monitoring duration + top 3 KEKW leaderboard

### v0.18
- KPP (Kick Projected Payout) section in Pocket Watcher
- Session history: stream title, category, tips, gifted subs, KPP
- OAuth ? HELP modal with DevTools guide
- Disconnect alert: red overlay, sound, auto-retry with backoff
- Tooltips on panels and spike detection inputs
- 📷 Screenshot button (5:7 PNG)

### v0.17
- Clip thumbnail fetched from clips API response and shown in frame column
- `fetchProxyImage` helper shared across thumbnail fetching

### v0.16
- Clip URL: `kick.com/{slug}/clips/{id}` format (was returning raw .m3u8)
- Stream Title + Category chips in header
- Unique Chatters/min in header next to Viewers
- Monitoring header: duration above label, streamer name inline

### v0.15
- Clip button re-enabled on clip found (was staying disabled)
- Monitoring section: 3 items horizontal left-to-right

### v0.14
- Panel order standardised
- Verified Watchers panel max-height increased

### v0.13
- **Critical fix:** `recordSpike` crashed due to removed DOM elements (`s-record`, `s-spikes`, `s-total`) — null reference
- `setEl()` null-safe DOM helper added

### v0.12
- **Critical fix:** Spike detection rewritten with console logging
- TEST SPIKE button added
- Chat promoted to own full column (4-column layout)
- CX Detector: 10+ distinct users required; pending count shown

### v0.11
- **Critical fix:** KEKW regex used ES2018 lookbehind — threw `SyntaxError` in older Chrome/Edge, silently swallowing all chat messages. Replaced with `\bKEKW\b`
- `ws.onmessage` errors now logged to console
- CX Detector: purple theme + CX icon

### v0.10
- CX Detector panel (standalone CX from 10+ users)
- Apply Settings button in Spike Detection panel
- Spammer detector skips emote-leading messages
- KickBot, BotRix and other bots excluded from Verified Watchers
- Pocket Watcher totals displayed

### v0.09 and earlier
- Session history, leaderboard panels, clip finder, chart, word cloud, all core panels established

---

## File Structure

```
index.html   — main app (single file, no dependencies)
404.html     — custom 404 page
README.md    — this file
```
