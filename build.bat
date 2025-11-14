@echo off
setlocal

set "p=%~p0"
for %%A in (%p:\= %) do set "folder=%%~A"

:: Clean the old folder
rmdir /s /q dist
rmdir /s /q build
for /d %%i in (*.egg-info) do rmdir /s /q "%%i"
rmdir /s /q __pycache__

:: Run the Build
python setup.py sdist bdist_wheel
if errorlevel 1 (
    sendgrowl %folder% BuildEvent "Build Failed" "An error occurs when building package!" -p 2
    exit /b 1
)

:: Upload ke repository
twine upload dist\* -r pypihub
if errorlevel 1 (
    sendgrowl %folder% UploadEvent "Upload Failed" "Failed to upload to the pypi!" -p 2
    exit /b 1
)

twine upload dist\*
if errorlevel 1 (
    sendgrowl %folder% UploadEvent "Upload Failed" "Failed to upload to Pypi Default!" -p 2
    exit /b 1
)

:: If everything works
sendgrowl %folder% BuildEvent "Build Success" "Build and Upload SUCCESSFUL!" -p 0

endlocal
