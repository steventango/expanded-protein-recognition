from pymol import cmd
from typing import Tuple
from pathlib import Path
from itertools import product

def rotate_protein_view_spherical(pdb_id: str, rotation: Tuple[float, float, float], output_dir: Path):
    cmd.show('surface')
    cmd.color('white')

    rx, ry, rz = rotation
    cmd.turn('x', rx)
    cmd.turn('y', ry)
    cmd.turn('z', rz)

    output_dir_pdb_id = output_dir / pdb_id
    output_dir_pdb_id.mkdir(parents=True, exist_ok=True)
    output_path = output_dir_pdb_id / f"{rz}.{ry}.{rz}.png"
    cmd.png(str(output_path), width=128, height=128, dpi=100)


def main():
    cmd.fetch('1A2K', 'https://files.rcsb.org/download/1A2K.pdb')

    output_dir = Path("data/images/")

    angles = list(range(0, 360, 10))
    for rx, ry, rz in product(*([angles] * 3)):
        rotate_protein_view_spherical("1A2K", (rx, ry, rz), output_dir)


main()
