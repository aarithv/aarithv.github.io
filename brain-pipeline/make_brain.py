"""Build the site's navigable 3D brain from real anatomical data.

Everything here lives in MNI152 space, the standard coordinate system used in
neuroimaging, so each region sits where it actually is in a human brain:

- Brain surface: the ICBM 2009 MNI152 grey + white matter probability
  templates (shipped with nilearn), iso-surfaced at 50%.
- Regions: the Harvard-Oxford cortical and subcortical atlases (maximum
  probability, 25% threshold, 1 mm), iso-surfaced per structure.

Output: public/brain/brain.glb (home page) and brain-lite.glb (page headers),
each with one node per region (named by the site's region id) plus a "cortex"
node for the outer surface; and src/data/brain-coords.json, the MNI centroid
of each structure per hemisphere.

Usage:
    python -m venv .venv && .venv/bin/pip install -r requirements.txt
    .venv/bin/python make_brain.py
"""

import json
from pathlib import Path

import fast_simplification
import nibabel as nib
import numpy as np
import trimesh
from nilearn import datasets
from scipy import ndimage
from skimage import measure

OUT = Path(__file__).resolve().parent.parent / "public" / "brain" / "brain.glb"
OUT_LITE = OUT.with_name("brain-lite.glb")
# Imported by the site at build time (src/data), not served.
COORDS = Path(__file__).resolve().parent.parent / "src" / "data" / "brain-coords.json"

# Site region id -> Harvard-Oxford labels that make up that structure.
# Cortical labels index into the cortical atlas, subcortical into the
# subcortical one; both hemispheres are included.
REGIONS = {
    # Medial prefrontal cortex: ventromedial (Frontal Medial Cortex) plus
    # dorsomedial (Paracingulate Gyrus), kept anterior of y = +10 mm so the
    # paracingulate's posterior tail doesn't count as prefrontal.
    "about": {"cort": ["Frontal Medial Cortex", "Paracingulate Gyrus"], "min_y": 10},
    "research": {"sub": ["Left Thalamus", "Right Thalamus"]},
    # Primary motor cortex is the precentral gyrus (Brodmann area 4).
    "projects": {"cort": ["Precentral Gyrus"]},
    # Striatum: caudate + putamen (dorsal) and nucleus accumbens (ventral).
    "awards": {
        "sub": [
            "Left Caudate", "Right Caudate",
            "Left Putamen", "Right Putamen",
            "Left Accumbens", "Right Accumbens",
        ]
    },
    "resume": {"sub": ["Left Hippocampus", "Right Hippocampus"]},
    # Primary visual cortex (V1, Brodmann 17) lines the calcarine sulcus and
    # extends onto the occipital pole.
    "photography": {"cort": ["Intracalcarine Cortex", "Supracalcarine Cortex", "Occipital Pole"]},
}

CORTEX_FACES = 90_000
REGION_FACES = 6_000


def load(img):
    return img if hasattr(img, "shape") else nib.load(img)


def to_scene(vertices_mm):
    """MNI mm (x right, y anterior, z superior) -> three.js (y up), in decimetres.

    (x, y, z) -> (x, z, -y) is a proper rotation, so left/right is preserved.
    """
    v = np.asarray(vertices_mm, dtype=np.float64)
    return np.column_stack([v[:, 0], v[:, 2], -v[:, 1]]) / 100.0


def surface(volume, affine, level, sigma, target_faces):
    smooth = ndimage.gaussian_filter(volume.astype(np.float32), sigma)
    verts, faces, _, _ = measure.marching_cubes(smooth, level=level)
    verts_mm = nib.affines.apply_affine(affine, verts)
    if len(faces) > target_faces:
        verts_mm, faces = fast_simplification.simplify(
            verts_mm.astype(np.float32), faces.astype(np.int32), 1 - target_faces / len(faces)
        )
    mesh = trimesh.Trimesh(to_scene(verts_mm), faces, process=True)
    trimesh.smoothing.filter_taubin(mesh, iterations=8)
    mesh.fix_normals()
    return mesh


def main():
    gm = load(datasets.load_mni152_gm_template(resolution=1))
    wm = load(datasets.load_mni152_wm_template(resolution=1))
    tissue = np.asarray(gm.get_fdata()) + np.asarray(wm.get_fdata())

    cort = datasets.fetch_atlas_harvard_oxford("cort-maxprob-thr25-1mm")
    sub = datasets.fetch_atlas_harvard_oxford("sub-maxprob-thr25-1mm")
    atlases = {
        "cort": (np.asarray(load(cort.maps).get_fdata()).round().astype(int), load(cort.maps).affine, list(cort.labels)),
        "sub": (np.asarray(load(sub.maps).get_fdata()).round().astype(int), load(sub.maps).affine, list(sub.labels)),
    }

    masks = {}
    for region, spec in REGIONS.items():
        affine = None
        mask = None
        for kind in ("cort", "sub"):
            for name in spec.get(kind, []):
                data, aff, labels = atlases[kind]
                index = labels.index(name)
                part = data == index
                mask = part if mask is None else mask | part
                affine = aff
        if "min_y" in spec:
            # Voxel -> world y for every voxel row, then keep only anterior.
            ys = nib.affines.apply_affine(affine, np.column_stack([
                np.zeros(mask.shape[1]), np.arange(mask.shape[1]), np.zeros(mask.shape[1])
            ]))[:, 1]
            mask = mask & (ys >= spec["min_y"])[None, :, None]
        masks[region] = (mask, affine)

    # Per-hemisphere centroid of each structure in MNI mm, shown as the
    # coordinate readout on each page header.
    coords = {}
    for region, (mask, affine) in masks.items():
        world = nib.affines.apply_affine(affine, np.argwhere(mask))
        coords[region] = {
            side: [round(float(v)) for v in world[sel].mean(axis=0)]
            for side, sel in (("left", world[:, 0] < 0), ("right", world[:, 0] >= 0))
            if sel.any()
        }
    COORDS.write_text(json.dumps(coords, indent=2) + "\n")
    print(f"wrote {COORDS}")

    # Full model for the home page, and a light one for the page-header minis.
    for out, cortex_faces, region_faces in ((OUT, CORTEX_FACES, REGION_FACES), (OUT_LITE, 24_000, 1_800)):
        scene = trimesh.Scene()
        cortex = surface(tissue, gm.affine, level=0.5, sigma=0.6, target_faces=cortex_faces)
        scene.add_geometry(cortex, node_name="cortex", geom_name="cortex")
        for region, (mask, affine) in masks.items():
            mesh = surface(mask.astype(np.float32), affine, level=0.5, sigma=0.8, target_faces=region_faces)
            scene.add_geometry(mesh, node_name=region, geom_name=region)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(scene.export(file_type="glb"))
        print(f"wrote {out} ({out.stat().st_size / 1e6:.2f} MB)")


if __name__ == "__main__":
    main()
