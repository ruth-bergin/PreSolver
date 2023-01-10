class Clause:

    def __init__(self, instance, index):
        self.instance = instance
        self.index = index
        self.size = 0
        self.variables = []

    def remove_variable(self, literal, sign):
        self.variables.remove((literal, sign))
        self.size -= 1
        if self.size==1:
            self.instance.unary_clauses += [self]

    def __str__(self):
        return "{}\n{}".format(self.index, " ".join([str((literal.index*sign)) for literal,sign in self.variables]))
