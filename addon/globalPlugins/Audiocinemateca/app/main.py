# -*- coding: utf-8 -*-
# Copyright (C) 2023 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.

import addonHandler
import globalVars
import gui
import ui
import os
import sys
import wx
from threading import Thread
from . import ajustes
from . import utilidades
from . import dialogos

addonHandler.initTranslation()

_selfTemp = None

class VentanaPrincipal(wx.Dialog):
	def __init__(self, parent, frame):
		super(VentanaPrincipal, self).__init__(parent, -1, _("Audiocinemateca"), size = (800, 600)) #(1400, 850))

		msg = \
_("""Cargando la interface...""")
		if ajustes.IS_HABLAR:
			utilidades.speak(0.1, msg)

		# Bandera ventana principal abierta.
		ajustes.IS_WinON = True
		# Obtenemos el frame del complemento
		self.frame = frame
		global _selfTemp
		_selfTemp = frame
		# Definimos el reproductor que obtenemos del frame del complemento y le añadimos el frame de esta ventana principal
		self.reproductor = self.frame.reproductor
		self.reproductor.addFrameMain(self)
		# Definimos las teclas globales del reproductor que obtenemos de el frame del complemento y le pasamos el frame de la ventana principal para poder ser usado en esta ventana.
		self.reproductorKeyboard = self.frame.reproductorKeyboard
		self.reproductorKeyboard.addFrame(self)

		# Obtenemos los datos de las categorías, se obtienen los dict por separado para cada categoría.
		self.datos = self.frame.datos
		if not len(self.datos.resultados_datos):
			self.datos.cargaDatos()
			self.datos.cargaVersion()

		self.Peliculas = self.datos.GetDatos(0)
		self.Series = self.datos.GetDatos(1)
		self.Documentales = self.datos.GetDatos(2)
		self.Cortometrajes = self.datos.GetDatos(3)

		self.bandera_foco = 0
		self.tempBusquedaPeliculas = None
		self.tempBusquedaSeries = None
		self.tempBusquedaDocumentales = None
		self.tempBusquedaCortometrajes = None
		self.IS_BUSQUEDA_PELICULAS = False
		self.IS_BUSQUEDA_SERIES = False
		self.IS_BUSQUEDA_DOCUMENTALES = False
		self.IS_BUSQUEDA_CORTOMETRAJES = False

		# Definimos todos los widgets de la pantalla principal.
		self.panel_1 = wx.Panel(self, wx.ID_ANY)

		sizer_general = wx.BoxSizer(wx.VERTICAL)

		self.lst_book = wx.Notebook(self.panel_1, wx.ID_ANY)
		sizer_general.Add(self.lst_book, 1, wx.EXPAND, 0)

		self.panel_general = wx.Panel(self.lst_book, wx.ID_ANY)
		self.lst_book.AddPage(self.panel_general, _("General (Alt+1)"))

		sizer_principal_general = wx.BoxSizer(wx.VERTICAL)

		label_1 = wx.StaticText(self.panel_general, wx.ID_ANY, _(u"Últimos &contenidos agregados:"))
		sizer_principal_general.Add(label_1, 0, wx.EXPAND, 0)

		self.choice_ultimos = wx.Choice(self.panel_general, 1, choices=[_("Películas"), _("Series"), _("Documentales"), _("Cortometrajes")])
		self.choice_ultimos.SetSelection(0)
		sizer_principal_general.Add(self.choice_ultimos, 0, wx.EXPAND, 0)

		label_2 = wx.StaticText(self.panel_general, wx.ID_ANY, _("&Lista de las últimas entradas:"))
		sizer_principal_general.Add(label_2, 0, wx.EXPAND, 0)

		self.list_box_ultimos = wx.ListBox(self.panel_general, 2)
		sizer_principal_general.Add(self.list_box_ultimos, 1, wx.ALL | wx.EXPAND, 0)

		self.aleatorioBTN = wx.Button(self.panel_general, 3, _("¿No sabes qué ver? &Pulsa aquí y te ofreceré algo, a ver si acierto."))
		sizer_principal_general.Add(self.aleatorioBTN, 0, wx.EXPAND, 0)

		self.panel_peliculas = wx.Panel(self.lst_book, wx.ID_ANY)
		self.lst_book.AddPage(self.panel_peliculas, _("Películas (Alt+2)"))

		sizer_principal_peliculas = wx.BoxSizer(wx.VERTICAL)

		self.label_6 = wx.StaticText(self.panel_peliculas, wx.ID_ANY, _(u"&Buscar películas por {}:").format(ajustes.listaFiltroBusqueda[self.frame.categoriaBusqueda[0]]))
		sizer_principal_peliculas.Add(self.label_6, 0, wx.EXPAND, 0)

		self.text_busqueda_peliculas = wx.TextCtrl(self.panel_peliculas, 101, "", style=wx.TE_PROCESS_ENTER)
		sizer_principal_peliculas.Add(self.text_busqueda_peliculas, 0, wx.EXPAND, 0)

		label_7 = wx.StaticText(self.panel_peliculas, wx.ID_ANY, _(u"&Lista de películas:"))
		sizer_principal_peliculas.Add(label_7, 0, wx.EXPAND, 0)

		self.list_box_peliculas = wx.ListBox(self.panel_peliculas, 102)
		sizer_principal_peliculas.Add(self.list_box_peliculas, 1, wx.ALL | wx.EXPAND, 0)

#		self.accionPeliculasBTN = wx.Button(self.panel_peliculas, 103, _(u"&Acción"))
#		sizer_principal_peliculas.Add(self.accionPeliculasBTN, 0, wx.EXPAND, 0)

		self.panel_series = wx.Panel(self.lst_book, wx.ID_ANY)
		self.lst_book.AddPage(self.panel_series, _("Series (Alt+3)"))

		sizer_principal_series = wx.BoxSizer(wx.VERTICAL)

		self.label_8 = wx.StaticText(self.panel_series, wx.ID_ANY, _("&Buscar series por {}:").format(ajustes.listaFiltroBusqueda[self.frame.categoriaBusqueda[1]]))
		sizer_principal_series.Add(self.label_8, 0, wx.EXPAND, 0)

		self.text_busqueda_series = wx.TextCtrl(self.panel_series, 201, "", style=wx.TE_PROCESS_ENTER)
		sizer_principal_series.Add(self.text_busqueda_series, 0, wx.EXPAND, 0)

		label_9 = wx.StaticText(self.panel_series, wx.ID_ANY, _("&Lista de series:"))
		sizer_principal_series.Add(label_9, 0, wx.EXPAND, 0)

		self.list_box_series = wx.ListBox(self.panel_series, 202)
		sizer_principal_series.Add(self.list_box_series, 1, wx.ALL | wx.EXPAND, 0)

#		self.accionSeriesBTN = wx.Button(self.panel_series, 203, _(u"&Acción"))
#		sizer_principal_series.Add(self.accionSeriesBTN, 0, wx.EXPAND, 0)

		self.panel_documentales = wx.Panel(self.lst_book, wx.ID_ANY)
		self.lst_book.AddPage(self.panel_documentales, _("Documentales (Alt+4)"))

		sizer_principal_documentales = wx.BoxSizer(wx.VERTICAL)

		self.label_10 = wx.StaticText(self.panel_documentales, wx.ID_ANY, _("&Buscar documentales por {}:").format(ajustes.listaFiltroBusqueda[self.frame.categoriaBusqueda[2]]))
		sizer_principal_documentales.Add(self.label_10, 0, wx.EXPAND, 0)

		self.text_busqueda_documentales = wx.TextCtrl(self.panel_documentales, 301, "", style=wx.TE_PROCESS_ENTER)
		sizer_principal_documentales.Add(self.text_busqueda_documentales, 0, wx.EXPAND, 0)

		label_11 = wx.StaticText(self.panel_documentales, wx.ID_ANY, _("&Lista de documentales:"))
		sizer_principal_documentales.Add(label_11, 0, wx.EXPAND, 0)

		self.list_box_documentales = wx.ListBox(self.panel_documentales, 302)
		sizer_principal_documentales.Add(self.list_box_documentales, 1, wx.ALL | wx.EXPAND, 0)

