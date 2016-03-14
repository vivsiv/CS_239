import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.lang.Class;
import java.lang.reflect.Method;
import java.lang.annotation.Annotation;

// JUnit
import org.junit.runner.JUnitCore;

public class ExtractTestCaseName {
	public static String rootPath;

    public static void main(String... args) throws IOException, ClassNotFoundException {
    	System.out.println("Start test case extraction...");

    	rootPath = args[0];

    	walkDirectoryStructure(rootPath);

        System.exit(0);
    }

	public static void walkDirectoryStructure(String sourcePath) throws IOException, ClassNotFoundException {
		File sourceFile = new File(sourcePath);

		// Walk through all files and sub-directories in the source file path
		for (File file: sourceFile.listFiles()) {
			String nextLevelPath = "\\" + file.getName();
			
			// If the file visited is a directory, go into that directory.
			if (file.isDirectory()) {
				walkDirectoryStructure(sourcePath + nextLevelPath);
			// If the file visited is a *.java
			} else {
				if (file.getName().endsWith((".java")) && file.getName().contains("Test")) {
					extractTestCaseName(sourcePath, file.getName());
				}
			} // If
		} // For
	}

	public static void extractTestCaseName(String sourcePath, String fileName) throws IOException, ClassNotFoundException {
		String fileName_wo_ext = fileName.substring(0, fileName.lastIndexOf("."));

		File outputFile = new File(sourcePath + "\\" + fileName_wo_ext + "_" + "TestCases.txt");
		FileWriter fileWriter = new FileWriter(outputFile);

		String className = (sourcePath + "\\" + fileName_wo_ext).replace(rootPath + "\\", "").replace("\\", ".");
		System.out.println("Current class: " + className);

        // Go through all methods within the class
		for(Method method: Class.forName(className).getMethods()) {
		 	//System.out.println("Visiting method: " + method.getName());

		 	// Get all method annotation
			for (Annotation annotation: method.getAnnotations()) {
				//System.out.println("Visiting annotation: " + annotation.toString());

				// Check whether it is a Junit test case
				if (annotation.toString().contains("org.junit.Test")) {
					//System.out.println("Visiting method: " + method.getName());

					fileWriter.write(method.getName());
					fileWriter.write("\n");

			        break;
				} // If
			} // For
		} // For

		fileWriter.flush();
		fileWriter.close();
	}
}

