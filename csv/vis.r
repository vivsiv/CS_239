data <- read.csv(file="myClass_out.csv",sep=",",head=TRUE)
plot(data$Function.Name,data$Avg.Execution.Time..usec.,xlab="Function Name",ylab="Avg. Ex Time (usec)")
plot(data$Call.Stack,data$Avg.Execution.Time..usec.,xlab="Call Stack",ylab="Avg. Ex Time (usec)")
barplot(data$Avg.Execution.Time..usec.,xlab="Function Name",names.arg=data$Function.Name,ylab="Avg. Ex Time (usec)")