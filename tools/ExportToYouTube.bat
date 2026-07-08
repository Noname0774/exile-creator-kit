@echo off
setlocal

if "%~1"=="" (
    echo Drag and drop a video file onto ExportToYouTube.bat.
    echo No video file was provided.
    pause
    exit /b 1
)

cd /d "%~dp0.."
python tools\export_to_youtube.py "%~1"

pause
