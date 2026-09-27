@echo off
REM ============================================================
REM One-click single-file exe build script (build-exe.bat)
REM Output: build\LogParser-<version>-x64.exe (standalone, zero external DLL deps)
REM
REM The actual pipeline is in scripts\build-exe.mjs:
REM   frontend build - cargo build (custom-protocol + crt-static)
REM   - copy to build\ - PE import table check - asset embed check
REM
REM Usage:
REM   Double-click this file, or run: build-exe.bat [args]
REM   --skip-frontend   skip frontend build (Rust iteration only)
REM   --no-pause        do not pause at the end (CI / CLI usage)
REM NOTE: keep this file pure ASCII - cmd parses it safely on any codepage
REM ============================================================
setlocal

REM cd to script directory (project root), works from any location
cd /d "%~dp0"

set "NO_PAUSE="
set "MJS_ARGS="

:parse_args
if "%~1"=="" goto after_args
if /i "%~1"=="--no-pause" set "NO_PAUSE=1"
if /i not "%~1"=="--no-pause" set "MJS_ARGS=%MJS_ARGS% %~1"
shift
goto parse_args
:after_args

REM --- check: Node.js ---
where node >nul 2>nul
if errorlevel 1 (
  echo [build-exe] ERROR: node not found. Install Node.js ^>= 20 first.
  goto fail
)

REM --- check: cargo, auto-add ~/.cargo/bin to PATH if missing ---
where cargo >nul 2>nul
if errorlevel 1 (
  if exist "%USERPROFILE%\.cargo\bin\cargo.exe" (
    set "PATH=%USERPROFILE%\.cargo\bin;%PATH%"
    echo [build-exe] cargo added to PATH automatically
  ) else (
    echo [build-exe] ERROR: cargo not found. Install Rust MSVC toolchain:
    echo         rustup default stable-x86_64-pc-windows-msvc
    goto fail
  )
)

REM cargo uses rsproxy mirror (direct connection), clear proxies to avoid interference
set "https_proxy="
set "http_proxy="

echo [build-exe] environment ready, building...
echo.

node scripts\build-exe.mjs %MJS_ARGS%
if errorlevel 1 goto fail

echo.
echo [build-exe] ===== DONE =====
echo [build-exe] output is in build\ directory - standalone single-file exe
if not defined NO_PAUSE pause
exit /b 0

:fail
echo.
echo [build-exe] ===== BUILD FAILED =====
echo [build-exe] see error messages above
if not defined NO_PAUSE pause
exit /b 1
