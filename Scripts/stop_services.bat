@echo off

%cd%\nssm.exe stop "HISHTP Service"

%cd%\nssm.exe stop "Print Watcher"