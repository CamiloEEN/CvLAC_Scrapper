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
        self.productos=[]
        
        
    
    
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

            elif nombreSec != None and nombreSec == "Informes de investigaci&oacuten":
                self.ProcesaSecInformesInvestigacion(sec, nombreInvestigador)

    def ProcesaSecInformesInvestigacion(self, sec,investigador):
        """
        Procesa la sección de Informes de investigación
        """
        # Contenedor con la información de cada Informe de investigación
        contInfo = sec.findAll("blockquote")
        # contenedor con los títulos con el tipo de Informe de investigación
        contTipo = sec.findAll("li") 
        
        articulos=[]
        for i in range(0, len(contInfo)):
            tipo = contTipo[i].text
            info_articulo = contInfo[i].text
            
            #Nombre Normas o Regulaciones
            linesInfo = [ l.strip() for l in info_articulo.split("\n")]
            linesInfo = [ l for l in linesInfo if len(l)>0]
            NombreProducto=""
            listaAutores=[]
            
            try:
                lineaClave=linesInfo.index(". En: ,")
            except:
                lineaClave=2

            NombreProducto = linesInfo[lineaClave-1]

            for i in range(0,lineaClave-1):
                listaAutores.append(linesInfo[i])
            
            #print(linesInfo)
            if tipo.strip() == "Producción técnica - Informes de investigación":
                tipo = "Por definir"
            else:
                print ("ALERTA: Tipo de informe no reconocido.log")
            #Coautores
            coautores = ", ".join(listaAutores)
            #Lugar
            lugar = linesInfo[lineaClave]
            lugar = lugar.replace(". En:","")
            #Año
            AnoEvento = linesInfo[lineaClave+1]
            AnoEvento = AnoEvento[1:-1]

            
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
           
            
            articulo = [investigador, NombreProducto, tipo, coautores,lugar, 
                AnoEvento, Palabras, Area, Sectores]
            self.productos.append(articulo)
        
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def SaveInformesInvestigacion(self,fname):
        """
        Guarda los articulos en un archivo csv
        """
        encabezado=["Investigador","Nombre del producto", "Tipo", "Autores", "Lugar","Año",  "Palabras", "Aréa", "Sectores"]
        datos=[encabezado]+self.productos
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
