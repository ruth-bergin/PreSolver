from SATfeatPy.sat_instance.sat_instance import SATInstance
from SATInstance.CNF import CNF
from VariableSelector import VariableSelector
from time import time
from os import listdir
from DatasetPopulator import DatasetPopulator
from os.path import isfile
# from RandomForest import RandomForestClassifier
import sys

def experiment(dataset, category, save_instances=False, heuristic="complete"):
    path = r"../instances/cbs/"
    output_file = f"../performance/{category}/{dataset}.txt"
    if category=="heuristic":
        output_file = f"../performance/{category}/{heuristic}.txt"
    files = listdir(path)[300:350]
    for i,file in enumerate(files):
        print(f"Reading file {i} - {file}")
        file = open(path+file, "r")
        cnf_string = file.read()
        file.close()

        #if cnf_string[:-2]!="\n":
        #    cnf_string += "\n"
        cnf = CNF(cnf_string)

        print("Constructing selector.")
        selector = VariableSelector(cnf_string, verbose=False, cutoff=0, use_dpll=True,
                                    selection_complexity=heuristic, dataset=dataset+".txt")

        num_clauses, num_literals = cnf.num_clauses, cnf.num_literals

        print(f"Running selector.\nOriginal cnf has {cnf.num_clauses} clauses and {cnf.num_literals} variables.\nInstance sat is {cnf.solve()}")
        exit_code, cnf = selector.run(to_failure=False, instance=i)

        print(f"Finished running with exit code {exit_code}.\nReduced cnf has {cnf.num_clauses} clauses and {cnf.num_literals} variables.\nInstance sat is now {cnf.solve()}")

        file = open(output_file, "a+")
        file.write(",".join([str(i) for i in
                             [num_literals, num_literals-cnf.num_literals, num_clauses - cnf.num_clauses, selector.assignments, selector.assignments_to_failure, cnf.solve(), cnf.solved]]) + "\n")
        file.close()

        if save_instances:
            fn = open(f"../instances/performance/{dataset}_instances/{i}.txt", "w+")
            fn.write(str(cnf))
            fn.close()

        for k in range(10):
            j = k/10
            if str(j) not in selector.cutoff_curve.keys():
                selector.cutoff_curve[str(j)] = [str(cnf.solve), str(selector.assignments), str(cnf.solved)]

        fn = open(f"../performance/cutoff/{dataset}/{i}.txt","w+")
        fn.write("\n".join([",".join([key]+selector.cutoff_curve[key]) for key in selector.cutoff_curve.keys()]))
        fn.close()

experiment("cbs_dpll_50", "cutoff",False)


"""


for i in range(150,200):
    wd = "../instances/cbs/"
    info = ""
    print(f"On file {i}")
    print("Starting CNF {}".format(i))
    fn = "CBS_k3_n100_m403_b10_{}.cnf".format(i)
    file = open(wd+fn, "r")
    cnf_string = file.read()
    file.close()

    cnf = CNF(cnf_string)
    populator = DatasetPopulator(cnf, fn[:-4])
    info += populator.populate(random=True)

    if info!="":
        print("Writing to main")
        file = open("../instances/population/cbs_supplementary1.txt", "a+")
        file.write(info)
        file.close()




print("Function called")
file = open("../instances/population/cbs_supplementary.txt", "r")
txt = [line.strip().split(",") for line in file.readlines()]
file.close()

i = 0
init = False
issues = 0
print("Entering for loop")
for filename, sat in txt:
    info = ""
    if sat=="False":
        i+=1
    else:
        continue
    print(i, filename)
    if isfile(filename):
        feats = SATInstance(filename, preprocess=False)
        feats.gen_basic_features()

        if init:
            init = False
            header = ",".join(feats.features_dict.keys())
            info = f"filename,{header},sat\n"
            file = open("../instances/rfc/cbs_base_complete.txt", "w")
            file.write(info)
            file.close()
            info = ""
        info += filename + ","
        info += ",".join([str(feats.features_dict[key]) for key in feats.features_dict.keys()])
        info += "," + str(sat) + "\n"
        file = open("../instances/rfc/cbs_base_complete.txt", "a")
        file.write(info)
        file.close()
"""
