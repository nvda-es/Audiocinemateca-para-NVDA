# -*- coding: utf-8 -*-
# Copyright (C) 2023 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.

import addonHandler
import globalVars
import os
import sys
import json
import random
import string

addonHandler.initTranslation()

class Pelicula:
	"""
    Clase que representa una película.
    Atributos:
        - id (str): Identificador único de la película.
        - Titulo (str): Título de la película.
        - anio (str): Año de estreno de la película.
        - genero (str): Género de la película.
        - pais (str): País de producción de la película.
        - director (str): Nombre del director de la película.
        - guion (str): Nombre del guionista de la película.
        - musica (str): Nombre del compositor de la música de la película.
        - fotografia (str): Nombre del director de fotografía de la película.
        - reparto (str): Reparto de la película.
        - productora (str): Nombre de la productora de la película.
        - narracion (str): Nombre de la persona que narra la serie o compañia referido al Audesc.
        - duracion (str): Duración de la película en minutos.
        - idioma (str): Idioma original de la película 0 para Español y 1 para Español latinoamericano.
        - partes (str): Número de partes en las que se divide la película.
        - filmaffinity (str): La URL de FilmAffinity o pagina que tenga información sobre la pelicula.
        - sinopsis (str): Sinopsis de la película.
        - enlaces (list): Enlaces de la película.
	"""
	def __init__(self, id, Titulo, anio, genero, pais, director, guion, musica, fotografia, reparto, productora, narracion, duracion, idioma, partes, filmaffinity, sinopsis, enlaces):

		self.id = id
		self.titulo = Titulo
		self.anio = anio
		self.genero = genero
		self.pais = pais
		self.director = director
		self.guion = guion
		self.musica = musica
		self.fotografia = fotografia
		self.reparto = reparto
		self.productora = productora
		self.narracion = narracion
		self.duracion = duracion
		self.idioma = idioma
		self.partes = partes
		self.filmaffinity = filmaffinity
		self.sinopsis = sinopsis
		self.enlaces = enlaces

class Serie:
	"""
    Clase que representa a una serie de televisión.
    
    Atributos:
        - id (str): Identificador único de la serie.
        - titulo (str): Título de la serie.
        - anio (str): Año de estreno de la serie.
        - duracion (str): Duración de cada episodio de la serie en minutos.
        - pais (str): País de origen de la serie.
        - director (str): Nombre del director de la serie.
        - guion (str): Nombre de la persona o personas que escribieron el guion.
        - musica (str): Nombre de la persona o personas que compusieron la música.
        - fotografia (str): Nombre de la persona que fue el director de fotografía.
        - reparto (str): Nombre de los actores que participan en la serie.
        - genero (str): Género de la serie.
        - temporadas (str): Número de temporadas de la serie.
        - idioma (str): Idioma original de la serie 0 para Español y 1 para Español latinoamericano.
        - narracion (str): Nombre de la persona que narra la serie o compañia referido al Audesc.
        - filmaffinity (str): La URL de FilmAffinity o pagina que tenga información sobre la pelicula.
        - sinopsis (str): Resumen de la trama de la serie.
        - productora (str): Nombre de la productora de la serie.
        - capitulos (dict): Número de episodios de la serie, tiene las llaves capitulo, titulo y enlace.
	"""
	def __init__(self, id, titulo, anio, duracion, pais, director, guion, musica, fotografia, reparto, genero, temporadas, idioma, narracion, filmaffinity, sinopsis, productora, capitulos):

		self.id = id
		self.titulo = titulo
		self.anio = anio
		self.duracion = duracion
		self.pais = pais
		self.director = director
		self.guion = guion
		self.musica = musica
		self.fotografia = fotografia
		self.reparto = reparto
		self.genero = genero
		self.temporadas = temporadas
		self.idioma = idioma
		self.narracion = narracion
		self.filmaffinity = filmaffinity
		self.sinopsis = sinopsis
		self.productora = productora
		self.capitulos = capitulos

