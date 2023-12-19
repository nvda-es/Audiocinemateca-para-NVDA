@cls
@echo off
scons --clean
git init
git add --all
git commit -m "v1.2 ctypes add"
git push -u origin master
pause