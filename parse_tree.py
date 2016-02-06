import sys
class Node:
	def __init__(self,name,num_calls,parent,children,start_time,avg_ex_time):
		self.name = name
		self.num_calls = num_calls
		self.parent = parent
		self.children = children
		self.start_time = start_time
		self.avg_ex_time = avg_ex_time

	def add_child(self,child):
		self.children.append(child)

	def node_string(self,level):
		return "<L" + str(level) + ">: (" + str(self.num_calls) + "x) " + self.name + " (" + str(self.avg_ex_time_ms()) + " ms) "

	def has_child(self,node_name):
		for child in self.children:
			if child.name == node_name:
				return child
		return None

	def update_ex_time(self,new_time):
		total_ex_time = (self.avg_ex_time * (self.num_calls - 1)) + new_time
		self.avg_ex_time = total_ex_time / self.num_calls

	def avg_ex_time_ms(self):
		return self.avg_ex_time / 1000.0

def has_root(node_name,root_arr):
	for r in root_arr:
		if node_name == r.name:
			return r
	return None

print "Building Tree..."
roots = []
root = None
level = 0
for line in open(sys.argv[1], 'r'):
	if "[Call begin]" in line:
		print_str = ""
		for i in range (0,level):
			print_str += "\t"
		if root:
			name = (line.split("$$")[2]).rstrip()
			prev_child = root.has_child(name)
			if prev_child != None:
				prev_child.num_calls += 1
				print_str += "<" + str(level) + ">: (" + str(prev_child.num_calls) + ")" + prev_child.name + " Parent: " + prev_child.parent.name
				root = prev_child
			else:
				child = Node(name,1,root,[],0,0)
				root.add_child(child)
				print_str += "<" + str(level) + ">: (" + str(child.num_calls) + ")" + child.name + " Parent: " + child.parent.name
				root = child
			#print print_str
			
		else:
			name = (line.split("$$")[2]).rstrip()
			prev_root = has_root(name, roots)
			if prev_root != None:
				prev_root.num_calls += 1
				print_str = "<" + str(level) + ">: (" + str(prev_root.num_calls) + ")" + prev_root.name
				root = prev_root
			else:
				root = Node(name,1,None,[],0,0)
				roots.append(root)
				print_str = "<" + str(level) + ">: (" + str(root.num_calls) + ")" + root.name
			#print print_str
		root.start_time = float((line.split("$$")[1]).rstrip())
		level += 1
	elif "[Call  end ]" in line :
		end_time = float((line.split("$$")[1]).rstrip())
		new_ex_time = end_time - root.start_time
		root.update_ex_time(new_ex_time)
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
	print_str += node.node_string(level)
	print print_str
	for child in node.children:
		dfs(child, level+1)

print "Parsing Tree..."
for node in roots:
	dfs(node,0)
print "Tree Parsed"