class Documental:
	"""
    Clase que representa a un documental.
    
    Atributos:
        - id (str): Identificador único del documental.
        - titulo (str): Título del documental.
        - anio (str): Año de estreno del documental.
        - genero (str): Género del documental.
        - pais (str): País de origen del documental.
        - director (str): Nombre del director del documental.
        - guion (str): Nombre de la persona o personas que escribieron el guion.
        - musica (str): Nombre de la persona o personas que compusieron la música.
        - fotografia (str): Nombre de la persona que fue el director de fotografía.
        - reparto (str): Nombre de las personas que participan en el documental.
        - productora (str): Nombre de la productora del documental.
        - narracion (str): Nombre de la persona que narra la serie o compañia referido al Audesc.
        - duracion (str): Duración del documental en minutos.
        - idioma (str): Idioma original de la serie 0 para Español y 1 para Español latinoamericano.
        - filmaffinity (str): La URL de FilmAffinity o pagina que tenga información sobre la pelicula.
        - sinopsis (str): Resumen de la trama del documental.
        - enlace  (str): Enlace del documental online.
	"""
	def __init__(self, id, titulo, anio, genero, pais, director, guion, musica, fotografia, reparto, productora, narracion, duracion, idioma, filmaffinity, sinopsis, enlace):

		self.id = id
		self.titulo = titulo
		self.anio = anio
		self.genero = genero
		self.pais = pais
		self.director = director
		self.guion = guion
		self.musica = musica
		self.fotografia = fotografia
		self.reparto = reparto
		self.productora = productora
		self.narracion = narracion
		self.duracion = duracion
		self.idioma = idioma
		self.filmaffinity = filmaffinity
		self.sinopsis = sinopsis
		self.enlace = enlace

class Cortometraje:
	"""
    Clase que representa a un cortometraje.
    
    Atributos:
        - id (str): Identificador único del cortometraje.
        - titulo (str): Título del cortometraje.
        - anio (str): Año de estreno del cortometraje.
        - genero (str): Género del cortometraje.
        - pais (str): País de origen del cortometraje.
        - director (str): Nombre del director del cortometraje.
        - guion (str): Nombre de la persona o personas que escribieron el guion.
        - musica (str): Nombre de la persona o personas que compusieron la música.
        - fotografia (str): Nombre de la persona que fue el director de fotografía.
        - reparto (str): Nombre de las personas que participan en el cortometraje.
        - productora (str): Nombre de la productora del cortometraje.
        - narracion (str): Nombre de la persona que narra la serie o compañia referido al Audesc.
        - duracion (str): Duración del cortometraje en minutos.
        - idioma (str): Idioma original de la serie 0 para Español y 1 para Español latinoamericano.
        - filmaffinity (str): La URL de FilmAffinity o pagina que tenga información sobre la pelicula.
        - sinopsis (str): Resumen de la trama del cortometraje.
        - enlace (str): Enlace a donde se puede ver el cortometraje online.
	"""
	def __init__(self, id, titulo, anio, genero, pais, director, guion, musica, fotografia, reparto, productora, narracion, duracion, idioma, filmaffinity, sinopsis, enlace):

		self.id = id
		self.titulo = titulo
		self.anio = anio
		self.genero = genero
		self.pais = pais
		self.director = director
		self.guion = guion
		self.musica = musica
		self.fotografia = fotografia
		self.reparto = reparto
		self.productora = productora
		self.narracion = narracion
		self.duracion = duracion
		self.idioma = idioma
		self.filmaffinity = filmaffinity
		self.sinopsis = sinopsis
		self.enlace = enlace

class Episodio:
	"""
    Clase que representa un episodio de una serie.

    Atributos:
        - temporada (str): Número de temporada del episodio.
        - capitulo (str): Número de episodio dentro de la temporada.
        - titulo (str): Título del episodio.
        - enlace (str): URL del episodio.
	"""
	def __init__(self, temporada, capitulo, titulo, enlace):

		self.temporada = temporada
		self.capitulo = capitulo
		self.titulo = titulo
		self.enlace = enlace

