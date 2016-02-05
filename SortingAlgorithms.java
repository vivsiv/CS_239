public class SortingAlgorithms {
	/*
	Counting Sort
	  1) Create an array of indices that would represent a sorted array
	  2) Use this array to sort the original array
	  Run Time -> O(n^2)
	  Space -> O(3n)
	  Stable? -> Yes if in[i] > in[j], No in[i] >= in[j]
	*/
   public static int[] countingSort(int[] in){
	   int[] indices = new int[in.length];
	   for (int i = 0; i < in.length - 1; i++){
		   for (int j = i+1; j < in.length; j++){
			   if (in[i] > in[j]) indices[i]++;
			   else indices[j]++;
		   }
	   }
	   
	   int[] sorted = new int[in.length];
	   for (int i = 0; i < in.length; i++){
		   sorted[indices[i]] = in[i]; 
	   }
	   return sorted;
   }
   
   
   /*
   Selection Sort
     1) Go through array if you find a smaller number to the right save it
     2) Once your through the array if you found a smaller number swqp the two
     Run Time -> O(n^2)
     Space -> O(n)
     Stable? => No eg [3,3,2]
   */
   public static int[] selectionSort(int[] in){
	   for (int i = 0; i < in.length; i++){
		   int minIdx = i;
		   for (int j = i+1; j < in.length; j++){
			   if (in[j] < in[minIdx]) minIdx = j;
		   }
		   if (minIdx != i){
			   int tmp = in[minIdx];
			   in[minIdx] = in[i];
			   in[i] = tmp;
		   }
	   }
	   return in;
   }
   
   /*
   Insertion Sort
     1) Go through the array determine that elements position in the left subarray
     Run Time -> O(n^2)
     Space => O(n)
     Stable? => Yes
   */
   public static int[] insertionSort(int[] in){
	   for (int i = 1; i < in.length; i++){
		   for (int j = i; j >= 0 && in[j] < in[j-1]; j--){
			   int tmp = in[j-1];
			   in[j-1] = in[j];
			   in[j] = tmp;
		   }
	   }
	   return in;
   }
   
   /*
   Bubble Sort
     1) Go through the array and swap items that are out of order
     2) Continue going through array until it is in order
     Run Time -> O(n^2)
     Space -> O(n)
     Stable -> Yes
   */
   public static int[] bubbleSort(int[] in){
	   boolean swapped = false;
	   do {
		   for (int i = 1; i < in.length; i++){
			   if (in[i] < in[i-1]){
				   int tmp = in[i];
				   in[i] = in[i-1];
				   in[i-1] = tmp;
				   swapped = true;
			   }
		   }
	   } while (swapped);
	   return in;
   }
   
   /*
   Merge Sort
     1) Split the array in half
     2) Merge the individual arrays back together in order
     Run Time -> O(nlogn)
     Stable
   */

   public static int[] mergeSort(int[] in){
	   if (in.length == 1) return in;
	   
	   int midIdx = in.length / 2;
	   int[] left = new int[midIdx];
	   int[] right = new int[in.length - midIdx];
	   
	   System.arraycopy(in, 0, left, 0, midIdx);
	   System.arraycopy(in, midIdx, right, 0, in.length - midIdx);
	   
	   left = mergeSort(left);
	   right = mergeSort(right);
	   
	   return merge(left,right);
   }
   
   private static int[] merge(int[] left, int[] right){
	   int leftIdx = 0;
	   int rightIdx = 0;
	   int mergedIdx = 0;
	   int[] merged = new int[left.length + right.length];
	   while(leftIdx < left.length && rightIdx < right.length){
		   if (left[leftIdx] <= right[rightIdx]){
			   merged[mergedIdx] = left[leftIdx];
			   leftIdx++;
		   }
		   else {
			   merged[mergedIdx] = right[rightIdx];
			   rightIdx++;
		   }
		   mergedIdx++;
	   }
	   
	   if (leftIdx < left.length) System.arraycopy(left, leftIdx, merged, mergedIdx, left.length - leftIdx);
	   if (rightIdx < right.length) System.arraycopy(right, rightIdx, merged, mergedIdx, right.length - rightIdx);
	   
	   return merged;
   }
   
   public static String arrayString(int[] in){
	   String arr = "";
	   for (int i = 0; i < in.length; i++){
		   arr += (in[i] + " ");
	   }
	   return arr.trim();
   }
   
   public static void main(String[] args){
	   int[] test = {4,5,6,4,2,3,7,8,4,5,7,8};
	   System.out.println("Unsorted... " + arrayString(test));
	   System.out.println("CountingSort... " + arrayString(countingSort(test)));
	   System.out.println("SelectionSort... " + arrayString(selectionSort(test)));
	   System.out.println("InserionSort... " + arrayString(insertionSort(test)));
	   System.out.println("BubbleSort... " + arrayString(bubbleSort(test)));
	   System.out.println("MergeSort... " + arrayString(mergeSort(test)));
   }
}