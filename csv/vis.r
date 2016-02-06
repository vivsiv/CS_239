data <- read.csv(file="myClass_out.csv",sep=",",head=TRUE)
plot(data$Function_Name,data$Avg_Execution_Time,xlab="Function Name",ylab="Avg Ex Time (usec)")
plot(data$Call_Stack,data$Avg_Execution_Time,xlab="Call Stack",ylab="Avg Ex Time (usec)")
barplot(data$Avg_Execution_Time,xlab="Function Name",names.arg=data$Function_Name,ylab="Avg Ex Time (usec)")