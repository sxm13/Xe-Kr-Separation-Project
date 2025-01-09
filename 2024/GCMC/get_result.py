from raspa3_tools import result
import os,json

all_result = {}

with open("./top_list") as f:
    S = [line.strip() for line in f.readlines()]
with open("./p_list") as f:
    P = [line.strip() for line in f.readlines()]

gas = ["Xe", "Kr"]
all_result["pressure"] = P

for s in S[:]:
    all_result[s] = {}
    s = s.replace("\n","")
    for g in gas:
        all_result[s][g] = []
        for p in P:
            path = os.path.join("./calc", s, g, p)
            if os.path.exists(path):
                try:
                    data = result.search(os.path.join("./calc", s, g, p))
                    all_result[s][g].append(data[g])
                except:
                    print(s)
            else:
                print(f"Folder '{path}' does not exist.")

        with open("XeKr_single_isotherms.json","w") as result_file:
            json.dump(all_result,result_file,indent=4)