import os
os.system('rm inst/out.txt')

# Compile the ASM_Example class
os.system('javac -cp asm-all-5.0.4.jar ASM_Instrument_Tool.java')

os.system('javac u_inst/FbClass.java')
os.system('javac u_inst/SortingAlgorithms.java')

os.system('java -cp .:asm-all-5.0.4.jar ASM_Instrument_Tool u_inst inst')
		
# Run the newly generated myClass class
os.system('touch inst/out.txt')
#os.system('java -cp inst myClass > inst/out.txt')
os.system('java -cp inst SortingAlgorithms > out.txt')
# Remove all class files
os.system('rm *.class')
os.system('rm u_inst/*.class')
os.system('rm inst/*.class')

os.system('python generate_call_stack.py inst/out.txt > inst/sort_calls.txt')
os.system('python parse_tree.py inst/out.txt > inst/sort_tree.txt')





