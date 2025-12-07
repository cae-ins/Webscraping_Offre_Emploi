@echo OFF
rem Define the path to your Anaconda installation
set CONDA_PATH=%CONDA_EXE%
rem Define the name of the base environment
set ENVNAME=WebScraping_OJA

rem Activate the base environment
call %CONDAPATH%\Scripts\activate.bat %CONDAPATH%

rem Run a Python script in that environment
python C:\Users\Dell\Documents\UB\IPC\CODE_IPC\SCRAPPE_SE\script_scrapping_nettoyage_offre_main.py

rem Deactivate the environment
call conda deactivate

rem Pause to keep the window open
pause
