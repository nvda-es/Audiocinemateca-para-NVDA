# Manual de la Audiocinemateca para NVDA

Este complemento nos ofrece la posibilidad de tener la página de la Audiocinemateca en nuestro NVDA.

La audiocinemateca es un sitio web, creado en el año 2015, que mantiene y actualiza una colección de películas, series, documentales y cortometrajes en formato sólo audio con audiodescripción para personas ciegas, totalmente gratis y en español.

Si quieres conocerla antes de profundizar en este complemento, [visita la audiocinemateca pinchando en este enlace](https://audiocinemateca.com).

Este complemento permite acceder al contenido de la web desde una interfaz nativa de Windows, sencilla, con atajos de teclado y sin necesidad de abrir un programa adicional, con todas sus funciones integradas en NVDA.

## Qué ofrece el complemento

 El complemento te dejará consultar, reproducir, descargar cualquier película, serie, documental o cortometraje que se encuentre en la Audiocinemateca.

* Podremos consultar la ficha con los mismos datos que en la página web.
* Podremos reproducir en un sencillo reproductor las películas, series (eligiendo temporada y episodio), documental o cortometraje.
* También podremos descargar cualquier película, serie (eligiendo temporada y episodio), documental y cortometraje.

En el caso de las películas puede haber alguna que contenga más de una parte, por lo que nos dejará elegir qué parte de la película deseamos reproducir o descargar.

En las series,  tendremos que elegir la temporada que deseamos (en caso de haber más de una) y el episodio tanto en la reproducción como en la descarga.

El complemento podrá ser manejado a través de una interfaz que permite realizar tanto consultas como reproducción y descarga.

Además, cuando estemos reproduciendo algo, podremos manejar todo el aspecto de la reproducción desde cualquier parte de Windows.

El complemento puede ser lanzado desde el menú Herramientas / Audiocinemateca, o asignando las correspondientes teclas en Gestos de entrada / Audiocinemateca.

El complemento viene sin teclas asignadas, por lo que tendremos que asignárselas.

El complemento requiere que tengamos un usuario y contraseña válidos de la Audiocinemateca.

El complemento viene sin la base de datos, por lo que la primera vez que ejecutemos el complemento nos pedirá que descarguemos la base de datos.

La primera vez que ejecutemos el complemento, se nos pedirá que metamos nuestro usuario y contraseña de la Audiocinemateca. En la pantalla de iniciar sesión podremos también ir a la página web para registrarnos o solicitar una nueva contraseña, en caso de no acordarnos, simplemente pulsando el botón "Visitar la web". Si creaste tu cuenta iniciando sesión desde Facebook o tienes activada la verificación en dos pasos, no podrás usar este complemento.

Una vez verificados, se nos pedirá que descarguemos la base de datos. Si no tenemos la base de datos el complemento no iniciará, por lo que tenemos que decir que si.

### Unos apuntes sobre el inicio de sesión y la base de datos.

Cuando iniciemos sesión y descarguemos la base de datos, se creará en nuestra carpeta de usuario de NVDA una carpeta llamada Audiocinemateca.

En dicha carpeta hay un archivo llamado .audiocinemateca. Este archivo contiene nuestro usuario y contraseña, junto a la configuración del complemento.

Luego hay dos archivos  .json, que son el catálogo y la versión del catálogo.

Ten en cuenta que si hacemos un portable y lo compartimos, en esta carpeta estará nuestro usuario y contraseña de la Audiocinemateca. Es aconsejable que si vamos a compartir el portable, antes de crear dicho portable, regresemos a valores por defecto el complemento o borremos la carpeta que se encuentra en nuestro usuario de NVDA llamada Audiocinemateca.

El autor del complemento no se responsabiliza si compartes el usuario o contraseña, quedas avisado de la ubicación de dichos datos y en tu mano está el que no sean compartidos.

El tamaño de las actualizaciones de este complemento de la base de datos es aproximadamente entre 1.5 / 2 megas.

## Menú Herramientas / Audiocinemateca

En este menú tenemos las siguientes posibilidades:

* Iniciar la Audiocinemateca: nos mostrará la interfaz del complemento. Sólo podremos tener un diálogo abierto, o la interfaz de la Audiocinemateca o las Opciones.
* Opciones: nos mostrará un diálogo con opciones para personalizar el complemento a nuestro gusto. El diálogo de opciones sólo puede mostrarse si la interfaz de la Audiocinemateca está cerrada y no hay nada reproduciéndose.
* Volver a valores por defecto: regresará todos los ajustes del complemento a sus valores por defecto, quedando como si hubiese sido recién instalado.
* Documentación del complemento: esto está bien para aquellos que no saben cómo encontrar la documentación. Mostrará este documento.

##  Teclas que podemos asignar en Gestos de entrada

En este apartado podemos asignar las siguientes teclas:

* Muestra la ventana de Audiocinemateca: cargará la interfaz del complemento.
* Muestra la ventana de Opciones: nos mostrará el diálogo con opciones para personalizar el complemento.
* Bajar volumen y Subir volumen: nos permitirá controlar el volumen dándonos información en todo momento desde cualquier parte.
* Bajar velocidad y Subir velocidad: nos permitirá manejar la velocidad de reproducción dándonos información en todo momento desde cualquier parte.
* Adelantar la reproducción y Atrasar la reproducción: nos permitirá atrasar o adelantar en segundos o minutos la reproducción según tengamos configurado en opciones.
* Reproducir / Pausar la reproducción: nos permitirá poner en pausa o reproducir desde cualquier parte.
* Detener la reproducción: parará la reproducción que en ese momento esté sonando o pausada.
* Información de la reproducción: nos dará el tiempo transcurrido de la reproducción, así como el tiempo total de duración de la reproducción.

Todas las acciones referidas al reproductor podrán ser ejecutadas sólo si la ventana de la Audiocinemateca está cerrada.

En todo momento tendremos mensajes hablados de lo que ocurre al presionar cualquier opción anterior.

Sólo podremos tener un diálogo abierto, o la interfaz de la Audiocinemateca o las Opciones.

El diálogo de opciones sólo puede mostrarse si la interfaz de la Audiocinemateca está cerrada y no hay nada reproduciéndose.

## Interfaz principal

La pantalla principal del complemento consta de 3 secciones: consultas, reproductor y otros.

* Consultas: en esta parte tendremos toda la información de las películas, series, documentales y cortometrajes ordenados en pestañas. Consta de 5 pestañas:
	* Pestaña General (Alt+1): esta es la pestaña que se enfocará cada vez que abramos el complemento, dejándonos en la lista de las últimas películas añadidas. En esta pestaña, si pulsamos Alt+C nos llevará a un cuadro combinado donde podremos elegir las distintas categorías. Si pulsamos Alt+L nos llevará a la lista de nuevo y nos mostrará lo último añadido de la categoría que hayamos elegido. A esta pestaña podemos llegar rápidamente pulsando Alt+1 desde cualquier parte de la interfaz. Si pulsamos intro en un elemento de la lista, se nos abrirá un diálogo con información de la película, serie, documental o cortometraje. Estos diálogos son todos iguales, con algunas diferencias para contemplar cada categoría. Los diálogos de documentales y cortometrajes son exactamente iguales. El de películas trae un cuadro combinado para dejarnos elegir qué parte de la película queremos ver, en caso de que la película sea muy larga y se haya dividido en varias partes. El diálogo de las series se diferencia en tener un cuadro combinado donde podremos elegir la temporada en caso de tener más de una, y un listado con los episodios. Todos los diálogos tienen un cuadro de edición de solo lectura, donde podremos ver la ficha de lo que hayamos elegido con las teclas. Además, todos los diálogos tienen un botón reproducir, descargar, Información adicional en la web y cerrar. Reproducir y descargar siempre será sobre lo elegido, en el caso de las series por ejemplo nos reproducirá o descargará el episodio x de la temporada x que tengamos elegido. El botón Información adicional en la web nos dará más información en caso de haberla en la web, principalmente en Filmaffinity, aunque puede que se derive a otras webs que contengan información sobre lo elegido. Estos diálogos son iguales en todas las pestañas, y sólo pueden ser llamados desde la lista pulsando intro sobre algún elemento. Si pulsamos el botón Reproducir, se activará el reproductor explicado más adelante. Si pulsamos descargar se abrirá un diálogo donde tendremos que elegir la carpeta donde deseamos que se guarde la descarga. Sólo se puede descargar un archivo a la vez y siempre tendremos que decir dónde lo queremos. Esto a sido hecho así para que no se abuse de las descargas. También en la pestaña General tenemos un botón llamado "¿No sabes qué ver? Pulsa aquí y te ofreceré algo, a ver si acierto", que podemos llamar con Alt+P. Este botón nos abrirá un diálogo con algo aleatorio, por si no sabemos qué ver.
	* Pestañas Películas, Series, Documentales y Cortometrajes (Alt+2 hasta Alt+5): en estas pestañas tendremos un cuadro de edición para buscar. Podemos acceder a este cuadro rápidamente con Alt+B. En este cuadro, si escribimos algo y pulsamos intro, se nos mostrará en el listado todo lo que corresponda. La búsqueda que realicemos es indiferente a si está escrito en minúsculas, mayúsculas o mezclado. Cuando hace internamente la búsqueda, todo es convertido en minúsculas para facilitar la búsqueda. Si no encuentra nada en el listado, nos dirá sin resultados. Si encuentra, nos mostrará todos los resultados. Si pulsamos intro en la lista, se abrirá el correspondiente diálogo con la ficha y las acciones explicado más arriba. Para volver a tener todo el listado, tenemos que borrar todo el campo de búsqueda y dar a intro. Con esto volverá a tener el listado todos los elementos de la categoría en la que nos encontremos. Todos los listados, además, tienen 2 teclas para orientarnos en ellos: Ctrl+I, que nos informará de la posición del listado que estamos, dándonos el elemento que nos encontramos y el total de elementos. Y tenemos la otra combinación, que es Ctrl+F. Con esto se nos mostrará un diálogo donde podremos poner la posición que queremos que nos deje el foco. Esto va bien por ejemplo en las películas, que hay muchas, y si no queremos ir con las flechas o subir o bajar página esto nos ahorrará tiempo. De momento las búsquedas sólo son sobre el título, pero próximamente se agregarán más filtros de búsqueda. Existe para esta sección otra combinación, que es Ctrl+Espacio. Cuando pulsemos esta combinación nos informará de la pestaña en la que nos encontramos.

Si pulsamos del Alt+1 al Alt+5, siempre con estas combinaciones, el foco nos dejará en la lista de títulos de la pestaña que hayamos elegido.

## Reproductor

Cuando demos en alguno de los diálogos de las fichas al botón reproducir en la pantalla principal, se activarán los botones del reproductor, siendo atrasar, reproducir o pausar (este botón cambiará según el estado de la reproducción), adelantar y detener.

En los botones atrasar y adelantar, si pulsamos la tecla aplicaciones o Shift+f10, nos mostrará un menú con el tiempo que podemos asignar al botón. Dicho tiempo es el que se guardará en la configuración y estará marcado el que en ese momento tengamos elegido. Esto se puede cambiar también desde el diálogo Opciones.

El botón reproducir / pausar cambiará su nombre dependiendo del estado de la reproducción.

El botón detener parará por completo la reproducción.

Este área tiene las siguientes teclas:

* F1 y F3: Atrasa y adelanta el tiempo según lo que tengamos seleccionado.
* F2: Pausa o reproduce según estado.
* F4: Detiene por completo la reproducción.
* F5 y F6: Baja y sube el volumen de reproducción.
* F7 y F8: Baja y sube la velocidad de reproducción.
* F9: Nos da información del tiempo transcurrido de reproducción y tiempo total de reproducción.

Las teclas de función funcionan en cualquier diálogo de la interfaz principal, por lo que podemos seguir viendo la ficha de una película y pausar desde el diálogo de la ficha lo que esté reproduciéndose.

Los botones del reproductor no tienen atajos, por lo que nos tendremos que mover por ellos con tab y Shift+TAB.

Mientras haya algo reproduciéndose, tendremos la posibilidad de usar las teclas de función.

Las teclas de función verbalizarán información si en Opciones tenemos marcado que así lo haga sobre lo que sucede en cada momento que las pulsamos. La única tecla que siempre dirá algo y no está supeditada a si en opciones tenemos marcada o no la opción Activar o desactivar los mensajes informativos es F9. Esta tecla siempre nos hablará.

Aviso sobre las teclas de Función: si las pulsamos repetitivamente y está activada la verbalización de información, podemos encontrar un pequeño retraso. Esto es debido a que para dar la información es necesario callar a NVDA y mandar por un hilo aparte la información. Si vemos que se sobreponen mensajes podemos callarlo pulsando Ctrl.

Se aconseja no dejar pulsadas estas teclas de función y escuchar el mensaje tras cada pulsación. Si está desactivado, ese retraso ya no aparecerá, por lo que si deseamos bajar rápidamente el volumen podemos dejar pulsada la tecla.

## Otros

En esta sección nos encontramos el volumen, que es una barra deslizante, la velocidad, que es un cuadro combinado, y si la reproducción está activa, un cuadro combinado de salida.

El volumen y la velocidad tienen el mismo atajo, Alt+V, moviéndonos entre estos dos controles conforme pulsamos el atajo. Estos dos controles pueden ser llamados desde cualquier parte de la interfaz principal.

El cuadro combinado para la salida tiene el atajo Alt+S, y sólo puede ser llamado si la reproducción está activa. De lo contrario, este cuadro se oculta. Mientras la reproducción esté activa, puede ser llamado desde cualquier parte de la interfaz principal.

La salida nos mostrará todos los dispositivos por los que podemos escuchar la reproducción. Cada vez que termine o detengamos la reproducción, este cuadro volverá a su valor por defecto, poniendo el dispositivo de salida predeterminado. Por tanto, en la siguiente reproducción, si queremos otro dispositivo, tendremos que volverlo a elegir.

La salida del audio de la reproducción es independiente de la salida de NVDA, por lo que podríamos estar escuchando a NVDA por unos auriculares y la película, serie, documental o cortometraje por unos altavoces.

Luego tenemos el botón menú, con el atajo Alt+M. Cuando lo pulsemos se nos mostrará un menú con los siguientes ítems:

* Actualizar base de datos: nos mostrará un diálogo para actualizar la base de datos. En dicho diálogo, se nos informará en todo momento de lo que está sucediendo y si hay actualizaciones. Si existen actualizaciones, nos informará y tendremos que dar al botón actualizar. No hay un día ni una hora establecida para que la base de datos tenga actualizaciones. Tendremos que revisarlo nosotros cada cierto tiempo. La web estará siempre más actualizada con algún título que la base de datos no tiene todavía, ya que se va actualizando conforme entra el material. La base de datos que el complemento usa hay que generarla manualmente, por lo que puede existir esa diferencia durante horas o algún día respecto a la base de datos de la web y el complemento. Espero que esto se automatice y cada vez tengamos las novedades antes. No obstante, no es mucha la diferencia. Cada vez que actualicemos, el complemento se cerrará y tendremos que volver a llamarlo. Si hay algo reproduciéndose, continuará sin que la actualización de la base de datos le afecte.
* Donar a la Audiocinemateca: nos llevará a la página web de la Audiocinemateca y nos dejará en la sección para donar. Tengo que decir que este proyecto lleva un coste, el cual se sufraga gracias a las donaciones. En la página está todo bien explicado. Por favor, por poco que sea, todo ayuda a que el proyecto siga adelante.
* Cerrar: sale del complemento. Si hay algo reproduciéndose, continuará y podremos manejar la reproducción desde los atajos que hayamos configurado en gestos de entrada.

## El diálogo de opciones

Este diálogo tiene dos pestañas:

### General

En esta pestaña tenemos las siguientes opciones:

* Activar o desactivar los mensajes informativos: si la marcamos, tendremos mensajes informativos en distintas acciones del complemento.
* Cantidad de resultados a mostrar de las últimas entradas: aquí podremos elegir cuantos resultados deseamos ver en la pestaña general del complemento.
* Botón Volver a valores por defecto: volveremos a valores por defecto los ajustes del complemento. Si tenemos usuario y contraseña se borrarán y tendremos que volver a iniciar sesión en el complemento. En todos los Volver a valores por defecto del complemento la base de datos nunca se borra si ya a sido descargada.

### Reproductor:

En esta pestaña tenemos las siguientes opciones:

* Seleccione el tiempo para retroceder la reproducción: en este cuadro podemos elegir el tiempo que se retrocederá la reproducción.
* Seleccione el tiempo para adelantar la reproducción: en este cuadro podremos elegir el tiempo para adelantar la reproducción.

Tenemos dos botones: Aceptar, que guardará los cambios, o Cancelar, que no guardará nada y dejará los ajustes del complemento como estaban.

Podemos cerrar este diálogo también con Alt+F4, pero de esta manera tampoco se guardarán los cambios si habíamos echo alguno.

Este diálogo irá incorporando pestañas y opciones conforme se vayan agregando nuevas características al complemento.

## Agradecimientos:

Deseo agradecer a José Manuel Delicado su paciencia, que me a tenido durante el desarrollo del complemento, aguantando todas mis consultas.

Igualmente, quiero agradecerle a él y a todos sus colaboradores de la Audiocinemateca todo su buen hacer y su trabajo para que este proyecto siga adelante.

No quiero dejar de mencionar, por favor, que por poco que sea, si se puede donar, hacedlo. Este proyecto creo que nos da un lugar de disfrute, mucho entretenimiento, y para esto hay gente detrás empleando mucho tiempo de su vida personal junto a dinero que cuesta la infraestructura de dicho proyecto.

## Registro de cambios.
### Información sobre las actualizaciones:

Este complemento seguirá la siguiente ruta de actualizaciones:

Solo las versiones de tipo mayor.menor (por ejemplo v3.1) son listados en este historial.

Las versiones de tipo mayor.menor.x (por ejemplo v3.1.2) son actualizaciones de corrección de errores.

Los cambios en el complemento se reflejarán en esta sección explicando las novedades.

El documento principal no se modificará, siendo una orientación para el usuario.

El usuario es el responsable de revisar esta sección para estar informado de los cambios.

### Versión 1.2.

* Añadido nueva carga de la interface al actualizar la base de datos.

Ahora cuando se actualice la base de datos, automáticamente la interface se volverá a cargar.

* Añadida nueva búsqueda inmediata por @javidominguez

Ahora cuando empecemos a escribir en la búsqueda se irán mostrando los resultados que coincidan.

* Compatible con NVDA 2024.1

### Versión 1.1.

* Añadidos filtros de búsqueda.

Se han añadido los siguientes filtros de búsqueda:

Título, año, genero, país, director, guion, música, fotografía, reparto, productora, narración y sinopsis.

Por defecto cuando lancemos el complemento después de iniciar NVDA el filtro elegido en todas las categorías es por título.

Los filtros una vez elegidos se mantendrán en la sesión actual de NVDA, esto quiere decir que mientras no cerremos NVDA los filtros elegidos se mantendrán indiferentemente de si cerramos la interface de la Audiocinemateca.

Cada categoría tiene independencia de filtros, lo que quiere decir que podemos buscar en películas por año por ejemplo y en series por narración.

Para poder elegir los filtros tendremos que tener el foco en el campo de búsqueda de cualquiera de las categorías y pulsar Ctrl+F. Aparecerá un menú con todos los filtros, el filtro actual estará marcado. Al pulsar intro en un filtro se seleccionará y quedará marcado ese filtro.

También en la etiqueta identificativa del campo de búsqueda cambiara al filtro que hayamos elegido.

* Añadido atajo de teclado para borrar rápidamente los campos de búsqueda.

Ahora si en un campo de búsqueda de cualquiera de las categorías pulsamos Ctrl+B el campo de texto se borrara.

Si el campo ya a echo una búsqueda el comportamiento es como si hiciéramos intro, borrara el texto y nos mostrara todos los títulos de esa categoría.

Si no hemos hecho ninguna búsqueda borrará el texto que haya en el campo de búsqueda y no hará nada más.

* Añadido F12 para activar o desactivar los mensajes en la pantalla principal y secundarias.

Ahora podremos desactivar los mensajes informativos si lo deseamos sin necesidad de entrar al dialogo de opciones. Pulsando F12 nos informara si se desactivan o activan los mensajes.

* Corregido al pulsar intro en cuadro de texto en el dialogo ir a la posición.

Se a corregido que si apretábamos intro en el campo de texto del dialogo de posición a veces si había un valor erróneo no actuaba como toca.

* Corregido size de la ventana principal a 800x600.

Se a corregido la resolución del complemento a 800x600 para soportar monitores más antiguos.

Esto esta pendiente de valoración según llegue retroalimentación de usuarios con resto visual.

Se intentará dar la resolución óptima para todos.

* Corrección de errores internos y ortográficos.

Se agradece que si se encuentran errores ortográficos por favor los mencionéis y con gusto se corregirán.

### Versión 1.0.

* Versión inicial.
