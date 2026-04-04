# KEKWClips v0.18

A single-file browser tool for monitoring Kick.com live streams in real time. Detects KEKW emote spikes in chat, logs highlights with thumbnails and clip links, and tracks detailed session statistics.

**No install needed** — open `kekw-detector.html` in Chrome or Edge and go.

---

## Features

### Real-Time Monitoring
- Connects to any Kick channel's live chat via WebSocket (Pusher)
- Auto-resolves chatroom ID from streamer username — no manual lookup
- Case-insensitive channel name input

### KEKW Spike Detection
- Configurable threshold, rolling time window, and cooldown
- Live bar graph showing KEKW message rate (last 60 seconds)
- Window counter shows real-time accumulation toward the spike threshold
- Toast notifications for spikes (green) and all-time records (purple)
- Sound alerts (toggle on/off)

### Highlight Log
- Every spike is logged with: VOD timestamp, exact KEKW count, viewer count, viewer delta, unique chatters, wall time, top spammers (purple tag bubbles), stream thumbnail, and clip link
- KEKW count color scales light→dark purple with intensity
- Viewer delta shown as dark red bubble when gain ≥15k
- Auto-searches Kick's clips API 10 seconds after each spike; uses the closest clip within 30 seconds of the spike time
- Clip thumbnail replaces the stream thumbnail in the frame column once found

### Header Bar Stats
- Stream Duration, Viewers, Unique Chatters/min, Date/Time, Total KEKWs, Spikes, All Time High
- Stream Title and Category fetched at connect time
- Monitoring duration displayed above streamer name in upper right
- 📷 Screenshot button exports a 5:7 PNG of all stats

### Chat Column
- Full-width live chat with KEKW messages highlighted in purple
- Rolling 60-second unique chatter count
- Scroll-to-bottom button

### Right-Side Panels (top to bottom)
| Panel | What it does |
|---|---|
| 🔴 KickSupport Watch | Logs all KickSupport messages with VOD time, viewers, wall clock. Sound alert. |
| ✅ Verified Streamers | Tracks verified Kick partners who appear in chat. Excludes bots. Auto-expanding height. |
| CX Detector | Fires when 10+ distinct users send CX/Cx/cx in a rolling window. Shows pending count. |
| 💰 Pocket Watchin | Parses KickBot tip and gifted sub messages into leaderboards with totals. Includes KPP estimate. |
| 🅵 F Detector | Groups F-spam waves into events with start/end VOD and wall times. |
| 🔇 Muted Detector | Same as F Detector but for "muted" messages. |
| 🚨 Spammer Detector | Flags users repeating the same 5+ word message 3+ times. Ignores emote messages. |

### Pocket Watchin — KPP (Kick Projected Payout)
Estimates hourly revenue using the formula: **$10 per 100 average viewers per hour**. Samples viewer count every 30 seconds and shows a running estimate.

### Sidebar
- Collapsible panels: Channel config, Spike Detection (with Apply button), Monitor Controls, KEKW Leaderboard, Word Cloud
- Favourite channels saved as tag bubbles (one-click load)
- OAuth token field is masked when not focused

### Session History
- Every spike is saved to localStorage
- Sessions are grouped per streamer
- Each session card shows: stream title, category, ATH spike, total KEKWs, spike count, duration, peak viewers, tips (USD), gifted subs, KPP estimate
- Comparison bar shows this session's ATH relative to all sessions
- Click a card to expand the full spike log

---

## Getting Started

1. Download `kekw-detector.html`
2. Open it in Chrome or Edge (Firefox works but CORS proxy behaviour may vary)
3. Type a Kick streamer's username in the **Channel Name** field
4. Click **CONNECT**

### Spike Detection Settings
| Setting | Default | Effect |
|---|---|---|
| Min KEKWs | 10 | Messages containing KEKW in the window needed to fire |
| Window (sec) | 10 | Rolling time window |
| Cooldown (sec) | 30 | Minimum gap between spikes |

Click **✓ APPLY SETTINGS** to apply changes without reconnecting.

### OAuth Token (Optional)
The token is not required for clip finding. It is kept for potential future use.

**How to get your token:**
1. Open kick.com and log in
2. Press F12 → Network tab
3. Filter by `api/v2`
4. Click any request → Headers panel → copy the value after `Bearer `

Click the **? HELP** button in the Channel panel for the full guide.

> **Note:** "Login with Kick" via OAuth requires a registered Kick developer app with a server-side redirect URI — not possible from a local HTML file.

---

## Auto-Reconnect
If the stream disconnects, a red overlay appears centre-screen with a sound alert. The app automatically attempts to reconnect at increasing intervals (10s, 15s, 20s... up to 60s). You can also reconnect manually or dismiss the overlay.

