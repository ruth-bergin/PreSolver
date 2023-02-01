import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

TRAIN, TEST = "train", "test"

filename = r"C:\Users\Ruth Bergin\Desktop\College_Work\fourth_year\FYP\PreSolver\instances\dataset.txt"
model = RandomForestClassifier()

# Read in file
data = pd.read_csv(filename, header=0)
data = data.drop("filename", axis=1)

# Scale data
sc = StandardScaler()
numeric_cols = data.select_dtypes(include=np.number).columns.tolist()
data.loc[:,numeric_cols] = sc.fit_transform(data.loc[:,numeric_cols])

# Split predictors and label
predictors, label = data.loc[:, data.columns[:-1]],data.loc[:, data.columns[-1:]]
x_train, x_test, y_train,  y_test = train_test_split(predictors, label, test_size=0.20, shuffle=True)

model.fit(X=x_train, y=y_train["sat"].ravel())

# test
predicted = model.predict(x_test).tolist()
actual = y_test.values.ravel()

accuracy = accuracy_score(predicted, actual)
print(f"PREDICTED: {predicted}")
print(f"ACCURACY: {accuracy}")

print(model.predict_proba(x_test))
