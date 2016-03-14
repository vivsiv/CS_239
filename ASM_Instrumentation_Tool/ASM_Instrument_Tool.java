// Import core library
import java.io.*;
import java.util.*;

// Import ASM Library
import org.objectweb.asm.*;
import org.objectweb.asm.commons.*; 

class ASM_Instrument_Tool {
	public static int classCount = 0;
	public static long startTime = 0;
	public static long stopTime = 0;

	public static void main(String[] args) {
		// Check the validity of input commandline arguments
		if (args.length != 2) {
			System.out.println("Please provide both input path and output path!");
			throw new UnsupportedOperationException();
		}

		File inputDir = new File(args[0]);
		File outputDir = new File(args[1]);

		// Check input directory path
		if (!inputDir.exists()) {
			System.out.println("Please specify a correct input directory path!");
			throw new NullPointerException();
		}

		startTime = System.currentTimeMillis();
		walkDirectoryStructure(args[0], args[1]);
		stopTime = System.currentTimeMillis();

		System.out.println("*Summary*");
		System.out.println(" >>Total instrumented class: " + Integer.toString(classCount));
		System.out.println(" >>Total instrumented time: " + Long.toString(stopTime - startTime) + " ms");
	}

	public static void instrumentByteCode(String inputFile, String outputFile) {
		System.out.println("Start processing source class file: " + inputFile + "");

		classCount++;

		try {
			FileInputStream input_bytecode = new FileInputStream(inputFile);
			FileOutputStream output_bytecode = new FileOutputStream(outputFile);

			ClassReader reader = new ClassReader(input_bytecode);
			//TraceClassWriter writer = new TraceClassWriter(TraceClassWriter.COMPUTE_FRAMES, ASM_Instrument_Tool.class.getClassLoader());
			ClassWriter writer = new ClassWriter(TraceClassWriter.COMPUTE_FRAMES);

			//********************************************************************************
			// wrap ClassWriter using MyClassVisitor
			// accept MyClassVisitor to visit ClassReader
			ClassVisitor visitor = new MyClassVisitor(writer);
			reader.accept(visitor, ClassReader.EXPAND_FRAMES);
			//********************************************************************************

			output_bytecode.write(writer.toByteArray());
			input_bytecode.close();
			output_bytecode.close();

		} catch (IOException e) {
			e.printStackTrace();
		}
		System.out.println("Finish processing source class file! \n\n");
	}

	public static void walkDirectoryStructure(String sourcePath, String targetPath) {
		File sourceFile = new File(sourcePath);
		File targetFile = new File(targetPath);

		// If current directory does not exist in the target path, create one.
		if (!targetFile.exists()) {
			targetFile.mkdir();
		}

		// Walk through all files and sub-directories in the source file path
		for (File file: sourceFile.listFiles()) {
			String nextLevelPath = "\\" + file.getName();
			
			// If the file visited is a directory, go into that directory.
			if (file.isDirectory()) {
				System.out.println("Target directory: " + targetPath + nextLevelPath);

				walkDirectoryStructure(sourcePath + nextLevelPath, targetPath + nextLevelPath);
			// If the file visited is a *.class
			} else {
				if (file.getName().toLowerCase().endsWith((".class"))) {
					instrumentByteCode(sourcePath + nextLevelPath, targetPath + nextLevelPath);
				}
			} // if
		} // for
	}
}

//********************************************************************************
// MyClassVisitor: user-defined ClassVisitor
// MyClassVisitor overrides the visitMethod method to return user-defined MethodVisitor
class MyClassVisitor extends ClassVisitor implements Opcodes {
	private String owner;
	private boolean isInterface;

	public MyClassVisitor(final ClassVisitor cv) {
		super(ASM5, cv);
	}

	@Override
	public void visit(int version, int access, String name, String signature, String superName, String[] interfaces) {
		super.visit(version, access, name, signature, superName, interfaces);

		System.out.println("Visiting class: " + name);
		System.out.println("Class Major Version: " + version);

		owner = name;
		isInterface = (access & ACC_INTERFACE) != 0;
	}

