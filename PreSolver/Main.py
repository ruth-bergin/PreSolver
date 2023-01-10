from CNF import CNF
from VariableSelector import VariableSelector

basic = open("instances/basic.txt", "r")
cnf_string = basic.read()
basic.close()

print(CNF(cnf_string))
variable_selector = VariableSelector(cnf_string, cutoff=-1, verbose=True)

reduced_cnf = variable_selector.run()

print(reduced_cnf)
