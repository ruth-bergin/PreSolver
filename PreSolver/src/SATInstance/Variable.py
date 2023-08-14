import numpy as np

CLAUSE_SUMMARY_STATS, CLAUSE_MIN_SIZE, CLAUSE_MAX_SIZE = "clause summary stats", "clause min size", "clause max size"
CLAUSE_MEDIAN_SIZE, CLAUSE_MEAN_SIZE, CLAUSE_STD_SIZE = "clause median size", "clause mean size", "clause std size"
COVARIANCE_MATRIX_STATISTIC = "covariance matrix statistic"
DLIS, RELATIVE_APPEARANCES, WEIGHTED_PURITY = "dlis", "relative_appearances", "weighted_purity"

class Variable:

    def dlis(self, assignment):
        if assignment:
            return self.num_affirmations
        else:
            return self.num_negations

    def relative_appearances(self, assignment):
        positive_purity = self.num_affirmations/self.appearances()
        if assignment:
            return positive_purity
        else:
            return 1-positive_purity

    def weighted_purity(self, assignment):
        return self.dlis(assignment) * self.relative_appearances(assignment)

    def __init__(self, index, metric):

        self.metrics = {
            DLIS: self.dlis,
            RELATIVE_APPEARANCES: self.relative_appearances,
            WEIGHTED_PURITY: self.weighted_purity
        }

        self.org_index = index
        self.index = index
        self.affirmations = []
        self.negations = []
        self.num_affirmations = 0
        self.num_negations = 0
        self.affirmation_statistics = {}
        self.negation_statistics = {}
        self.removed = False
        self.major_literal = False
        self.covariance_matrix_statistic_true = 0
        self.covariance_matrix_statistic_false = 0
        self.instance_num_clauses = 0
        self.reason_for_assignment = 0
        self.metric = self.metrics[metric.lower()]

    def get_heuristic(self, verbose=False):
        if self.pure():
            if verbose:
                print(f"Pure literal {self.major_literal}, returning number of appearances")
            return self.appearances()
        self.calculate_clause_summary_statistics()
        affirmation_metric = self.get_metric(True)
        negation_metric = self.get_metric(False)
        if affirmation_metric>negation_metric:
            self.set_major_literal(True)
        else:
            self.set_major_literal(False)
        return max([affirmation_metric, negation_metric])

    def set_major_literal(self, assignment):
        self.major_literal = assignment

    def get_metric(self, assignment):
        return self.metric(assignment)

    def get_clause_mean_size(self, affirmation):
        if affirmation:
            metrics = self.affirmation_statistics[CLAUSE_SUMMARY_STATS]
        else:
            metrics = self.negation_statistics[CLAUSE_SUMMARY_STATS]
        return metrics[CLAUSE_MEAN_SIZE]

    def get_clause_min_size(self, affirmation):
        if affirmation:
            metrics = self.affirmation_statistics[CLAUSE_SUMMARY_STATS]
        else:
            metrics = self.negation_statistics[CLAUSE_SUMMARY_STATS]
        return metrics[CLAUSE_MIN_SIZE]

    def calculate_clause_summary_statistics(self):
        self.affirmation_statistics[CLAUSE_SUMMARY_STATS], self.negation_statistics[CLAUSE_SUMMARY_STATS] = {}, {}
        self.get_clause_stats(True)
        self.get_clause_stats(False)

    def get_clause_stats(self, affirmation):
        clause_stats = self.negation_statistics[CLAUSE_SUMMARY_STATS]
        clauses = [clause.size for clause in self.negations]
        if affirmation:
            clause_stats = self.affirmation_statistics[CLAUSE_SUMMARY_STATS]
            clauses = [clause.size for clause in self.affirmations]
        if len(clauses)<1:
            clause_stats[CLAUSE_MIN_SIZE] = 0
            clause_stats[CLAUSE_MAX_SIZE] = 0
            clause_stats[CLAUSE_MEAN_SIZE] = 0
            clause_stats[CLAUSE_MEDIAN_SIZE] = 0
            clause_stats[CLAUSE_STD_SIZE] = 0
            return
        clause_stats[CLAUSE_MIN_SIZE] = min(clauses)
        clause_stats[CLAUSE_MAX_SIZE] = max(clauses)
        clause_stats[CLAUSE_MEAN_SIZE] = np.mean(clauses)
        clause_stats[CLAUSE_MEDIAN_SIZE] = np.median(clauses)
        clause_stats[CLAUSE_STD_SIZE] = np.std(clauses)

    def pure(self):
        if self.num_negations==0 or self.num_affirmations==0:
            if self.num_negations==0:
                self.set_major_literal(True)
            else:
                self.set_major_literal(False)
            return True
        return False

    def appearances(self):
        return self.num_negations + self.num_affirmations

    def purity(self):
        major_literal = max([self.num_negations, self.num_affirmations])
        return major_literal/self.appearances()

    def covariance(self):
        return max(self.covariance_matrix_statistic_false, self.covariance_matrix_statistic_true)

    def __gt__(self, other):
        #if self.pure() and not other.pure():
        #    return True
        #if (not self.pure()) and other.pure():
        #    return False
        diff = self.get_heuristic() - other.get_heuristic()
        if diff==0:
            return self.covariance() > other.covariance()
        return diff > 0

    def __lt__(self, other):
        #if (not self.pure()) and other.pure():
        #    return True
        #if self.pure() and not other.pure():
        #    return False
        diff = self.get_heuristic() - other.get_heuristic()
        if diff==0:
            return self.covariance() > other.covariance()
        return diff < 0

    def __str__(self):
        return "{} {} {}\n{}".format(
            self.index,
            self.num_affirmations,
            self.num_negations,
            " ".join([str(clause.index) for clause in self.affirmations+self.negations]))
