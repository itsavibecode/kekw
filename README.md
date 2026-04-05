# KEKWClips v0.32

A single-file browser tool for monitoring Kick.com live streams in real time. Detects KEKW emote spikes, logs highlights with clips and thumbnails, and tracks session statistics. No install, no server, no dependencies.

🔗 **[itsavibecode.github.io/kekw](https://itsavibecode.github.io/kekw)**  
📁 **[github.com/itsavibecode/kekw](https://github.com/itsavibecode/kekw)**

---

## Files
```
index.html   — main app (single file, ~216KB, fully self-contained)
404.html     — custom 404 page with animated KEKW
README.md    — this file
```

---

## Quick Start
1. Download `index.html`
2. Open in Chrome or Edge
3. Type a streamer's username → **CONNECT**

---

## Features

### Spike Detection
- Configurable Min KEKWs / Window (sec) / Cooldown (sec) in ⚙️ Settings & Controls
- Live KEKW rate bar graph (last 60 seconds)
- `🧪 TEST SPIKE` button to verify the log is working
- ✓ APPLY SPIKE SETTINGS without reconnecting

### Highlight Log Columns
| Column | Notes |
|---|---|
| VOD TIME | **Clickable** → opens kick.com/{slug}/videos?t=N at that exact timestamp |
| KEKWs | Purple scaled by intensity. 💰 dono bubble below count if tip was near spike |
| VIEWERS | Count at spike |
| ΔVIEW | Delta since previous spike. Dark red bubble if ≥15k gain |
| UNIQ | Unique chatters in rolling 60s window |
| WALL TIME | Real clock |
| TOP SPAMMERS | Flex-wrap purple tag bubbles |
| HOT WORDS | Top 5 words from **chat during the spike window** (not cumulative word cloud). Compact tags with ×count |
| FRAME / CLIP | Thumbnail + clip title (linked) + clipper username |

- **📎 Clip filter** — show only spikes with confirmed clips
- **💰 dono bubble** — click to show/hide tooltip (tipper, amount, time)
- Record spikes have a purple left border

### Clip Finding
Viewer clips are searched at T+10s, T+25s, T+45s after spike. Accepts clips −45s to +120s from spike. Each clip used at most twice. Hard 90s fallback prevents stuck "searching" state.

### Right Column Panels (each has 📷 export)
| Panel | Theme | What it tracks |
|---|---|---|
| 🔴 KickSupport Watch | Dark red | Messages from KickSupport account with VOD+wall+viewers |
| ⚡ Verified Watchers | Green | Verified Kick partners in chat with last message + timestamp |
| CX Detector | Purple | CX waves from 10+ distinct users |
| 💰 Pocket Watcher | Gold | Tips + gifted subs from KickBot. KPP estimate. |
| 🅵 F Detector | Red | F-spam event groups |
| 🔇 Muted Detector | Blue | Muted-spam event groups |
| 🚨 Spammer Detector | Orange | Repeat message spammers |

### Panel PNG Exports (📷 button, uniform badge|cam|▼ alignment)
- **Verified Watchers** — 840×Npx, 2-column layout with KV badge, name, msg count, last message + timestamp
- **KickSupport Watch** — 840×Npx, meme-style large message per entry, VOD time, wall time, monitored duration
- **Muted Detector** — 840×Npx, ranked by count descending, start/end VOD + wall timestamps per event
- **Word Cloud** — 840×560px, visual cloud with word bubbles sized by frequency
- All other panels — 840×560px color-accurate DOM renderer

### Sidebar
- 📡 **Channel** — slug, favourites, Connect/Disconnect button
- ⚙️ **Settings & Controls** — Spike detection, OAuth token, Custom alert sound (MP3/WAV/OGG stored in browser), Clear/History/Test
- 🏆 **KEKW Leaderboard** — session leaderboard with 📷 export
- ☁️ **Word Cloud** — top chat words with 30s refresh countdown

### Header Bar 📷 Screenshot (500×825px)
- Streamer + **STAT OVERVIEW** subtitle
- Stream title, category
- "Stats based on monitored duration of: Xhr Ym Zs"
- KEKW last-60s bar graph with count labels and KEKW icon strip
- 6-stat grid (stream duration, viewers, KEKWs, spikes, ATH, unique chatters)
- Top 3 KEKW leaderboard
- Top 5 word cloud bubbles
- Timestamped footer (captured, start, end, timezone)

### Session History
Cards grouped by streamer showing: stream title, category, ATH spike, total KEKWs, spike count, duration, peak viewers, tips (USD), gifted subs, KPP estimate, connect/disconnect wall times.

### Auto-Reconnect
Red centre-screen overlay with descending tone. Retries 10s → 15s → … → 60s. Auto-dismisses on reconnect.

### Mobile (≤ 900px)
Tab-bar navigation: ⚙️ Settings | 📊 Log | 💬 Chat | 📋 Panels. Desktop layout completely unchanged above 900px.

---

## Data Storage

| Key | Content | Typical size |
|---|---|---|
| `kekwclips_sessions` | All session history (up to 100 sessions) | ~50–200 KB |
| `kekwclips_favs` | Favourite channel names | <1 KB |
| `kekwclips_custom_sound` | Base64 audio file if uploaded | Up to ~3 MB |

Stored in **browser localStorage** (device-local, no server). Data persists until you clear browser data or use the Clear button. Future enhancement: optional cloud sync via a simple backend.

---

## Gifted Subs Detection
Currently parsed from KickBot messages matching: `"X just gifted N subs"`. Alternative sources:
- The Kick API `/v2/channels/{slug}/gifted-subscriptions` (requires OAuth, not yet implemented)
- WebSocket subscription events (Pusher channel `channel.subscription_gifted`) — could be added as a future listener

---

## VOD Linking
Each VOD timestamp in the highlight log is a clickable link to `kick.com/{slug}/videos?t=N` where `N` is the seconds elapsed since stream start. Kick's VOD player seeks to that position automatically.

---

## Changelog

### v0.32
- **Pocket Watcher:** Full username now captured (e.g. "Tazo is gay" from "Tazo is gay just tipped $5.00!") using greedy regex matching everything before "just tipped"
- **Hot words:** Now captures words from rolling 60s chat window at spike time — not the cumulative word cloud. Tags are compact flex-wrap with bold ×N count
- **Verified Watchers:** Stores last message + timestamp per watcher; shows them in panel and PNG export
- **Verified Watchers panel icon:** Uses KV badge image instead of ✅
- **Panel headers:** Uniform badge | 📷 | ▼ alignment across all panels
- **KickSupport Watch export:** Meme-style large message with VOD timestamp, wall time, monitored duration
- **Muted Detector export:** Ranked by count descending, start/end timestamps per event
- **Verified Watchers export:** 2-column layout with KV badge, last message, timestamp
- **VOD timestamps:** Clickable — opens Kick VOD at exact spike position
- **Stats PNG:** Resized to 500×825, "STAT OVERVIEW" subtitle added
- **Clip search:** 90s hard timeout prevents stuck "searching (3/3)" state
- **v0.31:** Mobile responsive layout with @media (max-width:900px) tab navigation

### v0.31
- Mobile responsive: @media (max-width:900px) tab-based layout (Settings/Log/Chat/Panels)
- Fixed layout collapse bug from v0.29 sidebar restructure (stray </div> breaking 4-column grid)
- kickverified.png embedded as base64 for Verified Watchers badge

### v0.30
- kickverified.png badge embedded in Verified Watchers panel
- Fixed 4-column desktop layout (was collapsed to single column due to misplaced </div>)

### v0.29
- Spam tags: flex-wrap responsive cloud style
- Clip filter rewritten: only shows confirmed hasClip=true rows
- Sidebar: ⚙️ Settings & Controls panel (merged spike + OAuth + monitor)
- Connect button moved into Channel panel
- Custom alert sound: upload MP3/WAV/OGG, stored in localStorage as base64
- Word cloud PNG: fixed number overlap
- Chart PNG: KEKW icons below bars

### v0.28
- Favicon set to KEKW icon
- Hot words show count (word ×N)
- Dono bubble moved to KEKWs column with click-tooltip
- Tooltip system: hover (data-tip) + click-toggle (data-click-tip)
- Clip counter 4/3 bug fixed
- F badge=blue, Muted badge=red (corrected)
- Toast colors: F=blue, Muted=red, CX=purple
- Right column scrollable independently
- Clip thumbnail: /clips/{channelId}/{clipId}/thumbnail.webp format
- Screenshot bar graph: 60s live chart with KEKW icon row

### v0.27
- tipsLog per-tip event log with timestamps
- Dono bubble: one tip → one spike (120s window)
- Chart 📷 export button (900×200 PNG)
- Screenshot fonts enlarged

### v0.26
- Word cloud: live status + 30s refresh countdown
- Clip searches: T+10s/25s/45s, accept window −45s to +120s

### v0.25
- Fixed screenshot crash (gridTop TDZ bug)
- Panel export doubled to 840×560, color-aware DOM renderer

### v0.24
- index.html renamed for GitHub Pages
- 404.html custom page
- Clip thumbnail multi-proxy with webp CDN format
- Countdown: 🔍 Ns → 🔍 searching (N/3) → No clip found
- Reconnect overlay auto-dismisses
- HOT WORDS column + dono bubble
- Clip filter toggle
- All panel 📷 exports

### v0.23
- Multi-attempt clip search (T+10s/30s/60s)
- Clip accept window: 30s before → 90s after spike
- KEKW bar graph in screenshot

### v0.22
- Clip deduplication (max 2 uses per clip)
- Top 5 word cloud bubbles in screenshot

### v0.21
- Proxy list: 5 options, shuffled per connect to prevent rate-limiting
- F/Muted badge color fix

### v0.20 and earlier
- Panel renames, sound defaults, F/Muted themes, merged Frame+Clip column, screenshot improvements
