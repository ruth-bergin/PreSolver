class Clause:

    def __init__(self, index):
        self.index = index
        self.size = 0
        self.variables = []
        self.removed = False

    def remove_variable(self, instance, literal, sign):
        if self.size != len(self.variables):
            raise ValueError(f"Length not same as size for clause - l {len(self.variables)} s {self.size}")
        try:
            self.variables.remove((literal, sign))
        except Exception as e:
            raise ValueError(f"Attempted to remove variable {(literal.index, sign)} from list {str(self)}\n{e}\n"
                             f"Clause before:{str(instance.clauses[self.index-1])}\n"
                             f"CLause after:{str(instance.clauses[self.index+1])}")
        self.size -= 1
        if self.size==1:
            instance.unary_clauses += [self]

    def __gt__(self, other):
        return self.size>other.size

    def __lt__(self, other):
        return self.size<other.size

    def __str__(self):
        return "{}: {}".format(self.index, " ".join([str((literal.index*sign)) for literal,sign in self.variables]))