class ColeccionPeliculas:
	"""
    Clase que representa una colección de películas.

    Atributos:
        - datos (list): Lista de diccionarios, cada uno representando una película con sus atributos.
        - reversed_datos (list): Lista de diccionarios, con los datos de las películas en orden inverso al de 'datos'.
        - peliculas (list): Lista de objetos Pelicula creados a partir de los diccionarios en 'datos'.

    Métodos:
        - leer_datos(): Crea objetos Pelicula a partir de los diccionarios en 'datos' y los guarda en 'peliculas'.
        - get_original_orden(indice): Devuelve el diccionario de la película en 'datos' que corresponde al índice 'indice' en 'reversed_datos'.
        - buscar(valor): Devuelve una lista de diccionarios de películas cuyo título contiene 'valor'. Si no hay resultados, devuelve None.
	"""
	def __init__(self, datos):

		self.datos = datos['peliculas']
		self.reversed_datos = list(reversed(self.datos))
		self.peliculas = []
		self.leer_datos()

	def leer_datos(self):
		for pelicula in self.reversed_datos:
			self.peliculas.append(Pelicula(**pelicula))

	def get_original_orden(self, indice):
		original_indice = len(self.reversed_datos) - indice - 1
		return self.datos[original_indice]

	def buscar(self, valor, categoria):
		results = []
		for pelicula in self.reversed_datos:
			texto = pelicula[categoria].lower()
			# Eliminamos cualquier signo de puntuacion
			for s in string.punctuation:
				texto = texto.replace(s,"")
				valor = valor.replace(s, "")
			# Eliminamos los signos diacríticos 
			for s in (("á", "a"), ("é", "e"), ("í","i"), ("ó","o"), ("ú","u"), ("ü","u")):
				texto = texto.replace(s[0],s[1])
				valor = valor.replace(s[0],s[1])
			# Convertimos las cadenas de texto en conjuntos de palabras
			palabras_texto = set(texto.split())
			palabras_buscadas = set(valor.split())
			# Eliminamos de la busqueda los articulos y otras palabras superfluas. Solo español.
			palabras_buscadas = palabras_buscadas-set(["a", "y", "el", "la", "los", "las", "en", "un", "una", "unos", "de", "del"])
			if palabras_buscadas and palabras_buscadas.issubset(palabras_texto): # Si todas las palabras buscadas están en texto
				results.append(pelicula)
			elif palabras_buscadas.intersection(palabras_texto) and len(palabras_buscadas.difference(palabras_texto)) == 1:
				if palabras_buscadas.difference(palabras_texto).pop() in texto:
					# Si están todas las palabras menos una y la que falta es parte del texto aunque no sea una palabra completa, la incluimos también.
					results.append(pelicula)
			elif valor in texto: # Si la búsqueda por palabras no da resultado probamos una búsqueda de texto completo.
				results.append(pelicula)
		return results if len(results) >= 1 else None

