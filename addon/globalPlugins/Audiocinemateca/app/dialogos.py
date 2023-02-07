# -*- coding: utf-8 -*-
# Copyright (C) 2023 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.

import addonHandler
import globalVars
import winsound
import wx
import os
import sys
import json
from threading import Thread
from .utilidades import mensaje, descargador, decompress_gz, decompress_bz2, partir_texto, es_url, get_filename_from_url, compare_dict_times

addonHandler.initTranslation()

class DownloadDialog(wx.Dialog):
	def __init__(self, frame, opcion, datos=[]):

		WIDTH = 550
		HEIGHT = 400

		super(DownloadDialog, self).__init__(None, -1, title=_('Descargando...'), size = (WIDTH, HEIGHT))

		self.frame = frame
		self.opcion = opcion
		self.datos = datos
		self.url_datos = "https://audiocinemateca.com/system/files/catalogo/catalogo.json.bz2"
		self.url_version = "https://audiocinemateca.com/system/files/catalogo/version.json.gz"
		self.dirGeneral =os.path.join(globalVars.appArgs.configPath, "Audiocinemateca")
		self.fichero_datos = os.path.join(globalVars.appArgs.configPath, "Audiocinemateca", "catalogo.json")
		self.fichero_version = os.path.join(globalVars.appArgs.configPath, "Audiocinemateca", "version.json")
		if self.opcion == 1: # Descarga inicio
			self.usuario = self.frame.AjustesApp.opciones[0][0]
			self.contraseña = self.frame.AjustesApp.opciones[0][1]
		elif self.opcion == 2: #Descarga archivo
			self.frame.reproductorKeyboard.addFrameSecundario(self)
			self.frame.reproductorKeyboard.onTeclasReproductor(1)
		elif self.opcion == 3: #Comprueba actualizaciones
			self.SetTitle(_("Actualizando..."))
			self.frame.reproductorKeyboard.addFrameSecundario(self)
			self.frame.reproductorKeyboard.onTeclasReproductor(1)

		self.CenterOnScreen()

		self.Panel = wx.Panel(self)

		self.progressBar=wx.Gauge(self.Panel, wx.ID_ANY, range=100, style = wx.GA_HORIZONTAL)

		self.textorefresco = wx.TextCtrl(self.Panel, wx.ID_ANY, style =wx.TE_MULTILINE|wx.TE_READONLY)
		self.textorefresco.Bind(wx.EVT_CONTEXT_MENU, self.skip)

		self.update_button = wx.Button(self.Panel, 2, _("&Actualizar"))
		self.Bind(wx.EVT_BUTTON, self.on_update, self.update_button)
		self.update_button.Disable()

		self.ok_button = wx.Button(self.Panel, 0, _("&Aceptar"))
		self.Bind(wx.EVT_BUTTON, self.on_ok, self.ok_button)
		self.ok_button.Disable()

		self.cancel_button = wx.Button(self.Panel, 1, _("&Cerrar"))
		self.Bind(wx.EVT_BUTTON, self.on_cancel, self.cancel_button)
		self.cancel_button.Disable()

		self.Bind(wx.EVT_CLOSE, self.skip)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer_botones = wx.BoxSizer(wx.HORIZONTAL)

		sizer.Add(self.progressBar, 0, wx.EXPAND)
		sizer.Add(self.textorefresco, 1, wx.EXPAND)

		sizer_botones.Add(self.update_button, 2, wx.CENTER)
		sizer_botones.Add(self.ok_button, 2, wx.CENTER)
		sizer_botones.Add(self.cancel_button, 2, wx.CENTER)

		sizer.Add(sizer_botones, 0, wx.EXPAND)

		self.Panel.SetSizer(sizer)

		self.textorefresco.SetFocus()
		if self.opcion == 1: # Hilo para descarga y descompresión de catalogo y versión .json
			self.download_thread = Thread(target=self.download_catalogo, daemon = True).start()
		elif self.opcion == 2: # Descarga de archivo
			self.download_thread = Thread(target=self.download_fichero, daemon = True).start()
		elif self.opcion == 3: # Actualizar
			self.download_thread = Thread(target=self.download_actualizacionVersion, daemon = True).start()

	def skip(self, event):
		return

	def actualizar(self, opcion):
		if opcion: # Descarga catalogo
			x = descargador(self, self.datos[0], self.datos[1], self.url_datos, self.dirGeneral, 1)
			if x[0]:
				return [True, None]
			elif x[1] == None:
				msg = \
_("""No se pudo descargar el archivo, intentelo más tarde.""")
				return [False, msg]
			else:
				msg = \
_("""Se produjo un error.

Error:

{}""").format(x[1])
				return [False, msg]

		else: # Descarga version
			x = descargador(self, self.datos[0], self.datos[1], self.url_version, self.dirGeneral, 1)
			if x[0]:
				return [True, None]
			elif x[1] == None:
				msg = \
_("""No se pudo descargar el archivo, intentelo más tarde.""")
				return [False, msg]
			else:
				msg = \
