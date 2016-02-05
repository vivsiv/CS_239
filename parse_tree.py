# class Node:
# 	def __init__(self,name,num_calls,parent,children):
# 		self.name = name
# 		self.num_calls = num_calls
# 		self.children = children

# 	def add_child(child):
# 		self.children.append(child)

# 	def addNode(name):
# 		for node in children:
# 		self.root = node


# f = open('out.text','r')
# text = f.readline()
# tree = 
num_tabs = 0
for line in open('out.txt', 'r'):
	if ('[Call end]' in line):
		num_tabs -= 1
		
	line_string = ""
	for i in range(0,num_tabs):
		line_string += "\t"

	line_string += line
	print line_string

	if ('[Call begin]' in line): 
		num_tabs += 1
	

	# line_string = ""
	# for i in range(0,num_tabs):
	# 	line_string += "\t"

	# line_string += line
	# print line_string