import os
import shutil
from properties import DATA_PATH
from pydriller import RepositoryMining
from pydriller.domain.commit import ModificationType
from relationship_extractor import extract_relationships



def commit_evolution(repo_name, reposFolderPath, evolutionFolderPath):
    print("Mining repo commits")
    repomining = RepositoryMining(reposFolderPath)
    # The path where the code and the structure of a specific project are evolved
    repository_path = evolutionFolderPath + "/repository/"
    if not os.path.exists(repository_path):
       os.makedirs(repository_path)
    # The path where differential relationships between commits are saved   
    diff_relationships = evolutionFolderPath + "/diff_relationships/"
    if not os.path.exists(diff_relationships):
        os.makedirs(diff_relationships)
    # The path where deleted and added relationships of commits of all the projects are saved
    commit_relationships = os.path.join(DATA_PATH, "commit_relationships/")
    if not os.path.exists(commit_relationships):
        os.makedirs(commit_relationships)
    # The path where commits of a specific project are saved
    new_commit_path = evolutionFolderPath + "/commit_"
    # Including modification types apart from add, delete, modify, rename or not
    unknown_copy = False
    # The serial number of a commit in main branch
    commit_number = 0
    # The index of the previous commit, in which there were modifications in java files
    previous_commit = 0
    for commit in repomining.traverse_commits():
        # Analyze only commits of the main branch
        if commit.in_main_branch:
            commit_number += 1
            if not os.path.exists(new_commit_path + str(commit_number)):
                os.makedirs(new_commit_path + str(commit_number))
            if commit.merge:
                # Do not analyze merging commits
                pass
            else:
                # The list of files that were added
                added_files = []
                # The list of files that were deleted
                deleted_files = []
                for modification in commit.modifications:
                    # Take only modifications on java files
                    if modification.filename.endswith(".java"):
                        # Take the name of the java file
                        file_name = modification.filename
                        # Take the type of the change
                        change = modification.change_type
                        if change == ModificationType.DELETE:
                            # Delete file from the repository and create an empty one with the same name in this commit folder
                            o_path = '/'.join(modification.old_path.split('\\'))
                            o_path = repository_path + o_path
                            if os.path.exists(o_path):
                                os.remove(o_path)
                            with open(new_commit_path + str(commit_number) + "/" + file_name, 'w+') as outfile:
                                outfile.write("")
                            deleted_files.append(file_name.split('.java')[0])
                        elif change == ModificationType.MODIFY or change == ModificationType.RENAME:
                            # These types of changes are similar
                            # In MODIFY, the code of a file changes
                            # In RENAME, the code may change as well as the path or the name or both
                            # Find the folder path of the file after the change
                            n_path = '/'.join(modification.new_path.split('\\')[:-1])
                            n_path = repository_path + n_path
                            if not os.path.exists(n_path):
                                os.makedirs(n_path)
                            # Find the path of the file before the change
                            o_path = '/'.join(modification.old_path.split('\\'))
                            o_path = repository_path + o_path
                            if not modification.source_code == None:
                                # Get the code after the change
                                code_after = "\n".join(modification.source_code.splitlines()).encode('ascii', 'ignore').decode()
                                if change == ModificationType.RENAME and n_path == o_path.split('/')[:-1]:
                                    # This happens when there are modifications in the source code and the name of the file changes
                                    os.remove(o_path)
                                with open(new_commit_path + str(commit_number) + "/" + file_name, 'w+') as outfile:
                                    outfile.write(code_after)
                                try:
                                    with open(n_path + "/" + file_name, 'w+') as outfile:
                                        outfile.write(code_after)
                                except:
                                    file_not_found_error(repo_name, evolutionFolderPath, commit_number)
                                    unknown_copy = True
                                    break
                            else:
                                # There are no modifications of the source code, only the path or the name of the file changes (or both)
                                n_path = '/'.join(modification.new_path.split('\\'))
                                n_path = repository_path + n_path
                                if n_path.split('/')[:-1] == o_path.split('/')[:-1]:
                                    try:
                                        os.rename(o_path, n_path)
                                    except:
                                        file_not_found_error(repo_name, evolutionFolderPath, commit_number)
                                        unknown_copy = True
                                        break
                                else:
                                    if os.path.exists(o_path):
                                        try: 
                                            n_path = shutil.copy(o_path, n_path)
                                        except:
                                            same_file_error(repo_name, evolutionFolderPath, commit_number)
                                            unknown_copy = True
                                            break
                                    else:
                                        unknown_copy = True
                                        if os.path.exists(evolutionFolderPath):
                                            shutil.rmtree(evolutionFolderPath)
                                        break
                            if os.path.exists(o_path) and change == ModificationType.RENAME:
                                # In this case, the full path has definitely changed
                                # If the path remains the same, remove will throw an error
                                if not n_path.split('/')[:-1] == o_path.split('/')[:-1]:
                                    os.remove(o_path)
                        elif change == ModificationType.ADD:
                            # Add a new file in the repository and create the same one in this commit folder
                            n_path = '/'.join(modification.new_path.split('\\')[:-1])
                            n_path = repository_path + n_path
                            if not os.path.exists(n_path):
                                os.makedirs(n_path)
                            # Get the code of the new file
                            code_after = "\n".join(modification.source_code.splitlines()).encode('ascii', 'ignore').decode()
                            with open(new_commit_path + str(commit_number) + "/" + file_name, 'w+') as outfile:
                                outfile.write(code_after)
                            try: 
                                with open(n_path + "/" + file_name, 'w+') as outfile:
                                    outfile.write(code_after)
                                added_files.append(file_name.split('.java')[0])
                            except:
                                file_not_found_error(repo_name, evolutionFolderPath, commit_number)
                                unknown_copy = True
                                break
                        else:
                            unknown_copy_modification(repo_name, evolutionFolderPath)
                            unknown_copy = True
                            break
                if unknown_copy:
                    unknown_copy = False
                    break
                # Checking if the evolution folder still exists
                if os.path.exists(evolutionFolderPath):
                    # Checking if there are java files modified, added, deleted or renamed in this commit
                    if os.listdir(new_commit_path + str(commit_number)):
                        # Extract relationships from the repo as it has been formed until this commit
                        extract_relationships(repository_path, new_commit_path + str(commit_number) + "/relationships_" + str(commit_number) + ".txt")
                        # Checking if this is the first commit with changes or not
                        if previous_commit == 0:
                            # In the first commit with changes, there are only files that were added
                            with open(diff_relationships + "commit_" + str(commit_number) + ".txt", 'w+') as outfile:
                                outfile.write("")
                            # Now the previous commit index is assigned to the first commit with changes in java files
                            previous_commit = commit_number
                        else:
                            added_lines = []
                            deleted_lines = []
                            # Read the extracted relationships from the project after the changes of the current commit
                            with open(new_commit_path + str(commit_number) + "/relationships_" + str(commit_number) + ".txt", 'r+') as infile:
                                lines_after = infile.readlines()
                            # Read the extracted relationships from the project after the changes of the previous commit
                            with open(new_commit_path + str(previous_commit) + "/relationships_" + str(previous_commit) + ".txt", 'r+') as infile:
                                lines_before = infile.readlines()
                            # Take the relationships that are added and do not correspond to the class of a file that was added
                            for line in lines_after:
                                if line.split(' ')[1] not in added_files and line not in lines_before:
                                    added_lines.append(line)
                            # Take the relationships that are deleted and do not correspond to the class of a file that was deleted
                            for line in lines_before:
                                if line.split(' ')[1] not in deleted_files and line not in lines_after:
                                    deleted_lines.append(line)
                            # Write the relationships that were added or deleted
                            with open(diff_relationships + "commit_" + str(commit_number) + ".txt", 'w+') as outfile:
                                for line in added_lines:
                                    outfile.write("+ " + line)
                                for line in deleted_lines:
                                    outfile.write("- " + line)
                            # The current commit will be the previous for the next one with changes in java files
                            previous_commit = commit_number
                            # Save the added and deleted relationships of interesting commits in the commit_relationships folder
                            if len(added_lines) + len(deleted_lines) > 0:
                                n_path = os.path.join(commit_relationships, repo_name + "_" + str(commit_number) + ".txt")
                                n_path = shutil.copy(diff_relationships + "commit_" + str(commit_number) + ".txt", n_path)
                        
    print("Done!")
    
