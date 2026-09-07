# Michael Gar Fan Page - Project Guide

## Project Overview
This is a fan page website for Michael Gar, an elite British triathlete. The site showcases his achievements, career timeline, gallery, and social media presence.

## Tech Stack
- **HTML5** - Semantic markup, single page
- **CSS3** - Inline in `index.html` (built from `redesign/template.html`), CSS variables, no gradients
- **Vanilla JavaScript** - Dive-hero scroll scrub (rAF, transform/opacity only) and the news loader (`news.json` → Latest news section, hidden when empty)
- **Google Fonts** - Bebas Neue (display), Hanken Grotesk (body), JetBrains Mono (times, labels)

## Two designs: live and classic (rollback)
- **Live (root `index.html`)** - the "editorial" redesign, went live Sep 2026. Source of truth is `redesign/template.html`; `index.html` is generated from it (see Build below). Do not hand-edit `index.html` without also updating the template.
- **Classic (`classic/index.html`, served at `/classic/`)** - the previous design, kept for rollback and comparison. It uses the root `styles.css`, `images/`, `videos/`, `news.json` via `../` paths and is `noindex`. Git tag `classic-design` marks the last commit before the switch.
- **Rollback** - `git mv classic/index.html index.html` and drop the `../` prefixes (or `git checkout classic-design -- index.html`), commit, push. Render redeploys on push to main.
- **Build** - the template has placeholders (`{{IMG:file}}`, `{{VIDEO}}`, `{{RIBBON}}`, `{{TITLE}}`, `{{HEAD_EXTRA}}`, `{{FOOTER_LINKS}}`). The build script that fills them lived in the session scratchpad; regenerating is a simple substitution: images → `images/gallery/<file>`, video → `<video poster="images/haikou-poster.jpg"><source src="videos/haikou-wc-720.mp4">`, ribbon empty, footer links to `classic/` and `admin/`. `redesign/index.html` is the local demo variant (relative `../` paths, preview ribbon).
- **Video** - `videos/haikou-wc-720.mp4` (9 MB, 720p) is the committed web encode. The 89 MB original `videos/haikou-wc.mp4` stays untracked.

## Project Structure
```
/
├── index.html          # LIVE page (editorial redesign, generated from redesign/template.html)
├── redesign/           # template.html (source of truth), index.html (local demo), haikou-poster.jpg
├── classic/index.html  # Previous design, served at /classic/ (rollback + comparison)
├── styles.css          # Stylesheet for the classic page only
├── favicon.svg         # Site favicon
├── news.json           # News articles data
├── images/             # Image assets
│   ├── gallery/        # Gallery photos (local JPEGs, max 1600px, descriptive names)
│   ├── haikou-poster.jpg  # Video poster frame
│   ├── hero-poster.jpg    # Dive-hero frame 1 (LCP + OG image)
│   ├── hero-frames/       # 32 scroll-scrubbed dive frames (WebP)
│   └── gallery/hamburg-dive.jpg  # Dive-hero image (root hamburg-dive.jpeg is the classic page's copy)
│   └── news/           # News article images
├── videos/haikou-wc-720.mp4  # Featured video (web encode)
├── audio/hero-theme.m4a      # Hero music, opt-in via the Sound button
└── admin/              # Admin panel for news management
    ├── index.html      # Admin dashboard
    └── admin.css       # Admin styles
```

## Design System (live page)
"Editorial performance": dark navy ground, one teal accent, condensed uppercase display type, 1px rules instead of cards, sharp corners, no gradients, no emoji. Originated as Stitch concept A (project "Michael Gar Fan Page — Reimagined").

### Colors (CSS variables in index.html)
- `--ground`: #0a1628 · `--deep`: #060d18 · `--surface`: #10203a
- `--line`: #1e3050 · `--line-strong`: #2c4268
- `--teal`: #00d4aa (accent, primary buttons, key numbers) · `--teal-ink`: #062a24 (text on teal)
- `--ink`: #f2f5fa · `--ink-2`: #c3cddd · `--slate`: #8c9bb3 · `--silver` / `--gold` for medal rows

### Typography
- Display: Bebas Neue, always uppercase, tight leading
- Body: Hanken Grotesk 400/500/600/700
- Data and labels: JetBrains Mono, letter-spaced uppercase, tabular numerals

The classic page keeps its own system in `styles.css` (Montserrat/Open Sans, blue-teal gradients).

