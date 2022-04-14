import os
from properties import DATA_PATH
from graphs_of_projects import create_gspan_input

def select_projects(input_folder, output_file, min_lines, max_lines):
    print("Selecting project relationships with more than " + str(min_lines) + " and less than " + str(max_lines) + " lines.")
    last_repo = False
    # Serial number of the project meeting the specified requirements
    i = 0
    # Get the list of projects
    list_of_projects = os.listdir(input_folder)
    # Take only the downloaded projects
    list_of_projects = [project for project in list_of_projects if not os.path.getsize(input_folder + project) == 0]
    # Do not take into account text files and the commit_relationships folder
    list_of_projects = [project for project in list_of_projects if not project.endswith(".txt") and project != "commit_relationships" and os.path.getsize(input_folder + project + "/relationships.txt") != 0]
    for counter, project in enumerate(list_of_projects):
        project_path = os.path.join(DATA_PATH, project + "/")
        relationships_path = os.path.join(project_path, "relationships.txt")
        with open(relationships_path, "r+") as infile:
            lines = infile.readlines()
        if counter == len(list_of_projects) - 1:
            last_repo = True
        if len(lines) > min_lines and len(lines) < max_lines:
            create_gspan_input(relationships_path, output_file, i, last_repo)
            i += 1
        elif last_repo:
            # This happens when we have reached the last repo of the dataset, but this does not have less than max_lines and more than min_lines relationships
            with open(output_file, "a+") as outfile:
                outfile.write("t # -1")
                print("Done")
                
                
if __name__ == '__main__':
    """ This main function is used for testing. """
    input_folder = DATA_PATH
    # Select projects whose relationships are more than this value
    min_lines = 100
    # Select projects whose relationships are less than this value
    max_lines = 400
    output_file = "./graphs_of_projects_" + str(min_lines) + "_" + str(max_lines) + ".txt"
    select_projects(input_folder, output_file, min_lines, max_lines)