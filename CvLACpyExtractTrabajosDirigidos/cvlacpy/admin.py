"""
Administra la lectura de datos, y el modo de guardarlos
"""
from .utils import getCvlacsDirs
import bs4
import ssl
from urllib.request import urlopen
from bs4 import BeautifulSoup 
import csv
import re
# Ajusta los certificados utilizados para realizar las conexiones
ssl._create_default_https_context = ssl._create_unverified_context

class Admin(object):
    
    
    def __init__(self,filename):
        
        self.cvlacDirs=getCvlacsDirs(filename)
        self.articulos=[]
        
        
    
    
    def Run(self):
        """
        Realiza la lectura
        """
        if len(self.cvlacDirs)<2:
            print("No hay información para procesar")
            return
        for i in range(1,len(self.cvlacDirs)):
            self.LecturaCvlac(self.cvlacDirs[i][-1])

    def LecturaCvlac(self, urlCvlac):
        """
        Realiza la lectura de una url de CvLAC
        """
        uClient = urlopen(urlCvlac)
        page_html = uClient.read()
        uClient.close()
        page_soup = BeautifulSoup(page_html,"html.parser")
        # Cada sección de información se maneja como una tabla
        secciones = page_soup.findAll("table")
        nombreInvestigador = ""
        for i, sec in enumerate( secciones[0:] ):
            nombreSec = sec.h3
            if nombreSec != None:
                nombreSec = nombreSec.text
            else:
                nombreSec = ""
            if nombreSec != "":
                print(f"seccion {i}:", nombreSec)
            # Extrae el nombre del investigador
            if nombreInvestigador == "" and nombreSec == "" :
                tdNombre = self.ExtraerTag(sec,['tr','td'])
                
                filas = sec.findAll("tr", limit=12)
                for fila in filas:
                    if fila.td.text == "Nombre":
                        nombreInvestigador = fila.findAll("td")[1].text.strip()
                        print("  Nombre identificado:", nombreInvestigador)
                        break

            elif nombreSec != None and nombreSec == "Trabajos dirigidos/tutorías":
                self.ProcesaSecTrabajosDirigidos(sec, nombreInvestigador)

    def ProcesaSecTrabajosDirigidos(self, sec,investigador):
        """
        Procesa la sección de Trabajos Dirigidos
        """
        # Contenedor con la información de cada Trabajo Dirigido
        contInfo = sec.findAll("blockquote")
        # contenedor con los títulos con el tipo de Trabajo Dirigido
        contTipo = sec.findAll("li") 
        
        articulos=[]
        for i in range(0, len(contInfo)):
            tipo = contTipo[i].text
            tipo = tipo.split("-")[1]
            tipo = tipo.strip()

            info_trabDirigido = contInfo[i].text
            
            #Nombre Articulo
            linesInfo = [ l.strip() for l in info_trabDirigido.split("\n")]
            linesInfo = [ l for l in linesInfo if len(l)>0]
            NombreProducto=""
            listaAutores=[]
            lineaClave=0
            if(linesInfo[0][-1] == ","):
                lineaClave=1
                listaAutores= linesInfo[0].split(",")
                
            #print(linesInfo)
            
            
            
            #Nombre del Producto
            NombreProducto=linesInfo[lineaClave]
            #Coautores
            coautores = ", ".join(listaAutores)
            #Lugar
            lugar = linesInfo[lineaClave+1]
            #Estado
            estado = linesInfo[lineaClave+2]
            estado = estado[7:]
            #Programa
            programa = linesInfo[lineaClave+3]
            #Dirigido como
            DirigidoComo = [ l for l in linesInfo if "Dirigió como:" in l]
            DirigidoComo = DirigidoComo[0]
            DirigidoComo = DirigidoComo.split(":")[1]
            #Persona orientada
            PersonaOrientada = ""
            try:
                PersonaOrientada = linesInfo[linesInfo.index("Persona(s) orientada(s):")+1]
                if "Tutor(es)/Cotutor(es):" in PersonaOrientada:
                    PersonaOrientada = ""
            except:
                PersonaOrientada = ""

            #Tutor(es)/cotutor(es)
            try:
                tutores = linesInfo[linesInfo.index("Persona(s) orientada(s):")+2]
                tutores = tutores[23:]
            except:
                tutores = ""
            #Año
            AnoEvento = linesInfo[lineaClave+4]
            AnoEvento = AnoEvento[0:-1]
            
            #Area
            try:
                Area = linesInfo[linesInfo.index("Areas:")+1]
            except:
                Area = ""
            
            articulo = [investigador, NombreProducto, tipo, tutores,lugar, estado, programa,
                DirigidoComo, PersonaOrientada, AnoEvento, Area ]
            self.articulos.append(articulo)
        
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def SaveArticulos(self,fname):
        """
        Guarda los articulos en un archivo csv
        """
        encabezado=["Investigador","Nombre del producto", "Tipo", "Tutor(es)/cotutor(es)", "Lugar",
        "Estado", "Programa", "Dirigido como:", "Persona(s) orientada(s):","Año de inicio del trabajo", 
        "Area:"]
        datos=[encabezado]+self.articulos
        with open( fname,'w', encoding="UTF-8") as f:
            writer = csv.writer(f, delimiter=',',quotechar='"')
            for row in datos:
                writer.writerow(row)
    
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def ExtraerTag(self,soup,ruta):
        """
        Extrae un un tag siguiendo la ruta de nodos en orden descendente, si 
        reverse está activado la ruta indica como ascender en el arbol
        """
        tagResultado = soup
        for tagName in ruta:
            tagResultado = tagResultado.find(tagName)
            #print("  tag:",tagName)
            if tagResultado == None:
                break
        return tagResultado
