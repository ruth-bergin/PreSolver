from statistics import mean
import os
from VariableSelector import VariableSelector
from time import time
"""
file = open("instances/basic.txt", "r")

cnf_string = file.read()
print("\n", cnf_string[cnf_string.find("p cnf"):cnf_string.find("p cnf")+17], "\n")
file.close()

vs = VariableSelector(cnf_string, cutoff=-0.5)
reduced_cnf = vs.run()

print(reduced_cnf)


"""

def ii_dataset():
    times = []
    num_solved = 0
    n = 41

    path = "instances/inductive-inference"
    i = 1
    for fn in os.listdir(path):
        print(f"On file {i} ~ {fn}")
        start_time = time()
        file = open(path+"/"+fn, "r")
        cnf_string = file.read()
        print("\n", cnf_string[cnf_string.find("p cnf"):cnf_string.find("p cnf")+17], "\n")
        file.close()

        vs = VariableSelector(cnf_string, cutoff=-0.5)
        vs.run()

        time_taken = time() - start_time
        times.append(time_taken)
        print(f"Time taken:\t{time_taken//60} minutes {time_taken%60} seconds")

        if vs.solved:
            num_solved += 1
            print("solved")

        print("\n~~~~~~~\n")
        i += 1


    string = f"PROPORTION SOLVED:\t{num_solved / n}\nTIMING:\nMIN:\t{min(times)}\tMAX:\t{max(times)}\tMEAN:\t{mean(times)}\nTimes:\t{times}"

    print(string)

def CBS_dataset():
    times = []
    reduction_prop = []
    num_solved = 0
    n = 100

    for i in range(n):
        print("Starting CNF {}".format(i))
        start_time = time()
        fn = "instances/CBS_k3_n100_m403_b10/CBS_k3_n100_m403_b10_{}.cnf".format(i)
        file = open(fn, "r")
        cnf_string = file.read()
        file.close()

        org_num_clauses = len(cnf_string[cnf_string.find("p cnf"):].split("\n"))-1
        vs = VariableSelector(cnf_string, cutoff=-0.5)
        reduced_cnf = vs.run()[1]

        times.append(time() - start_time)

        if vs.solved:
            num_solved += 1
        else:
            reduced_num_clauses = reduced_cnf.num_clauses
            reduction_prop.append(reduced_num_clauses/org_num_clauses)

    print()
    print("PROPORTION SOLVED:\t{}".format(num_solved / n))
    print("TIMES\nMIN:\t{}\nMAX:\t{}\nMEAN:\t{}\n".format(min(times), max(times), mean(times)))
    print("REDUCED TO PROP OF ORIGINAL\nMIN:\t{}\nMAX:\t{}\nMEAN:\t{}\n".format(min(reduction_prop), max(reduction_prop), mean(reduction_prop)))

CBS_dataset()