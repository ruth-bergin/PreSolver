from statistics import mean
import os
from VariableSelector import VariableSelector
from time import time

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
    num_solved = 0
    n = 500

    for i in range(n):
        print("Starting CNF {}".format(i))
        start_time = time()
        fn = "instances/CBS_k3_n100_m403_b10/CBS_k3_n100_m403_b10_{}.cnf".format(i)
        file = open(fn, "r")
        cnf_string = file.read()
        file.close()

        vs = VariableSelector(cnf_string, cutoff=-0.5)
        vs.run()

        times.append(time() - start_time)

        if vs.solved:
            num_solved += 1

    print()
    print("PROPORTION SOLVED:\t{}".format(num_solved / n))
    print("MIN:\t{}\nMAX:\t{}\nMEAN:\t{}\n".format(min(times), max(times), mean(times)))

ii_dataset()