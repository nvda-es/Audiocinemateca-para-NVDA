# -*- coding: utf-8 -*-
# Copyright (C) 2023 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.

import addonHandler
import ui
import speech
from time import sleep
from threading import Thread
from urllib.error import HTTPError, URLError
from datetime import datetime, timedelta
import wx
import socket
import textwrap
import urllib.request
import urllib.parse
import gzip
import bz2
import base64
import os
import sys

addonHandler.initTranslation()

def get_filename_from_url(url:str)->str:
	"""
    Esta función toma una URL como argumento y devuelve el nombre del archivo MP3. Se sustituye los %20 por espacios.
    
    Parameters:
        - url (str): La url del archivo mp3.
    
    Returns:
        - str: El nombre del archivo mp3 con espacios en lugar de %20.
    
    Ejemplo:
        get_filename_from_url("http://www.example.com/songs/song%20title.mp3")
        > "song title.mp3"
	"""
	parsed_url = urllib.parse.urlparse(url)
	filename = parsed_url.path.split("/")[-1]
	return urllib.parse.unquote(filename)

def partir_texto(texto:str, longitud:int)->str:
	"""
    La función recibe una cadena 'texto' y un entero 'longitud', y devuelve la cadena 'texto' con saltos de línea cada 'longitud' caracteres.
	"""
	return "\n".join(textwrap.wrap(texto, longitud))

def es_url(cadena:str)->bool:
	"""
    La función recibe una cadena y verifica si es una url valida.
    Retorna True si es una url valida, False en caso contrario
	"""
	try:
		result = urllib.parse.urlparse(cadena)
		return all([result.scheme, result.netloc])
	except ValueError:
		return False

def IS_INTERNET(host="8.8.8.8", port=53, timeout=3):
	"""
    Comprueba si hay conexión a Internet intentando conectarse a un host y puerto específicos.

    Args:
        - host (str): El host al que se intentará conectar. El valor predeterminado es "8.8.8.8", que es uno de los servidores DNS públicos de Google.
        - port (int): El puerto al que se intentará conectar. El valor predeterminado es 53, que es el puerto utilizado por el protocolo DNS.
        - timeout (int): El tiempo máximo en segundos que se esperará antes de considerar que la conexión ha fallado. El valor predeterminado es 3.

    Returns:
        - bool: True si se ha podido conectar al host y puerto especificados, False en caso contrario.
	"""
	try:
		socket.setdefaulttimeout(timeout)
		socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
		return True
	except socket.error as ex:
		return False

def mensaje(mensaje, titulo, valor):
	"""
    Muestra un cuadro de diálogo con un mensaje y título especificados.

    Args:
        - mensaje (str): El mensaje que se mostrará en el cuadro de diálogo.
        - titulo (str): El título que se mostrará en el cuadro de diálogo.
        - valor (int): El tipo de cuadro de diálogo a mostrar. 0 muestra un cuadro de diálogo de información, 1 muestra un cuadro de diálogo de error.

    Returns:
        - None
	"""
	parametro = wx.OK | wx.ICON_INFORMATION if valor == 0 else wx.OK | wx.ICON_ERROR
	dlg = wx.MessageDialog(None, mensaje, titulo, parametro)
	dlg.SetOKLabel(_("&Aceptar"))
	dlg.ShowModal()
	dlg.Destroy()

def IS_LOGIN(credenciales):
	"""
    Verifica si un usuario tiene autorización para descargar un recurso específico de una URL específica.

    Argumentos:
        - credenciales (str): Las credenciales de autorización del usuario que se utilizarán para enviar una solicitud de autorización. "usuario:contraseña"

    Excepciones:
        - HTTPError, URLError, Exception: en caso de cualquier excepción, la función devuelve False.

    Resultado:
        - bool: True si el usuario tiene autorización para descargar el recurso, False de lo contrario.
	"""
	req = urllib.request.Request("https://audiocinemateca.com/system/files/catalogo/version.json.gz")
	req.add_header('Authorization', 'Basic ' + base64.b64encode(credenciales.encode()).decode())
	try:
		with urllib.request.urlopen(req) as res:
			return [True, None] if res.status == 200 else [False, _("Codigo de estado: {}").format(res.status)]
	except (HTTPError, URLError, Exception) as e:
		return [False, e]

