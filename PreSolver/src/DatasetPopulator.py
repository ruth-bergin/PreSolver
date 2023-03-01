from statistics import mean
import os

from VariableSelector import VariableSelector
from src.SATInstance.CNF import CNF
from time import time
from SATfeatPy.sat_instance.sat_instance import *
from random import shuffle, randint, choice


class DatasetPopulator:

    def __init__(self, i, filename, cnf):
        self.i = i
        self.filename = filename
        self.cnf = cnf

    def populate(self, random=False):
        print(f"Random: {random}")
        string = ""
        i = 0
        prev_cnf = None
        while (str(prev_cnf)!=str(self.cnf)):
            prev_cnf = self.cnf
            print(f"On assignment {i}.")
            self.cnf.rearrange()
            variable = randint(1, self.cnf.num_literals)
            valid = []
            for j in [True, False]:
                print(f"Solving for shadow branch {j} - num literals {self.cnf.num_literals}")
                try:
                    name, shadow_cnf = self.write_and_solve_shadow_cnf(variable, self.convert_to_int(j))
                    if shadow_cnf.solved:
                        print("###Solved.###")
                        return string
                    if str(shadow_cnf)==str(self.cnf):
                        sat=False
                    else:
                        sat = shadow_cnf.solve()
                    if sat:
                        valid.append((shadow_cnf, j))
                    elif random:
                        valid.append((shadow_cnf, j))
                    row = f"{name},{sat}\n"
                    string += row
                except Exception as e:
                    raise e
            if len(valid)<1:
                raise ValueError(f"Neither is SAT. Problem. {self.cnf.solve()}")
            assignment = choice(valid)
            print(f"Assigning value {assignment[1]} to {variable}.")
            self.cnf = assignment[0]
            i += 1
        if str(self.cnf)==str(prev_cnf):
            print("***No further change viable.***")
        return string

    def get_shadow_divergence(self, shadow):
        i = 0
        org = str(self.cnf).split("\n")
        shadow = str(shadow).split("\n")
        print(f"ORG\n{org[0]}\nSHADOW\n{shadow[0]}")
        while i < len(org):
            if org[i]!=shadow[i]:
                print(f"Divergence at {i}\nORG\n{org[i]}\nSHADOW\n{shadow[i]}")
                break
            i += 1

    def write_and_solve_shadow_cnf(self, variable, assignment):
        if variable>self.cnf.num_literals:
            raise IndexError("Num literals changed since function call.")
        shadow_cnf = CNF(str(self.cnf))
        if variable>shadow_cnf.num_literals:
            raise IndexError(f"Num literals changed since shadow cnf formation. Variable {variable} num lit {shadow_cnf.num_literals}")
        success = shadow_cnf.assign_literal_by_integer(variable*assignment)
        name = f"../instances/shadow/{self.i}_n{self.cnf.num_literals}_m{self.cnf.num_clauses}_{variable}{assignment}.txt"
        if success != 0:
            print("~~~~~~Returning shadow CNF to original state.~~~~~~")
            shadow_cnf = CNF(str(self.cnf))
        elif not shadow_cnf.solved:
            fn = open(name, "w")
            fn.write(str(shadow_cnf))
            fn.close()
        return name, shadow_cnf

    def convert_to_int(self, sat):
        if sat:
            return 1
        return -1

    def generate_satfeatpy_dataset(self, init=False):
        print("Function called")
        file = open("../instances/main.txt", "r")
        txt = [line.strip().split(",") for line in file.readlines()]
        file.close()

        if init:
            info = "filename,c,v,clauses_vars_ratio,vars_clauses_ratio,vcg_var_mean,vcg_var_coeff,vcg_var_min,vcg_var_max,vcg_var_entropy,vcg_clause_mean,vcg_clause_coeff,vcg_clause_min,vcg_clause_max,vcg_clause_entropy,vg_mean,vg_coeff,vg_min,vg_max,pnc_ratio_mean,pnc_ratio_coeff,pnc_ratio_min,pnc_ratio_max,pnc_ratio_entropy,pnv_ratio_mean,pnv_ratio_coeff,pnv_ratio_min,pnv_ratio_max,pnv_ratio_entropy,pnv_ratio_stdev,binary_ratio,ternary_ratio,ternary+,hc_fraction,hc_var_mean,hc_var_coeff,hc_var_min,hc_var_max,hc_var_entropy,sat\n"
            file = open("../instances/dataset.txt", "w")
            file.write(info)
            file.close()

        i = 0
        print("Entering for loop")
        try:
            for filename, sat in txt[3::9]:
                info = ""
                i+=1
                print(i, filename)
                feats = SATInstance(filename, preprocess=False)
                feats.gen_basic_features()
                info += filename + ","
                info += ",".join([str(feats.features_dict[key]) for key in feats.features_dict.keys()])
                info += "," + str(sat) + "\n"
                file = open("../instances/dataset.txt", "a")
                file.write(info)
                file.close()
        except Exception as e:
            print(f"{i+1} with value {txt[i+1]}")
            raise e

    def solve_ii_dataset(self):

        path = r"..\instances\inductive-inference"
        i = 1
        info = ""
        files = os.listdir(path)
        shuffle(files)
        for fn in files:
            i += 1
            print(f"On file {i} ~ {fn}")
            file = open(path+"/"+fn, "r")
            cnf_string = file.read()
            file.close()

            cnf = CNF(cnf_string, sep="\n 0 \n")
            populator = DatasetPopulator(fn[:-4], fn[:-4], cnf)
            info += populator.populate(random=i % 4 == 0)

            file = open("../instances/main.txt", "a")
            file.write(info)
            file.close()

    def ii_dataset(self):
        times = []
        red_prop = []
        num_solved = 0
        n = 41

        path = "../instances/inductive-inference"
        i = 1
        for fn in os.listdir(path):
            print(f"On file {i} ~ {fn}")
            start_time = time()
            file = open(path+"/"+fn, "r")
            cnf_string = file.read()
            print("\n", cnf_string[cnf_string.find("p cnf"):cnf_string.find("p cnf")+17], "\n")
            file.close()

            vs = VariableSelector(cnf_string, cutoff=-0.5)
            org_num_clauses = vs.cnf.num_clauses
            reduced_cnf = vs.run()[1]

            time_taken = time() - start_time
            times.append(time_taken)
            print(f"Time taken:\t{time_taken//60} minutes {time_taken%60} seconds")

            reduced_num_clauses = reduced_cnf.num_clauses
            red_prop.append(reduced_num_clauses/org_num_clauses)

            if vs.solved:
                num_solved += 1
                print("solved")

            print("\n~~~~~~~\n")
            i += 1
            break


        string = f"PROPORTION SOLVED:" \
                 f"\t{num_solved / n}\n" \
                 f"TIMING:\nMIN:\t{min(times)}\tMAX:\t{max(times)}\tMEAN:\t{mean(times)}\n" \
                 f"Times:\t{times}" \
                 f"REDUCED TO PROP OF ORIGINAL\nMIN:\t{min(red_prop)}\nMAX:\t{max(red_prop)}\nMEAN:\t{mean(red_prop)}\n"
        print(string)

    def CBS_dataset(self):
        times = []
        reduction_prop = []
        num_solved = 0
        n = 10

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


