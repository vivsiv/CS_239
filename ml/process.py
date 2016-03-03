import os
import sys
# from pyspark import SparkContext, SQLContext
import numpy as numpy
import csv
import pandas

# sc = SparkContext(appName="testProcessing")
# sqlc = SQLContext(sc)

test_dir = sys.argv[1]
csv_out_headers = ["test_name","longest_1","longest_2","longest_3","longest_4","longest_5","pass/fail"]
out_data = pandas.DataFrame(columns=csv_out_headers)

for test_file in os.listdir(test_dir):
	if test_file.endswith(".csv"):
		test_file = test_dir + "/" + test_file
		test_data = pandas.read_csv(test_file)
		test_data["Total_Execution_Time"] = test_data["Avg_Execution_Time"] * test_data["Num_Calls"]
		longest_methods = test_data.sort(["Total_Execution_Time"],ascending=False)[0:5]["Total_Execution_Time"]
		longest_methods.index = csv_out_headers[1:-1]
		longest_methods["test_name"] = test_file.split(".")[0]
		longest_methods["pass/fail"] = "pass"
		print longest_methods
		out_data = out_data.append(longest_methods)

print out_data
out_dir = sys.argv[2]
out_data.to_csv(out_dir + "/" + "test_out.csv")






