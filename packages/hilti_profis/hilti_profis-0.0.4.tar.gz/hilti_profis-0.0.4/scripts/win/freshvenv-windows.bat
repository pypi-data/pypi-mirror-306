@echo off
echo "Navigating to Root Dir"
cd /d %~dp0
cd ..\..

if not exist pyproject.toml (
    echo "Error: pyproject.toml not found in the current directory."
    exit /b 1
) else (
    echo "pyproject.toml found. Continuing with the script."
)

echo "Clearing old `.venv`"
RD /S /Q .venv

echo "Creating new `.venv`"
python -m venv .venv
call .venv\Scripts\activate.bat

echo "Installing dependencies"
python.exe -m pip install --upgrade pip
pip install flit
flit install --pth-file
