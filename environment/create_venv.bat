 @echo off
REM Set the conda path from the OS environment variable
set CONDA_PATH=%CONDA_EXE%

REM Do something with the conda path
echo %CONDA_PATH%

REM Create conda environment
call conda create -n WebScraping_OJA

REM Activate conda environment
call conda activate WebScraping_OJA

REM Install Python 3.11.5
call conda install python=3.11.5

REM Install pip
call conda install pip

REM Install packages from requirements.txt
call pip install -r requirements.txt

REM Deactivate conda environment
call conda deactivate

        