class ColeccionSeries:
	"""
    La clase `ColeccionSeries` representa una colección de series de televisión.

    Atributos:
        - datos (dict): Un diccionario con información sobre las series.
        - reversed_datos (list): Una lista con los datos de las series en orden inverso.
        - series (list): Una lista de objetos `Serie` creados a partir de los datos de las series.

    Métodos:
        - leer_datos(self): Crea una lista de objetos `Serie` a partir de los datos de las series.
        - get_original_orden(self, indice): Devuelve la serie en el índice original del diccionario de datos.
        - buscar(self, valor): Busca series en la colección que tengan el valor dado en el título y devuelve una lista con ellas. Si no se encuentran resultados, devuelve None.
	"""
	def __init__(self, datos):

		self.datos = datos['series']
		self.reversed_datos = list(reversed(self.datos))
		self.series = []
		self.leer_datos()

	def leer_datos(self):
		for serie in self.reversed_datos:
			self.series.append(Serie(**serie))

	def get_original_orden(self, indice):
		original_indice = len(self.reversed_datos) - indice - 1
		return self.datos[original_indice]

	def buscar(self, valor, categoria):
		results = []
		for serie in self.reversed_datos:
			texto = serie[categoria].lower()
			# Eliminamos cualquier signo de puntuacion
			for s in string.punctuation:
				texto = texto.replace(s,"")
				valor = valor.replace(s, "")
			# Eliminamos los signos diacríticos 
			for s in (("á", "a"), ("é", "e"), ("í","i"), ("ó","o"), ("ú","u"), ("ü","u")):
				texto = texto.replace(s[0],s[1])
				valor = valor.replace(s[0],s[1])
			# Convertimos las cadenas de texto en conjuntos de palabras
			palabras_texto = set(texto.split())
			palabras_buscadas = set(valor.split())
			# Eliminamos de la busqueda los articulos y otras palabras superfluas. Solo español.
			palabras_buscadas = palabras_buscadas-set(["a", "y", "el", "la", "los", "las", "en", "un", "una", "unos", "de", "del"])
			if palabras_buscadas and palabras_buscadas.issubset(palabras_texto): # Si todas las palabras buscadas están en texto
				results.append(serie)
			elif palabras_buscadas.intersection(palabras_texto) and len(palabras_buscadas.difference(palabras_texto)) == 1:
				if palabras_buscadas.difference(palabras_texto).pop() in texto:
					# Si están todas las palabras menos una y la que falta es parte del texto aunque no sea una palabra completa, la incluimos también.
					results.append(serie)
			elif valor in texto: # Si la búsqueda por palabras no da resultado probamos una búsqueda de texto completo.
				results.append(serie)
		return results if len(results) >= 1 else None

class ColeccionDocumentales:
	"""
    La clase `ColeccionDocumentales` representa una colección de documentales.

    Atributos:
        - datos (dict): Un diccionario con información sobre los documentales.
        - reversed_datos (list): Una lista con los datos de los documentales en orden inverso.
        - documentales (list): Una lista de objetos `Documental` creados a partir de los datos de los documentales.

     Métodos:
        - leer_datos(self): Crea una lista de objetos `Documental` a partir de los datos de los documentales.
        - get_original_orden(self, indice): Devuelve el documental en el índice original del diccionario de datos.
        - buscar(self, valor): Busca documentales en la colección que tengan el valor dado en el título y devuelve una lista con ellos. Si no se encuentran resultados, devuelve None.
	"""
	def __init__(self, datos):

		self.datos = datos['documentales']
		self.reversed_datos = list(reversed(self.datos))
		self.documentales = []
		self.leer_datos()

	def leer_datos(self):
		for documental in self.reversed_datos:
			self.documentales.append(Documental(**documental))

	def get_original_orden(self, indice):
		original_indice = len(self.reversed_datos) - indice - 1
		return self.datos[original_indice]

	def buscar(self, valor, categoria):
		results = []
		for documental in self.reversed_datos:
			texto = documental[categoria].lower()
			# Eliminamos cualquier signo de puntuacion
			for s in string.punctuation:
				texto = texto.replace(s,"")
				valor = valor.replace(s, "")
			# Eliminamos los signos diacríticos 
			for s in (("á", "a"), ("é", "e"), ("í","i"), ("ó","o"), ("ú","u"), ("ü","u")):
				texto = texto.replace(s[0],s[1])
				valor = valor.replace(s[0],s[1])
			# Convertimos las cadenas de texto en conjuntos de palabras
			palabras_texto = set(texto.split())
			palabras_buscadas = set(valor.split())
			# Eliminamos de la busqueda los articulos y otras palabras superfluas. Solo español.
			palabras_buscadas = palabras_buscadas-set(["a", "y", "el", "la", "los", "las", "en", "un", "una", "unos", "de", "del"])
			if palabras_buscadas and palabras_buscadas.issubset(palabras_texto): # Si todas las palabras buscadas están en texto
				results.append(documental)
			elif palabras_buscadas.intersection(palabras_texto) and len(palabras_buscadas.difference(palabras_texto)) == 1:
				if palabras_buscadas.difference(palabras_texto).pop() in texto:
					# Si están todas las palabras menos una y la que falta es parte del texto aunque no sea una palabra completa, la incluimos también.
					results.append(documental)
			elif valor in texto: # Si la búsqueda por palabras no da resultado probamos una búsqueda de texto completo.
				results.append(documental)
		return results if len(results) >= 1 else None

