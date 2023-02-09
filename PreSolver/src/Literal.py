from random import randint
import numpy as np
import math

CLAUSE_SUMMARY_STATS, CLAUSE_MIN_SIZE, CLAUSE_MAX_SIZE = "clause summary stats", "clause min size", "clause max size"
CLAUSE_MEDIAN_SIZE, CLAUSE_MEAN_SIZE, CLAUSE_STD_SIZE = "clause median size", "clause mean size", "clause std size"

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

    def get_heuristic(self):
        self.calculate_clause_summary_statistics()
        affirmation_metric = self.num_affirmations/self.get_metric(True)
        negation_metric = self.num_negations/self.get_metric(False)
        if affirmation_metric>negation_metric:
            return affirmation_metric/negation_metric
        else:
            return negation_metric/affirmation_metric

    def get_metric(self, affirmation):
        if affirmation:
            metrics = self.affirmation_statistics[CLAUSE_SUMMARY_STATS]
        else:
            metrics = self.negation_statistics[CLAUSE_SUMMARY_STATS]
        return metrics[CLAUSE_MEAN_SIZE]

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

    def __gt__(self, other):
        return self.get_heuristic() > other.get_heuristic()

    def __lt__(self, other):
        return self.get_heuristic() < other.get_heuristic()

    def __str__(self):
        return "{} {} {}\n{}".format(
            self.index,
            self.num_affirmations,
            self.num_negations,
            " ".join([str(clause.index) for clause in self.affirmations+self.negations]))
