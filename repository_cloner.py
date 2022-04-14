import os
import subprocess
from properties import GIT_PATH

def clone_repo(repo_address, reposFolderPath):
    print("Downloading repo")
    p = subprocess.Popen([GIT_PATH, 'clone', repo_address, reposFolderPath], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    while True:
        line = p.stdout.readline()
        if line == b'':
            break
    print("Done!")

if __name__ == '__main__':
    """ This main function is not meant to be run. It is used only for testing. """
    repo_address = "https://github.com/chrisbanes/cheesesquare"
    reposFolderPath = "./test/chrisbanes_cheesesquare/code"
    if os.path.exists(reposFolderPath):
        print("Repo already exists!")
    else:
        clone_repo(repo_address, reposFolderPath)
