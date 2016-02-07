data <- read.csv(file="batch_out.csv",sep=",",head=TRUE)

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

#Bar plot for top 10 most frequent call stacks
# order.call_stack_desc <- order(data$Avg_Execution_Time, decreasing=TRUE)
# sorted_exe_time_desc <- data[order.exe_time_desc,]
# slowest_exe_time <- head(sorted_exe_time_desc,10)
# barplot(slowest_exe_time$Avg_Execution_Time,main="Top 10 Slowest Methods",xlab="Function Name",names.arg=slowest_exe_time$Function_Name,ylab="Avg Ex Time (usec)",cex.names=0.75,las=2)