@cls
@echo off
scons --clean
git init
git add --all
git commit -m "release 1.1"
git push -u origin master
git tag 1.1
git push --tags
pause