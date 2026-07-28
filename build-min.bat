@echo off
setlocal
chcp 65001 >nul 2>nul

set "SCRIPT=%~dp0build_min.py"

REM 探测 Python 解释器
REM 不使用命令链接符，改用 if errorlevel 写法，以兼容未完整实现 cmd 语法的 IDE 内置终端。
set "PYEXE="

where py >nul 2>nul
if not errorlevel 1 set "PYEXE=py"

if not defined PYEXE (
    where python >nul 2>nul
    if not errorlevel 1 set "PYEXE=python"
)

if not defined PYEXE (
    where python3 >nul 2>nul
    if not errorlevel 1 set "PYEXE=python3"
)

if not defined PYEXE (
    echo 未找到 Python 解释器，请先安装 Python 3 或使用 py 启动器，并确保其在 PATH 中。
    pause
    exit /b 1
)

"%PYEXE%" "%SCRIPT%" %*
if errorlevel 1 (
    echo.
    echo 构建失败，错误码 %errorlevel%
    pause
    exit /b %errorlevel%
)

echo.
echo 构建完成，已生成 peroxide.min.css
pause