#		self.accionDocumentalesBTN = wx.Button(self.panel_documentales, 303, _(u"&Acción"))
#		sizer_principal_documentales.Add(self.accionDocumentalesBTN, 0, wx.EXPAND, 0)

		self.panel_cortometrajes = wx.Panel(self.lst_book, wx.ID_ANY)
		self.lst_book.AddPage(self.panel_cortometrajes, _("Cortometrajes (Alt+5)"))

		sizer_principal_cortometrajes = wx.BoxSizer(wx.VERTICAL)

		self.label_12 = wx.StaticText(self.panel_cortometrajes, wx.ID_ANY, _("&Buscar cortometrajes por {}:").format(ajustes.listaFiltroBusqueda[self.frame.categoriaBusqueda[3]]))
		sizer_principal_cortometrajes.Add(self.label_12, 0, wx.EXPAND, 0)

		self.text_busqueda_cortometrajes = wx.TextCtrl(self.panel_cortometrajes, 401, "", style=wx.TE_PROCESS_ENTER)
		sizer_principal_cortometrajes.Add(self.text_busqueda_cortometrajes, 0, wx.EXPAND, 0)

		label_13 = wx.StaticText(self.panel_cortometrajes, wx.ID_ANY, _("&Lista de cortometrajes:"))
		sizer_principal_cortometrajes.Add(label_13, 0, wx.EXPAND, 0)

		self.list_box_cortometrajes = wx.ListBox(self.panel_cortometrajes, 402)
		sizer_principal_cortometrajes.Add(self.list_box_cortometrajes, 1, wx.ALL | wx.EXPAND, 0)

#		self.accionCortometrajesBTN = wx.Button(self.panel_cortometrajes, 403, _(u"&Acción"))
#		sizer_principal_cortometrajes.Add(self.accionCortometrajesBTN, 0, wx.EXPAND, 0)

#		self.panel_favoritos = wx.Panel(self.lst_book, wx.ID_ANY)
#		self.lst_book.AddPage(self.panel_favoritos, _("Favoritos (Alt+6)"))

#		sizer_principal_favoritos = wx.BoxSizer(wx.VERTICAL)

#		sizer_principal_favoritos.Add((0, 0), 0, 0, 0)

#		self.panel_estadisticas = wx.Panel(self.lst_book, wx.ID_ANY)
#		self.lst_book.AddPage(self.panel_estadisticas, _(u"Estadísticas (Alt+7)"))

#		sizer_principal_estadisticas = wx.BoxSizer(wx.VERTICAL)

#		sizer_principal_estadisticas.Add((0, 0), 0, 0, 0)

#		self.panel_opciones = wx.Panel(self.lst_book, wx.ID_ANY)
#		self.lst_book.AddPage(self.panel_opciones, _("Opciones (Alt+8)"))

#		sizer_principal_opciones = wx.BoxSizer(wx.VERTICAL)

#		sizer_principal_opciones.Add((0, 0), 0, 0, 0)

		sizer_reproductor = wx.BoxSizer(wx.HORIZONTAL)
		sizer_general.Add(sizer_reproductor, 0, wx.EXPAND, 0)

		self.atrasarBTN = wx.Button(self.panel_1, 1001, _("Atrasar"))
		sizer_reproductor.Add(self.atrasarBTN, 2, wx.EXPAND, 0)

		self.reproducirBTN = wx.Button(self.panel_1, 1002, _("Reproducir"))
		sizer_reproductor.Add(self.reproducirBTN, 2, wx.EXPAND, 0)

		self.adelantarBTN = wx.Button(self.panel_1, 1003, _("Adelantar"))
		sizer_reproductor.Add(self.adelantarBTN, 2, wx.EXPAND, 0)

		self.detenerBTN = wx.Button(self.panel_1, 1004, _("Detener"))
		sizer_reproductor.Add(self.detenerBTN, 2, wx.EXPAND, 0)

		sizer_menu = wx.BoxSizer(wx.HORIZONTAL)
		sizer_general.Add(sizer_menu, 0, wx.EXPAND, 0)

		sizer_controles = wx.BoxSizer(wx.HORIZONTAL)
		sizer_menu.Add(sizer_controles, 1, wx.EXPAND, 0)

		label_3 = wx.StaticText(self.panel_1, wx.ID_ANY, _("&Volumen:"))
		sizer_controles.Add(label_3, 0, 0, 0)

		self.volumenSLD = wx.Slider(self.panel_1, 1100, 0, 0, 100)
		self.volumenSLD.SetValue(ajustes.volumen)
		sizer_controles.Add(self.volumenSLD, 0, wx.EXPAND, 0)

		label_4 = wx.StaticText(self.panel_1, wx.ID_ANY, _("&Velocidad:"))
		sizer_controles.Add(label_4, 0, 0, 0)

		self.choiceRate = wx.Choice(self.panel_1, 1101, choices=ajustes.listaVelocidad)
		self.choiceRate.SetSelection(ajustes.velocidad)
		sizer_controles.Add(self.choiceRate, 0, wx.EXPAND, 0)

		label_5 = wx.StaticText(self.panel_1, wx.ID_ANY, _("&Salida:"))
		sizer_controles.Add(label_5, 0, 0, 0)

		self.choiceSalida = wx.Choice(self.panel_1, 1102, choices=self.reproductor.devicesHummans)
		self.choiceSalida.SetSelection(self.reproductor.deviceSelection)
		sizer_controles.Add(self.choiceSalida, 0, wx.EXPAND, 0)

		self.menuBTN = wx.Button(self.panel_1, 3000, _(u"&Menú"))
		sizer_menu.Add(self.menuBTN, 0, wx.BOTTOM | wx.RIGHT, 0)

#		self.panel_opciones.SetSizer(sizer_principal_opciones)

#		self.panel_estadisticas.SetSizer(sizer_principal_estadisticas)

#		self.panel_favoritos.SetSizer(sizer_principal_favoritos)

		self.panel_cortometrajes.SetSizer(sizer_principal_cortometrajes)

		self.panel_documentales.SetSizer(sizer_principal_documentales)

		self.panel_series.SetSizer(sizer_principal_series)

		self.panel_peliculas.SetSizer(sizer_principal_peliculas)

		self.panel_general.SetSizer(sizer_principal_general)

		self.panel_1.SetSizer(sizer_general)

		self.Layout()
		self.CenterOnScreen()
		self.cargaEventos()

	def cargaEventos(self):
		""" Definimos todos los eventos de la ventana principal """
		self.lst_book.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.tabChange)
		self.Bind(wx.EVT_CHOICE,self.onChoice)
		self.volumenSLD.Bind(wx.EVT_SLIDER, self.onVolumen)
		self.Bind(wx.EVT_CONTEXT_MENU, self.menuSetID)

		self.Bind(wx.EVT_BUTTON, self.onBoton)

		self.Bind(wx.EVT_CHAR_HOOK, self.OnKeyEvent)
		self.Bind(wx.EVT_CLOSE, self.onSalir)

		self.cargaInicio()

	def cargaInicio(self):
		""" Esta función tendra lo necesario para cuando abra la ventana principal """
		self.IS_SONANDO = False
		if self.reproductor.estado() == "State.Playing":
			self.reproductor.pause()
			msg = \
_("""Pausando la reproducción hasta que cargue la interface.""")
			if ajustes.IS_HABLAR:
				utilidades.speak(0.1, msg)
			self.IS_SONANDO = True

		# Mostramos últimas 10 peliculas.
		for i in range(ajustes.dict_resultados.get(ajustes.resultados)):
			self.list_box_ultimos.Append(self.Peliculas.peliculas[i].titulo)
		self.list_box_ultimos.SetSelection(0)
		self.list_box_ultimos.SetFocus()

		# Añadimos peliculas
		self.list_box_peliculas.Clear()
		for i in range(0, len(self.Peliculas.peliculas)):
			self.list_box_peliculas.Append(self.Peliculas.peliculas[i].titulo)
		self.list_box_peliculas.SetSelection(0)

		# Añadimos series
		self.list_box_series.Clear()
		for i in range(0, len(self.Series.series)):
			self.list_box_series.Append(self.Series.series[i].titulo)
		self.list_box_series.SetSelection(0)

		# Añadimos documentales
		self.list_box_documentales.Clear()
		for i in range(0, len(self.Documentales.documentales)):
			self.list_box_documentales.Append(self.Documentales.documentales[i].titulo)
		self.list_box_documentales.SetSelection(0)

		# Añadimos cortometrajes
		self.list_box_cortometrajes.Clear()
		for i in range(0, len(self.Cortometrajes.cortometrajes)):
			self.list_box_cortometrajes.Append(self.Cortometrajes.cortometrajes[i].titulo)
		self.list_box_cortometrajes.SetSelection(0)

		# Actualizamos pestaña.
		self.onTabAcciones(0)

		# Comprobamos si estaba sonando algo
		if self.IS_SONANDO:
			msg = \
