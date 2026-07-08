@echo off
setlocal

if "%~1"=="" (
    echo Drag and drop a video file onto ValidateMedia.bat.
    echo No video file was provided.
    pause
    exit /b 1
)

cd /d "%~dp0.."
python tools\validate_media_inspector.py "%~1"

pause
