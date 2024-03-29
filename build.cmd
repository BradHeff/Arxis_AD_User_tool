@ECHO off

python updateSettings.py
python update_version.py %3
python preBuild.py

if '%username%' == 'bheffernan' goto work
if '%username%' == 'brad.heffernan' goto home

goto ender

:home
pyinstaller.exe --clean --noconfirm --onefile --distpath="scrap/dist" --workpath="scrap/build" --name=%1 --hidden-import="ldap3" --hidden-import="ttkbootstrap" --icon="icon.ico" --version-file="version.rc" %2
exit

:work
pyinstaller.exe --clean --noconfirm --onefile --distpath="scrap/dist" --workpath="scrap/build" --name=%1 --hidden-import="ldap3" --hidden-import="ttkbootstrap" --icon="icon.ico" --version-file="version.rc" %2


:ender
exit
