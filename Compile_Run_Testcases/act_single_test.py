import os
import sys
import subprocess

targetSoftware = sys.argv[1]
codeMutation = True

# Specify the path for the porgram source and the program testbench
if targetSoftware == "jsoup":
	"""
	srcFilePath   = r"E:\Courses\Winter2016\CS239\PartA\Targets\jsoup_example\jsoup-master\src\main\java"
	testFilePath  = r"E:\Courses\Winter2016\CS239\PartA\Targets\jsoup_example\jsoup-master\src\test\java"
	instFilePath  = r"E:\Courses\Winter2016\CS239\PartA\Targets\jsoup_example\jsoup-instrumented\main"
	outputLogPath = r"E:\Courses\Winter2016\CS239\PartA\Targets\jsoup_example\jsoup-instrumented\logs"
	"""
	srcFilePath   = r"E:\Courses\Winter2016\CS239\PartA\Targets\jsoup_example\jsoup-mutated\jsoup-mutated-inst\java"
	testFilePath  = r"E:\Courses\Winter2016\CS239\PartA\Targets\jsoup_example\jsoup-mutated\jsoup-mutated\src\test\java"
	instFilePath  = r"E:\Courses\Winter2016\CS239\PartA\Targets\jsoup_example\jsoup-mutated\jsoup-mutated-inst\java"
	outputLogPath = r"E:\Courses\Winter2016\CS239\PartA\Targets\jsoup_example\jsoup-mutated\jsoup-mutated-inst\logs"
elif targetSoftware == "jline":
	#srcFilePath   = r"E:\Courses\Winter2016\CS239\PartA\Targets\jline2-example\jline2-master\jline2-master\src\main\java"
	#testFilePath  = r"E:\Courses\Winter2016\CS239\PartA\Targets\jline2-example\jline2-master\jline2-master\src\test\java"
	#instFilePath  = r"E:\Courses\Winter2016\CS239\PartA\Targets\jline2-example\jline2-master\jline2-instrumented\java"
	#outputLogPath = r"E:\Courses\Winter2016\CS239\PartA\Targets\jline2-example\jline2-master\jline2-instrumented\logs"
	srcFilePath   = r"E:\Courses\Winter2016\CS239\PartA\Targets\jline2-example\jline2-master-mutated\jline2-master-mutated-inst\main"
	testFilePath  = r"E:\Courses\Winter2016\CS239\PartA\Targets\jline2-example\jline2-master-mutated\jline2-master-mutated\src\test\java"
	instFilePath  = r"E:\Courses\Winter2016\CS239\PartA\Targets\jline2-example\jline2-master-mutated\jline2-master-mutated-inst\main"
	outputLogPath = r"E:\Courses\Winter2016\CS239\PartA\Targets\jline2-example\jline2-master-mutated\jline2-master-mutated-inst\logs"
elif targetSoftware == "jgap":
	srcFilePath   = r"E:\Courses\Winter2016\CS239\PartA\Targets\jgap_example\jgap-master\src"
	testFilePath  = r"E:\Courses\Winter2016\CS239\PartA\Targets\jgap_example\jgap-master\tests"
	instFilePath  = r"E:\Courses\Winter2016\CS239\PartA\Targets\jline2-example\jline2-master\jline2-instrumented\java"
	outputLogPath = r"E:\Courses\Winter2016\CS239\PartA\Targets\jline2-example\jline2-master\jline2-instrumented\logs"
else:
	print ("Unsupported target software!")
	sys.exit(1)

# Specify the jar library dependency
# srcFilePath is always added to.
jarLibraryList = None

if targetSoftware == "jsoup":
	jarLibraryList = [r".\lib\junit-4.12.jar", \
					  r".\lib\hamcrest-core-1.3.jar", \
					  r"E:\Courses\Winter2016\CS239\PartA\Targets\jsoup_example\jsoup-master\src\test\resources"]
elif targetSoftware == "jline":
	jarLibraryList = [r".\lib\asm-all-5.0.4.jar", \
					  r".\lib\junit-4.12.jar", \
					  r".\lib\hamcrest-core-1.3.jar", \
					  r".\lib\jansi-1.11.jar", \
					  r".\lib\easymock-3.4.jar", \
					  r".\lib\javassist-3.20.0-GA.jar", \
					  r".\lib\objenesis-2.2.jar", \
					  r".\lib\cglib-3.2.1.jar", \
					  r".\lib\powermock-core-1.6.4.jar", \
					  r".\lib\powermock-reflect-1.6.4.jar", \
					  r".\lib\powermock-api-easymock-1.6.4.jar", \
					  r".\lib\powermock-api-support-1.6.4.jar", \
					  r".\lib\powermock-module-junit4-1.6.4.jar", \
					  r".\lib\powermock-module-junit4-common-1.6.4.jar", \
					  r"E:\Courses\Winter2016\CS239\PartA\Targets\jline2-example\jline2-master\jline2-master\src\main\resources", \
					  r"E:\Courses\Winter2016\CS239\PartA\Targets\jline2-example\jline2-master\jline2-master\src\test\resources"]
