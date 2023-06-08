# Archivo principal

import os
import argparse

from cvlacpy import getCvlacsDirs, Admin
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--file", required = False,
        help="Arcivo excel con las url de los CvLAC (*.xlsx)."
        +" Por defecto toma el archivo './Input/consulta.xlsx'.",
        default="./Input/consulta.xlsx")
    parser.add_argument("-o", "--out", required=False, help='Nombre del '+
    'resultado, no es necesario que se de una extensión', default="Proyectos")
    args = parser.parse_args()
    
    baseInputName, extension = os.path.splitext(args.file)
    extension = extension.lower()
    print("baseInputName:",baseInputName, '  extensión:',extension)
    # Verifica la extensión del archivo de entrada
    if extension != '.xlsx':
        raise Exception(f'El archivo "{args.file}" no es válido, debe tener extension *.xlsx')
    
    if not os.path.isfile(args.file):
        raise Exception(f'No se hallo el archivo "{args.file}".')
    
    admin = Admin(args.file)
    admin.Run()
    admin.SaveProyectos("./Output/%s.csv"%args.out)
    #print("Datos:", admin.cvlacDirs)
    
    print("Hecho!")
    
