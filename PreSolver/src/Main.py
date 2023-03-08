from SATfeatPy.sat_instance.sat_instance import SATInstance
from src.SATInstance.CNF import CNF
from VariableSelector import VariableSelector
from time import time
from os import listdir
from DatasetPopulator import DatasetPopulator
from os.path import isfile
from RandomForest import RandomForestClassifier

"""
path = r"../instances/CBS_k3_n100_m403_b10/CBS_k3_n100_m403_b10_"
i = 1
time_taken = []
solved = 0
satisfiability_maintained = 0
clause_size_reduced, variable_size_reduced = [], []
for i in range(150, 200):
    print(f"Reading file {i}")
    filename = path + str(i) + ".cnf"
    file = open(filename, "r")
    cnf_string = file.read()
    file.close()

    cnf = CNF(cnf_string)

    print("Constructing selector.")
    selector = VariableSelector(cnf_string, verbose=True, cutoff=0, use_dpll=False)

    # time1 = time()

    num_clauses, num_literals = cnf.num_clauses, cnf.num_literals

    print(f"Running selector.\nOriginal cnf has {cnf.num_clauses} clauses and {cnf.num_literals} variables.\nInstance sat is {cnf.solve()}")
    exit_code, cnf = selector.run(to_failure=False, single_path=True)

    print(f"Finished running with exit code {exit_code}.\nReduced cnf has {cnf.num_clauses} clauses and {cnf.num_literals} variables.\nInstance sat is now {cnf.solve()}")

    file = open("../instances/performance_with_purity.txt", "a+")
    file.write(",".join([str(i) for i in
                         [num_literals-cnf.num_literals, num_clauses - cnf.num_clauses, selector.assignments, selector.assignments_to_failure, selector.purity, selector.heuristic, cnf.solve()]]) + "\n")

    
    if cnf.solved:
        solved = True
        satisfiability_maintained = True
    elif cnf.solve():
        satisfiability_maintained = True
        solved = False
    else:
        solved = False
        satisfiability_maintained = False
    clause_size = cnf.num_clauses
    variable_size = cnf.num_literals

    time2 = time() - time1
    print(f"Time taken: {time2}")

    file = open("../instances/performance_no_dpll.txt", "a")
    file.write(",".join(
        [str(i) for i in [solved, satisfiability_maintained, clause_size, variable_size, time2, selector.assignments, selector.assignments_to_failure]]) + "\n")
    file.close()

"""
n = 30
for i in range(60, 120):
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
    info += populator.populate(random=True)

    if info!="":
        print("Writing to main")
        file = open("../instances/main.txt", "a+")
        file.write(info)
        file.close()



print("Function called")
file = open("../instances/main.txt", "r")
txt = [line.strip().split(",") for line in file.readlines()]
file.close()

i = 0
init = False
issues = 0
print("Entering for loop")
try:
    for filename, sat in txt[2589:]:
        info = ""
        i+=1
        print(i, filename)
        if isfile(filename):
            feats = SATInstance(filename, preprocess=False)
            feats.gen_basic_features()

            if init:
                init = False
                header = ",".join(feats.features_dict.keys())
                info = f"filename,{header},sat\n"
                file = open("../instances/dataset_no_dpll.txt", "w")
                file.write(info)
                file.close()
                info = ""
            info += filename + ","
            info += ",".join([str(feats.features_dict[key]) for key in feats.features_dict.keys()])
            info += "," + str(sat) + "\n"
            file = open("../instances/dataset_no_dpll.txt", "a")
            file.write(info)
            file.close()
except Exception as e:
    problem = open(txt[i][0], "r")
    length = len(problem.readlines())
    problem.close()
    print(f"{i} with value {txt[i]} and length {length}")
    raise e

print(f"Number skipped due to issues with dpll probing: {issues}")

