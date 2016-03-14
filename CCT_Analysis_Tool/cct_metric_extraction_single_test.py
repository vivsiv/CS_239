import sys
import os
import csv
import re
import operator
import pickle

from collections import Counter

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

# creare output files
output_time_file    = open(sys.argv[2] + r"\metric_time.csv", 'w')
output_count_file  = open(sys.argv[2] + r"\metric_count.csv", 'w')
output_depth_file   = open(sys.argv[2] + r"\metric_depth.csv", 'w')
output_breadth_file = open(sys.argv[2] + r"\metric_breadth.csv", 'w')
output_time_name_file    = open(sys.argv[2] + r"\metric_time_name.csv", 'w')
output_count_name_file  = open(sys.argv[2] + r"\metric_count_name.csv", 'w')
output_depth_name_file   = open(sys.argv[2] + r"\metric_depth_name.csv", 'w')
output_breadth_name_file = open(sys.argv[2] + r"\metric_breadth_name.csv", 'w')

# prepare csv writers
csv_time_writer    = csv.writer(output_time_file, delimiter=',', lineterminator='\n')
csv_count_writer  = csv.writer(output_count_file, delimiter=',', lineterminator='\n')
csv_depth_writer   = csv.writer(output_depth_file, delimiter=',', lineterminator='\n')
csv_breadth_writer = csv.writer(output_breadth_file, delimiter=',', lineterminator='\n')
csv_time_name_writer    = csv.writer(output_time_name_file, delimiter=',', lineterminator='\n')
csv_count_name_writer  = csv.writer(output_count_name_file, delimiter=',', lineterminator='\n')
csv_depth_name_writer   = csv.writer(output_depth_name_file, delimiter=',', lineterminator='\n')
csv_breadth_name_writer = csv.writer(output_breadth_name_file, delimiter=',', lineterminator='\n')

# prepare csv headers
csv_time_writer.writerow(["test_name", "longest_1", "longest_2", "longest_3", "longest_4", "longest_5", "longest_6", "longest_7", "longest_8", "longest_9", "longest_10", "pass/fail"])
csv_count_writer.writerow(["test_name", "most_common_1", "most_common_2", "most_common_3", "most_common_4", "most_common_5", "most_common_6", "most_common_7", "most_common_8", "most_common_9", "most_common_10", "pass/fail"])
csv_depth_writer.writerow(["test_name", "deepest_1", "deepest_2", "deepest_3", "deepest_4", "deepest_5", "deepest_6", "deepest_7", "deepest_8", "deepest_9", "deepest_10", "pass/fail"])
csv_breadth_writer.writerow(["test_name", "breadthest_1", "breadthest_2", "breadthest_3", "breadthest_4", "breadthest_5", "breadthest_6", "breadthest_7", "breadthest_8", "breadthest_9", "breadthest_10", "pass/fail"])
csv_time_name_writer.writerow(["test_name", "longest_1", "longest_2", "longest_3", "longest_4", "longest_5", "longest_6", "longest_7", "longest_8", "longest_9", "longest_10", "pass/fail"])
csv_count_name_writer.writerow(["test_name", "most_common_1", "most_common_2", "most_common_3", "most_common_4", "most_common_5", "most_common_6", "most_common_7", "most_common_8", "most_common_9", "most_common_10", "pass/fail"])
csv_depth_name_writer.writerow(["test_name", "deepest_1", "deepest_2", "deepest_3", "deepest_4", "deepest_5", "deepest_6", "deepest_7", "deepest_8", "deepest_9", "deepest_10", "pass/fail"])
csv_breadth_name_writer.writerow(["test_name", "breadthest_1", "breadthest_2", "breadthest_3", "breadthest_4", "breadthest_5", "breadthest_6", "breadthest_7", "breadthest_8", "breadthest_9", "breadthest_10", "pass/fail"])


# global dict. for project specific feature
method_time_global = dict()
method_count_global = dict()
method_depth_global = dict()
method_breadth_global = dict()

with open(r".\project_specific\jsoup_time_global.pkl", "rb") as f:
	method_time_global = pickle.load(f)
with open(r".\project_specific\jsoup_count_global.pkl", "rb") as f:
	method_count_global = pickle.load(f)
with open(r".\project_specific\jsoup_depth_global.pkl", "rb") as f:
	method_depth_global = pickle.load(f)
with open(r".\project_specific\jsoup_breadth_global.pkl", "rb") as f:
	method_breadth_global = pickle.load(f)

