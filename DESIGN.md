---
name: Aarith Veerabhadran
description: An atlas of one brain. A phosphor-on-black personal site where every section is a labeled region.
colors:
  phosphor-300: "#7dffa3"
  phosphor-400: "#33ff66"
  phosphor-500: "#00ff41"
  phosphor-600: "#00cc34"
  phosphor-dim: "#4ade80"
  crt-black: "#0a0a0a"
  crt-void: "#000000"
typography:
  display:
    fontFamily: "VT323, JetBrains Mono, monospace"
    fontSize: "clamp(3rem, 9vw, 5.5rem)"
    fontWeight: 400
    lineHeight: 0.9
  headline:
    fontFamily: "VT323, JetBrains Mono, monospace"
    fontSize: "1.9rem"
    fontWeight: 400
    lineHeight: 1.02
  numeral:
    fontFamily: "VT323, JetBrains Mono, monospace"
    fontSize: "clamp(3.5rem, 8vw, 4.5rem)"
    fontWeight: 400
    lineHeight: 0.8
  headline-sm:
    fontFamily: "VT323, JetBrains Mono, monospace"
    fontSize: "1.5rem"
    fontWeight: 400
    lineHeight: 1.05
  title:
    fontFamily: "VT323, JetBrains Mono, monospace"
    fontSize: "1.25rem"
    fontWeight: 400
    lineHeight: 1
    letterSpacing: "0.025em"
  body:
    fontFamily: "JetBrains Mono, ui-monospace, Courier New, monospace"
    fontSize: "0.94rem"
    fontWeight: 400
    lineHeight: 1.75
  body-sm:
    fontFamily: "JetBrains Mono, ui-monospace, Courier New, monospace"
    fontSize: "0.875rem"
    fontWeight: 400
    lineHeight: 1.625
  label:
    fontFamily: "JetBrains Mono, ui-monospace, Courier New, monospace"
    fontSize: "0.75rem"
    fontWeight: 400
    letterSpacing: "0.08em"
    fontFeature: "\"tnum\""
rounded:
  none: "0px"
  node: "9999px"
spacing:
  gutter: "20px"
  gutter-sm: "32px"
  container: "72rem"
  row-y: "1.4rem"
  page-end: "7rem"
components:
  button:
    backgroundColor: "transparent"
    textColor: "{colors.phosphor-400}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0 1.1rem"
    height: "44px"
  button-solid:
    backgroundColor: "{colors.phosphor-500}"
    textColor: "{colors.crt-void}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0 1.1rem"
    height: "44px"
  button-solid-hover:
    backgroundColor: "{colors.phosphor-400}"
    textColor: "{colors.crt-void}"
  icon-button:
    backgroundColor: "transparent"
    textColor: "{colors.phosphor-400}"
    rounded: "{rounded.none}"
    size: "44px"
  nav-link:
    textColor: "{colors.phosphor-dim}"
    typography: "{typography.label}"
  nav-link-active:
    textColor: "{colors.phosphor-400}"
  link:
    textColor: "{colors.phosphor-400}"
  atlas-plate:
    backgroundColor: "{colors.crt-void}"
    rounded: "{rounded.none}"
    padding: "16px 24px 24px"
---

# Design System: Aarith Veerabhadran

## Overview

**Creative North Star: "The Atlas of One Brain"**

The site is drawn as an anatomical atlas plate on a dark phosphor screen. The home page opens on a real 3D brain (MNI152 template surface, Harvard-Oxford regions; built by `brain-pipeline/`), a translucent rim-lit hologram you can rotate, with each section's structure glowing where it actually sits: About is the medial prefrontal cortex, Research the thalamus, Projects the motor cortex, Awards the striatum, Resume the hippocampus, Photography the visual cortex. The face hologram and bio follow below it. The brain is the navigation; each interior page keeps its place on it through a mini brain in the header (its own structure lit, with that structure's real MNI coordinates) and a plate number on the ruler beneath the title. Interior headers sit in a band of rune rain, and their titles decode out of runes on load.

Everything is one colour of light on black. Hierarchy comes from luminance steps inside the phosphor band, from the change of face between VT323 (headings, labels, region names) and JetBrains Mono (everything read), and from hairlines: frames, rules, tick rulers and axon fibres at 1px. There are no cards, no fills, no rounded containers; content sits on ruled plates and lists that read like an instrument readout. Density is moderate and text-led; the only motion is signal: pathways lighting, pulses travelling, rings pinging on the current node.

