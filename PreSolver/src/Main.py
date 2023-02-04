from SATfeatPy.sat_instance.sat_instance import SATInstance
from VariableSelector import VariableSelector
from CNF import CNF
from DatasetPopulator import DatasetPopulator

print("Function called")
file = open("../instances/main.txt", "r")
txt = [line.strip().split(",") for line in file.readlines()]
file.close()
init = False

file = open("../instances/dataset.txt", "r")
print(len(file.readlines()))
file.close()

if init:
    info = "filename,c,v,clauses_vars_ratio,vars_clauses_ratio,vcg_var_mean,vcg_var_coeff,vcg_var_min,vcg_var_max,vcg_var_entropy,vcg_clause_mean,vcg_clause_coeff,vcg_clause_min,vcg_clause_max,vcg_clause_entropy,vg_mean,vg_coeff,vg_min,vg_max,pnc_ratio_mean,pnc_ratio_coeff,pnc_ratio_min,pnc_ratio_max,pnc_ratio_entropy,pnv_ratio_mean,pnv_ratio_coeff,pnv_ratio_min,pnv_ratio_max,pnv_ratio_entropy,pnv_ratio_stdev,binary_ratio,ternary_ratio,ternary+,hc_fraction,hc_var_mean,hc_var_coeff,hc_var_min,hc_var_max,hc_var_entropy,sat\n"
    file = open("../instances/dataset.txt", "w")
    file.write(info)
    file.close()

i = 0
print("Entering for loop")
try:
    for filename, sat in txt[7::9]:
        info = ""
        print(i, filename)
        feats = SATInstance(filename, preprocess=False)
        feats.gen_basic_features()
        info += filename + ","
        info += ",".join([str(feats.features_dict[key]) for key in feats.features_dict.keys()])
        info += "," + str(sat) + "\n"
        file = open("../instances/dataset.txt", "a")
        file.write(info)
        file.close()
        i+=1
except Exception as e:
    print(f"{i+1} with value {txt[i+1]}")
    raise e

file = open("../instances/dataset.txt", "r")
print(len(file.readlines()))
file.close()

print("Reading file")
filename = "../instances/inductive-inference/ii8a1.cnf"
file = open(filename, "r")
cnf_string = file.read()
file.close()


cnf = CNF(cnf_string, sep="\n 0 \n")
cnf_string = str(cnf)
print("Constructing selector.")
selector = VariableSelector(cnf_string, verbose=True)

print(f"Running selector.\nOriginal cnf has {cnf.num_clauses} clauses and {cnf.num_literals} variables.\nInstance sat is {cnf.solve()}")
exit_code, cnf = selector.run()

print(f"Finished running with exit code {exit_code}.\nReduced cnf has {cnf.num_clauses} clauses and {cnf.num_literals} variables.\nInstance sat is now {cnf.solve()}")