# -*- coding: utf-8 -*-
# Copyright (C) 2023 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.

import addonHandler
import ui
import wx
import threading
import os
dirAddon=os.path.dirname(__file__)
os.environ['PYTHON_VLC_MODULE_PATH']=os.path.abspath(os.path.dirname(__file__))
os.environ['PYTHON_VLC_LIB_PATH']=os.path.abspath(os.path.join(os.path.dirname(__file__), "libvlc.dll"))
curDir = os.getcwd()
os.chdir(dirAddon)
from . import vlc
os.chdir(curDir)

addonHandler.initTranslation()

def call_threaded(func, *args, **kwargs):
	#Call the given function in a daemonized thread and return the thread.
	def new_func(*a, **k):
		try:
			func(*a, **k)
		except:
			pass
	thread = threading.Thread(target=new_func, args=args, kwargs=kwargs)
	thread.daemon = True
	thread.start()
	return thread

class VlcClassLib():
	def __init__(self):

		self.frame = None
		self.frameMain = None
		self.Instance = vlc.Instance("--quiet") #"--quiet", "--file-logging", "--logfile=f:/vlc_log.txt") # Añadir log. 
		self.Instance.log_unset() # Evita mensajes de consola.
		self.handle = None
		self.fullscreen = False
		self.player = self.Instance.media_player_new()
		self.player.video_set_mouse_input(False)
		self.player.video_set_key_input(False)
		self.event_manager = self.player.event_manager()
		self.deviceSelection = 0
		self.devices = []
		self.devicesHummans = []
		self.playerDevices = self.Instance.media_player_new()
		self.GetDevices()

		self.EVENT_TYPE_MAP = {
			"MediaPlayerMediaChanged": vlc.EventType.MediaPlayerMediaChanged,
			"MediaPlayerNothingSpecial": vlc.EventType.MediaPlayerNothingSpecial,
			"MediaPlayerOpening": vlc.EventType.MediaPlayerOpening,
			"MediaPlayerBuffering": vlc.EventType.MediaPlayerBuffering,
			"MediaPlayerPlaying": vlc.EventType.MediaPlayerPlaying,
			"MediaPlayerPaused": vlc.EventType.MediaPlayerPaused,
			"MediaPlayerStopped": vlc.EventType.MediaPlayerStopped,
			"MediaPlayerForward": vlc.EventType.MediaPlayerForward,
			"MediaPlayerBackward": vlc.EventType.MediaPlayerBackward,
			"MediaPlayerEndReached": vlc.EventType.MediaPlayerEndReached,
			"MediaPlayerEncounteredError": vlc.EventType.MediaPlayerEncounteredError,
			"MediaPlayerTimeChanged": vlc.EventType.MediaPlayerTimeChanged,
			"MediaPlayerPositionChanged": vlc.EventType.MediaPlayerPositionChanged,
			"MediaPlayerSeekableChanged": vlc.EventType.MediaPlayerSeekableChanged,
			"MediaPlayerPausableChanged": vlc.EventType.MediaPlayerPausableChanged,
			"MediaPlayerTitleChanged": vlc.EventType.MediaPlayerTitleChanged,
			"MediaPlayerSnapshotTaken": vlc.EventType.MediaPlayerSnapshotTaken,
			"MediaPlayerLengthChanged": vlc.EventType.MediaPlayerLengthChanged,
			"MediaPlayerVout": vlc.EventType.MediaPlayerVout,
		}

		self.add_event_listener("MediaPlayerEndReached", self.handle_end_reached)
		self.add_event_listener("MediaPlayerEncounteredError", self.handle_error)

	def add_event_listener(self, event_type, callback):
		event = self.EVENT_TYPE_MAP.get(event_type)
		if event:
			self.event_manager.event_attach(event, callback)
		else:
			raise ValueError(_("Tipo de evento invalido: {event_type}"))

	def remove_event_listener(self, event_type, callback):
		event = self.EVENT_TYPE_MAP.get(event_type)
		if event:
			self.event_manager.event_detach(event, callback)
		else:
			raise ValueError(_("Tipo de evento invalido: {event_type}"))

	def addFrame(self, frame):
		self.frame = frame

	def addFrameMain(self, frame):
		self.frameMain = frame

	def SetHandle(self, event):
		self.handle = event
		self.player.set_hwnd(self.handle)

	def GetDevices(self):
		self.devices = []
		self.devicesHummans = []
		"""
		Hay que pausar el dispositivo para cambiar, la primera lista es la que hay que aplicar, la segunda es la que contiene el nombre de los dispositivos
podemos hacer: 
p = VlcClass.GetDevices()
VlcClass().SetDevice(p[0][0]) 
Es el dispositivo por defecto.
		"""
		mods = self.playerDevices.audio_output_device_enum()
		if mods:
			mod = mods
			while mod:
				mod = mod.contents
				self.devices.append(mod.device)
				if mod.description == b'Default':
					self.devicesHummans.append(_("Dispositivo salida de audio (por defecto)"))
				else:
					self.devicesHummans.append(mod.description)
				mod = mod.next       

	def SetDevice(self, valor):
		self.player.audio_output_device_set(None, valor)

	def file(self, valor):
		self.Media = self.Instance.media_new(valor)
		self.player.set_media(self.Media)

	def play(self):
		self.player.play()

	def pause(self):
		self.player.pause()

	def mute(self):
		muted = self.player.audio_get_mute()
		self.player.audio_set_mute(not muted)

	def stop(self):
		self.player.stop()

	def velocidad(self, valor):
		self.player.set_rate(valor)

	def volumen(self, valor):
		self.player.audio_set_volume(valor)

	def tiempotranscurrido(self):
		return self.player.get_time()

	def tiempototal(self):
		return self.player.get_length()

	def conviertetiempo(self, seconds):
		seconds = seconds / 1000 % (24 * 3600)
		hour = seconds // 3600
		seconds %= 3600
		minutes = seconds // 60
		seconds %= 60
		return "%d:%02d:%02d" % (hour, minutes, seconds)

	def atrasar(self, valor):
		valorAtrasar = valor * 1000
		self.player.set_time(self.tiempotranscurrido() - valorAtrasar)

	def adelantar(self, valor):
		valorAdelantar = valor * 1000
		self.player.set_time(self.tiempotranscurrido() + valorAdelantar)

	def estado(self):
		""" Los valores posibles a devolver son: VLC_STATE_PLAYING, VLC_STATE_PAUSED, VLC_STATE_STOPPED, VLC_STATE_ENDED, VLC_STATE_ERROR."""
		return str(self.player.get_state())

	def sonando(self):
		return self.player.is_playing()

	def handle_end_reached(self, event, *args, **kwargs):
		wx.CallAfter(self.stop)
		if self.frameMain:
			wx.CallAfter(self.frameMain.reproducirBTN.SetLabel, _("Pausar")) if self.estado() == "State.Playing" else wx.CallAfter(self.frameMain.reproducirBTN.SetLabel, _("Reproducir"))
			wx.CallAfter(self.frameMain.estadoBotones, False)
			wx.CallAfter(self.frameMain.onTabAcciones, self.frameMain.lst_book.GetSelection())
			wx.CallAfter(self.frameMain.onFoco)

	def handle_nothing_special(self, event):
		pass

	def handle_opening(self, event):
		pass

	def handle_buffering(self, event):
		pass

	def handle_playing(self, event):
		pass

	def handle_paused(self, event):
		pass

	def handle_stopped(self, event):
		pass

	def handle_forward(self, event):
		pass

	def handle_backward(self, event):
		pass

	def handle_error(self,event):
		msg = \
_("""Se a producido un error interno en el reproductor.

Error: {}

El complemento se cerrará.

Vuelva a abrirlo para reintentar la acción.

Si los problemas persisten póngase en contacto con el autor del complemento.""").format(event.type)
		dlg = wx.MessageDialog(None, msg, _("Error"), wx.OK | wx.ICON_ERROR)
		dlg.SetOKLabel(_("&Aceptar"))
		dlg.ShowModal()
		dlg.Destroy()
		if self.frameMain:
			self.frameMain.onSalir(None)
			wx.CallAfter(self.stop)

	def __del__(self):
		self.event_manager.event_detach(vlc.EventType.MediaPlayerEndReached)

