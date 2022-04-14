# thesis-pattern-extraction
Diploma thesis for extracting design and evolution patterns.

# Abstract
Close collaboration between software developers is considered essential in order to build innovative software projects. For this reason, there are several online program-hosting platforms, which enable their users to watch each other’s changes, recommendations and comments towards the improvement and evolution of code. These platforms also control different versions of the software code so that the developer can revert to previous ones if desired. All the modifications performed at a given time by a member of the software development team are bundled in a commit, where the main reasons behind them are also recorded. As a consequence, it goes without saying that these series of changes include a lot of useful information about the way a software project evolves.
	Applying data mining techniques on public software repositories and the data we discussed above could unveil some common bug fixes, systematic edits, frequent types of changes in a project’s architecture and frequently-used design patterns either known or unknown ones. An extensive bibliographic research in this domain reveals that the majority of scientific efforts has focused on bug fixes and systematic edits ignoring some more coarse-grained (high-level) code evolution or design patterns. In this context, this dissertation tries to extract the relationships between the classes of an object-oriented program, while also seeking to monitor the way they evolve over time.
	To achieve these goals, this diploma thesis adapts a Relationship Extractor tool based on the Abstract Syntax Trees analysis of some of the most popular software projects in Github web platform. After analyzing and processing those syntax trees, useful information is extracted concerning the operation, the abstraction level as well as the inheritance of classes. This information is then modeled as graphs (with classes as nodes and the connections between them as edges). These steps are not only executed for the latest version of a project, but also in each and every commit with a view to extracting the difference in relationships between the versions of a project before and after the specific commit. Finally, gSpan, which is a frequent-subgraph mining algorithm, is applied, in order to detect code design and evolution patterns used by the software community worldwide.

# Compiling
Before executing the code, one has to compile the Relationship Extractor, which is written in Java. To do so, open the folder RelationshipExtractor and follow the instructions on that readme (use maven to compile with the command `mvn install`).

# Setting properties
Set the properties at the file properties.py. Instructions:
- `GIT_PATH`: the path to the git executable, e.g. `"C:/Program Files/Git/bin/git.exe"`
- `JAVA_PATH`: the path to the Java executable, e.g. `"C:/Program Files/Java/jdk-15.0.1/bin/java.exe"`
- `REL_EXTRACTOR_PATH`: the path to the RelationshipExtractor, in most cases leave this to `"./RelationshipExtractor/target/RelationshipExtractor-0.1.jar"`
- `REPOS_FILE`: the path to the txt file containing the repos, e.g. `"./repos3000Java.txt"`
- `DATA_PATH`: the path where the data is downloaded, e.g. `"./data/"`

# Executing
Executing the file main.py performs the following actions:
- The repos of the `REPOS_FILE` are cloned to the `DATA_PATH`
- The relationships of each cloned repo are extracted.
- The relationships are parsed and a Graphviz-formatted file is produced for each repo.
- A gspan-formatted file is produced for each repo from the parsed relationships.
- The evolving relationships for each repo are tracked
- A gspan-formatted file is produced for each commit from the evolving relationships.

Now, files graphs_of_commits.txt and graphs_of_projects.txt is ready to be used as input to gspan. The python release of this algorithm is used: https://github.com/betterenvi/gSpan.

By executing the file project_graph_selector.py, projects, whose number of relationships is between two specific values, are selected.

By executing the file commit_selector.py, commits, whose overall number of added and deleted relationships is between two specific values, are selected.

# Testing
The files repository_cloner, relationship_extractor, graph_creator, evolution, graphs_of_projects and graphs_of_commits can also function individually for testing purposes. In order to run a test, one can execute the main functions that are inside these files.

# Final Results
The "results" folder keeps the final results of all the experiments conducted. 
The symbol "s" corresponds to the minimum support that was given as input in the gspan algorithm. 
The symbol "l" corresponds to the minimum number of nodes for the frequent subgraphs extracted by gspan.
"ab_eq_int" means we assume that the abstraction levels "Abstract" and "Interface" are identical.
