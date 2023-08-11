#!/usr/bin/bash

usage() {
  echo "Usage: $0 <dataset name> [initialisation] [randomisationProb]"
}

handle_error() {
  echo "Error: $1"
  usage
  exit 1
}

# trap 'handle_error "An error occurred."' ERR

if [ $# -lt 1 ]; then
  handle_error "At least one argument is required."
fi

dataset=$1

if [ $# -lt 2 ]; then
    initialisation="control"
  else
    initialisation=$2
fi

if [ $# -lt 3 ]; then
    randomisationProb=25
  else
    randomisationProb=$3
fi

instance_folder="PreSolver/instances/${dataset}/"

if [ $initialisation = "control" ]; then
  output_folder="${instance_folder}results_control_0/"
  randomisationProb=0
else
  output_folder="${instance_folder}results_${initialisation}_${randomisationProb}/"
fi

solver="PreSolver/probSAT-master/probSAT"

if [ -d "$output_folder" ]; then
  rm -r "$output_folder"
fi
mkdir $output_folder

for file in "$instance_folder"*.cnf; do
  filename=$(basename "$file" .cnf)
  echo "On file ${filename}"
  if [ $initialisation = "control" ]; then
    "$solver" -a "$file" > "${output_folder}${filename}.txt"
  else
      initialisation_file="${instance_folder}/${initialisation}_predictions/${filename}.txt"
      "$solver" -a -i "$initialisation_file" -r "$randomisationProb" "$file" > "${output_folder}${filename}.txt"
  fi
done

python collate_results.py -d "$dataset" -e "$initialisation" -r "$randomisationProb"