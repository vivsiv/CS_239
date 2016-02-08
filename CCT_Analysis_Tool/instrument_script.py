import os
import sys


# os.system('rm inst/inst_out.txt')

# Compile the ASM_Example class
os.system('javac -cp asm-all-5.0.4.jar ASM_Instrument_Tool.java')

u_inst_dir = sys.argv[1]
for u_inst_file in os.listdir(u_inst_dir):
	javac_call = 'javac ' + u_inst_dir + '/' + u_inst_file
	os.system(javac_call)

inst_dir = sys.argv[2]
inst_call = 'java -cp .:asm-all-5.0.4.jar ASM_Instrument_Tool'
inst_call += ' ' + u_inst_dir
inst_call += ' ' + inst_dir
os.system(inst_call)

# Run the newly generated myClass class
for inst_file in os.listdir(inst_dir):
	if inst_file.endswith(".class"):
		file_name = inst_file.split(".")[0]
		out_file_name = file_name + "_out.txt"
		output_call = 'java -cp ' + inst_dir + ' ' + file_name + '> ' + inst_dir + '/' + out_file_name 
		os.system(output_call)

# Remove all class files
os.system('rm *.class')
os.system('rm ' + u_inst_dir + '/*.class')
os.system('rm ' + inst_dir + '/*.class')