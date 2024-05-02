@echo OFF
rem Define the path to your Anaconda installation
set CONDAPATH=C:\Users\dell\anaconda3
rem Define the name of the base environment
rem set ENVNAME=base

rem Activate the base environment
call %CONDAPATH%\Scripts\activate.bat %CONDAPATH%

rem Run a Python script in that environment
python C:\Users\Dell\Documents\UB\IPC\CODE_IPC\SCRAPPE_SE\script_scrapping_nettoyage_offre_main.py

rem Deactivate the environment
call conda deactivate

rem Pause to keep the window open
pause
