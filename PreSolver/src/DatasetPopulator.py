from CNF import CNF
from random import randint, choice

class DatasetPopulator:

    def __init__(self, i, filename, cnf):
        self.i = i
        self.filename = filename
        self.cnf = cnf

    def populate(self, random=True):
        string = ""
        i = 0
        prev_num_clauses = 1
        reassigning = 0
        while (prev_num_clauses!=self.cnf.num_clauses or reassigning>0) and reassigning<3\
                and not self.cnf.solved:
            self.cnf.rearrange()
            print(f"On assignment {i}.")
            prev_num_clauses = self.cnf.num_clauses
            if reassigning<1:
                i += 1
            self.cnf.rearrange()
            variable = randint(0, self.cnf.num_literals-1)
            if reassigning > 0:
                print("Current literal index: {} length of list: {} variable random assignment: {}".format(self.cnf.num_literals-1, len(self.cnf.literals), variable))
            valid = []
            for j in [True, False]:
                print(f"Solving for shadow branch {j} - num literals {self.cnf.num_literals}")
                try:
                    name, shadow_cnf = self.write_and_solve_shadow_cnf(variable, self.convert_to_int(j))
                    if shadow_cnf==self.cnf:
                        sat=False
                    else:
                        sat = shadow_cnf.solve()
                    if sat:
                        print(f"{j} is sat for variable {variable}")
                        valid.append((shadow_cnf, j))
                    elif random:
                        valid.append((shadow_cnf, j))
                    row = f"{name},{sat}\n"
                    string += row
                except Exception as e:
                    raise e
            if len(valid)<1:
                print(f"Neither is SAT. Problem. {self.cnf.solve()}")
                reassigning += 1
            else:
                reassigning = 0
            if reassigning > 0:
                print(f"Reassigning value: {reassigning}")
                continue
            assignment = choice(valid)
            print(f"Assigning value {assignment[1]} to {variable}.")
            self.cnf = assignment[0]
            if not self.cnf.solve() and not random:
                print("ISSUE: variable {} assignment {} is not SAT but was found to be.".format(variable, assignment))
                raise ValueError
        if self.cnf.solved:
            print("Solved.")
        elif prev_num_clauses==self.cnf.num_clauses:
            print("No further change viable.")
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
        shadow_cnf = CNF(str(self.cnf), verbose=True)
        if variable>shadow_cnf.num_literals:
            raise IndexError(f"Num literals changed since shadow cnf formation. Variable {variable} num lit {shadow_cnf.num_literals}")
        success = shadow_cnf.assign_literal_by_integer(variable*assignment)
        if success !=0:
            shadow_cnf = CNF(str(self.cnf))
        name = f"../instances/shadow/{self.i}_n{self.cnf.num_literals}_m{self.cnf.num_clauses}_{variable}{assignment}.txt"
        fn = open(name, "w")
        fn.write(str(shadow_cnf))
        fn.close()
        return name, shadow_cnf

    def convert_to_int(self, sat):
        if sat:
            return 1
        return -1

