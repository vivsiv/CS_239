import os
import sys

directory_in = sys.argv[1]
directory_out = sys.argv[2]
for csv_file in os.listdir(directory_in):
	if csv_file.endswith(".csv"):
		print ("Plotting csv file " + csv_file)

		script_call = "Rscript vis.r " + directory_in + "/" + csv_file + " " + directory_out

		os.system(script_call)