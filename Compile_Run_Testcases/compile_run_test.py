import os
import sys
import subprocess

# Specify the path for the porgram source and the program testbench
srcFilePath  = r"E:\Courses\Winter2016\CS239\PartA\Targets\jsoup_example\jsoup-instrumented\main";
testFilePath = r"E:\Courses\Winter2016\CS239\PartA\Targets\jsoup_example\jsoup-instrumented\test";

# Find out all *.java file and compile it to *.class
for path, subdirs, files in os.walk(testFilePath):
	for filename in files:
		f = os.path.join(path, filename)

		# Ignore directory and non-java files
		if f.endswith(".java"):
			print ("Compiling: " + f)
			
			compileCmd = r"javac -encoding UTF-8 -cp .\lib\junit-4.12.jar;.\lib\hamcrest-core-1.3.jar;" \
						+ srcFilePath + ";" + testFilePath + " " + f
			subprocess.run(compileCmd)

# Find out all test file and run it with JUnit
for path, subdirs, files in os.walk(testFilePath):
	for filename in files:
		f = os.path.join(path, filename)

		# Run only test cases
		if f.endswith("Test.class"):
			# Extract test case names
			testCaseName = f.replace(testFilePath + "\\", "")
			testCaseName = testCaseName.replace(".class", "")
			testCaseName = testCaseName.replace("\\", ".")

			print ("Running test: " + testCaseName)

			testCmd = r"java -cp .\lib\junit-4.12.jar;.\lib\hamcrest-core-1.3.jar;" \
						+ srcFilePath + ";" + testFilePath + " org.junit.runner.JUnitCore " \
						+ testCaseName

			logFile = open(".\\logs\\" + testCaseName + ".txt", 'wb')
			
			proc = subprocess.Popen(testCmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			proc_output, _ =  proc.communicate()

			logFile.write(proc_output)
			logFile.close()