def pattern_viz(input_file, output_file, draw_design_patterns):
    
    # the serial number of a frequent subgraph
    gph_serial_number = 0
    
    # the serial number of a node of a frequent subgraph
    node_serial_number = 0
    
    # the serial number of a node of a specific frequent subgraph
    spec_serial_number = 0
    
    # the abstraction level of a node as an integer
    node_label_int = 0
    
    # the abstraction level of a node as a string
    node_label_str = ""
    
    # the type of relationship that is described by the current edge
    edge_label_str = ""
    
    # the dictionary about the serial number of a class node in a frequent subgraph
    class_dictionary = {"1": "A", "2": "B", "3": "C", "4": "D", "5": "E", "6": "F", "7": "G", "8": "H", "9": "I", "10": "J", "11": "K", "12": "L", "13": "M", "14": "N", "15": "O", "16": "P", "17": "Q", "18": "R", "19": "S", "20": "T", "21": "U", "22": "V", "23": "W", "24": "X", "25": "Y", "26": "Z"}
    
    # the dictionary about the type of relationship that is described by an edge
    if draw_design_patterns:
        relationship_dictionary = {"2": "inherits", "3": "uses", "4": "calls", "5": "creates", "6": "has", "7": "references"}
    else:
        relationship_dictionary = {"2": " - inherits", "3": " - uses", "4": " - calls", "5": " - creates", "6": " - has", "7": " - references", "8": " + inherits", "9": " + uses", "10": " + calls", "11": " + creates", "12": " + has", "13": " + references"}
    
    # the dictionary about the type of arrow that corresponds to a specific relationship
    arrowtail_dictionary = {"2": "empty", "3": "vee", "4": "vee", "5": "diamond", "6": "odiamond", "7": "vee", "8": "empty", "9": "vee", "10": "vee", "11": "diamond", "12": "odiamond", "13": "vee"}
    
    
    with open(input_file, 'r+') as infile:
        input_lines = infile.readlines()
    
    with open(output_file, 'w+') as outfile:
        outfile.write("digraph G {\n\n")
        # the arrows will be orthogonal
        outfile.write("splines=ortho\n")
        # the node has the appropriate shape, which is similar to the one that is used in uml diagrams
        outfile.write("node[shape=record,style=filled,fillcolor=gray95]\n")
        # backward direction of arrows in edges
        outfile.write("edge[dir=back, arrowtail=empty]\n\n")
        for line in input_lines:
            if line.startswith("t #"):
                gph_serial_number += 1
                spec_serial_number = 0
                outfile.write("subgraph cluster_" + str(gph_serial_number) + "{\n\n")
            elif line.startswith("v"):
                node_serial_number += 1
                spec_serial_number += 1
                node_label_int = int(line.split(' ')[2].split('\n')[0])
                if node_label_int == 2:
                    node_label_str = "Normal"
                else:
                    node_label_str = "Abstracted"
                outfile.write(str(node_serial_number) + r'[label = "{\"' + node_label_str + r'\"\nClass ' + class_dictionary[str(spec_serial_number)] + r'|...|...}"]' + "\n")
            elif line.startswith("e"):
                # the start node of the edge
                node_from = int(line.split(' ')[1])
                # the end node of the edge
                node_to = int(line.split(' ')[2])
                edge_label_str = line.split(' ')[3].split('\n')[0]
                if edge_label_str == "5" or edge_label_str == "6" or edge_label_str == "11" or edge_label_str == "12":
                    # put first the node at the start, because this will have the diamond
                    outfile.write(str(node_serial_number - spec_serial_number + node_from + 1) + '->' + str(node_serial_number - spec_serial_number + node_to + 1) + '[arrowtail=' + arrowtail_dictionary[edge_label_str] + ', label = "' + relationship_dictionary[edge_label_str] + '"]\n')
                elif edge_label_str == "3" or edge_label_str == "4" or edge_label_str == "9" or edge_label_str == "10":
                    # put first the node at the end, because this will have the arrow
                    outfile.write(str(node_serial_number - spec_serial_number + node_to + 1) + '->' + str(node_serial_number - spec_serial_number + node_from + 1) + '[arrowtail=' + arrowtail_dictionary[edge_label_str] + ', label = "' + relationship_dictionary[edge_label_str] + '", style=dashed]\n')
                else:
                    # put first the node at the end, because this will have the arrow
                    outfile.write(str(node_serial_number - spec_serial_number + node_to + 1) + '->' + str(node_serial_number - spec_serial_number + node_from + 1) + '[arrowtail=' + arrowtail_dictionary[edge_label_str] + ', label = "' + relationship_dictionary[edge_label_str] + '"]\n')
            elif line.startswith("Support:"):
                # this is the end of one of the frequent subgraphs
                outfile.write("}\n\n")
            else:
                pass
        outfile.write("}\n")
                
    
    
if __name__ == '__main__':
    
    # the file that includes the frequent subgraphs detected by gspan
    input_file = "C:/Users/nikos/OneDrive/Desktop/results/15_80_commits_ab_eq_int/diff_lines_8+_40-/s_13_l_5_commits/frequent_subgraphs.txt"
    # this file will be the input to the GraphViz tool
    output_file = "C:/Users/nikos/OneDrive/Desktop/results/15_80_commits_ab_eq_int/diff_lines_8+_40-/s_13_l_5_commits/evolution_patterns.txt"
    # if this variable is true, then visualize design patterns, else visualize evolution patterns
    draw_design_patterns = False
    
    pattern_viz(input_file, output_file, draw_design_patterns)