elif targetSoftware == "jgap":
	jarLibraryList = [r".\lib\junit-4.12.jar", \
					  r".\lib\hamcrest-core-1.3.jar", \
					  r"E:\Courses\Winter2016\CS239\PartA\Targets\jgap_example\jgap-master\lib\appframework-1.0.3.jar", \
					  r"E:\Courses\Winter2016\CS239\PartA\Targets\jgap_example\jgap-master\lib\commons-codec-1.3.jar", \
					  r"E:\Courses\Winter2016\CS239\PartA\Targets\jgap_example\jgap-master\lib\commons-cli-1.2.jar", \
					  r"E:\Courses\Winter2016\CS239\PartA\Targets\jgap_example\jgap-master\lib\commons-lang-2.1.jar", \
					  r"E:\Courses\Winter2016\CS239\PartA\Targets\jgap_example\jgap-master\lib\commons-math-2.2.jar", \
					  r"E:\Courses\Winter2016\CS239\PartA\Targets\jgap_example\jgap-master\lib\trove-2.0.2.jar", \
					  r"E:\Courses\Winter2016\CS239\PartA\Targets\jgap_example\jgap-master\lib\jcgrid.jar", \
					  r"E:\Courses\Winter2016\CS239\PartA\Targets\jgap_example\jgap-master\lib\jcommon-1.0.14.jar", \
					  r"E:\Courses\Winter2016\CS239\PartA\Targets\jgap_example\jgap-master\lib\log4j.jar", \
					  r"E:\Courses\Winter2016\CS239\PartA\Targets\jgap_example\jgap-master\lib\xstream-1.3.1.jar"]

# Enable mutation test
if codeMutation:
	jarLibraryList += [r".\lib\config.jar"]

# Generate a list of folders where files are needed to be compiled
#compPathList = [srcFilePath, testFilePath]
compPathList = [instFilePath, testFilePath]

# Generate JAR library arguements to be passed to Java bytecode compiler
jarLibraryArg = ""

for jar in jarLibraryList:
	jarLibraryArg += (jar + ";")

for tarFilePath in compPathList:
	jarLibraryArg += (tarFilePath + ";")
"""
# Find out all *.java file and compile it to *.class
for tarFilePath in compPathList:
	for path, subdirs, files in os.walk(tarFilePath):
		for filename in files:
			f = os.path.join(path, filename)

			# Ignore directory and non-java files
			if f.endswith(".java"):
				print ("Compiling: " + f)

				compileCmd = r"javac -encoding UTF-8 -cp " + jarLibraryArg + " " + f
				#compileCmd = r"javac -cp " + jarLibraryArg + " " + f
				proc_ret = subprocess.call(compileCmd)

				#print ("Compiling cmd: " + compileCmd)

				# print out generated logs
				#for line in proc.stdout:
				#	print (line)
				#output = proc.stdout.read()
				#print (output)
				#print (proc_ret)
"""

# Check the existence of output directory first
if not os.path.exists(outputLogPath):
	os.makedirs(outputLogPath)

# Find out all test file and run it with JUnit
for path, subdirs, files in os.walk(testFilePath):
	for filename in files:
		file = os.path.join(path, filename)

		# Run only test cases
		if file.endswith("Test.class"):
			# Extract test file name
			testFileName = file.replace(testFilePath + "\\", "")
			testFileName = testFileName.replace(".class", "")
			testFileName = testFileName.replace("\\", ".")

			testCaseListFile = file.replace(".class", "")
			testCaseListFile = testCaseListFile + "_TestCases.txt"
			with open(testCaseListFile) as testCaseList:
				for line in testCaseList.readlines():
					testCaseName = line.rstrip()
					print ("Running JUnit test: " + testFileName + "#" + testCaseName)

					testCmd = r"java -cp " + jarLibraryArg + " SingleJUnitTestRunner " + testFileName + " " + testCaseName
					logFile = open(outputLogPath + "\\" + testFileName + "#" + testCaseName + ".txt", 'wb')
					
					print ("Test cmd: " + testCmd)

					proc = subprocess.Popen(testCmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

					# write generated logs to file
					#for line in proc.stdout.read():
					#	logFile.write(line)

					(outs, errs) = proc.communicate()
					logFile.write(outs)

					logFile.close()


