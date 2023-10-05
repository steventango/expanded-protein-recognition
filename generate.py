from itertools import product
from pathlib import Path
from typing import Tuple

import numpy as np
from pymol import cmd
from tqdm import tqdm


def rotate_protein_view_spherical(pdb_id: str, rotation: Tuple[float, float, float], output_dir: Path):
    output_dir_pdb_id = output_dir / pdb_id
    output_dir_pdb_id.mkdir(parents=True, exist_ok=True)
    rx, ry, rz = rotation
    output_path = output_dir_pdb_id / f"{rz}.{ry}.{rz}.png"
    if output_path.exists():
        return

    cmd.set('direct', 1)
    cmd.show('surface')
    cmd.color('white')
    cmd.bg_color('black')

    selection = cmd.get_object_list()[0]
    atom_coords = cmd.get_coords(selection)
    distances = np.linalg.norm(atom_coords[:, np.newaxis, :] - atom_coords, axis=2)
    max_distance = distances.max()
    protein_size_nm = max_distance / 10.0
    zoom_buffer = 128 * 9 / protein_size_nm
    # measured that we want about 9px / nm
    # this is not quite right, we probably need to use trig
    cmd.zoom('all', zoom_buffer)

    cmd.turn('x', rx)
    cmd.turn('y', ry)
    cmd.turn('z', rz)

    cmd.png(str(output_path), width=128, height=128, dpi=128)


def main():
    data_dir = Path("data/")
    output_dir = data_dir / "images"
    pdb_dir = data_dir / "pdb"
    output_dir.mkdir(parents=True, exist_ok=True)
    pdb_dir.mkdir(parents=True, exist_ok=True)

    # NB 2 fluorophores on a nanobody, eGFP, Actin, Tubulin dimer, GABA_AR, Otoferlin, IgG, IgA, IgM
    pdb_ids = [None, "2Y0G", None, None, None, None, "1HZH", "1IGA", "2RCJ"]
    angles = list(range(0, 360, 60))

    for pdb_id in tqdm(pdb_ids):
        if pdb_id is None:
            continue
        cmd.fetch(pdb_id, f'https://files.rcsb.org/download/{pdb_id}.pdb', path=pdb_dir)
        for rx, ry, rz in tqdm(list(product(*([angles] * 3)))):
            rotate_protein_view_spherical(pdb_id, (rx, ry, rz), output_dir)
        cmd.delete('all')


main()
