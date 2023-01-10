from CNF import CNF

VARIABLE, TRUE, FALSE = "variable", "true", "false"


class VariableSelector:

    # pick the variable with best metric
    # assign it positive and negative
    # choose the one with the highest improvement in SAT-probability
    # if the improvement isn't greater than cutoff, terminate
    # how to terminate? one large function.

    def __init__(self, cnf_string, cutoff=0.05, verbose=False):
        self.cnf = CNF(cnf_string, verbose=verbose)
        self.cutoff = cutoff
        self.verbose = verbose

    def run(self):
        improvement = self.cutoff + 0.1
        first_pass = True
        cv_ratio, is_negation = None, None
        if self.verbose:
            print("Running first pass")
        while improvement > self.cutoff and self.cnf.num_clauses>1:
            if self.verbose:
                print("CNF currently has {} literals and {} clauses left.".format(self.cnf.num_literals, self.cnf.num_clauses))
            if not first_pass:
                if self.verbose:
                    print("Improvement of {} exceeds cutoff {}. Assigning {} to variable {}"
                          .format(improvement, self.cutoff, is_negation, cv_ratio[VARIABLE].index))
                self.cnf.assign_literal(cv_ratio[VARIABLE], is_negation)
            else:
                first_pass = False
            if self.cnf.num_clauses < 10:
                print(self.cnf)
            cv_ratio = self.branch_cnf()
            if self.verbose:
                print("Current CV ratio: {}".format(self.get_sat_probability(self.cnf)))
            if cv_ratio[TRUE] < cv_ratio[FALSE]:
                if self.verbose:
                    print("CV ratio of {} for True assignment is chosen instead of false value {}".format(cv_ratio[TRUE], cv_ratio[FALSE]))
                is_negation = False
                improvement = self.get_sat_probability(self.cnf) - cv_ratio[TRUE]
            else:
                if self.verbose:
                    print("CV ratio of {} for False assignment is chosen instead of true value {}".format(cv_ratio[FALSE], cv_ratio[TRUE]))
                is_negation = True
                improvement = self.get_sat_probability(self.cnf) - cv_ratio[FALSE]
        if self.cnf.num_clauses == 1:
            if self.verbose:
                print("Solved.")
                print(str(self.cnf))
        elif self.verbose:
            print("Improvement of {} did not exceed cutoff of {}. Terminating.".format(improvement, self.cutoff))
        return self.cnf

    def branch_cnf(self):
        self.cnf.rearrange()
        cnf_branch_true = CNF(str(self.cnf))
        cnf_branch_false = CNF(str(self.cnf))
        next_variable = self.select_next_variable()

        if self.verbose:
            print("Branching CNF on {}".format(next_variable.index))
        cnf_branch_true.assign_literal_by_integer(next_variable.index)
        cnf_branch_true.rearrange()
        cnf_branch_false.assign_literal_by_integer(next_variable.index*-1)
        cnf_branch_false.rearrange()

        return {VARIABLE: next_variable,
                TRUE:  self.get_sat_probability(cnf_branch_true),
                FALSE: self.get_sat_probability(cnf_branch_false)}

    def get_sat_probability(self, cnf):
        return cnf.num_clauses/cnf.num_literals

    def select_next_variable(self):
        return max(self.cnf.literals)
