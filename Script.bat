@echo off

REM Define la variable de entrada para el archivo de URLs
set input_file=urls.txt
setlocal enabledelayedexpansion

REM Inicializa una variable para las URLs
set urls=

REM Lee el archivo y agrega las URLs a la variable 'urls'
for /f "delims=" %%a in (%input_file%) do (
    REM Ignora líneas vacías
    if not "%%a"=="" (
        set "urls=!urls! %%a"
    )
)

REM Ejecuta el script de Python con las URLs como parámetros
python ScrappingCompatibilidadesPython.py %urls%
