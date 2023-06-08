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
        print(urlCvlac)
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

            elif nombreSec != None and nombreSec == "Formación Académica":
                self.ProcesaSecFormAcad(sec, nombreInvestigador)

    def ProcesaSecFormAcad(self, sec,investigador):
        """
        Procesa la sección de Formación Académica
        """
        # Contenedor con la información de cada título
        contInfo = sec.findAll("tr")
        # contenedor con los tipos con el tipo del libro
        contTipo = sec.findAll("li") 

        formacion=[]
        for i in range(0, len(contInfo)):
            info_formAcad = contInfo[i].text

            #Nombre Libro
            linesInfo = [ l.strip() for l in info_formAcad.split("\n")]
            linesInfo = [ l for l in linesInfo if len(l)>0]

            try:
                if linesInfo[i]=='Formación Académica':
                    continue
            except:
                continue

            #print(linesInfo)

            NombreFormacion=linesInfo[0]
            if len(linesInfo)<4:
                print('La información registrada está incompleta.')
                tipo = linesInfo[1]
            else:
                tipo = linesInfo[2]

            lineaClave=0
            
            #Lugar
            lugar = linesInfo[lineaClave+1]
            if len(linesInfo)<4:
                lugar = ""
            
            #Año
            try:
                AnoEvento = linesInfo[lineaClave+3]
            except:
                AnoEvento = linesInfo[-1]
            
            #Tesis
            try:
                tesis = linesInfo[lineaClave+4]
            except:
                tesis = "No registrada o está en curso"
                if len(linesInfo)<4:
                    tesis = "Error: puede que la información registrada en el CvLAC no este incompleta"
            
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
            

            
            formacion = [investigador, NombreFormacion, tipo, lugar, AnoEvento, tesis, Palabras, Area]
            self.libros.append(formacion)
        
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def SaveFormAcad(self,fname):
        """
        Guarda los articulos en un archivo csv
        """
        encabezado=["Investigador","Nombre de Formación", "Tipo",  "Lugar",
         "Año", "Trabajo de grado", "Páginas", "Palabras","Área"]
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