	@Override
	public MethodVisitor visitMethod(int access, String name, String desc, String signature, String[] exceptions) {
		MethodVisitor mv = cv.visitMethod(access, name, desc, signature, exceptions);

		// Instantiate a customized MethodVisitor
		if (!isInterface && mv != null) {
			MyMethodVisitor at = new MyMethodVisitor(mv, name);

			at.aa = new AnalyzerAdapter(owner, access, name, desc, at);
			at.lvs = new LocalVariablesSorter(access, desc, at.aa);
			
			return at.lvs;
		}

		return mv;
	}

	@Override
	public FieldVisitor visitField(int access, String name, String desc, String signature, Object value) {
		FieldVisitor fv = cv.visitField(access, name, desc, signature, value);

		return fv;
	}
}
//********************************************************************************

//********************************************************************************
// MyMethodVisitor: user-defined MethodVisitor
// MyMethodVisitor overrides the visitMethodInsn method to prepare for bytecode instruction instrumentation
class MyMethodVisitor extends MethodVisitor implements Opcodes {
	public LocalVariablesSorter lvs;
	public AnalyzerAdapter aa;
	private Map<String, Boolean> exceptionLabels;
	private String methodName;
	private int timestampID;
	private int threadstampID;
	private int maxStack;

	public MyMethodVisitor(MethodVisitor mv, String methodName) {
		super(ASM5, mv);
		
		this.methodName = methodName;
		exceptionLabels = new HashMap<String, Boolean>();
	}

	@Override
	public void visitCode() {
		mv.visitCode();

		// Allocate an empty space in the stack and assign it with a new ID.
		timestampID = lvs.newLocal(Type.LONG_TYPE);
		threadstampID = lvs.newLocal(Type.LONG_TYPE);
		maxStack = 4;
	}

	@Override
	// Currently do nothing but invoke the visitMethodInsn method of its base class
	public void visitMethodInsn(int opcode, String owner, String name, String desc, boolean itf) {

		// Get the thread ID associated with current method.
		mv.visitMethodInsn(INVOKESTATIC, "java/lang/Thread", "currentThread", "()Ljava/lang/Thread;", false);
		mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/Thread", "getId", "()J", false);
		mv.visitVarInsn(LSTORE, threadstampID);
		// Get current system timestamp.
		mv.visitMethodInsn(INVOKESTATIC, "java/lang/System", "nanoTime", "()J", false); // Invoke nanoTime() to get current system timestamp.
		mv.visitVarInsn(LSTORE, timestampID);   // Store the timestamp into the newly allocated variable.
		// Below code is the preparation for System.out.println().
		mv.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");
		mv.visitTypeInsn(NEW, "java/lang/StringBuilder");
		mv.visitInsn(DUP);
		mv.visitMethodInsn(INVOKESPECIAL, "java/lang/StringBuilder", "<init>", "()V", false);
		mv.visitLdcInsn("[Call begin]$$");
		mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(Ljava/lang/String;)Ljava/lang/StringBuilder;", false);
		mv.visitVarInsn(LLOAD, threadstampID);
		mv.visitMethodInsn(INVOKESTATIC, "java/lang/Long", "toString", "(J)Ljava/lang/String;", false);
		mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(Ljava/lang/String;)Ljava/lang/StringBuilder;", false);
		mv.visitLdcInsn("$$");
		mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(Ljava/lang/String;)Ljava/lang/StringBuilder;", false);
		mv.visitVarInsn(LLOAD, timestampID);
		mv.visitMethodInsn(INVOKESTATIC, "java/lang/Long", "toString", "(J)Ljava/lang/String;", false);
		mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(Ljava/lang/String;)Ljava/lang/StringBuilder;", false);
		mv.visitLdcInsn("$$" + owner + "::" + name);
		mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(Ljava/lang/String;)Ljava/lang/StringBuilder;", false);
		mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;", false);
		mv.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println", "(Ljava/lang/String;)V", false);

		// Continue parsing...
		mv.visitMethodInsn(opcode, owner, name, desc, itf);

		// Get the thread ID associated with current method.
		mv.visitMethodInsn(INVOKESTATIC, "java/lang/Thread", "currentThread", "()Ljava/lang/Thread;", false);
		mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/Thread", "getId", "()J", false);
		mv.visitVarInsn(LSTORE, threadstampID);
		// Get current system timestamp.
		mv.visitMethodInsn(INVOKESTATIC, "java/lang/System", "nanoTime", "()J", false); // Invoke nanoTime() to get current system timestamp.
		mv.visitVarInsn(LSTORE, timestampID);   // Store the timestamp into the newly allocated variable.
		// Below code is the preparation for System.out.println().
		mv.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");
		mv.visitTypeInsn(NEW, "java/lang/StringBuilder");
		mv.visitInsn(DUP);
		mv.visitMethodInsn(INVOKESPECIAL, "java/lang/StringBuilder", "<init>", "()V", false);
		mv.visitLdcInsn("[Call  end ]$$");
		mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(Ljava/lang/String;)Ljava/lang/StringBuilder;", false);
		mv.visitVarInsn(LLOAD, threadstampID);
		mv.visitMethodInsn(INVOKESTATIC, "java/lang/Long", "toString", "(J)Ljava/lang/String;", false);
		mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(Ljava/lang/String;)Ljava/lang/StringBuilder;", false);
		mv.visitLdcInsn("$$");
		mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(Ljava/lang/String;)Ljava/lang/StringBuilder;", false);
		mv.visitVarInsn(LLOAD, timestampID);
		mv.visitMethodInsn(INVOKESTATIC, "java/lang/Long", "toString", "(J)Ljava/lang/String;", false);
		mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(Ljava/lang/String;)Ljava/lang/StringBuilder;", false);
		mv.visitLdcInsn("$$" + owner + "::" + name);
		mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(Ljava/lang/String;)Ljava/lang/StringBuilder;", false);
		mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;", false);
		mv.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println", "(Ljava/lang/String;)V", false);

		// Adjust max stack size    
		maxStack = Math.max(aa.stack.size() + 4, maxStack);
	}

