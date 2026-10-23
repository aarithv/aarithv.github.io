# Photography

This folder is the set of photos shown on the Photography page. Notes like
this README are not published.

- **Every image here (.jpg, .jpeg, .png, .webp, .avif, .gif) appears on the
  Photography page automatically.** Delete a file to take it down.
- Order and cameras are tracked in `content/pages/photography.md`:

  ```yaml
  camera: Sony ZV-1        # default for every photo
  photos:
    - file: pv_beach.jpeg  # listed photos come first, in this order
    - file: bris_rest_sunset.jpeg
      camera: iPhone 16    # override for one photo
  ```

  Photos you haven't listed appear after the listed ones, alphabetically.

**Tips:** keep file names lowercase with underscores (`place_subject_1.jpeg`)
so they sort predictably. Large originals slow the page down; exporting at
about 2400px on the long edge is plenty for the gallery and lightbox.
