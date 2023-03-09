from statistics import mean
import os

from VariableSelector import VariableSelector
from src.SATInstance.CNF import CNF
from time import time
from SATfeatPy.sat_instance.sat_instance import *
from random import shuffle, randint, choice


class DatasetPopulator:

    def __init__(self, cnf, i=0, filename=""):
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
            self.cnf.rearrange()
            variable = randint(1, self.cnf.num_literals)
            valid = []
            for j in [True, False]:
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

    def random_assignment(self):
        assignments = 0
        while self.cnf.solve():
            success = self.cnf.assign_literal_by_integer(randint(1, self.cnf.num_literals-1)*choice([-1,1]))
            if success == 0:
                assignments += 1
            else:
                break
        file = open("../instances/random_assignment.txt", "a+")
        file.write(",".join([str(100-self.cnf.num_literals), str(403-self.cnf.num_clauses), str(assignments)]) + "\n")
        file.close()
