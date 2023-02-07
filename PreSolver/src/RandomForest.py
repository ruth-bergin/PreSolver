import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from SATfeatPy.sat_instance.sat_instance import *

TRAIN, TEST = "train", "test"
INTERMEDIARY_FILENAME = "../instances/intermediary/shadow_cnf_features.txt"

class SAT_RFC:

    def __init__(self, filename="..\\instances\\dataset.txt"):
        self.filename = filename
        self.model = RandomForestClassifier(n_estimators=10, max_depth=8)
        self.data = pd.read_csv(self.filename, header=0).drop("filename", axis=1)

        # Split predictors and label
        predictors, label = self.data.loc[:, self.data.columns[:-1]],self.data.loc[:, self.data.columns[-1:]]
        self.x_train, self.x_test, self.y_train,  self.y_test = train_test_split(predictors, label, test_size=0.20, shuffle=True)

        self.model.fit(X=self.x_train, y=self.y_train["sat"].ravel())

    def test_accuracy(self):
        # test
        predicted = self.model.predict(self.x_test).tolist()
        actual = self.y_test.values.ravel()

        accuracy = accuracy_score(predicted, actual)
        print(f"PREDICTED: {predicted}")
        print(f"ACCURACY: {accuracy}")

    def predict_cnf(self, branch_true, branch_false):
        for cnf_string, assignment in [(branch_true, True), (branch_false, False)]:
            filename = open(f"../instances/intermediary/shadow_cnf_{assignment}.txt", "w")
            filename.write(cnf_string)
            filename.close()
        self.write_satfeatpy_features_to_file("../instances/intermediary/shadow_cnf_True.txt",
                                              "../instances/intermediary/shadow_cnf_False.txt")
        test_data = pd.read_csv(INTERMEDIARY_FILENAME, header=0)
        predictions = self.model.predict_proba(test_data)
        return {
            "true":predictions[0][1],
            "false":predictions[1][1]
        }

    def write_satfeatpy_features_to_file(self, branch_true, branch_false):
        info = "c,v,clauses_vars_ratio,vars_clauses_ratio,vcg_var_mean,vcg_var_coeff,vcg_var_min,vcg_var_max,vcg_var_entropy,vcg_clause_mean,vcg_clause_coeff,vcg_clause_min,vcg_clause_max,vcg_clause_entropy,vg_mean,vg_coeff,vg_min,vg_max,pnc_ratio_mean,pnc_ratio_coeff,pnc_ratio_min,pnc_ratio_max,pnc_ratio_entropy,pnv_ratio_mean,pnv_ratio_coeff,pnv_ratio_min,pnv_ratio_max,pnv_ratio_entropy,pnv_ratio_stdev,binary_ratio,ternary_ratio,ternary+,hc_fraction,hc_var_mean,hc_var_coeff,hc_var_min,hc_var_max,hc_var_entropy"
        for filename in branch_true, branch_false:
            info += "\n"
            feats = SATInstance(filename, preprocess=False)
            feats.gen_basic_features()
            info += filename + ","
            info += ",".join([str(feats.features_dict[key]) for key in feats.features_dict.keys()])

        shadow_cnf_features = open(INTERMEDIARY_FILENAME, "w")
        shadow_cnf_features.write(info)
        shadow_cnf_features.close()

if __name__=='__main__':
    rfc = SAT_RFC()

    rfc.test_accuracy()
