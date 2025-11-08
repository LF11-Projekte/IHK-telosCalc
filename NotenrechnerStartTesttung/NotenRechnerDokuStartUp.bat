@echo off
Title: NotenRechner Dokumentation Installieren
SET VENV_NAME=venv
SET PROJECT_NAME=NotenRechner

python -m venv %VENV_NAME%

call %VENV_NAME%\Scripts\activate.bat

cd C:\Users\d22weissenbornka

if not exist %PROJECT_NAME% mkdir %PROJECT_NAME%
cd %PROJECT_NAME%
REM Navigated to %PROJECT_NAME%

pip install mkdocs

REM for design
pip install mkdocs-material

mkdocs new .

REM for using the design

REM used design

del mkdocs.yml
REM deletet yml


copy "C:\Users\d22weissenbornka\testung karl\mkdocs.yml" "C:\Users\d22weissenbornka\%PROJECT_NAME%"
REM copied yml


cd C:\Users\d22weissenbornka\NotenrechnerStartTesttung\needed
START StartMkDocsWebsite.bat

cd C:\Users\d22weissenbornka\NotenRechner

mkdocs serve



