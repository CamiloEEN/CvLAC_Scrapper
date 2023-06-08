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

            elif nombreSec != None and nombreSec == "Normas y Regulaciones":
                self.ProcesaSecNormasYRegulaciones(sec, nombreInvestigador)

    def ProcesaSecNormasYRegulaciones(self, sec,investigador):
        """
        Procesa la sección de Normas y Regulaciones
        """
        # Contenedor con la información de cada Normas y Regulaciones
        contInfo = sec.findAll("blockquote")
        # contenedor con los títulos con el tipo del Normas y Regulaciones
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
                lineaClave=linesInfo.index("Nombre comercial: ,")
            except:
                lineaClave=2

            NombreProducto = linesInfo[lineaClave-1]
            NombreProducto = NombreProducto[0:-1]

            for i in range(0,lineaClave-1):
                listaAutores.append(linesInfo[i])
            
            print(linesInfo)
            if tipo.strip() == "Producción técnica - Regulación, norma, reglamento o legislación - Ambiental o de Salud":
                tipo = "61"
            elif tipo.strip() == "Producción técnica - Regulación, norma, reglamento o legislación - Educativa":
                tipo = "62"
            elif tipo.strip() == "Producción técnica - Regulación, norma, reglamento o legislación - Social":
                tipo = "63"
            elif tipo.strip() == "Producción técnica - Regulación, norma, reglamento o legislación - Técnica":
                tipo = "64"
            elif tipo.strip() == "Producción técnica - Regulación, norma, reglamento o legislación - Guía de práctica clínica":
                tipo = "65"
            elif tipo.strip() == "Producción técnica - Regulación, norma, reglamento o legislación - Proyecto de ley":
                tipo = "66"
            elif tipo.strip() == "Producción técnica - Regulación, norma, reglamento o legislación - Técnica - Básica":
                tipo = "74"
            elif tipo.strip() == "Producción técnica - Regulación, norma, reglamento o legislación - Técnica - Ensayo":
                tipo = "75"
            elif tipo.strip() == "Producción técnica - Regulación, norma, reglamento o legislación - Técnica - Proceso":
                tipo = "77"
            elif tipo.strip() == "Producción técnica - Regulación, norma, reglamento o legislación - Técnica - Proceso":
                tipo = "128"
            else:
                print ("ALERTA: Tipo de norma o regulación desconocido")
            #Coautores
            coautores = ", ".join(listaAutores)
            #Lugar
            lugar = linesInfo[lineaClave+2]
            lugar = lugar[6:-1]
            #Nombre Comercial
            NombreComercial = linesInfo[lineaClave]
            #Contrato o registro
            ContratoORegistro = linesInfo[lineaClave+1]
            #Año
            AnoEvento = linesInfo[lineaClave+3]
            AnoEvento = AnoEvento[1:-1]

            #Edicion
            Edicion = linesInfo[lineaClave+4]
            
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
           
            
            articulo = [investigador, NombreProducto, tipo, coautores,lugar, NombreComercial, ContratoORegistro,
                AnoEvento, Edicion,Palabras, Area, Sectores]
            self.productos.append(articulo)
        
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def SaveNormasYRegulaciones(self,fname):
        """
        Guarda los articulos en un archivo csv
        """
        encabezado=["Investigador","Nombre del producto", "Tipo", "Autores", "Lugar",
        "Nombre Comercial", "Contrato o Registro","Año", "Edición", "Palabras", "Area", "Sectores"]
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
