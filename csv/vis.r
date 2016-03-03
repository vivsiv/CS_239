data <- read.csv(file="myClass_out.csv",sep=",",head=TRUE)

# par(mfrow = c(2,2))
par(mfrow = c(2,3),mar=c(8.5,6.5,2,2))
#Bar plot for top 10 fastest methods
order.exe_time_asc <- order(data$Avg_Execution_Time)
sorted_exe_time_asc <- data[order.exe_time_asc,]
pos_exe_time_asc <- sorted_exe_time_asc[sorted_exe_time_asc$Avg_Execution_Time > 0,]
fastest_exe_time <- head(pos_exe_time_asc,10)
plt1 <- barplot(fastest_exe_time$Avg_Execution_Time,main="Top 10 Fastest Methods",ylab="Avg Ex Time (usec)")
text(plt1, par("usr")[3], labels = fastest_exe_time$Function_Name, srt = 45, adj = c(1,1.1), xpd = TRUE, cex=0.8)
text(plt1, fastest_exe_time$Avg_Execution_Time, labels = round(fastest_exe_time$Avg_Execution_Time,1), pos = 3, cex=0.5)

#Bar plot for 10 slowest methods
order.exe_time_desc <- order(data$Avg_Execution_Time, decreasing=TRUE)
sorted_exe_time_desc <- data[order.exe_time_desc,]
slowest_exe_time <- head(sorted_exe_time_desc,10)
plt2 <- barplot(slowest_exe_time$Avg_Execution_Time,main="Top 10 Slowest Methods",ylab="Avg Ex Time (usec)")
text(plt2, par("usr")[3], labels = slowest_exe_time$Function_Name, srt = 45, adj = c(1,1.1), xpd = TRUE, cex=0.8)
text(plt2, slowest_exe_time$Avg_Execution_Time, labels = round(slowest_exe_time$Avg_Execution_Time,1), pos = 3, cex=0.5)

#Bar plot for top 10 most frequent methods
order.num_calls_desc <- order(data$Num_Calls, decreasing=TRUE)
sorted_num_calls_desc <- data[order.num_calls_desc,]
most_num_calls <- head(sorted_num_calls_desc,10)
plt3 <- barplot(most_num_calls$Num_Calls,main="Top 10 Frequent Methods",ylab="Number of Calls")
text(plt3, par("usr")[3], labels = most_num_calls$Function_Name, srt = 45, adj = c(1,1.1), xpd = TRUE, cex=0.8)
text(plt3, most_num_calls$Num_Calls, labels = round(most_num_calls$Num_Calls,1), pos = 3, cex=0.5)

#Bar plot for top 10 most frequent call stacks
order.num_calls_desc <- order(data$Num_Calls, decreasing=TRUE)
sorted_num_calls_desc <- data[order.num_calls_desc,]
call_stack_desc <- sorted_num_calls_desc[sorted_num_calls_desc$Parent_Name == "None",]
most_call_stack <- head(call_stack_desc,10)
plt4 <- barplot(most_call_stack$Num_Calls,main="Top 10 Frequent Call Stacks",ylab="Number of Calls")
text(plt4, par("usr")[3], labels = most_call_stack$Function_Name, srt = 45, adj = c(1,1.1), xpd = TRUE, cex=0.8)
text(plt4, most_call_stack$Num_Calls, labels = round(most_call_stack$Num_Calls,1), pos = 3, cex=0.5)

#Bar plot for top 10 most frequent call stacks
order.num_calls_desc <- order(data$Num_Calls, decreasing=TRUE)
sorted_num_calls_desc <- data[order.num_calls_desc,]
call_stack_desc <- sorted_num_calls_desc[sorted_num_calls_desc$Parent_Name == "None",]
most_call_stack <- head(call_stack_desc,10)
plt4 <- barplot(most_call_stack$Num_Calls,main="Top 10 Frequent Call Stacks",ylab="Number of Calls")
text(plt4, par("usr")[3], labels = most_call_stack$Function_Name, srt = 45, adj = c(1,1.1), xpd = TRUE, cex=0.8)
text(plt4, most_call_stack$Num_Calls, labels = round(most_call_stack$Num_Calls,1), pos = 3, cex=0.5)

#Bar plot for top 10 slowest call stacks
order.exe_time_desc <- order(data$Avg_Execution_Time, decreasing=TRUE)
sorted_exe_time_desc <- data[order.exe_time_desc,]
sorted_call_stack_exe_desc <- sorted_exe_time_desc[sorted_exe_time_desc$Parent_Name == "None",]
slowest_call_stack <- head(sorted_call_stack_exe_desc,10)
plt5 <- barplot(slowest_call_stack$Avg_Execution_Time,main="Top 10 Slowest Call Stacks",ylab="Avg Ex Time (usec)")
text(plt5, par("usr")[3], labels = slowest_call_stack$Function_Name, srt = 45, adj = c(1,1.1), xpd = TRUE, cex=0.8)
text(plt5, slowest_call_stack$Avg_Execution_Time, labels = round(slowest_call_stack$Avg_Execution_Time,1), pos = 3, cex=0.5)

#Bar plot for top 10 fastest call stacks
order.exe_time_asc <- order(data$Avg_Execution_Time)
sorted_exe_time_asc <- data[order.exe_time_asc,]
sorted_call_stack_exe_asc <- sorted_exe_time_asc[sorted_exe_time_asc$Parent_Name == "None",]
fastest_call_stack <- head(sorted_call_stack_exe_asc,10)
plt5 <- barplot(fastest_call_stack$Avg_Execution_Time,main="Top 10 Fastest Call Stacks",ylab="Avg Ex Time (usec)")
text(plt5, par("usr")[3], labels = fastest_call_stack$Function_Name, srt = 45, adj = c(1,1.1), xpd = TRUE, cex=0.8)
text(plt5, fastest_call_stack$Avg_Execution_Time, labels = round(fastest_call_stack$Avg_Execution_Time,1), pos = 3, cex=0.5)