_("""Reanudando la reproducción.""")
			if ajustes.IS_HABLAR:
				utilidades.speak(0.1, msg)
			self.reproductor.volumen(int(ajustes.volumen))
			self.reproductor.velocidad(float(ajustes.listaVelocidad[ajustes.velocidad]))
			self.reproductor.play()

		# Comprobamos si la reproducción esta activa y activamos botones o no del reproductor igualmente cambiamos la etiqueta del botón reproducir segun estado y añadimos las teclas globales del reproductor.
		self.estadoBotones(False) if self.reproductor.estado() in ["State.NothingSpecial", "State.Stopped"] else self.estadoBotones(True)
		self.reproducirBTN.SetLabel(_("Pausar")) if self.reproductor.estado() == "State.Playing" else self.reproducirBTN.SetLabel(_("Reproducir"))
		self.reproductorKeyboard.onTeclasReproductor()
		# Si la reproducción esta parada actualizamos con lo que hay en ajustes, volumen, velocidad y dispositivo salida.
		if self.reproductor.estado() in ["State.NothingSpecial", "State.Stopped"]:
			self.reproductor.volumen(int(ajustes.volumen))
			self.reproductor.velocidad(float(ajustes.listaVelocidad[ajustes.velocidad]))
			self.reproductor.deviceSelection = 0
			self.reproductor.GetDevices()
			self.choiceSalida.Clear()
			self.choiceSalida.Append(self.reproductor.devicesHummans)
			self.choiceSalida.SetSelection(self.reproductor.deviceSelection)
			self.reproductor.SetDevice(self.reproductor.devices[self.reproductor.deviceSelection])

	def onFoco(self):
		if self.bandera_foco == 0: # 		self.list_box_ultimos
			self.list_box_ultimos.SetFocus()
		elif self.bandera_foco == 1: # 		self.list_box_peliculas
			self.list_box_peliculas.SetFocus()
		elif self.bandera_foco == 2: # 		self.list_box_series
			self.list_box_series.SetFocus()
		elif self.bandera_foco == 3: # 		self.list_box_documentales
			self.list_box_documentales.SetFocus()
		elif self.bandera_foco == 4: # 		self.list_box_cortometrajes
			self.list_box_cortometrajes.SetFocus()

	def tabChange(self, event):
		""" Función para llamar a onTabAcciones y pasarle la pestaña que esta activa """
		self.onTabAcciones(event.GetSelection())

	def onTabAcciones(self, event):
		""" Función para ejecutar acciones dependiendo de la pestaña seleccionada """
		nombre = "{} {}".format(addonHandler.Addon(os.path.join(globalVars.appArgs.configPath, "addons", "Audiocinemateca")).name, addonHandler.Addon(os.path.join(globalVars.appArgs.configPath, "addons", "Audiocinemateca")).version)
		self.bandera_foco = event
		if event == 0: # Pagina General
			self.SetTitle("{} - {}".format(nombre, _("General")))
		elif event == 1: # Pagina películas
			self.SetTitle("{} - {}".format(nombre, _("Películas")))
		elif event == 2: # Pagina series
			self.SetTitle("{} - {}".format(nombre, _("Series")))
		elif event == 3: # Pagina documentales
			self.SetTitle("{} - {}".format(nombre, _("Documentales")))
		elif event == 4: # Pagina cortometrajes
			self.SetTitle("{} - {}".format(nombre, _("Cortometrajes")))
		elif event == 5: # Pagina estadísticas
			self.SetTitle("{} - {}".format(nombre, _("Estadísticas")))

	def onChoice(self, event):
		""" Función que manejara los choices de las distintas pestañas y realizara las correspondientes acciones dependiendo de lo elegido """
		itemID = event.GetId()
		obj = event.GetEventObject()
		id = obj.GetSelection()
		if itemID == 1: # choice_ultimos
			self.list_box_ultimosChoice(id)
		elif itemID == 1101: # choice de velocidad
			ajustes.velocidad = event.GetSelection()
			self.reproductor.velocidad(float(ajustes.listaVelocidad[ajustes.velocidad]))
		elif itemID == 1102: # choice de salida sonido
			self.reproductor.deviceSelection = event.GetSelection()
			self.reproductor.SetDevice(self.reproductor.devices[self.reproductor.deviceSelection])

	def list_box_ultimosChoice(self, event):
		""" Función que cambiara en el listbox ultimos añadidos segun elijamos en el choice de ultimos añadidos, el event recibe un número dependiendo del GetSelection del choice """
		self.list_box_ultimos.Clear()
		for i in range(ajustes.dict_resultados.get(ajustes.resultados)):
			if event == 0: # Peliculas
				self.list_box_ultimos.Append(self.Peliculas.peliculas[i].titulo)
			elif event == 1: # Series
				self.list_box_ultimos.Append(self.Series.series[i].titulo)
			elif event == 2: # Documentales
				self.list_box_ultimos.Append(self.Documentales.documentales[i].titulo)
			elif event == 3: # Cortometrajes
				self.list_box_ultimos.Append(self.Cortometrajes.cortometrajes[i].titulo)
		self.list_box_ultimos.SetSelection(0)

	def onVolumen(self, event):
		""" Función para actualizar el volumen del complemento """
		ajustes.volumen = self.volumenSLD.GetValue()
		self.reproductor.volumen(ajustes.volumen)

	def estadoBotones(self, event):
		""" Función para manejar el estado de los botones del reproductor, el evento recibe True o False dependiendo de si estan habilitados o deshabilitados """
		if event:
			self.atrasarBTN.Enable()
			self.reproducirBTN.Enable()
			self.adelantarBTN.Enable()
			self.detenerBTN.Enable()
			self.reproducirBTN.SetFocus()
			self.choiceSalida.Enable()
			self.reproductor.SetDevice(self.reproductor.devices[self.reproductor.deviceSelection])
		else:
			self.atrasarBTN.Disable()
			self.reproducirBTN.Disable()
			self.adelantarBTN.Disable()
			self.detenerBTN.Disable()
			self.choiceSalida.Disable()
			self.reproductor.deviceSelection = 0
			self.reproductor.GetDevices()
			self.choiceSalida.Clear()
			self.choiceSalida.Append(self.reproductor.devicesHummans)
			self.choiceSalida.SetSelection(self.reproductor.deviceSelection)
			self.reproductor.SetDevice(self.reproductor.devices[self.reproductor.deviceSelection])

	def onPrevisualizadorFicha(self, id, datos, datosSeries=None):
		if id in [0, 2, 3]: # Para peliculas, documentales y cortometrajes
			dlg = dialogos.Previsualizador(self, datos, id)
		else: # Para series
			dlg = dialogos.PrevisualizadorSerie(self, datos, datosSeries)

		res = dlg.ShowModal()
		if res == 0: # Reproducir
			dlg.Destroy()

			if id == 0: # Peliculas
				enlace_temporal = datos["enlaces"][dlg.choice_enlaces.GetSelection()]
			elif id == 1: # Series
				enlace_temporal = dlg.enlacesEpisodios[dlg.list_box_episodios.GetSelection()]
			elif id in [2, 3]: # Documentales y Cortometrajes
				enlace_temporal = datos["enlace"]

			url_temporal = "https://audiocinemateca.com/{}".format(enlace_temporal)
			url= url_temporal.replace("//", "//{}:{}@".format(ajustes.usuario, ajustes.contraseña))
			self.reproductor.file(url)
			self.reproductor.volumen(int(ajustes.volumen))
			self.reproductor.velocidad(float(ajustes.listaVelocidad[ajustes.velocidad]))
			self.reproductor.play()
			self.reproducirBTN.SetLabel(_("Pausar"))
			self.estadoBotones(True)

		elif res == 1: # Descargar
			dlg.Destroy()
			if id == 0: # Peliculas
				enlace_temporal = datos["enlaces"][dlg.choice_enlaces.GetSelection()]
			elif id == 1: # Series
				enlace_temporal = dlg.enlacesEpisodios[dlg.list_box_episodios.GetSelection()]
			elif id in [2, 3]: # Documentales y Cortometrajes
				enlace_temporal = datos["enlace"]

			url_temporal = "https://audiocinemateca.com/{}".format(enlace_temporal)
			dlgDir = wx.DirDialog(self, _("Seleccione un directorio donde guardar el MP3:"),
				style=wx.DD_DEFAULT_STYLE
			)
			if dlgDir.ShowModal() == wx.ID_OK:
				directorio =dlgDir.GetPath()
				dlgDir.Destroy()
				dlg1 = dialogos.DownloadDialog(self, 2, [ajustes.usuario, ajustes.contraseña, url_temporal, directorio])
				result = dlg1.ShowModal()
				if result == 0:
					dlg1.Destroy()
					return
				else:
					dlg1.Destroy()
					return
			else:
				dlgDir.Destroy()

		elif res == 10: # Cerrar
			dlg.Destroy()
		return

	def onTextFiltro(self, event):
		id = event.GetId()
		menu = wx.Menu()
		if id == 101: # Campo peliculas
			for i in range(len(ajustes.listaFiltroBusqueda)):
				i = menu.Append(i+ 1000, ajustes.listaFiltroBusqueda[i], "", wx.ITEM_CHECK)
			menu.Bind(wx.EVT_MENU_RANGE, self.onTextFiltroValor, id=1000, id2=len(ajustes.listaFiltroBusqueda)-1+1000)
			menu.Check(self.frame.categoriaBusqueda[0]+1000, True)
			self.text_busqueda_peliculas.PopupMenu(menu)
		elif id == 201: # Campo series
			for i in range(len(ajustes.listaFiltroBusqueda)):
				i = menu.Append(i+ 2000, ajustes.listaFiltroBusqueda[i], "", wx.ITEM_CHECK)
			menu.Bind(wx.EVT_MENU_RANGE, self.onTextFiltroValor, id=2000, id2=len(ajustes.listaFiltroBusqueda)-1+2000)
			menu.Check(self.frame.categoriaBusqueda[1]+2000, True)
			self.text_busqueda_series.PopupMenu(menu)
		elif id == 301: # Campo documentales
			for i in range(len(ajustes.listaFiltroBusqueda)):
				i = menu.Append(i+ 3000, ajustes.listaFiltroBusqueda[i], "", wx.ITEM_CHECK)
			menu.Bind(wx.EVT_MENU_RANGE, self.onTextFiltroValor, id=3000, id2=len(ajustes.listaFiltroBusqueda)-1+3000)
			menu.Check(self.frame.categoriaBusqueda[2]+3000, True)
			self.text_busqueda_documentales.PopupMenu(menu)
		elif id == 401: # Campo cortometrajes
			for i in range(len(ajustes.listaFiltroBusqueda)):
				i = menu.Append(i+ 4000, ajustes.listaFiltroBusqueda[i], "", wx.ITEM_CHECK)
			menu.Bind(wx.EVT_MENU_RANGE, self.onTextFiltroValor, id=4000, id2=len(ajustes.listaFiltroBusqueda)-1+4000)
			menu.Check(self.frame.categoriaBusqueda[3]+4000, True)
			self.text_busqueda_cortometrajes.PopupMenu(menu)

	def onTextFiltroValor(self, event):
		id = event.GetId()
		if id in [1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011]: # Filtro peliculas
			self.frame.categoriaBusqueda[0] = id - 1000
			self.label_6.SetLabel(_(u"&Buscar películas por {}:").format(ajustes.listaFiltroBusqueda[self.frame.categoriaBusqueda[0]]))
		elif id in [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011]: # Filtro series
			self.frame.categoriaBusqueda[1] = id - 2000
			self.label_8.SetLabel(_(u"&Buscar series por {}:").format(ajustes.listaFiltroBusqueda[self.frame.categoriaBusqueda[1]]))
		elif id in [3000, 3001, 3002, 3003, 3004, 3005, 3006, 3007, 3008, 3009, 3010, 3011]: # Filtro documentales
			self.frame.categoriaBusqueda[2] = id - 3000
			self.label_10.SetLabel(_(u"&Buscar documentales por {}:").format(ajustes.listaFiltroBusqueda[self.frame.categoriaBusqueda[2]]))
		elif id in [4000, 4001, 4002, 4003, 4004, 4005, 4006, 4007, 4008, 4009, 4010, 4011]: # Filtro cortometrajes
			self.frame.categoriaBusqueda[3] = id - 4000
			self.label_12.SetLabel(_(u"&Buscar cortometrajes por {}:").format(ajustes.listaFiltroBusqueda[self.frame.categoriaBusqueda[3]]))

	def onTextEnter(self, event):
		dict_filtro = {
			0: "titulo",
			1: "anio",
			2: "genero",
			3: "pais",
			4: "director",
			5: "guion",
			6: "musica",
			7: "fotografia",
			8: "reparto",
			9: "productora",
			10: "narracion",
			11: "sinopsis",
		}
		msg_info_1 = _("Cargando todos los títulos…")
		msg_info_2 = _("No a echo ninguna búsqueda todavía. Ya se muestran todos los títulos.")
		id = event.GetId()
		if event.GetValue() == "": # Sin nada en el campo de busqueda volvemos a valores defecto
			if id == 101: # peliculas
				if self.IS_BUSQUEDA_PELICULAS:
					if ajustes.IS_HABLAR: utilidades.speak(0.1, msg_info_1)
				else:
					if ajustes.IS_HABLAR: utilidades.speak(0.1, msg_info_2)
					return
				self.tempBusquedaPeliculas = None
				self.IS_BUSQUEDA_PELICULAS = False
				# Añadimos peliculas
				self.list_box_peliculas.Clear()
				for i in range(0, len(self.Peliculas.peliculas)):
					self.list_box_peliculas.Append(self.Peliculas.peliculas[i].titulo)
				self.list_box_peliculas.SetSelection(0)
			elif id == 201: # series
				if self.IS_BUSQUEDA_SERIES:
					if ajustes.IS_HABLAR: utilidades.speak(0.1, msg_info_1)
				else:
					if ajustes.IS_HABLAR: utilidades.speak(0.1, msg_info_2)
					return
				self.tempBusquedaSeries = None
				self.IS_BUSQUEDA_SERIES = False
				# Añadimos series
				self.list_box_series.Clear()
				for i in range(0, len(self.Series.series)):
					self.list_box_series.Append(self.Series.series[i].titulo)
				self.list_box_series.SetSelection(0)
			elif id == 301: # documentales
				if self.IS_BUSQUEDA_DOCUMENTALES:
					if ajustes.IS_HABLAR: utilidades.speak(0.1, msg_info_1)
				else:
					if ajustes.IS_HABLAR: utilidades.speak(0.1, msg_info_2)
					return
				self.tempBusquedaDocumentales = None
				self.IS_BUSQUEDA_DOCUMENTALES = False
				# Añadimos documentales
				self.list_box_documentales.Clear()
				for i in range(0, len(self.Documentales.documentales)):
					self.list_box_documentales.Append(self.Documentales.documentales[i].titulo)
				self.list_box_documentales.SetSelection(0)
			elif id == 401: # cortometrajes
				if self.IS_BUSQUEDA_CORTOMETRAJES:
					if ajustes.IS_HABLAR: utilidades.speak(0.1, msg_info_1)
				else:
					if ajustes.IS_HABLAR: utilidades.speak(0.1, msg_info_2)
					return
				self.tempBusquedaCortometrajes = None
				self.IS_BUSQUEDA_CORTOMETRAJES = False
				# Añadimos cortometrajes
				self.list_box_cortometrajes.Clear()
				for i in range(0, len(self.Cortometrajes.cortometrajes)):
					self.list_box_cortometrajes.Append(self.Cortometrajes.cortometrajes[i].titulo)
				self.list_box_cortometrajes.SetSelection(0)
			self.onFoco()
		else: # Hay texto en el campo busqueda
			buscar = event.GetValue().lower()
			if id == 101: # peliculas
				filtro = "Titulo" if self.frame.categoriaBusqueda[0] == 0 else dict_filtro.get(self.frame.categoriaBusqueda[0])
				self.tempBusquedaPeliculas = self.Peliculas.buscar(buscar, filtro)
				if self.tempBusquedaPeliculas: # Si hay resultados
					self.IS_BUSQUEDA_PELICULAS = True
					# Añadimos peliculas
					self.list_box_peliculas.Clear()
					for i in range(0, len(self.tempBusquedaPeliculas)):
						self.list_box_peliculas.Append(self.tempBusquedaPeliculas[i]["Titulo"])
					self.list_box_peliculas.SetSelection(0)
					self.onFoco()
				else: # No hay resultados
					self.IS_BUSQUEDA_PELICULAS = True
					self.list_box_peliculas.Clear()
					self.list_box_peliculas.Append(_("Sin resultados"))
					self.list_box_peliculas.SetSelection(0)
					self.onFoco()

			elif id == 201: # series
				filtro = dict_filtro.get(self.frame.categoriaBusqueda[1])
				self.tempBusquedaSeries = self.Series.buscar(buscar, filtro)
				if self.tempBusquedaSeries: # Si hay resultados
					self.IS_BUSQUEDA_SERIES = True
					# Añadimos series
					self.list_box_series.Clear()
					for i in range(0, len(self.tempBusquedaSeries)):
						self.list_box_series.Append(self.tempBusquedaSeries[i]["titulo"])
					self.list_box_series.SetSelection(0)
					self.onFoco()
				else: # No hay resultados
					self.IS_BUSQUEDA_SERIES = True
					self.list_box_series.Clear()
					self.list_box_series.Append(_("Sin resultados"))
					self.list_box_series.SetSelection(0)
					self.onFoco()

			elif id == 301: # documentales
				filtro = dict_filtro.get(self.frame.categoriaBusqueda[2])
				self.tempBusquedaDocumentales = self.Documentales.buscar(buscar, filtro)
				if self.tempBusquedaDocumentales: # Si hay resultados
					self.IS_BUSQUEDA_DOCUMENTALES = True
					# Añadimos documentales
					self.list_box_documentales.Clear()
					for i in range(0, len(self.tempBusquedaDocumentales)):
						self.list_box_documentales.Append(self.tempBusquedaDocumentales[i]["titulo"])
					self.list_box_documentales.SetSelection(0)
					self.onFoco()
				else: # No hay resultados
					self.IS_BUSQUEDA_DOCUMENTALES = True
					self.list_box_documentales.Clear()
					self.list_box_documentales.Append(_("Sin resultados"))
					self.list_box_documentales.SetSelection(0)
					self.onFoco()

			elif id == 401: # cortometrajes
				filtro = dict_filtro.get(self.frame.categoriaBusqueda[3])
				self.tempBusquedaCortometrajes = self.Cortometrajes.buscar(buscar, filtro)
				if self.tempBusquedaCortometrajes: # Si hay resultados
					self.IS_BUSQUEDA_CORTOMETRAJES = True
					# Añadimos cortometrajes
					self.list_box_cortometrajes.Clear()
					for i in range(0, len(self.tempBusquedaCortometrajes)):
						self.list_box_cortometrajes.Append(self.tempBusquedaCortometrajes[i]["titulo"])
					self.list_box_cortometrajes.SetSelection(0)
					self.onFoco()
				else: # No hay resultados
					self.IS_BUSQUEDA_CORTOMETRAJES = True
					self.list_box_cortometrajes.Clear()
					self.list_box_cortometrajes.Append(_("Sin resultados"))
					self.list_box_cortometrajes.SetSelection(0)
					self.onFoco()

	def onListboxEnter(self, event, ):
		""" Función que controlara cuando pulsemos intro en un item en los listbox"""
		id = event.GetId()
		if event.GetString(event.GetSelection()) == _("Sin resultados"): return # No hay resultados de busqueda y no continuamos
		if id == 2: # listbox ultimos
			categoria_id = self.choice_ultimos.GetSelection()
			if categoria_id == 0: # Categoría peliculas
				datos = self.Peliculas.get_original_orden(event.GetSelection())
			elif categoria_id == 1: # Categoría series
				datos = self.Series.get_original_orden(event.GetSelection())
				datosSeries = self.datos.GetDatosSerie(datos["capitulos"])
			elif categoria_id == 2: # Categoría documentales
				datos = self.Documentales.get_original_orden(event.GetSelection())
			elif categoria_id == 3: # Categoría cortometrajes
				datos = self.Cortometrajes.get_original_orden(event.GetSelection())
			self.onPrevisualizadorFicha(categoria_id, datos) if categoria_id in [0, 2, 3] else self.onPrevisualizadorFicha(categoria_id, datos, datosSeries)
		elif id == 102: # listbox peliculas
			if self.IS_BUSQUEDA_PELICULAS: # Estamos en busqueda
				datos = self.tempBusquedaPeliculas[event.GetSelection()]
			else: # Estamos en normal
				datos = self.Peliculas.get_original_orden(event.GetSelection())
			self.onPrevisualizadorFicha(0, datos)
		elif id == 202: # listbox series
			if self.IS_BUSQUEDA_SERIES: # Estamos en busqueda
				datos = self.tempBusquedaSeries[event.GetSelection()]
				datosSeries = self.datos.GetDatosSerie(datos["capitulos"])
			else: # Estamos en normal
				datos = self.Series.get_original_orden(event.GetSelection())
				datosSeries = self.datos.GetDatosSerie(datos["capitulos"])
			self.onPrevisualizadorFicha(1, datos, datosSeries)
		elif id == 302: # listbox documentales
			if self.IS_BUSQUEDA_DOCUMENTALES: # Estamos en busqueda
				datos = self.tempBusquedaDocumentales[event.GetSelection()]
			else: # Estamos en normal
				datos = self.Documentales.get_original_orden(event.GetSelection())
			self.onPrevisualizadorFicha(2, datos)
		elif id == 402: # listbox cortometrajes
			if self.IS_BUSQUEDA_CORTOMETRAJES: # Estamos en busqueda
				datos = self.tempBusquedaCortometrajes[event.GetSelection()]
			else: # Estamos en normal
				datos = self.Cortometrajes.get_original_orden(event.GetSelection())
			self.onPrevisualizadorFicha(3, datos)

	def onBoton(self, event):
		""" Función para manejar todos los botones apartir del id unico de la pantalla principal """
		obj = event.GetEventObject()
		itemID = obj.GetId()
		if itemID == 3: # Resultado aleatorio.
			z = self.datos.GetAleatoria(self.Peliculas, self.Series, self.Documentales, self.Cortometrajes)
			if z[0] == "peliculas":
				categoria_id = 0
				datos = self.Peliculas.get_original_orden(z[1])
			elif z[0] == "series":
				categoria_id = 1
				datos = self.Series.get_original_orden(z[1])
				datosSeries = self.datos.GetDatosSerie(datos["capitulos"])
			elif z[0] == "documentales":
				categoria_id = 2
				datos = self.Documentales.get_original_orden(z[1])
			elif z[0] == "cortometrajes":
				categoria_id = 3
				datos = self.Cortometrajes.get_original_orden(z[1])
			self.onPrevisualizadorFicha(categoria_id, datos) if categoria_id in [0, 2, 3] else self.onPrevisualizadorFicha(categoria_id, datos, datosSeries)

		elif itemID == 1001: # Atrasar
			self.reproductor.atrasar(ajustes.dict_tiempo.get(ajustes.atrasar))
		elif itemID == 1002: # Reproducir / Pausar
			self.reproductor.pause()
			self.reproducirBTN.SetLabel(_("Reproducir")) if self.reproductor.estado() == "State.Playing" else self.reproducirBTN.SetLabel(_("Pausar"))
		elif itemID == 1003: # Adelantar
			self.reproductor.adelantar(ajustes.dict_tiempo.get(ajustes.adelantar))
		elif itemID == 1004: # Parar
			self.reproductor.stop()
			self.reproducirBTN.SetLabel(_("Pausar")) if self.reproductor.estado() == "State.Playing" else self.reproducirBTN.SetLabel(_("Reproducir"))
			self.estadoBotones(False)
			self.onTabAcciones(self.lst_book.GetSelection())
			self.onFoco()
		elif itemID == 3000: # Botón Menú
			self.menu = wx.Menu()
			item1 = self.menu.Append(1, _("&Actualizar base de datos"))
			item2 = self.menu.Append(2, _("&Donar a la Audiocinemateca"))
			item3 = self.menu.Append(3, _("&Cerrar"))
			self.menu.Bind(wx.EVT_MENU, self.onMenusAcciones)
			self.menuBTN.PopupMenu(self.menu)

	def menuSetID(self, event):
		""" Función para obtener el id del widget desde que se invoca y se lo pasa a la función onMenus que contendra todos los menús de la aplicación """
		self.onMenus(event.GetId())

	def onMenus(self, event):
		""" Función que recibe el id en el evento de la función menuSetID para mostrar el menú del widget si lo tiene """
		id = event
		menu = wx.Menu()
		if id == 1001: # Menú boton atrasarBTN
			for i in range(len(ajustes.listaAtrasar)):
				i = menu.Append(i+ 4000, "{}".format(ajustes.listaAtrasar[i]), "", wx.ITEM_CHECK)
			menu.Bind(wx.EVT_MENU_RANGE, self.onMenusAcciones, id=4000, id2=len(ajustes.listaAtrasar)-1+4000)
			menu.Check(ajustes.atrasar+4000, True)
			self.atrasarBTN.PopupMenu(menu)
		elif id == 1003: # menu botón adelantarBTN
			for i in range(len(ajustes.listaAdelantar)):
				i = menu.Append(i + 5000, "{}".format(ajustes.listaAdelantar[i]), "", wx.ITEM_CHECK)
			menu.Bind(wx.EVT_MENU_RANGE, self.onMenusAcciones, id=5000, id2=len(ajustes.listaAdelantar)-1 + 5000)
			menu.Check(ajustes.adelantar + 5000, True)
			self.adelantarBTN.PopupMenu(menu)

	def onMenusAcciones(self, event):
		""" Recibe el id unico de los menus y ejecuta la acción """
		id = event.GetId()
		if id == 1: # Actualizar
			dlg1 = dialogos.DownloadDialog(self, 3, [ajustes.usuario, ajustes.contraseña, ajustes.versionLocal])
			result = dlg1.ShowModal()
			if result == 0:
				dlg1.Destroy()
				return
			elif result == 2:
				dlg1.Destroy()
				self.onSalir(None, True)
			else:
				dlg1.Destroy()
				return
		elif id == 2: # donar
			wx.LaunchDefaultBrowser("https://audiocinemateca.com/donaciones", flags=0)
		elif id == 3: # Cerrar
			self.onSalir(None)
		elif id in [4000, 4001, 4002, 4003, 4004]: # Ids de atrasar, hay que restar 4000 para guardar en ajustes ya que son ids creados especialmente para los menús y tienen que coincidir con la listaAtrasar
			ajustes.atrasar = id - 4000
			self.frame.AjustesApp.GuardaDatos()
			self.frame.AjustesApp.CargaDatos()
			self.frame.AjustesApp.refrescaDatos()
		elif id in [5000, 5001, 5002, 5003, 5004, 5005, 5006, 5007]: # Ids de adelantar, hay que restar 5000 para guardar en ajustes ya que son ids creados especialmente para los menús y tienen que coincidir con la listaAdelantar
			ajustes.adelantar = id - 5000
			self.frame.AjustesApp.GuardaDatos()
			self.frame.AjustesApp.CargaDatos()
			self.frame.AjustesApp.refrescaDatos()

	def OnKeyEvent(self, event):
		""" Función para controlar teclas especiales en toda la aplicación """
		foco = wx.Window.FindFocus().GetId()
		robot = wx.UIActionSimulator()
		if event.GetUnicodeKey() == wx.WXK_RETURN:
			# listbox
			if foco in [2, 102, 202, 302, 402]: # listbox ultimos, peliculas, series, documentales, cortometrajes
				wx.CallAfter(self.onListboxEnter, event.GetEventObject())
			# TextCtrl
			elif foco in [101, 201, 301, 401]: # campo busqueda peliculas, series, documentales, cortometrajes
				wx.CallAfter(self.onTextEnter, event.GetEventObject())

		elif (event.ControlDown(), event.GetUnicodeKey()) == (True, 73): # Control+I anuncia información posición listbox.
			if foco in [2, 102, 202, 302, 402]: # listbox ultimos
				obj = event.GetEventObject()
				if obj.GetString(obj.GetSelection()) == _("Sin resultados"): return
				msg = \
