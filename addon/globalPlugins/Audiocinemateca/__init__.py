# -*- coding: utf-8 -*-
# Copyright (C) 2023 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.

import globalPluginHandler
import addonHandler
import globalVars
import gui
import ui
import config
import core
from scriptHandler import script
from logHandler import log
import json
import wx
import os
import sys
from threading import Thread
from .app.lib import vlclib_reproductor
from .app.main import *
from .app.basedatos import *

addonHandler.initTranslation()

def disableInSecureMode(decoratedCls):
	if globalVars.appArgs.secure:
		return globalPluginHandler.GlobalPlugin
	return decoratedCls

@disableInSecureMode
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(GlobalPlugin, self).__init__()

		self.AjustesApp = None
		self.reproductor = None
		self.reproductorKeyboard = None
		self.datos = None
		self.categoriaBusqueda = [0, 0, 0, 0]
		if hasattr(globalVars, "audiocinemateca_nvda"):
			self.postStartupHandler()
		core.postNvdaStartup.register(self.postStartupHandler)
		globalVars.audiocinemateca_nvda = None

	def postStartupHandler(self):
		Thread(target=self.inicio, daemon = True).start()

	def inicio(self):
		self.AjustesApp = AjustesApp()
		self.AjustesApp.CargaDatos()
		self.AjustesApp.refrescaDatos()
		self.reproductor = vlclib_reproductor.VlcClassLib()
		self.reproductor.addFrame(self)
		self.reproductorKeyboard = keyboardReproductor()
		self.datos = Inicio_DB(self)
		self.datos.cargaDatos()
		self.datos.cargaVersion()
		self.menu = wx.Menu()
		self.tools_menu = gui.mainFrame.sysTrayIcon.toolsMenu
		self.item1 = self.menu.Append(wx.ID_ANY, _("Iniciar la Audiocinemateca"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.menu_inicio, self.item1)
		self.item2 = self.menu.Append(wx.ID_ANY, _("Opciones"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.menu_opciones, self.item2)
		self.item3 = self.menu.Append(wx.ID_ANY, _("Volver a valores por defecto"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.defecto_Menu, self.item3)
		self.item4 = self.menu.Append(wx.ID_ANY, _("Documentación del complemento"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.documentacion_Menu, self.item4)
		self.audiocinematecaMenu = self.tools_menu.AppendSubMenu(self.menu, _("&Audiocinemateca"))

	def guardarAjustes(self):
		self.AjustesApp.GuardaDatos()
		self.AjustesApp.CargaDatos()
		self.AjustesApp.refrescaDatos()

	def mensaje(self):
		msg = \
_("""La ventana de Audiocinemateca está abierta.

Las teclas para manejar el reproductor de manera externa solo se pueden usar si la pantalla de la Audiocinemateca está cerrada.""")
		return msg
	def terminate(self):
		try:
			core.postNvdaStartup.unregister(self.postStartupHandler)
			self.tools_menu.Remove(self.audiocinematecaMenu)
		except:
			pass
		super().terminate()

	def menu_inicio(self, event):
		self.script_inicio(event, True)

	def menu_opciones(self, event):
		self.script_opciones(event, True)

	def defecto_Menu(self, event):
		msg = \
_("""El complemento solo se puede volver a valores por defecto cuando no está cargada la interfaz y no hay nada reproduciéndose.""")
		if ajustes.IS_WinON:
			gui.messageBox(msg, _("Información"), wx.ICON_INFORMATION)
		else:
			if self.reproductor.estado() in ["State.NothingSpecial", "State.Stopped"]:
				xguiMsg = \
_("""El complemento borrará toda la configuración guardada y volverá a valores por defecto.

¿Está seguro de que desea continuar?""")
				msgx = wx.MessageDialog(None, xguiMsg, "Pregunta", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
				ret = msgx.ShowModal()
				if ret == wx.ID_YES:
					msgx.Destroy
					self.AjustesApp.GuardaDatosDefecto()
					self.AjustesApp.CargaDatos()
					self.AjustesApp.refrescaDatos()
				else:
					msgx.Destroy
			else:
				gui.messageBox(msg)

	def documentacion_Menu(self, event):
		wx.LaunchDefaultBrowser(addonHandler.Addon(os.path.join(os.path.dirname(__file__), "..", "..")).getDocFilePath())

	@script(gesture=None, description= _("Muestra la ventana de Audiocinemateca"), category= "audiocinemateca")
	def script_inicio(self, event, menu=False):
		if ajustes.IS_WinON == False:
			if utilidades.IS_INTERNET():
				if not len(self.datos.resultados_datos):
					if not os.path.exists(ajustes.dirGeneral):
						try:
							os.mkdir(ajustes.dirGeneral)
						except:
							pass
					self.datos.cargaDatos()
					self.datos.cargaVersion()
				HiloComplemento(self, 1).start()
			else:
				ui.message("No se encontró conexión a internet. No es posible iniciar el complemento.")
		else:
			msg = \
_("""Ya hay una instancia de Audiocinemateca abierta.""")
			if menu:
				gui.messageBox(msg, _("Información"), wx.ICON_INFORMATION)
			else:
				ui.message(msg)

	@script(gesture=None, description= _("Muestra la ventana de Opciones"), category= "audiocinemateca")
	def script_opciones(self, event, menu=False):
		if ajustes.IS_WinON == False and self.reproductor.estado() in ["State.NothingSpecial", "State.Stopped"]:
			if not os.path.exists(ajustes.dirGeneral):
				try:
					os.mkdir(ajustes.dirGeneral)
				except:
					pass
			HiloComplemento(self, 2).start()
		else:
			msg = \
_("""La ventana de opciones solo puede ser llamada cuando la interfaz de la Audiocinemateca está cerrada y cuando no hay nada reproduciéndose.""")
			if menu:
				gui.messageBox(msg, _("Información"), wx.ICON_INFORMATION)
			else:
				ui.message(msg)

	@script(gesture=None, description= _("Bajar volumen"), category= "audiocinemateca")
	def script_BajarVolumen(self, event):
		if ajustes.IS_WinON:
			ui.message(self.mensaje())
		else:
			if ajustes.volumen == 0:
				ui.message(_("No se puede bajar más el volumen. Ya se encuentra al 0%"))
			else:
				volTemporal = ajustes.volumen - 1
				ajustes.volumen = volTemporal
				self.reproductor.volumen(ajustes.volumen)
				self.guardarAjustes()
				ui.message(_("Volumen al {}%").format(ajustes.volumen))

	@script(gesture=None, description= _("Subir volumen"), category= "audiocinemateca")
	def script_SubirVolumen(self, event):
		if ajustes.IS_WinON:
			ui.message(self.mensaje())
		else:
			if ajustes.volumen == 100:
				ui.message(_("No se puede subir más el volumen. Ya se encuentra al 100%"))
			else:
				volTemporal = ajustes.volumen + 1
				ajustes.volumen = volTemporal
				self.reproductor.volumen(ajustes.volumen)
				self.guardarAjustes()
				ui.message(_("Volumen al {}%").format(ajustes.volumen))

	@script(gesture=None, description= _("Bajar velocidad"), category= "audiocinemateca")
	def script_BajarVelocidad(self, event):
		if ajustes.IS_WinON:
			ui.message(self.mensaje())
		else:
			if ajustes.velocidad == 0:
				ui.message(_("No se puede bajar más la velocidad. Ya se encuentra al mínimo posible"))
			else:
				velTemporal = ajustes.velocidad - 1
				ajustes.velocidad = velTemporal
				self.reproductor.velocidad(float(ajustes.listaVelocidad[ajustes.velocidad]))
				self.guardarAjustes()
				ui.message(_("Velocidad {}").format(ajustes.listaVelocidad[ajustes.velocidad]))

	@script(gesture=None, description= _("Subir velocidad"), category= "audiocinemateca")
	def script_SubirVelocidad(self, event):
		if ajustes.IS_WinON:
			ui.message(self.mensaje())
		else:
			if ajustes.velocidad == 17:
				ui.message(_("No se puede subir más la velocidad. Ya se encuentra al máximo"))
			else:
				velTemporal = ajustes.velocidad + 1
				ajustes.velocidad = velTemporal
				self.reproductor.velocidad(float(ajustes.listaVelocidad[ajustes.velocidad]))
				self.guardarAjustes()
				ui.message(_("Velocidad {}").format(ajustes.listaVelocidad[ajustes.velocidad]))

	@script(gesture=None, description= _("Atrasar la reproducción"), category= "audiocinemateca")
	def script_Atrasar(self, event):
		if ajustes.IS_WinON:
			ui.message(self.mensaje())
		else:
			self.reproductor.atrasar(ajustes.dict_tiempo.get(ajustes.atrasar))
			msg = _("Sin nada en reproducción") if self.reproductor.estado() in ["State.NothingSpecial", "State.Stopped"] else _("Atrasando {}").format(ajustes.listaAtrasar[ajustes.atrasar])
			ui.message(msg)

	@script(gesture=None, description= _("Adelantar la reproducción"), category= "audiocinemateca")
	def script_Adelantar(self, event):
		if ajustes.IS_WinON:
			ui.message(self.mensaje())
		else:
			self.reproductor.adelantar(ajustes.dict_tiempo.get(ajustes.adelantar))
			msg = _("Sin nada en reproducción") if self.reproductor.estado() in ["State.NothingSpecial", "State.Stopped"] else _("Adelantando {}").format(ajustes.listaAdelantar[ajustes.adelantar])
			ui.message(msg)

	@script(gesture=None, description= _("Reproducir / Pausar la reproducción"), category= "audiocinemateca")
	def script_ReproducirPausar(self, event):
		if ajustes.IS_WinON:
			ui.message(self.mensaje())
		else:
			self.reproductor.pause()
			msg = _("Sin nada en reproducción") if self.reproductor.estado() in ["State.NothingSpecial", "State.Stopped"] else _("Pausando...") if self.reproductor.estado() == "State.Playing" else _("Reproduciendo...")
			ui.message(msg)

	@script(gesture=None, description= _("Detener la reproducción"), category= "audiocinemateca")
	def script_Detener(self, event):
		if ajustes.IS_WinON:
			ui.message(self.mensaje())
		else:
			msg = _("Detenido") if self.reproductor.estado() in ["State.Playing", "State.Paused"] else _("Sin nada en reproducción")
			ui.message(msg)
			self.reproductor.stop()

	@script(gesture=None, description= _("Información de la reproducción"), category= "audiocinemateca")
	def script_Informacion(self, event):
		if ajustes.IS_WinON:
			ui.message(self.mensaje())
		else:
			msg = _("Sin nada en reproducción") if self.reproductor.estado() in ["State.NothingSpecial", "State.Stopped"] else _("Tiempo transcurrido: {} / Tiempo total: {}").format(self.reproductor.conviertetiempo(self.reproductor.tiempotranscurrido()), self.reproductor.conviertetiempo(self.reproductor.tiempototal()))
			ui.message(msg)

class AjustesApp():
	def __init__(self, version= None):

		self.version = version
		self.fichero = os.path.join(ajustes.dirGeneral, ".audiocinemateca") #os.environ['USERPROFILE'], ".audiocinemateca")

		self.opcionesDefectoLogin = ["", ""]
		self.opcionesDefectoGeneral = [50, 5, 2, 3, 0, True]
		self.opcionesDefectoBaneo = [False, 0, None, None]
		self.opcionesDefectoVersionLocal = [None]
		self.opciones = []

	def GuardaDatos(self):
		try:
			with open(self.fichero, "w") as fp:
				json.dump([
					[ajustes.usuario, ajustes.contraseña], # Opciones login
					[ajustes.volumen, ajustes.velocidad, ajustes.atrasar, ajustes.adelantar, ajustes.resultados, ajustes.IS_HABLAR], # opciones generales
					[ajustes.IS_BANEO, ajustes.intentosBaneo, ajustes.fechaIntento, ajustes.fechaBaneo], # Opciones para el baneo
					[ajustes.versionLocal], # Versión local de la base de datos
				], fp)
		except Exception as e:
			msg = \
_("""Error al guardar la configuración de la Audiocinemateca.

Error:

{}""").format(e)
			log.error(msg)

	def GuardaDatosDefecto(self):
		try:
			with open(self.fichero, "w") as fp:
				json.dump([self.opcionesDefectoLogin, self.opcionesDefectoGeneral, self.opcionesDefectoBaneo, self.opcionesDefectoVersionLocal], fp)
		except Exception as e:
			msg = \
_("""Error al guardar la configuración por defecto de la Audiocinemateca.

Error:

{}""").format(e)
			log.error(msg)

	def CargaDatos(self):
		if os.path.isfile(self.fichero):
			with open(self.fichero, "r") as fp:
				try:
					self.opciones = json.load(fp)
				except json.JSONDecodeError:
					msg = \
_("""Se a producido un error de codificación json al cargar el archivo de configuración de la Audiocinemateca.""")
					log.warning(msg)
					self.GuardaDatosDefecto()
					self.CargaDatos()
		else:
			self.GuardaDatosDefecto()
			self.CargaDatos()

	def refrescaDatos(self):
		try:
			ajustes.usuario = self.opciones[0][0] # usuario
			ajustes.contraseña = self.opciones[0][1] # contraseña
			ajustes.volumen = self.opciones[1][0] # volumen
			ajustes.velocidad = self.opciones[1][1] # velocidad
			ajustes.atrasar = self.opciones[1][2] # atrasar
			ajustes.adelantar = self.opciones[1][3] # adelantar
			ajustes.resultados = self.opciones[1][4] # resultados
			ajustes.IS_HABLAR = self.opciones[1][5] # hablar
			ajustes.IS_BANEO = self.opciones[2][0] # bandera beneado True o False
			ajustes.intentosBaneo = self.opciones[2][1] # Intentos que llevamos de para el baneo
			ajustes.fechaIntento = self.opciones[2][2] # Contiene el datatime de la hora que se a producido el error de login
			ajustes.fechaBaneo = self.opciones[2][3] # Contiene el datatime de la hora que termina y fecha que termina baneo
			ajustes.versionLocal = self.opciones[3][0] #Versión de la base de datos
		except Exception as e:
			msg = \
_("""Se a producido un error al refrescar la configuración.

Error:

{}""").format(e)
			log.warning(msg)
			self.GuardaDatosDefecto()
			self.CargaDatos()
			self.refrescaDatos()

