import os

def search(folder, unit="mol/kg-framework"):

    path = os.path.join(folder, "output")
    all_files = os.listdir(path)
    out_file = all_files[0]
    
    with open(path + "/" + out_file, "r") as file:
        lines = file.readlines()

    results = {}
    current_gas = None

    for _, line in enumerate(lines):
        if line.startswith("Loadings"):
            continue
        if line.startswith("Component"):
            parts = line.split()
            if len(parts) > 2:
                current_gas = parts[2].strip("()")
        if current_gas and line.strip().startswith("Abs. loading average"):
            if unit in line:
                parts = line.split()
                try:
                    N_gas = float(parts[3])
                    E_gas = float(parts[5])
                    results[current_gas] = [N_gas, E_gas]
                except (IndexError, ValueError):
                    continue
    return results
