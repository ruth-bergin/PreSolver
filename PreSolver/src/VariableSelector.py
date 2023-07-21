from src.SATInstance.CNF import CNF
from src.SATInstance.Solution import Solution
from src.ml.RandomForest import SAT_RFC
from random import choice

VARIABLE, TRUE, FALSE, BRANCH_TRUE, BRANCH_FALSE = "variable", "true", "false", "branch_t", "branch_f"

class VariableSelector:

    def __init__(self, cnf_string, cutoff=0.6, verbose=False, sep=" 0\n", use_dpll=True,dataset="cbs_dpll_50.txt",
                 selection_complexity = "complete", fn=""):
        self.cnf = CNF(cnf_string, sep=sep, verbose=verbose)
        self.solution = Solution(str(self.cnf), fn)
        if use_dpll:
            self.fn = fn.replace("processed","assignment_confidence_dpll")
        else:
            self.fn = fn.replace("processed","assignment_confidence_base")
        self.cutoff = cutoff
        self.verbose = verbose
        self.assignments = 0
        self.p = 0
        self.assignments_to_failure = 0
        self.selection_complexity = selection_complexity
        if self.verbose:
            print("Training RFC.")
        self.rfc = SAT_RFC(dataset=dataset,dpll=use_dpll)
        if self.verbose:
            print("Model training complete.")
        self.solved = False
        self.dataset=dataset

    def run(self, to_failure=False, single_path=False):
        better_option_sat_probability = self.cutoff + 0.1
        first_pass = True
        branches_sat_probability, assignment = None, None
        i = 0
        nvars = self.cnf.num_variables
        last_known_sat = str(self.cnf)
        if self.verbose:
            print("Running first pass")
        branches_sat_diff=1
        while better_option_sat_probability > self.cutoff:
            if self.rfc.predict_sat(str(self.cnf)):
                last_known_sat = str(self.cnf)
            i += 1
            if self.verbose:
                print(f"CNF currently has {self.cnf.num_variables} literals "
                      f"and {self.cnf.num_clauses} clauses left.\n**ASSIGNMENT {i}**")
            if not first_pass:
                if self.verbose:
                    print("Sat probability of {} exceeds cutoff {}. Assigning variable"
                          .format(better_option_sat_probability, self.cutoff))
                self.cnf.assign_literal_by_integer(branches_sat_probability[VARIABLE].index*assignment)
                self.update_solution()
                file = open(self.fn,"a+")
                file.write(f"{self.assignments},{nvars-self.cnf.num_variables}"
                           f",{round(better_option_sat_probability,2)},{branches_sat_diff}"
                           f",{self.cnf.num_clauses/self.cnf.num_variables},{self.cnf.solve()}\n")
                file.close()
                if to_failure:
                    if not self.cnf.solve():
                        return 0, self.cnf
                self.assignments += 1
            else:
                first_pass = False
                file = open(self.fn,"w+")
                file.write("assignments,literals.assigned,sat.confidence,diff.sat.con,cv_ratio,sat"
                           f"\n0,{nvars},1,1,{self.cnf.num_clauses/self.cnf.num_variables},True\n")
                file.close()
            if not self.cnf.solve() and self.assignments_to_failure == 0:
                self.assignments_to_failure = self.assignments
            branches_sat_probability = self.branch_cnf()
            branches_sat_diff = round(abs(branches_sat_probability[TRUE]-branches_sat_probability[FALSE]),2)
            if self.solved:
                if self.verbose or True:
                    print("Solved.")
                variable = branches_sat_probability[VARIABLE]
                assignment = -1
                if variable.major_literal:
                    assignment = 1
                self.cnf.assign_literal_by_integer(variable.index*assignment)
                self.update_solution()
                for variable in self.cnf.variables+self.cnf.obsolete_variables:
                    variable.get_heuristic()
                    variable.post_solution=True
                    self.solution.add_assignment(variable, variable.major_literal, -5)
                return 0, self.cnf
            elif branches_sat_probability[TRUE]==0 and branches_sat_probability[FALSE]==0:
                if self.verbose:
                    print("Both branches unsat. Terminating.")
                self.update_solution()
                return 3, CNF(last_known_sat)
            if single_path: # or branches_sat_diff<0.15:
                variable = branches_sat_probability[VARIABLE]
                if variable.major_literal:
                    assignment=1
                    better_option_sat_probability = branches_sat_probability[TRUE]
                else:
                    assignment = -1
                    better_option_sat_probability = branches_sat_probability[FALSE]
            elif branches_sat_probability[TRUE] - branches_sat_probability[FALSE]>0:
                assignment = 1
                better_option_sat_probability = branches_sat_probability[TRUE]
            else:
                assignment = -1
                better_option_sat_probability = branches_sat_probability[FALSE]

        if self.verbose:
            print("Satisfiability of {} did not exceed cutoff of {}. "
                  "Terminating.".format(better_option_sat_probability, self.cutoff))
        self.update_solution()
        return 2, CNF(last_known_sat)

    def branch_cnf(self):
        self.cnf.update_covariance_matrix()
        self.cnf.update_covariance_matrix_statistics()
        next_variable = self.select_next_variable()
        if self.verbose:
            print("Branching CNF on {} - {}".format(next_variable.index, next_variable.major_literal))
        branch_true = self.create_branch(next_variable.index, 1)
        branch_false = self.create_branch(next_variable.index, -1)

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
            self.solved = True
            if self.verbose:
                print(f"Ending shadow branch for variable {variable} assignment {assignment>0} - solved")
            return self.cnf
        else:
            if self.verbose:
                print(f"Ending shadow branch for variable {variable} assignment {assignment>0} - reduced")
            return shadow_cnf

    def get_sat_probability(self, cnf_branch_true, cnf_branch_false):
        return self.rfc.predict_shadow_cnfs(cnf_branch_true, cnf_branch_false)

    def select_next_variable(self):
        return max(self.cnf.variables)

    def update_solution(self):
        new_assignments = self.cnf.assignments
        for variable, assignment in new_assignments:
            if (variable,assignment) in self.solution.assignments:
                continue
            self.solution.add_assignment(variable, assignment)
