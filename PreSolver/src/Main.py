from VariableSelector import VariableSelector
from os import listdir

path = "../instances/andrea/DatasetB/"

solved = 0
sat = 0
assignments_to_failure = []
for index, filename in enumerate(listdir(path)):
    if filename[-4:]!=".cnf":
        continue
    file = open(path+filename, "r")
    cnf_string = file.read()
    file.close()
    print(f"File {index}")

    file = open(path+"processed/"+filename[:-4]+"_dlisObsoleteVarsReserved_p0.cnf", "w")
    file.write(cnf_string)
    file.close()

    try:
        selector = VariableSelector(cnf_string, cutoff=-1, use_dpll=False, dataset="cbs_base_50.txt",
                                    fn=path+"processed/"+filename, verbose=False)
    except:
        selector = VariableSelector(cnf_string, cutoff=-1, sep="0 \n", use_dpll=False, dataset="cbs_base_50.txt",
                                    fn=path+"processed/"+filename, verbose=False)

    selector.run(single_path=True)

    if selector.solved:
        solved += 1
    if selector.cnf.solve():
        sat += 1
    assignments_to_failure.append(selector.assignments_to_failure)


print(f"SOLVED:\t{solved}\nSAT:\t{sat}")
print(assignments_to_failure)
