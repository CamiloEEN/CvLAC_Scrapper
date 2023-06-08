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

            elif nombreSec != None and nombreSec == "Capitulos de libro":
                self.ProcesaSecLibros(sec, nombreInvestigador)

    def ProcesaSecLibros(self, sec,investigador):
        """
        Procesa la sección de Capítulos de Libros
        """
        # Contenedor con la información de cada libro junto con el tipo
        contInfo = sec.findAll("blockquote")
        
        libro=[]
        for i in range(0, len(contInfo)):
            info_libro = contInfo[i].text
            
            #Nombre Libro
            linesInfo = [ l.strip() for l in info_libro.split("\n")]
            linesInfo = [ l for l in linesInfo if len(l)>0]
            #print(linesInfo)

            #Contiene la información del tipo de producto
            tipo = linesInfo[0]
            tipo = tipo[6:]

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
            

            #NombreProducto = info_articulo[index1:index2]
            #print("\n linesInfo:")
            #for l in linesInfo:
            #    print(l)
            #print("Nombre Producto", NombreProducto)
            #Tipo Capitulo de libro
            if tipo == "Capítulo de libro":
                tipo = "Capítulo de libro"
            elif tipo == "Otro capítulo de libro publicado":
                tipo = "Otro capítulo de libro publicado"
            else:
                print ("ALERTA: Revisar el archivo Capítulos Libros.log")
            #Coautores
            coautores = ", ".join(listaAutores)
            #Lugar
            lugar = linesInfo[lineaClave+2]
            lugar = lugar[6:]
            #Editorial
            editorial = linesInfo[lineaClave+4]
            editorial = editorial[3:]
            #Libro Completo
            LibroCompleto = linesInfo[lineaClave+1]
            #ISBN
            ISBN = linesInfo[lineaClave+3]
            ISBN = ISBN[6:]
            #Año
            AnoEvento = linesInfo[lineaClave+8]
            AnoEvento = AnoEvento[1:]
            if (not AnoEvento.isnumeric()):
                AnoEvento = linesInfo[lineaClave+9]
                AnoEvento = AnoEvento[1:]
            #Volumen
            Volumen = linesInfo[lineaClave+5]
            Volumen = Volumen[3:]
            #Paginas
            Paginas = linesInfo[lineaClave+6]+linesInfo[lineaClave+7]
            Paginas = Paginas[4:]
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
            

            
            libro = [investigador, NombreProducto, tipo, coautores,lugar, LibroCompleto , editorial,
                ISBN, AnoEvento, Volumen, Paginas, Palabras, Area, Sectores]
            self.libros.append(libro)
        
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def SaveCapDeLibros(self,fname):
        """
        Guarda los articulos en un archivo csv
        """
        encabezado=["Investigador","Nombre del producto", "Tipo", "Autores", "Lugar", "Libro",
        "Editorial", "ISBN", "Año", "Volumen", "Páginas", "Palabras","Área", "Sectores"]
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
