from SATfeatPy.sat_instance.sat_instance import SATInstance
from CNF import CNF
from VariableSelector import VariableSelector
from DatasetPopulator import DatasetPopulator
from os.path import isfile

"""
n = 300
for i in range(n):
    wd = "../instances/CBS_k3_n100_m403_b10/"
    info = ""
    print(f"On file {i}")
    print("Starting CNF {}".format(i))
    fn = "CBS_k3_n100_m403_b10_{}.cnf".format(i)
    file = open(wd+fn, "r")
    cnf_string = file.read()
    file.close()

    cnf = CNF(cnf_string)
    populator = DatasetPopulator(fn[:-4], fn[:-4], cnf)
    info += populator.populate(random=False)

    if info!="":
        print("Writing to main")
        file = open("../instances/main.txt", "a+")
        file.write(info)
        file.close()


print("Function called")
file = open("../instances/main.txt", "r")
txt = [line.strip().split(",") for line in file.readlines()]
file.close()
init = True

if init:
    info = "filename,c,v,clauses_vars_ratio,vars_clauses_ratio,vcg_var_mean,vcg_var_coeff,vcg_var_min,vcg_var_max,vcg_var_entropy,vcg_clause_mean,vcg_clause_coeff,vcg_clause_min,vcg_clause_max,vcg_clause_entropy,vg_mean,vg_coeff,vg_min,vg_max,pnc_ratio_mean,pnc_ratio_coeff,pnc_ratio_min,pnc_ratio_max,pnc_ratio_entropy,pnv_ratio_mean,pnv_ratio_coeff,pnv_ratio_min,pnv_ratio_max,pnv_ratio_entropy,pnv_ratio_stdev,binary_ratio,ternary_ratio,ternary+,hc_fraction,hc_var_mean,hc_var_coeff,hc_var_min,hc_var_max,hc_var_entropy,sat\n"
    file = open("../instances/dataset.txt", "w")
    file.write(info)
    file.close()

i = 0
print("Entering for loop")
try:
    for filename, sat in txt[1:]:
        info = ""
        i+=1
        print(i, filename)
        if isfile(filename):
            feats = SATInstance(filename, preprocess=False)
            feats.gen_basic_features()
            info += filename + ","
            info += ",".join([str(feats.features_dict[key]) for key in feats.features_dict.keys()])
            info += "," + str(sat) + "\n"
            file = open("../instances/dataset.txt", "a")
            file.write(info)
            file.close()
except Exception as e:
    problem = open(txt[i][0], "r")
    length = len(problem.readlines())
    problem.close()
    print(f"{i} with value {txt[i]} and length {length}")
    raise e

"""

file = open("../instances/dataset.txt", "r")
print(len(file.readlines()))
file.close()

print("Reading file")
filename = "../instances/CBS_k3_n100_m403_b10/CBS_k3_n100_m403_b10_0.cnf"
file = open(filename, "r")
cnf_string = file.read()
file.close()


cnf = CNF(cnf_string)
cnf_string = str(cnf)
print("Constructing selector.")
selector = VariableSelector(cnf_string, verbose=True)

selector.rfc.test_accuracy()

print(f"Running selector.\nOriginal cnf has {cnf.num_clauses} clauses and {cnf.num_literals} variables.\nInstance sat is {cnf.solve()}")
exit_code, cnf = selector.run()

print(f"Finished running with exit code {exit_code}.\nReduced cnf has {cnf.num_clauses} clauses and {cnf.num_literals} variables.\nInstance sat is now {cnf.solve()}")
