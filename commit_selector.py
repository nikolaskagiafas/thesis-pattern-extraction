import os
import shutil
from properties import DATA_PATH

def commit_selector(input_folder, output_folder, min_lines, max_lines):
    for file in os.listdir(input_folder):
        with open(os.path.join(input_folder, file), "r+") as infile:
            lines = infile.readlines()
            if len(lines) > min_lines and len(lines) < max_lines:
                n_path = shutil.copy(os.path.join(input_folder, file), os.path.join(output_folder, file))
                if not os.path.exists(n_path):
                    print("Something strange happened!")
                    break
                
                
                


if __name__ == '__main__':
    """ This main function is used for testing. """
    input_folder = os.path.join(DATA_PATH, "commit_relationships/")
    output_folder = "./other_results/"
    # Select commits whose relationships are more than this value
    min_lines = 7
    # Select commits whose relationships are less than this value
    max_lines = 40
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(input_folder):
        print("Commit relationships have not been extracted yet!")
    else:
        commit_selector(input_folder, output_folder, min_lines, max_lines)