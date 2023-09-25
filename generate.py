from pymol import cmd
import math


# Define the function to rotate the protein view using spherical coordinates
def rotate_protein_view_spherical(pdb_id, spherical_rotation, output_filename):
    # Create a visualization
    cmd.show('surface')
    cmd.color('white')

    # Zoom to fit the protein in the view
    cmd.zoom('all', 0.6)

    # Convert spherical coordinates to Cartesian coordinates
    azimuth, elevation = math.radians(spherical_rotation[0]), math.radians(spherical_rotation[1])
    x = math.sin(azimuth) * math.cos(elevation)
    y = math.sin(azimuth) * math.sin(elevation)
    z = math.cos(azimuth)

    # Rotate the view using the Cartesian coordinates
    cmd.rotate([x, y, z], 0)

    # Save the rendered image
    cmd.png(output_filename, width=128, height=128, dpi=100)


def main():
  # Start PyMOL and load your protein structure
  cmd.fetch('1A2K', 'https://files.rcsb.org/download/1A2K.pdb')
  # Example usage:
  spherical_rotation = (60, 120)  # Replace with your desired spherical rotation angles (azimuth, elevation) in degrees
  output_file = 'output_image2.png'  # Replace with your desired output file name

  # Call the function to rotate and render the protein view
  rotate_protein_view_spherical('1A2K', spherical_rotation, output_file)


main()
