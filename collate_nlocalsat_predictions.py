import os
import argparse

def main(input_folder):
    for filename in os.listdir(input_folder):
        file = open(input_folder+filename, "r")
        assignment = [line.strip("\n") for line in file.readlines()]
        file.close()

        if len(assignment)==1:
            raise ValueError("Already collated.")
            
        newfile = open(input_folder+filename[:-3]+"txt", "w")
        newfile.write("".join(assignment[2:]))
        newfile.close()
        
        os.remove(input_folder+filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", required=True, type=str)

    args = parser.parse_args()

    input_folder = path = f"PreSolver/instances/{args.dataset}/predictions_nlocalsat/"
    main(
        input_folder
    )
