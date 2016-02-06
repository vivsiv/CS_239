import java.io.*;
import org.objectweb.asm.*;
class ASM_Example {
	public static void main(String[] args) {
		try {
			FileInputStream input_bytecode = new FileInputStream(args[0]);
			FileOutputStream output_bytecode = new FileOutputStream(args[1]);

			ClassReader reader = new ClassReader(input_bytecode);
			ClassWriter writer = new ClassWriter(ClassWriter.COMPUTE_FRAMES);

			//********************************************************************************
			// wrap ClassWriter using MyClassVisitor
			// accept MyClassVisitor to visit ClassReader
			ClassVisitor visitor = new MyClassVisitor(writer);
			reader.accept(visitor, 0);
			//********************************************************************************

			output_bytecode.write(writer.toByteArray());
			input_bytecode.close();
			output_bytecode.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}

//********************************************************************************
// MyClassVisitor: user-defined ClassVisitor
// MyClassVisitor overrides the visitMethod method to return user-defined MethodVisitor

class MyClassVisitor extends ClassVisitor implements Opcodes {
	public MyClassVisitor(final ClassVisitor cv) {
		super(ASM5, cv);
	}
	@Override
	public MethodVisitor visitMethod(int access, String name, String desc, String signature, String[] exceptions) {
		MethodVisitor mv = cv.visitMethod(access, name, desc, signature, exceptions);
		if (mv == null) return null;
		return new MyMethodVisitor(mv);
	}
}
//********************************************************************************

//********************************************************************************
// MyMethodVisitor: user-defined MethodVisitor
// MyMethodVisitor overrides the visitMethodInsn method to prepare for bytecode instruction instrumentation
class MyMethodVisitor extends MethodVisitor implements Opcodes {
	public MyMethodVisitor(MethodVisitor mv) {
		super(ASM5, mv);
	}

	@Override
	// Now we add instrumentation code for printing
	public void visitMethodInsn(int opcode, String owner, String name, String desc, boolean itf) {
		//********************************************************************************
		// print "[Call begin] ..."
		// use ASMifier to generate instrumentation code for your need
		mv.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");
		mv.visitLdcInsn("[Call begin]$$" + owner + "::" + name);
		mv.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println", "(Ljava/lang/String;)V", false);
		//********************************************************************************

		mv.visitMethodInsn(opcode, owner, name, desc, itf);

		//********************************************************************************
		// print "[Call end] ..."
		mv.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");
		mv.visitLdcInsn("[Call end]$$" + owner + "::" + name);
		mv.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println", "(Ljava/lang/String;)V", false);
		//********************************************************************************
	}
}

// RUNNING

// # Compile the ASM_Example class
// javac -cp asm-5.0.4/lib/all/asm-all-5.0.4.jar ASM_Example.java
// # Instrument FbClass.class
// java -cp asm-5.0.4/lib/all/asm-all-5.0.4.jar:. ASM_Example FbClass.class FbClass_new.class
// mv FbClass_new.class FbClass.class
// # Instrument myClass.class
// java -cp asm-5.0.4/lib/all/asm-all-5.0.4.jar:. ASM_Example myClass.class myClass_new.class
// mv myClass_new.class myClass.class
// # Run the newly generated myClass class
// java -cp . myClass
//********************************************************************************