_("""Se produjo un error.

Error:

{}""").format(x[1])
				return [False, msg]

	def descargar_fichero(self):
		x = descargador(self, self.datos[0], self.datos[1], self.datos[2], self.datos[3], 2)
		if x[0]:
			return [True, None]
		elif x[1] == None:
			msg = \
_("""No se pudo descargar el archivo, intentelo más tarde.""")
			return [False, msg]
		else:
			msg = \
_("""Se produjo un error.

Error:

{}""").format(x[1])
			return [False, msg]

	def descargar_catalogo(self):
		# Descargamos el catalogo y lo guardamos en el directorio usuario_nvda/audiocinemateca
		x = descargador(self, self.usuario, self.contraseña, self.url_datos, self.dirGeneral, 1)
		if x[0]: # Descarga del catalogo exitoso.
			z = descargador(self, self.usuario, self.contraseña, self.url_version, self.dirGeneral, 1)
			if z[0]:
				return [True, None]
			elif z[1] == None:
				msg = \
_("""No se pudo descargar la versión  del catalogo, intentelo más tarde.""")
				return [False, msg]
			else:
				msg = \
_("""Se produjo un error.

Error:

{}""").format(z[1])
				return [False, msg]
		elif x[1] == None:
			msg = \
_("""No se pudo descargar el catalogo, intentelo más tarde.""")
			return [False, msg]
		else:
			msg = \
_("""Se produjo un error.

Error:

{}""").format(x[1])
			return [False, msg]

	def descomprimir(self):
		# descomprimimos el catalogo
		x = decompress_bz2(self, os.path.join(self.dirGeneral, "catalogo.json.bz2"), os.path.join(self.dirGeneral, "catalogo.json"))
		if x[0]: # descompresión del catalogo exitoso.
			z = decompress_gz(self, os.path.join(self.dirGeneral, "version.json.gz"), os.path.join(self.dirGeneral, "version.json"))
			if z[0]:
				return [True, None]
			else:
				msg = \
_("""Se produjo un error.

Error:

{}""").format(z[1])
				return [False, msg]
		else:
			msg = \
_("""Se produjo un error.

Error:

{}""").format(x[1])
			return [False, msg]

	def borrar(self, error=False):
		if error:
			try:
				os.remove(os.path.join(self.dirGeneral, "catalogo.json.bz2"))
			except:
				pass
			try:
				os.remove(os.path.join(self.dirGeneral, "version.json.gz"))
			except:
				pass
			try:
				os.remove(os.path.join(self.dirGeneral, "catalogo.json"))
			except:
				pass
			try:
				os.remove(os.path.join(self.dirGeneral, "version.json"))
			except:
				pass
		else:
			try:
				os.remove(os.path.join(self.dirGeneral, "catalogo.json.bz2"))
			except:
				pass
			try:
				os.remove(os.path.join(self.dirGeneral, "version.json.gz"))
			except:
				pass

	def download_catalogo(self):
		msg = \
_("""Descargando el catalogo de la Audiocinemateca.
Esta acción tiene varios pasos.
Espere por favor…""")
		self.textorefresco.Clear()
		self.textorefresco.AppendText(msg)
		x = self.descargar_catalogo()
		if x[0]:  # Descarga correcta.
			msg = \
_("""Descomprimiendo el catalogo de la Audiocinemateca.
Esta acción tiene varios pasos.
Espere por favor…""")
			self.textorefresco.Clear()
			self.textorefresco.AppendText(msg)
			z = self.descomprimir()
			if z[0]: # Descompresión correcta.
				self.borrar()
				msg = \
_("""Descarga del catalogo de la Audiocinemateca correcto.
Ya puede cerrar esta pantalla y disfrutar.""")
				self.textorefresco.Clear()
				self.textorefresco.AppendText(msg)
				wx.CallAfter(self.enable_ok_button)
			else: # Descompresión fallida.
				self.borrar(True)
				self.textorefresco.Clear()
				self.textorefresco.AppendText(z[1])
				wx.CallAfter(self.enable_cancel_button)
		else: # Descarga fallida.
			self.borrar(True)
			self.textorefresco.Clear()
			self.textorefresco.AppendText(x[1])
			wx.CallAfter(self.enable_cancel_button)

	def download_fichero(self):
		tempDescarga = os.path.join(self.datos[3], get_filename_from_url(self.datos[2]))
		msg = \
_("""Descargando el fichero en la siguiente ruta:

{}

Espere por favor…""").format(tempDescarga)
		self.textorefresco.Clear()
		self.textorefresco.AppendText(msg)
		x = self.descargar_fichero()
		if x[0]:  # Descarga correcta.
			msg = \
