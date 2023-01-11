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

    def __gt__(self, other):
        return self.size>other.size

    def __lt__(self, other):
        return self.size<other.size

    def __str__(self):
        return "{} {}".format(self.index, " ".join([str((literal.index*sign)) for literal,sign in self.variables]))
