@echo off

if %1 == /b (
  mkdir C:\\bkp
  xcopy C:\\HISHTPService\* C:\\bkp /s /e
)

if %1 == /r (
  xcopy C:\\bkp\* C:\\HISHTPService /s /e /y
  rmdir C:\\bkp /S /Q 
)