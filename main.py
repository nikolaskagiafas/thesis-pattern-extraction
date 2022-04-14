import os
from repository_cloner import clone_repo
from properties import REPOS_FILE, DATA_PATH
from relationship_extractor import extract_relationships
from graph_creator import create_graphviz_graphs
from graphs_of_projects import create_gspan_input
from graphs_of_commits import commit_gspan_input
from evolution import commit_evolution

def process_repo(repo_address, i, last_repo):
    # The person or the team that produced the specific project along with its name
    repo_name = '_'.join(repo_address.split('/')[-2:])
    
    # The path, where information about the specific repository is saved
    repo_path = os.path.join(DATA_PATH, repo_name)
    
    # The path where the code of the specific repository is saved
    reposFolderPath = os.path.join(repo_path + "/", "code")
    
    # The path where the evolution mining results of the projects are saved
    evolutionFolderPath = os.path.join(repo_path + "/", "evolution")
    
    print("\nProcessing repo " + repo_name)
    
    download_repo = True

    # Clone repo
    # If repo already exists, return
    if os.path.exists(reposFolderPath):
        print("Repo already exists!\nDone processing repo " + repo_name + "\n")
        download_repo = False
        return download_repo
    clone_repo(repo_address, reposFolderPath)
    # If repo does not exist in GitHub, return
    if not os.path.exists(reposFolderPath):
        print("Repo does not exist in GitHub!\nDone processing repo " + repo_name + "\n")
        download_repo = False
        return download_repo

    # Extract relationships
    relationships_path = os.path.join(repo_path + "/", "relationships.txt")
    extract_relationships(reposFolderPath, relationships_path)

    # Produce graphviz relationships
    outputfile = os.path.join(repo_path + "/", "relationships.dot")
    create_graphviz_graphs(relationships_path, outputfile)
    
    # Produce input for gspan
    outputfile = os.path.join(DATA_PATH, "graphs_of_projects.txt")
    create_gspan_input(relationships_path, outputfile, i, last_repo)
    
    # Produce commit mining results
    commit_evolution(repo_name, reposFolderPath, evolutionFolderPath)
    if last_repo == True:
        commit_graphs()

    print("Done processing repo " + repo_name + "\n")
    
    return download_repo

def commit_graphs():
    # The path where deleted and added relationships of commits of all the projects are saved
    commit_relationships = os.path.join(DATA_PATH, "commit_relationships/")
    # The file that is going to be the input of gspan
    outputfile = os.path.join(DATA_PATH, "graphs_of_commits.txt")
    # Is this the last graph of the dataset or not
    last_graph = False
    # Checking if the commit_relationships path exists
    if os.path.exists(commit_relationships):
       for counter, infile in enumerate(os.listdir(commit_relationships)):
           if counter == len(os.listdir(commit_relationships)) - 1:
               # This is the last graph of the dataset
               last_graph = True
           commit_gspan_input(os.path.join(commit_relationships, infile), outputfile, counter, last_graph)

if __name__ == '__main__':
    # Read repos and iterate one by one
    with open(REPOS_FILE) as infile:
        repos = infile.readlines()

    # Keep only repos with less than 40 commits
    repos = [line.split(';')[0].rstrip() for line in repos if 15 < int(line.split(';')[3]) < 80]
    
    print(len(repos))
    
    # Serial number of project, starting from 0
    j = 0
    
    # Processing the last repo of the list or not
    last_repo = False
    
    # Checking if current repo was downloaded or not
    download_repo = True
    
    # Serial number of downloaded project, starting from 0
    i = 0
    
    # Process repos
    for repo_address in repos:
        if j == len(repos) - 1: last_repo = True
        download_repo = process_repo(repo_address, i, last_repo)
        if download_repo == True: i += 1
        j += 1
