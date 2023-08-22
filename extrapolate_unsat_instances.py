import argparse
import os
import shutil
from random import randint, choice

from PreSolver.src.SATInstance.CNF import CNF

def main(input_folder, output_folder):
    print("Checking if folder exists.")
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    print("Beginning to iterate through CNFs.")
    for index, filename in enumerate(os.listdir(input_folder)):
        print(f"On file {index}")
        file = open(input_folder+filename, "r")
        cnf_string = file.read()
        file.close()

        lines = cnf_string.split("\n")
        i = 0
        while lines[i][0]=="c":
            i += 1

        lines = lines[i:]

        description = lines[0]
        print(f"Instance details:\t{description}")
        if int(description.split(" ")[2])>5000:
            print("Instance too large. Skipping.")
            file = open("large_files.txt", "a+")
            file.write(filename + "\n")
            file.close()
            continue
        else:
            print("Constructing CNF.")
        try:
            cnf = CNF(cnf_string, verbose=True, ignore_conflicts=False)
        except:
            cnf = CNF(cnf_string+"\n", verbose=True, ignore_conflicts=False)
        success = 0
        i = 0
        print("Constructed. Beginning assignments.")
        while success==0:
            print(f"On assignment {i}, writing to file.")
            file = open(f"{output_folder}{filename[:filename.index('.')]}_{i}_unsat.cnf", "w")
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