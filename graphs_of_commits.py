import os

def commit_gspan_input(inputfile, outputfile, i, last_graph):
    print("Creating input for gspan for commits of projects")
    with open(inputfile) as infile:
        relationships = [l.strip() for l in infile.readlines()]
        
    with open(outputfile, 'a+') as outfile:
        outfile.write("t # " + str(i) + "\n")
        s1 = ""
        s2 = ""
        s3 = ""
        for line in relationships:
            lineSegments = line.split()
            
            if line.startswith("-"):
                # Type of the edge between two class nodes which corresponds to the type of the relationship between them
                if lineSegments[3] == "inherits": s2 = "2"
                elif lineSegments[3] == "uses": s2 = "3"
                elif lineSegments[3] == "calls": s2 = "4"
                elif lineSegments[3] == "creates": s2 = "5"
                elif lineSegments[3] == "has": s2 = "6"
                elif lineSegments[3] == "references": s2 = "7"
                else: print("Something strange happened!")
                
            elif line.startswith("+"):
                # Type of the edge between two class nodes which corresponds to the type of the relationship between them
                if lineSegments[3] == "inherits": s2 = "8"
                elif lineSegments[3] == "uses": s2 = "9"
                elif lineSegments[3] == "calls": s2 = "10"
                elif lineSegments[3] == "creates": s2 = "11"
                elif lineSegments[3] == "has": s2 = "12"
                elif lineSegments[3] == "references": s2 = "13"
                else: print("Something strange happened!")                
                
            else:
                print("Something strange happened!")
                
            # Shape of the class node which corresponds to its abstraction level
            if lineSegments[1] == "Normal": s1 = "2"
            elif lineSegments[1] == "Unknown": s1 = "3"
            elif lineSegments[1] == "Abstract": s1 = "4"
            elif lineSegments[1] == "Interface": s1 = "5"
            elif lineSegments[1] == "Abstracted": s1 = "6"
            elif lineSegments[1] == "Any": s1 = "7"
            else: print("Something strange happened!")
    
            # Shape of the class node which corresponds to its abstraction level
            if lineSegments[4] == "Normal": s3 = "2"
            elif lineSegments[4] == "Unknown": s3 = "3"
            elif lineSegments[4] == "Abstract": s3 = "4"
            elif lineSegments[4] == "Interface": s3 = "5"
            elif lineSegments[4] == "Abstracted": s3 = "6"
            elif lineSegments[4] == "Any": s3 = "7"
            else: print("Something strange happened!")
                
            outfile.write("v " + lineSegments[2] + " " + s1 + "\n") 
            outfile.write("v " + lineSegments[5] + " " + s3 + "\n")
            outfile.write("e " + lineSegments[2] + " " + lineSegments[5] + " " + s2 + "\n")
        if last_graph == True: outfile.write("t # -1")
        print("Done!")
        
if __name__ == '__main__':
    """ This main function is not meant to be run. It is used only for testing. """
    commit_relationships = "./other_results/"
    last_graph = False
    outputfile = os.path.join("./graphs_of_commits_8+_40-.txt")
    if os.path.exists(commit_relationships):
        for counter, infile in enumerate(os.listdir(commit_relationships)):
            if counter == len(os.listdir(commit_relationships)) - 1:
                last_graph = True
            commit_gspan_input(os.path.join(commit_relationships, infile), outputfile, counter, last_graph)
    else:
        print("Commit relationships have not been extracted yet!")