## Key Sections (live page, in order)
1. **Dive hero** - Pinned, scroll-scrubbed frame sequence. The camera opens on the photographer's framing, swings round behind Michael as he holds a flat streamlined dive, and rides with him into the water. Scroll position picks the frame; nothing autoplays.
   - **Source: Grok Imagine (xAI), image-to-video, 1728x1152 @24fps**, seeded with a 16:9 crop of `hamburg-dive.jpeg`. This replaced an OpenAI `sora-2` attempt that only rendered 1280x720 and was visibly soft. Original clip is 10s; the hero uses the **first 5.5s**, which runs dive to entry to surfacing into freestyle with the camera locked behind his back. Seconds 5.5-10 continue that back-mounted swim and are available if a longer hero is ever wanted.
   - Frames: `images/hero-frames/f001..f042.webp` (42 frames, 1280px downscaled from 1728 so the pixels are genuinely sharp, WebP q66, ~7.0 MB). `COUNT`/`EXT` in the inline script must match the folder. This is a deliberate weight/sharpness trade: dropping quality or resolution was rejected after repeated feedback that the hero looked soft. If it ever needs to be lighter, cut frames before cutting quality.
   - Poster: `images/hero-poster.jpg`, frame 1 downscaled from the 1728 source. The canvas only fades in past scroll 0.012, so a visitor who never scrolls sees a sharp still.
   - **Music:** `audio/hero-theme.m4a` is the audio track from the Grok clip. It NEVER autoplays - a "Sound off/on" button in the hero toggles it, the choice is remembered in `localStorage` under `mg-sound`, and a remembered "on" still waits for one pointer gesture because browsers block audio without one.
   - Debug: append `?dive=0.5` (0..1) to freeze the camera at any point for screenshots.
   - Fallbacks: static poster under `prefers-reduced-motion`, with JS off (`no-js` on `<html>`), and on `saveData`/2g connections, which skip the frames entirely.
   - Prompt lessons (see `~/Downloads/michael-dive-PROMPT.txt`): never use "down", "plunge", "descend" or "underwater" - they make the model rotate the athlete feet-up into a vertical sink that reads as drowning. Repeat "flat", "horizontal", "streamlined" more than once or the body pikes within a second. Do not name nationality, kit or "body-mounted camera"; that tripped OpenAI moderation.
   - Rejected approaches: CSS transforms over the flat photo (reads as a pan-and-zoom); scrubbing a `<video>` via `currentTime` (needs dense keyframes, which came out at 8.5 MB versus 4.75 MB for frames); AVIF frames (no smaller than WebP on spray-heavy content); upscaling frames (bytes without detail).

2. **Stat strip** - #19 WTCS standing, 2× British Champion, 2 European silvers 2026, 29:38 fastest 10 km
3. **About** - Portrait, bio, pull quote, fact list
4. **Sponsors** - Light band: 707 Team Minini, Podium Racing, C-Bear (with Michael's quote); nav link + hero button
5. **Results** - 2026 season table (position, event, date, time); medal rows highlighted
6. **Video** - Haikou World Cup (720p encode, poster frame)
7. **Gallery** - CSS column masonry (fills without holes; no fixed row spans) with hover captions. 25 photos covering Elblag, Tarragona, supertri Jersey, Miyazaki, Llanelli and 707 Team Minini. Three of them (Miyazaki podium, 707 group, Llanelli swim start) were hotlinked from third-party sites on the classic page and are now local files.
8. **Fan wall** - Three fan quotes
9. **Latest news** - Hidden until `news.json` has articles
10. **Follow** - Instagram, World Triathlon profile, British Triathlon
11. **Footer** - Disclaimer, links to `/classic/` and `/admin/`

Not carried over from classic: Instagram embed, World Triathlon ranking/starts/podiums cards (stale data), achievements timeline (folded into Results).

## News System
- **Data**: Articles stored in `news.json`
- **Fields**: id, title, date, content, image, youtubeUrl, externalLink, category
- **Categories**: announcement, race-result, training, media, other
- **Display (live)**: "Latest news" section renders up to 6 newest articles and stays hidden when the file is `[]`
- **Admin link**: "Admin" in the live footer; lock icon in the classic news header

## Admin Panel
- Located at `/admin/`
- Password protected (session-based, password: michaelgar2025)
- Form to create news articles with all fields
- Generates JSON for copy/paste into `news.json`
- Step-by-step instructions for adding articles

## Social Links
- Instagram: @michaelgar_tri
- World Triathlon: Profile ID 160628
- British Triathlon: GB Elite Team profile

## Sponsors
- 707 Team Minini (https://www.707team.com/) - racing team, Italy
- Podium Racing (https://www.podium-racing.com) - supertri team
- C-Bear (https://c-bear.com/) - ceramic bearings; quote: "I use C-Bear ceramic bearings and bottom bracket"

## 2026 Season Results (newest first)
- 2nd, Europe Triathlon Sprint Championships Elbląg (31 Jul, 54:25)
- 18th, WTCS London (25 Jul)
- 2nd, Europe Triathlon Championships Tarragona, standard distance (13 Jun, 1:47:44)
- 1st, British Elite Triathlon Championships, Llanelli (9 May) - British Champion 2026
- 19th, WTCS Samarkand (25 Apr) · 10th, World Cup Haikou (21 Mar)

## Key Features
- Responsive down to 390px, no horizontal overflow
- Sticky nav, in-page anchors, reduced-motion respected
- Sharp, rule-based layout; hover states only (no scroll animations)

## Recent Updates
- Sep 2026: Dive hero regenerated with Grok Imagine at 1728x1152 (sharp), plus opt-in hero music; gallery grew to 25 photos (3 previously hotlinked, 11 new from WhatsApp) and switched to a column layout
- Sep 2026: Editorial redesign went live at root; previous design kept at `/classic/` (tag `classic-design`); 720p Haikou video committed; Cervia women's podium photo and Tarragona full-podium photo removed from all pages
- Sep 2026: Sponsors section (707, Podium Racing, C-Bear), 11 new gallery photos (Tarragona, Elbląg, supertri Jersey), 2026 results in timeline + results table, British Champion 2026 badge, age 22
- Added News section with dynamic JSON-powered article cards
- Redesigned admin panel with modern UI, password toggle, step-by-step instructions
- Added British Triathlon profile link
- Added 707 Minini sponsor button
- Added British Champion 2025 badge
