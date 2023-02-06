# Manual de la Audiocinemateca para NVDA

Este complemento nos ofrece el tener la pagina de la Audiocinemateca en nuestro NVDA.

Por si alguien no sabe lo que es la Audiocinemateca aconsejo pegarse un paseo por aquí:

[Pagina oficial de la Audiocinemateca](https://www.audiocinemateca.com)

Bien si continuas es por que ya sabes lo que es, pues ahora en NVDA podrás tener en un complemento la Audiocinemateca.

Que ofrece el complemento

 El complemento te dejara, consultar, reproducir, descargar cualquier película, serie, documental o cortometraje que se encuentre en la Audiocinemateca.

* Podremos consultar la ficha con los mismos datos que en la pagina web.

* Podremos reproducir en un sencillo reproductor las películas, series eligiendo temporada y episodio, documental o cortometraje.

* También podremos descargar cualquier película, serie eligiendo temporada y episodio, documental y cortometraje.

En el caso de las películas puede haber alguna que contenga más de una parte por lo que nos dejara elegir que parte de la película deseamos reproducir o descargar.

Las series tanto la reproducción como la descarga tendremos que elegir la temporada que deseamos en caso de haber más de una y el episodio.

El complemento podrá ser manejado a través de una interface tanto las consultas, reproducción como descarga.

Además cuando estemos reproduciendo algo podremos manejar todo el aspecto de la reproducción desde cualquier parte de Windows.

Bien el complemento puede ser lanzado desde el menú Herramientas / Audiocinemateca o asignando las correspondientes teclas en Gestos de entrada / Audiocinemateca.

Bien el complemento viene sin teclas asignadas por lo que tendremos que asignárselas.

El complemento requiere que tengamos un usuario y contraseña validos de la Audiocinemateca.

El complemento viene sin la base de datos por lo que la primera vez que ejecutemos el complemento nos pedirá que descarguemos la base de datos.

La primera vez que ejecutemos el complemento se nos pedirá que metamos nuestro usuario y contraseña de la Audiocinemateca, en la pantalla de iniciar sesión podremos también ir a la pagina web para registrarnos o solicitar una nueva contraseña en caso de no acordarnos simplemente pulsando el botón Visitar la web.

Una vez verificados se nos pedirá que descarguemos la base de datos, si no tenemos la base de datos el complemento no iniciara por lo que tenemos que decir que si.

Unos apuntes sobre el inicio de sesión y la base de datos.

Bien cuando iniciemos sesión y descarguemos la base de datos se creará en nuestra carpeta de usuario de NVDA una carpeta llamada Audiocinemateca.

En dicha carpeta hay un archivo llamado .audiocinemateca, este archivo contiene nuestro usuario y contraseña junto a la configuración del complemento.

Luego hay dos archivos. json que son el catalogo y la versión del catalogo.

Bien advertir que si hacemos un portable y lo compartimos en esta carpeta estará nuestro usuario y contraseña de la Audiocinemateca, es aconsejable que si vamos a compartir el portable antes de crear dicho portable regresemos a valores por defecto el complemento o borrar la carpeta que se encuentra en nuestro usuario de NVDA llamada Audiocinemateca.

El autor del complemento no se responsabiliza si usted comparte el usuario o contraseña, queda avisado de la ubicación de dichos datos y en su mano esta el que no sea compartido.

## Menú Herramientas / Audiocinemateca

En este menú tenemos las siguientes posibilidades:

* Iniciar la Audiocinemateca

Nos mostrara la interface del complemento. Solo podremos tener un dialogo abierto, o la interface de la Audiocinemateca o las Opciones.

* Opciones

Nos mostrara un dialogo con opciones para personalizar el complemento a nuestro gusto. El dialogo de opciones solo puede mostrarse si la interface de la Audiocinemateca esta cerrada y no hay nada reproduciéndose.

* Volver a valores por defecto

Regresara todos los ajustes del complemento a sus valores por defecto quedando como si hubiese sido recién instalado.

* Documentación del complemento

Esto esta bien para aquellos que no saben como encontrar la documentación. Mostrara este documento.


##  Teclas que podemos asignar en Gestos de entrada

En este apartado podemos asignar las siguientes teclas:

* Muestra la ventana de Audiocinemateca

Cargara la interface del complemento.

* Muestra la ventana de Opciones

Nos mostrara el dialogo con opciones para personalizar el complemento.

* Bajar volumen y Subir volumen

Nos permitirá controlar el volumen dándonos información en todo momento desde cualquier parte.

* Bajar velocidad y Subir velocidad

Nos permitirá manejar la velocidad de reproducción dándonos información en todo momento desde cualquier parte.

* Adelantar la reproducción y Atrasar la reproducción

Nos permitirá atrasar o adelantar en segundos o minutos la reproducción según tengamos 
configurado en opciones.

* Reproducir / Pausar la reproducción

Nos permitirá poner en pausa o reproducir desde cualquier parte.

* Detener la reproducción

Parara la reproducción que en ese momento este sonando o pausada.

* Información de la reproducción

Nos dará el tiempo transcurrido de la reproducción como el tiempo total de duración de la reproducción.

Todas las acciones referidas al reproductor podrán ser ejecutadas solo si la ventana de la Audiocinemateca esta cerrada.

En todo momento tendremos mensajes hablados de lo que ocurre al presionar cualquier opción anterior.

Solo podremos tener un dialogo abierto, o la interface de la Audiocinemateca o las Opciones.

El dialogo de opciones solo puede mostrarse si la interface de la Audiocinemateca esta cerrada y no hay nada reproduciéndose.

# Interface principal

La pantalla principal del complemento consta de 3 secciones.

Consultas, reproductor y otros.

* Consultas:

En esta parte tendremos toda la información de las películas, series, documentales y cortometrajes ordenados en pestañas.

Consta de 5 pestañas:

* Pestaña General (Alt+1)

Esta es la pestaña que enfocara cada vez que abramos el complemento, dejándonos en la lista de las ultimas películas añadidas.

En esta pestaña si pulsamos Alt+C nos llevara a un cuadro combinado donde podremos elegir las distintas categorías.

Si pulsamos Alt+L nos llevara a la lista de nuevo y nos mostrara lo ultimo añadido de la categoría que hayamos elegido.

Bien a esta pestaña podemos llegar rápidamente pulsando Alt+1 desde cualquier parte de la interface.

Si pulsamos intro en un item de la lista se nos abrirá un dialogo con información de la película, serie, documental o cortometraje.

Estos diálogos son todos iguales con algunas diferencias para contemplar cada categoría.

Los diálogos de documentales y cortometrajes son exactamente iguales, el de películas trae un cuadro combinado para dejarnos elegir que parte de la película queremos ver en caso de que la película sea muy larga y se haya dividido en varias partes. El dialogo de las series se diferencia en tener un cuadro combinado donde podremos elegir la temporada en caso de tener más de una y un listado con los episodios.

Todos los cuadros tienen un cuadro de edición de solo lectura donde con las teclas podremos ver la ficha de lo que hayamos elegido.

Además, todos los diálogos tienen un botón reproducir, descargar, Información adicional en la web y cerrar.

Reproducir y descargar siempre será sobre lo elegido, en el caso de las series por ejemplo nos reproducirá o descargara el episodio x de la temporada x que tengamos elegido. El botón Información adicional en la web nos dará más información en caso de haberla en la web principalmente en Filmaffinity aunque puede que se derive a otras webs que contengan información sobre lo elegido.

Estos diálogos son iguales en todas las pestañas y solo pueden ser llamados desde la lista pulsando intro sobre algún item.

Si pulsamos el botón Reproducir se activará el reproductor explicado más adelante.

Si pulsamos descargar se abrirá un dialogo donde tendremos que elegir la carpeta donde deseamos que se guarde la descarga, solo puede descargar un item a la vez y siempre tendremos que decir donde lo queremos.

Esto a sido echo a si para que no se abuse de las descargas. Lo que viene siendo quien algo quiere algo le cuesta.

También en la pestaña General tenemos un botón llamado ¿No sabes que ver? Pulsa aquí y te ofreceré algo, haber si acierto el cual podemos también llamar con Alt+P. Este botón nos abrirá un dialogo con algo aleatorio, por si no sabemos que ver.

* Pestañas Películas, Series, Documentales y Cortometrajes (Alt+2 hasta Alt+5)

En estas pestañas tendremos un cuadro de edición para buscar, podemos acceder a este cuadro rápidamente con Alt+B.

Bien en este cuadro si escribimos algo y pulsamos intro se nos mostrara en el listado todo lo que corresponda.

La búsqueda que realicemos es indiferentemente si esta escrito en minúsculas, mayúsculas o mezclado cuando hace internamente la búsqueda todo es convertido en minúsculas para facilitar la búsqueda.

Si no encuentra nada en el listado nos dirá sin resultados. Si encuentra nos mostrara todos los resultados.

Si pulsamos intro en la lista se abrirá el correspondiente dialogo con la ficha y las acciones explicado más arriba.

Para volver a tener todo el listado tenemos que borrar todo el campo de búsqueda y dar a intro, con esto volverá a tener el listado todos los ítems de la categoría en la que nos encontremos.

Todos los listados además tienen 2 teclas para orientarnos en ellos, Ctrl+I que nos informara en la posición del listado que estamos dándonos el item que nos encontramos y el total de ítems.

Y tenemos la otra combinación que es Ctrl+F, con esto se nos mostrara un dialogo donde podremos poner la posición que queremos que nos deje el foco, esto va bien por ejemplo en las películas que hay muchas y si no queremos ir con las flechas o subir o bajar pagina esto nos ahorrara tiempo.

De momento las búsquedas solo son sobre el titulo, pero próximamente se agregarán más filtros de búsqueda.

Existe para esta sección otra combinación que es Ctrl+Espacio, cuando pulsemos esta combinación nos informara de la pestaña en la que nos encontramos.

Decir que si pulsamos del Alt+1 al Alt+5 siempre con estas combinaciones el foco nos dejara en la lista de títulos de la pestaña que hayamos elegido.

Reproductor

Cuando demos en alguno de los diálogos de las fichas al botón reproducir en la pantalla principal se activarán los botones del reproductor.

Siendo atrasar, reproducir o pausar (este botón cambiara según el estado de la reproducción), adelantar y detener.

Bien en los botones atrasar y adelantar si pulsamos la tecla aplicaciones o Shift+10 nos mostrara un menú con el tiempo que podemos asignar al botón, dicho tiempo es el que se guardara en la configuración y estará marcado el que en ese momento tengamos elegido. Esto se puede cambiar también desde el dialogo Opciones.

El botón reproducir / pausar cambiara su nombre dependiendo del estado de la reproducción.

El botón detener parara por completo la reproducción.

Bien esta área tiene las siguientes teclas:

* F1 y F3: Atrasa y adelanta el tiempo según lo que tengamos seleccionado.
* F2: Pausa o reproduce según estado.
* F4: Detiene por completo la reproducción.
* F5 y F6: Baja y sube el volumen de reproducción.
* F7 y F8: Baja y sube la velocidad de reproducción.
* F9: Nos da información del tiempo transcurrido de reproducción y tiempo total de reproducción.

Las teclas de funciones funcionan en cualquier dialogo de la interface principal por lo que podemos seguir por ejemplo viendo la ficha de una película y poder pausar desde el dialogo de la ficha lo que este reproduciéndose.

Bien los botones del reproductor no tienen atajos por lo que nos tendremos que mover por ellos con tab y Shift+TAB.

Pero mientras haya algo reproduciéndose tendremos la posibilidad de usar las teclas de función.

Las teclas de función nos informaran en todo momento si en Opciones tenemos marcado que así lo haga sobre lo que sucede en cada momento que las pulsamos, la única tecla que siempre dirá algo y no esta supeditada a si en opciones tenemos marcada o no la opción Activar o desactivar los mensajes informativos. Es F9, esta tecla siempre nos hablara.

Doy un aviso sobre las teclas de Función, si las pulsamos muy continuamente y esta activada que nos de información podemos encontrar un pequeño retraso esto es por que para dar la información es necesario callar al NVDA y mandar por un hilo aparte la información. Si vemos que se sobreponen mensajes podemos callarlo pulsando Ctrl.

Aconsejo no dejar pulsadas estas teclas de función e ir pulsación, escuchar mensaje, pulsación. Si esta desactivado la información ese retraso ya no aparecerá por lo que por ejemplo si deseamos bajar rápidamente el sonido podemos dejar pulsado.

Con la información activa también, pero recordar que se pueden sobreponer mensajes y a veces es molesto.

Otros:

En esta sección nos encontramos el volumen que es una barra deslizante, la velocidad que es un cuadro combinado y si la reproducción esta activa un cuadro combinado de salida.

El volumen y la velocidad tienen el mismo atajo Alt+V moviéndonos entre estos dos controles conforme pulsamos el atajo. Estos dos controles pueden ser llamados desde cualquier parte de la interface principal.

El cuadro combinado para la salida tiene el atajo Alt+S y solo puede ser llamado si la reproducción esta activa de lo contrario este cuadro se oculta, mientras la reproducción este activa puede ser llamado desde cualquier parte de la interface principal.

Sobre la salida nos mostrará todos los dispositivos por los que podemos escuchar la reproducción, decir que cada vez que termine o detengamos la reproducción este cuadro volverá a valor por defecto poniendo el dispositivo de salida por defecto. Por lo que la siguiente reproducción si queremos otro dispositivo tendremos que volverlo a elegir.

La salida del audio de la reproducción es aparte de la salida de NVDA. Por lo que podríamos estar escuchando por ejemplo a NVDA por unos auriculares y la película, serie, documental o cortometraje por unos altavoces.

Luego tenemos el botón menú con el atajo Alt+M, cuando lo pulsemos se nos mostrara un menú con los siguientes ítems:

* Actualizar base de datos. 

Nos mostrara un dialogo para actualizar la base de datos, en dicho dialogo nos informara en todo momento de lo que esta sucediendo y si existe o no actualizaciones.

Si existen actualizaciones nos informara y tendremos que dar al botón actualizar.

Este dialogo es sencillo por lo que poco más que explicar.

Decir que no hay un día ni una hora establecida para que la base de datos tenga actualizaciones, tendremos que revisarlo nosotros cada x tiempo.

Comentar que la web estará siempre más actualizada con algún titulo que la base de datos no tiene todavía ya que se va actualizando conforme entra el material.

La base de datos que el complemento usa hay que generarla manualmente por lo que puede haber esa diferencia durante horas o algún día respecto a la base de datos de la web y el complemento.

Espero que esto se automatice y cada vez tengamos las novedades antes, no obstante, no es mucha la diferencia.

Cada vez que actualicemos el complemento se cerrara y tendremos que volver a llamarlo. Si hay algo reproduciéndose continuara sin afectar la actualización de la base de datos a la reproducción.

* Donar a la Audiocinemateca.

Nos llevara a la pagina web de la Audiocinemateca y nos dejara en la sección para donar. Tengo que decir que este proyecto lleva un coste el cual se sufraga gracias a las donaciones. En la pagina esta todo bien explicado.

Por favor por poco que sea, todo ayuda a que el proyecto siga adelante.

* Cerrar

Sale del complemento, si hay algo reproduciéndose continuara y podremos manejar la reproducción desde los atajos que hayamos configurado en gestos de entrada.

# Dialogo opciones

Este dialogo tiene dos pestañas:

General:

En esta pestaña tenemos las siguientes opciones:

* Activar o desactivar los mensajes informativos.

Si la marcamos tendremos mensajes informativos en distintas acciones del complemento.

* Cantidad de resultados a mostrar de las ultimas entradas

Aquí podremos elegir cuantos resultados deseamos ver en la pestaña general del complemento.

* Botón Volver a valores por defecto

Volveremos a valores por defecto los ajustes del complemento, si tenemos usuario y contraseña se borrarán y tendremos que volver a iniciar sesión en el complemento.

En todos los Volver a valores por defecto del complemento la base de datos nunca se borra si ya a sido descargada.

Reproductor:

En esta pestaña tenemos las siguientes opciones:

* Seleccione el tiempo para retroceder la reproducción:

En este cuadro podemos elegir el tiempo que se retrocederá la reproducción.

* Seleccione el tiempo para adelantar la reproducción:

En este cuadro podremos elegir el tiempo para adelantar la reproducción.

Tenemos dos botones Aceptar que guardara los cambios o Cancelar que no guardara nada y dejara los ajustes del complemento como estaban.

Podemos cerrar este dialogo también con Alt+F4 pero de esta manera tampoco se guardarán los cambios si habíamos echo alguno.

Este dialogo ira incorporando pestañas y opciones conforme se vayan agregando nuevas características al complemento.

# Agradecimientos:

Deseo agradecer a José Manuel Delicado su paciencia que me a tenido durante el desarrollo del complemento, aguantando todas mis consultas.

Igualmente quiero agradecerle a el y a todos sus colaboradores de la Audiocinemateca todo su buen hacer y su trabajo para que este proyecto siga adelante.

No quiero dejar de mencionar por favor que por poco que sea si se puede donar, hacerlo que este proyecto creo que nos da un lugar de disfrute, mucho entretenimiento y para esto hay gente detrás empleando mucho tiempo de su vida personal junto a dinero que cuesta la infraestructura de dicho proyecto.

# Registro de cambios.
## Información sobre las actualizaciones:

Este complemento seguirá la siguiente ruta de actualizaciones:

Solo las versiones de tipo mayor.menor (por ejemplo v3.1) son listados en este historial.

Las versiones de tipo mayor.menor.x (por ejemplo v3.1.2) son actualizaciones de corrección de errores.

Los cambios en el complemento se reflejarán en esta sección explicando las novedades.

El documento principal no se modificará siendo una orientación para el usuario.

El usuario es el responsable de revisar esta sección para estar informados de los cambios.

## Versión 1.0.

* Versión inicial.
