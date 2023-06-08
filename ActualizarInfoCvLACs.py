# El programa CvLACpyExtractArticulos fue creado por Carlos Antonio Jacanamejoy Jamioy y
# sus modificaciones y derivados CvLACpyExtract(tipo de producto) fueron creados por
# Camilo Eduardo Echeverry Naranjo con fines de Acreditación y para uso exclusivo de la
# Universidad de Ibagué. Reservados todos los derechos por la Universidad de Ibagué.

import os
import subprocess
import shutil

#Proceso de extracción de información
#--------------------------------------------------------------------------------------------------------------

#Extrae Información de artículos
os.chdir('CvLACpyExtractArticulos')
subprocess.call("python main.py", shell=True)
os.chdir("..")

try:
    shutil.copy2('CvLACpyExtractArticulos/Output/articulos.csv','CvLACResults/articulos.csv')
    print('articulos copiados con éxito')
except:
    print('No se pudo copiar el archivo articulos.csv')

#Extrae Información de capítulos de libro
os.chdir('CvLACpyExtractCapDeLibros')
subprocess.call("python main.py", shell=True)
os.chdir("..")

try:
    shutil.copy2('CvLACpyExtractCapDeLibros/Output/capitulos_de_libros.csv','CvLACResults/capitulos_de_libros.csv')
    print('capitulos_de_libros copiados con éxito')
except:
    print('No se pudo copiar el archivo capitulos_de_libros.csv')

#Extrae Información de Diseños Industriales
os.chdir('CvLACpyExtractDisenosIndustriales')
subprocess.call("python main.py", shell=True)
os.chdir("..")

try:
    shutil.copy2('CvLACpyExtractDisenosIndustriales/Output/Diseños_Industriales.csv','CvLACResults/Diseños_Industriales.csv')
    print('capitulos_de_libros copiados con éxito')
except:
    print('No se pudo copiar el archivo Diseños_Industriales.csv')

#Extrae Información de Documentos de trabajo
os.chdir('CvLACpyExtractDocumentosDeTrabajo')
subprocess.call("python main.py", shell=True)
os.chdir("..")

try:
    shutil.copy2('CvLACpyExtractDocumentosDeTrabajo/Output/Documentos_de_trabajo.csv','CvLACResults/Documentos_de_trabajo.csv')
    print('Documentos_de_trabajo copiados con éxito')
except:
    print('No se pudo copiar el archivo Documentos_de_trabajo.csv')

#Extrae Información de Estrategias de fomento de CTel
os.chdir('CvLACpyExtractEstrFomentoCTI')
subprocess.call("python main.py", shell=True)
os.chdir("..")

try:
    shutil.copy2('CvLACpyExtractEstrFomentoCTI/Output/Estrategias_de_fomento_de_las_CTI.csv','CvLACResults/Estrategias_de_fomento_de_las_CTI.csv')
    print('Estrategias_de_fomento_de_las_CTI copiados con éxito')
except:
    print('No se pudo copiar el archivo Estrategias_de_fomento_de_las_CTI.csv')

#Extrae Información de Eventos
os.chdir('CvLACpyExtractEventos')
subprocess.call("python main.py", shell=True)
os.chdir("..")

try:
    shutil.copy2('CvLACpyExtractEventos/Output/Eventos.csv','CvLACResults/Eventos.csv')
    print('Eventos copiados con éxito')
except:
    print('No se pudo copiar el archivo Eventos.csv')

#Extrae Información de Formación Académica
os.chdir('CvLACpyExtractEventos')
subprocess.call("python main.py", shell=True)
os.chdir("..")

try:
    shutil.copy2('CvLACpyExtractFormacionAcademica/Output/Formacion_Academica.csv','CvLACResults/Formacion_Academica.csv')
    print('Formacion_Academica copiados con éxito')
except:
    print('No se pudo copiar el archivo Formacion_Academica.csv')


#Extrae Información de informes de investigacion
os.chdir('CvLACpyExtractIformesDeInvestigacion')
subprocess.call("python main.py", shell=True)
os.chdir("..")

try:
    shutil.copy2('CvLACpyExtractIformesDeInvestigacion/Output/Informes_de_investigación.csv','CvLACResults/Informes_de_investigación.csv')
    print('Informes_de_investigación copiados con éxito')
except:
    print('No se pudo copiar el archivo Informes_de_investigación.csv')

#Extrae Información de Jurados
os.chdir('CvLACpyExtractJurados')
subprocess.call("python main.py", shell=True)
os.chdir("..")

try:
    shutil.copy2('CvLACpyExtractJurados/Output/Participacion_como_jurados.csv','CvLACResults/Participacion_como_jurados.csv')
    print('Participacion_como_jurados copiados con éxito')
