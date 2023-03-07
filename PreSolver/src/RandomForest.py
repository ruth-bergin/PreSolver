import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, RocCurveDisplay, roc_curve, auc
from sklearn.ensemble import RandomForestClassifier
from SATfeatPy.sat_instance.sat_instance import *
import matplotlib.pyplot as plt

TRAIN, TEST = "train", "test"
INTERMEDIARY_FILENAME = "../instances/intermediary/shadow_cnf_features.txt"

class SAT_RFC:

    def __init__(self, dpll_included = False):
        self.filename = "..\\instances\\dataset_no_dpll.txt"
        if dpll_included:
            self.filename = "..\\instances\\dataset.txt"
        self.dpll_included = dpll_included
        self.model = RandomForestClassifier(n_estimators=250, max_depth=8)
        self.data = pd.read_csv(self.filename, header=0).drop("filename", axis=1)

        # Split predictors and label
        predictors, label = self.data.loc[:, self.data.columns[:-1]],self.data.loc[:, self.data.columns[-1:]]
        self.x_train, self.x_test, self.y_train,  self.y_test = train_test_split(predictors, label, test_size=0.20, shuffle=True)

        self.model.fit(X=self.x_train, y=self.y_train["sat"].ravel())

    def test_accuracy(self):
        # test
        predicted = self.model.predict(self.x_test).tolist()
        actual = self.y_test.values.ravel()

        fpr, tpr, thresholds = roc_curve(actual, predicted)
        roc_auc = auc(fpr, tpr)

        accuracy = accuracy_score(predicted, actual)
        print(f"PREDICTED: {predicted}")
        print(f"ACCURACY: {accuracy}")

        display = RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=roc_auc)
        display.plot()
        plt.show()

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
        info = ",".join(list(self.data.drop("sat", axis=1).columns.values))
        for filename in branch_true, branch_false:
            info += "\n"
            feats = SATInstance(filename, preprocess=False)
            feats.gen_basic_features()
            if self.dpll_included:
                feats.gen_dpll_probing_features()
            info += ",".join([str(feats.features_dict[key]) for key in feats.features_dict.keys()])

        shadow_cnf_features = open(INTERMEDIARY_FILENAME, "w")
        shadow_cnf_features.write(info)
        shadow_cnf_features.close()

if __name__=='__main__':
    rfc = SAT_RFC()

    rfc.test_accuracy()
