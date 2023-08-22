import os
import argparse

def main(input_folder):
    for index, filename in enumerate(os.listdir(input_folder)):
        if not os.path.exists(input_folder+"solutions"):
            os.mkdir(input_folder+"solutions")
        print(f"On file {index}.")
        file = open(input_folder+filename, "r")
        assignment = [lit for line in file.readlines() if line[0]=="v"
                      for lit in line.strip("\n").split(" ")[1:]]
        file.close()

        newfile = open(input_folder+"solutions/"+filename[:-3]+"txt", "w")
        newfile.write(",".join(assignment))
        newfile.close()

        os.remove(input_folder+filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", required=True, type=str)

    args = parser.parse_args()

    input_folder = f"../instances/{args.dataset}/results_control_0/"
    main(
        input_folder
    )
