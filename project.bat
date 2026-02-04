@echo off
chcp 65001 >nul

if not exist .\Backup mkdir .\Backup
if not exist .\In mkdir .\In
if not exist .\Out mkdir .\Out

rem Prompt for number of table states (non-negative integer)
echo Enter the number of table states to generate:
:askCount
set /p n="> "
set "n=%n: =%"
if not defined n (
  echo Please enter a non-negative integer.
  goto askCount
)
echo %n%|findstr /R "^[0-9][0-9]*$" >nul || (
  echo Please enter a non-negative integer.
  goto askCount
)

rem Prompt for weight (non-negative float)
echo Enter the weight (non-negative real number):
:askWeight
set /p w="> "
set "w=%w: =%"
if not defined w (
  echo Please enter a non-negative real number.
  goto askWeight
)
rem Accept integers (e.g., 2) or decimals (e.g., 2.5)
echo %w%|findstr /R "^[0-9][0-9]*$" >nul && goto weightOk
echo %w%|findstr /R "^[0-9][0-9]*\.[0-9][0-9]*$" >nul && goto weightOk
echo Please enter a non-negative real number.
goto askWeight

:weightOk
echo Running the main script
python main.py "%n%" "%w%"

echo Creating the report and adding it to the Backup directory
python backup_script.py

echo Opening the latest report
start "" LastRaport.html

pause