"""Se encuentra en el resultado {} de {}""".format(obj.GetSelection()+1, obj.GetCount())
				utilidades.speak(0.1, msg)

		elif (event.ControlDown(), event.GetUnicodeKey()) == (True, 70): # Control+F mueve foco en el listbox a número dado. o saca menú en campos de busqueda para filtrar
			if foco in [2, 102, 202, 302, 402]: # listbox
				obj = event.GetEventObject()
				if obj.GetString(obj.GetSelection()) == _("Sin resultados"): return
				total = obj.GetCount()
				dlg = dialogos.posicion(self.frame, total)
				result = dlg.ShowModal()
				if result == 0: # movemos foco
					dlg.Destroy()
					obj.SetSelection(int(dlg.numero.GetValue()) - 1)
				else: # Cancelamos
					dlg.Destroy()
			elif foco in [101, 201, 301, 401]: # campo busqueda peliculas, series, documentales, cortometrajes
				wx.CallAfter(self.onTextFiltro, event.GetEventObject())

		elif (event.ControlDown(), event.GetKeyCode()) == (True, 66): # Ctrl+B borra campo y vuelve listbox a predefinido
			if foco in [101, 201, 301, 401]: # campo busqueda peliculas, series, documentales, cortometrajes
				obj = event.GetEventObject()
				obj.Clear()
				wx.CallAfter(self.onTextEnter, obj)

		elif event.GetUnicodeKey() == wx.WXK_ESCAPE:
			self.onSalir(None)

		elif (event.AltDown(), event.GetKeyCode()) == (True, 49): # Alt + 1 lleva a la pestaña general
			self.lst_book.ChangeSelection(0)
			robot.KeyUp(wx.WXK_RETURN)
			self.list_box_ultimos.SetFocus()
			self.onTabAcciones(0)
		elif (event.AltDown(), event.GetKeyCode()) == (True, 50): # Alt + 2 lleva a la pestaña peliculas
			self.lst_book.ChangeSelection(1)
			robot.KeyUp(wx.WXK_RETURN)
			self.list_box_peliculas.SetFocus()
			self.onTabAcciones(1)
		elif (event.AltDown(), event.GetKeyCode()) == (True, 51): # Alt + 3 lleva a la pestaña series
			self.lst_book.ChangeSelection(2)
			robot.KeyUp(wx.WXK_RETURN)
			self.list_box_series.SetFocus()
			self.onTabAcciones(2)
		elif (event.AltDown(), event.GetKeyCode()) == (True, 52): # Alt + 4 lleva a la pestaña documentales
			self.lst_book.ChangeSelection(3)
			robot.KeyUp(wx.WXK_RETURN)
			self.list_box_documentales.SetFocus()
			self.onTabAcciones(3)
		elif (event.AltDown(), event.GetKeyCode()) == (True, 53): # Alt + 5 lleva a la pestaña cortometrajes
			self.lst_book.ChangeSelection(4)
			robot.KeyUp(wx.WXK_RETURN)
			self.list_box_cortometrajes.SetFocus()
			self.onTabAcciones(4)

		elif (event.ControlDown(), event.GetKeyCode()) == (True, 32): # Ctrl+Espacio da información de pestaña
			pestañaDict = {
				0: _("General"),
				1: _("Películas"),
				2: _("Series"),
				3: _("Documentales"),
				4: _("Cortometrajes"),
			}
			utilidades.speak(0.1, _("Se encuentra en la pestaña {}".format(pestañaDict.get(self.lst_book.GetSelection()))))

		else:
			event.Skip()

	def onSalir(self, event, lanzar=False):
		ajustes.IS_WinON = False
		self.reproductor.addFrameMain(None)
		self.frame.AjustesApp.GuardaDatos()
		self.frame.AjustesApp.CargaDatos()
		self.frame.AjustesApp.refrescaDatos()
		self.datos.clear()
		self.Destroy()
		gui.mainFrame.postPopup()
		if lanzar:
			HiloComplemento(_selfTemp, 1).start()

