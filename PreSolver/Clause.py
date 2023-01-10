class Clause:

    def __init__(self, index):
        self.index = index
        self.size = 0
        self.variables = []

    def remove_variable(self, instance, literal, sign):
        self.variables.remove((literal, sign))
        self.size -= 1
        if self.size==1:
            instance.unary_clauses += [self]
        if self.size==0:
            instance.remove_clause(self)
            if self in instance.unary_clauses:
                instance.unary_clauses.remove(self)

    def __str__(self):
        return "{}\n{}".format(self.index, " ".join([str((literal.index*sign)) for literal,sign in self.variables]))
