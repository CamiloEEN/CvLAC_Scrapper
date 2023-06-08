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
        self.libros=[]
        
        
    
    
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

            elif nombreSec != None and nombreSec == "Signos distintivos":
                self.ProcesaSecSignosDist(sec, nombreInvestigador)

    def ProcesaSecSignosDist(self, sec,investigador):
        """
        Procesa la sección de Signos distintivos
        """
        # Contenedor con la información de cada Signos distintivo junto con el tipo
        contInfo = sec.findAll("blockquote")
        
        proyecto=[]
        for i in range(0, len(contInfo)):
            info_proyecto = contInfo[i].text
            
            #Nombre Libro
            linesInfo = [ l.strip() for l in info_proyecto.split("\n")]
            linesInfo = [ l for l in linesInfo if len(l)>0]
            print(linesInfo)

            #Contiene la información del tipo de producto
            tipo = linesInfo[0]
            tipo = tipo.replace("\xa0"," ")

            NombreProducto=linesInfo[1]

            try:
                lineaClave = linesInfo.index("Resumen")
            except:
                lineaClave = 0

            if tipo == "Tipo de proyecto: Investigación y desarrollo":
                tipo = "Tipo de proyecto: Investigación y desarrollo"
            elif tipo == "Tipo de proyecto: Investigación y creación":
                tipo = "Tipo de proyecto: Investigación y creación"
            else:
                print ("ALERTA: Tipo de proyecto no reconocido.log")
            #Lugar
            lugar = linesInfo[1]
            lugar = lugar[3:]
            

            
            
            #Año
            AnoEvento = linesInfo[2]
            AnoEvento = AnoEvento.split("\xa0")
            AnoEvento = AnoEvento[0]
            #Fin

            #Registro
            registro=linesInfo[2]
            registro = registro.split("\xa0")
            registro = registro[-1]

            #Resumen
            Titular = linesInfo[-1].split("\xa0")
            Titular = Titular[-1]
            

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
            

            
            proyecto = [investigador, NombreProducto, tipo,lugar, AnoEvento , registro,
                Titular, Palabras, Area, Sectores]
            self.libros.append(proyecto)
        
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def SaveSignosDist(self,fname):
        """
        Guarda los articulos en un archivo csv
        """
        encabezado=["Investigador","Signo distintivo", "Tipo", "Lugar", "Año",
        "Registro", "Titular", "Palabras","Área", "Sectores"]
        datos=[encabezado]+self.libros
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