def file_not_found_error(repo_name, evolutionFolderPath, commit_number):
    with open(DATA_PATH + "possible_errors.txt", 'a+') as outfile:
       outfile.write("FileNotFoundError occured in repository " + repo_name + " at commit " + str(commit_number) + "\n")
    if os.path.exists(evolutionFolderPath):
       shutil.rmtree(evolutionFolderPath) 
       
def same_file_error(repo_name, evolutionFolderPath, commit_number):
    with open(DATA_PATH + "possible_errors.txt", 'a+') as outfile:
       outfile.write("SameFileError occured in repository " + repo_name + " at commit " + str(commit_number) + "\n")
    if os.path.exists(evolutionFolderPath):
       shutil.rmtree(evolutionFolderPath)
       
def unknown_copy_modification(repo_name, evolutionFolderPath):
    with open(DATA_PATH + "possible_errors.txt", 'a+') as outfile:
       outfile.write("There is at least one commit with one or more copy or unknown modification types in the repository " + repo_name + "\n")
    if os.path.exists(evolutionFolderPath):
       shutil.rmtree(evolutionFolderPath) 
    
                
if __name__ == '__main__':
    """ This main function is not meant to be run. It is used only for testing. """
    repo_name = "chrisbanes_cheesesquare"
    reposFolderPath = "./test/chrisbanes_cheesesquare/code"
    evolutionFolderPath = "./test/chrisbanes_cheesesquare/evolution"
    if os.path.exists(reposFolderPath):
        commit_evolution(repo_name, reposFolderPath, evolutionFolderPath)
    else:
        print("This project has not been downloaded yet!")
    
    
    
    
    
    