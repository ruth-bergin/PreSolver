import os
import argparse

def main(input_folder, output_file):
    print(f"Writing collated results to output file {output_file}")
    file = open(output_file, "w")
    file.write("instance,tries,cpu_time\n")
    file.close()
    for filename in os.listdir(input_folder):
        fn = open(input_folder+filename, "r")
        messy = [line.strip("\n") for line in fn.readlines()]
        fn.close()
        tries_index, cpu_index = -1,-1
        for index,line in enumerate(messy):
            if "tries" in line:
                tries_index = index
            elif "CPU Time" in line:
                cpu_index = index
        tries = messy[tries_index].split(" ")[-1]
        cpu_time =[word for word in messy[cpu_index].strip("\n").split(" ") if word!=""][-1]
        out = open(output_file, "a")
        out.write(f"{filename},{tries},{cpu_time}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", required=True, type=str)
    parser.add_argument("-e","--experiment", required=True, type=str)
    parser.add_argument("-r", "--randomisationProb", required=True, type=int)

    args = parser.parse_args()

    input_folder = path = f"PreSolver/instances/{args.dataset}/results_{args.experiment}_{args.randomisationProb}/"
    output_file = f"results/{args.dataset}_{args.experiment}_{args.randomisationProb}.txt"
    main(
        input_folder,
        output_file
    )
