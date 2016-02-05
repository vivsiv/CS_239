class Node:
	def __init__(self,name,num_calls,parent,children):
		self.name = name
		self.num_calls = num_calls
		self.parent = parent
		self.children = children

	def add_child(self,child):
		self.children.append(child)

	def node_string(self):
		ns = "<Node>:" + self.name + " calls:" + str(self.num_calls)
		if self.parent:
			ns += (" parent:" + self.parent.name)
		return ns

	# def addNode(name):
	# 	for node in children:
	# 	self.root = node


root = None
level = 0
for line in open('out.txt', 'r'):
	if "[Call begin]" in line:
		print_str = ""
		for i in range (0,level):
			print_str += "\t"
		if root:
			name = (line.split("$$")[1]).rstrip()
			child = Node(name,1,root,[])
			root.add_child(child)
			print_str += "<" + str(level) + ">: " + child.name + " num_calls: " + str(child.num_calls) + " Parent: " + child.parent.name
			print print_str
			root = child
		else:
			name = (line.split("$$")[1]).rstrip()
			root = Node(name,1,None,[])
			print_str = "<" + str(level) + ">:" + root.name + " num_calls: " + str(root.num_calls)
			print print_str
		level += 1
	else :
		#print "<Leave>:" + root.name + " num_calls: " + str(root.num_calls)
		root = root.parent
		level -= 1


# num_tabs = 0
# for line in open('out.txt', 'r'):
# 	if ('[Call end]' in line):
# 		num_tabs -= 1

# 	line_string = ""
# 	for i in range(0,num_tabs):
# 		line_string += "\t"

# 	line_string += line.split("$$")[1]
# 	print line_string.rstrip()

# 	if ('[Call begin]' in line): 
# 		num_tabs += 1