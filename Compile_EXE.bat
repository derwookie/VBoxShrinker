:: Clear the last dist to avoid duplications
rmdir /s /q dist
del shrink.spec

REM Build the new .exe-file out of the original script
pyinstaller -c -F -i icon.ico shrink.py

:: Clear the build-directories
rmdir /s /q __pycache__
rmdir /s /q build

:: Copy the Icon into the final directory
xcopy /v /y icon.ico .\dist

REM ".exe con be found in ./dist"
pause