The one sanctioned departure from monochrome is photography, which resolves from a phosphor duotone into full colour when attended, because a photography portfolio has to show frames as shot.

**Key Characteristics:**
- Phosphor-only palette on pure black; luminance is the only hierarchy axis in colour.
- VT323 for anything named, JetBrains Mono for anything read.
- Hairline geometry: 1px frames, corner registration ticks, tick rulers, leader lines.
- Square corners everywhere except nodes, which are always circles.
- A fixed six-region map (order and positions from `src/data/regions.ts`) recurs on home, in every page header, and as plate numbers PL. 01 to PL. 06.
- Photographs sit in phosphor duotone and resolve into colour when attended.

## Colors

A single phosphor-green ramp on void black; no secondary or tertiary hue exists.

### Primary
- **Signal Phosphor** (phosphor-500): the base emission. Default body text colour, solid button fill, node strokes, synapse dots, the tick rulers' majors, `::selection` fill.
- **Lit Phosphor** (phosphor-400): the attended or "named" state. Headings, region labels, links, button text, active nav item, lit pathways, the current node's fill, focus outlines, caret.
- **Hot Phosphor** (phosphor-300): peak emission only, reserved for the strongest signal pulse travelling a lit pathway. Never text.
- **Low Phosphor** (phosphor-600): structure, not content. Hairline borders and rules (mixed down to 28-60% alpha), box-drawing glyphs, scrollbar thumb.

### Neutral
- **Dim Phosphor** (phosphor-dim): secondary text. Structure names, metadata, captions, dates, plate numbers, inactive nav items, the page-header lede. Contrast against void black is roughly 11:1, so it carries small text legibly.
- **CRT Void** (crt-void): the page ground and the fill inside hollow nodes.
- **CRT Black** (crt-black): one step off void, used only as a recessed well (PDF viewer ground, scrollbar track).

### Named Rules
**The One Light Rule.** Every pixel the system draws is phosphor green or black. Hierarchy is expressed by stepping along the ramp (600 structure, dim secondary, 500 base, 400 named or attended, 300 peak signal), never by introducing a hue.

**The Attended Colour Rule.** The single exception is photographs (the photo grid, the About figures, the home index thumbnails). They render through a phosphor duotone (`grayscale(1) sepia(1) hue-rotate(62deg) saturate(2.6) brightness(0.8)`) and resolve to full colour when attended: on hover, on focus, or when scrolled into the middle band of the viewport (an IntersectionObserver with `-38%` top and bottom root margins). The lightbox always shows full colour. No other element may leave the ramp.

**The Hairline Alpha Rule.** Borders and rules are phosphor-600 mixed toward transparent, not new grey tokens: 28-30% for list separators and nav/footer rules, 35% for plate frames, 40% for photo frames, 55-60% for rulers and button outlines.

## Typography

**Display Font:** VT323 (with JetBrains Mono, monospace)
**Body Font:** JetBrains Mono (with ui-monospace, Courier New, monospace)

**Character:** VT323 is the CRT's own voice, a bitmap terminal face used large and for anything that is a name: page titles, region labels, entry titles, plate headings. JetBrains Mono carries every sentence and every datum, so reading stays comfortable at length while the whole page remains monospaced.

### Hierarchy
- **Display** (VT323 400, clamp(3rem, 9vw, 5.5rem), line-height 0.9): page titles, with the soft phosphor glow. The home name runs slightly larger (clamp(3.25rem, 7.4vw, 5.75rem), 0.88).
- **Numeral** (VT323 400, clamp(3.5rem, 8vw, 4.5rem), line-height 0.8): the year numerals on Awards.
- **Headline** (VT323 400, 1.9rem, line-height 1.02): entry titles inside a plate (research labs, region names in the home index).
- **Headline small** (VT323 400, 1.5rem, line-height 1.05): award names.
- **Title** (VT323 400, 1.25rem, line-height 1, slight tracking): plate headings, and the brain's callout labels.
- **Body** (JetBrains Mono 400, 0.94rem, line-height 1.75): long-form running text, capped at 62-64ch.
- **Body small** (JetBrains Mono 400, 0.875rem, relaxed leading): descriptions, readout values, page-header ledes, capped at max-prose.
- **Label** (JetBrains Mono 400, 0.75rem, 0.08-0.1em tracking, uppercase where it is navigation or a plate number; tabular numerals for counts, dates, plates): nav, buttons, metadata, captions.

