--------------------
Ejemplo de ejecucion
--------------------


python hu.py --user USUARIO_AQUI --passwd PASSWD_AQUI --db 849 --userstory \[CICSA\]Compras\ y\ Contratos/cyc.csv --process \[CICSA\]Compras\ y\ Contratos/procesos_cyc.csv --project "[CICSA]Compras y Contratos" --port 10000 --assistant \[CICSA\]Compras\ y\ Contratos/cc_asistente.csv --supervisor "Rafael Silva [vauxoo]" --execution "Ma. Gabriela Quilarque[SI] [Vauxoo]"

---------------
Generar los csv
---------------

1. Descagar el documento de requerimientos por ejemplo el de compras y contratos: https://docs.google.com/a/vauxoo.com/spreadsheet/ccc?key=0AqiJAVelZw_IdEY0a2NtZmNHeUlfTTM4Wk5NRGZJalE&usp=drive_web#gid=0 como tipo ods.

2. Crear una carpeta donde se tendran los csv de las historia de usuario a cargar

3. Abrir el archivo ODS descargado, y hacer click en "guardar como" y colocar de tipo csv. 
   Definir delimitadores con comillas (") y separadores con coma (,)

4. Separar ese archivo csv, en dos archivos diferentes, asistentes.csv y hu.csv(por ejemplo).

   4.1 hu.csv será el archivo que contenga solo las historias de usuario.
   por lo tanto eliminar el encabezado que contiene los asistentes, fechas, etc.
   (En pocas palabras, eliminar las filas 1,2,3,4,5,6,7,8).

   El archivo debe ir separado por coma, y delimitado por doble comilla. (Ya esto debe estar con
   el paso 2)

   Se debe agregar una nueva columna date al principio del csv.

   Limpiar el archivo csv, de resto de informacion que no corresponden a columnas.
   Por ejemplo, las ultimas líneas siempre tienen información que no se usara, como
   total de tiempo, filas con ids que no tienen información, etc. Todo eso eliminarlo
   A veces existe información en celdas que no corresponden a una columna específica, tambien
   se debe borrar esas columnas, que siempre estan de último.

   4.2 asistentes.csv será el archivo con los asistentes, puedes ver un ejemplo en cualquier de las
   carpetas presentes en este branch (ejemplo: [CICSA]SG), solo tendrá 3 columnas, el ID que 
   corresponde al número que se usa para nombrarlo en el título de la HU, el name y el rol.

5. Luego ejecutar el script

6. Colocar en el archivo Run.rst el comando a ejecutar las historias de usuario deseada
   para que el administrador del sistema sepa lo que tiene que hacer

.. note::

    Pueden hacer python hu.py --help para mas información

------
Campos
------

Para csv de HU
~~~~~~~~~~~~~~

En el nombre de las HU se debe colocar entre parentesis cuando se refiere a una persona
Yo como (2)

ID
Historias de Usuario
Estimación (min)
Observaciones Técnicas
Prioridad
date
Criterios de Aceptación
Nivel de Dificultad
Existe

Cualquier otro campo no se tomara en cuenta

Csv de asistentes
-----------------

id
name
rol

Cualquier otro campo no se tomara en cuenta


Csv de procesos
---------------

Campos del csv de procesos:
~~~~~~~~~~~~~~~~~~~~~~~~~~~

ID
HU ID
Procesos

Ejemplo en:
~~~~~~~~~~~

\[CICSA\]Compras\ y\ Contratos/procesos_cyc.csv

------
TO DO:
------

1. Cambiar la forma en que se especifican los archivos en 2.3) usando un archivo de 
configuración, lo agregaré en la brevedad posible.
**DONE** 2. Voy a revisar el problema del bug para poder crear los proyectos desde el script.
**DONE** 3. mejorar la carga del date en las HU, tengo pensando que se coloque la fecha de una HU, 
y al dejar vacío los date siguientes, se tome la última fecha registrada, para así no 
tener que repetir las fechas, eso lo haré en 5 minutitos que tenga.
4. Tuve que devolver los addons vauxoo a la revision 968, porque con los cambios nuevos el script no está funcionando. Revisaré eso
**DONE** 5. Buscar proyectos por name y no por id
6. mejorar el patron de comparacion, guiado por el id xml
