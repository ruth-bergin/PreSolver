from ml.RandomForest import RandomForest
import os

rfc = RandomForest("../classifiers/rfcBase.joblib", dpll=False)

path = "../instances/satcomp_unsat/"
instances = [path+instance for instance in os.listdir(path)]

predictions = []
for file in instances:
  try:
    p = rfc.predict_sat(file)
    predictions.append(p)
    print(p)
  except:
    print("Fail")
    predictions.append(0)
    
  if len(predictions)==10:
    break

print(predictions)

print(f"Number of correct predictions:\t{len(list(filter(lambda x: x < 0.5, predictions)))}")
print(f"Number of correct predictions:\t{len(list(filter(lambda x: x < 0.5, predictions)))/len(predictions)}")
