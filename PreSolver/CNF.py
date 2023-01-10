from Clause import Clause
from Literal import Literal
import numpy as np


class CNF:

    def __init__(self, cnf_string, verbose=False):
        self.verbose = verbose
        self.num_clauses = 0
        self.num_literals = 0
        self.clauses = []
        self.literals = []
        self.unary_clauses = []
        self.construct(cnf_string)
        self.propagate_units()

    def construct(self, cnf_string):
        lines = cnf_string.strip("\n").split("\n")
        self.num_literals, self.num_clauses = int(lines[0].split()[-2]), int(lines[0].split()[-1])
        self.literals = [Literal(self, i) for i in range(1, self.num_literals + 1)]
        self.clauses = [Clause(i) for i in range(self.num_clauses)]
        print("~~~~~ {} ~~~~~".format(self.num_clauses==len(lines[1:])))
        if not self.num_clauses==len(lines[1:]):
            print(cnf_string)
            print(self.num_clauses, len(lines[1:]), lines[1], lines[-1])
        for index, variables in enumerate(lines[1:]):
            clause = self.clauses[index]
            variables = [(self.literals[abs(int(i))-1], np.sign(int(i))) for i in variables.split()][:-1]
            if len(variables)==1:
                self.unary_clauses += [clause]
            clause.variables += variables
            for literal, sign in variables:
                clause.size+=1
                if sign > 0:
                    literal.affirmations.append(clause)
                    literal.num_affirmations += 1
                else:
                    literal.negations.append(clause)
                    literal.num_negations += 1

    def assign_literal(self, literal, is_negation):
        if self.verbose:
            print("Assigning value {} to literal {}".format(not is_negation, literal.index))
        if is_negation:
            for clause in literal.affirmations:
                clause.remove_variable(self, literal, 1)
            while len(literal.negations) > 0:
                self.remove_clause(literal.negations[0])
        else:
            for clause in literal.negations:
                clause.remove_variable(self, literal, -1)
            while len(literal.affirmations) > 0:
                self.remove_clause(literal.affirmations[0])
        literal.index = None
        self.num_literals -= 1
        self.propagate_units()

    def assign_literal_by_integer(self, int):
        literal, is_negation = self.get_variable_from_integer(int)
        self.assign_literal(literal, is_negation)

    def propagate_units(self):
        while len(self.unary_clauses)>0:
            if self.verbose:
                print("{} unary clauses. Propagating.".format(len(self.unary_clauses)))
            literal, is_negation = self.unary_clauses[0].variables[0]
            if self.verbose:
                print("Removing unary clause {} with literal {} {}".format(self.unary_clauses[0].index, literal.index, not is_negation))
            self.unary_clauses = self.unary_clauses[1:]
            self.assign_literal(literal, is_negation)

    def remove_clause(self, clause):
        print("Removing clause {}".format(clause.index))
        self.num_clauses -= 1
        for literal, sign in clause.variables:
            if sign>0:
                if self.verbose:
                    print("Removing clause {} of size {} from literal {}".format(clause.index, clause.size, literal.index))
                literal.affirmations.remove(clause)
            else:
                if self.verbose:
                    print("Removing clause {} of size {} from literal {}".format(clause.index, clause.size, literal.index))
                literal.negations.remove(clause)
        clause.index = None

    def get_variable_from_integer(self, int):
        literal_index = abs(int)-1
        is_negation = int<0
        literal = self.literals[literal_index]
        return literal, is_negation

    def rearrange(self):
        self.clauses = [clause for clause in self.clauses if clause.index is not None]
        self.literals = [literal for literal in self.literals if literal.index is not None]
        for index, clause in enumerate(self.clauses):
            clause.index = index
        for index, literal in enumerate(self.literals):
            literal.index = index + 1

    def __str__(self):
        self.rearrange()
        string = "p cnf {} {}\n".format(self.num_literals, self.num_clauses)
        for clause in self.clauses:
            for literal, sign in clause.variables:
                try:
                    string += "{} ".format(literal.index*sign)
                except:
                    string += "error "
            string = string + "0\n"
        return string
