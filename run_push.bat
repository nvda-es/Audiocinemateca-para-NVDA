@cls
@echo off
scons --clean
git init
git add --all
git commit -m "Corregida versión 1.1"
git push -u origin master
pause