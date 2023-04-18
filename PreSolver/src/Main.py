from SATfeatPy.sat_instance.sat_instance import SATInstance
from SATInstance.CNF import CNF
from VariableSelector import VariableSelector
from time import time
from os import listdir
# from DatasetPopulator import DatasetPopulator
from os.path import isfile
# from RandomForest import RandomForestClassifier
import sys

"""use_dpll = sys.argv[1].lower() in ["t", "true"]
single_path = sys.argv[2].lower() in ["t", "true"]
to_failure = sys.argv[3].lower() in ["t", "true"]
cutoff = float(sys.argv[4])

print(use_dpll, single_path, to_failure, cutoff)

if cutoff==0:
    cutoff = int(cutoff)

output_file = f"../instances/performance/cbs_{use_dpll}_{single_path}_{to_failure}_{int(cutoff*100)}.txt"""""

path = r"../instances/dataset_final/"
output_file = f"../instances/performance/dataset_final_True_False_True_50.txt"
to_failure=True
single_path=False
use_dpll=True
files = [file for file in listdir(path) if file[:3]=="sat"]
solved = 0
satisfiability_maintained = 0
clause_size_reduced, variable_size_reduced = [], []
for i,file in enumerate(files[945:1020:15]):
    print(f"Reading file {i} - {file}")
    file = open(path+file, "r")
    cnf_string = file.read()
    file.close()

    if cnf_string[:-2]!="\n":
        cnf_string += "\n"
    cnf = CNF(cnf_string)

    print("Constructing selector.")
    selector = VariableSelector(cnf_string, verbose=True, cutoff=0, use_dpll=use_dpll)

    num_clauses, num_literals = cnf.num_clauses, cnf.num_literals

    print(f"Running selector.\nOriginal cnf has {cnf.num_clauses} clauses and {cnf.num_literals} variables.\nInstance sat is {cnf.solve()}")
    exit_code, cnf = selector.run(to_failure=to_failure, single_path=single_path)

    print(f"Finished running with exit code {exit_code}.\nReduced cnf has {cnf.num_clauses} clauses and {cnf.num_literals} variables.\nInstance sat is now {cnf.solve()}")

    file = open(output_file, "a+")
    file.write(",".join([str(i) for i in
                         [num_literals, num_literals-cnf.num_literals, num_clauses - cnf.num_clauses, selector.assignments, selector.assignments_to_failure, cnf.solve(), cnf.solved]]) + "\n")
    file.close()

"""

n = 30
for i in range(75):
    wd = "../instances/CBS_k3_n100_m403_b10/"
    info = ""
    print(f"On file {i}")
    print("Starting CNF {}".format(i))
    fn = "CBS_k3_n100_m403_b10_{}.cnf".format(i)
    file = open(wd+fn, "r")
    cnf_string = file.read()
    file.close()

    cnf = CNF(cnf_string)
    populator = DatasetPopulator(cnf, fn[:-4])
    info += populator.populate(random=i%5!=0)

    if info!="":
        print("Writing to main")
        file = open("../instances/main_balanced.txt", "a+")
        file.write(info)
        file.close()



print("Function called")
file = open("../instances/main_balanced.txt", "r")
txt = [line.strip().split(",") for line in file.readlines()]
file.close()

i = 0
init = True
issues = 0
print("Entering for loop")
try:
    for filename, sat in txt[1:]:
        info = ""
        i+=1
        print(i, filename)
        if isfile(filename):
            feats = SATInstance(filename, preprocess=False)
            feats.gen_basic_features()
            feats.gen_dpll_probing_features()

            if init:
                init = False
                header = ",".join(feats.features_dict.keys())
                info = f"filename,{header},sat\n"
                file = open("../instances/rfc/dataset.txt", "w")
                file.write(info)
                file.close()
                info = ""
            info += filename + ","
            info += ",".join([str(feats.features_dict[key]) for key in feats.features_dict.keys()])
            info += "," + str(sat) + "\n"
            file = open("../instances/rfc/dataset.txt", "a")
            file.write(info)
            file.close()
except Exception as e:
    problem = open(txt[i][0], "r")
    length = len(problem.readlines())
    problem.close()
    print(f"{i} with value {txt[i]} and length {length}")
    raise e

print(f"Number skipped due to issues with dpll probing: {issues}")
"""