	@Override
	public void visitTryCatchBlock(Label start, Label end, Label handler, String type) {
		// Put the label of catch block into the map
		exceptionLabels.put(handler.toString(), true);

		mv.visitTryCatchBlock(start, end, handler, type);

	}

	@Override
	public void visitLabel(Label label) {
		mv.visitLabel(label);

		// If the visiting label is in the map (such label corresponds to a catch block)
		if (exceptionLabels.containsKey(label.toString())) {
			mv.visitMethodInsn(INVOKESTATIC, "java/lang/Thread", "currentThread", "()Ljava/lang/Thread;", false);
			mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/Thread", "getId", "()J", false);
			mv.visitVarInsn(LSTORE, threadstampID);
			// Get current system timestamp.
			mv.visitMethodInsn(INVOKESTATIC, "java/lang/System", "nanoTime", "()J", false); // Invoke nanoTime() to get current system timestamp.
			mv.visitVarInsn(LSTORE, timestampID);   // Store the timestamp into the newly allocated variable.
			// Below code is the preparation for System.out.println().
			mv.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");
			mv.visitTypeInsn(NEW, "java/lang/StringBuilder");
			mv.visitInsn(DUP);
			mv.visitMethodInsn(INVOKESPECIAL, "java/lang/StringBuilder", "<init>", "()V", false);
			mv.visitLdcInsn("[Exception ]$$");
			mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(Ljava/lang/String;)Ljava/lang/StringBuilder;", false);
			mv.visitVarInsn(LLOAD, threadstampID);
			mv.visitMethodInsn(INVOKESTATIC, "java/lang/Long", "toString", "(J)Ljava/lang/String;", false);
			mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(Ljava/lang/String;)Ljava/lang/StringBuilder;", false);
			mv.visitLdcInsn("$$");
			mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(Ljava/lang/String;)Ljava/lang/StringBuilder;", false);
			mv.visitVarInsn(LLOAD, timestampID);
			mv.visitMethodInsn(INVOKESTATIC, "java/lang/Long", "toString", "(J)Ljava/lang/String;", false);
			mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(Ljava/lang/String;)Ljava/lang/StringBuilder;", false);
			mv.visitLdcInsn("$$" + methodName);
			mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "append", "(Ljava/lang/String;)Ljava/lang/StringBuilder;", false);
			mv.visitMethodInsn(INVOKEVIRTUAL, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;", false);
			mv.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println", "(Ljava/lang/String;)V", false);
		}
	}

	@Override
	public void visitMaxs(int maxStack, int maxLocals) {
		mv.visitMaxs(Math.max(this.maxStack, maxStack), maxLocals);
	}
}
//********************************************************************************
