---
# Site-wide text. Lines starting with # are notes and are ignored.
# Wrap a value in quotes if it contains a colon (:) or starts with a symbol.

name: Aarith Veerabhadran # used in page titles and the footer
brand: AARITH_ # the logo text at the top left
description: Personal site — research, projects, and photography. # fallback search/share description

# Link preview: the picture shown when someone texts or posts a link to the site.
# Put the image in public/images/ and give its path here. Best size: 1200 × 630 (PNG or JPG).
# Any page can use its own by adding a shareImage: line to its file in content/pages/.
shareImage: /images/share.png
tagline: An atlas of one brain. # big line in the footer
location: Ann Arbor, Michigan # shown in the footer after the copyright

# Footer buttons. Add, remove or reorder freely.
links:
  - label: Email
    href: mailto:aarith@umich.edu
  - label: GitHub
    href: https://github.com/aarithv
  - label: LinkedIn
    href: https://www.linkedin.com/in/aarith-veerabhadran-218687322

# The six sections of the site. Each one is also a region of the brain.
# label: name in the nav and on the brain
# structure / role: the brain region and what it does (shown in page headers)
# summary: one line about the section, shown in the region index on the home page
# (Which brain region each page lives in, and where it sits on the 3D model,
# is set in src/data/regions.ts and brain-pipeline/, not here.)
sections:
  about:
    label: About
    structure: Medial prefrontal cortex
    role: sense of self
    summary: Neuroscience & Cognitive Science at the University of Michigan. Tennis, violin, photography.
  research:
    label: Research
    structure: Thalamus
    role: relay for consciousness
    summary: "Huang Lab, Center for Consciousness Science: changes in functional brain connectivity in anesthetized patients."
  projects:
    label: Projects
    structure: Motor cortex
    role: making things
    summary: Write-ups in progress.
  awards:
    label: Awards
    structure: Striatum
    role: reward signalling
    summary: William J. Branstrom Prize, 2026. National Merit Finalist, 2025.
  resume:
    label: Resume
    structure: Hippocampus
    role: long-term memory
    summary: Resume, plus awards & publications. Read in the browser or download the PDFs.
  photography:
    label: Photography
    structure: Visual cortex
    role: what the eyes keep
    summary: Shot mostly on a Sony ZV-1 — a look at what I see when I'm not in the lab.
---
