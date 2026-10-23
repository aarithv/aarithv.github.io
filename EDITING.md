# Editing the site

Everything you'd normally change lives in two places: **`content/`** for text
and **`public/`** for files. You never need to touch `src/` for everyday edits.

Preview while you edit with `npm run dev` and open http://localhost:4321.
Save a file and the page updates. If something doesn't show up, stop the
server (`npx astro dev stop`) and start it again with `npx astro dev --force`,
which also clears the content cache.

## Text: `content/`

Each file has a short header between two `---` lines (labelled fields), and
some have normal text below it. Lines starting with `#` are notes to you; the
site ignores them.

| File | What it controls |
|---|---|
| `content/site.md` | Your name, the logo text, footer line and location, footer links, and each section's name, brain region and one-line summary |
| `content/bio.md` | Your bio (home page and About) |
| `content/pages/home.md` | Home page: tab title, the ROLE and STATUS lines |
| `content/pages/about.md` | About: portrait, the facts list, the photo row |
| `content/pages/research.md` | Research intro |
| `content/pages/projects.md` | Projects intro, the tools list, the "in progress" panel |
| `content/pages/gradients.md` | Gradient viewer intro |
| `content/pages/awards.md` | Awards intro |
| `content/pages/resume.md` | Resume intro and names for your PDFs |
| `content/pages/photography.md` | Photography intro, default camera, photo order |
| `content/research/*.md` | One file per research entry |
| `content/awards/*.md` | One file per award |

In every page file, `title` is the page heading and tab title, and
`description` is what search engines and link previews show. The text under
the header block is the intro under the heading. Leave a blank line between
paragraphs, and use `[link text](https://example.com)` for a link or
`**bold**` for bold.

**Add a research entry or award:** copy an existing file in
`content/research/` or `content/awards/`, give the copy a new file name, and
edit it. Delete a file to remove the entry. Entries sort themselves by date
(research) or year (awards).

**Header tips:** keep the spacing at the start of lines as it is (it shows
what belongs to what). If a value contains a colon followed by a space, put
the whole value in quotes, like `summary: "Huang Lab: complexity measures"`.
If you make a mistake, the dev server shows an error naming the file and line.

## Files: `public/`

| Folder | What goes there | What happens |
|---|---|---|
| `public/images/photography/` | Your photos (.jpg, .png, .webp…) | **Every image appears on the Photography page automatically.** Optionally list files in `content/pages/photography.md` to set their order or a different camera; unlisted ones follow alphabetically. |
| `public/documents/` | PDFs for the Resume page | **Every PDF here appears automatically.** Give it a nicer name in `content/pages/resume.md`; otherwise it's named after the file (`conference_poster.pdf` → "Conference poster"). |
| `public/documents/research/` | PDFs you link from research entries (abstracts, posters) | Not listed on the Resume page. Link one from an entry as `/documents/research/your-file.pdf`. |
| `public/images/about/` | Portrait and About photos | Referenced by file name in `content/pages/about.md`. |

**Replacing your resume:** drop the new PDF into `public/documents/`, update
the `file:` line in `content/pages/resume.md` to its name, and delete the old
PDF. (Or keep the same file name and just overwrite it.)

`public/documents/` and `public/images/photography/` each have a README with
these instructions; those notes are left out of the published site.

Deleting a photo or PDF never breaks the site; any mention of it in a content
file is simply skipped.

## Not in `content/`

- Which brain region each section maps to, and where it sits on the 3D brain:
  `src/data/regions.ts` and `brain-pipeline/` (see its README).
- Small interface labels inside tools (e.g. the gradient viewer's buttons) are
  in their page files under `src/pages/`.
