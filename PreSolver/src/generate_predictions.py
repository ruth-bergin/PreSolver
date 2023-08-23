import argparse
import os
import time

from VariableSelector import VariableSelector
from SATInstance.CNF import CNF
from ml.RandomForest import RandomForest

def train_classifier(classifier):
    if classifier=="rfcBase":
        return RandomForest(f"../classifiers/{classifier}.joblib", dpll=False)
    elif classifier=="rfcDpll":
        return RandomForest(f"../classifiers/{classifier}.joblib", dpll=True)
    else:
        raise ValueError("Unrecognised classifier")
        
def main(classifier_selection, folder, variable_selection):
    classifier = train_classifier(classifier_selection)
    output_folder = f"{classifier_selection}_{variable_selection}_predictions"
    path = f"../instances/{folder}/"

    print("Cleaning up folders")
    folders_to_clear = [output_folder]
    for f in folders_to_clear:
        if os.path.isdir(f"{path}{f}"):
            for file in os.listdir(f"{path}{f}"):
                os.remove(f"{path}{f}/{file}")
            print(f"{path}{f} cleared")
        else:
            print(f"Making directory {path}{f}")
            os.mkdir(f"{path}{f}")
    files = [file for file in os.listdir(path) if file[-4:]==".cnf"]
    for index, filename in enumerate(files):
        start = time.time()
        if filename[-4:]!=".cnf":
            continue
        file = open(path+filename, "r")
        cnf_string = file.read()
        file.close()
        print(f"File {index} - {filename}")

        try:
            cnf = CNF(cnf_string, metric=variable_selection, ignore_conflicts=True)
        except:
            cnf = CNF(cnf_string, metric=variable_selection, sep="  0 \n ", ignore_conflicts=True)

        selector = VariableSelector(cnf, classifier, variable_selection, cutoff=-1, fn=f"{path}processed/{filename}")
        selector.run()
        solution = selector.solution.as_assignment(True)
              
        output = open(f"{path}/{output_folder}/{filename[:-4]}.txt", "w")
        output.write(solution)
        output.close()

        print(f"Time taken:\t{time.time()-start} seconds")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--classifier", required=True, type=str)
    parser.add_argument("-d","--dataset", required=True, type=str)
    parser.add_argument("-v", "--variableSelection", required=True, type=str)

    args = parser.parse_args()
    # Amend this list when a new metric is added
    if args.variableSelection.lower() not in ["dlis","weighted_purity", "relative_appearances"]:
        raise ValueError("Invalid variable selection method. Valid options are: "
                         "[dlis|weighted_purity|relative_appearances]")
    main(
        args.classifier,
        args.dataset,
        args.variableSelection
    )
