import os
import shutil

source_folder = "satcomp_sat"
destination_folder = "training_seed"
num_largest_files = 30

# Get a list of all files in the source folder
all_files = [(filename, os.path.getsize(os.path.join(source_folder, filename))) for filename in os.listdir(source_folder)]

# Sort the files by size in descending order and get the largest ones
largest_files = sorted(all_files, key=lambda x: x[1], reverse=True)[:num_largest_files]

# Get the names of the largest files
largest_file_names = [filename for filename, _ in largest_files]

# Move the largest files to the destination folder
for filename in largest_file_names:
    os.remove(source_folder+"/"+filename)