class VentanaOpciones(wx.Dialog):
	def __init__(self, parent, frame):
		super(VentanaOpciones, self).__init__(parent, -1, _("Opciones de Audiocinemateca"), size = (800, 600))

		# Bandera ventana opciones abierta.
		ajustes.IS_WinON = True
		# Obtenemos el frame del complemento
		self.frame = frame

		self.panel_general = wx.Panel(self, wx.ID_ANY)

		sizer_general = wx.BoxSizer(wx.VERTICAL)

		self.listBook = wx.Notebook(self.panel_general, wx.ID_ANY)
		sizer_general.Add(self.listBook, 1, wx.EXPAND, 0)

		self.panel_list_general = wx.Panel(self.listBook, wx.ID_ANY)
		self.listBook.AddPage(self.panel_list_general, _("General"))

		sizer_list_general = wx.BoxSizer(wx.VERTICAL)

		self.checkbox_1 = wx.CheckBox(self.panel_list_general, 1, _("Activar o desactivar los mensajes &informativos."))
		self.checkbox_1.SetValue(ajustes.IS_HABLAR)
		sizer_list_general.Add(self.checkbox_1, 0, wx.EXPAND, 0)

		label_1 = wx.StaticText(self.panel_list_general, wx.ID_ANY, _("Cantidad de resultados a mostrar de las &últimas entradas"))
		sizer_list_general.Add(label_1, 0, wx.EXPAND, 0)

		self.choice_resultados = wx.Choice(self.panel_list_general, 2, choices=ajustes.listaResultados)
		self.choice_resultados.SetSelection(ajustes.resultados)
		sizer_list_general.Add(self.choice_resultados, 0, wx.EXPAND, 0)

		self.defectoBTN = wx.Button(self.panel_list_general, 3, _("&Volver a valores por defecto"))
		sizer_list_general.Add(self.defectoBTN, 0, wx.EXPAND, 0)

		self.panel_list_reproductor = wx.Panel(self.listBook, wx.ID_ANY)
		self.listBook.AddPage(self.panel_list_reproductor, _("Reproductor"))

		sizer_list_reproductor = wx.BoxSizer(wx.VERTICAL)

		label_2 = wx.StaticText(self.panel_list_reproductor, wx.ID_ANY, _(u"Seleccione el tiempo para retroceder la reproducción:"))
		sizer_list_reproductor.Add(label_2, 0, wx.EXPAND, 0)

		self.choice_atrasar = wx.Choice(self.panel_list_reproductor, 101, choices=ajustes.listaAtrasar)
		self.choice_atrasar.SetSelection(ajustes.atrasar)
		sizer_list_reproductor.Add(self.choice_atrasar, 0, wx.EXPAND, 0)

		label_3 = wx.StaticText(self.panel_list_reproductor, wx.ID_ANY, _(u"Seleccione el tiempo para adelantar la reproducción:"))
		sizer_list_reproductor.Add(label_3, 0, wx.EXPAND, 0)

		self.choice_adelantar = wx.Choice(self.panel_list_reproductor, 102, choices=ajustes.listaAdelantar)
		self.choice_adelantar.SetSelection(ajustes.adelantar)
		sizer_list_reproductor.Add(self.choice_adelantar, 0, wx.EXPAND, 0)

		sizer_botones = wx.BoxSizer(wx.HORIZONTAL)
		sizer_general.Add(sizer_botones, 0, wx.EXPAND, 0)

		self.aceptarBTN = wx.Button(self.panel_general, 1001, _("&Aceptar"))
		sizer_botones.Add(self.aceptarBTN, 2, wx.EXPAND, 0)

		self.cancelarBTN = wx.Button(self.panel_general, 1002, _("&Cancelar"))
		sizer_botones.Add(self.cancelarBTN, 2, wx.EXPAND, 0)

		self.panel_list_reproductor.SetSizer(sizer_list_reproductor)

		self.panel_list_general.SetSizer(sizer_list_general)

		self.panel_general.SetSizer(sizer_general)

		self.Layout()
		self.CenterOnScreen()

		self.cargaEventos()

	def cargaEventos(self):
		self.Bind(wx.EVT_BUTTON,self.onBoton)
		self.Bind(wx.EVT_CLOSE, self.onSalir)
		self.checkbox_1.SetFocus()

	def onBoton(self, event):
		id = event.GetId()
		if id == 3: # Valores defecto
			xguiMsg = \