class ColeccionCortometrajes:
	"""
    La clase `ColeccionCortometrajes` representa una colección de cortometrajes.

    Atributos:
        - datos (dict): Un diccionario con información sobre los cortometrajes.
        - reversed_datos (list): Una lista con los datos de los cortometrajes en orden inverso.
        - cortometrajes (list): Una lista de objetos `Cortometraje` creados a partir de los datos de los cortometrajes.

    Métodos:
        - leer_datos(self): Crea una lista de objetos `Cortometraje` a partir de los datos de los cortometrajes.
        - get_original_orden(self, indice): Devuelve el cortometraje en el índice original del diccionario de datos.
        - buscar(self, valor): Busca cortometrajes en la colección que tengan el valor dado en el título y devuelve una lista con ellos. Si no se encuentran resultados, devuelve None.
	"""
	def __init__(self, datos):

		self.datos = datos['cortometrajes']
		self.reversed_datos = list(reversed(self.datos))
		self.cortometrajes = []
		self.leer_datos()

	def leer_datos(self):
		for cortometraje in self.reversed_datos:
			self.cortometrajes.append(Cortometraje(**cortometraje))

	def get_original_orden(self, indice):
		original_indice = len(self.reversed_datos) - indice - 1
		return self.datos[original_indice]

	def buscar(self, valor, categoria):
		results = []
		for cortometraje in self.reversed_datos:
			texto = cortometraje[categoria].lower()
			# Eliminamos cualquier signo de puntuacion
			for s in string.punctuation:
				texto = texto.replace(s,"")
				valor = valor.replace(s, "")
			# Eliminamos los signos diacríticos 
			for s in (("á", "a"), ("é", "e"), ("í","i"), ("ó","o"), ("ú","u"), ("ü","u")):
				texto = texto.replace(s[0],s[1])
				valor = valor.replace(s[0],s[1])
			# Convertimos las cadenas de texto en conjuntos de palabras
			palabras_texto = set(texto.split())
			palabras_buscadas = set(valor.split())
			# Eliminamos de la busqueda los articulos y otras palabras superfluas. Solo español.
			palabras_buscadas = palabras_buscadas-set(["a", "y", "el", "la", "los", "las", "en", "un", "una", "unos", "de", "del"])
			if palabras_buscadas and palabras_buscadas.issubset(palabras_texto): # Si todas las palabras buscadas están en texto
				results.append(cortometraje)
			elif palabras_buscadas.intersection(palabras_texto) and len(palabras_buscadas.difference(palabras_texto)) == 1:
				if palabras_buscadas.difference(palabras_texto).pop() in texto:
					# Si están todas las palabras menos una y la que falta es parte del texto aunque no sea una palabra completa, la incluimos también.
					results.append(cortometraje)
			elif valor in texto: # Si la búsqueda por palabras no da resultado probamos una búsqueda de texto completo.
				results.append(cortometraje)
		return results if len(results) >= 1 else None

