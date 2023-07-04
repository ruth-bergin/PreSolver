
class Solution:

    def __init__(self, cnf_string, filename):
        self.assignments = []
        self.filename = filename
        self.cnf = None
        self.num_variables = int(cnf_string[:cnf_string.find("\n")].split(" ")[2])
        self.construct(cnf_string)

    def construct(self, cnf_string):
        clauses = [clause for clause in cnf_string[cnf_string.find("\n"):].split(" 0\n") if clause!=""]
        self.cnf = [[int(var) for var in clause.split(" ")] for clause in clauses]

    def add_assignment(self, variable, assignment):
        literal = self.get_var_as_int(variable, assignment)
        self.handle_clause_removal_and_reduction(literal)
        self.add_unit_clause(literal)

    def add_unit_clause(self, literal):
        self.assignments.append(literal)
        self.cnf = [[literal]] + self.cnf

        filename = f"{self.filename}_freqClauseCov_p{len(self.assignments)}_x{literal}.cnf"
        file = open(f"../instances/andrea/DatasetA/processed/{filename}", "w+")
        file.write(str(self))
        file.close()

    def handle_clause_removal_and_reduction(self, literal):
        i = len(self.cnf)
        while i >=0:
            i -= 1
            clause = self.cnf[i]
            if literal in clause:
                self.cnf.remove(clause)
            elif literal*-1 in clause and len(clause)>1:
                clause.remove(literal*-1)

    def get_var_as_int(self, variable, assignment):
        sign = -1
        if assignment:
            sign = 1
        return variable*sign

    def __str__(self):
        num_clauses = len(self.cnf)
        string = f"p cnf {self.num_variables} {num_clauses}\n"
        for clause in self.cnf:
            string += " ".join([str(var) for var in clause]) + " 0\n"
        return string