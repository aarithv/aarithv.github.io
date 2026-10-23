# Brain pipeline

Builds `public/brain/brain.glb` (the navigable home-page brain),
`public/brain/brain-lite.glb` (the page-header minis) and
`src/data/brain-coords.json` (per-hemisphere MNI centroids), from
real anatomical data in MNI152 space:

- **Brain surface:** ICBM 2009 MNI152 grey + white matter probability templates
  (bundled with nilearn), iso-surfaced at 50%.
- **Regions:** Harvard-Oxford cortical and subcortical atlases (max-probability,
  25% threshold, 1 mm, fetched by nilearn from FSL), one mesh per site region:

| Region id | Page | Structure | Harvard-Oxford labels |
|---|---|---|---|
| about | About | Medial prefrontal cortex | Frontal Medial Cortex + Paracingulate Gyrus (y ≥ +10 mm) |
| research | Research | Thalamus | Left/Right Thalamus |
| projects | Projects | Primary motor cortex | Precentral Gyrus |
| awards | Awards | Striatum | Caudate, Putamen, Accumbens (both sides) |
| resume | Resume | Hippocampus | Left/Right Hippocampus |
| photography | Photography | Primary visual cortex | Intracalcarine + Supracalcarine Cortex, Occipital Pole |

Run:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python make_brain.py
```

Licensing: the MNI152 template is © 1993–2009 Louis Collins, McConnell Brain
Imaging Centre, McGill University (free to use with this notice). The
Harvard-Oxford atlases are released under the FSL licence, which is
non-commercial only. Both are credited on the home page.
