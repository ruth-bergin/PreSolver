from SATfeatPy import sat_instance
from os import listdir

from src.SATInstance.CNF import CNF
from src.SATfeatPy.sat_instance.sat_instance import SATInstance
import argparse



def extract(src, dst, create, feature_set="dpll", unsat_only=False):
    output = f"../instances/rfc/{dst}.txt"

    for index, filename in enumerate(listdir(src)):
        print(f"On file {index}")
        fn = open(src+filename, "r")
        cnf_string = fn.read()
        fn.close()
        if unsat_only and CNF(cnf_string).solve():
            print("Sat - skipping")
            continue
        instance = SATInstance(src+filename,preprocess=False,preprocess_tmp=False)
        instance.gen_basic_features()
        if feature_set=="dpll":
            instance.gen_dpll_probing_features()
        if create:
            create = False
            file = open(output, "w")
            file.write(",".join(["filename"]+[key for key in instance.features_dict.keys()]+["sat"])+"\n")
            file.close()
        file = open(output, "a+")
        file.write(",".join([filename]+
                            [str(value) for value in instance.features_dict.values()]+
                            [str(CNF(cnf_string).solve())])+"\n")
        file.close()

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--src", required=True, type=str)
    parser.add_argument("-d", "--dst", required=True, type=str)
    parser.add_argument("-c", "--createfile", required=True, type=bool)
    parser.add_argument("-f", "--featureset", default="base", type=str)
    parser.add_argument("-u", "--unsatonly", type=bool)

    try:
        args = parser.parse_args()
    except Exception as e:
        print("--src:\tsource folder\n"
              "--dst:\tdestination folder\n"
              "--createfile:\tcreate new file with headings (overwrite if exists)\n"
              "--featureset:\tif [dpll] generates dpll features\n"
              "--unsatonly:\tonly take unsat instances - for class balance tuning\n")
        raise e
        
    extract(args.src,
            args.dst,
            args.createfile,
            args.featureset,
            args.unsatonly)