_("""La descarga fue un éxito.
Ya puede cerrar esta pantalla y disfrutar.""")
			self.textorefresco.Clear()
			self.textorefresco.AppendText(msg)
			wx.CallAfter(self.enable_ok_button)
		else: # Descarga fallida.
			try:
				os.remove(tempDescarga)
			except:
				pass
			self.textorefresco.Clear()
			self.textorefresco.AppendText(x[1])
			wx.CallAfter(self.enable_cancel_button)

	def download_actualizacionVersion(self):
		msg = \
_("""Comprobando si hay actualizaciones.

Espere por favor…""")
		self.textorefresco.Clear()
		self.textorefresco.AppendText(msg)
		x = self.actualizar(False)
		if x[0]:  # Descarga correcta.
			z = decompress_gz(self, os.path.join(self.dirGeneral, "version.json.gz"), os.path.join(self.dirGeneral, "version.json"))
			if z[0]: # Descompresión correcta
				with open(self.fichero_version) as f:
					self.resultados_version = json.load(f)
				try:
					os.remove(os.path.join(self.dirGeneral, "version.json.gz"))
				except:
					pass
				if compare_dict_times(self.datos[2], self.resultados_version): # Si hay actualizaciones
					msg = \
_("""Hay actualizaciones de la base de datos.

¿Desea actualizar?""")
					self.textorefresco.Clear()
					self.textorefresco.AppendText(msg)
					wx.CallAfter(self.enable_update_button)
				else: # No hay actualizaciones
					self.opcion = 1
					try:
						os.remove(os.path.join(self.dirGeneral, "version.json.gz"))
					except:
						pass
					msg = \
_("""No existen actualizaciones.

Compruébelo más adelante.""")
					self.textorefresco.Clear()
					self.textorefresco.AppendText(msg)
					wx.CallAfter(self.enable_ok_button)
			else: # Descompresion fallida
				self.opcion = 1
				try:
					os.remove(os.path.join(self.dirGeneral, "version.json.gz"))
				except:
					pass
				msg = \
_("""Se produjo un error.

Error:

{}""").format(z[1])
				self.textorefresco.Clear()
				self.textorefresco.AppendText(msg)
				wx.CallAfter(self.enable_cancel_button)
		else: # Descarga fallida de la versión en el servidor.
			self.opcion = 1
			try:
				os.remove(os.path.join(self.dirGeneral, "version.json.gz"))
			except:
				pass
			self.textorefresco.Clear()
			self.textorefresco.AppendText(x[1])
			wx.CallAfter(self.enable_cancel_button)

	def download_actualizacionCatalogo(self):
		msg = \
_("""Actualizando la base de datos.

Espere por favor…""")
		self.textorefresco.Clear()
		self.textorefresco.AppendText(msg)
		x = self.actualizar(True)
		if x[0]:  # Descarga correcta.
			z = decompress_bz2(self, os.path.join(self.dirGeneral, "catalogo.json.bz2"), os.path.join(self.dirGeneral, "catalogo.json"))
			if z[0]: # Descompresión correcta
				with open(self.fichero_version) as f:
					self.resultados_version = json.load(f)
				self.frame.frame.AjustesApp.opciones[-1] = [self.resultados_version]
				self.frame.frame.AjustesApp.refrescaDatos()
				self.frame.frame.AjustesApp.GuardaDatos()
				self.frame.frame.AjustesApp.CargaDatos()
				self.frame.frame.AjustesApp.refrescaDatos()
				try:
					os.remove(os.path.join(self.dirGeneral, "catalogo.json.bz2"))
				except:
					pass
				msg = \
_("""Actualización de la base de datos completada.

El complemento se cerrará, para cargar la nueva base de datos vuelva a abrirlo.

Disfrute de la Audiocinemateca.""")
				self.textorefresco.Clear()
				self.textorefresco.AppendText(msg)
				wx.CallAfter(self.enable_ok_button)
			else: # Descompresion fallida
				self.opcion = 1
				try:
					os.remove(os.path.join(self.dirGeneral, "catalogo.json.bz2"))
				except:
					pass
				msg = \
_("""Se produjo un error.

Error:

{}""").format(z[1])
				self.textorefresco.Clear()
				self.textorefresco.AppendText(msg)
				wx.CallAfter(self.enable_cancel_button)
		else: # Descarga fallida del catalogo en el servidor.
			self.opcion = 1
			try:
				os.remove(os.path.join(self.dirGeneral, "catalogo.json.bz2"))
			except:
				pass
			self.textorefresco.Clear()
			self.textorefresco.AppendText(x[1])
			wx.CallAfter(self.enable_cancel_button)

	def update_progress(self, percent):
		self.progressBar.SetValue(int(percent))

	def enable_update_button(self):
		winsound.MessageBeep(0)
		self.update_button.Enable()
		self.cancel_button.Enable()
		self.textorefresco.SetInsertionPoint(0) 

	def enable_ok_button(self):
		winsound.MessageBeep(0)
		self.ok_button.Enable()
		self.textorefresco.SetInsertionPoint(0) 

	def enable_cancel_button(self):
		winsound.MessageBeep(16)
		self.cancel_button.Enable()
		self.textorefresco.SetInsertionPoint(0) 

	def on_update(self, event):
		self.download_thread = Thread(target=self.download_actualizacionCatalogo, daemon = True).start()
		self.update_button.Disable()
		self.cancel_button.Disable()

	def on_ok(self, event):
		if self.opcion == 3:
			self.EndModal(2)
		else:
			self.EndModal(0)

	def on_cancel(self, event):
		self.EndModal(1)

