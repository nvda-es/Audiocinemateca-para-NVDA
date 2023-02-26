@cls
@echo off
scons --clean
git init
git add --all
git commit -m "Ahora la gui se vuelve a cargar cuando se actualiza la base de datos"
git push -u origin master
pause