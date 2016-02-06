@echo off

:: Change to cuurent working directory
cd /D %~dp0%
echo.

:: Compile our instrumentation tool
javac -cp .;.\lib\asm-all-5.0.4.jar;.\lib\jsoup-1.8.3.jar ASM_Instrument_Tool.java
echo.

java -cp .;.\lib\asm-all-5.0.4.jar;.\lib\jsoup-1.8.3.jar ASM_Instrument_Tool E:\\Courses\\Winter2016\\CS239\\PartA\\Targets\\jsoup_example\\jsoup-master\\src\\main\\java E:\\Courses\\Winter2016\\CS239\\PartA\\Targets\\jsoup_example\\jsoup-instrumented\main
echo.


pause