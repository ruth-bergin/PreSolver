import argparse
import os

from VariableSelector import VariableSelector
from SATInstance.CNF import CNF
from ml.RandomForest import SAT_RFC
from os import listdir

def train_classifier(classifier, training_set):
    if classifier=="rfcBase":
        return SAT_RFC(training_set, dpll=False)
    elif classifier=="rfcDpll":
        return SAT_RFC(training_set, dpll=True)
    else:
        raise ValueError("Unrecognised classifier")
def main(classifier_selection, training_set, folder):
    classifier = train_classifier(classifier_selection, training_set)
    output_folder = f"{classifier_selection}_predictions"
    path = f"../instances/{folder}/"

    print("Cleaning up folders")
    folders_to_clear = [output_folder]
    for f in folders_to_clear:
        if os.path.isdir(f"{path}{f}"):
            for file in listdir(f"{path}{f}"):
                os.remove(f"{path}{f}/{file}")
            print(f"{path}{f} cleared")
        else:
            print(f"Making directory {path}{f}")
            os.mkdir(f"{path}{f}")
    for index, filename in enumerate(listdir(path)):
        if filename[-4:]!=".cnf":
            continue
        file = open(path+filename, "r")
        cnf_string = file.read()
        file.close()
        print(f"File {index} - {filename}")

        try:
            cnf = CNF(cnf_string, ignore_conflicts=True)
        except:
            cnf = CNF(cnf_string, sep="  0 \n ", ignore_conflicts=True)

        num_vars = cnf.num_variables
        selector = VariableSelector(cnf, classifier, cutoff=-1, fn=f"{path}processed/{filename}")
        selector.run()
        solution = selector.solution.as_assignment(True)
        if len(solution)!=num_vars:
            raise ValueError(f"Length of solution is {len(solution)} when it should be {num_vars}\n"
                             f"{selector.solution}")
        output = open(f"{path}/{output_folder}/{filename[:-4]}.txt", "w")
        output.write(solution)
        output.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--classifier", required=True, type=str)
    parser.add_argument("-t","--training_set", required=True, type=str)
    parser.add_argument("-d","--dataset", required=True, type=str)

    args = parser.parse_args()
    main(
        args.classifier,
        args.training_set,
        args.dataset
    )
