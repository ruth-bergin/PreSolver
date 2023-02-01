from pysat.solvers import Solver

from src.Clause import Clause
from Literal import Literal
import numpy as np


def check_for_zero_integer(string):
    for index, line in enumerate(string.split("\n")):
        chars = line.split(" ")
        if chars.count("0")>1:
            raise ValueError(f"Index:\t{index}\n{chars}\nRepeated zeros in line: {chars.count(str(0))}")

class TermReducer:

    def __init__(self, cnf_string, sep=" 0\n", verbose=False):
        self.solved = False
        self.unary_unsat = False
        self.verbose = verbose
        self.num_clauses = 0
        self.num_literals = 0
        self.clauses = []
        self.literals = []
        self.unary_clauses = []
        self.assignments = []
        self.recent_assignments = []
        self.construct(cnf_string, sep)
        self.sat = self.solve()
        if self.verbose:
            print("Propagating from __init__()")
        self.propagate_units()

    def construct(self, cnf_string, sep):
        if self.verbose:
            print("Constructing")
        text = [line.strip() for line in cnf_string[cnf_string.find("p cnf"):].split(sep)]
        line1, rest_of_text = text[0], text[1:]
        if "\n" in line1:
            description, first_clause = [line.strip() for line in line1.split("\n")]
            lines = [line for line in [first_clause] + rest_of_text if line!=""]
        else:
            description, lines = line1, rest_of_text
        self.num_literals, self.num_clauses = int(description.split()[-2]), int(description.split()[-1])
        self.literals = [Literal(i) for i in range(1, self.num_literals + 1)]
        self.clauses = [Clause(i) for i in range(self.num_clauses)]
        for index, variables in enumerate(lines):
            clause = self.clauses[index]
            for i in variables.split():
                if np.sign(int(i))==0:
                    raise ValueError(f"Sign for value {i} in clause {index} is 0\nVariables:\n{variables}")
            variables = [variable.strip("\n") for variable in variables.split(" ")]
            variables = list(set([(self.literals[abs(int(i))-1], np.sign(int(i))) for i in variables]))
            if len(variables)==1:
                self.unary_clauses += [clause]
            clause.variables += variables
            for literal, sign in variables:
                clause.size+=1
                if sign > 0:
                    literal.affirmations.append(clause)
                    literal.num_affirmations += 1
                else:
                    literal.negations.append(clause)
                    literal.num_negations += 1
        self.check_for_tautologies()

    def check_for_tautologies(self):
        for literal in self.literals:
            for clause in literal.affirmations:
                if clause in literal.negations:
                    print(f"Handling tautology for clause {clause.index}")
                    self.remove_clause(clause)

    def set_solved(self):
        if not self.sat:
            raise ValueError("Marking as solved when unsat.")
        self.solved = True

    def get_variables_in_unit_clauses(self):
        return [clause.variables[0][0].index*clause.variables[0][1] for clause in self.unary_clauses]

    def check_for_unary_unsat(self):
        for clause in self.unary_clauses:
            for other_clause in self.unary_clauses:
                if clause.variables[0][0]==other_clause.variables[0][0] and clause.variables[0][1]!=other_clause.variables[0][1]:
                    return True
        return False

    def solve(self):
        s = Solver(name='g4')
        for clause in self.get_as_list_of_clauses():
            s.add_clause(clause)
        return s.solve()

    def get_as_list_of_clauses(self):
        return [[int(literal.index*sign) for literal, sign in clause.variables] for clause in self.clauses]

    def assign_literal(self, literal, is_negation, propagating=False):
        if self.solved:
            return
        if self.verbose:
            print("Assigning value {} to literal {}".format(not is_negation, literal.index))
        self.remove_clauses_and_variables(literal, is_negation)
        self.assignments.append((literal.index, not is_negation))
        self.recent_assignments.append((literal.index, not is_negation))
        literal.removed = True
        self.num_literals -= 1
        if not propagating:
            if self.verbose:
                print("Propagating from assign_literal()")
            success = self.propagate_units()
            if success != 0:
                return -1
        self.rearrange()
        return 0

    def remove_clauses_and_variables(self, literal, is_negation):
        satisfied_clauses, unsatisfied_clauses = literal.affirmations, literal.negations
        if is_negation:
            satisfied_clauses, unsatisfied_clauses = literal.negations, literal.affirmations
            print(f"Assigned literal {literal.index} so removing clauses {[clause.index for clause in literal.negations]}")
        for clause in satisfied_clauses:
            self.remove_clause(clause)
            if self.solve() and not self.sat:
                raise ValueError(f"Unsat problem made sat through assignment removing clause {clause.index} from variable assignment {literal.index}")
        for clause in unsatisfied_clauses:
            if self.verbose:
                print("Removing variable {} from clause {}".format(literal.index, clause.index))
            if clause in self.get_unary_clauses():
                self.unary_unsat = True
                return -1
            clause.remove_variable(self, literal, 1)
            if self.solve() and not self.sat:
                raise ValueError("Unsat problem made sat through assignment")

    def assign_literal_by_integer(self, int):
        self.recent_assignments = []
        literal, is_negation = self.get_variable_from_integer(int)
        if self.verbose:
            print(f"Assigning value {not is_negation} to {literal.index}")
        success = self.assign_literal(literal, is_negation)
        if success == 0:
            if self.solve() and not self.sat:
                raise ValueError("Unsat problem made sat through assignment")
        return success

    def propagate_units(self):
        if self.unary_unsat:
            return -1
        while len(self.get_unary_clauses())>0 and not self.solved:
            if self.verbose:
                print(
                    f"Current unary clause list: {[clause.variables[0][0].index*clause.variables[0][1] for clause in self.get_unary_clauses()]}")
            clause = self.get_unary_clauses()[-1]
            if self.verbose:
                print("Clause chosen: {}".format(clause.variables[0][0].index*clause.variables[0][1]))
            literal, is_negation = clause.variables[0][0], clause.variables[0][1]<0
            if self.verbose:
                print("Removing unary clause {} with literal {} {}".format(self.get_unary_clauses()[-1], literal.index, not is_negation))
            success = self.assign_literal(literal, is_negation, propagating=True)
            if success!=0:
                if self.verbose:
                    print(f"Contradictory unary clauses for literal {literal.index}. Aborting assignment.")
                return -1
        return 0

    def remove_clause(self, clause):
        if clause.size<2:
            if clause in self.unary_clauses:
                self.unary_clauses.remove(clause)
        if self.verbose:
            print("Removing clause {}".format(clause.index))
        self.num_clauses -= 1
        clause.removed = True
        print(f"Clause {clause.index} removed successfully.")

    def get_variable_from_integer(self, int):
        literal_index = abs(int)-1
        is_negation = int<0
        try:
            literal = self.literals[literal_index]
        except Exception as e:
            print(f"{e}: attempting to access index {literal_index} with list length {len(self.literals)} and num literals {self.num_literals}")
            raise e
        return literal, is_negation

    def rearrange(self):
        if self.solved or self.num_literals==len(self.literals):
            return
        self.clauses = [clause for clause in self.clauses if not clause.removed and clause.size>0]
        for literal in self.literals:
            literal.affirmations = [clause for clause in literal.affirmations if not clause.removed]
            literal.negations = [clause for clause in literal.negations if not clause.removed]
            literal.num_affirmations, literal.num_negations = len(literal.affirmations), len(literal.negations)
        self.literals = [literal for literal in self.literals
                         if not literal.removed and literal.num_negations+literal.num_affirmations>0]
        self.unary_clauses = [clause for clause in self.clauses if clause.size==1]
        for index, clause in enumerate(self.clauses):
            clause.index = index
        for index, literal in enumerate(self.literals):
            literal.index = index + 1
        self.num_literals = len(self.literals)
        self.num_clauses = len(self.clauses)
        if self.verbose:
            print("Propagating from rearrange()")
        success = self.propagate_units()
        if not success:
            return -1
        if self.num_clauses<2 or self.num_literals<2:
            self.set_solved()

    def __str__(self):
        if self.verbose:
            print("Propagating from __str__()")
        self.propagate_units()
        self.rearrange()
        if self.solved:
            return ""
        string = "p cnf {} {}\n".format(self.num_literals, self.num_clauses)
        for clause in self.clauses:
            for literal, sign in clause.variables:
                if sign==0:
                    raise ValueError("Sign is somehow zero???")
                elif literal.index==0:
                    raise ValueError("Literal index is 0 despite check otherwise")
                try:
                    string += "{} ".format(literal.index*sign)
                except:
                    string += "error "
            string = string + "0\n"
        return string

    def check_for_zero_literal(self):
        for literal in self.literals:
            if literal.index==0:
                raise ValueError("Literal index 0")

    def get_unary_clauses(self):
        return [clause for clause in self.clauses if len(clause.variables)==1 and not clause.removed]