_("""El complemento borrará toda la configuración guardada y volverá a valores por defecto.

¿Esta seguro que desea continuar?""")
			msgx = wx.MessageDialog(None, xguiMsg, "Pregunta", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
			ret = msgx.ShowModal()
			if ret == wx.ID_YES:
				msgx.Destroy
				self.frame.AjustesApp.GuardaDatosDefecto()
				self.frame.AjustesApp.CargaDatos()
				self.frame.AjustesApp.refrescaDatos()
				self.onSalir(None)
			else:
				msgx.Destroy
		elif id == 1001: # Aceptar
			ajustes.IS_HABLAR = self.checkbox_1.GetValue()
			ajustes.resultados = self.choice_resultados.GetSelection()
			ajustes.atrasar = self.choice_atrasar.GetSelection()
			ajustes.adelantar = self.choice_adelantar.GetSelection()
			self.frame.AjustesApp.GuardaDatos()
			self.frame.AjustesApp.CargaDatos()
			self.frame.AjustesApp.refrescaDatos()
			self.onSalir(None)

		elif id == 1002: # Cancelar
			self.onSalir(None)

	def onSalir(self, event):
		ajustes.IS_WinON = False
		self.Destroy()
		gui.mainFrame.postPopup()

class keyboardReproductor():
	""" Esta clase controlara las teclas especiales para el reproductor mientras la aplicación este abierta, funcionara en todas las ventanas de la aplicación """
	def __init__(self, ):

		# Pasaremos tanto el frame de la ventana principal, como de las ventanas de dialogo
		self.frame = None
		self.frameSecundario = None

	def addFrame(self, frame):
		""" Función para poder pasar el frame principal desde la ventana principal a esta clase """
		self.frame = frame

	def addFrameSecundario(self, frameSecundario):
		""" Función para recibir el frame de los dialogos """
		self.frameSecundario = frameSecundario

	def onTeclasReproductor(self, opcion=0):
		""" Función para definir las teclas que se utilizarán en el reproductor en cualquier ventana del complemento """
		IDS = [10000, 10001, 10002, 10003, 10004, 10005, 10006, 10007, 10008, 10009]
		for i in IDS:
			wx.RegisterId(i)
			if opcion == 0: # Pantalla principal
				self.frame.Bind(wx.EVT_MENU, self.onTeclasReproductorFunciones, id=i)
			else:
				self.frameSecundario.Bind(wx.EVT_MENU, self.onTeclasReproductorFunciones, id=i)

		volumenAbajo = wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F5, 10000)
		volumenArriba = wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F6, 10001)
		velocidadAbajo = wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F7, 10002)
		velocidadArriba = wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F8, 10003)
		atrsar = wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F1, 10004)
		reproducir = wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F2, 10005)
		adelantar = wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F3, 10006)
		detener = wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F4, 10007)
		informacion = wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F9, 10008)
		informacionValor = wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F12, 10009)
		listaTeclas = [volumenAbajo, volumenArriba, velocidadAbajo, velocidadArriba, atrsar, reproducir, adelantar, detener, informacion, informacionValor]
		tabla_acceleradora = wx.AcceleratorTable(listaTeclas)
		if opcion == 0:
			self.frame.SetAcceleratorTable(tabla_acceleradora)
		else:
			self.frameSecundario.SetAcceleratorTable(tabla_acceleradora)

	def onTeclasReproductorFunciones(self, event):
		""" Función que recibe que tecla fue pulsada y realiza la acción """
		id = event.GetId()
		if id == 10000: # Bajar volumen
			ajustes.volumen = self.frame.volumenSLD.GetValue() - 1 if self.frame.volumenSLD.GetValue() > 0 else 0
			self.frame.reproductor.volumen(ajustes.volumen)
			self.frame.volumenSLD.SetValue(ajustes.volumen)
			msg = f"Volumen {ajustes.volumen}%"
			info = ""
		elif id == 10001: # Subir volumen
			ajustes.volumen = self.frame.volumenSLD.GetValue() +1 if self.frame.volumenSLD.GetValue() < 100 else 100
			self.frame.reproductor.volumen(ajustes.volumen)
			self.frame.volumenSLD.SetValue(ajustes.volumen)
			msg = f"Volumen {ajustes.volumen}%"
			info = ""
		elif id == 10002: # bajar velocidad
			ajustes.velocidad = self.frame.choiceRate.GetSelection() - 1 if self.frame.choiceRate.GetSelection() - 1 > 0 else 0
			self.frame.reproductor.velocidad(float(ajustes.listaVelocidad[ajustes.velocidad]))
			self.frame.choiceRate.SetSelection(ajustes.velocidad)
			msg = f"Velocidad {ajustes.listaVelocidad[ajustes.velocidad]}"
			info = ""
		elif id == 10003: # subir velocidad
			ajustes.velocidad = self.frame.choiceRate.GetSelection() + 1 if self.frame.choiceRate.GetSelection() + 1 < 17 else 17
			self.frame.reproductor.velocidad(float(ajustes.listaVelocidad[ajustes.velocidad]))
			self.frame.choiceRate.SetSelection(ajustes.velocidad)
			msg = f"Velocidad {ajustes.listaVelocidad[ajustes.velocidad]}"
			info = ""
		elif id == 10004: # Atrasar
			self.frame.reproductor.atrasar(ajustes.dict_tiempo.get(ajustes.atrasar))
			msg = _("Sin nada en reproducción") if self.frame.reproductor.estado() in ["State.NothingSpecial", "State.Stopped"] else _("Atrasando {}").format(ajustes.listaAtrasar[ajustes.atrasar])
			info = ""
		elif id == 10005: # Reproducir / Pausar
			self.frame.reproductor.pause()
			self.frame.reproducirBTN.SetLabel(_("Reproducir")) if self.frame.reproductor.estado() == "State.Playing" else self.frame.reproducirBTN.SetLabel(_("Pausar"))
			msg = _("Sin nada en reproducción") if self.frame.reproductor.estado() in ["State.NothingSpecial", "State.Stopped"] else _("Reproduciendo...") if self.frame.reproductor.estado() == "State.Playing" else _("Pausando...")
			info = ""
		elif id == 10006: # Adelantar
			self.frame.reproductor.adelantar(ajustes.dict_tiempo.get(ajustes.adelantar))
			msg = _("Sin nada en reproducción") if self.frame.reproductor.estado() in ["State.NothingSpecial", "State.Stopped"] else _("Adelantando {}").format(ajustes.listaAdelantar[ajustes.adelantar])
			info = ""
		elif id == 10007: # Detener
			msg = _("Deteniendo...") if self.frame.reproductor.estado() in ["State.Playing", "State.Paused"] else _("Sin nada en reproducción")
			info = ""
			self.frame.reproductor.stop()
			self.frame.reproducirBTN.SetLabel(_("Pausar")) if self.frame.reproductor.estado() == "State.Playing" else self.frame.reproducirBTN.SetLabel(_("Reproducir"))
			self.frame.estadoBotones(False)
			self.frame.onTabAcciones(self.frame.lst_book.GetSelection())
			self.frame.onFoco()
		elif id == 10008: # Información
			info = _("Sin nada en reproducción") if self.frame.reproductor.estado() in ["State.NothingSpecial", "State.Stopped"] else _("Tiempo transcurrido: {} / Tiempo total: {}").format(self.frame.reproductor.conviertetiempo(self.frame.reproductor.tiempotranscurrido()), self.frame.reproductor.conviertetiempo(self.frame.reproductor.tiempototal()))
			msg = _("Sin nada en reproducción") if self.frame.reproductor.estado() in ["State.NothingSpecial", "State.Stopped"] else _("Tiempo transcurrido: {} / Tiempo total: {}").format(self.frame.reproductor.conviertetiempo(self.frame.reproductor.tiempotranscurrido()), self.frame.reproductor.conviertetiempo(self.frame.reproductor.tiempototal()))
		elif id == 10009: # InformaciónValor (activa o desactiva mensajes)
			ajustes.IS_HABLAR = False if ajustes.IS_HABLAR else True
			msgAccion = _("Mensajes de información activados") if ajustes.IS_HABLAR else _("Mensajes de información desactivados")
			self.frame.frame.AjustesApp.GuardaDatos()
			self.frame.frame.AjustesApp.CargaDatos()
			self.frame.frame.AjustesApp.refrescaDatos()
			info = msgAccion
			msg = msgAccion
		utilidades.speak(0.1, msg) if ajustes.IS_HABLAR else utilidades.speak(0.1, info)

