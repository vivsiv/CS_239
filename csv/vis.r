data <- read.csv(file="batch_out.csv",sep=",",head=TRUE)

par(mfrow = c(2,2))
#Bar plot for top 10 fastest methods
order.exe_time_asc <- order(data$Avg_Execution_Time)
sorted_exe_time_asc <- data[order.exe_time_asc,]
fastest_exe_time <- head(sorted_exe_time_asc,10)
barplot(fastest_exe_time$Avg_Execution_Time,main="Top 10 Fastest Methods",xlab="Function Name",names.arg=fastest_exe_time$Function_Name,ylab="Avg Ex Time (usec)",cex.names=0.75,las=2)

#Bar plot for 10 slowest methods
order.exe_time_desc <- order(data$Avg_Execution_Time, decreasing=TRUE)
sorted_exe_time_desc <- data[order.exe_time_desc,]
slowest_exe_time <- head(sorted_exe_time_desc,10)
barplot(slowest_exe_time$Avg_Execution_Time,main="Top 10 Slowest Methods",xlab="Function Name",names.arg=slowest_exe_time$Function_Name,ylab="Avg Ex Time (usec)",cex.names=0.75,las=2)

#Bar plot for top 10 most frequent methods
order.num_calls_desc <- order(data$Num_Calls, decreasing=TRUE)
sorted_num_calls_desc <- data[order.num_calls_desc,]
most_num_calls <- head(sorted_num_calls_desc,10)
barplot(most_num_calls$Num_Calls,main="Top 10 Frequent Methods",xlab="Function Name",names.arg=most_num_calls$Function_Name,ylab="Number of Calls",cex.names=0.75,las=2)

#Bar plot for top 10 most frequent call stacks
order.num_calls_desc <- order(data$Num_Calls, decreasing=TRUE)
sorted_num_calls_desc <- data[order.num_calls_desc,]
call_stack_desc <- sorted_num_calls_desc[sorted_num_calls_desc$Parent_Name == "None",]
most_call_stack <- head(call_stack_desc,10)
barplot(most_call_stack$Num_Calls,main="Top 10 Frequent Call Stacks",xlab="Stack Name Name",names.arg=most_call_stack$Function_Name,ylab="Number of Calls",cex.names=0.75,las=2)