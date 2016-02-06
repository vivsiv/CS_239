num_tabs = 0
for line in open('out.txt', 'r'):
	if ('[Call  end ]' in line) or ('[Call begin]' in line):
		if ('[Call  end ]' in line):
			num_tabs -= 1

		line_string = ""
		for i in range(0,num_tabs):
			line_string += "\t"

		line_string += ": ".join(line.split("$$"))
		print line_string.rstrip()

		if ('[Call begin]' in line): 
			num_tabs += 1