class ColeccionEpisodios:
	"""
    La clase `ColeccionEpisodios` representa una colección de episodios de una serie de televisión.

    Atributos:
        - datos (dict): Un diccionario con información sobre los episodios de la serie.
        - episodios (list): Una lista de objetos `Episodio` creados a partir de los datos de los episodios.

    Métodos:
        - leer_datos(self): Crea una lista de objetos `Episodio` a partir de los datos de los episodios.
        - obtener_episodios_por_temporada(self, temporada:str): Devuelve una lista de objetos `Episodio` de la temporada dada.
	"""
	def __init__(self, datos):

		self.datos = datos
		self.episodios = []
		self.leer_datos()

	def leer_datos(self):
		for temporada, episodios in self.datos.items():
			for episodio in episodios:
				p = Episodio(temporada, episodio['capitulo'], episodio['titulo'], episodio['enlace'])
				self.episodios.append(p)

	def obtener_episodios_por_temporada(self, temporada:str):
		resultados = []
		for t, episodios in self.datos.items():
			if t == temporada:
				for episodio in episodios:
					p = Episodio(t, episodio['capitulo'], episodio['titulo'], episodio['enlace'])
					resultados.append(p)
		return resultados

class RandomTitleGenerator:
	"""
    Inicializa el generador con las listas de títulos de las diferentes categorías.
        
    Args:
        - peliculas (list): Lista con los títulos de las películas.
        - series (list): Lista con los títulos de las series.
        - documentales (list): Lista con los títulos de los documentales.
        - cortometrajes (list): Lista con los títulos de los cortometrajes.
	"""
	def __init__(self, peliculas, series, documentales, cortometrajes):

				self.categories = {
			'peliculas': peliculas,
			'series': series,
			'documentales': documentales,
			'cortometrajes': cortometrajes
		}
    
	def get_random_title(self):
		category = random.choice(list(self.categories.keys()))
		titles = self.categories[category]
		title = random.choice(titles)
		index = titles.index(title)
		return [category, index, title]

class Inicio_DB:
	def __init__(self, frame):

		self.frame = frame
		self.existeDatos = False
		self.existeVersion = False

		self.datos_fichero = os.path.join(globalVars.appArgs.configPath, "Audiocinemateca", "catalogo.json")
		self.version_fichero = os.path.join(globalVars.appArgs.configPath, "Audiocinemateca", "version.json")

		self.resultados_datos = []
		self.resultados_version = []

	def clear(self):
		self.resultados_datos = []
		self.resultados_version = []

	def cargaDatos(self):
		if os.path.isfile(self.datos_fichero):
			with open(self.datos_fichero) as f:
				self.resultados_datos = json.load(f)
			self.existeDatos = True
		else:
			self.existeDatos = False

	def cargaVersion(self):
		if os.path.isfile(self.version_fichero):
			with open(self.version_fichero) as f:
				self.resultados_version = json.load(f)
			self.existeVersion = True
			self.frame.AjustesApp.opciones[-1] = [self.resultados_version]
			self.frame.AjustesApp.refrescaDatos()
			self.frame.AjustesApp.GuardaDatos()
			self.frame.AjustesApp.CargaDatos()
			self.frame.AjustesApp.refrescaDatos()
		else:
			self.existeVersion = False

	def GetDatos(self, valor):
		if valor == 0: # Devuelve peliculas
			return ColeccionPeliculas(self.resultados_datos)
		elif valor == 1: # Devuelve series
			return ColeccionSeries(self.resultados_datos)
		elif valor == 2: # Devuelve documentales
			return ColeccionDocumentales(self.resultados_datos)
		elif valor == 3: # Devuelve cortometrajes
			return ColeccionCortometrajes(self.resultados_datos)

	def GetDatosSerie(self, valor):
		return ColeccionEpisodios(valor)

	def GetAleatoria(self, Peliculas, Series, Documentales, Cortometrajes):
		return RandomTitleGenerator([Peliculas.peliculas[i].titulo for i in range(len(Peliculas.peliculas))], [Series.series[i].titulo for i in range(len(Series.series))], [Documentales.documentales[i].titulo for i in range(len(Documentales.documentales))], [Cortometrajes.cortometrajes[i].titulo for i in range(len(Cortometrajes.cortometrajes))]).get_random_title()
