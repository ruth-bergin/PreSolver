from random import randint

class Literal:

    def __init__(self, index):
        self.index = index
        self.affirmations = []
        self.negations = []
        self.num_affirmations = 0
        self.num_negations = 0
        self.removed = False

    def get_metric(self):
        return randint(0,100000)
        #return (self.num_negations+self.num_affirmations)**abs(self.num_affirmations/(self.num_negations+self.num_affirmations)-0.5)

    def __gt__(self, other):
        return self.get_metric() > other.get_metric()

    def __lt__(self, other):
        return self.get_metric() < other.get_metric()

    def __str__(self):
        return "{} {} {}\n{}".format(
            self.index,
            self.num_affirmations,
            self.num_negations,
            " ".join([str(clause.index) for clause in self.affirmations+self.negations]))