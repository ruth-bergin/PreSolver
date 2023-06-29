import os
import shutil

from SATfeatPy.sat_instance.sat_instance import SATInstance
from SATInstance.CNF import CNF
from VariableSelector import VariableSelector
from time import time
from os import listdir
from DatasetPopulator import DatasetPopulator
from os.path import isfile
# from RandomForest import RandomForestClassifier
import sys
from random import sample
from pysat.solvers import Solver

def experiment(dataset, category, save_instances=False, heuristic="complete"):
    path = r"../instances/cbs/"
    output_file = f"../performance/{category}/{dataset}.txt"
    if category=="heuristic":
        output_file = f"../performance/{category}/{heuristic}.txt"
    files = listdir(path)
    failures_to_read = 0
    for j,file in enumerate(files[23+19:50]):
        i = j + 23+19
        print(f"Reading file {i} - {file}")
        file = open(path+file, "r")
        cnf_string = file.read()
        file.close()

        if cnf_string[:-2]!="\n":
            cnf_string += "\n"
        try:
            cnf = CNF(cnf_string)
        except:
            failures_to_read += 1
            print("***FAILURES TO READ***",failures_to_read)
            continue

        print("Constructing selector.")
        selector = VariableSelector(cnf_string, verbose=False, cutoff=0, use_dpll=False,
                                    selection_complexity=heuristic, dataset=dataset+".txt")

        num_clauses, num_literals = cnf.num_clauses, cnf.num_literals

        print(f"Running selector.\nOriginal cnf has {cnf.num_clauses} clauses and {cnf.num_literals} variables.\nInstance sat is {cnf.solve()}")
        exit_code, cnf = selector.run(to_failure=True, instance=i, single_path=True)

        print(f"Finished running with exit code {exit_code}.\nReduced cnf has {cnf.num_clauses} clauses and {cnf.num_literals} variables.\nInstance sat is now {cnf.solve()}")

        file = open(output_file, "a+")
        file.write(",".join([str(i) for i in
                             [num_literals, num_literals-cnf.num_literals, num_clauses - cnf.num_clauses, selector.assignments, selector.assignments_to_failure, cnf.solve(), cnf.solved]]) + "\n")
        file.close()

        if save_instances:
            fn = open(f"../instances/performance/{dataset}_instances/{i}.txt", "w+")
            fn.write(str(cnf))
            fn.close()

experiment("cbs_base_50","verification", heuristic="complete")

"""file = open("../instances/population/cbs_supplementary.txt","r")
instances = [line.strip("\n").split(",") for line in file.readlines()]
file.close()

refined = ""
i = 0
for filename, sat in instances:
    if sat=="False":
        refined += f"{filename},{sat}\n"
        i += 1
    if i==300:
        break

file = open("../instances/population/dataset_final_refined.txt","a+")
file.write(refined)
file.close()


path = "../instances/dataset_final/"
indices = indices[101:]
files = [os.listdir(path)[index] for index in indices]

for index,fn in enumerate(files[15+18+13:]):
    print(index)
    info=""
    file = open(path+fn, "r")
    cnf_string = file.read() + "\n"
    file.close()

    cnf = CNF(cnf_string)
    populator = DatasetPopulator(cnf, fn[:-4])
    info += populator.populate(random=True)

    if info!="":
        print("Writing to main")
        file = open("../instances/population/dataset_final_supplementary.txt", "a+")
        file.write(info)
        file.close()



print("Function called")
file = open("../instances/population/dataset_final_refined.txt", "r")
txt = [line.strip().split(",") for line in file.readlines()]
file.close()

i = 0
init = False
issues = 0
print("Entering for loop")
for filename, sat in txt[2030:]:
    info = ""
    print(i, filename)
    i+=1
    if isfile(filename):
        feats = SATInstance(filename, preprocess=False)
        feats.gen_basic_features()
        feats.gen_dpll_probing_features()

        if init:
            init = False
            header = ",".join(feats.features_dict.keys())
            info = f"filename,{header},sat\n"
            file = open("../instances/rfc/dataset_final.txt", "w")
            file.write(info)
            file.close()
            info = ""
        info += filename + ","
        info += ",".join([str(feats.features_dict[key]) for key in feats.features_dict.keys()])
        info += "," + str(sat) + "\n"
        file = open("../instances/rfc/dataset_final.txt", "a")
        file.write(info)
        file.close()
"""

