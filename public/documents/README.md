# Documents (current resume)

This folder holds the current copy of your resume and any other PDFs for the
Resume page. Notes like this README are not published.

- **Every PDF directly in this folder appears on the Resume page automatically.**
- To name a PDF or set the order, list it in `content/pages/resume.md`:

  ```yaml
  documents:
    - file: av_resume_102326.pdf
      label: Resume
  ```

  Unlisted PDFs appear after the listed ones, named after the file
  (`conference_poster.pdf` → "Conference poster").

**Updating your resume:** either overwrite the PDF with the new one under the
same name (nothing else to change), or add the new file, point the `file:` line
in `content/pages/resume.md` at it, and delete the old one.

`research/` holds PDFs linked from research entries (abstracts, posters). They
are not listed on the Resume page; link one as `/documents/research/<file>.pdf`.
