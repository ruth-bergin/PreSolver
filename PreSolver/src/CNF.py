from pysat.solvers import Solver

from src.Clause import Clause
from Literal import Literal
import numpy as np


class CNF:

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
        self.construct(cnf_string, sep)
        self.sat = self.solve()
        if self.verbose:
            print(f"Propagating from __init__() with unary clauses {[clause.index for clause in self.unary_clauses]}")
        self.propagate_units()

    def construct(self, cnf_string, sep):
        if self.verbose:
            print("Constructing")
        text = [line.strip() for line in cnf_string[cnf_string.find("p cnf"):].split(sep)]
        line1, rest_of_text = text[0], text[1:]
        if "\n" in line1:
            description, first_clause = [line.strip() for line in line1.split("\n")]
            lines = [line for line in [first_clause] + rest_of_text if line != ""]
        else:
            description, lines = line1, rest_of_text
        self.num_literals, self.num_clauses = int(description.split()[-2]), int(description.split()[-1])
        self.literals = [Literal(i) for i in range(1, self.num_literals + 1)]
        self.clauses = [Clause(i) for i in range(self.num_clauses)]
        for index, variables in enumerate(lines):
            if index >= self.num_clauses:
                raise ValueError(f"Number of clauses {self.num_clauses} and number of lines {len(lines)} do not match.")
            clause = self.clauses[index]
            for i in variables.split():
                if np.sign(int(i)) == 0:
                    raise ValueError(f"Sign for value {i} in clause {index} is 0\nVariables:\n{variables}")
            variables = [variable.strip("\n") for variable in variables.split(" ") if variable!=""]
            try:
                variables = [(self.literals[abs(int(i)) - 1], np.sign(int(i))) for i in variables]
            except Exception as e:
                print(self.num_literals, len(variables), "\n", variables)
                raise e
            if len(variables) == 1:
                self.unary_clauses += [clause]
            clause.variables += variables
            for literal, sign in variables:
                clause.size += 1
                if sign > 0:
                    literal.affirmations.append(clause)
                    literal.num_affirmations += 1
                else:
                    literal.negations.append(clause)
                    literal.num_negations += 1

    @staticmethod
    def get_sign_from_bool(boolean):
        if boolean:
            return 1
        return -1

    def set_solved(self):
        if not self.sat:
            raise ValueError("Marking as solved when unsat.")
        self.solved = True

    def solve(self):
        s = Solver(name='g4')
        for clause in self.get_as_list_of_clauses():
            s.add_clause(clause)
        return s.solve()

    def get_as_list_of_clauses(self):
        return [[int(literal.index * sign) for literal, sign in clause.variables] for clause in self.clauses]

    def assign_literal(self, literal, is_negation):
        if (literal, not is_negation) in [clause.variables[0] for clause in self.unary_clauses]:
            if self.verbose:
                print("Contradictory unit clauses. Aborting.")
            return -1
        if literal.removed:
            raise ValueError(f"Attempting to assign {literal.index} when it has already been assigned.")
        if self.solved:
            return
        if self.verbose:
            print("Assigning value {} to literal {}".format(not is_negation, literal.index))
        success = self.handle_clause_removal_and_reduction(literal, is_negation)
        if success != 0:
            return -1
        self.assignments.append((literal.index, not is_negation))
        literal.removed = True
        self.num_literals -= 1
        return 0

    def handle_clause_removal_and_reduction(self, literal, is_negation):
        assignment = not is_negation
        satisfied_clauses, unsatisfied_clauses = literal.negations, literal.affirmations
        if assignment:
            satisfied_clauses, unsatisfied_clauses = literal.affirmations, literal.negations
        for clause_list in [satisfied_clauses, unsatisfied_clauses]:
            if (not all([len(clause.variables)==clause.size for clause in clause_list])) or any([clause.removed for clause in clause_list]):
                raise ValueError(f"Clauses:\t{[(clause.index, len(clause.variables), clause.size, clause.removed, (literal, self.get_sign_from_bool(assignment)) in clause.variables) for clause in clause_list]}")
        if self.verbose:
            print(
                f"Assigned literal {literal.index} so removing clauses {[str(clause) for clause in satisfied_clauses]}")
        while len(satisfied_clauses)>0:
            clause = satisfied_clauses[-1]
            if clause.removed:
                raise ValueError(f"Clause {clause} has been removed.")
            if (literal, self.get_sign_from_bool(assignment)) not in clause.variables:
                raise ValueError(
                    f"Infeasible assignment - literal {literal.index} not in clause {clause} so cannot satisfy it.\n"
                    f"Check for other clauses: {[(literal, self.get_sign_from_bool(assignment)) in clause.variables for clause in satisfied_clauses]}")
            self.remove_clause(clause)
        if self.verbose:
            print(
                f"Assigned literal {literal.index} so reducing clauses {[clause.index for clause in unsatisfied_clauses]}")
        for clause in unsatisfied_clauses:
            if clause.removed:
                raise ValueError(f"Clause has {clause} been removed.")
            if (literal, self.get_sign_from_bool(not assignment)) not in clause.variables:
                raise ValueError(
                    f"Infeasible assignment - literal {literal.index} is not present in clause {clause} to be removed.\n"
                    f"Previous clause: {self.clauses[clause.index - 1]}\n"
                    f"Next clause: {self.clauses[clause.index + 1]}")
            if clause in self.unary_clauses:
                self.unary_unsat = True
                return -1
            clause.remove_variable(self, literal, self.get_sign_from_bool(not assignment))
        return 0

    def remove_clause(self, clause):
        clause.removed = True
        for literal, assignment in clause.variables:
            if assignment>0:
                if literal.affirmations.count(clause)>1:
                    raise ValueError(f"Count for clause {clause} in literal {literal.index} is {literal.affirmations.count(clause)}")
                literal.affirmations.remove(clause)
                literal.num_affirmations -= 1
            else:
                if literal.negations.count(clause)>1:
                    raise ValueError(f"Count for clause {clause} in literal {literal.index} is {literal.negations.count(clause)}")
                literal.negations.remove(clause)
                literal.num_negations -= 1
        self.num_clauses -= 1

    def propagate_units(self):
        if len(self.unary_clauses) == 0:
            return 1
        while len(self.unary_clauses) > 0:
            if self.verbose:
                print(
                    f"Current unary clause list: {[str(clause) for clause in self.unary_clauses]}")
            clause = self.unary_clauses[0]
            if not clause.removed:
                literal, is_negation = clause.variables[0][0], clause.variables[0][1] < 0
                success = self.assign_literal(literal, is_negation)
                if success != 0:
                    return -1
            elif self.verbose:
                print(f"Clause {clause} has been removed already, skipping")
            self.unary_clauses.remove(clause)
        self.check_for_sat_violation()
        return 0

    def assign_literal_by_integer(self, integer):
        literal, is_negation = self.get_variable_from_integer(integer)
        success = self.assign_literal(literal, is_negation)
        self.rearrange()
        if self.verbose:
            print(f"Completed run of assignment of {integer}")
        print(f"Satisfiability: {self.solve()}")
        return success

    def get_variable_from_integer(self, integer):
        literal_index, is_negation = abs(integer) - 1, integer < 0
        try:
            literal = self.literals[literal_index]
        except Exception as e:
            print(
                f"{e}: attempting to access index {literal_index} with list length {len(self.literals)} and num literals {self.num_literals}")
            raise e
        return literal, is_negation

    def rearrange(self):
        if self.solved or self.num_literals == len(self.literals):
            return
        self.clauses = [clause for clause in self.clauses if not clause.removed and clause.size > 0]
        for literal in self.literals:
            literal.affirmations = [clause for clause in literal.affirmations if not clause.removed]
            literal.negations = [clause for clause in literal.negations if not clause.removed]
            literal.num_affirmations, literal.num_negations = len(literal.affirmations), len(literal.negations)
        self.literals = [literal for literal in self.literals
                         if not literal.removed and literal.num_negations + literal.num_affirmations > 0]
        for index, clause in enumerate(self.clauses):
            clause.index = index
        for index, literal in enumerate(self.literals):
            literal.index = index + 1
        self.num_literals = len(self.literals)
        self.num_clauses = len(self.clauses)
        if self.verbose:
            print("Propagating from rearrange()")
        if self.num_clauses < 2 or self.num_literals < 2:
            self.solved = True
        self.unary_clauses = [clause for clause in self.clauses if clause.size == 1]
        if self.propagate_units() == 0:
            return self.rearrange()

    def check_for_sat_violation(self):
        if not self.sat and self.solve():
            raise ValueError("Unsat problem made sat through assignment.")

    def __str__(self):
        self.rearrange()
        if self.solved:
            return ""
        string = "p cnf {} {}\n".format(self.num_literals, self.num_clauses)
        for clause in self.clauses:
            for literal, sign in clause.variables:
                if sign == 0:
                    raise ValueError("Sign is somehow zero???")
                elif literal.index == 0:
                    raise ValueError("Literal index is 0 despite check otherwise")
                try:
                    string += "{} ".format(literal.index * sign)
                except:
                    string += "error "
            string = string + "0\n"
        return string
