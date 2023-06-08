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

            elif nombreSec != None and nombreSec == "Textos en publicaciones no científicas":
                self.ProcesaSecTextPubNoCientificas(sec, nombreInvestigador)

    def ProcesaSecTextPubNoCientificas(self, sec,investigador):
        """
        Procesa la sección de artículos no cientificos
        """
        # Contenedor con la información de cada artículo
        contInfo = sec.findAll("blockquote")
        # contenedor con los títulos con el tipo del artículo
        contTipo = sec.findAll("li") 
        
        articulos=[]
        for i in range(0, len(contInfo)):
            tipo = contTipo[i].text
            info_articulo = contInfo[i].text
            
            #Nombre Articulo
            linesInfo = [ l.strip() for l in info_articulo.split("\n")]
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
            
            #NombreProducto = info_articulo[index1:index2]
            #print("\n linesInfo:")
            #for l in linesInfo:
            #    print(l)
            #print("Nombre Producto", NombreProducto)
            #Tipo Artículo
            if tipo.strip() == "Producción bibliográfica - Otro artículo publicado - Periódico de noticias":
                tipo = "22"
            elif tipo.strip() == "Producción bibliográfica - Otro artículo publicado - Revista de divulgación":
                tipo = "23"
            elif tipo.strip() == "Producción bibliográfica - Otro artículo publicado - Carta al editor":
                tipo = "24"
            elif tipo.strip() == "Producción bibliográfica - Otro artículo publicado - Reseñas de libros":
                tipo = "25"
            elif tipo.strip() == "Producción bibliográfica - Otro artículo publicado - Columna de opinión":
                tipo = "26"
            else:
                print ("ALERTA: Revisar el archivo Textos No Cientificos.log")
            #Coautores
            coautores = ", ".join(listaAutores)
            #Lugar
            lugar = linesInfo[lineaClave+1]
            lugar = lugar[4:]
            #Editorial
            editorial = linesInfo[lineaClave+4]
            #DOI
            #doi = linesInfo[lineaClave+6]
            #ISSN
            ISSN = linesInfo[lineaClave+4]
            ISSN = ISSN[6:]
            #Nombre Revista
            Revista = linesInfo[lineaClave+3]
            #Año
            AnoEvento = linesInfo[lineaClave+2]
            AnoEvento = AnoEvento[0:-1]
            #Volumen
            Volumen = linesInfo[-1]
            Volumen = Volumen[2:] 
            #Fasciculo
            #fasciculo = linesInfo[-1]
            #Páginas

            Pagini = linesInfo[-3]
            Pagini = Pagini[2:]

            Pagfin = linesInfo[-2]
            Pagfin = Pagfin[2:] 
            
            articulo = [investigador, NombreProducto, tipo, coautores,lugar, editorial, 
                ISSN, Revista, AnoEvento, Volumen, Pagini,Pagfin]
            self.articulos.append(articulo)
        
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def SavePubNoCientificas(self,fname):
        """
        Guarda los articulos en un archivo csv
        """
        encabezado=["Investigador","Nombre del producto", "Tipo", "Autores", "Lugar",
        "Editorial", "ISSN", "Revista","Año", "Volumen",
        "Página inicial","Página final"]
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