def descargador(frame, user_name, user_pwd, url, file_path, option):
	"""
    La función `descargador` descarga un archivo desde una URL protegida por autenticación básica.

    Parámetros:
        - frame`: marco donde se visualizará el progreso de la descarga (opcional).
        - user_name`: nombre de usuario para la autenticación.
        - user_pwd`: contraseña para la autenticación.
        - url`: URL del archivo a descargar.
        - file_path`: ruta donde se guardará el archivo descargado.
        - option: 1 para catalogo y version 2 para ficheros.

    Excepciones:
        - HTTPError`: si ocurre un error HTTP durante la descarga.
        - URLError`: si ocurre un error de URL durante la descarga.
	"""
	try:
		if option == 1:
			file_name = url.rsplit('/', 1)[-1]
		else:
			file_name = get_filename_from_url(url)

		# Creamos una instancia de la clase Request
		request = urllib.request.Request(url)
		# Añadimos el encabezado 'Authorization' a la petición
		request.add_header('Authorization', 'Basic ' + base64.b64encode(f"{user_name}:{user_pwd}".encode()).decode())
		# Enviamos la petición
		response = urllib.request.urlopen(request)
		# Obtenemos el tamaño total del archivo
		total_size = int(response.headers.get('Content-Length'))
		# Inicializamos la variable que almacena el tamaño descargado
		downloaded_size = 0
		with open(file_path + "/" + file_name, 'wb') as f:
			# Leemos 8192 bytes del contenido de la respuesta
			chunk = response.read(8192)
			while chunk:
				# Escribimos el chunk en el archivo
				f.write(chunk)
				# Sumamos el tamaño del chunk descargado a la variable downloaded_size
				downloaded_size += len(chunk)
				# Calculamos el porcentaje de descarga
				progress = (downloaded_size / total_size) * 100
				wx.CallAfter(frame.update_progress, progress) #frame.next, int(progress))
#				sleep(1 / 995)
				# Leemos otro chunk
				chunk = response.read(8192)
		# Cerramos la respuesta
		response.close()
		# Comprobamos si la descarga se completó correctamente
		if response.status in [200, 206]:
			return [True, None]
		else:
			return [False, None]
	except (HTTPError, URLError, Exception) as e:
		return [False, e]

def compare_dict_times(local_dict, server_dict):
	"""
    Compara dos diccionarios que contienen información de fecha y hora y determina cuál es más reciente.

    Args:
        - local_dict (dict): El primer diccionario a comparar. Debe tener la misma estructura que el diccionario servidor.
        - server_dict (dict): El segundo diccionario a comparar. Debe tener la misma estructura que el diccionario local.

    Returns:

        - bool: True si el diccionario local es más antiguo que el diccionario servidor, False en caso contrario.
	"""
	# Convierte cada diccionario en un objeto datetime
	local_time = datetime(local_dict["year"], local_dict["mon"], local_dict["mday"], local_dict["hours"], local_dict["minutes"], local_dict["seconds"])
	server_time = datetime(server_dict["year"], server_dict["mon"], server_dict["mday"], server_dict["hours"], server_dict["minutes"], server_dict["seconds"])
	# Compara los objetos datetime para ver cuál es más reciente
	return True if local_time < server_time else False

def convertir_obj_datatime(valor, formato=None):
	"""
    Convierte un objeto datetime a str y viceversa.
    
    Parámetros:
        - valor (datetime o str): el valor a convertir.
        - formato (str, opcional): el formato en el que se desea la salida str.
              Si no se especifica, se usa el formato ISO.
    
    Resultado:
        - datetime o str: dependiendo del tipo de valor de entrada.
    
    Raises:
        - TypeError: si el valor de entrada no es datetime o str.
	"""
	if isinstance(valor, datetime):
		return valor.strftime(formato) if formato else valor.isoformat()
	elif isinstance(valor, str):
		return datetime.strptime(valor, formato) if formato else datetime.fromisoformat(valor)
	else:
		raise TypeError(_("Debe ser datetime o str"))

def guarda_tiempo(opcion):
	"""
    Esta función guarda en una variable la hora actual y fecha añadiendo a la hora actual 2 horas más en la opción 1 y 10 minutos en la opción 2.
	"""
	current_time = datetime.now()
	if opcion == 1:
		future_time = current_time + timedelta(hours=2)
	else:
		future_time = current_time + timedelta(minutes=10)
	return future_time

