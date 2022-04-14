import os

def create_gspan_input(inputfile, outputfile, i, last_repo):
    print("Creating input for gspan")
    with open(inputfile) as infile:
        relationships = [l.strip() for l in infile.readlines()]
        
    with open(outputfile, 'a+') as outfile:
        outfile.write("t # " + str(i) + "\n")
        s1 = ""
        s2 = ""
        s3 = ""
        for line in relationships:
            lineSegments = line.split()
            # Shape of the class node which corresponds to its abstraction level
            if lineSegments[0] == "Normal": s1 = "2"
            elif lineSegments[0] == "Unknown": s1 = "3"
            elif lineSegments[0] == "Abstract": s1 = "4"
            elif lineSegments[0] == "Interface": s1 = "5"
            elif lineSegments[0] == "Abstracted": s1 = "6"
            elif lineSegments[0] == "Any": s1 = "7"
            else: print("Something strange happened!")
    
            # Shape of the class node which corresponds to its abstraction level
            if lineSegments[3] == "Normal": s3 = "2"
            elif lineSegments[3] == "Unknown": s3 = "3"
            elif lineSegments[3] == "Abstract": s3 = "4"
            elif lineSegments[3] == "Interface": s3 = "5"
            elif lineSegments[3] == "Abstracted": s3 = "6"
            elif lineSegments[3] == "Any": s3 = "7"
            else: print("Something strange happened!")
               
            # Type of the edge between two class nodes which corresponds to the type of the relationship between them
            if lineSegments[2] == "inherits": s2 = "2"
            elif lineSegments[2] == "uses": s2 = "3"
            elif lineSegments[2] == "calls": s2 = "4"
            elif lineSegments[2] == "creates": s2 = "5"
            elif lineSegments[2] == "has": s2 = "6"
            elif lineSegments[2] == "references": s2 = "7"
            else: print("Something strange happened!")
            outfile.write("v " + lineSegments[1] + " " + s1 + "\n") 
            outfile.write("v " + lineSegments[4] + " " + s3 + "\n")
            outfile.write("e " + lineSegments[1] + " " + lineSegments[4] + " " + s2 + "\n")
        if last_repo == True: outfile.write("t # -1")
        print("Done!")

if __name__ == '__main__':
    relationships_path = "./test/chrisbanes_cheesesquare/"
    inputfile = os.path.join(relationships_path, "relationships.txt")
    last_repo = True
    i = 0
    if not os.path.exists(relationships_path):
        os.makedirs(relationships_path)
    outputfile = "./test/graphs_of_projects.txt"
    if os.path.exists(inputfile):
        create_gspan_input(inputfile, outputfile, i, last_repo)
    else:
        print("Relationships of this project have not been extracted yet!")