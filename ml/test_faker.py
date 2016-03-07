import os
import sys
import numpy as numpy
import csv
import pandas
import random

to_fake_file = sys.argv[1]
to_fake = pandas.read_csv(to_fake_file)
faked_file = to_fake_file.split(".")[0] + "_fake.csv"

with open(faked_file, 'w') as csvOutput:
    writer = csv.writer(csvOutput, delimiter=',', quotechar='"')

    with open(to_fake_file, 'r') as csvFile:
        reader = csv.reader(csvFile, delimiter=',', quotechar='"')

        
        for row in reader:
			rand = random.randint(1,100)
			if rand <= 30:
				row[-1] = "fail"
			else:
				row[-1] = "pass"
			writer.writerow(row)

