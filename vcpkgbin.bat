@echo off
set "ConanUrl=https://github.com/conan-io/conan.git"
set "ConanDir=%~d0\Software\conans"

echo. & echo Installing/updating Conan...
call :BootstrapConan "%ConanUrl%" "%ConanDir%"
if %errorlevel% neq 0 echo An error occured in %~n0, bailing out & exit /b %errorlevel%
echo. & echo conan % successfully installed...

call :WriteConanScript "%ConanDir%"
set "Path=%Path%;%ConanDir%;%programfiles%\7-Zip"
set "PYTHONPATH=%ConanDir%"

call python conan_script\vcpkgbin.py %*

goto :eof

:BootstrapConan
setlocal
	set "LocConanGitUrl=https://github.com/conan-io/conan.git"
	set "LocConanDir=%~d0\Software\conans"
	
    echo Checking for existence of "%LocConanDir%"...
    if not exist "%LocConanDir%" (
        echo Attempt to: git clone "%LocConanGitUrl%" "%LocConanDir%"...
        git clone "%LocConanGitUrl%" "%LocConanDir%"
		pip install -r %LocConanDir%/conans/requirements.txt
    )
	
	if %errorlevel% neq 0 echo An error occured in %~n0, bailing out & exit /b %errorlevel%
	
    pushd "%LocConanDir%"
    if %errorlevel% neq 0 echo An error occured in %~n0, bailing out & exit /b %errorlevel%

    popd
endlocal & exit /b %errorlevel%

goto :eof

:WriteConanScript
setlocal
    set "ConanDir=%~1"

	echo #!/usr/bin/env python > %ConanDir%\conan.py
	echo import sys >> %ConanDir%\conan.py
	echo conan_sources_dir = '%ConanDir%' >> %ConanDir%\conan.py

	echo sys.path.insert(1, conan_sources_dir) >> %ConanDir%\conan.py
	echo # Or append to sys.path to prioritize a binary installation before the source code one >> %ConanDir%\conan.py
	echo # sys.path.append(conan_sources_dir) >> %ConanDir%\conan.py

	echo from conans.conan import main >> %ConanDir%\conan.py
	echo main(sys.argv[1:]) >> %ConanDir%\conan.py
	echo call python %ConanDir%\conan.py %%* > %ConanDir%\conan.bat 
	
endlocal & exit /b %errorlevel%

goto :eof
