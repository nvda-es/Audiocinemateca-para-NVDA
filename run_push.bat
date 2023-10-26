@cls
@echo off
scons --clean
git init
git add --all
git commit -m "Añadida búsqueda por Javi y preparación del código para NVDA 2024"
git push -u origin master
pause