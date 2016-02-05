import os
os.system('rm out.txt')

# Compile the ASM_Example class
os.system('javac -cp asm-all-5.0.4.jar ASM_Example.java')
all_files = os.listdir(".")
old_class_files = [f for f in all_files if f.endswith(".class")]

#Compile file to instrument
os.system('javac FbClass.java')

for f in os.listdir(".") :
	if (f.endswith(".class") and (not f in old_class_files)) :
		file_name = f.split(".")[0]
		compile_string = "java -cp asm-all-5.0.4.jar:. ASM_Example "
		compile_string += (f + " ")
		compile_string += (file_name + "_new.class")
		print(compile_string)
		os.system(compile_string)

		move_string = "mv " + file_name + "_new.class " + f
		print(move_string)
		os.system(move_string)
		
# Instrument FbClass.class
# os.system('java -cp asm-all-5.0.4.jar:. ASM_Example FbClass.class FbClass_new.class')
# os.system('mv FbClass_new.class FbClass.class')
# Instrument myClass.class
# os.system('java -cp asm-all-5.0.4.jar:. ASM_Example myClass.class myClass_new.class')
# os.system('mv myClass_new.class myClass.class')
# Run the newly generated myClass class
os.system('touch out.txt')
os.system('java -cp . myClass > out.txt')
# Remove all class files
os.system('rm *.class')