class HiloComplemento(Thread):
	""" Clase para lanzar el complemento desde un hilo separado del de NVDA y dependiendo de la opción realizara lo correspondiente """
	def __init__(self, frame, opcion):
		super(HiloComplemento, self).__init__()

		self.frame = frame
		self.opcion = opcion
		self.daemon = True

	def run(self):
		def lanzaApp():
			""" Función para lanzar la ventana principal si todo fue correcto """
			self._principal = VentanaPrincipal(gui.mainFrame, self.frame)
			gui.mainFrame.prePopup()
			self._principal.Show()

		def lanzaDescargaInicio():
			""" Función para comprobar si tenemos login y la base de datos, en caso negativo en cualquiera de las dos hara las acciones correspondientes """
			ajustes.IS_WinON = True
			self.BANDERA_PASA_MENSAJE = False
			self.BANDERA_CONTINUAR = False
			if ajustes.intentosBaneo >= 2: # Estamos baneados ya usamos todos los intentos
				if utilidades.check_time_passed(utilidades.convertir_obj_datatime(ajustes.fechaBaneo)): # Comprobamos si pasa 2 horas y levantamos baneo
					msg= \
_("""Han pasado más de 2 horas desde el baneo.

Por lo que el contador de intentos se pone a 0 teniendo 2 intentos.""")
					utilidades.mensaje(msg, _("Información"), 0)
					self.BANDERA_PASA_MENSAJE = True
					ajustes.IS_BANEO = False
					ajustes.intentosBaneo = 0
					ajustes.fechaIntento = None
					ajustes.fechaBaneo = None
					self.frame.AjustesApp.GuardaDatos()
					self.frame.AjustesApp.CargaDatos()
					self.frame.AjustesApp.refrescaDatos()
				else: # No a pasado 2 horas por lo que no le dejamos continuar
					msg= \
