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

            elif nombreSec != None and nombreSec == "Proyectos":
                self.ProcesaSecProyectos(sec, nombreInvestigador)

    def ProcesaSecProyectos(self, sec,investigador):
        """
        Procesa la sección de Proyectos
        """
        # Contenedor con la información de cada Proyecto junto con el tipo
        contInfo = sec.findAll("blockquote")
        
        proyecto=[]
        for i in range(0, len(contInfo)):
            info_proyecto = contInfo[i].text
            
            #Nombre Libro
            linesInfo = [ l.strip() for l in info_proyecto.split("\n")]
            linesInfo = [ l for l in linesInfo if len(l)>0]
            #print(linesInfo)

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
            #Inicio
            inicio = linesInfo[2]
            inicio = inicio[8:]
            inicio += " "+linesInfo[3]

            Anoinicio = inicio[-4:]
            
            #Duración
            duracion = linesInfo[lineaClave-1]
            duracion = duracion.replace("\xa0"," ")
            duracion = duracion[8:]
            #Fin
            if linesInfo[3]==linesInfo[lineaClave-2]:
                fin = ""
                Anofin = ""
            else:
                fin = linesInfo[lineaClave-3]
                #print(linesInfo[lineaClave-3])
                fin = fin[5:]
                fin += " "+linesInfo[lineaClave-2]
                Anofin = fin[-4:]

            #Resumen
            resumen = ""
            for i in range(lineaClave+1,len(linesInfo)):
                resumen += " "+linesInfo[i]

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
            

            
            proyecto = [investigador, NombreProducto, tipo,inicio,Anoinicio, duracion , fin,Anofin,
                resumen, Palabras, Area, Sectores]
            self.libros.append(proyecto)
        
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def SaveProyectos(self,fname):
        """
        Guarda los articulos en un archivo csv
        """
        encabezado=["Investigador","Nombre del proyecto", "Tipo", "Inicio","Año de inicio", "Duración",
        "Fin","Año de finalización", "Resumen", "Palabras","Área", "Sectores"]
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
