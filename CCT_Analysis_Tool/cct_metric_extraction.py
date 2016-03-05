import sys
import os
import csv
import re

# define Node class
class Node:
	def __init__(self, parent_node, thread_id, start_time, method_name):
		self.parent_node = parent_node;
		self.method_name = method_name
		self.thread_id = thread_id
		self.start_time = start_time
		self.exe_time = list()
		self.avg_exe_time = 0
		self.child_node = list()
		self.call_count = 1

	def has_child(self, method_name):
		for child in self.child_node:
			if child.method_name == method_name:
				return child
		return None

# extract interested information from the CCT. (DFS)
def Extract_CCT(node, level, method_count, method_depth, method_breadth):
	#print ("Current node: " + node.method_name)

	# increment the global method counter
	if node.method_name not in method_count:
		method_count[node.method_name] = node.call_count
	else:
		method_count[node.method_name] += node.call_count

	# count how many children a node has
	if node.method_name not in method_breadth:
		method_breadth[node.method_name] = len(node.child_node)
	else:
		# only update the global breadth dict. when the child node number is larger
		if method_breadth[node.method_name] <= len(node.child_node):
			method_breadth[node.method_name] = len(node.child_node)

	# if there is no more child node (leaf node is reached)
	if not node.child_node:
		if node.method_name not in method_depth:
			method_depth[node.method_name] = level
		else:
			# only update the global depth dict. when the current call level is deeper
			if method_depth[node.method_name] <= level:
				method_depth[node.method_name] = level

		# return to its parent node
		return
	# if a child node exists
	else:
		# iterate through each child node
		for child in node.child_node:
			Extract_CCT(child, level+1, method_count, method_depth, method_breadth)

# open up the output files first
output_time_file    = open(sys.argv[2] + r"\metric_time.csv", 'w')
output_count_file  = open(sys.argv[2] + r"\metric_count.csv", 'w')
output_depth_file   = open(sys.argv[2] + r"\metric_depth.csv", 'w')
output_breadth_file = open(sys.argv[2] + r"\metric_breadth.csv", 'w')

# prepare csv writers
csv_time_writer    = csv.writer(output_time_file, delimiter=',', lineterminator='\n')
csv_count_writer  = csv.writer(output_count_file, delimiter=',', lineterminator='\n')
csv_depth_writer   = csv.writer(output_depth_file, delimiter=',', lineterminator='\n')
csv_breadth_writer = csv.writer(output_breadth_file, delimiter=',', lineterminator='\n')

