from CNF import CNF
from VariableSelector import VariableSelector

"""
basic = open("instances/basic.txt", "r")
cnf_string = basic.read()
basic.close()

print(CNF(cnf_string))
variable_selector_basic = VariableSelector(cnf_string, cutoff=-1, verbose=False)

reduced_cnf = variable_selector_basic.run()

print(reduced_cnf)"""

example_zero = open("instances/CBS_k3_n100_m403_b10/CBS_k3_n100_m403_b10_0.cnf", "r")
cnf_string_zero = example_zero.read()
example_zero.close()

variable_selector_zero = VariableSelector(cnf_string_zero, cutoff= -1, verbose=True)
reduced_cnf_zero = variable_selector_zero.run()
