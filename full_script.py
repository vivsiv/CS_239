import os
import sys
os.system('rm inst/inst_out.txt')
os.system('rm inst/call_stack_out.txt')
os.system('rm inst/parse_tree_out.txt')

sample = sys.argv[1]
if sample == "fb" :
	os.system('python instrument_script.py fb')
elif sample == "sort":
	os.system('python instrument_script.py sort')
os.system('python generate_call_stack.py inst/inst_out.txt > inst/call_stack_out.txt')
os.system('python parse_tree.py inst/inst_out.txt > inst/parse_tree_out.txt')