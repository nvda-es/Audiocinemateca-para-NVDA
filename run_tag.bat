@cls
@echo off
scons --clean
git init
git add --all
git commit -m "release 1.0"
git push -u origin master
git tag 1.0
git push --tags
pause