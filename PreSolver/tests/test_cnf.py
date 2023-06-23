import unittest
from src.SATInstance.CNF import CNF

file = open("instances/basic.cnf", "r")
CNF_STRING_BASIC = file.read()
LIST_OF_CLAUSES_BASIC = [[int(var) for var in clause.split(" ") if var != "0"]
                         for clause in CNF_STRING_BASIC.split("\n")[1:-1]]
file.close()

class SampleTestCase(unittest.TestCase):
    def test_construction(self):
        cnf = CNF(CNF_STRING_BASIC)

        self.assertEqual(CNF_STRING_BASIC, str(cnf))

    def test_getAsListOfClauses(self):
        cnf = CNF(CNF_STRING_BASIC)

        self.assertEqual(LIST_OF_CLAUSES_BASIC, cnf.get_as_list_of_clauses())

    def test_assignLiteralByInteger(self):
        file_org = open("instances/single_assignment.cnf", "r")
        cnf_str_org = file_org.read()
        file_org.close()
        cnf = CNF(cnf_str_org)
        file_red = open("instances/single_assignment_reduced.cnf", "r")
        cnf_str_red = file_red.read()
        file_red.close()

        cnf.assign_literal_by_integer(2)

        self.assertEqual(cnf_str_red, str(cnf))

    def test_propagateUnits(self):
        file_org = open("instances/basic.cnf", "r")
        cnf_str_org = file_org.read()
        file_org.close()
        cnf = CNF(cnf_str_org)
        file_red = open("instances/basic_assigned_twenty_true.cnf", "r")
        cnf_str_red = file_red.read()
        file_red.close()

        cnf.assign_literal_by_integer(20)

        self.assertEqual(cnf_str_red, str(cnf))

if __name__ == '__main__':
    unittest.main()