_("""No han pasado más de 2 horas desde el baneo.

El baneo se levantará en: {}.""").format(utilidades.tiempo_queda(utilidades.convertir_obj_datatime(ajustes.fechaBaneo)))
					utilidades.mensaje(msg, _("Información"), 0)
					ajustes.IS_WinON = False
					return
			else: # Quedan intentos
				if ajustes.intentosBaneo >= 1:
					msg = \
_("""Le quedan {} intentos.

Si no está seguro del usuario y contraseña, le aconsejo vaya a la web y solicite una nueva contraseña.

Le recuerdo que en la pantalla del inicio de sesión tiene un botón para ir directamente a la web de Audiocinemateca.""").format(2 - ajustes.intentosBaneo)
					utilidades.mensaje(msg, _("Información"), 0)
					self.BANDERA_PASA_MENSAJE = True

			if len(self.frame.AjustesApp.opciones[0][0]) == 0:
				msg = \
_("""Bienvenidos al complemento para NVDA de la Audiocinemateca.

A continuación, se abrirá una ventana de inicio de sesión para identificarse en la Audiocinemateca.

Es obligatorio tener una cuenta operativa en la pagina web.

Si ya dispone de usuario y contraseña en la siguiente ventana introdúzcalos.

Si no dispone de usuario y contraseña, en la siguiente pantalla tendrá un botón para abrir la web en su navegador y poder crear una cuenta.

Si no sabe como hacerlo le recomiendo visite en la web el enlace Guía para crear y gestionar tu cuenta de usuario.

Cuando pulse en la pantalla siguiente aceptar se validara su cuenta y si es exitoso la validación ya tendrá acceso al complemento.

En caso que intente acceder y su usuario o contraseña no sean correctas después de 2 intentos tendrá que esperar aproximadamente 2 horas para volver a intentarlo.

Si no desea continuar en la siguiente pantalla pulse cancelar para salir por completo del complemento.""")
				if not self.BANDERA_PASA_MENSAJE:
					self.BANDERA_PASA_MENSAJE = False
					utilidades.mensaje(msg, _("Información"), 0)
				dlg = dialogos.Login(self.frame, )
				result = dlg.ShowModal()
				if result == 0: # Intentamos login
					dlg.Destroy()
					temp_datos = "{}:{}".format(dlg.textoUsuario.GetValue(), dlg.contraseña)
					z = utilidades.IS_LOGIN(temp_datos)
					if z[0]: # Comprobamos si login correcto
						ajustes.IS_BANEO = False
						ajustes.intentosBaneo = 0
						ajustes.fechaIntento = None
						ajustes.fechaBaneo = None
						ajustes.usuario =dlg.textoUsuario.GetValue()
						ajustes.contraseña = dlg.contraseña
						self.frame.AjustesApp.GuardaDatos()
						self.frame.AjustesApp.CargaDatos()
						self.frame.AjustesApp.refrescaDatos()
						self.BANDERA_CONTINUAR = True
					else: # Login incorrecto en la comprobación
						ajustes.intentosBaneo += 1
						ajustes.fechaIntento = utilidades.convertir_obj_datatime(utilidades.guarda_tiempo(2))
						self.frame.AjustesApp.GuardaDatos()
						self.frame.AjustesApp.CargaDatos()
						self.frame.AjustesApp.refrescaDatos()
						if ajustes.intentosBaneo >= 2: # Baneo que te crio.
							ajustes.IS_BANEO = True
							ajustes.fechaBaneo = utilidades.convertir_obj_datatime(utilidades.guarda_tiempo(1))
							self.frame.AjustesApp.GuardaDatos()
							self.frame.AjustesApp.CargaDatos()
							self.frame.AjustesApp.refrescaDatos()
							msg = \
_("""Lo siento, el usuario o contraseña son incorrectos.

Ha usado los 2 intentos.

Tiene que pasar 2 horas para poder volver a intentarlo.

El servidor devolvió el siguiente error:

{}""").format(z[1])
							utilidades.mensaje(msg, _("Información"), 0)
							ajustes.IS_WinON = False
							return
						else: # Todavia quedan intentos
							msg = \
_("""*** Advertencia ***

Introdujo un usuario o contraseña incorrecto.

El servidor devolvió el siguiente error:

{}

Tiene 2 intentos para intentarlo antes de que su IP sea baneada por 2 horas.

Le quedan {} intentos.

¿Desea continuar?""").format(z[1], 2 - ajustes.intentosBaneo)
							xguiMsg = wx.MessageDialog(None, msg, "Pregunta", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
							ret = xguiMsg.ShowModal()
							if ret == wx.ID_YES: # Si quiere seguir intentando el login.
								xguiMsg.Destroy
								wx.CallAfter(lanzaDescargaInicio)
							else: # No quiere seguir intentando el login
								xguiMsg.Destroy
								ajustes.IS_WinON = False
								return
				else: # Cancelamos el login
					dlg.Destroy()
					ajustes.IS_WinON = False
					return
			else: # Si hay usuario y contraseña
				self.BANDERA_CONTINUAR = True

			if self.BANDERA_CONTINUAR:
				temp_datos = "{}:{}".format(self.frame.AjustesApp.opciones[0][0], self.frame.AjustesApp.opciones[0][1])
				z = utilidades.IS_LOGIN(temp_datos)
				if z[0]: # Comprobamos si login correcto
					if all(x is False for x in [self.frame.datos.existeDatos, self.frame.datos.existeVersion]): # Si no hay datos
						xguiMsg = \
"""No se encontró la base de datos.

El complemento necesita descargarse la base de datos para funcionar.

¿Desea descargar la ultima versión de la base de datos?"""
						msg = wx.MessageDialog(None, xguiMsg, "Pregunta", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
						ret = msg.ShowModal()
						if ret == wx.ID_YES:
							msg.Destroy
							dlg = dialogos.DownloadDialog(self.frame, 1)
							result = dlg.ShowModal()
							if result == 0:
								dlg.Destroy()
								ajustes.IS_WinON = False
								self.frame.datos.cargaDatos()
								self.frame.datos.cargaVersion()
								wx.CallAfter(lanzaApp)
							else:
								dlg.Destroy()
								ajustes.IS_WinON = False
								return
						else:
							msg.Destroy
							ajustes.IS_WinON = False
							return
					else: # Si hay datos
						ajustes.IS_WinON = False
						wx.CallAfter(lanzaApp)
				else: # Error al obtener login.
					msg = \
_("""Se a producido un error al iniciar sesión en Audiocinemateca:

El servidor a devuelto el siguiente error:

{}

Vuelva a intentarlo de nuevo. Si el problema persiste vuelva a valores por defecto el complemento en el menú Herramientas / Audiocinemateca.""").format(z[1])
					utilidades.mensaje(msg, _("Error"), 1)
					ajustes.IS_WinON = False
					return
		def lanzaOpciones():
			self.principalOpciones = VentanaOpciones(gui.mainFrame, self.frame)
			gui.mainFrame.prePopup()
			self.principalOpciones.Show()

		if self.opcion == 1:
			wx.CallAfter(lanzaDescargaInicio)
		elif self.opcion == 2:
			wx.CallAfter(lanzaOpciones)
