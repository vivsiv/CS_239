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

	def has_child(self,node_name):
		for child in self.children:
			if child.name == node_name:
				return child
		return None

	# def addNode(name):
	# 	for node in children:
	# 	self.root = node

print "Building Tree..."
roots = []
root = None
level = 0
for line in open('out.txt', 'r'):
	if "[Call begin]" in line:
		print_str = ""
		for i in range (0,level):
			print_str += "\t"
		if root:
			name = (line.split("$$")[1]).rstrip()
			prev_child = root.has_child(name)
			if prev_child != None:
				prev_child.num_calls += 1
				print_str += "<" + str(level) + ">: (" + str(prev_child.num_calls) + ")" + prev_child.name + " Parent: " + prev_child.parent.name
				root = prev_child
			else:
				child = Node(name,1,root,[])
				root.add_child(child)
				print_str += "<" + str(level) + ">: (" + str(child.num_calls) + ")" + child.name + " Parent: " + child.parent.name
				root = child
			print print_str
			
		else:
			name = (line.split("$$")[1]).rstrip()
			root = Node(name,1,None,[])
			roots.append(root)
			print_str = "<" + str(level) + ">: (" + str(root.num_calls) + ")" + root.name
			print print_str
		level += 1
	else :
		#print "<Leave>:" + root.name + " num_calls: " + str(root.num_calls)
		root = root.parent
		level -= 1
print "Tree Built!"
print ""

print "Tree Roots"
for r in roots:
	print r.name
print ""

def dfs(node, level):
	if node == None:
		return
 	print_str = ""
	for i in range (0,level):
		print_str += "\t"
	print_str += "<" + str(level) + ">: (" + str(node.num_calls) + ")" + node.name
	print print_str
	for child in node.children:
		dfs(child, level+1)

print "Parsing Tree..."
for node in roots:
	dfs(node,0)
print "Tree Parsed"


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