class Login(wx.Dialog):
	def __init__(self, frame, editar=False):

		super(Login, self).__init__(None, -1, title=_("Editar sesión en Audiocinemateca") if editar else _("Iniciar sesión en Audiocinemateca"))

		self.frame = frame
		if editar:
			self.frame.reproductorKeyboard.addFrameSecundario(self)
			self.frame.reproductorKeyboard.onTeclasReproductor(1)
		self.contraseña = ""

		self.Panel = wx.Panel(self)

		label1 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("&Usuario:"))
		self.textoUsuario = wx.TextCtrl(self.Panel, wx.ID_ANY)
		if editar: self.textoUsuario.SetValue(self.frame.AjustesApp.opciones[0][0])

		label2 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("&Contraseña:"))
		self.textoContraseña_Oculto = wx.TextCtrl(self.Panel, wx.ID_ANY, style=wx.TE_PASSWORD)
		self.textoContraseña_Visible = wx.TextCtrl(self.Panel, wx.ID_ANY)
		self.textoContraseña_Visible.Hide()
		if editar:
			self.contraseña = self.frame.AjustesApp.opciones[0][1]
			self.textoContraseña_Oculto.SetValue(self.frame.AjustesApp.opciones[0][1])

		self.verContraseña = wx.CheckBox(self.Panel, label=_("&Mostrar contraseña"))
		self.verContraseña.SetValue(False)
		self.verContraseña.Bind(wx.EVT_CHECKBOX, self.onShowPwd)

		self.AceptarBTN = wx.Button(self.Panel, 0, label=_("&Aceptar"))
		self.Bind(wx.EVT_BUTTON, self.onAceptar, id=self.AceptarBTN.GetId())

		self.CancelarBTN = wx.Button(self.Panel, 1, label=_("Cancelar"))
		self.Bind(wx.EVT_BUTTON, self.onCancelar, id=self.CancelarBTN.GetId())

		self.webBTN = wx.Button(self.Panel, 2, label=_("&Visitar la web"))
		self.Bind(wx.EVT_BUTTON, self.onWeb, id=self.webBTN.GetId())

		self.Bind(wx.EVT_CHAR_HOOK, self.onkeyVentanaDialogo)

		sizeV = wx.BoxSizer(wx.VERTICAL)
		sizeH = wx.BoxSizer(wx.HORIZONTAL)

		sizeV.Add(label1, 0, wx.EXPAND)
		sizeV.Add(self.textoUsuario, 0, wx.EXPAND)

		sizeV.Add(label2, 0, wx.EXPAND)
		sizeV.Add(self.textoContraseña_Oculto, 0, wx.EXPAND)
		sizeV.Add(self.textoContraseña_Visible, 0, wx.EXPAND)

		sizeV.Add(self.verContraseña, 0, wx.EXPAND)

		sizeH.Add(self.AceptarBTN, 2, wx.EXPAND)
		sizeH.Add(self.CancelarBTN, 2, wx.EXPAND)
		sizeH.Add(self.webBTN, 2, wx.EXPAND)

		sizeV.Add(sizeH, 0, wx.EXPAND)

		self.Panel.SetSizer(sizeV)

		self.CenterOnScreen()

	def onShowPwd(self, event):
		if self.verContraseña.GetValue():
			self.textoContraseña_Oculto.Hide()
			self.textoContraseña_Visible.Show()
			self.textoContraseña_Visible.SetValue(self.textoContraseña_Oculto.GetValue())
			self.textoContraseña_Visible.GetParent().Layout()
			self.textoContraseña_Visible.SetFocus()
		else:
			self.textoContraseña_Oculto.Show()
			self.textoContraseña_Visible.Hide()
			self.textoContraseña_Oculto.SetValue(self.textoContraseña_Visible.GetValue())
			self.textoContraseña_Oculto.GetParent().Layout()
			self.textoContraseña_Oculto.SetFocus()

	def onAceptar(self, event):
		contraseñaBlanco = self.textoContraseña_Oculto.GetValue() if self.textoContraseña_Oculto.IsShown() else self.textoContraseña_Visible.GetValue()
		if any(x == "" for x in [self.textoUsuario.GetValue(), contraseñaBlanco]):
			msg = \
