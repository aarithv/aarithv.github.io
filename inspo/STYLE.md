# Site aesthetic — retro terminal / green-phosphor hacker core

Summary of the shared visual language across all images in this folder. Read this first; consult the individual per-image `.md` files (same basename as each `.jpg`) only for reference on a specific asset.

## Palette
- **Foreground**: a single saturated phosphor green, roughly `#00ff41` – `#33ff66` range, used for all text, lines, and UI chrome.
- **Background**: pure or near-pure black (`#000000` – `#0a0a0a`).
- No secondary hues — this is a strictly monochrome system. Grayscale only appears in "borrowed OS chrome" moments (Windows 95/98 dialog gray, mimicking real hardware).
- Occasional muted photographic tones (dim room lighting, phone-body plastic) where a real device/environment is being photographed rather than a pure UI render.

## Typography
- Monospace throughout — either a terminal/console font or a true bitmap/pixel font (visible pixel-stepping on curves, like old LCDs and 8-bit displays).
- All-caps or sentence-case labels for headers/warnings; lowercase, more "human" text used for casual/meme content (e.g. the SMS message).
- Text density is high — walls of log/code/command text are a recurring texture, not just isolated labels.

## Recurring motifs
- **CRT/scanline artifacts**: horizontal scanlines, chromatic-aberration glitching, static/noise bands, screen glow/bloom.
- **Retro OS chrome**: Windows 95/98-style beveled dialog boxes, title bars with minimize/maximize/close, taskbars — reappropriated in green instead of the original gray/blue.
- **Terminal/console windows**: black panels with green text, framed by thin rectangular or ASCII-drawn borders.
- **Glitch/corruption**: deliberately garbled characters, ghosting, misaligned duplicate text — implies decay, hacking, or a broken system.
- **Classified/security framing**: "REDACTED", "WARNING", "SECURITY BREACH", "TRACE ROUTE", ID-card/dossier layouts, halftone-dithered portraits.
- **Real hardware photographed in the dark**: CRT monitors, feature phones — macro/photoreal shots where the glow is the only light source, grounding the digital aesthetic in tangible retro objects.
- **Deadpan tech-horror humor**: personifying computers ("distressed", "upset"), interactive-fiction-style bracketed choice menus.

## Mood / tone
Y2K nostalgia crossed with dark sci-fi and analog horror — equal parts "cool retro hacker" and "something here is a little wrong." Playful enough to support humor (the SMS message, the upset computer) but atmospheric enough to support a moody hero/landing treatment. Read as: an old terminal that still boots, in a room nobody has cleaned out.

## Translating to the actual website
- Use the green-on-black palette as the site's dark-mode (likely default/only mode) design tokens.
- Reuse the "retro OS dialog" and "terminal window" chrome as literal reusable components (modal, card, loading state) rather than one-off decoration — see per-image "Site Application" notes for concrete mappings.
- Reserve full photographic/CRT-macro shots (images 2, 4) for hero/section-break moments; reserve dense collage/HUD compositions (images 1, 7) for content-heavy pages (about/resume, projects); reserve minimal single-focus screens (images 3, 6) for interstitial/error/loading states; reserve the vector wireframe scene (image 5) for ambient section backgrounds.
- Keep real body copy readable — don't let scanline/glitch texture reduce contrast below accessible levels; apply it as a background layer or subtle overlay, not on top of primary reading text.
