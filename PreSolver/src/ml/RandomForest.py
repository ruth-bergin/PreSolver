import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, RocCurveDisplay, roc_curve, auc, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from ..SATfeatPy.sat_instance.sat_instance import *
import matplotlib.pyplot as plt
import numpy as np

TRAIN, TEST = "train", "test"
INTERMEDIARY_FILENAME = "../instances/intermediary/shadow_cnf_features.txt"

class SAT_RFC:

    def __init__(self, dataset="cbs_dpll_50.txt", dpll=True):
        self.filename = "..\\instances\\rfc\\" + dataset
        self.model = RandomForestClassifier(n_estimators=250, max_depth=8)
        self.data = pd.read_csv(self.filename, header=0).drop(["filename"], axis=1)
        self.dpll=dpll

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

        tn, fp, fn, tp = confusion_matrix(actual, predicted).ravel()

        print(f"SPECIFICITY: {tn/(tn+fp)}")

        display = RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=roc_auc)
        display.plot()
        plt.show()

    def feature_importance(self):
        importances = self.model.feature_importances_

        forest_importances = pd.Series(importances, index=self.data.drop("sat",axis=1).columns)
        std = np.std([tree.feature_importances_ for tree in self.model.estimators_], axis=0)

        fig, ax = plt.subplots()
        forest_importances.plot.bar(yerr=std, ax=ax)
        ax.set_title("Feature importances using MDI")
        ax.set_ylabel("Mean decrease in impurity")
        fig.tight_layout()
        plt.show()

    def predict_shadow_cnfs(self, branch_true, branch_false):
        for cnf_string, assignment in [(branch_true, True), (branch_false, False)]:
            filename = open(f"../instances/intermediary/shadow_cnf_{assignment}.txt", "w")
            filename.write(cnf_string)
            filename.close()
        self.write_satfeatpy_features_to_file(["../instances/intermediary/shadow_cnf_True.txt",
                                              "../instances/intermediary/shadow_cnf_False.txt"])
        test_data = pd.read_csv(INTERMEDIARY_FILENAME, header=0)
        predictions = self.model.predict_proba(test_data)
        return {
            "true":predictions[0][1],
            "false":predictions[1][1]
        }

    def predict_sat(self, cnf_string):
        filename = open("../instances/intermediary/shadow_cnf_dominant.txt", "w")
        filename.write(cnf_string)
        filename.close()
        self.write_satfeatpy_features_to_file(["../instances/intermediary/shadow_cnf_dominant.txt"])
        test_data = pd.read_csv(INTERMEDIARY_FILENAME, header=0)
        return self.model.predict(test_data)

    def write_satfeatpy_features_to_file(self, filename_list):
        info = ",".join(list(self.data.drop("sat", axis=1).columns.values))
        for filename in filename_list:
            info += "\n"
            feats = SATInstance(filename, preprocess=False)
            feats.gen_basic_features()
            if self.dpll:
                feats.gen_dpll_probing_features()
            info += ",".join([str(feats.features_dict[key]) for key in feats.features_dict.keys()])
                              #if key not in ["v","c"]])

        shadow_cnf_features = open(INTERMEDIARY_FILENAME, "w")
        shadow_cnf_features.write(info)
        shadow_cnf_features.close()

if __name__=='__main__':
    rfc = SAT_RFC()

    rfc.test_accuracy()