_("""Los campos Usuario y Contraseña son obligatorios.

No pueden quedar en blanco.""")
			mensaje(msg, _("Información"), 0)
			self.textoUsuario.SetFocus() if self.textoUsuario.GetValue() == ""  else self.textoContraseña_Oculto.SetFocus() if self.textoContraseña_Oculto.IsShown() else self.textoContraseña_Visible.SetFocus()
			return
		self.contraseña =  self.textoContraseña_Oculto.GetValue() if self.textoContraseña_Oculto.IsShown() else self.textoContraseña_Visible.GetValue()

		if self.IsModal():
			self.EndModal(0)
		else:
			self.Close()

	def onWeb(self, event):
		wx.LaunchDefaultBrowser("https://www.audiocinemateca.com/")

	def onkeyVentanaDialogo(self, event):
		if event.GetKeyCode() == 27: # Pulsamos ESC y cerramos la ventana
			if self.IsModal():
				self.EndModal(1)
			else:
				self.Close()
		else:
			event.Skip()

	def onCancelar(self, event):
		if self.IsModal():
			self.EndModal(1)
		else:
			self.Close()

class posicion(wx.Dialog):
	def __init__(self, frame, datos):

		super(posicion, self).__init__(None, -1, title=_("Ir a la posición..."))

		self.frame = frame
		self.datos = datos
		self.frame.reproductorKeyboard.addFrameSecundario(self)
		self.frame.reproductorKeyboard.onTeclasReproductor(1)

		self.Panel = wx.Panel(self)

		label1 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("&Introduzca un número entre 1 y {}:").format(self.datos))
		self.numero = wx.TextCtrl(self.Panel, 101, "", style=wx.TE_PROCESS_ENTER)

		self.AceptarBTN = wx.Button(self.Panel, 0, label=_("&Aceptar"))
		self.Bind(wx.EVT_BUTTON, self.onAceptar, id=self.AceptarBTN.GetId())

		self.CancelarBTN = wx.Button(self.Panel, 1, label=_("Cancelar"))
		self.Bind(wx.EVT_BUTTON, self.onCancelar, id=self.CancelarBTN.GetId())

		self.Bind(wx.EVT_CHAR_HOOK, self.onkeyVentanaDialogo)

		sizeV = wx.BoxSizer(wx.VERTICAL)
		sizeH = wx.BoxSizer(wx.HORIZONTAL)

		sizeV.Add(label1, 0, wx.EXPAND)
		sizeV.Add(self.numero, 0, wx.EXPAND)

		sizeH.Add(self.AceptarBTN, 2, wx.EXPAND)
		sizeH.Add(self.CancelarBTN, 2, wx.EXPAND)

		sizeV.Add(sizeH, 0, wx.EXPAND)

		self.Panel.SetSizer(sizeV)

		self.CenterOnScreen()


	def onAceptar(self, event):
		msg = \
_("""El campo solo admite números y no puede quedar vacío.

Solo se admite un número comprendido entre 1 y {}.""").format(self.datos)
		if not self.numero.GetValue():
			mensaje(msg, _("Información"), 0)
			self.numero.Clear()
			self.numero.SetFocus()
			return
		else:
			try:
				z = 1 <= int(self.numero.GetValue()) <= self.datos
			except ValueError:
				mensaje(msg, _("Información"), 0)
				self.numero.Clear()
				self.numero.SetFocus()
				return

			if z:
				if self.IsModal():
					self.EndModal(0)
				else:
					self.Close()
			else:
				mensaje(msg, _("Información"), 0)
				self.numero.Clear()
				self.numero.SetFocus()
				return

	def onkeyVentanaDialogo(self, event):
		foco = wx.Window.FindFocus().GetId()
		robot = wx.UIActionSimulator()
		if event.GetUnicodeKey() == wx.WXK_RETURN:
			if foco in [101]: # campo texto pasamos.
				self.onAceptar(None)

		elif event.GetKeyCode() == 27: # Pulsamos ESC y cerramos la ventana
			if self.IsModal():
				self.EndModal(1)
			else:
				self.Close()
		else:
			event.Skip()

	def onCancelar(self, event):
		if self.IsModal():
			self.EndModal(1)
		else:
			self.Close()

