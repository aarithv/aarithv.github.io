# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Astro

## Users

The site's owner (aarith) showcasing their own work to visitors who land on it to see what they've made — a portfolio/showcase audience, not a specific conversion funnel (e.g. not framed as a job-hunting landing page).

## Product Purpose

A personal portfolio website. It exists to present the owner's projects and resume/CV in one place, in a distinct visual voice, so a visitor can see what they've built and who they are.

## Positioning

Undecided beyond the committed visual identity: a deliberately monochrome green-phosphor, retro-terminal/CRT aesthetic (see Evidence on Hand) is the intended differentiator versus a generic portfolio template, rather than any specific product mechanism or claim.

## Capabilities and Constraints

- Core content surfaces: a portfolio/showcase of projects, and a resume/CV.
- No specific page list, routing, or interactivity requirements confirmed yet beyond those two content types.
- No backend, auth, or dynamic data needs identified — static-first is sufficient for the current scope.

## Evidence on Hand

- `./inspo/` holds 7 curated reference images plus per-image `.md` notes (tags, description, recreation prompt, site-application idea) and a `STYLE.md` aggregate — an already-established visual mood board (green-phosphor terminal / CRT / retro-hacker Y2K aesthetic). This is visual-authority evidence for later design work, not itself a product fact.
- No resume/CV content or project write-ups exist in the repo yet. The owner will supply this content (text/details) conversationally as each page is built — future work must not invent placeholder projects, testimonials, employers, or credentials.

## Product Principles

- Real content only: build resume and project sections from what the owner actually supplies; never fabricate placeholder work history or projects to fill space.
- The portfolio content is the product; the retro-terminal visual identity is the differentiator, not a replacement for substance.
- Keep the build lean and static (Astro) — this is a small personal site, not an app; avoid backend/tooling complexity the scope doesn't need.
