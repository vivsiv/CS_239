rm out.txt

javac FbClass.java
# Compile the ASM_Example class
javac -cp asm-all-5.0.4.jar ASM_Example.java
# Instrument FbClass.class
java -cp asm-all-5.0.4.jar:. ASM_Example FbClass.class FbClass_new.class
mv FbClass_new.class FbClass.class
# Instrument myClass.class
java -cp asm-all-5.0.4.jar:. ASM_Example myClass.class myClass_new.class
mv myClass_new.class myClass.class
# Run the newly generated myClass class
touch out.txt
java -cp . myClass > out.txt
# Remove all class files
rm *.class