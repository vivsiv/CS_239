import os
import sys

directory_in = sys.argv[1]
directory_out = sys.argv[2]
for log_file in os.listdir(directory_in):
	if log_file.endswith(".txt"):
		print ("Processing file " + log_file)

		script_call = "python parse_tree.py " + directory_in + "/" + log_file + " "
		script_call += (directory_out + "/" + log_file + ".csv")

		os.system(script_call)