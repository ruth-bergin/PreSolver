import argparse
import os


def main(input_folder):
    to_be_removed = []
    for file in os.listdir(input_folder):
        if file[-4:]==".cnf":
            fn = open(input_folder+file, "r")
            nvar = [line.strip("\n") for line in fn.readlines() if line[0]!="c"][0].split(" ")[2]
            fn.close()
            
            print(nvar)

            if int(nvar)>5000:
              to_be_removed.append(file)
    print(f"{len(to_be_removed)} files to be removed.")
    for file in to_be_removed:
      os.remove(input_folder+file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", required=True, type=str)

    args = parser.parse_args()
    
    main(
        args.dataset
    )