class Previsualizador(wx.Dialog):
	def __init__(self, frame, datos, opcion):
		super(Previsualizador, self).__init__(None, -1)

		self.frame = frame
		self.datos = datos
		self.opcion = opcion
		self.frame.reproductorKeyboard.addFrameSecundario(self)
		self.frame.reproductorKeyboard.onTeclasReproductor(1)

		self.SetSize((640, 480))
		if self.opcion == 0: # Peliculas
			self.SetTitle(_("Ficha de la película"))
			label_texto_1 = _("&Información de la película:")
			label_texto_2 = _("&Enlaces de la película:")
		if self.opcion == 2: # Documentales
			self.SetTitle(_("Ficha del documental"))
			label_texto_1 = _("&Información del documental:")
		if self.opcion == 3: # cortometrajes
			self.SetTitle(_("Ficha del cortometraje"))
			label_texto_1 = _("&Información del cortometraje:")

		self.panel_principal = wx.Panel(self, wx.ID_ANY)

		sizer_principal = wx.BoxSizer(wx.VERTICAL)

		label_1 = wx.StaticText(self.panel_principal, wx.ID_ANY, label_texto_1)
		sizer_principal.Add(label_1, 0, wx.EXPAND, 0)

		self.textoResultado = wx.TextCtrl(self.panel_principal, wx.ID_ANY, "", style=wx.HSCROLL | wx.TE_MULTILINE | wx.TE_READONLY)
		sizer_principal.Add(self.textoResultado, 2, wx.EXPAND, 0)
		if self.opcion == 0: # Solo para peliculas
			label_2 = wx.StaticText(self.panel_principal, wx.ID_ANY, label_texto_2)
			sizer_principal.Add(label_2, 0, wx.EXPAND, 0)

			self.choice_enlaces = wx.Choice(self.panel_principal, wx.ID_ANY)
			sizer_principal.Add(self.choice_enlaces, 0, wx.EXPAND, 0)

		sizer_botones = wx.BoxSizer(wx.HORIZONTAL)
		sizer_principal.Add(sizer_botones, 0, wx.EXPAND, 0)

		self.reproducirBTN = wx.Button(self.panel_principal, 0, _("&Reproducir"))
		sizer_botones.Add(self.reproducirBTN, 2, wx.EXPAND, 0)

		self.descargaBTN = wx.Button(self.panel_principal, 1, _("&Descargar"))
		sizer_botones.Add(self.descargaBTN, 2, wx.EXPAND, 0)

		self.informacionBTN = wx.Button(self.panel_principal, 2, _("Información adicional en la &web"))
		sizer_botones.Add(self.informacionBTN, 2, wx.EXPAND, 0)

		self.cerrarBTN = wx.Button(self.panel_principal, 10, _("&Cerrar"))
		sizer_botones.Add(self.cerrarBTN, 2, wx.EXPAND, 0)

		self.panel_principal.SetSizer(sizer_principal)

		self.Layout()
		self.CenterOnScreen()
		self.cargaEventos()
		self.inicio()

	def cargaEventos(self):
		self.Bind(wx.EVT_BUTTON,self.onBoton)
		self.Bind(wx.EVT_CLOSE, self.onCerrar)
		self.Bind(wx.EVT_CHAR_HOOK, self.on_keyVentanaDialogo)

	def inicio(self):
		id = self.datos["id"]
		titulo = self.datos["Titulo"] if self.opcion == 0 else self.datos["titulo"]
		anio = self.datos["anio"]
		genero = self.datos["genero"]
		pais = self.datos["pais"]
		director = self.datos["director"]
		guion = self.datos["guion"]
		musica = self.datos["musica"]
		fotografia = self.datos["fotografia"]
		reparto = self.datos["reparto"]
		productora = self.datos["productora"]
		narracion = self.datos["narracion"]
		duracion = self.datos["duracion"]
		idioma = self.datos["idioma"]
		if self.opcion == 0:
			partes = self.datos["partes"]
		filmaffinity = self.datos["filmaffinity"]
		sinopsis = self.datos["sinopsis"]
		enlaces = self.datos["enlaces"] if self.opcion == 0 else self.datos["enlace"]

		self.textoResultado.WriteText(_("Título:\n"))
		self.textoResultado.WriteText(titulo + "\n")

		self.textoResultado.WriteText(_("Año:\n"))
		self.textoResultado.WriteText(anio + "\n")

		self.textoResultado.WriteText(_("Género:\n"))
		self.textoResultado.WriteText(genero + "\n")

		self.textoResultado.WriteText(_("País:\n"))
		self.textoResultado.WriteText(pais + "\n")

		self.textoResultado.WriteText(_("Director:\n"))
		self.textoResultado.WriteText(director + "\n")

		self.textoResultado.WriteText(_("Guión:\n"))
		self.textoResultado.WriteText(guion + "\n")

		self.textoResultado.WriteText(_("Música:\n"))
		self.textoResultado.WriteText(musica + "\n")

		self.textoResultado.WriteText(_("Fotografía:\n"))
		self.textoResultado.WriteText(fotografia + "\n")

		self.textoResultado.WriteText(_("Reparto:\n"))
		self.textoResultado.WriteText(partir_texto(reparto, 70) + "\n")

		self.textoResultado.WriteText(_("Productora:\n"))
		self.textoResultado.WriteText(productora + "\n")

		self.textoResultado.WriteText(_("Narración:\n"))
		self.textoResultado.WriteText(narracion + "\n")

		self.textoResultado.WriteText(_("Duración:\n"))
		self.textoResultado.WriteText(duracion + _(" minutos\n"))

		self.textoResultado.WriteText(_("Idioma:\n"))
		self.textoResultado.WriteText(_("Español") + "\n" if idioma == "1" else _("Español latino") + "\n")

		self.textoResultado.WriteText(_("Sinopsis:\n"))
		self.textoResultado.WriteText(partir_texto(sinopsis, 100) + "\n")

		if self.opcion == 0:
			for i in range(0, len(partes)):
				self.choice_enlaces.Append(_("Partes ({} de {})").format(i + 1, len(partes)))
			self.choice_enlaces.SetSelection(0)

		self.textoResultado.SetInsertionPoint(0) 

	def onBoton(self, event):
		id = event.GetId()
		if id == 2: # Información en la web
			msg = \
