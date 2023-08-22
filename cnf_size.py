import argparse
import os
import shutil

from PreSolver.src.SATInstance.CNF import CNF

def main(input_folder):
    output_folder = "PreSolver/instances/satcomp22/"
    for index, file in enumerate(os.listdir(input_folder)):
        print(f"On file {index} - {file}")
        if file[-4:]!=".cnf":
          continue
        fn = open(input_folder+file, "r")
        text = [line.strip("\n") for line in fn.readlines()][0].split(" ")
        fn.close()

        fn = open(input_folder+file, "r")
        cnf_string = fn.read()
        fn.close()

        print(text[2])
        fn_new = f"n{text[2]}_m{text[3]}_{CNF(cnf_string).solve()}.cnf"

        shutil.copy(input_folder+file, output_folder+fn_new)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", required=True, type=str)

    args = parser.parse_args()

    input_folder = path = f"PreSolver/instances/{args.dataset}/"
    main(
        input_folder
    )
