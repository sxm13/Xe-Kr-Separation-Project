import json
import pandas as pd
from pymatgen.core import Structure


def molec(mol_csv,out_folder):
    gas = str(mol_csv).replace(".csv","").split("/")[-1]
    info=pd.read_csv(mol_csv)
    gas_def = {}
    
    gas_def["CriticalTemperature"]=float(info["CriticalTemperature"].dropna().values[0])
    gas_def["CriticalPressure"]=float(info["CriticalPressure"].dropna().values[0])
    gas_def["AcentricFactor"]=float(info["AcentricFactor"].dropna().values[0])
    gas_def["Type"]=str(info["Type"][0])
    
    gas_def["pseudoAtoms"]=[]
    for i in range(len(info["atom"].dropna().values)):
        gas_def["pseudoAtoms"].append([info["atom"][i],
                                       [float(info["posx"][i]),
                                        float(info["posy"][i]),
                                        float(info["posz"][i])]])

    # gas_def["Bonds"]=[]
    # for j in range(len(info["Bonds"].dropna().values)):
    #     gas_def["Bonds"].append([int(info["Bonds"][j]),int(info["Bonds0"][j])])

    with open(out_folder+ "/" + gas+".json","w") as mol_file:
        json.dump(gas_def,mol_file,indent=2)
    mol_file.close()


def FF(structure_path, FF_para_csv, out_folder):
    ff = {"PseudoAtoms": [], "SelfInteractions": []}

    structure = Structure.from_file(structure_path+".cif")
    unique_elements = {str(site.specie) for site in structure.sites}
    
    para = pd.read_csv(FF_para_csv)

    for i, name in enumerate(para["name"]):

        element = para["element"][i]
        is_framework = para["framework"][i] == "yes"
        
        if element in unique_elements or not is_framework:
            paras = {
                "name": name,
                "framework": is_framework,
                "print_to_output": para["print_to_output"][i] == "yes",
                "element": element,
                "print_as": para["print_as"][i],
                "mass": float(para["mass"][i]),
                "charge": float(para["charge"][i]),
            }
            ff["PseudoAtoms"].append(paras)

    for i, name in enumerate(para["name"]):
        element = para["element"][i]
        is_framework = para["framework"][i] == "yes"

        if element in unique_elements or not is_framework:
            paras = {
                "name": name,
                "type": para["type"][i],
                "parameters": [float(para["parameter1"][i]), float(para["parameter2"][i])],
                "source": para["source"][i],
            }
            ff["SelfInteractions"].append(paras)

    ff["MixingRule"] = "Lorentz-Berthelot"
    ff["TruncationMethod"] = "truncated"
    ff["TailCorrections"] = True

    output_file = f"{out_folder}/force_field.json"
    with open(output_file, "w") as FF_file:
        json.dump(ff, FF_file, indent=2)

