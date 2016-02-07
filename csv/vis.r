data <- read.csv(file="batch_out.csv",sep=",",head=TRUE)

#Bar plot for top 10 fastest methods
order.avg_exe_time <- order(data$Avg_Execution_Time)
sorted_avg_exe <- data[order.avg_exe_time,]
top_10_avg_exe <- head(sorted_avg_exe,10)
barplot(top_10_avg_exe$Avg_Execution_Time,main="Top 10 Fastest Methods",xlab="Function Name",names.arg=top_10_avg_exe$Function_Name,ylab="Avg Ex Time (usec)")

#plot(data$Function_Name,data$Avg_Execution_Time,xlab="Function Name",ylab="Avg Ex Time (usec)")
#plot(data$Call_Stack,data$Avg_Execution_Time,xlab="Call Stack",ylab="Avg Ex Time (usec)")