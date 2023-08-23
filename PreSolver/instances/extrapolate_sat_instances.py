import argparse
import os
import shutil

def main(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    for filename in os.listdir(input_folder):
        file = open(input_folder+filename, "r")
        lines = [line.strip("\n") for line in file.readlines()]
        file.close()

        # skip comment lines at beginning
        i = 0
        while i < len(lines) and lines[i][0]=="c":
            i += 1
        lines = lines[i:]

        description, clauses = lines[0].split(" "), [[int(lit) for lit in line.split(" ")] for line in lines[1:]]

        num_vars, num_clauses = description[2], description[3]

        nvar = num_vars
        working_clauses = clauses
        i = 0
        while len(working_clauses)>0:
            i += 1
            working_clauses = [clause for clause in working_clauses
                               if nvar not in [abs(lit) for lit in clause]]
            nvar = max([abs(lit) for clause in working_clauses
                        for lit in clause])
            write_cnf(filename, i, nvar, working_clauses)


def write_cnf(filename, i, nvar, working_clauses):
    string = f"p cnf {nvar} {len(working_clauses)}\n"
    for clause in working_clauses:
        string += " ".join([str(lit) for lit in clause]) + " 0\n"
    file = open(f"{output_folder}{filename[:filename.index('.')]}_{i}_sat.cnf", "w")
    file.write(string)
    file.close()


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