---

## Known Limitations

| Issue | Status |
|---|---|
| Clip creation via API | Blocked by CORS (Kick requires cookies + session token server-side). Clip finding from viewer clips is used instead. |
| Exact frame capture at spike | Stream thumbnail has ~30s delay. Clip thumbnail is used when a nearby clip is found. |
| Login with Kick | Requires registered Kick app + server redirect URI — not feasible from local HTML. |
| Verified streamer detection | Reads `identity.badges[].type` from WebSocket payload — best-effort, not guaranteed for all message types. |
| Captions/transcripts | Kick has no public caption API. Future enhancement requiring server-side Whisper. |

---

## Changelog

### v0.19
- OAuth token "? HELP" modal now properly hidden on load (missing  CSS fixed)
- Close button and backdrop click both dismiss the OAuth modal correctly
- Tooltips now render at document body level — no longer clipped by  column containers
- Session history records connect wall time and disconnect wall time, shown on session cards
- Screenshot PNG includes monitoring duration and top 3 KEKW leaderboard

### v0.18
- Clip search restricted to ±30 seconds of spike time
- Clip thumbnail used as the highlight log frame (replaces stream thumbnail once clip is found)
- Verified Streamers panel auto-expands — no fixed max height
- Pocket Watchin totals displayed in larger font
- KPP (Kick Projected Payout) section added to Pocket Watchin ($10/100 viewers/hr formula)
- Session history now includes: stream title, category, tips total, gifted subs total, KPP estimate
- OAuth token ? HELP button with step-by-step DevTools guide
- Disconnect alert: centre-screen red overlay with sound, auto-retry with backoff (10s → 60s), retry counter
- Tooltips on all panels (hover icon) and spike detection inputs
- 📷 Screenshot button in header exports a 5:7 PNG of all stats

### v0.17
- Clip thumbnail: the clips API `thumbnail` field is now fetched via proxy and replaces the stream capture
- `fetchProxyImage` helper shared between clip thumb and stream thumb fetching

### v0.16
- Clip URL format fixed to `kick.com/{slug}/clips/{id}` (was returning raw .m3u8 playlist)
- Stream Title and Category chips added to header bar
- Unique Chatters/min chip added to header bar next to Viewers
- Monitoring header redesigned: duration above "MONITORING ●" label, streamer name to the right

### v0.15
- Clip button re-enabled after clip is found (was staying disabled)
- Monitoring section layout: 3 items now horizontal left-to-right

### v0.14
- Panel order: KickSupport Watch → Verified Streamers → CX Detector → Pocket Watchin → F Detector → Muted Detector → Spammer Detector
- Verified Streamers panel max-height increased to 220px

### v0.13
- Fixed crash in `recordSpike` caused by removed DOM elements (`s-record`, `s-spikes`, `s-total`)
- Added `setEl()` null-safe DOM helper used throughout
- Added hidden carrier elements for stat IDs referenced by JS

### v0.12
- Spike detection rewritten with console logging for debugging
- TEST SPIKE button added to Monitor Controls
- Live chat promoted to its own full column (4-column layout)
- CX Detector: now requires 10+ distinct users; shows pending count

### v0.11
- KEKW detection regex fixed: removed ES2018 lookbehind (`(?<!...)`) that threw SyntaxError in older Chrome/Edge — root cause of all spike detection failures from v0.09 onwards
- `ws.onmessage` error handler now logs to console instead of silently swallowing
- CX Detector panel: purple theme + CX icon

### v0.10
- CX Detector panel added (standalone CX detection)
- Apply Settings button in Spike Detection panel
- Spammer detector skips emote-leading messages
- KickBot, BotRix and other bots excluded from Verified Streamers
- Pocket Watchin totals added

### v0.09
- Clip finder: searches Kick clips API for viewer clips near spike time
- KEKW Leaderboard, Monitor Controls, Word Cloud moved to collapsible sidebar panels
- Redundant stats row removed from sidebar (shown in header)
- Session history: spike events stored to localStorage with per-streamer grouping

### v0.08
- KEKW icon embedded in chart bars and logo
- Collapsible Channel and Spike Detection config panels
- F Detector and Muted Detector event panels
- Verified Streamers reads `identity.badges[].type`
- Monitoring duration in header

### v0.07
- Viewer delta column with big-gain bubble
- Top spammers as purple tag bubbles (color scales with count)
- Unique chatters (60s rolling) and scroll-to-bottom in chat panel
- Spammer Detector, Verified Streamers, KickSupport Watch, Pocket Watchin, Word Cloud panels
- Session history stored in localStorage
- Toast duration extended; ATH uses purple toast

---

## Repo
[github.com/itsavibecode/kewkchat](https://github.com/itsavibecode/kewkchat)
