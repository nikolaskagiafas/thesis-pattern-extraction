import os

def create_graphviz_graphs(inputfile, outputfile):
    print("Creating graph from repo")
    with open(inputfile) as infile:
        relationships = [l.strip() for l in infile.readlines()]

    with open(outputfile, 'w') as outfile:
        outfile.write("digraph G {\n")
        s1 = ""
        s2 = ""
        s3 = ""
        for line in relationships:
            lineSegments = line.split();
            # Shape of the class node which corresponds to its abstraction level
            if lineSegments[0] == "Normal": s1 = "ellipse"
            elif lineSegments[0] == "Unknown": s1 = "box"
            elif lineSegments[0] == "Abstract": s1 = "diamond"
            elif lineSegments[0] == "Interface": s1 = "hexagon"
            elif lineSegments[0] == "Abstracted": s1 = "triangle"
            elif lineSegments[0] == "Any": s1 = "parallelogram"
            else: print("Something strange happened!")
    
            # Shape of the class node which corresponds to its abstraction level
            if lineSegments[3] == "Normal": s3 = "ellipse"
            elif lineSegments[3] == "Unknown": s3 = "box"
            elif lineSegments[3] == "Abstract": s3 = "diamond"
            elif lineSegments[3] == "Interface": s3 = "hexagon"
            elif lineSegments[3] == "Abstracted": s3 = "triangle"
            elif lineSegments[3] == "Any": s3 = "parallelogram"
            else: print("Something strange happened!")
    
            # Color of the edge between two class nodes which corresponds to the type of the relationship between them
            if lineSegments[2] == "inherits": s2 = "brown"
            elif lineSegments[2] == "uses": s2 = "black"
            elif lineSegments[2] == "calls": s2 = "blue"
            elif lineSegments[2] == "creates": s2 = "red"
            elif lineSegments[2] == "has": s2 = "green"
            elif lineSegments[2] == "references": s2 = "orange"
            else: print("Something strange happened!")
            outfile.write("\"" + lineSegments[1] + "\"" + " [shape = " + s1 + "];\n") 
            outfile.write("\"" + lineSegments[4] + "\"" + " [shape = " + s3 + "];\n")
            outfile.write("\"" + lineSegments[1] + "\"" + "->" + "\"" + lineSegments[4] + "\" [color = " + s2 + "];\n")
        outfile.write("}\n")
    print("Done!")

if __name__ == '__main__':
    relationships_path = "./test/chrisbanes_cheesesquare/"
    if not os.path.exists(relationships_path):
        os.makedirs(relationships_path)
    inputfile = os.path.join(relationships_path, "relationships.txt")
    outputfile = os.path.join(relationships_path, "relationships.dot")
    if os.path.exists(inputfile):
        create_graphviz_graphs(inputfile, outputfile)
    else:
        print("Relationships of this project have not been extracted yet!")
