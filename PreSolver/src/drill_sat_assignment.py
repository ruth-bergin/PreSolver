import os
import argparse
from random import choice

from SATInstance.CNF import CNF

def main(input_folder, solution_folder, output_folder):
    for filename in os.listdir(input_folder):
        sfile = open(solution_folder+filename[:-3]+"txt", "r")
        assignment = [int(lit) for lit in sfile.read().split(",") if lit!=""]
        sfile.close()

        file = open(input_folder+filename, "r")
        cnf_string = file.read()
        file.close()

        try:
            cnf = CNF(cnf_string, verbose=True)
        except:
            cnf = CNF(cnf_string+"\n", verbose=True)

        i = 0
        while not cnf.solved:
            newfile = open(f"{output_folder}{filename[:-4]}_{i}_sat.cnf", "w")
            newfile.write(str(cnf))
            newfile.close()
            i += 1
            cnf.assign_literal_by_original_integer(choice(assignment))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", required=True, type=str)
    parser.add_argument("-o", "--output", required=True, type=str)

    args = parser.parse_args()

    input_folder = f"../instances/{args.dataset}/"
    solution_folder = f"../instances/{args.dataset}/results_control_0/solutions/"
    output_folder = f"../instances/{args.output}/"
    main(
        input_folder,
        solution_folder,
        output_folder
    )
