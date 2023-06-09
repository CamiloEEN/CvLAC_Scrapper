# CvLAC_Scrapper
Conjunto de programas hechos en python que scrappean las páginas públicas de CvLACs de investigadores Colombianos.

<h1>Propósito</h1>
Estos programas fueron desarrollados inicialmente para facilitar la recopilación de información y posterior analisis de los productos resultados de investigación del grupos NATURATU de la Universidad de Ibagué. Dado que su uso fue requerido en otras áreas de la universidad y la utilidad que se le puede dar a otras instituciones, se hace público su acceso por este medio. 

<b>Nota 1: La información extraida proviene directamente de las páginas públicas del CvLAC por lo tanto la información extraida es de caracter público</b>
<b>Nota 2: Se pone a disposición todos los programas de forma pública bajo la licencia: MIT License el día 8 de junio de 2023.</b>

<h1>Instalación</h1>
<h2>Requerimientos</h2>
1. Tener instalado Visual Studio Code con las opciones de abrir carpetas con VS Code (https://code.visualstudio.com/)
2. Tener instalado Excel y LibreOffice (Opcional)
3. Tener instalado Python (versión>3.7) y las librerías bs4 (Beatiful soup) y openpyxl. Si tiene instalado pip “pip install bs4” y “pip install openpyxl” en la CMD basta para instalarlos. Esta información se encuentra fácilmente en internet.
4. Para la instalación de Python, se recomienda buscar en google de “install python” o accediendo al link https://www.python.org/downloads/
En la instalación asegúrese de añadir python a la variable PATH.


<h2>Uso</h2>

Cada programa CvLACpyExtract<b color="Blue">item</b> funciona como se muestra en la imagen:

<img width="581" alt="Funcionamiento_de_los_programas_de_scrappear_CvLACS" src="https://github.com/CamiloEEN/CvLAC_Scrapper/assets/88359710/40ac5cc7-e39a-49bc-b236-12bc066ac041">

Al ejecutarse toma por defecto un archivo llamado consulta.xlsx con la lista de investigadores y los correspondientes links a los CvLACs en la carpeta input y devuelve un archivo .csv en la carpeta output con la lista de <b color="Blue">items</b> obtenidos directamente de los CvLACs.

Para ejecutar cada programa basta con correr el archivo main.py en la respectiva carpeta que contiene el programa. Para más detalles consulte el manual de instrucciones contenido en el repositorio.

<h1>Historia</h1>
El primer programa fue desarrollado por el Docente <b>Carlos Antonio Jacanamejoy Jamioy</b> permite extraer todos los artículos de una lista de CvLACs en un documento excel y los almacena como .csv. Con este programa, <b>Camilo Eduardo Echeverry Naranjo</b> desarrolló varios programas para extraer información de otros productos del CvLAC como parte de su trabajo como Joven Investigador durante el transcurso del año 2022. Además agregó un script que ejecuta todos los programas secuencialmente.


