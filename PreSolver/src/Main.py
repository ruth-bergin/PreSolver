from VariableSelector import VariableSelector
from os import listdir

path = "../instances/andrea/DatasetA/"

for filename in [file for file in listdir(path) if file != "processed"]:
    file = open(path+filename, "r")
    cnf_string = file.read()
    file.close()

    selector = VariableSelector(cnf_string, cutoff=0.01, verbose=True, use_dpll=False, dataset="cbs_base_50.txt",
                                fn=filename)

    selector.run(single_path=True)