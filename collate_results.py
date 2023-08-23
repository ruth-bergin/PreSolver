import os
import argparse

def main(input_folder, output_file):
    print(f"Writing collated results to output file {output_file}")
    file = open(output_file, "w")
    file.write("instance,tries,cpu_time,solved\n")
    file.close()
    for filename in os.listdir(input_folder):
        fn = open(input_folder+filename, "r")
        messy = [line.strip("\n") for line in fn.readlines()]
        fn.close()
        tries, cpu_index = 0,-1
        solved = False
        for index,line in enumerate(messy):
            if "UNKNOWN" in line:
                tries += 1
            elif "CPU Time" in line:
                cpu_index = index
            elif "SATISFIABLE" in line:
                solved = True
        cpu_time =[word for word in messy[cpu_index].strip("\n").split(" ") if word!=""][-1]
        out = open(output_file, "a")
        out.write(f"{filename},{tries},{cpu_time},{solved}\n")

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
