from random import randint
import numpy as np

CLAUSE_SUMMARY_STATS, CLAUSE_MIN_SIZE, CLAUSE_MAX_SIZE = "clause summary stats", "clause min size", "clause max size"
CLAUSE_MEDIAN_SIZE, CLAUSE_MEAN_SIZE, CLAUSE_STD_SIZE = "clause median size", "clause mean size", "clause std size"
COVARIANCE_MATRIX_STATISTIC = "covariance matrix statistic"

class Literal:

    def __init__(self, index):
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

    def get_heuristic(self, verbose=False):
        if self.pure():
            if verbose:
                print(f"Pure literal {self.major_literal}, returning number of appearances")
            return self.appearances()
        self.calculate_clause_summary_statistics()
        affirmation_metric = self.get_metric(True)*self.covariance_matrix_statistic_true
        negation_metric = self.get_metric(False)*self.covariance_matrix_statistic_false
        if affirmation_metric>negation_metric:
            self.set_major_literal(True)
            return affirmation_metric - negation_metric
        else:
            self.set_major_literal(False)
            return negation_metric - affirmation_metric

    def set_major_literal(self, assignment):
        self.major_literal = assignment

    def get_metric(self, assignment):
        if self.pure():
            if assignment:
                return self.num_affirmations
            else:
                return self.num_negations
        if assignment:
            return (self.num_affirmations)/(self.get_clause_mean_size(True)+self.get_clause_min_size(True))
        else:
            return (self.num_negations)/(self.get_clause_mean_size(False)+self.get_clause_min_size(False))

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

    def get_clause_median_size(self, affirmation):
        if affirmation:
            metrics = self.affirmation_statistics[CLAUSE_SUMMARY_STATS]
        else:
            metrics = self.negation_statistics[CLAUSE_SUMMARY_STATS]
        return metrics[CLAUSE_MEDIAN_SIZE]

    def calculate_clause_summary_statistics(self):
        self.affirmation_statistics[CLAUSE_SUMMARY_STATS], self.negation_statistics[CLAUSE_SUMMARY_STATS] = {}, {}
        if not self.pure():
            self.get_clause_stats(True)
            self.get_clause_stats(False)

    def get_clause_stats(self, affirmation):
        clause_stats = self.negation_statistics[CLAUSE_SUMMARY_STATS]
        clauses = [clause.size for clause in self.negations]
        if affirmation:
            clause_stats = self.affirmation_statistics[CLAUSE_SUMMARY_STATS]
            clauses = [clause.size for clause in self.affirmations]
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

    def __gt__(self, other):
        if self.pure() and not other.pure():
            return True
        elif other.pure() and self.pure():
            return self.num_affirmations+self.num_negations
        return self.get_heuristic() > other.get_heuristic()

    def __lt__(self, other):
        if (not self.pure()) and other.pure():
            return True
        return self.get_heuristic() < other.get_heuristic()

    def __str__(self):
        return "{} {} {}\n{}".format(
            self.index,
            self.num_affirmations,
            self.num_negations,
            " ".join([str(clause.index) for clause in self.affirmations+self.negations]))
