from pysat.solvers import Solver

from src.SATInstance.Clause import Clause
from src.SATInstance.Variable import Variable
import numpy as np


class CNF:

    def __init__(self, cnf_string, sep=" 0\n", verbose=False):
        self.solved = False
        self.verbose = verbose
        self.num_clauses = 0
        self.num_variables = 0
        self.clauses = []
        self.variables = []
        self.unary_clauses = []
        self.obsolete_variables = []
        self.assignments = []
        self.temp_assignments = []
        self.construct(cnf_string, sep)
        self.update_covariance_matrix()
        self.update_covariance_matrix_statistics()
        if self.verbose:
            print("Solving")
        self.sat = self.solve()
        if self.verbose:
            print(f"Propagating from __init__() with unary clauses {[clause.index for clause in self.unary_clauses]}")
        self.propagate_units()
        for literal in self.variables:
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
                print([line for line in line1.split("  0 \n ")])
                raise e
            lines = [line for line in [first_clause] + rest_of_text if line != ""]
        else:
            description, lines = line1, rest_of_text
        self.num_variables, self.num_clauses = int(description.split()[-2]), int(description.split()[-1])
        self.variables = [Variable(i) for i in range(1, self.num_variables + 1)]
        self.clauses = [Clause(i) for i in range(self.num_clauses)]
        for index, variables in enumerate(lines):
            if index >= self.num_clauses:
                print(variables)
                raise ValueError(f"Number of clauses {self.num_clauses} and number of lines {len(lines)} do not match.")
            clause = self.clauses[index]
            for i in variables.split():
                if np.sign(int(i)) == 0:
                    raise ValueError(f"Sign for value {i} in clause {index} is 0\nVariables:\n{variables}")
            variables = [variable.strip("\n") for variable in variables.split(" ") if variable!=""]
            try:
                variables = [(self.variables[abs(int(i)) - 1], np.sign(int(i))) for i in variables]
            except Exception as e:
                print(self.num_variables, len(variables), "\n", variables)
                raise e
            if len(variables) == 1:
                self.unary_clauses += [clause]
            clause.literals += variables
            for variable, sign in variables:
                clause.size += 1
                if sign > 0:
                    variable.affirmations.append(clause)
                    variable.num_affirmations += 1
                else:
                    variable.negations.append(clause)
                    variable.num_negations += 1

    @staticmethod
    def get_sign_from_bool(boolean):
        if boolean:
            return 1
        return -1

    def solve(self):
        s = Solver(name='g4')
        for clause in self.get_as_list_of_clauses():
            s.add_clause(clause)
        return s.solve()

    def get_as_list_of_clauses(self):
        return [[int(variable.index * sign) for variable, sign in clause.literals] for clause in self.clauses]

    def assign_variable(self, variable, assignment, reason):
        variable.reason_for_assignment = reason
        if (variable, self.get_sign_from_bool(not assignment)) in [clause.literals[0] for clause in self.unary_clauses]:
            if self.verbose:
                print("Contradictory unit clauses. Aborting.")
            return -1
        if variable.removed:
            raise ValueError(f"Attempting to assign {variable.index} when it has already been assigned.")
        if self.solved:
            return
        if self.verbose:
            print("Assigning value {} to literal {}".format(assignment, variable.index))
        success = self.handle_clause_removal_and_reduction(variable, assignment)
        if success != 0:
            return -1
        self.temp_assignments.append((variable, assignment))
        variable.removed = True
        self.num_variables -= 1
        return 0

    def handle_clause_removal_and_reduction(self, variable, assignment):
        satisfied_clauses, unsatisfied_clauses = variable.negations, variable.affirmations
        if assignment:
            satisfied_clauses, unsatisfied_clauses = variable.affirmations, variable.negations
        if self.verbose:
            print(
                f"Assigned literal {variable.index} so removing clauses {[str(clause) for clause in satisfied_clauses]}")
        if len(satisfied_clauses)==0 and self.verbose:
            print(f"No clauses satisfied. Clauses unsatisfied: {[str(clause) for clause in unsatisfied_clauses]}")
        while len(satisfied_clauses)>0:
            clause = satisfied_clauses[-1]
            if clause.removed:
                raise ValueError(f"Clause {clause} has been removed.")
            if (variable, self.get_sign_from_bool(assignment)) not in clause.literals:
                raise ValueError(
                    f"Infeasible assignment - literal {variable.index} not in clause {clause} so cannot satisfy it.\n"
                    f"Check for other clauses: {[(variable, self.get_sign_from_bool(assignment)) in clause.literals for clause in satisfied_clauses]}")
            self.remove_clause(clause)
        if self.verbose:
            print(
                f"Assigned literal {variable.index} so reducing clauses {[str(clause) for clause in unsatisfied_clauses]}")
        for clause in unsatisfied_clauses:
            if clause.removed:
                raise ValueError(f"Clause has {clause} been removed.")
            if (variable, self.get_sign_from_bool(not assignment)) not in clause.literals:
                raise ValueError(
                    f"Infeasible assignment - literal {variable.index} is not present in clause {clause} to be removed.\n"
                    f"Previous clause: {self.clauses[clause.index - 1]}\n"
                    f"Next clause: {self.clauses[clause.index + 1]}")
            if clause in self.unary_clauses:
                return -1
            clause.remove_variable(self, variable, self.get_sign_from_bool(not assignment))
        return 0

    def remove_clause(self, clause):
        clause.removed = True
        for variable, assignment in clause.literals:
            if assignment>0:
                if variable.affirmations.count(clause)>1:
                    raise ValueError(f"Count for clause {clause} in variable {variable.index} is {variable.affirmations.count(clause)}")
                variable.affirmations.remove(clause)
                variable.num_affirmations -= 1
            else:
                if variable.negations.count(clause)>1:
                    raise ValueError(f"Count for clause {clause} in variable {variable.index} is {variable.negations.count(clause)}")
                variable.negations.remove(clause)
                variable.num_negations -= 1
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
                variable, assignment = clause.literals[0][0], clause.literals[0][1] > 0
                if not variable.removed:
                    success = self.assign_variable(variable, assignment, -2)
                    if success != 0:
                        if self.verbose:
                            print("Failed to assign unit clause. Aborting.")
                        return -1
                elif self.verbose:
                    raise ValueError(f"Clause {clause} has not been removed already, but its literal {variable.index} has")
            elif self.verbose:
                print(f"Clause {clause} has been removed already, skipping")
            self.unary_clauses.remove(clause)
        return 0

    def assign_literal_by_integer(self, integer, reason=0):
        if integer == 0:
            raise ValueError("Something is wrong")
        variable, assignment = self.get_literal_from_integer(integer)
        if reason!=0:
            success = self.assign_variable(variable, assignment, reason)
        elif variable.pure():
            success = self.assign_variable(variable, assignment, -3)
        else:
            success = self.assign_variable(variable, assignment, variable.get_heuristic())
        if success < 0:
            self.temp_assignments = []
            return success
        success = self.rearrange()
        if self.verbose:
            print(f"Completed run of assignment of {integer} with success {success}")
            print(f"Satisfiability: {self.solve()}")
        self.check_for_literal_clause_inconsistency()
        self.check_for_sat_violation()
        if not self.solved:
            self.update_covariance_matrix()
            self.update_covariance_matrix_statistics()
        self.assignments += self.temp_assignments
        self.temp_assignments = []
        return success

    def check_for_literal_clause_inconsistency(self):
        variables_still_contain_clauses, clauses_still_contain_literals = 0, 0
        unique_variables, unique_clauses = 0,0
        clauses, variables = {}, {}
        for variable in self.variables:
            unique = True
            for clause in variable.affirmations:
                if (variable, 1) not in clause.literals:
                    variables_still_contain_clauses += 1
                    if unique:
                        unique = False
                        unique_variables += 1
                    variables[str(variable.index)] = f"{variables.get(str(variable.index), str())} {str(clause)}\n"
            for clause in variable.negations:
                if (variable, -1) not in clause.literals:
                    variables_still_contain_clauses += 1
                    if unique:
                        unique = False
                        unique_variables += 1
                    variables[str(variable.index)] = f"{variables.get(str(variable.index), str())} {str(clause)}\n"
        for clause in self.clauses:
            unique = True
            for variable, sign in clause.literals:
                if sign>0:
                    if clause not in variable.affirmations:
                        clauses_still_contain_literals += 1
                        if unique:
                            unique = False
                            unique_clauses += 1
                        clauses[str(clause.index)] = f"{clauses.get(str(clause.index), str())} {str(variable)}\n"
                elif clause not in variable.negations:
                    clauses_still_contain_literals += 1
                    if unique:
                        unique = False
                        unique_clauses += 1
                    clauses[str(clause.index)] = f"{clauses.get(str(clause.index), str())} {str(variable)}\n"
        if variables_still_contain_clauses + clauses_still_contain_literals>0:
            raise ValueError(f"Inconsistency with clause and literal lists.\n"
                             f"{unique_clauses} unique clauses mention a total of {clauses_still_contain_literals} literals which don't mention them.\n"
                             f"{[(clause, clauses[clause]) for clause in clauses.keys()]}\n"
                             f"{unique_variables} unique literals mention a total of {variables_still_contain_clauses} clauses which don't contain them.\n"
                             f"{variables}")


    def get_literal_from_integer(self, integer):
        variable_index, assignment = abs(integer) - 1, integer > 0
        try:
            variable = self.variables[variable_index]
        except Exception as e:
            print(
                f"{e}: attempting to access index {variable_index} with list length {len(self.variables)} and num literals {self.num_variables}")
            raise e
        return variable, assignment

    def rearrange(self):
        if self.solved or (self.num_variables == len(self.variables) and self.num_clauses == len(self.clauses)):
            if self.handle_obsolete_variables():
                return self.rearrange()
            return 0
        self.clauses = [clause for clause in self.clauses if not clause.removed and clause.size > 0]
        for variable in self.variables:
            variable.affirmations = [clause for clause in variable.affirmations if not clause.removed]
            variable.negations = [clause for clause in variable.negations if not clause.removed]
            variable.num_affirmations, variable.num_negations = len(variable.affirmations), len(variable.negations)
        self.handle_obsolete_variables()
        for index, clause in enumerate(self.clauses):
            clause.index = index
        for index, variable in enumerate(self.variables):
            variable.index = index + 1
        self.num_variables = len(self.variables)
        self.num_clauses = len(self.clauses)
        if self.num_clauses < 2:
            self.solved = True
            return 0
        self.unary_clauses = [clause for clause in self.clauses if len(clause.literals) == 1]
        if self.variables[-1].index!=self.num_variables:
            raise ValueError(f"Largest index {self.variables[-1].index} with {self.num_variables} literals counted.")
        if self.verbose:
            print("Propagating from rearrange()")
        success = self.propagate_units()
        if success == 0:
            if self.verbose:
                print("Propagating from rearrange() at depth")
            return self.rearrange()
        elif success < 0:
            return -1
        for variable in self.variables:
            variable.instance_num_clauses = self.num_clauses
        for variable in self.variables:
            if len(variable.affirmations)+len(variable.negations)==0:
                raise ValueError("Problem in rearrange")
        return 0

    def handle_obsolete_variables(self):
        new_obsolete_variables = [variable for variable in self.variables
                                  if (not variable.removed) and variable.appearances()==0
                                  and variable not in self.obsolete_variables]
        self.obsolete_variables += new_obsolete_variables
        self.variables = [variable for variable in self.variables if not variable.removed and variable.appearances()>0]
        return len(new_obsolete_variables)>0

    def check_for_sat_violation(self):
        if not self.sat and self.solve():
            raise ValueError("Unsat problem made sat through assignment.")

    def __str__(self):
        self.rearrange()
        #if len(self.unary_clauses)>0 and not self.solved:
        #    print(f"There shouldn't be unit clauses.\n{[str(clause) for clause in self.unary_clauses]}")
        if self.solved:
            return ""
        string = "p cnf {} {}\n".format(self.num_variables, self.num_clauses)
        for clause in self.clauses:
            for variable, sign in clause.literals:
                if sign == 0:
                    raise ValueError("Sign is somehow zero???")
                elif variable.index == 0:
                    raise ValueError("Literal index is 0 despite check otherwise")
                try:
                    string += "{} ".format(variable.index * sign)
                except:
                    string += "error "
            string = string + "0\n"
        return string

    def update_covariance_matrix(self):
        # Initialise square matrix of size number of literals, all 0.
        self.covariance_matrix = [[0 for i in range(self.num_variables * 2)] for j in range(self.num_variables * 2)]
        for clause in self.clauses:
            # For each clause, compare each variable to each other
            for variable, assignment in clause.literals:
                for other_variable, other_assignment in clause.literals:
                    # Make each variable skip over itself
                    if variable==other_variable:
                        continue
                    # Off-by-one indexing
                    index, other_index = variable.index - 1, other_variable.index - 1
                    # if literal is negative go to second half of covariance matrix
                    if assignment==-1:
                        index += self.num_variables
                    if other_assignment == -1:
                        other_index += self.num_variables
                    # These literals share a clause
                    self.covariance_matrix[index][other_index] += 1

    def update_covariance_matrix_statistics(self):
        for variable in self.variables:
            variable.calculate_clause_summary_statistics()
        # number of covariant literals and the sum of their negated values for each literal
        count_value = [[0,0] for i in range(self.num_variables * 2)]
        metrics = []
        i= 0
        # for every literal
        while i < self.num_variables*2:
            j = 0
            # get the total number of covariant literals
            total_children = sum(self.covariance_matrix[i])
            # if it doesn't share with anybody it doesn't matter
            if total_children == 0:
                metric = 0
            # For the positive literals - get the negated literal metric
            elif i < self.num_variables:
                metric = self.variables[i].get_metric(False)
                # divide amongst potential satisfiers
                metric = metric/total_children
            # For the negative literals - get the negated (positive) literal metric
            else:
                # back to variables instead of literals
                metric = self.variables[i - self.num_variables].get_metric(True)
                metric = metric/total_children
            # Weight the metric by the number of clauses shared
            while j < self.num_variables*2:
                # Skip literals with no common clauses
                if self.covariance_matrix[i][j]==0:
                    j+=1
                    continue
                # Increase the count of covariant literals by one
                count_value[j][0] += 1
                # Increment the weight of the covariance of the literal
                count_value[j][1] += metric * self.covariance_matrix[i][j]
                j += 1
            metrics.append(metric)
            i += 1
        # we don't want this to be 0
        min_value = min([i[1] for i in count_value if i!=0])*0.9
        for i in range(self.num_variables):
            # if the literal doesn't have covariance it doesn't matter
            if count_value[i][0]==0:
                self.variables[i].covariance_matrix_statistics_true = min_value
            else:
                self.variables[i].covariance_matrix_statistic_true = count_value[i][1]
        for i in range(self.num_variables, 2 * self.num_variables):
            if count_value[i][0]==0:
                self.variables[i - self.num_variables].covariance_matrix_statistic_false = min_value
            else:
                self.variables[i - self.num_variables].covariance_matrix_statistic_false = count_value[i][1]
