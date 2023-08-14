import os
import argparse

def main(input_folder):
    for filename in os.listdir(input_folder):
        file = open(input_folder+filename, "r")
        assignment = [line.strip("\n") for line in file.readlines()]
        file.close()

        if len(assignment)==1:
            raise ValueError("Already collated.")

        print(assignment[0])
        print(len(assignment)-2)
        newfile = open(input_folder+filename, "w")
        newfile.write("".join(assignment[2:]))
        newfile.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", required=True, type=str)

    args = parser.parse_args()

    input_folder = path = f"PreSolver/instances/{args.dataset}/nlocalsat_predictions/"
    if "/" in args.dataset:
        raise ValueError("Restructure folders so instances are not in subfolder.")
    main(
        input_folder
    )