### Named Rules
**The Named Things Rule.** If it is a name (a page, a region, a lab, an award, a plate), it is set in VT323 in Lit Phosphor. If it is read, it is JetBrains Mono. Never set running text in VT323.

**The Tabular Readout Rule.** Dates, counts, frame numbers and plate numbers use tabular numerals and Dim Phosphor, so columns of data align like an instrument display.

**The Verbatim Bio Rule.** The bio paragraph on Home and About is the owner's own text and is reproduced exactly; layout may change around it, the words may not.

## Layout

A single centred column (max 72rem) with 20px side gutters on phones and 32px from 640px up. Pages end with a generous 6-7rem bottom pad before the footer. The home first viewport is the brain stage alone, the full container width and up to 82svh tall (52svh on phones), with a one-line hint and the dataset credit beneath it. Callout labels sit in two columns either side of the brain, de-overlapped, with elbow leaders to each structure's facing hemisphere; the labels themselves are the region links. The face hologram and bio follow as a two-column split from 1024px, stacked on phones.

Interior pages share one header: display title, region structure and role, a short lede, the mini-brain plate at right (18-21rem from 768px; full width under the lede on phones), then a full-width tick ruler ending in the plate label. Content below uses ruled grids rather than containers: definition-list readouts with a 7.5rem key column, a fixed 10rem date column on the Research axon and the Awards year column, a four-column region index (12rem, 11rem, fluid, 7rem) from 900px. Rows are separated by hairlines and padded about 1.4rem vertically. The photo grid is a masonry of one, two (from 480px) and three (from 1024px) columns with 20px gaps.

**The Fixed Map Rule.** The six regions keep their positions and order everywhere: the home brain's callout labels, every header mini brain, the nav, and plate numbers PL. 01 to PL. 06 all derive from `regions.ts`. A new section is a new region in that file, never a free-floating page.

**The Scale Mark Rule.** Tick rulers carry minor ticks every 8px and majors every 64px, as unlabeled scale marks. Whether they should carry coordinate labels is an open decision for the owner; until it is made, do not add numbers to them.

## Elevation & Depth

The system is flat. There are no drop shadows. Depth comes from light and layering: a fixed neuron-network canvas and a rune-rain canvas sit behind content, the brain and face holograms are opaque-black WebGL canvases with bloom, blended in with `mix-blend-mode: screen` and a feathered radial mask, and the sticky nav, footer and plates sit on void black at 78-88% opacity so the network shows faintly through. Emission replaces elevation: display titles carry a soft phosphor glow, and a hovered brain region brightens rather than lifting. There are no box-shadows.

### Shadow Vocabulary
- **Phosphor glow** (`text-shadow: 0 0 18px color-mix(in srgb, #00ff41 35%, transparent)`): display titles only.

### Named Rules
**The Emission Not Elevation Rule.** Things never lift off the screen; they glow brighter. State is shown by stepping up the phosphor ramp or by a faint 7-12% phosphor wash, never by a shadow.

## Shapes

Square corners throughout: buttons, plates, photo frames, the lightbox and its controls all have 0 radius. Circles are reserved for nodes (region dots, axon nodes, the live status dot), drawn as hollow 1.2-1.3px phosphor-500 rings on void that fill with Lit Phosphor when current or hovered. Lines are 1px, square-capped where they end in arrows. The plate frame is a hairline rectangle with 14px registration ticks in Signal Phosphor at each corner. Pathways are quadratic curves from the face to each node; arrows are two-stroke SVG chevrons.

## Components

### Buttons
Outlined terminal keys, square and quiet until touched.
- **Shape:** square corners (0px), 44px minimum height.
- **Outline (default):** transparent with a phosphor-500 hairline at 60%, Lit Phosphor label, uppercase 0.75rem at 0.08em tracking, 1.1rem side padding, an optional trailing arrow icon.
- **Solid:** Signal Phosphor fill and border with void-black label, for the one primary action on a page (PDF download).
- **Hover / Focus:** outline brightens to phosphor-400 and gains a 12% phosphor wash; solid steps up to phosphor-400. 160ms ease-out on colour only. Focus is the global 2px phosphor-400 outline at 2px offset.
- **Icon button:** a 44px square in the same outline style (lightbox previous, close, next).

