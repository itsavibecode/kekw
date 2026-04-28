# KEKWClips — BETA v0.47

A single-file browser tool for monitoring Kick.com live streams in real time. Detects KEKW emote spikes, logs highlights with clips/thumbnails, and tracks detailed session statistics. No install, no server, no dependencies.

🔗 **[itsavibecode.github.io/kekw](https://itsavibecode.github.io/kekw)**  
📁 **[github.com/itsavibecode/kekw](https://github.com/itsavibecode/kekw)**

---

## Files
```
index.html   — main app (~400KB, fully self-contained)
404.html     — custom 404 page with animated KEKW
README.md    — this file
```

---

## Quick Start
1. Download `index.html`
2. Open in Chrome or Edge
3. Enter a Kick streamer's username → **CONNECT**

---

## Changelog

### v0.47
- **Column order fix**: `clips-col` was previously appended after `right-col`'s closing tags, falling outside the CSS grid container. HTML order now matches the grid order exactly: `sidebar | main | chat-col | clips-col | right-col`
- Removed mislabeled `<!-- ══ RIGHT COL ══ -->` comment that was sitting above the chat-col block

### v0.46
- **Stream offline auto-detect**: `parseChannelData` extracts `isLive` from `livestream.is_live || !!livestream.id`. `refreshStreamInfo` polls every 2 minutes; after 2 consecutive offline polls (4-min grace) it saves the session and disconnects with toast *"📴 Stream ended — auto-disconnecting"*
- **Clips column** added as 5th grid column. Layout: `260px 1fr 200px 210px 190px` — sidebar | main | chat+WC | stats panels | clips. 📎 Clips tab added to the mobile tab bar
- **Strict 1 use per clip ID** (was max 2). Picker skips any clip already in `clipUsageCount`; falls back to least-used if all are taken
- **90-second clip duration filter** in `withinWindow` — avoids picking highlight reels or VOD clips
- **Spike export PNG rebuilt**: 800×600 canvas with right-side clip info box (210px wide, thumbnail + title + clipper + duration + source). Top Chatters now rendered as styled tag bubbles matching Hot Words. Clip metadata (`clipTitle`, `clipper`, `clipDuration`) stored on the spike object at find time for reliable export

### v0.45
- **KickBot detection**: regex pulls `kickbot.com/clip/` URLs plus the mentioned `@username` (or `username just created…` pattern) out of chat. Each entry is added to the **🤖 Chat Clips** panel and assigned to the nearest unclipped spike within 3 minutes
- **Dual clip panels**: 🎬 Streamer Clips (green) and 🤖 Chat Clips / KickBot (blue), collapsible, at the bottom of the right column
- **Kickclipify** added as 5th clip endpoint: `kickclipify.com/{slug}?sort=date&time=day`. `extractClips()` detects HTML responses (looks for `<html`) and regex-parses `kick.com/.../clips/...` URLs out of the page
- **Stats PNG bar graph fix**: `kpmS` (KEKW/min average) computed before the bar graph renders so it can appear in the chart header. Bars now divide the full session into up to 50 equal-width buckets with spike counts plotted per bucket. Time axis labels at `0m`, midpoint, end
- **🎬 AUTO-CLIP button** at bottom of Settings & Controls. When enabled (turns green, requires OAuth token), every spike triggers `checkAutoClip()` which fires `!clip 60` only if chat message rate in the last 10s is ≥2× prior 10s AND 90s cooldown has elapsed. KickBot's reply is then caught by the chat detector
- **Green neon footers**: all 10 export PNG functions draw a `#53fc18` rectangle behind footer text with `#000` text on top

### v0.44
- **Word Cloud moved**: removed from sidebar, now lives as a collapsible `rpanel` at the top of the chat column, directly above Live Chat. Has its own ↺ refresh, 📷 export, collapse arrow, and countdown label inside the panel body
- **Clip search rewrite** addressing the 1/209 clip success rate:
  - Wider time window: `−2m to +5m` from spike (was `−45s to +120s`)
  - 4 search attempts at `T+15s/40s/90s/180s` (was 3 attempts at T+10s/25s/45s)
  - All 4 API endpoints tried per attempt: v2 day, v2 week, v1 day, v2 sorted-by-views; each through all 3 proxies before moving on
  - New `extractClips()` handles every Kick response shape: `{clips:{data:[]}}`, `{data:{clips:[]}}`, `{data:{clips:{data:[]}}}`, `{clips:[]}`, `{data:[]}`
  - **UTC timestamp fix**: appends `Z` to `created_at` if no timezone is present so the browser doesn't parse it as local time (caused 5–6h offset)
  - Console diagnostics: every attempt logs endpoint, proxy, clips found, spike UTC time, nearest delta, nearest clip timestamp

### v0.43
- **Sound bug fixed**: `spike` and `record` slots had no `active` property initialized, so `s.active === 'default'` was always `undefined === 'default' = false`, causing the custom path to try a null buffer. Now initialized with `active:'default'`. `cx` and `boo` initialized with `active:'cx_bundled'` and `active:'boo_bundled'`
- **All dropdowns share all options**: Default tone/fanfare, 🐴 Ice Heehaw, 🎧 alert-cx.mp3, 🎧 alert-boo.mp3, 🔕 Off, plus any user upload. `playCustomSound` resolves `cx_bundled`/`boo_bundled` by playing that type's buffer; `off` returns true to silence without falling through
- **Word cloud countdown** moved from panel header title into a small right-aligned label inside the panel body (`wc-countdown-lbl`); header is now permanently "☁️ Word Cloud"
- **PatrickBoo PNG export**: each wave event now lists contributing usernames (up to 14, then "…") in peach below the timestamps
- **📷 Camera button on every spike row** — added in `addRow()` itself, so every spike gets a button regardless of clip status

### v0.42
- **Alert Sounds panel**: all 4 sound slots (Spike, Record Spike, CX Wave, PatrickBoo Wave) consolidated into one section
- **ice_heehaw.mp3**: embedded as base64, pre-decoded at startup, available as "🐴 Ice Heehaw" in Record Spike dropdown
- **Spike row 📷 export**: when a clip is confirmed, a 📷 button appears on that row. Exports a 4:3 800×600 PNG with spike count headline, stat boxes (KEKW/s, viewers, Δ viewers, uniq chatters), 60s bar chart snapshot, hot word tags, clip thumbnail, top chatters
- **RSS feed**: confirmed uses live in-memory session data (`highlights[]`, `cxEvents[]`, `pbEvents[]`) — exports all events from the current monitoring session on demand
- **Toast notifications**: all toasts use solid opaque backgrounds (cx-wave `#3b1f6b`, pb-wave `#7a3020`)
- **Stream title chip**: `white-space:normal`, `overflow-wrap:break-word` — title wraps instead of being clipped

### v0.41
- **Session filter**: rebuilds from localStorage on every open — all monitored streamers now appear
- **Peak Viewers**: header chip tracks session-high viewer count with VOD timestamp; included in stats PNG export
- **KEKW/min chip**: live rolling rate in header bar; included in stats PNG
- **Stats PNG**: 8 stat boxes (added Peak Viewers, KEKW/min, Avg KEKW/Spike)
- **Panel reorganisation**: Session History moved into Channel panel; Clear Log + Test Spike moved into Spike Detection
- **CX + PB events**: usernames who triggered the wave are stored and shown (up to 8 per event, truncated)
- **CX Alert sound** (`alert-cx.mp3`): bundled, pre-loaded, separate volume slider in Alert Sounds
- **PatrickBoo Alert sound** (`alert-boo.mp3`): bundled, pre-loaded, separate volume slider
- **RSS feed export**: 📡 button in Session History exports all spikes, CX events, and PatrickBoo events as XML

### v0.40
- Favourites act as channel switch when connected to a different streamer
- Disconnect button freeze fixed: `switchChannel` uses `try/finally` to always re-enable button
- `checkSlugChanged` guards against button being disabled mid-switch
- Spike detection buttons: equal `flex:1`, RESET button red with label

### v0.39
- **Save Spike Settings as Default**: 💾 DEFAULT button saves threshold/window/cooldown to localStorage; loaded automatically on next open
- **↺ RESET**: resets to factory defaults (10/10/30)
- **Channel Switching**: typing a different channel name while connected changes DISCONNECT → SWITCH TO {name}; clicking SWITCH saves the current session, resets all state, and connects to the new channel
- Favourites trigger switch if a different channel is already connected

### v0.38
- **Record spike sound logic confirmed**: `count > allTimeRecord` already strictly greater-than (a tie does NOT fire). The earlier bug was `testSpike()` passing 99 and setting `allTimeRecord=99`; fixed in v0.37 so test spikes use the threshold value
- **Patrick icon** embedded as base64; appears in the PatrickBoo panel header
- **Peach theme** for PatrickBoo: panel bg `rgba(255,179,153,.07)`, text `#ffb399`, badges + event labels + wave toast all peach. Export PNG matches

### v0.37
- **CX Detector** confirmed behaviour: fires when 10+ distinct users each send a message containing `CX` (case-insensitive, word-boundary, text only — not inside emote tags) within a rolling 8s inactivity window. Pending counter shows `7/10 unique users — waiting for threshold…`
- **PatrickBoo Detector** mirrors CX, triggers on emotes `[emote:3111349:]`, `[emote:3111350:]`, `[emote:3111348:]`, `[emote:3111346:]`, `[emote:4147892:PatrickBoo]` or words `iceposeidonppatrick1`, `iceposeidonrpatrick1`, `iceposeidonypatrick1`, `iceposeidongpatrick1`, `patrickboo`. One message = one user vote. 10+ distinct users → 🐸 wave event. Orange `#f97316`
- **Record spike sound fix**: `testSpike()` no longer passes 99 (which was incorrectly setting `allTimeRecord=99`); now passes the current threshold so test spikes behave like real ones
- **Word Cloud PNG**: 1200×800px, font range 16–52px (was 14–36px), starts at top corner, subtle purple grid background
- **CX Detector PNG**: stat boxes (Waves, Peak Unique Users, Peak Messages) + styled event log with alternating row backgrounds
- **Pocket Watcher PNG**: clean 2-column layout — stat boxes (Tips Total, Gifted Subs, KPP/hr) at top, Tips leaderboard left, Gifts leaderboard right, medal colors for ranks 1–3

### v0.36
- **Collapse/Expand All** buttons at top of sidebar and right-column panels
- **Spam threshold** raised from 3→ to 7+ repeated messages
- **Record spike alert** only fires when count is strictly greater than the all-time high (not equal)
- **Sound alerts**: per-type dropdown selector (Default / Custom: filename). Upload button adds to dropdown. Dropdown selection determines which sound plays
- **VOD links**: now uses `livestream.video.uuid` from Kick API for correct UUID-based URL
- Spike detection fields: all 3 in one compact horizontal row

### v0.35
- **BETA label** added to logo (BETA v0.35)
- **Sound system rebuilt**: two separate slots — 🔥 Spike Alert and 🏆 Record Spike Alert
- Each slot: upload button, volume slider (affects both custom and default tones)
- `customSounds` object replaces single-slot system; per-type `playCustomSound(type)`
- **Highlight log desktop fixed**: `mob-row-detail` hidden on desktop, shown only on mobile
- **Spike detection layout**: 3 fields in one row (compact)
- **VOD URL**: uses `currentLivestreamVideoId` (UUID) when available

### v0.34
- Stream title/category auto-refresh every 15 minutes
- Session history: Export (JSON), Import (merge, skip duplicates), Delete (filtered or all)
- `streamInfoTimer` declared at top level (was causing connect failure)
- Sound startup deferred to `window.load` (was crashing on null DOM elements)
- Stats PNG: `kekwIconImg` declared before bars loop (was crashing captureStats)
- KEKW icons only draw under bars with `v > 0` (matches live chart)
- Manual word cloud refresh button (↺) in panel header
- Mobile log: 4 visible columns + sub-detail row with wall time/spammers/words
- VOD timestamps now clickable links (kick.com/{slug}/videos/{id}?t=N)

### v0.33
- Fixed `winMs` duplicate `const` declaration (caused connect button to do nothing)
- Fixed broken `.toLowerCase()` in `updateWordCloud` (left from bytes replacement)

### v0.32
- **Pocket Watcher**: Full username captured — regex now matches everything before "just tipped" (e.g. "Tazo is gay just tipped $5.00!" → "Tazo is gay")
- **Hot words**: Now captures words from rolling 60s chat window at spike time, not cumulative word cloud
- Hot word tags: compact flex-wrap, bold ×N count
- Verified Watchers: stores last message + timestamp per watcher
- Verified Watchers panel icon: KV badge (kickverified.png)
- Panel headers: uniform badge | 📷 | ▼ alignment across all panels
- KickSupport Watch export: meme-style large message with VOD/wall/duration
- Muted Detector export: ranked by count desc, start/end timestamps per event
- Verified Watchers export: 2-col layout with KV badge, last message, timestamp
- Stats PNG: resized 500×825, "STAT OVERVIEW" subtitle

### v0.31
- Mobile responsive: `@media (max-width:900px)` tab-bar layout (Settings/Log/Chat/Panels)
- Fixed layout collapse bug from v0.29 sidebar restructure
- kickverified.png embedded as base64

### v0.30
- kickverified.png badge in Verified Watchers panel rows and panel title

### v0.29
- Spam tags: flex-wrap responsive cloud style
- Clip filter: only shows confirmed `hasClip=true` rows
- Sidebar: ⚙️ Settings & Controls merged panel
- Connect button moved into Channel panel
- Custom alert sound: upload MP3/WAV/OGG, stored in localStorage
- Word cloud PNG: fixed overlap
- Chart PNG: KEKW icons below bars

### v0.28
- Favicon: KEKW icon as browser tab favicon
- Hot words show ×N count inline
- Dono bubble: click-toggle tooltip with tipper/amount/time
- Tooltip system: hover (`data-tip`) + click-toggle (`data-click-tip`)
- Clip counter 4/3 bug fixed
- F badge=blue, Muted badge=red
- Toast colors: F=blue, Muted=red, CX=purple
- Clip thumbnail: `/clips/{channelId}/{clipId}/thumbnail.webp` CDN format
- Screenshot bar graph: 60s live chart with KEKW icon row

### v0.27
- `tipsLog` per-tip event log (timestamp, amount, one-spike assignment)
- Dono bubble: one tip → one spike (120s window)
- Chart 📷 export button (900×200 PNG)
- Screenshot fonts enlarged

### v0.26
- Word cloud: live "Gathering…" status + 30s refresh countdown in header
- Clip searches: T+10s / T+25s / T+45s; accept window −45s to +120s

### v0.25
- Fixed screenshot crash (`gridTop` TDZ bug)
- Panel export doubled to 840×560, color-aware DOM renderer

### v0.24
- `index.html` renamed for GitHub Pages
- `404.html` custom page with animated KEKW
- Clip thumbnail: multi-proxy with webp CDN fallback
- Countdown: `🔍 Ns` → `🔍 searching (N/3)` → `No clip found`
- Disconnect overlay auto-dismisses on reconnect
- HOT WORDS column in highlight log
- 💰 dono bubble in KEKWs column
- 📎 Clip filter toggle
- All panel 📷 exports (9 panels)
- `hasClip` flag on spikes

### v0.23
- Multi-attempt clip search: T+10s / T+30s / T+60s
- Clip accept window: 30s before → 90s after spike
- KEKW bar graph added to stats PNG

### v0.22
- Clip deduplication: max 2 uses per clip ID
- Top 5 word cloud bubbles in stats PNG

### v0.21
- Proxy list: 5 options, shuffled per connect
- F/Muted badge color fix

### v0.20
- Panel renames: "Pocket Watcher", "Verified Watchers"
- Sound ON by default
- F Detector = red, Muted Detector = blue
- Frame + Clip merged into single column
- Screenshot: monitoring duration label + timestamp footer

### v0.19
- OAuth modal: hidden on load (display:none CSS fix)
- Tooltips: body-level rendering (no overflow:hidden clipping)
- Session history: connect/disconnect wall times
- Screenshot: monitoring duration + top 3 leaderboard

### v0.18
- KPP (Kick Projected Payout) in Pocket Watcher
- Session history: stream title, category, tips, gifts, KPP
- OAuth ? HELP modal with DevTools walkthrough
- Disconnect alert: red overlay, sound, auto-retry with backoff
- Tooltips on panels and spike inputs
- 📷 Header screenshot (5:7 PNG)

### v0.17 and earlier
- Clip thumbnail from clips API
- Stream title + category in header
- Monitoring header redesign
- Core spike detection, KEKW regex fixes, panel system established

---

## Data Storage

| Key | Content | Size |
|---|---|---|
| `kekwclips_sessions` | Session history (up to 100) | ~50–200 KB |
| `kekwclips_favs` | Favourite channels | <1 KB |
| `kekwclips_sounds_v2` | Custom sounds (base64) | Up to ~3 MB each |

All data is stored in browser `localStorage` — device-local, no server. Export sessions as JSON from the Session History overlay to back them up or transfer to another device.

---

## Limitations

| Issue | Status |
|---|---|
| Clip creation via API | Blocked by CORS. Viewer clip search used instead |
| VOD UUID availability | Only available if stream is live when connecting |
| Exact frame capture | Stream thumbnail ~30s delay; clip thumbnail used when found |
| Login with Kick | Requires registered app + server redirect URI |
| Captions/transcripts | No public Kick API |

---

## Q&A

**Can the current stream video be embedded in a panel?**  
Technically yes — Kick streams are HLS (`.m3u8`). You'd need an HLS player library like `hls.js` added via CDN, then point it at `https://kick.com/api/v2/channels/{slug}` to get the playback URL. The main constraint is CORS: Kick's CDN may block cross-origin video requests from a local HTML file. It's feasible as a future panel if hosted on a proper domain.

**Can screenshots be tweeted?**  
Yes — the Web Share API (`navigator.share({files:[...]})`) can share canvas-exported PNGs on mobile. For desktop Twitter/X posting you'd need the Twitter/X API v2 with OAuth2 and a backend to handle the token exchange. A simpler approach: add a "Copy image" button that puts the PNG on the clipboard, then the user pastes into a tweet manually. The Twitter API route is doable but requires registering a developer app.
