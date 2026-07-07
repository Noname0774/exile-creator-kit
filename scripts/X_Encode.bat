@echo off
chcp 65001 >nul
title POE2 X Encoder

if "%~1"=="" (
    echo.
    echo ==========================================
    echo  動画をこのファイルへドラッグしてください
    echo ==========================================
    pause
    exit
)

set "INPUT=%~1"
set "NAME=%~n1"
set "OUTPUT=D:\POE2\X\%NAME%_X.mp4"

echo.
echo ==========================================
echo      PoE2 Creator Kit - X Encoder
echo ==========================================
echo.
echo 入力:
echo %INPUT%
echo.
echo 出力:
echo %OUTPUT%
echo.

ffmpeg -y ^
-i "%INPUT%" ^
-c:v h264_nvenc ^
-preset p7 ^
-rc vbr ^
-b:v 7M ^
-maxrate 9M ^
-bufsize 18M ^
-profile:v high ^
-pix_fmt yuv420p ^
-c:a aac ^
-b:a 192k ^
"%OUTPUT%"

echo.
echo ==========================================
echo        エンコード完了！
echo ==========================================
echo.

explorer "D:\POE2\X"
pause