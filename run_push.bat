@cls
@echo off
scons --clean
git init
git add --all
git commit -m "Corregido al pulsar intro en cuadro de texto en el dialogo ir a la posición"
git push -u origin master
pause