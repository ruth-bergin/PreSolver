from src.SATInstance.CNF import CNF
from random import randint, choice


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
        # Condition: prevent infinite loop of aborted variable assignments
        while (str(prev_cnf)!=str(self.cnf)):
            prev_cnf = self.cnf
            # Choose a random variable
            variable = randint(1, self.cnf.num_literals)
            # Valid branches to pursue - relevant if only following SAT branches
            valid = []
            # Assigning both ways
            for j in [True, False]:
                name, shadow_cnf = self.write_and_solve_shadow_cnf(variable, self.convert_to_int(j))
                if shadow_cnf.solved:
                    print("###Solved.###")
                    return string
                # if the assignment was aborted it must be unsat
                if str(shadow_cnf)==str(self.cnf):
                    sat=False
                else:
                    sat = shadow_cnf.solve()
                if sat:
                    valid.append((shadow_cnf, j))
                # ignore the sat-only criterion if randomised
                elif random:
                    valid.append((shadow_cnf, j))
                row = f"{name},{sat}\n"
                string += row
            if len(valid)<1:
                raise ValueError(f"Neither branch is SAT, despite the requirement.")
            assignment = choice(valid)
            self.cnf = assignment[0]
            i += 1
        if str(self.cnf)==str(prev_cnf):
            print("***No further change viable.***")
        return string

    def write_and_solve_shadow_cnf(self, variable, assignment):
        if variable>self.cnf.num_literals:
            raise IndexError("Num literals changed since function call.")
        # Create a copy of the CNF so the original is unchanged
        shadow_cnf = CNF(str(self.cnf))
        if variable>shadow_cnf.num_literals:
            raise IndexError(f"Num literals changed since shadow cnf formation. Variable {variable} num lit {shadow_cnf.num_literals}")
        outcome = shadow_cnf.assign_literal_by_integer(variable*assignment)
        name = f"../instances/population/{self.i}_n{self.cnf.num_literals}_m{self.cnf.num_clauses}_{variable}{str(assignment>0)}.txt"
        # Return the original cnf if assignment aborted
        if outcome != 0:
            shadow_cnf = CNF(str(self.cnf))
        # If it's solved there's no CNF to save
        elif not shadow_cnf.solved:
            fn = open(name, "w")
            fn.write(str(shadow_cnf))
            fn.close()
        return name, shadow_cnf

    def convert_to_int(self, sat):
        if sat:
            return 1
        return -1
