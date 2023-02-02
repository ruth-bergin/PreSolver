from src.CNF import CNF

VARIABLE, TRUE, FALSE = "variable", "true", "false"


class VariableSelector:

    def __init__(self, cnf_string, cutoff=0.05, verbose=False):
        self.cnf = CNF(cnf_string, verbose=verbose)
        self.cutoff = cutoff
        self.verbose = verbose
        self.solved = False

    def run(self):
        improvement = self.cutoff + 0.1
        first_pass = True
        cv_ratio, is_negation = None, None
        if self.verbose:
            print("Running first pass")
        while improvement > self.cutoff and not self.solved:
            if self.verbose:
                print("CNF currently has {} literals and {} clauses left.".format(self.cnf.num_literals, self.cnf.num_clauses))
            if not first_pass:
                if self.verbose:
                    print("Improvement of {} exceeds cutoff {}. Assigning {} to variable {}"
                          .format(improvement, self.cutoff, not is_negation, cv_ratio[VARIABLE].index))
                self.cnf.assign_literal(cv_ratio[VARIABLE], is_negation)
            else:
                first_pass = False
            cv_ratio = self.branch_cnf()
            if self.solved:
                if self.verbose:
                    print("Solved.")
                return 0, self.cnf
            elif cv_ratio[TRUE]==0 and cv_ratio[FALSE]==0:
                return 1, self.cnf
            elif cv_ratio[TRUE] < cv_ratio[FALSE]:
                if self.verbose:
                    print("CV ratio of {} for True assignment is chosen instead of false value {}, with current ratio {}"
                          .format(cv_ratio[TRUE], cv_ratio[FALSE], self.get_sat_probability(self.cnf)))
                is_negation = False
                improvement = cv_ratio[TRUE] - self.get_sat_probability(self.cnf)
            else:
                if self.verbose:
                    print("CV ratio of {} for False assignment is chosen instead of true value {}, with current ratio {}"
                          .format(cv_ratio[FALSE], cv_ratio[TRUE], self.get_sat_probability(self.cnf)))
                is_negation = True
                improvement = cv_ratio[FALSE] - self.get_sat_probability(self.cnf)
        if self.verbose:
            print("Improvement of {} did not exceed cutoff of {}. Terminating.".format(improvement, self.cutoff))
        return 2, self.cnf

    def branch_cnf(self):
        self.cnf.rearrange()
        next_variable = self.select_next_variable()
        if self.verbose:
            print("Branching CNF on {}".format(next_variable.index))
        branch_true = self.create_branch(next_variable.index, 1)
        if self.solved:
            return
        branch_false = self.create_branch(next_variable.index, -1)
        if self.solved:
            return

        return {VARIABLE: next_variable,
                TRUE: branch_true,
                FALSE: branch_false}

    def create_branch(self, variable, assignment):
        if self.verbose:
            print(f"Beginning shadow branch for variable {variable} assignment {assignment>0}")
        shadow_cnf = CNF(str(self.cnf), verbose=self.verbose)
        success = shadow_cnf.assign_literal_by_integer(variable*assignment)
        if success<0:
            if self.verbose:
                print(f"Ending shadow branch for variable {variable} assignment {assignment>0} - non-viable")
            return 0
        shadow_cnf.rearrange()
        if shadow_cnf.num_clauses<2:
            self.cnf = shadow_cnf
            self.cnf.rearrange()
            self.solved = True
            if self.verbose:
                print(f"Ending shadow branch for variable {variable} assignment {assignment>0} - solved")
            return 1
        else:
            if self.verbose:
                print(f"Ending shadow branch for variable {variable} assignment {assignment>0} - reduced")
            return self.get_sat_probability(shadow_cnf)

    def get_sat_probability(self, cnf):
        return (4.2-(cnf.num_clauses/cnf.num_literals))/4.2

    def select_next_variable(self):
        return max(self.cnf.literals)