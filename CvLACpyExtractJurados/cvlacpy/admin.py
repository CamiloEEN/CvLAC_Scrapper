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

            elif nombreSec != None and nombreSec == "Jurado en comités de evaluación":
                self.ProcesaSecJurados(sec, nombreInvestigador)

    def ProcesaSecJurados(self, sec,investigador):
        """
        Procesa la sección de Jurado en comités de evaluación
        """
        # Contenedor con la información de cada Jurado en comité de evaluación
        contInfo = sec.findAll("blockquote")
        # contenedor con los títulos con el tipo del Jurado en comité de evaluación
        contTipo = sec.findAll("li") 
        
        articulos=[]
        for i in range(0, len(contInfo)):
            tipo = contTipo[i].text
            tipo = tipo.replace("Datos complementarios -","")

            info_jurado = contInfo[i].text
            
            #Nombre Articulo
            linesInfo = [ l.strip() for l in info_jurado.split("\n")]
            linesInfo = [ l for l in linesInfo if len(l)>0]
            
            NombreProducto=linesInfo[1]
            NombreProducto = NombreProducto[7:]
            
            lineaClave=0
            
            #NombreProducto = info_articulo[index1:index2]
            #print(linesInfo)
            #for l in linesInfo:
            #    print(l)
            #print("Nombre Producto", NombreProducto)
            #Tipo Artículo
            
            #Jurado
            jurado = linesInfo[0]
            #Lugar

            lugar = linesInfo[lineaClave+3]
            lugar = lugar[4:]
            #lugar = lugar.replace(":"," ")

            #Programa académico
            programa = linesInfo[lineaClave+4]
            programa = programa.replace("programa académico","")
            
            #Estudiante orientado
            orientado = linesInfo[lineaClave+5]
            orientado = orientado.replace("Nombre del orientado:","")
            #Año
            AnoEvento = "Esta información no suele aparecer en los CvLACs"
            

            #Palabras
            try:
                Palabras = linesInfo[linesInfo.index("Palabras:")+1]
            except:
                Palabras = ""
            #Area
            try:
                Area = linesInfo[linesInfo.index("Areas:")+1]
            except:
                Area = ""
            #Sectores
            try:
                Sectores = linesInfo[linesInfo.index("Sectores:")+1]
            except:
                Sectores = ""
            
            articulo = [investigador, NombreProducto, tipo, jurado,lugar, programa, orientado,
                 AnoEvento, Palabras,Area,Sectores]
            self.articulos.append(articulo)
        
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def SaveJurados(self,fname):
        """
        Guarda los articulos en un archivo csv
        """
        encabezado=["Investigador","Nombre del producto", "Tipo", "Jurado", "Lugar",
        "Programa", "Orientado", "Año", "Palabras","Area","Sectores"]
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
