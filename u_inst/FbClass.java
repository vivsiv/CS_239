class FbClass {
	int value;
	public FbClass() {
		value = 0;
	}
	public void calc(int n) {
		if (n <= 0) 
			value += 0;
		else if (n <= 2)
			value += 1;
		else {
			//System.out.println("[Call begin] FBClass::calc");
			calc(n - 1);
			//System.out.println("[Call end] FBClass::calc");
			//System.out.println("[Call begin] FBClass::calc");
			calc(n - 2);
			//System.out.println("[Call end] FBClass::calc");
		}
		return ;
	}

	public void print() {
		//System.out.println("[Call begin] System.out::println");
		//System.out.println(value);
		//System.out.println("[Call end] System.out::println");
	}
};

class myClass {
	public static void main(String[] args) {
		//System.out.println("[Call begin] Object::init");
		FbClass cls = new FbClass();
		//System.out.println("[Call end] Object::init");

		//System.out.println("[Call begin] FBClass::calc");
		cls.calc(4);
		//System.out.println("[Call end] FBClass::calc");

		//System.out.println("[Call begin] FBClass::print");
		cls.print();
		//System.out.println("[Call end] FBClass::print");
	}
};