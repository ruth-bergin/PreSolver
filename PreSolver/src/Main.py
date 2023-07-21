import os
from random import randint,choice

from VariableSelector import VariableSelector
from SATInstance.CNF import CNF
from ml.DatasetPopulator import DatasetPopulator
from ml.FeatureExtractor import extract
from os import listdir
import wget
import lzma

def truncate_instances():
    path = "../instances/satcomp/instances/"

    for file in os.listdir(path):
        nvar = int(file[file.find("_n")+2:file.find("_m")])
        if nvar<=1000:
            print(nvar)
            fn = open(path+file,"r")
            src = fn.read()
            fn.close()
            dst = open(f"../instances/sat_comp_refined/{file}", "w")
            dst.write(src)
            dst.close()

def extract_dataset(path):
    for i,file in enumerate(listdir(path)[412:]):
        index = i + 412
        try:
            with lzma.open(path+file, mode='rt', encoding='utf-8') as fid:
                cnf_string = "".join(fid)
                nvar, nclause = cnf_string.split(" ")[2:4]
                nclause = nclause.split("\n")[0]
                fn = open(f"{path}instances/{index}_n{nvar}_m{nclause}.cnf","w")
                fn.write(cnf_string)
                fn.close()

                print("Index:{} \t{} vars \t{} clauses".format(index,nvar, nclause))
        except:
            print("skipping")
            continue

# extract_dataset("../instances/satcomp/")
def download_dataset(src):
    file = open(src, "r")
    urls = file.readlines()
    file.close()
    os.chdir("../instances/satcomp/")

    for index,url in enumerate(urls):
        print(index)
        wget.download(url)

# download_dataset("C:\\Users\\rbergin\\Downloads\\track_main_2022.uri")
def populate_dataset(folder, n=50, step=1):
    path = f"../instances/{folder}/"
    for file in listdir("../instances/population/"):
        os.remove(f"../instances//population/{file}")
    print("Directory cleared")

    for index, filename in enumerate(listdir(path)[:n*step:step]):
        if filename[-4:]!=".cnf":
            continue
        print(f"File {index} - {filename}")
        file = open(path+filename, "r")
        cnf_string = file.read()
        file.close()

        cnf = CNF(cnf_string)

        populator = DatasetPopulator(cnf, index, filename)
        populator.populate(random_after=choice([i*10 for i in range(10)]))
        print(f"CNF SAT {populator.cnf.solve()} with {populator.cnf.num_variables} variables left")
        #*(randint(0,100)/100)**2))

#populate_dataset("cbs", 80)
#extract("../instances/population/","cbs_base",True, feature_set="base")
def experiment(folder_list, single_path=False):
    for folder in folder_list:
        print(f"On folder {folder}")
        path = f"../instances/{folder}/"

        solved = 0
        sat = 0
        assignments_to_failure = []
        for file in listdir(path+"processed/"):
            os.remove(f"{path}processed/{file}")
        print("processed cleared")
        for file in listdir(path+"assignment_confidence_base/"):
            os.remove(f"{path}assignment_confidence_base/{file}")
        print("assignment confidence base cleared")
        for index, filename in enumerate(listdir(path)):
            if filename[-4:]!=".cnf":
                continue
            file = open(path+filename, "r")
            cnf_string = file.read()
            file.close()
            print(f"File {index} - {filename}")
            #if not CNF(cnf_string, sep="  0 \n ").solve():
            #    print("Unsat, skipping.")
            #    continue

            file = open(path+"processed/"+filename[:-4]+"_dlisTieBreakPurity_p0.cnf", "w")
            file.write(cnf_string)
            file.close()

            try:
                selector = VariableSelector(cnf_string, sep="  0 \n ", cutoff=-1, use_dpll=False, dataset="cbs_base.txt",
                                            fn=path+"processed/"+filename, verbose=False)
            except:
                selector = VariableSelector(cnf_string, cutoff=-1, use_dpll=False, dataset="cbs_base.txt",
                                            fn=path+"processed/"+filename, verbose=False)

            selector.run(single_path=single_path)

            if selector.solved:
                solved += 1
            if selector.cnf.solve():
                sat += 1
            assignments_to_failure.append(selector.assignments_to_failure)


        print(f"SOLVED:\t{solved}\nSAT:\t{sat}")
        print(assignments_to_failure)

experiment([f"andrea/iscas/iscas{i}" for i in []]+["andrea/DatasetB"], single_path=True)

