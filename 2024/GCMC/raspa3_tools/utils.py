import numpy as np
from CifFile import ReadCif


def unit_cell(cif_file,cutoff):
    with open(cif_file+".cif", 'r') as cif:
        mof_cif= cif.read()
    for line in mof_cif.split("\n"):
        if "_cell_length_a" in line:
            length_a = line.split()[1]
            length_a =float(length_a)
        if "_cell_length_b" in line:
            length_b = line.split()[1]
            length_b = float(length_b)
        if "_cell_length_c" in line:
            length_c= line.split()[1]
            length_c= float(length_c)
        if "_cell_angle_alpha" in line:
            alpha = line.split()[1]
            alpha = float(alpha)
        if "_cell_angle_beta" in line:
            beta= line.split()[1]
            beta= float(beta)
        if "_cell_angle_gamma" in line:
            gamma = line.split()[1]
            gamma = float(gamma)
    
    ax = length_a
    ay = 0.0
    az = 0.0
    bx = length_b * np.cos(gamma * np.pi / 180.0)
    by = length_b * np.sin(gamma * np.pi / 180.0)
    bz = 0.0
    cx = length_c * np.cos(beta * np.pi / 180.0)
    cy = (length_c * length_b * np.cos(alpha * np.pi /180.0) - bx * cx) / by
    cz = (length_c ** 2 - cx ** 2 - cy ** 2) ** 0.5
    
    unit_cell =  np.asarray([[ax, ay, az],[bx, by, bz], [cx, cy, cz]])
    A = unit_cell[0]
    B = unit_cell[1]
    C = unit_cell[2]

    Wa = np.divide(np.linalg.norm(np.dot(np.cross(B,C),A)), np.linalg.norm(np.cross(B,C)))
    Wb = np.divide(np.linalg.norm(np.dot(np.cross(C,A),B)), np.linalg.norm(np.cross(C,A)))
    Wc = np.divide(np.linalg.norm(np.dot(np.cross(A,B),C)), np.linalg.norm(np.cross(A,B)))
    
    uc_x = int(np.ceil(cutoff/(0.5*Wa)))
    uc_y = int(np.ceil(cutoff/(0.5*Wb)))
    uc_z = int(np.ceil(cutoff/(0.5*Wc)))
    
    return [uc_x,uc_y,uc_z]

def CIF_process(structure, output_folder):

    cif_data = ReadCif(structure+".cif")
    struc_name=structure.split("/")[-1]

    block = cif_data.first_block()

    atom_site_label = block["_atom_site_label"]
    atom_site_type_symbol = block["_atom_site_type_symbol"]

    if len(atom_site_label) != len(atom_site_type_symbol):
        raise ValueError("The lengths of _atom_site_label and _atom_site_type_symbol do not match.")

    block["_atom_site_label"] = atom_site_type_symbol

    cif_content = cif_data.WriteOut()

    lines = cif_content.splitlines()

    process_lines = [line for line in lines if not line.startswith("#") and line.strip()]

    process_lines.insert(0, "# process by raspa3_tools")

    process_lines.append("")
    process_lines.append("")

    with open(output_folder+"/"+struc_name + ".cif", "w") as f:
        f.write("\n".join(process_lines))
        f.write("\n")
