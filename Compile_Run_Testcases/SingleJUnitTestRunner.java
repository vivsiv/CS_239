import java.lang.Class;
import java.lang.reflect.Method;
import java.lang.annotation.Annotation;
import java.util.List;
//import java.lang.Thread;
//import java.util.ArrayList;
//import java.util.Set;

// JUnit
import org.junit.runner.JUnitCore;
import org.junit.runner.Request;
import org.junit.runner.Result;

// Major Mutation
import major.mutation.Config;

public class SingleJUnitTestRunner {
    public static void main(String... args) throws ClassNotFoundException {
    	//String testClassFile = args[0];

    	/*
		try {
			Class testClass = ;
		} catch(ClassNotFoundException e) {
			System.out.println("Unable to locate specified class: " + args[0] + "!");
			System.exit(1);
		}
		*/

        
		System.out.println("[Test begin]$$" + Class.forName(args[0]).getName());
		Request request = Request.method(Class.forName(args[0]), args[1]);
		Result result = new JUnitCore().run(request);
		if (result.wasSuccessful()) {
			System.out.println("[Test  end ]$$" + Class.forName(args[0]).getName() + "$$Pass");
		} else {
			System.out.println("[Test  end ]$$" + Class.forName(args[0]).getName() + "$$Fail");
		}


		/*
        // Go through all methods within the class
		for(Method method: Class.forName(testClassFile).getMethods()) {
		 	//System.out.println("Visiting method: " + method.getName());

		 	// Get all method annotation
			for (Annotation annotation: method.getAnnotations()) {
				// Check whether it is a Junit test case
				if (annotation.toString().contains("org.junit.Test")) {
					System.out.println("[Test begin]$$" + method.getName());

					// Create a test request to the test case.
			        Request request = Request.method(Class.forName(testClassFile), args[1]);

			        // Run the test
			        Result result = new JUnitCore().run(request);

			        //Set<Thread> threadSet = Thread.getAllStackTraces().keySet();
			        //System.out.println("Total threads: " + Integer.toString(threadSet.size()));
			        //System.out.println("All threads: " + threadSet.toString());
*/
			        /*
			        for (Thread thread : threadSet) {
			        	if (thread.getThreadGroup().getName().contains("main")) {
			        		System.out.println("Main thread found: " + thread.toString());
			        		try {
			        			thread.join();
			        		} catch (InterruptedException e) {

			        		}
			        	}
			        }
			        */
/*
			        // Test outcome
			        if (result.wasSuccessful()) {
			        	System.out.println("[Test  end ]$$" + method.getName() + "$$Pass");
			        } else {
			        	System.out.println("[Test  end ]$$" + method.getName() + "$$Fail");
			        }

			        break;
				} // If
			} // For
		} // For
*/

        System.exit(0);
    }
}

