@echo off
REM Peroxide CSS Build Script
REM 将5个CSS文件拼接成一个完整的peroxide.css文件

echo Start building Peroxide Release...
echo.

REM 清空输出文件
if exist peroxide.css del peroxide.css

REM 逐个读取并拼接CSS文件
echo /* === Variables.css === */ >> peroxide.css
type CSS\Variables.css >> peroxide.css
echo. >> peroxide.css
echo /* === 结束 Variables.css === */ >> peroxide.css
echo. >> peroxide.css

echo /* === Base.css === */ >> peroxide.css
type CSS\Base.css >> peroxide.css
echo. >> peroxide.css
echo /* === 结束 Base.css === */ >> peroxide.css
echo. >> peroxide.css

echo /* === Elements.css === */ >> peroxide.css
type CSS\Elements.css >> peroxide.css
echo. >> peroxide.css
echo /* === 结束 Elements.css === */ >> peroxide.css
echo. >> peroxide.css

echo /* === Capabilities.css === */ >> peroxide.css
type CSS\Capabilities.css >> peroxide.css
echo. >> peroxide.css
echo /* === 结束 Capabilities.css === */ >> peroxide.css
echo. >> peroxide.css

echo /* === Localization.css === */ >> peroxide.css
type CSS\Localization.css >> peroxide.css
echo. >> peroxide.css
echo /* === 结束 Localization.css === */ >> peroxide.css
echo. >> peroxide.css

echo.
echo Build complete. Output file: peroxide.css
echo Press any key to exit.
pause > nul