except:
    print('No se pudo copiar el archivo Participacion_como_jurados.csv')

#Extrae Información de Libros
os.chdir('CvLACpyExtractLibros')
subprocess.call("python main.py", shell=True)
os.chdir("..")

try:
    shutil.copy2('CvLACpyExtractLibros/Output/libros.csv','CvLACResults/libros.csv')
    print('libros copiados con éxito')
except:
    print('No se pudo copiar el archivo libros.csv')

#Extrae Información de Lineas de investigación
os.chdir('CvLACpyExtractLineasDeInvestigacion')
subprocess.call("python main.py", shell=True)
os.chdir("..")

try:
    shutil.copy2('CvLACpyExtractLineasDeInvestigacion/Output/Lineas.csv','CvLACResults/Lineas.csv')
    print('Lineas copiados con éxito')
except:
    print('No se pudo copiar el archivo Lineas.csv')

#Extrae Información de Normas y Regulaciones
os.chdir('CvLACpyExtractNormasYRegulaciones')
subprocess.call("python main.py", shell=True)
os.chdir("..")

try:
    shutil.copy2('CvLACpyExtractNormasYRegulaciones/Output/Normas_y_Regulaciones.csv','CvLACResults/Normas_y_Regulaciones.csv')
    print('Normas_y_Regulaciones copiados con éxito')
except:
    print('No se pudo copiar el archivo Normas_y_Regulaciones.csv')


#Extrae Información de Plantas Piloto
os.chdir('CvLACpyExtractPlantaPiloto')
subprocess.call("python main.py", shell=True)
os.chdir("..")

try:
    shutil.copy2('CvLACpyExtractPlantaPiloto/Output/Plantas_Piloto.csv','CvLACResults/Plantas_Piloto.csv')
    print('Plantas_Piloto copiados con éxito')
except:
    print('No se pudo copiar el archivo Plantas_Piloto.csv')

#Extrae Información de Prototipos
os.chdir('CvLACpyExtractPrototipos')
subprocess.call("python main.py", shell=True)
os.chdir("..")

try:
    shutil.copy2('CvLACpyExtractPrototipos/Output/Prototipos.csv','CvLACResults/Prototipos.csv')
    print('Prototipos copiados con éxito')
except:
    print('No se pudo copiar el archivo Prototipos.csv')

#Extrae Información de Proyectos
os.chdir('CvLACpyExtractProyectos')
subprocess.call("python main.py", shell=True)
os.chdir("..")

try:
    shutil.copy2('CvLACpyExtractProyectos/Output/Proyectos.csv','CvLACResults/Proyectos.csv')
    print('Proyectos copiados con éxito')
except:
    print('No se pudo copiar el archivo Proyectos.csv')

#Extrae Información de Publicaciones No Cientificas
os.chdir('CvLACpyExtractPublicacionesNoCientificas')
subprocess.call("python main.py", shell=True)
os.chdir("..")

try:
    shutil.copy2('CvLACpyExtractPublicacionesNoCientificas/Output/Publicaciones_No_Cientificas.csv','CvLACResults/Publicaciones_No_Cientificas.csv')
    print('Publicaciones_No_Cientificas copiados con éxito')
except:
    print('No se pudo copiar el archivo Publicaciones_No_Cientificas.csv')

#Extrae Información de Signos Distintivos
os.chdir('CvLACpyExtractSignosDistintivos')
subprocess.call("python main.py", shell=True)
os.chdir("..")

try:
    shutil.copy2('CvLACpyExtractSignosDistintivos/Output/Signos_distintivos.csv','CvLACResults/Signos_distintivos.csv')
    print('Signos_distintivos copiados con éxito')
except:
    print('No se pudo copiar el archivo Signos_distintivos.csv')

#Extrae Información de Softwares
os.chdir('CvLACpyExtractSoftwares')
subprocess.call("python main.py", shell=True)
os.chdir("..")

try:
    shutil.copy2('CvLACpyExtractSoftwares/Output/Softwares.csv','CvLACResults/Softwares.csv')
    print('Softwares copiados con éxito')
except:
    print('No se pudo copiar el archivo Softwares.csv')

#Extrae Información de Trabajos Dirigidos
os.chdir('CvLACpyExtractTrabajosDirigidos')
subprocess.call("python main.py", shell=True)
os.chdir("..")

try:
    shutil.copy2('CvLACpyExtractTrabajosDirigidos/Output/Trabajos_de_Grado.csv','CvLACResults/Trabajos_de_Grado.csv')
    print('Trabajos_de_Grado copiados con éxito')
except:
    print('No se pudo copiar el archivo Trabajos_de_Grado.csv')