sorted_method_time_global = sorted(method_time_global.items(), key=operator.itemgetter(1), reverse=True)
sorted_method_count_global = sorted(method_count_global.items(), key=operator.itemgetter(1), reverse=True)
sorted_method_depth_global = sorted(method_depth_global.items(), key=operator.itemgetter(1), reverse=True)
sorted_method_breadth_global = sorted(method_breadth_global.items(), key=operator.itemgetter(1), reverse=True)


# find out all test file and run it with JUnit
for path, subdirs, files in os.walk(sys.argv[1]):
	for filename in files:
		file = os.path.join(path, filename)

		print ("[INFO] Building CCT from the log file: " + file)

		# initialize parser variables
		test_case_name = ""
		root_nodes = dict() # <k,v>=<thread_id, node>: store the root node with different thread_id
		resume_node = dict() # <k,v>=<thread_id, node>: store the node whether the parser should resume to when the next node comes in.
		num_of_node = 0
		num_of_call = 0
		test_result = ""
		# dict.
		method_time = dict()
		method_count = dict()
		method_depth = dict()
		method_breadth = dict()
		# list.
		top_method_time = list()
		top_method_count = list()
		top_method_depth = list()
		top_method_breadth = list()
		top_method_time_name = list()
		top_method_count_name = list()
		top_method_depth_name = list()
		top_method_breadth_name = list()

		# parse the log file line by line
		with open(file, 'r') as log_file:
			test_file_name = filename.rsplit('.', 1)[0]

			for line in log_file:
				# test case starts
				if "[Test begin]" in line:
					test_case_name = line.split("$$")[1]

					print ("[INFO] Parsing log for test case: " + test_case_name)

					# reset all parser variables to 0
					root_nodes.clear()
					resume_node.clear()
					num_of_node = 0
					num_of_call = 0
					test_result = ""
					method_time.clear()
					method_count.clear()
					method_depth.clear()
					method_breadth.clear()
					del top_method_time[:]
					del top_method_count[:]
					del top_method_depth[:]
					del top_method_breadth[:]
					del top_method_time_name[:]
					del top_method_count_name[:]
					del top_method_depth_name[:]
					del top_method_breadth_name[:]

				# test case ends
				elif "[Test  end ]" in line:
					test_result = line.split("$$")[2].rstrip()

					# extract information from the CCT.
					for key in root_nodes:
						Extract_CCT(root_nodes[key], 0, method_count, method_depth, method_breadth)

					# sort metrics based on
					sorted_method_time = sorted(method_time.items(), key=operator.itemgetter(1), reverse=True)
					sorted_method_count = sorted(method_count.items(), key=operator.itemgetter(1), reverse=True)
					sorted_method_depth = sorted(method_depth.items(), key=operator.itemgetter(1), reverse=True)
					sorted_method_breadth = sorted(method_breadth.items(), key=operator.itemgetter(1), reverse=True)

					
					# project specific
					for i in range(0, 10):
						if i < len(sorted_method_time) and sorted_method_time_global[i][0] in method_time:
							#top_method_time_name.append(method_time[i][0])
							top_method_time.append(method_count[sorted_method_time_global[i][0]])
						else:
							#top_method_time_name += [""]
							top_method_time += [0]

					for i in range(0, 10):			
						if i < len(sorted_method_count) and sorted_method_count_global[i][0] in method_count:
							#top_method_count_name.append(sorted_method_count[i][0])
							top_method_count.append(method_count[sorted_method_count_global[i][0]])
						else:
							#top_method_count_name += [""]
							top_method_count += [0]

					for i in range(0, 10):	
						if i < len(sorted_method_depth) and sorted_method_depth_global[i][0] in method_depth:	
							#top_method_depth_name.append(sorted_method_depth[i][0])
							top_method_depth.append(method_count[sorted_method_depth_global[i][0]])
						else:
							#top_method_depth_name += [""]
							top_method_depth += [0]

					for i in range(0, 10):		
						if i < len(sorted_method_breadth) and sorted_method_breadth_global[i][0] in method_breadth:
							#top_method_breadth_name.append(sorted_method_breadth[i][0])
							top_method_breadth.append(method_count[sorted_method_breadth_global[i][0]])
						else:
							#top_method_breadth_name += [""]
							top_method_breadth += [0]

					"""
					for i in range(0, 10):
						if i < len(sorted_method_time):
							top_method_time_name.append(sorted_method_time[i][0])
							top_method_time.append(sorted_method_time[i][1])
						else:
							top_method_time_name += [""]
							top_method_time += [0]

					for i in range(0, 10):			
						if i < len(sorted_method_count):
							top_method_count_name.append(sorted_method_count[i][0])
							top_method_count.append(sorted_method_count[i][1])
						else:
							top_method_count_name += [""]
							top_method_count += [0]

					for i in range(0, 10):	
						if i < len(sorted_method_depth):	
							top_method_depth_name.append(sorted_method_depth[i][0])
							top_method_depth.append(sorted_method_depth[i][1])
						else:
							top_method_depth_name += [""]
							top_method_depth += [0]

					for i in range(0, 10):		
						if i < len(sorted_method_breadth):
							top_method_breadth_name.append(sorted_method_breadth[i][0])
							top_method_breadth.append(sorted_method_breadth[i][1])
						else:
							top_method_breadth_name += [""]
							top_method_breadth += [0]
					"""

					# print out summary
					print ("[INFO] CCT has been built successfully!")
					print ("[INFO] Generating report...")
					print ("[INFO] >> # Test Case: " + test_file_name + "#" + test_case_name)
					print ("[INFO] >> # Test result: " + test_result)
					print ("[INFO] >> # of threads: " + str(len(root_nodes)))
					print ("[INFO] >> # of method calls: " + str(num_of_call))
					print ("[INFO] >> # of nodes: " + str(num_of_node))
					#print ("\n\n")
					"""
					print ("[INFO] >> Top 10 slowest methods: " + str(top_method_time))
					print ("[INFO] >> Top 10 common methods: " + str(top_method_count))
					print ("[INFO] >> Top 10 deepest methods: " + str(top_method_depth))
					print ("[INFO] >> Top 10 widest methods: " + str(top_method_breadth))
					"""

					# generate metric file in csv foramt
					csv_time_writer.writerow([test_file_name] + top_method_time + [test_result])
					csv_count_writer.writerow([test_file_name] + top_method_count + [test_result])
					csv_depth_writer.writerow([test_file_name] + top_method_depth + [test_result])
					csv_breadth_writer.writerow([test_file_name] + top_method_breadth + [test_result])
					csv_time_name_writer.writerow([test_file_name] + top_method_time_name + [test_result])
					csv_count_name_writer.writerow([test_file_name] + top_method_count_name + [test_result])
					csv_depth_name_writer.writerow([test_file_name] + top_method_depth_name + [test_result])
					csv_breadth_name_writer.writerow([test_file_name] + top_method_breadth_name + [test_result])

					
					# project specific feature
					method_time_global = dict(Counter(method_time_global) + Counter(method_time))
					method_count_global = dict(Counter(method_count_global) + Counter(method_count))
					method_depth_global = dict(Counter(method_depth_global) + Counter(method_depth))
					method_breadth_global = dict(Counter(method_breadth_global) + Counter(method_breadth))
					

				# the method call is invoked
				elif "[Call begin]" in line:
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
						#print ("[ERROR] Method names are not matched: " + thread_id + ", " + str(end_time) + ", " + method_name)
						#print ("[ERROR] Current node: " + current_node.method_name)

						# print out current call stack
						while current_node.method_name != "Root":
							current_node = current_node.parent_node
							#print ("[ERROR] Current node: " + current_node.method_name)

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
					#print ("Current node: " + current_node.method_name)
					
					while current_node.method_name != "Root" and method_name not in current_node.method_name:
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
					resume_node[thread_id] = current_node

					"""
					# When exception happens in a recursive call, it will return to the first node which invokes such recursive call.
					while current_node.method_name != "Root":
						#print ("Current node: " + current_node.method_name)

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
					"""

"""
# save project specific feature
with open("jline_time_global.pkl", "wb") as f:
	pickle.dump(method_time_global, f, pickle.HIGHEST_PROTOCOL)

with open("jline_count_global.pkl", "wb") as f:
	pickle.dump(method_count_global, f, pickle.HIGHEST_PROTOCOL)

with open("jline_depth_global.pkl", "wb") as f:
	pickle.dump(method_depth_global, f, pickle.HIGHEST_PROTOCOL)

with open("jline_breadth_global.pkl", "wb") as f:
	pickle.dump(method_breadth_global, f, pickle.HIGHEST_PROTOCOL)
"""