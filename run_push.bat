@cls
@echo off
scons --clean
git init
git add --all
git commit -m "v1.3"
git push -u origin master
pause