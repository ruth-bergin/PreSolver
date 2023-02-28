from SATfeatPy.sat_instance.sat_instance import SATInstance
from CNF import CNF
from VariableSelector import VariableSelector
from DatasetPopulator import DatasetPopulator
from os.path import isfile


print("Reading file")
filename = "../instances/CBS_k3_n100_m403_b10/CBS_k3_n100_m403_b10_3.cnf"
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

"""

n = 30
for i in range(2*n, 4*n):
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
    info += populator.populate(random=i%3!=0)

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
init = True
issues = 0
print("Entering for loop")
# Reached 520:824
try:
    for filename, sat in txt[520:]:
        info = ""
        i+=1
        print(i, filename)
        if isfile(filename):
            feats = SATInstance(filename, preprocess=False)
            feats.gen_basic_features()

            try:
                feats.gen_dpll_probing_features()
            except Exception as e:
                print("Error.")
                issues += 1
                cnf = open(filename, "r")
                cnf_string = file.read()
                cnf.close()
                fn = open(f"/instances/dpll/example_{issues}", "w+")
                fn.write(cnf_string)
                fn.close()
                continue

            if init:
                init = False
                header = ",".join(feats.features_dict.keys())
                info = f"filename,{header},sat\n"
                file = open("../instances/dataset.txt", "w")
                file.write(info)
                file.close()
                info = ""
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

print(f"Number skipped due to issues with dpll probing: {issues}")
"""