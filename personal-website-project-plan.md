# Personal Website — Project Plan

A reference doc to guide the build in Claude Code + GitHub. Style direction: **warm & personal**, but still credible for an MD/PhD-track applicant (professors, PIs, admissions committees, collaborators will look at this).

---

## 1. Recommended Tech Stack

**Astro + Tailwind CSS**, deployed via **GitHub Pages** (or Vercel if you want zero-config previews per branch).

Why Astro over Next.js for this specific project:
- Your site is content-heavy (projects, research, photos, writing) and mostly static — Astro ships near-zero JS by default, so it's fast and simple to reason about.
- You can still drop in React/Vue "islands" later for anything interactive (e.g., a filterable project grid, a photo lightbox) without adopting a full SPA framework.
- Simpler mental model for Claude Code to work in one file/component at a time — good fit for iterative building in small sessions.
- Markdown-based content collections make it trivial to add a new project or paper as a `.md` file rather than editing code.

If down the road you want more interactivity (e.g. a dashboard, live data viz of your research), Next.js is the natural upgrade path — but start simple.

**Supporting tools:**
- Tailwind CSS for styling (fast to iterate, easy for Claude Code to generate consistent, tasteful layouts)
- `astro-icon` or `lucide` for icons
- Deployment: GitHub Pages (free, simple, fine for a static portfolio) or Vercel (free tier, nicer previews, auto HTTPS)
- Domain: consider a `.com` or `.dev` with your name if available

---

## 2. Site Map

```
/ (Home)
├── /about              — who you are, photo, quick bio, personality
├── /research            — research experience, publications, posters
├── /projects             — CS/EE/neuro projects, each with its own page
│   └── /projects/[slug]  — individual project deep-dive
├── /awards               — honors, scholarships, fellowships
├── /resume               — embedded PDF + link to download
├── /photography           — gallery
└── /contact (or footer)   — email, LinkedIn, GitHub, CV link
```

**Home page** should function as a hub, not a wall of text: short intro, headline research/project highlights, and clear navigation into the sections above. This is the page that gets 90% of the traffic (recruiters, PI's skimming), so it should sell the "who are you" story in ~10 seconds of scrolling.

---

## 3. Content Inventory (gather before/while building)

Start a simple checklist — Claude Code can scaffold pages before you have final content (use placeholders), but having this list ready speeds things up a lot:

- [ ] Short bio (2–3 sentences) + longer bio (1–2 paragraphs)
- [ ] Professional headshot + a few "personality" photos
- [ ] Resume/CV as PDF
- [ ] Research: lab name, PI, dates, 2–3 sentence description of your role/contribution, any posters/pubs (links or PDFs)
- [ ] Projects: for each — title, 1-line summary, tech/methods used, your role, links (GitHub repo, demo, writeup), images/screenshots
- [ ] Awards: name, granting body, year, 1-line context
- [ ] Photography: best 10–20 images, organized by theme or just chronologically
- [ ] Contact links: email, LinkedIn, GitHub, Google Scholar/ORCID if applicable

Tip: for projects and awards, structure this as data (a `.json` or `.md` file per project) rather than hardcoded HTML — makes future updates trivial for Claude Code to help with.

---

## 4. Repo Structure

```
your-name.github.io  (or personal-site)
├── src/
│   ├── layouts/
│   │   └── BaseLayout.astro
│   ├── components/
│   │   ├── Nav.astro
│   │   ├── Footer.astro
│   │   ├── ProjectCard.astro
│   │   └── PhotoGrid.astro
│   ├── content/
│   │   ├── projects/          ← one .md file per project
│   │   ├── research/          ← one .md file per experience
│   │   └── awards/            ← one .md file per award
│   ├── pages/
│   │   ├── index.astro
│   │   ├── about.astro
│   │   ├── research.astro
│   │   ├── projects/
│   │   │   ├── index.astro
│   │   │   └── [slug].astro
│   │   ├── awards.astro
│   │   ├── resume.astro
│   │   └── photography.astro
│   └── styles/
│       └── global.css
├── public/
│   ├── images/
│   └── resume.pdf
├── astro.config.mjs
├── tailwind.config.mjs
├── package.json
└── README.md
```

---

## 5. Design Direction Notes (warm & personal)

Since you picked **warm & personal**, some concrete direction to hand to Claude Code so it doesn't default to generic templated portfolio look:

- **Typography**: pair a warm serif (for headings — e.g. Fraunces, Lora, or Source Serif) with a clean sans-serif body font (Inter, Work Sans). Serif headings read as more human/personal than the all-sans-bold look most portfolio templates default to.
- **Color palette**: avoid pure black/white/blue-accent (the generic "tech portfolio" look). Consider warm neutrals (cream/off-white background) with one or two accent colors pulled from your photography or personality (e.g., a warm terracotta, muted sage, or deep plum).
- **Photography as texture, not just gallery**: let a few personal photos bleed into the About/Home page design itself (not just relegated to a "Photography" tab) — this is what makes a site feel personal rather than templated.
- **Voice**: write bios and project descriptions in first person, conversational but competent — avoid overly formal "Objective: To leverage synergies..." resume-speak on the web pages (save formality for the actual PDF resume).
- **Whitespace**: generous spacing, avoid cramming — signals confidence rather than trying to prove everything at once.

---

## 6. Suggested Build Order (milestones)

1. **Scaffold**: `npm create astro@latest`, add Tailwind, set up folder structure above, push empty repo to GitHub.
2. **Layout + Nav + Footer**: get the shared shell working across all pages first.
3. **Home page**: hero/intro section with placeholder content — get the visual identity (fonts, colors, spacing) locked in here before propagating to other pages.
4. **About page**: bio + photo.
5. **Projects**: build the card grid + one detail page template, then populate with your real projects.
6. **Research**: similar pattern to projects, simpler layout (list/timeline style works well).
7. **Awards**: simple list or timeline.
8. **Resume**: embed PDF viewer + download button.
9. **Photography**: gallery component (grid + lightbox).
10. **Polish pass**: responsive/mobile check, favicon, meta tags/OG image for link previews, accessibility check (alt text, contrast).
11. **Deploy**: connect GitHub Pages (Settings → Pages → deploy from Actions) or Vercel.

---

## 7. Claude Code + GitHub Workflow

1. Create the GitHub repo first (empty, with README), clone locally.
2. Open the repo folder in Claude Code — work in small, reviewable chunks (one page or component per session/commit) rather than asking for the whole site at once. This keeps diffs reviewable and lets you course-correct on design early.
3. Commit after each working milestone (scaffold, nav, home page, etc.) — meaningful commit messages will help you (and Claude Code, reading history later) track what changed and why.
4. Use a `content/` folder of markdown/JSON files (per section 4) so future updates ("add a new project", "swap out a photo") are quick asks rather than code surgery.
5. Set up GitHub Actions for auto-deploy on push to `main` (Astro's GitHub Pages integration guide covers this — Claude Code can set up the workflow file for you).
6. Optional: use a `dev` branch or PR previews (Vercel does this automatically) so you can review changes before they go live.

---

## Next Step

Bring this plan into Claude Code and start with milestone 1 (scaffold). If you want, I can also help you draft the actual bio copy, project descriptions, or the initial Astro scaffold commands here first.