def check_time_passed(future_time):
	"""
    Esta función comprueba si a pasado el tiempo necesario devolviendo true o false.
	"""
	current_time = datetime.now()
	time_difference = future_time - current_time
	return False if time_difference.total_seconds() > 0 else True

def tiempo_queda(future_time):
	"""
    Esta función tiene que devolverme el tiempo que queda de la hora actual a la hora lo que pasemos.
	"""
	current_time = datetime.now()
	time_difference = future_time - current_time
	if time_difference.days < 0:
		return None
	else:
		hours, remainder = divmod(time_difference.seconds, 3600)
		minutes, seconds = divmod(remainder, 60)
		return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)

def decompress_gz(frame, file_path, output_path):
	"""
La función `decompress_gz(file_path, output_path)` descomprime un archivo comprimido en formato gzip, dado su ruta `file_path`, y escribe el contenido descomprimido en un archivo en la ruta especificada por `output_path`. La función también imprime el porcentaje de progreso de la descompresión.
	"""
	try:
		# Abrimos el archivo gz y obtenemos su tamaño total
		with gzip.open(file_path, 'rb') as f:
			total_size = f.seek(0, 2)
			# Volvemos al inicio del archivo
			f.seek(0, 0)
			# Inicializamos la variable que almacena el tamaño descomprimido
			decompressed_size = 0
			# Creamos un archivo de salida
			with open(output_path, 'wb') as out:
				# Leemos el archivo por bloques y escribimos el contenido en el archivo de salida
				while True:
					chunk = f.read(8192)
					if not chunk:
						break
					out.write(chunk)
					# Sumamos el tamaño del bloque descomprimido a la variable decompressed_size
					decompressed_size += len(chunk)
					# Calculamos el porcentaje de progreso
					progress = (decompressed_size / total_size) * 100
					wx.CallAfter(frame.update_progress, progress)
		return [True, None]
	except Exception as e:
		return [False, e]

def decompress_bz2(frame, file_path, output_path):
	"""
La función `decompress_bz2(file_path, output_path)` descomprime un archivo comprimido en formato bz2, dado su ruta `file_path`, y escribe el contenido descomprimido en un archivo en la ruta especificada por `output_path`. La función también imprime el porcentaje de progreso de la descompresión.
	"""
	try:
		# Abrimos el archivo bz2 y obtenemos su tamaño total
		with bz2.open(file_path, 'rb') as f:
			total_size = f.seek(0, 2)
			# Volvemos al inicio del archivo
			f.seek(0, 0)
			# Inicializamos la variable que almacena el tamaño descomprimido
			decompressed_size = 0
			# Creamos un archivo de salida
			with open(output_path, 'wb') as out:
				# Leemos el archivo por bloques y escribimos el contenido en el archivo de salida
				while True:
					chunk = f.read(8192)
					if not chunk:
						break
					out.write(chunk)
					# Sumamos el tamaño del bloque descomprimido a la variable decompressed_size
					decompressed_size += len(chunk)
					# Calculamos el porcentaje de progreso
					progress = (decompressed_size / total_size) * 100
					wx.CallAfter(frame.update_progress, progress)
		return [True, None]
	except Exception as e:
		return [False, e]

def isRango(cadena: str, min_value: int = None, max_value: int = None) -> bool:
	"""
    Comprueba si un string es un número entero dentro de un rango especifico.
        :param cadena: El string a comprobar si es un número entero.
        :param min_value: El valor minimo permitido (opcional).
        :param max_value: El valor maximo permitido (opcional).
        :return: True si es un número entero dentro del rango especificado, False en caso contrario.
	"""
	try:
		num = int(cadena)
	except ValueError:
		return False
	if min_value is not None and num < min_value: return False
	if max_value is not None and num > max_value: return False
	return True

# Inicio Funciones obtenidas del complemento UNIGRAM de Gerardo Kessler
def speak(time, msg= False):
	if speech.getState().speechMode == speech.SpeechMode.off: return
	if msg:
		ui.message(msg)
		sleep(0.1)
	Thread(target=killSpeak, args=(time,), daemon= True).start()

def killSpeak(time):
	speech.setSpeechMode(speech.SpeechMode.off)
	sleep(time)
	speech.setSpeechMode(speech.SpeechMode.talk)
# Fin Funciones obtenidas del complemento UNIGRAM de Gerardo Kessler
