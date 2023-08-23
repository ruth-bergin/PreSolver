import argparse
import os
import shutil
from random import randint, choice

from PreSolver.src.SATInstance.CNF import CNF

def main(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    for filename in os.listdir(input_folder):
        file = open(input_folder+filename, "r")
        cnf_string = file.read()
        file.close()

        # skip comment lines at beginning
        cnf = CNF(cnf_string, ignore_conflicts=False)
        success = 0
        i = 0
        while success==0:
            file = open(f"{output_folder}{filename[:filename.index('.')]}_i_unsat.cnf", "w")
            file.write(str(cnf))
            file.close()
            i += 1
            literal = randint(1, cnf.num_variables) * choice([-1, 1])
            success = cnf.assign_literal_by_integer(literal)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", required=True, type=str)
    parser.add_argument("-o", "--output", type=str)

    args = parser.parse_args()

    input_folder = f"PreSolver/instances/{args.dataset}/"
    output_folder = input_folder.strip(r"/") + "-extended/" if args.output is None else args.output
    main(
        input_folder,
        output_folder
    )