package parser;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintStream;

public class GraphVisualization {
	
	/**
	 * Function to create files suitable for GraphViz tool.
	 * 
	 * @param projectName defines the name of the project whose relationships are to be visualized
	 * @throws FileNotFoundException 
	 */
    public static void graphVizFormat(String projectName) throws FileNotFoundException {
    	
	// Create a file which will save relationships between classes of the project in graphviz format
    	File graphKnown = new File(".\\extracted_relationships\\" + projectName + "\\graphKnown.txt");
	    
	// Create a file which will save relationships between classes of the project and imported ones in graphviz format
    	File graphUnknown = new File(".\\extracted_relationships\\" + projectName + "\\graphUnknown.txt");
    	
	// Initialize the appropriate stream objects for data transfer in the previous files
    	PrintStream knownStream = new PrintStream(graphKnown);
    	PrintStream unknownStream = new PrintStream(graphUnknown);
    	
	// Define BufferedReader objects which will read data from extracted relationships
    	BufferedReader knownReader, unknownReader;
    	
    	try {
    		knownReader = new BufferedReader(new FileReader(".\\extracted_relationships\\" + projectName + "\\known_relationships.txt"));
		// Call the function that is going to create the appropriate graphviz format
    		formatToFile(knownReader, knownStream);
		// Close the first reader
    		knownReader.close();
    	}catch(IOException e) {
    		e.printStackTrace();
    	}
    	
	// Close knownStream
    	knownStream.close();
    	
    	try {
    		unknownReader = new BufferedReader(new FileReader(".\\extracted_relationships\\" + projectName + "\\unknown_relationships.txt"));
		// Call the function that is going to create the appropriate graphviz format
    		formatToFile(unknownReader, unknownStream);
		// Close the second reader
    		unknownReader.close();
    	}catch(IOException e) {
    		e.printStackTrace();
    	}
    	
	// Close unknownStream
    	unknownStream.close();
    }
    
	/**
	* Function to create format suitable for graphViz tool
	*
	* @param reader defines the BufferedReader object which will read data from extracted relationships
	* @param stream defines the PrintStream object for printing new format type to the right file.
	* @throws IOException
	*/
    public static void formatToFile(BufferedReader reader, PrintStream stream) throws IOException {
    	
	// Store the shape of the class node which corresponds to its abstraction level
    	String s1 = null;
	// Store the color of the edge between two class nodes which corresponds to the type of the relationship between them
    	String s2 = null;
	// Store the shape of the class node which corresponds to its abstraction level
    	String s3 = null;
    	String line = reader.readLine();
    	System.setOut(stream);
    	String[] lineSegments;
    	while (line != null) {
			lineSegments = line.split(" ", 5);
			if (lineSegments[0].equals("Normal")) {
				s1 = "ellipse";
			}else if (lineSegments[0].equals("Unknown")) {
				s1 = "box";
			}else if (lineSegments[0].equals("Abstract")) {
				s1 = "diamond";
			}else if (lineSegments[0].equals("Interface")) {
				s1 = "hexagon";
			}else if (lineSegments[0].equals("Abstracted")) {
				s1 = "triangle";
			}else if (lineSegments[0].equals("Any")) {
				s1 = "parallelogram";
			}else {
				System.err.println("Something strange happened!");
			}
			if (lineSegments[3].equals("Normal")) {
				s3 = "ellipse";
			}else if (lineSegments[3].equals("Unknown")) {
				s3 = "box";
			}else if (lineSegments[3].equals("Abstract")) {
				s3 = "diamond";
			}else if (lineSegments[3].equals("Interface")) {
				s3 = "hexagon";
			}else if (lineSegments[3].equals("Abstracted")) {
				s3 = "triangle";
			}else if (lineSegments[3].equals("Any")) {
				s3 = "parallelogram";
			}else {
				System.err.println("Something strange happened!");
			}
			if (lineSegments[2].equals("inherits")) {
				s2 = "brown";
			}else if (lineSegments[2].equals("uses")) {
				s2 = "black";
			}else if (lineSegments[2].equals("calls")) {
				s2 = "blue";
			}else if (lineSegments[2].equals("creates")) {
				s2 = "red";
			}else if (lineSegments[2].equals("has")) {
				s2 = "green";
			}else if (lineSegments[2].equals("references")) {
				s2 = "orange";
			}else {
				System.err.println("Something strange happened!");
			}
			System.out.println("\"" + lineSegments[1] + "\"" + " [shape = " + s1 + "];"); 
			System.out.println("\"" + lineSegments[4] + "\"" + " [shape = " + s3 + "];");
			System.out.println("\"" + lineSegments[1] + "\"" + "->" + "\"" + lineSegments[4] + "\" [color = " + s2 + "];");
			line = reader.readLine();
    	}
    }
    
        /**
	* Function to create data format suitable for gspan algorithm
	*
	* @param reader defines the BufferedReader object which will read data of the input projects
	* @param i defines the serial order of the specific project, starting from zero
	* @throws IOException
	*/
    public static void formatToDataFile(BufferedReader reader, int i) throws IOException {
    	
	// Store a number between 1 and 6 indicating the abstraction level of the specific class
    	String s1 = null;
	// Store a number between 1 and 6 indicating the type of the relationship between two connected classes
    	String s2 = null;
	// Store a number between 1 and 6 indicating the abstraction level of the specific class
    	String s3 = null;
    	String line = reader.readLine();
    	String[] lineSegments;
    	System.out.println("t # " + i);
    	while (line != null) {
			lineSegments = line.split(" ", 5);
			if (lineSegments[0].equals("Normal")) {
				s1 = "1";
			}else if (lineSegments[0].equals("Unknown")) {
				s1 = "2";
			}else if (lineSegments[0].equals("Abstract")) {
				s1 = "3";
			}else if (lineSegments[0].equals("Interface")) {
				s1 = "4";
			}else if (lineSegments[0].equals("Abstracted")) {
				s1 = "5";
			}else if (lineSegments[0].equals("Any")) {
				s1 = "6";
			}else {
				System.err.println("Something strange happened!");
			}
			if (lineSegments[3].equals("Normal")) {
				s3 = "1";
			}else if (lineSegments[3].equals("Unknown")) {
				s3 = "2";
			}else if (lineSegments[3].equals("Abstract")) {
				s3 = "3";
			}else if (lineSegments[3].equals("Interface")) {
				s3 = "4";
			}else if (lineSegments[3].equals("Abstracted")) {
				s3 = "5";
			}else if (lineSegments[3].equals("Any")) {
				s3 = "6";
			}else {
				System.err.println("Something strange happened!");
			}
			if (lineSegments[2].equals("inherits")) {
				s2 = "1";
			}else if (lineSegments[2].equals("uses")) {
				s2 = "2";
			}else if (lineSegments[2].equals("calls")) {
				s2 = "3";
			}else if (lineSegments[2].equals("creates")) {
				s2 = "4";
			}else if (lineSegments[2].equals("has")) {
				s2 = "5";
			}else if (lineSegments[2].equals("references")) {
				s2 = "6";
			}else {
				System.err.println("Something strange happened!");
			}
			System.out.println("v " + lineSegments[1] + " " + s1); 
			System.out.println("v " + lineSegments[4] + " " + s3);
			System.out.println("e " + lineSegments[1] + " " + lineSegments[4] + " " + s2);
			line = reader.readLine();
    	}    	
    }
}
