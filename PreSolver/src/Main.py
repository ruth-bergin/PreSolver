from VariableSelector import VariableSelector
from os import listdir

path = "../instances/andrea/DatasetA/"

solved = 0
sat = 0
assignments_to_failure = []
for index, filename in enumerate(listdir(path)):
    if filename=="processed":
        continue
    file = open(path+filename, "r")
    cnf_string = file.read()
    file.close()
    print(f"File {index}")

    file = open(path+"processed/"+filename[:-4]+"_freqClause_p0.cnf", "w")
    file.write(cnf_string)
    file.close()

    selector = VariableSelector(cnf_string, cutoff=0, use_dpll=False, dataset="cbs_base_50.txt",
                                fn=path+"processed/"+filename)

    selector.run(single_path=True)

    if selector.cnf.solved:
        solved += 1
    else:
        print(f"File {index} unsolved but still sat")
    if selector.cnf.solve():
        sat += 1
    print(selector.cnf.solve())
    assignments_to_failure.append(selector.assignments_to_failure)

print(f"SOLVED:\t{solved}\nSAT:\t{sat}")
print(assignments_to_failure)