_("""Esta ficha no tiene información adicional para mostrar en la web.""")
			wx.LaunchDefaultBrowser(self.datos['filmaffinity'], flags=0) if es_url(self.datos['filmaffinity']) else mensaje(msg, _("Información"), 0)
			return
		if self.IsModal():
			self.EndModal(event.GetId())
		else:
			self.Close()

	def on_keyVentanaDialogo(self, event):
		foco = wx.Window.FindFocus().GetId()
		robot = wx.UIActionSimulator()
		if event.GetUnicodeKey() == wx.WXK_RETURN:
			if foco in [0, 1, 2, 10]: # listbox ultimos, peliculas, series, documentales, cortometrajes
				wx.CallAfter(self.onBoton, event.GetEventObject())

		elif event.GetUnicodeKey() == wx.WXK_ESCAPE: # Pulsamos ESC y cerramos la ventana
			if self.IsModal():
				self.EndModal(10)
			else:
				self.Close()
		else:
			event.Skip()

	def onCerrar(self, event):
		if self.IsModal():
			self.EndModal(10)
		else:
			self.Close()

class PrevisualizadorSerie(wx.Dialog):
	def __init__(self, frame, datos, datosSerie):
		super(PrevisualizadorSerie, self).__init__(None, -1)

		self.frame = frame
		self.datos = datos
		self.datosEpisodios = datosSerie
		self.episodios = self.datosEpisodios.obtener_episodios_por_temporada("1")
		self.temporadas = len(self.datos["capitulos"])
		self.enlacesEpisodios = []
		self.frame.reproductorKeyboard.addFrameSecundario(self)
		self.frame.reproductorKeyboard.onTeclasReproductor(1)

		self.SetSize((640, 480))
		self.SetTitle(_("Ficha de la Serie"))
		label_texto_1 = _("&Información de la serie:")
		label_texto_2 = _("&Temporada:") if self.temporadas <= 1 else _("&Temporadas:")

		self.panel_principal = wx.Panel(self, wx.ID_ANY)

		sizer_principal = wx.BoxSizer(wx.VERTICAL)

		label_1 = wx.StaticText(self.panel_principal, wx.ID_ANY, label_texto_1)
		sizer_principal.Add(label_1, 0, wx.EXPAND, 0)

		self.textoResultado = wx.TextCtrl(self.panel_principal, wx.ID_ANY, "", style=wx.HSCROLL | wx.TE_MULTILINE | wx.TE_READONLY)
		sizer_principal.Add(self.textoResultado, 2, wx.EXPAND, 0)

		label_2 = wx.StaticText(self.panel_principal, wx.ID_ANY, label_texto_2)
		sizer_principal.Add(label_2, 0, wx.EXPAND, 0)

		self.choice_temporadas = wx.Choice(self.panel_principal, wx.ID_ANY)
		sizer_principal.Add(self.choice_temporadas, 0, wx.EXPAND, 0)

		label_3 = wx.StaticText(self.panel_principal, wx.ID_ANY, _("&Episodios:"))
		sizer_principal.Add(label_3, 0, wx.EXPAND, 0)

		self.list_box_episodios = wx.ListBox(self.panel_principal, wx.ID_ANY)
		sizer_principal.Add(self.list_box_episodios, 2, wx.EXPAND, 0)

		sizer_botones = wx.BoxSizer(wx.HORIZONTAL)
		sizer_principal.Add(sizer_botones, 0, wx.EXPAND, 0)

		self.reproducirBTN = wx.Button(self.panel_principal, 0, _("&Reproducir"))
		sizer_botones.Add(self.reproducirBTN, 2, wx.EXPAND, 0)

		self.descargaBTN = wx.Button(self.panel_principal, 1, _("&Descargar"))
		sizer_botones.Add(self.descargaBTN, 2, wx.EXPAND, 0)

		self.informacionBTN = wx.Button(self.panel_principal, 2, _("Información adicional en la &web"))
		sizer_botones.Add(self.informacionBTN, 2, wx.EXPAND, 0)

		self.cerrarBTN = wx.Button(self.panel_principal, 10, _("&Cerrar"))
		sizer_botones.Add(self.cerrarBTN, 2, wx.EXPAND, 0)

		self.panel_principal.SetSizer(sizer_principal)

		self.Layout()
		self.CenterOnScreen()
		self.cargaEventos()
		self.inicio()

	def cargaEventos(self):
		self.Bind(wx.EVT_CHOICE,self.onChoice)
		self.Bind(wx.EVT_BUTTON,self.onBoton)
		self.Bind(wx.EVT_CLOSE, self.onCerrar)
		self.Bind(wx.EVT_CHAR_HOOK, self.on_keyVentanaDialogo)

	def onChoice(self, event):
		id = event.GetSelection()
		suma = id + 1
		del self.enlacesEpisodios[:]
		self.episodios = self.datosEpisodios.obtener_episodios_por_temporada(str(suma))
		self.list_box_episodios.Clear()
		for episodio in self.episodios:
			num = "{:02d}".format(int(episodio.capitulo))
			self.list_box_episodios.Append("{}x{} - {}".format(episodio.temporada, num, episodio.titulo))
			self.enlacesEpisodios.append(episodio.enlace)
		self.list_box_episodios.SetSelection(0)

	def inicio(self):
		id = self.datos["id"]
		titulo = self.datos["titulo"]
		anio = self.datos["anio"]
		duracion = self.datos["duracion"]
		pais = self.datos["pais"]
		director = self.datos["director"]
		guion = self.datos["guion"]
		musica = self.datos["musica"]
		fotografia = self.datos["fotografia"]
		reparto = self.datos["reparto"]
		genero = self.datos["genero"]
		temporadas = self.temporadas # self.datos['temporadas']
		idioma = self.datos["idioma"]
		narracion = self.datos["narracion"]
		filmaffinity = self.datos["filmaffinity"]
		sinopsis = self.datos["sinopsis"]
		productora = self.datos["productora"]

		self.textoResultado.WriteText(_("Título:\n"))
		self.textoResultado.WriteText(titulo + "\n")

		self.textoResultado.WriteText(_("Año:\n"))
		self.textoResultado.WriteText(anio + "\n")

		self.textoResultado.WriteText(_("Genero:\n"))
		self.textoResultado.WriteText(genero + "\n")

		self.textoResultado.WriteText(_("País:\n"))
		self.textoResultado.WriteText(pais + "\n")

		self.textoResultado.WriteText(_("Director:\n"))
		self.textoResultado.WriteText(director + "\n")

		self.textoResultado.WriteText(_("Guion:\n"))
		self.textoResultado.WriteText(guion + "\n")

		self.textoResultado.WriteText(_("Música:\n"))
		self.textoResultado.WriteText(musica + "\n")

		self.textoResultado.WriteText(_("Fotografía:\n"))
		self.textoResultado.WriteText(fotografia + "\n")

		self.textoResultado.WriteText(_("Reparto:\n"))
		self.textoResultado.WriteText(partir_texto(reparto, 70) + "\n")

		self.textoResultado.WriteText(_("Productora:\n"))
		self.textoResultado.WriteText(productora + "\n")

		self.textoResultado.WriteText(_("Narración:\n"))
		self.textoResultado.WriteText(narracion + "\n")

		self.textoResultado.WriteText(_("Duración:\n"))
		self.textoResultado.WriteText(duracion + _(" minutos\n"))

		self.textoResultado.WriteText(_("Idioma:\n"))
		self.textoResultado.WriteText(_("Español") + "\n" if idioma == "1" else _("Español latino") + "\n")

		self.textoResultado.WriteText(_("Temporadas:\n"))
		self.textoResultado.WriteText(str(temporadas) + "\n")

		self.textoResultado.WriteText(_("Sinopsis:\n"))
		self.textoResultado.WriteText(partir_texto(sinopsis, 100) + "\n")

		self.textoResultado.SetInsertionPoint(0) 
		for i in range(self.temporadas):
			self.choice_temporadas.Append(_("Temporada ({} de {})").format(i + 1, self.temporadas))
		self.choice_temporadas.SetSelection(0)
		for episodio in self.episodios:
			num = "{:02d}".format(int(episodio.capitulo))
			self.list_box_episodios.Append("{}x{} - {}".format(episodio.temporada, num, episodio.titulo))
			self.enlacesEpisodios.append(episodio.enlace)
		self.list_box_episodios.SetSelection(0)
	def onBoton(self, event):
		id = event.GetId()
		if id == 2: # Información en la web
			msg = \
_("""Esta ficha no tiene información adicional para mostrar en la web.""")
			wx.LaunchDefaultBrowser(self.datos['filmaffinity'], flags=0) if es_url(self.datos['filmaffinity']) else mensaje(msg, _("Información"), 0)
			return
		if self.IsModal():
			self.EndModal(event.GetId())
		else:
			self.Close()

	def on_keyVentanaDialogo(self, event):
		foco = wx.Window.FindFocus().GetId()
		robot = wx.UIActionSimulator()
		if event.GetUnicodeKey() == wx.WXK_RETURN:
			if foco in [0, 1, 2, 10]: # listbox ultimos, peliculas, series, documentales, cortometrajes
				wx.CallAfter(self.onBoton, event.GetEventObject())

		elif event.GetUnicodeKey() == wx.WXK_ESCAPE: # Pulsamos ESC y cerramos la ventana
			if self.IsModal():
				self.EndModal(10)
			else:
				self.Close()
		else:
			event.Skip()

	def onCerrar(self, event):
		if self.IsModal():
			self.EndModal(10)
		else:
			self.Close()
