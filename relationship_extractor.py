import os
import subprocess
from properties import JAVA_PATH, REL_EXTRACTOR_PATH

def extract_relationships(reposFolderPath, relationships_path, include_unknown = False):
    print("Extracting relationships from repo")
    if include_unknown:
        command = [JAVA_PATH, '-jar', REL_EXTRACTOR_PATH, reposFolderPath, "includeUnnkown"]
    else:
        command = [JAVA_PATH, '-jar', REL_EXTRACTOR_PATH, reposFolderPath]
    p = subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    with open(relationships_path, 'wb') as outfile:
        while True:
            line = p.stdout.readline()
            if line == b'':
                break
            outfile.write(line)
    print("Done!")

if __name__ == '__main__':
    """ This main function is not meant to be run. It is used only for testing. """
    reposFolderPath = "./test/chrisbanes_cheesesquare/code"
    relationships_path = "./test/chrisbanes_cheesesquare/relationships.txt"
    if os.path.exists(reposFolderPath):
        extract_relationships(reposFolderPath, relationships_path)
    else:
        print("This project has not been downloaded yet!")
