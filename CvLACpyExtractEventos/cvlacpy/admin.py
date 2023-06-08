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

            elif nombreSec != None and nombreSec == "Eventos científicos":
                self.ProcesaSecEventos(sec, nombreInvestigador)

    def ProcesaSecEventos(self, sec,investigador):
        """
        Procesa la sección de Eventos científicos
        """
        # Contenedor con la información de cada Evento junto con el tipo
        contInfo = sec.findAll("table")
        
        libro=[]
        for i in range(0, len(contInfo)):
            info_evento = contInfo[i].text.replace("\xa0"," ")
            
            #Nombre Libro
            linesInfo = [ l.strip() for l in info_evento.split("\n")]
            linesInfo = [ l for l in linesInfo if len(l)>0]
            #print(linesInfo)

            #Contiene la información del tipo de producto
            tipo = linesInfo[1]

            NombreEvento = linesInfo[0]
            NombreEvento = NombreEvento[NombreEvento.index("evento:")+8:]


            listaAutores=[]
            lineaClave=1
            
            

            #NombreProducto = info_articulo[index1:index2]
            #print("\n linesInfo:")
            #for l in linesInfo:
            #    print(l)
            #print("Nombre Producto", NombreProducto)
            #Tipo Capitulo de libro
            if tipo == "Tipo de evento: Otro":
                tipo = tipo[15:]
            elif tipo == "Tipo de evento: Taller":
                tipo = tipo[15:]
            elif tipo == "Tipo de evento: Congreso":
                tipo = tipo[15:]
            elif tipo == "Tipo de evento: Encuentro":
                tipo = tipo[15:]
            elif tipo == "Tipo de evento: Seminario":
                tipo = tipo[15:]
            elif tipo == "Tipo de evento: Simposio":
                tipo = tipo[15:]
            else:
                print ("ALERTA: tipo de producto no reconocido")
            #Coautores
            coautores = ", ".join(listaAutores)
            #Ámbito
            ambito = linesInfo[lineaClave+1]
            ambito = ambito[8:]
            #Año
            AnoEvento = linesInfo[lineaClave+2]
            AnoEvento = AnoEvento[13:17]
            #Lugar
            if(linesInfo[lineaClave+4][0:3]=="en "):
                lugar = linesInfo[lineaClave+4]
                lineaClave = lineaClave+4 
            else:
                lugar = linesInfo[lineaClave+3]
                lineaClave = lineaClave+3

            lugar = lugar[3:]
            #Productos asociados
            try:
                ProducAsociados = ""
                lineaClaveProductos=linesInfo.index("Productos asociados")
                for l in linesInfo:
                    if("Nombre del producto:" in l):
                        ProducAsociados+=l[20:]+": "
                    if("Tipo de producto:" in l):
                        ProducAsociados+=l[17:]+"\n"
            except:
                ProducAsociados = "Ninguno"
            
            #Instituciones asociadas
            try:
                InstitucAsociadas = ""
                lineaClaveInstituciones=linesInfo.index("Instituciones asociadas")
                for l in linesInfo:
                    if("Nombre de la institución:" in l):
                        InstitucAsociadas+=l[25:]+": "
                    if("Tipo de vinculación" in l):
                        InstitucAsociadas+=l[19:]+"\n"
            except:
                InstitucAsociadas = "Ninguno"
            
            
            #Instituciones asociadas
            try:
                participantes = ""
                lineaClaveParticipantes=linesInfo.index("Participantes")
                for l in linesInfo:
                    if("Nombre:" in l):
                        participantes+=l[8:]+": "
                    if("Rol en el evento:" in l):
                        participantes+=l[18:]+"\n"
            except:
                participantes = "No registrado"

            
            libro = [investigador, NombreEvento, tipo, lugar, ambito , ProducAsociados,
                InstitucAsociadas, participantes, AnoEvento]
            self.libros.append(libro)
        
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def SaveEventos(self,fname):
        """
        Guarda los articulos en un archivo csv
        """
        encabezado=["Investigador","Nombre del evento", "Tipo",  "Lugar", "Ámbito",
        "Productos asociados", "Instituciones asociadas","Participantes" ,"Año"]
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
