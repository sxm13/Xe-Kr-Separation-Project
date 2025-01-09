import os, shutil
from raspa3_tools import template, utils, FF

cif_folder = "./cifs/"
cutoff = 12
FF_folder = "./FF_files"

with open("./s_list") as f:
    S = [line.strip() for line in f.readlines()]
with open("./t_list") as f:
    T = [line.strip() for line in f.readlines()]
# with open("./p_list") as f:
#     P = [line.strip() for line in f.readlines()]
# for g in G:
#     g = g.replace("\n","")

P = ["100000"]

G = ["Xe","Kr"]
MolFrac = [0.2,0.8]
for s in S[:]:
    s = s.replace("\n","")
    UC = utils.unit_cell(os.path.join(cif_folder, s), cutoff)
    utils.CIF_process(os.path.join(cif_folder, s), cif_folder)
    # for t in T:
    #     t = t.replace("\n","")
    # for p in P:
    #     p = p.replace("\n","")
    t=298
    p=100000
    folder_parts = ["calc", s]
    folder_parts = [str(part) for part in folder_parts if part is not None]
    input_folder = os.path.join(*folder_parts)
    os.makedirs(input_folder, exist_ok=True)

    input = template.Generate(  task = "MixtureAdsorption",
                                CIFName = s,
                                MolName = G,
                                MolFrac = MolFrac,
                                CutOff = 12,
                                NumberOfUnitCells = UC,
                                ExternalTemperature = float(t),
                                ExternalPressure = float(p))
    for g in G:
        FF.molec(os.path.join(FF_folder, g+".csv"), input_folder)
    FF.FF(os.path.join(cif_folder, s), os.path.join(FF_folder, "FF_para.csv"), input_folder)

    input.save_to_json(os.path.join(input_folder, "simulation.json"))
    shutil.copy(os.path.join(cif_folder, s+".cif"), input_folder)
    shutil.copy("raspa3.slurm", input_folder)
    with open(os.path.join(input_folder, "raspa3.slurm"), "r") as file:
        job_script = file.read()
    job_script_name = job_script.replace("test", s)
    with open(os.path.join(input_folder, "raspa3.slurm"), "w") as file:
        file.write(job_script_name)