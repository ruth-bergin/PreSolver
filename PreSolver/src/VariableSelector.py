from src.SATInstance.CNF import CNF
from RandomForest import SAT_RFC

VARIABLE, TRUE, FALSE, BRANCH_TRUE, BRANCH_FALSE = "variable", "true", "false", "branch_t", "branch_f"


class VariableSelector:

    def __init__(self, cnf_string, cutoff=0.6, verbose=False, sep=" 0\n"):
        self.cnf = CNF(cnf_string, sep=sep)
        self.cutoff = cutoff
        self.verbose = verbose
        self.assignments = 0
        self.assignments_to_failure = 0
        if self.verbose:
            print("Training RFC.")
        self.rfc = SAT_RFC()
        if self.verbose:
            print("Model training complete.")
        self.solved = False

    def run(self):
        better_option_sat_probability = self.cutoff + 0.1
        first_pass = True
        branches_sat_probability, chosen_branch = None, None
        i = 0
        if self.verbose:
            print("Running first pass")
        while better_option_sat_probability > self.cutoff and not self.solved:
            i += 1
            if self.verbose:
                print(f"CNF currently has {self.cnf.num_literals} literals and {self.cnf.num_clauses} clauses left.\n**ASSIGNMENT {i}**")
            if not first_pass:
                if self.verbose:
                    print("Sat probability of {} exceeds cutoff {}. Assigning variable"
                          .format(better_option_sat_probability, self.cutoff))
                self.cnf = chosen_branch
                self.assignments += 1
            else:
                first_pass = False
            if not self.cnf.solve() and self.assignments_to_failure == 0:
                self.assignments_to_failure = self.assignments
            branches_sat_probability = self.branch_cnf()
            if self.solved:
                if self.verbose:
                    print("Solved.")
                return 0, self.cnf
            elif branches_sat_probability[TRUE]==0 and branches_sat_probability[FALSE]==0:
                if self.verbose:
                    print("Both branches unsat. Terminating.")
                return 3, self.cnf
            elif branches_sat_probability[TRUE] > branches_sat_probability[FALSE]:
                if self.verbose:
                    print("SAT probability of {} for True assignment is chosen instead of false value {}"
                          .format(branches_sat_probability[TRUE], branches_sat_probability[FALSE]))
                chosen_branch = branches_sat_probability[BRANCH_TRUE]
                better_option_sat_probability = branches_sat_probability[TRUE]
            else:
                if self.verbose:
                    print("SAT probability of {} for False assignment is chosen instead of true value {}"
                          .format(branches_sat_probability[FALSE], branches_sat_probability[TRUE]))
                chosen_branch = branches_sat_probability[BRANCH_FALSE]
                better_option_sat_probability = branches_sat_probability[FALSE]
        if self.verbose:
            print("Satisfiability of {} did not exceed cutoff of {}. Terminating.".format(better_option_sat_probability, self.cutoff))
        return 2, self.cnf

    def branch_cnf(self):
        self.cnf.update_covariance_matrix()
        next_variable = self.select_next_variable()
        if self.verbose:
            print("Branching CNF on {}".format(next_variable.index))
        branch_true = self.create_branch(next_variable.index, 1)
        if self.solved:
            return
        branch_false = self.create_branch(next_variable.index, -1)
        if self.solved:
            return

        sat_probability = self.get_sat_probability(str(branch_true), str(branch_false))
        for branch, assignment in [(branch_true, TRUE), (branch_false, FALSE)]:
            if branch==self.cnf:
                sat_probability[assignment] = 0
        sat_probability[VARIABLE] = next_variable
        sat_probability[BRANCH_TRUE] = branch_true
        sat_probability[BRANCH_FALSE] = branch_false
        return sat_probability

    def create_branch(self, variable, assignment):
        if self.verbose:
            print(f"Beginning shadow branch for variable {variable} assignment {assignment>0}")
        shadow_cnf = CNF(str(self.cnf))
        success = shadow_cnf.assign_literal_by_integer(variable*assignment)
        if success<0:
            if self.verbose:
                print(f"Ending shadow branch for variable {variable} assignment {assignment>0} - non-viable")
            return self.cnf
        if shadow_cnf.num_clauses<2:
            self.cnf = shadow_cnf
            self.solved = True
            if self.verbose:
                print(f"Ending shadow branch for variable {variable} assignment {assignment>0} - solved")
            return self.cnf
        else:
            if self.verbose:
                print(f"Ending shadow branch for variable {variable} assignment {assignment>0} - reduced")
            return shadow_cnf

    def get_sat_probability(self, cnf_branch_true, cnf_branch_false):
        return self.rfc.predict_cnf(cnf_branch_true, cnf_branch_false)

    def select_next_variable(self):
        return max(self.cnf.literals)