# find out all test file and run it with JUnit
for path, subdirs, files in os.walk(sys.argv[1]):
	for filename in files:
		file = os.path.join(path, filename)

		print ("[INFO] Building CCT from the log file: " + file)

		# initialize parser variables
		root_nodes = dict() # <k,v>=<thread_id, node>: store the root node with different thread_id
		resume_node = dict() # <k,v>=<thread_id, node>: store the node whether the parser should resume to when the next node comes in.
		num_of_node = 0
		num_of_call = 0
		test_result = None
		test_result_count = [0, 0]
		method_count = dict()
		method_time = dict()
		method_depth = dict()
		method_breadth = dict()

		# parse the log line by line
		with open(file, 'r') as log_file:
			for line in log_file:
				# the method call is invoked
				if "[Call begin]" in line:
					# Extract calling context information from the log
					thread_id = (line.split("$$")[1])
					start_time = float(line.split("$$")[2])
					method_name = (line.split("$$")[3]).rstrip()
					#print ("Current node: " + thread_id + ", " + start_time + ", " + method_name)

					# increment the global method call counter
					num_of_call += 1

					"""
					# increment the global method counter
					if method_name not in method_count:
						method_count[method_name] = 1
					else:
						method_count[method_name] += 1
					"""

					# if there is no root node for this thread_id in the dict.
					if thread_id not in root_nodes:
						# create a new root node and add it into the dict.
						root = Node(None, thread_id, start_time, "Root")
						root_nodes[thread_id] = root
						root.call_count = 1

						# increment the global node counter
						num_of_node += 1				

						# instantiate a new leaf node
						leaf = Node(root, thread_id, start_time, method_name)
						leaf.call_count = 1
						root.child_node.append(leaf)

						# update the pointer to point to the current node
						resume_node[thread_id] = leaf

					# if root node already exists in the dict., resume the parsing at where it stopped
					else:
						current_node = resume_node[thread_id]

						# check if the corresponding child has already existed
						leaf = current_node.has_child(method_name)
						# if exists...
						if leaf:
							leaf.call_count +=1
							leaf.start_time = start_time
						# if not...
						else:
							# instantiate a new leaf node
							leaf = Node(current_node, thread_id, start_time, method_name)
							leaf.call_count = 1
							current_node.child_node.append(leaf)

							# increment the global node counter
							num_of_node += 1

						# update the pointer to point to the current node
						resume_node[thread_id] = leaf

				# the method call is finished
				elif "[Call  end ]" in line:
					# Extract calling context information from the log
					thread_id = (line.split("$$")[1])
					end_time = float(line.split("$$")[2])
					method_name = (line.split("$$")[3]).rstrip()
					#print ("Current node: " + thread_id + ", " + start_time + ", " + method_name)

					current_node = resume_node[thread_id]

					# Sanity check: ensure that [Call begin] and [Call  end ] always appear in pair.
					# Quit parsing and let user to check for the cause of the error.
					if current_node.method_name != method_name:
						print ("[ERROR] Method names are not matched: " + thread_id + ", " + str(end_time) + ", " + method_name)
						print ("[ERROR] Current node: " + current_node.method_name)

						# print out current call stack
						while current_node.method_name != "Root":
							current_node = current_node.parent_node
							print ("[ERROR] Current node: " + current_node.method_name)

						# unexpected error, so quit parsing
						sys.exit(0)
					else:
						# compute execution time
						exe_time = float(end_time - current_node.start_time) / 1000.0; # unit: ms

						# update average execution time
						if len(current_node.exe_time) > 0:
							current_node.avg_exe_time = ((len(current_node.exe_time) * current_node.avg_exe_time) + exe_time) / (len(current_node.exe_time) + 1)
						else:
							current_node.avg_exe_time = exe_time;
						# append the execution time to the list
						current_node.exe_time.append(exe_time)

						# update the global avg execution time for the method
						method_time[method_name] = current_node.avg_exe_time

						# Go one level up to current node's parent
						resume_node[thread_id] = current_node.parent_node

				# an exception is raised
				elif "[Exception ]" in line:
					# Extract calling context information from the log
					thread_id = (line.split("$$")[1])
					end_time = float(line.split("$$")[2])
					method_name = (line.split("$$")[3]).rstrip()

					# silent exist - keep going to upper level of the tree until the method name is matched.
					current_node = resume_node[thread_id]
					return_node = resume_node[thread_id]
					first_excep_node_found = False

					#print ("Exception: " + thread_id + ", " + str(end_time) + ", " + method_name)

					#while current_node.method_name != "Root" and method_name not in current_node.method_name:
					# When exception happens in a recursive call, it will return to the first node which invokes such recursive call.
					while current_node.method_name != "Root":
						if first_excep_node_found:
							if method_name not in current_node.method_name:
								break

						if method_name in current_node.method_name:
							return_node = current_node
							first_excep_node_found = True

						current_node = current_node.parent_node

					current_node = resume_node[thread_id]
					while current_node != return_node:
						# compute execution time
						exe_time = float(end_time - current_node.start_time) / 1000.0; # unit: ms
						# update average execution time
						if len(current_node.exe_time) > 0:
							current_node.avg_exe_time = ((len(current_node.exe_time) * current_node.avg_exe_time) + exe_time) / (len(current_node.exe_time) + 1)
						else:
							current_node.avg_exe_time = exe_time;
						# append the execution time to the list
						current_node.exe_time.append(exe_time)
						current_node = current_node.parent_node
					resume_node[thread_id] = return_node

				# extract # of passed tests
				elif "OK" in line:
					test_result = "Pass"
					test_result_count[0] = int(re.findall(r"\d+", line)[0])

				# extract # of failed tests
				elif "FAILURES!!!" in line:
					line = next(log_file)
					num_of_test = int(re.findall(r"\d+", line)[0])
					num_of_failure = int(re.findall(r"\d+", line)[1])

					test_result = "Fail"
					test_result_count[0] = num_of_test - num_of_failure
					test_result_count[1] = num_of_failure

		# extract information from the CCT.
		for key in root_nodes:
			Extract_CCT(root_nodes[key], 0, method_count, method_depth, method_breadth)

		# print out summary
		print ("[INFO] CCT has been built successfully!")
		print ("[INFO] Generating report...")
		print ("[INFO] >> Test result ([Passed, Failed]): " + str(test_result_count))
		print ("[INFO] >> # of threads: " + str(len(root_nodes)))
		print ("[INFO] >> # of method calls: " + str(num_of_call))
		print ("[INFO] >> # of nodes: " + str(num_of_node))

		# compute interested metrics
		#top_method_time = sorted(method_time.items(), key=lambda x: (-x[1], x[0]))[0:9]
		#top_method_count = sorted(method_count.items(), key=lambda x: (-x[1], x[0]))[0:9]
		#top_method_depth = sorted(method_depth.items(), key=lambda x: (-x[1], x[0]))[0:9]
		#top_method_breadth = sorted(method_breadth.items(), key=lambda x: (-x[1], x[0]))[0:9]
		top_method_time = sorted(method_time.values(), reverse=True)[0:9]
		top_method_count = sorted(method_count.values(), reverse=True)[0:9]
		top_method_depth = sorted(method_depth.values(), reverse=True)[0:9]
		top_method_breadth = sorted(method_breadth.values(), reverse=True)[0:9]

		print ("[INFO] >> Top 10 slowest methods: " + str(top_method_time))
		print ("[INFO] >> Top 10 common methods: " + str(top_method_count))
		print ("[INFO] >> Top 10 deepest methods: " + str(top_method_depth))
		print ("[INFO] >> Top 10 widest methods: " + str(top_method_breadth))

		"""
		keys = toCSV[0].keys()
		with open(sys.argv[2], 'w') as output_file:
			csv_writer = csv.DictWriter(output_file, keys)
			csv_writer.writeheader()
			csv_writer.writerows(toCSV)
		"""

		# generate csv file
		csv_time_writer.writerow([filename.rsplit('.', 1)[0]] + top_method_time + [test_result])	
		csv_count_writer.writerow([filename.rsplit('.', 1)[0]] + top_method_count + [test_result])		
		csv_depth_writer.writerow([filename.rsplit('.', 1)[0]] + top_method_depth + [test_result])
		csv_breadth_writer.writerow([filename.rsplit('.', 1)[0]] + top_method_breadth + [test_result])