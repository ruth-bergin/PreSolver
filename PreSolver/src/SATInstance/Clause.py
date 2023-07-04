class Clause:

    def __init__(self, index):
        self.index = index
        self.size = 0
        self.literals = []
        self.removed = False

    def remove_variable(self, instance, variable, sign):
        if self.size != len(self.literals):
            raise ValueError(f"Length not same as size for clause - l {len(self.literals)} s {self.size}")
        try:
            self.literals.remove((variable, sign))
        except Exception as e:
            raise ValueError(f"Attempted to remove variable {(variable.index, sign)} from list {str(self)}\n{e}\n"
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
        return "{}: {}".format(self.index, " ".join([str((literal.index*sign)) for literal,sign in self.literals]))
