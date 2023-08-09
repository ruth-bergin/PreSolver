import os

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, RocCurveDisplay, roc_curve, auc, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import numpy as np
import joblib
import argparse

TRAIN, TEST = "train", "test"
INTERMEDIARY_FILENAME = "../instances/intermediary/shadow_cnf_features.txt"

class RandomForestTrainer:

    def __init__(self, name, dataset):
        self.name = name
        self.filename = "..\\..\\instances\\rfc\\" + dataset
        print(f"Current WD: {os.getcwd()}")
        self.model = RandomForestClassifier(n_estimators=250, max_depth=8)
        self.data = pd.read_csv(self.filename, header=0).drop(["filename"], axis=1)
        self.split()

    def split(self):
        # Split predictors and label
        predictors, label = self.data.loc[:, self.data.columns[:-1]],self.data.loc[:, self.data.columns[-1:]]
        self.x_train, self.x_test, self.y_train,  self.y_test = train_test_split(predictors, label, test_size=0.20, shuffle=True)
    def train(self):
        self.model.fit(X=self.x_train, y=self.y_train["sat"].ravel())

    def save(self):
        joblib.dump(self.model, f"../../classifiers/{self.name}.joblib")

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

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--dataset", required=True, type=str)
    parser.add_argument("-n", "--name", required=True, type=str)

    args = parser.parse_args()
    # Amend this list when a new metric is added
    random_forest_trainer = RandomForestTrainer(
        args.name,
        args.dataset
    )
    random_forest_trainer.train()
    random_forest_trainer.save()

