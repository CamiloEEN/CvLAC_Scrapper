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

            elif nombreSec != None and nombreSec == "Documentos de trabajo":
                self.ProcesaSecDocTrabajos(sec, nombreInvestigador)

    def ProcesaSecDocTrabajos(self, sec,investigador):
        """
        Procesa la sección de Documentos de trabajo
        """
        # Contenedor con la información de cada Documento de trabajo
        contInfo = sec.findAll("blockquote")
        # contenedor con el tipo del Documentos de trabajo
        contTipo = sec.findAll("b") 
        contTipo = [ l for l in contTipo if "Palabras:" not in l.text]
        
        libro=[]
        for i in range(0, len(contInfo)):
            tipo = contTipo[i].text
            tipo = tipo.replace("Producción bibliográfica -","")
            info_libro = contInfo[i].text

            
            #Nombre Libro
            linesInfo = [ l.strip() for l in info_libro.split("\n")]
            linesInfo = [ l for l in linesInfo if len(l)>0]
            #print(linesInfo)
            NombreProducto=""
            listaAutores=[]
            lineaClave=-1
            for i, l in enumerate(linesInfo):
                if l[-1]==',':
                    listaAutores.append(l[:-1])
                if  l[0] == '"':
                    NombreProducto = l[1:-1]
                    lineaClave = i
                    break
           
            #Coautores
            coautores = ", ".join(listaAutores)
            #Lugar
            lugar = linesInfo[lineaClave+1]
            lugar = lugar[4:]
           
            #Año
            AnoEvento = linesInfo[lineaClave+2]
            AnoEvento = AnoEvento[0:-1]
        
            #Paginas
            Paginas = [ l for l in linesInfo if "p." in l]
            Paginas = Paginas[0]
            Paginas = Paginas.replace("p.","")
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
            

            
            libro = [investigador, NombreProducto, tipo, coautores,lugar, AnoEvento, Paginas, Palabras, Area]
            self.libros.append(libro)
        
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def SaveDocTrabajos(self,fname):
        """
        Guarda los articulos en un archivo csv
        """
        encabezado=["Investigador","Nombre del producto", "Tipo", "Autores", "Lugar",
         "Año",  "Páginas", "Palabras","Área"]
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
