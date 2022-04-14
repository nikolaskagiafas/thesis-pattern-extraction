package parser;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.File;

import parser.ClassObject.Abstraction;

public class MainWindow {

	/**
	 * Executes the application.
	 * 
	 * @param args optional arguments for executing in command line mode.
	 * @throws FileNotFoundException
	 */
	public static void main(String args[]) throws IOException {
		if (args.length < 1) {
			System.out.println("Please provide the path to a project folder, and "
							+ "(optionally) the flag includeUnknown in order to "
							+ "include relationships to unknown classes.");
			System.exit(0);
		}
		boolean includeUnknown = (args.length > 1);
		File project = new File(args[0]);

		// Extract relationships between classes of a project
		ProjectASTParser.parse(project, includeUnknown);
	}

	/**
	 * Converts the input string to the equivalent Connection Type
	 * 
	 * @param string String representing a Connection Type
	 * @return Returns a Connection Type after processing input String
	 */
	public static Connection.Type StringtoConnectionType(String string) {
		Connection.Type t;
		switch (string) {
		case "uses":
			t = Connection.Type.uses;
			break;
		case "inherits":
			t = Connection.Type.inherits;
			break;
		case "creates":
			t = Connection.Type.creates;
			break;
		// Either interface or abstract
		case "calls":
			t = Connection.Type.calls;
			break;
		case "references":
			t = Connection.Type.references;
			break;
		case "has":
			t = Connection.Type.has;
			break;
		default:
			t = null;
		}
		return t;
	}

	/**
	 * Converts the input string to the equivalent Abstraction Type
	 * 
	 * @param string String representing an Abstraction Type
	 * @return Returns an Abstraction Type after processing the input String
	 */
	public static Abstraction StringtoAbstraction(String string) {
		Abstraction abs;
		switch (string) {
		case "Normal":
			abs = Abstraction.Normal;
			break;
		case "Interface":
			abs = Abstraction.Interface;
			break;
		case "Abstract":
			abs = Abstraction.Abstract;
			break;
		// Either interface or abstract
		case "Abstracted":
			abs = Abstraction.Abstracted;
			break;
		case "Any":
			abs = Abstraction.Any;
			break;
		default:
			abs = null;
		}
		return abs;
	}

}
