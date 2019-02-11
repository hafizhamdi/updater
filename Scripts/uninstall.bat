@echo off

%cd%\nssm.exe stop "Print Watcher"

%cd%\nssm.exe remove "Print Watcher" confirm

%cd%\nssm.exe stop "HTP Updater"

%cd%\nssm.exe remove "HTP Updater" confirm

set path=C:\Windows\Microsoft.NET\Framework\v4.0.30319
echo %path%
if not exist %path% ( 
	echo msgbox "Microsoft .NET Framework v4.7 is not installed in this system. Update or Install to continue" > "%temp%\msgbox.vbs" 
	wscript.exe "%temp%\msgbox.vbs"
) else (
	REM Uninstall existing service
    %path%\InstallUtil.exe /u %cd%\ServiceConsole.exe
	echo OK.
)


