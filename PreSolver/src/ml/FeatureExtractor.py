from SATfeatPy import sat_instance
from os import listdir

from src.SATInstance.CNF import CNF
from src.SATfeatPy.sat_instance.sat_instance import SATInstance


class FeatureExtractor:
    def extract(self, src, dst, create, feature_set="dpll"):
        output = f"../instances/rfc/{dst}.txt"

        for index, filename in enumerate(listdir(src)):
            print(f"On file {index}")
            fn = open(src+filename, "r")
            cnf_string = fn.read()
            fn.close()
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
