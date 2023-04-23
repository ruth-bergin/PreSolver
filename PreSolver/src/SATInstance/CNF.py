from pysat.solvers import Solver

from src.SATInstance.Clause import Clause
from src.SATInstance.Literal import Literal
import numpy as np


class CNF:

    def __init__(self, cnf_string, sep=" 0\n", verbose=False):
        self.solved = False
        self.verbose = verbose
        self.num_clauses = 0
        self.num_literals = 0
        self.clauses = []
        self.literals = []
        self.unary_clauses = []
        self.assignments = []
        self.construct(cnf_string, sep)
        self.update_covariance_matrix()
        self.update_covariance_matrix_statistics()
        self.sat = self.solve()
        if self.verbose:
            print(f"Propagating from __init__() with unary clauses {[clause.index for clause in self.unary_clauses]}")
        self.propagate_units()
        for literal in self.literals:
            literal.instance_num_clauses = self.num_clauses

    def construct(self, cnf_string, sep):
        if self.verbose:
            print("Constructing")
        text = [line.strip() for line in cnf_string[cnf_string.find("p cnf"):].split(sep)]
        line1, rest_of_text = text[0], text[1:]
        if "\n" in line1:
            try:
                description, first_clause = [line.strip() for line in line1.split("\n")]
            except Exception as e:
                print(line1.split("\n"))
                raise e
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
        if (literal, self.get_sign_from_bool(is_negation)) in [clause.variables[0] for clause in self.unary_clauses]:
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
        if self.verbose:
            print(
                f"Assigned literal {literal.index} so removing clauses {[str(clause) for clause in satisfied_clauses]}")
        if len(satisfied_clauses)==0 and self.verbose:
            print(f"No clauses satisfied. Clauses unsatisfied: {[str(clause) for clause in unsatisfied_clauses]}")
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
                f"Assigned literal {literal.index} so reducing clauses {[str(clause) for clause in unsatisfied_clauses]}")
        for clause in unsatisfied_clauses:
            if clause.removed:
                raise ValueError(f"Clause has {clause} been removed.")
            if (literal, self.get_sign_from_bool(not assignment)) not in clause.variables:
                raise ValueError(
                    f"Infeasible assignment - literal {literal.index} is not present in clause {clause} to be removed.\n"
                    f"Previous clause: {self.clauses[clause.index - 1]}\n"
                    f"Next clause: {self.clauses[clause.index + 1]}")
            if clause in self.unary_clauses:
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
        i = 0
        if len(self.unary_clauses) == 0:
            if self.verbose:
                print("No unit clauses to propagate.")
            return 1
        if len(self.unary_clauses) > 0:
            i += 1
            if self.verbose:
                print(
                    f"Current unary clause list: {[str(clause) for clause in self.unary_clauses]}")
            clause = self.unary_clauses[-1]
            if not clause.removed:
                literal, is_negation = clause.variables[0][0], clause.variables[0][1] < 0
                if not literal.removed:
                    success = self.assign_literal(literal, is_negation)
                    if success != 0:
                        if self.verbose:
                            print("Failed to assign unit clause. Aborting.")
                        return -1
                elif self.verbose:
                    raise ValueError(f"Clause {clause} has not been removed already, but its literal {literal.index} has")
            elif self.verbose:
                print(f"Clause {clause} has been removed already, skipping")
            self.unary_clauses.remove(clause)
        return 0

    def assign_literal_by_integer(self, integer):
        literal, is_negation = self.get_variable_from_integer(integer)
        num_clauses, num_literals = self.num_clauses, self.num_literals
        success = self.assign_literal(literal, is_negation)
        if success < 0:
            return success
        success = self.rearrange()
        if self.verbose:
            print(f"Completed run of assignment of {integer} with success {success}")
            print(f"Satisfiability: {self.solve()}")
        self.check_for_literal_clause_inconsistency()
        self.check_for_sat_violation()
        self.update_covariance_matrix()
        self.update_covariance_matrix_statistics()
        return success

    def check_for_literal_clause_inconsistency(self):
        literals_still_contain_clauses, clauses_still_contain_literals = 0, 0
        unique_literals, unique_clauses = 0,0
        clauses, literals = {}, {}
        for literal in self.literals:
            unique = True
            for clause in literal.affirmations:
                if (literal, 1) not in clause.variables:
                    literals_still_contain_clauses += 1
                    if unique:
                        unique = False
                        unique_literals += 1
                    literals[str(literal.index)] = f"{literals.get(str(literal.index), str())} {str(clause)}\n"
            for clause in literal.negations:
                if (literal, -1) not in clause.variables:
                    literals_still_contain_clauses += 1
                    if unique:
                        unique = False
                        unique_literals += 1
                    literals[str(literal.index)] = f"{literals.get(str(literal.index), str())} {str(clause)}\n"
        for clause in self.clauses:
            unique = True
            for literal, sign in clause.variables:
                if sign>0:
                    if clause not in literal.affirmations:
                        clauses_still_contain_literals += 1
                        if unique:
                            unique = False
                            unique_clauses += 1
                        clauses[str(clause.index)] = f"{clauses.get(str(clause.index), str())} {str(literal)}\n"
                elif clause not in literal.negations:
                    clauses_still_contain_literals += 1
                    if unique:
                        unique = False
                        unique_clauses += 1
                    clauses[str(clause.index)] = f"{clauses.get(str(clause.index), str())} {str(literal)}\n"
        if literals_still_contain_clauses + clauses_still_contain_literals>0:
            raise ValueError(f"Inconsistency with clause and literal lists.\n"
                             f"{unique_clauses} unique clauses mention a total of {clauses_still_contain_literals} literals which don't mention them.\n"
                             f"{[(clause, clauses[clause]) for clause in clauses.keys()]}\n"
                             f"{unique_literals} unique literals mention a total of {literals_still_contain_clauses} clauses which don't contain them.\n"
                             f"{literals}")


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
        if self.solved or (self.num_literals == len(self.literals) and self.num_clauses == len(self.clauses)):
            return 0
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
        if self.num_clauses < 2:
            self.solved = True
            return 0
        self.unary_clauses = [clause for clause in self.clauses if clause.size == 1]
        if self.literals[-1].index!=self.num_literals:
            raise ValueError(f"Largest index {self.literals[-1].index} with {self.num_literals} literals counted.")
        if self.verbose:
            print("Propagating from rearrange()")
        success = self.propagate_units()
        if success == 0:
            return self.rearrange()
        elif success < 0:
            return -1
        for literal in self.literals:
            literal.instance_num_clauses = self.num_clauses
        return 0

    def check_for_sat_violation(self):
        if not self.sat and self.solve():
            raise ValueError("Unsat problem made sat through assignment.")

    def __str__(self):
        self.rearrange()
        if len(self.unary_clauses)>0 and not self.solved:
            print(f"There shouldn't be unit clauses.\n{[str(clause) for clause in self.unary_clauses]}")
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

    def update_covariance_matrix(self):
        self.covariance_matrix = [[0 for i in range(self.num_literals*2)] for j in range(self.num_literals*2)]
        for clause in self.clauses:
            for variable, assignment in clause.variables:
                for other_variable, other_assignment in clause.variables:
                    index, other_index = variable.index - 1, other_variable.index - 1
                    if assignment==-1:
                        index += self.num_literals
                    if other_assignment == -1:
                        other_index += self.num_literals
                    try:
                        self.covariance_matrix[index][other_index] += 1
                        self.covariance_matrix[other_index][index] += 1
                    except:
                        raise ValueError(
                            f"Covariance matrix size {len(self.covariance_matrix)} "
                            f"with index {index} and other index {other_index}")

    def update_covariance_matrix_statistics(self):
        for literal in self.literals:
            literal.calculate_clause_summary_statistics()
        count_value = [[1,0] for i in range(self.num_literals*2)]
        metrics = []
        i= 0
        while i < self.num_literals*2:
            j = 0
            total_children = sum(self.covariance_matrix[i])
            if total_children == 0:
                metric = 0
            elif i < self.num_literals:
                metric = self.literals[i].get_metric(False)/self.literals[i].get_metric(True)
                metric = metric/total_children
            else:
                metric = self.literals[i-self.num_literals].get_metric(True)/self.literals[i-self.num_literals].get_metric(False)
                metric = metric/total_children
            while j < self.num_literals*2:
                count_value[j][0] += 1
                count_value[j][1] += metric * self.covariance_matrix[i][j]
                j += 1
            metrics.append(metric)
            i += 1
        for i in range(self.num_literals):
            if count_value[i][0]==0:
                self.literals[i].covariance_matrix_statistics_true = 0
            else:
                self.literals[i].covariance_matrix_statistic_true = count_value[i][1]
        for i in range(self.num_literals, 2*self.num_literals):
            if count_value[i][0]==0:
                self.literals[i-self.num_literals].covariance_matrix_statistic_false = 0
            else:
                self.literals[i-self.num_literals].covariance_matrix_statistic_false = count_value[i][1]
