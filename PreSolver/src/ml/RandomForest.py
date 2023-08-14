import pandas as pd
from src.SATfeatPy.sat_instance.sat_instance import *
import joblib

TRAIN, TEST = "train", "test"
INTERMEDIARY_FILENAME = "../instances/intermediary/shadow_cnf_features.txt"

class RandomForest:

    def __init__(self,model,dpll=True):
        self.model = joblib.load(model)
        self.dpll=dpll

    def predict_shadow_cnfs(self, shadow_cnf_filenames):
        self.write_satfeatpy_features_to_file(shadow_cnf_filenames)
        test_data = pd.read_csv(INTERMEDIARY_FILENAME, header=0)
        predictions = self.model.predict_proba(test_data)
        return {
            "true":predictions[0][1],
            "false":predictions[1][1]
        }

    def predict_sat(self, cnf_filename):
        self.write_satfeatpy_features_to_file([cnf_filename])
        features = pd.read_csv(INTERMEDIARY_FILENAME, header=0)
        predictions = self.model.predict_proba(features)
        return predictions[0][1]

    def write_satfeatpy_features_to_file(self, filename_list):
        info = ""
        init = True
        for filename in filename_list:
            feats = SATInstance(filename, preprocess=False)
            feats.gen_basic_features()
            if self.dpll:
                feats.gen_dpll_probing_features()
            if init:
                init = False
                info += ",".join([key for key in feats.features_dict.keys()])
            info += "\n"
            info += ",".join([str(feats.features_dict[key]) for key in feats.features_dict.keys()])

        shadow_cnf_features = open(INTERMEDIARY_FILENAME, "w")
        shadow_cnf_features.write(info)
        shadow_cnf_features.close()
