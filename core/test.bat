REM  @py.exe "C:\Users\Ana Ash\Desktop\skrapy3\project\core\schedule_task.py" %*
REM  pause
SchTasks /Create /SC DAILY /TN “My Task” /TR “C:\Windows\System32\calc.exe” /ST 09:00
pause