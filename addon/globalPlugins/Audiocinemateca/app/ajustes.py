# -*- coding: utf-8 -*-
# Copyright (C) 2023 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.

import addonHandler
import globalVars
import os
import sys

addonHandler.initTranslation()

dirGeneral =os.path.join(globalVars.appArgs.configPath, "Audiocinemateca")
if not os.path.exists(dirGeneral):
	try:
		os.mkdir(dirGeneral)
	except:
		pass

# Banderas generales
IS_WinON = False
IS_LOGIN = False
IS_BASE = False
IS_HABLAR = True
# Configuración login
usuario = ""
contraseña = ""
# Configuración baneo
IS_BANEO = False
intentosBaneo = 0
fechaIntento = None
fechaBaneo = None
# version base datos
versionLocal = None
# Configuración General
volumen = 50 # Volumen por defecto de reproducción
listaVelocidad = ["0.75", "0.80", "0.85", "0.90", "0.95", "1.0", "1.05", "1.10", "1.15", "1.20", "1.25", "1.30", "1.35", "1.40", "1.45", "1.50", "1.75", "2.0"]
velocidad = 5 # Velocidad de reproducción pertenece a la posición de la lista listaVelocidad
listaAtrasar = [_("1 segundo"), _("5 segundos"), _("15 segundos"), _("30 segundos"), _("1 minuto")]
atrasar = 2 # Atrasa la reproducción pertenece a la posición de la lista listaAtrasar
listaAdelantar = [_("1 segundo"), _("5 segundos"), _("15 segundos"), _("30 segundos"), _("1 minuto"), _("5 minutos"), _("10 minutos"), _("15 minutos")]
adelantar = 3 # Adelanta la reproducción pertenece a la posición de la lista listaAdelantar
listaResultados = [_("10 resultados"), _("15 resultados"), _("20 resultados"), _("25 resultados")]
resultados = 0
# Diccionario para el tiempo atrasar - adelantar en segundos
dict_tiempo = {
	0:1,
	1:5,
	2:15,
	3:30,
	4:60,
	5:300,
	6:600,
	7:900,
}
# Diccionario para resultados
dict_resultados = {
	0: 10,
	1: 15,
	2: 20,
	3: 25,
}