### Atlas Plate
The site's container, and the reason there are no cards.
- **Frame:** 1px phosphor-600 hairline at 35% with 14px corner ticks, over void black at 78%.
- **Head:** a box-drawing corner (`┌─`), the plate title in VT323, a horizontal rule that runs to the frame edge, and optional right-aligned tabular metadata in Dim Phosphor ("6 regions mapped", "3 figures").
- **Body:** 16-24px side padding; contents are ruled lists or grids, never nested boxes.

### Navigation
- **Style:** sticky 56px bar on void black at 88% with a bottom hairline. The wordmark "AARITH_" in VT323 Lit Phosphor at left with a ringed dot.
- **Items:** the six regions in map order, uppercase 0.8rem at 0.08em tracking, each with a small hollow node; inactive items in Dim Phosphor, hover to Lit Phosphor.
- **Active:** Lit Phosphor, filled node, 1px underline at 6px offset.
- **Mobile:** the list scrolls sideways under a right-edge fade mask, with the current item scrolled into the centre on load.

### Header Mini Brain (signature)
Every interior page header carries the real brain (`public/brain/brain-lite.glb`, same anatomy as the home page) in an atlas plate: the page's own structure glows and breathes, the other regions stay faint, and the brain turns slowly and can be dragged. The plate's top-left corner carries the plate number; its caption names the structure and gives its per-hemisphere MNI centroid from `src/data/brain-coords.json` (written by the pipeline), with true minus signs.

### Interior signals
Each section page adds one motif from its region's job, drawn from real content: Research's axon timeline carries action potentials that run down each segment in turn; Awards opens with a "reward signal" raster, one 2px spike per honor binned by year (quiet years shown as empty bins), each spike linking to its entry and naming it in the readout on hover or focus.

### Region Atlas (signature)
On home, hovering or focusing a region label lights its pathway from the face to the label and sends pulses along it (phosphor-400 signals, with phosphor-300 for the strong one). The same region list repeats below as the Region Index: rows with node, name, structure and role, a one-line summary, and plate number plus count, washing to 7% phosphor on hover with the arrow nudging 4px right.

### Axon Timeline
Research reads as one axon: a 1px vertical fibre with a hollow 11px node per entry, dates right-aligned in a 10rem column to its left from 768px. The current entry's node fills and pings; the fibre fades out after the last entry.

### Photo Frame and Lightbox
Photos sit in a 1px phosphor-600 frame at 40%, captioned below with a tabular frame counter and camera. They follow the Attended Colour Rule, with a 700ms resolve and a slight 1.025 scale on hover. The lightbox is a near-opaque void overlay with hairline-ruled top and bottom bars, the image in an atlas frame at full colour, and 44px icon buttons for previous, close and next.

### Links
Inline links are Lit Phosphor with a 1px underline at 40% alpha and 4px offset; the underline goes to full strength on hover. External links get a small trailing arrow icon.

## Do's and Don'ts

### Do:
- **Do** express every level of hierarchy as a step on the phosphor ramp: phosphor-600 for structure, phosphor-dim for secondary, phosphor-500 for base, phosphor-400 for named or attended, phosphor-300 for peak signal only.
- **Do** set names in VT323 and anything read in JetBrains Mono, with running text capped at 62-64ch.
- **Do** put new content on an atlas plate or a hairline-ruled list, with corner ticks on the plate and 28-35% phosphor-600 rules between rows.
- **Do** add a new section as a region in `regions.ts`, so it inherits its nav item, header mini brain and plate number.
- **Do** run every photograph through the phosphor duotone and resolve it to full colour on hover, focus, or mid-viewport scroll; show full colour in the lightbox.
- **Do** keep interactive targets at 44px or more and gate every authored animation behind `prefers-reduced-motion: no-preference`.
- **Do** show state by glowing brighter (ramp step or a 7-12% phosphor wash), with 160-200ms ease-out for colour and `cubic-bezier(0.16, 1, 0.3, 1)` for movement.

### Don't:
- **Don't** introduce any hue outside the phosphor ramp other than attended photographs.
- **Don't** use cards, filled panels, rounded containers or drop shadows; the plate frame and hairline are the only containers.
- **Don't** round corners on anything except nodes, which are always full circles.
- **Don't** add coordinate labels to tick rulers until the owner decides on them.
- **Don't** rewrite, trim or paraphrase the bio copy.
- **Don't** invent projects, credentials or placeholder entries to fill a plate; an empty region shows its unmapped state.
