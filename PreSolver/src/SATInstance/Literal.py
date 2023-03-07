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
        self.covariance_matrix_affirmation_row = []
        self.covariance_matrix_negation_row = []
        self.removed = False

    def get_heuristic(self):
        if self.pure():
            return self.appearances()
        self.calculate_clause_summary_statistics()
        affirmation_metric = self.num_affirmations/self.get_clause_mean_size(True)
        negation_metric = self.num_negations/self.get_clause_mean_size(False)
        if affirmation_metric>negation_metric:
            return affirmation_metric/negation_metric
        else:
            return negation_metric/affirmation_metric

    def get_clause_mean_size(self, affirmation):
        if affirmation:
            metrics = self.affirmation_statistics[CLAUSE_SUMMARY_STATS]
        else:
            metrics = self.negation_statistics[CLAUSE_SUMMARY_STATS]
        return metrics[CLAUSE_MEAN_SIZE]

    def calculate_covariance_matrix_statistics(self):
        nonzero_covariance_affirmation = list(filter(lambda x: (x > 0), self.covariance_matrix_affirmation_row))
        if len(nonzero_covariance_affirmation) > 0:
            self.affirmation_statistics[COVARIANCE_MATRIX_STATISTIC] = \
                np.mean(nonzero_covariance_affirmation)
        else:
            self.affirmation_statistics[COVARIANCE_MATRIX_STATISTIC] = 0
        nonzero_covariance_negation = list(filter(lambda x: (x > 0), self.covariance_matrix_negation_row))
        if len(nonzero_covariance_negation) > 0:
            self.negation_statistics[COVARIANCE_MATRIX_STATISTIC] = \
                np.mean(nonzero_covariance_negation)
        else:
            self.negation_statistics[COVARIANCE_MATRIX_STATISTIC] = 0


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
        clause_stats[CLAUSE_MIN_SIZE] = min(clauses)
        clause_stats[CLAUSE_MAX_SIZE] = max(clauses)
        clause_stats[CLAUSE_MEAN_SIZE] = np.mean(clauses)
        clause_stats[CLAUSE_MEDIAN_SIZE] = np.median(clauses)
        clause_stats[CLAUSE_STD_SIZE] = np.std(clauses)

    def pure(self):
        if self.num_negations==0 or self.num_affirmations==0:
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
