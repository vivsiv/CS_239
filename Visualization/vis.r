args <- commandArgs(TRUE)
output <- paste(args[2],basename(args[1]),sep="\\")
dir.create(output, showWarnings = FALSE)

# Read data from the .csv file
data <- read.csv(file=args[1],sep=",",head=TRUE)

#par(mfrow = c(2,2),mar=c(8.5,6.5,2,2))

img1 <- paste(output,"\\1_fast_exe_time.png",sep="")
png(img1,units="px",width=1600,height=1600,res=300)
par(mar=c(9,5,3,3))
# Bar plot for top 10 fastest methods
order.exe_time_asc <- order(data$Avg_Execution_Time)
sorted_exe_time_asc <- data[order.exe_time_asc,]
pos_exe_time_asc <- sorted_exe_time_asc[sorted_exe_time_asc$Avg_Execution_Time > 0,]
fastest_exe_time <- head(pos_exe_time_asc,10)
plt1 <- barplot(fastest_exe_time$Avg_Execution_Time,main="Top 10 Fastest Methods",ylab="Avg Ex Time (usec)",ylim=c(0,1.2*max(unlist(fastest_exe_time$Avg_Execution_Time))),col=rainbow(10))
text(plt1, par("usr")[3], labels = fastest_exe_time$Function_Name, srt = 45, adj = c(1,1.1), xpd = TRUE, cex=0.6)
text(plt1, fastest_exe_time$Avg_Execution_Time, labels = round(fastest_exe_time$Avg_Execution_Time,1), srt = 45, pos = 3, cex=0.5)

img2 <- paste(output,"\\2_slow_exe_time.png",sep="")
png(img2,units="px",width=1600,height=1600,res=300)
par(mar=c(9,8,2,2))
# Bar plot for 10 slowest methods
order.exe_time_desc <- order(data$Avg_Execution_Time, decreasing=TRUE)
sorted_exe_time_desc <- data[order.exe_time_desc,]
slowest_exe_time <- head(sorted_exe_time_desc,10)
plt2 <- barplot(slowest_exe_time$Avg_Execution_Time,main="Top 10 Slowest Methods",ylab="Avg Ex Time (usec)",ylim=c(0,1.2*max(unlist(slowest_exe_time$Avg_Execution_Time))),col=rainbow(10))
text(plt2, par("usr")[3], labels = slowest_exe_time$Function_Name, srt = 45, adj = c(1,1.1), xpd = TRUE, cex=0.6)
text(plt2, slowest_exe_time$Avg_Execution_Time, labels = round(slowest_exe_time$Avg_Execution_Time,1), srt = 45, pos = 3, cex=0.5)

img3 <- paste(output,"\\3_freq_call_method.png",sep="")
png(img3,units="px",width=1600,height=1600,res=300)
par(mar=c(9,8,2,2))
# Bar plot for top 10 most frequent methods
order.num_calls_desc <- order(data$Num_Calls, decreasing=TRUE)
sorted_num_calls_desc <- data[order.num_calls_desc,]
most_num_calls <- head(sorted_num_calls_desc,10)
plt3 <- barplot(most_num_calls$Num_Calls,main="Top 10 Frequent Methods",ylab="Number of Calls",ylim=c(0,1.2*max(unlist(most_num_calls$Num_Calls))),col=rainbow(10))
text(plt3, par("usr")[3], labels = most_num_calls$Function_Name, srt = 45, adj = c(1,1.1), xpd = TRUE, cex=0.6)
text(plt3, most_num_calls$Num_Calls, labels = round(most_num_calls$Num_Calls,1), srt = 45, pos = 3, cex=0.5)

img4 <- paste(output,"\\4_freq_call_stack.png",sep="")
png(img4,units="px",width=1600,height=1600,res=300)
par(mar=c(9,8,2,2))
# Bar plot for top 10 most frequent call stacks
order.num_calls_desc <- order(data$Num_Calls, decreasing=TRUE)
sorted_num_calls_desc <- data[order.num_calls_desc,]
call_stack_desc <- sorted_num_calls_desc[sorted_num_calls_desc$Parent_Name == "None",]
most_call_stack <- head(call_stack_desc,10)
plt4 <- barplot(most_call_stack$Num_Calls,main="Top 10 Frequent Call Stacks",ylab="Number of Calls",ylim=c(0,1.2*max(unlist(most_call_stack$Num_Calls))),col=rainbow(10))
text(plt4, par("usr")[3], labels = most_call_stack$Function_Name, srt = 45, adj = c(1,1.1), xpd = TRUE, cex=0.6)
text(plt4, most_call_stack$Num_Calls, labels = round(most_call_stack$Num_Calls,1), srt = 45, pos = 3, cex=0.5)

img5 <- paste(output,"\\5_slow_call_stack.png",sep="")
png(img5,units="px",width=1600,height=1600,res=300)
par(mar=c(9,8,2,2))
#Bar plot for top 10 slowest call stacks
order.exe_time_desc <- order(data$Avg_Execution_Time, decreasing=TRUE)
sorted_exe_time_desc <- data[order.exe_time_desc,]
sorted_call_stack_exe_desc <- sorted_exe_time_desc[sorted_exe_time_desc$Parent_Name == "None",]
slowest_call_stack <- head(sorted_call_stack_exe_desc,10)
plt5 <- barplot(slowest_call_stack$Avg_Execution_Time,main="Top 10 Slowest Call Stacks",ylab="Avg Ex Time (usec)",ylim=c(0,1.2*max(unlist(slowest_call_stack$Avg_Execution_Time))),col=rainbow(10))
text(plt5, par("usr")[3], labels = slowest_call_stack$Function_Name, srt = 45, adj = c(1,1.1), xpd = TRUE, cex=0.6)
text(plt5, slowest_call_stack$Avg_Execution_Time, labels = round(slowest_call_stack$Avg_Execution_Time,1), srt = 45, pos = 3, cex=0.5)

img6 <- paste(output,"\\6_fast_call_stack.png",sep="")
png(img6,units="px",width=1600,height=1600,res=300)
par(mar=c(9,8,2,2))
#Bar plot for top 10 fastest call stacks
order.exe_time_asc <- order(data$Avg_Execution_Time)
sorted_exe_time_asc <- data[order.exe_time_asc,]
sorted_call_stack_exe_asc <- sorted_exe_time_asc[sorted_exe_time_asc$Parent_Name == "None",]
fastest_call_stack <- head(sorted_call_stack_exe_asc,10)
plt6 <- barplot(fastest_call_stack$Avg_Execution_Time,main="Top 10 Fastest Call Stacks",ylab="Avg Ex Time (usec)",ylim=c(0,1.2*max(unlist(fastest_call_stack$Avg_Execution_Time))),col=rainbow(10))
text(plt6, par("usr")[3], labels = fastest_call_stack$Function_Name, srt = 45, adj = c(1,1.1), xpd = TRUE, cex=0.6)
text(plt6, fastest_call_stack$Avg_Execution_Time, labels = round(fastest_call_stack$Avg_Execution_Time,1), srt = 45, pos = 3, cex=0.5)


dev.off()