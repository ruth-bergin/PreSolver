import os

from VariableSelector import VariableSelector
from SATInstance.CNF import CNF
from ml.DatasetPopulator import DatasetPopulator
from ml.FeatureExtractor import FeatureExtractor
from os import listdir

def populateDataset(folder, n=50):
    path = f"../instances/{folder}/"

    for index, filename in enumerate(listdir(path)[:n]):
        if filename[-4:]!=".cnf":
            continue
        print(f"File {index} - {filename}")
        file = open(path+filename, "r")
        cnf_string = file.read()
        file.close()

        populator = DatasetPopulator(CNF(cnf_string), index, filename)
        populator.populate()
    FeatureExtractor().extract("../instances/population/","cbs_dpll",True)

populateDataset("cbs", 80)
def experiment(folder_list):
    for folder in folder_list:
        print(f"On folder {folder}")
        path = f"../instances/{folder}/"

        solved = 0
        sat = 0
        assignments_to_failure = []
        for file in listdir(path+"processed/"):
            os.remove(f"{path}processed/{file}")
        for index, filename in enumerate(listdir(path)[23:]):
            if filename[-4:]!=".cnf":
                continue
            file = open(path+filename, "r")
            cnf_string = file.read()
            file.close()
            print(f"File {index} - {filename}")
            if not CNF(cnf_string.strip("%\n0\n\n")).solve():
                print("Unsat, skipping.")
                continue

            file = open(path+"processed/"+filename[:-4]+"_dlisCovariance_p0.cnf", "w")
            file.write(cnf_string)
            file.close()

            try:
                selector = VariableSelector(cnf_string.strip("%\n0\n\n"), cutoff=-1, use_dpll=True, dataset="dataset_final.txt",
                                            fn=path+"processed/"+filename, verbose=True)
            except:
                selector = VariableSelector(cnf_string, cutoff=-1, sep=" 0 \n", use_dpll=True, dataset="dataset_final.txt",
                                            fn=path+"processed/"+filename, verbose=False)

            selector.run(single_path=False)

            if selector.solved:
                solved += 1
            if selector.cnf.solve():
                sat += 1
            assignments_to_failure.append(selector.assignments_to_failure)


        print(f"SOLVED:\t{solved}\nSAT:\t{sat}")
        print(assignments_to_failure)
