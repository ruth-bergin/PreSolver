from VariableSelector import VariableSelector

print("Reading file")
filename = "../instances/CBS_k3_n100_m403_b10/CBS_k3_n100_m403_b10_0.cnf"
file = open(filename, "r")
cnf_string = file.read()
file.close()

print("Constructing selector.")
selector = VariableSelector(cnf_string, verbose=True)

print("Running selector.")
exit_code, cnf = selector.run()

print(cnf.solve())

print(exit_code)