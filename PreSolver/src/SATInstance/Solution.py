
class Solution:

    def __init__(self, cnf_string, filename):
        self.assignments = []
        self.filename = filename
        if filename=="":
            self.save_to_file = False
        else:
            self.save_to_file = True
        self.cnf = None
        cnf_string = cnf_string[cnf_string.find("p cnf"):]
        self.num_variables = int(cnf_string[:cnf_string.find("\n")].split(" ")[2])
        self.construct(cnf_string)

    def construct(self, cnf_string):
        clauses = [clause for clause in cnf_string[cnf_string.find("\n"):].split(" 0\n") if clause!=""]
        self.cnf = [[int(var) for var in clause.split(" ") if var!=""] for clause in clauses if clause!=""]

    def add_assignment(self, variable, assignment, reason=0):
        if reason!=0:
            variable.reason_for_assignment=reason
        literal = self.get_var_as_int(variable, assignment)
        self.assignments.append((variable,assignment))
        self.handle_clause_removal_and_reduction(literal)
        self.add_unit_clause(literal, round(variable.reason_for_assignment))

    def add_unit_clause(self, literal, reason=0):
        self.cnf = [[literal]] + self.cnf

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
        return variable.org_index*sign

    def as_assignment(self, binary=True):
        assignment = sorted([self.get_var_as_int(v, a) for v,a in self.assignments], key=abs)
        if binary:
            return "".join(["1" if i>0 else "0" for i in assignment])
        return "".join([str(i) for i in assignment])

    def __str__(self):
        num_clauses = len(self.cnf)
        string = f"p cnf {self.num_variables} {num_clauses}\n"
        for clause in self.cnf:
            string += " ".join([str(var) for var in clause]) + " 0\n"
        return string