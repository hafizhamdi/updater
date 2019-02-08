@echo off
:: mergePdfs.bat

:: C:\HISHTPService\bin
SET BASE_DIR=%1
SET FILE_ID=%2
ECHO [%date%,%time%] START. >> %BASE_DIR%\\tmp\\merge.log
ECHO [%date%,%time%] PROCESSING... >> %BASE_DIR%\\tmp\\merge.log
%BASE_DIR%\\bin\\pdftk.exe %BASE_DIR%\\tmp\\%FILE_ID%*.pdf output %BASE_DIR%\\tmp\\%FILE_ID%_comb.pdf
ECHO [%date%,%time%] DONE. >> %BASE_DIR%\\tmp\\merge.log