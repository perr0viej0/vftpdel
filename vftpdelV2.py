#!/usr/bin/python3
# vftpdel V2- borra todos los archivos de un directorio en un servidor ftps
# uso: vftpdel server puerto user password ruta opcion
# opciones:
#           -s: simple, borra todos los archivos de la ruta, ignorando subdirectorios
#           -r: recursivo, borra todos los archivos de la ruta y de todos los subdirectorios
#           -t: total, borra todos los archivos y subdirectorios de la ruta
#
from ftplib import FTP_TLS
import ftputil
import ftputil.session
import sys
import ssl


# FUNCIONES
my_session_factory = ftputil.session.session_factory(       # definimos nuestra session_factory para poder pasar
                       base_class=FTP_TLS,                  # argumentos a nuestra conexion ftps
                       port=int(sys.argv[2]),
                       encrypt_data_channel=True,           # equivalente a prop_p en ftplib
                       encoding="UTF-8",
                       debug_level=0)

def borraftprec(server, user, passwd, path):
    sys.stdout = open('vftpdel.log', 'w')                   # pasamos stdout a un fichero
    print(getwelcome(), "\n")                               # obtenemos el welcome del server
    ftp = ftputil.FTPHost(server, user, passwd, session_factory=my_session_factory)
    ftp.chdir(path)                             # Creamos conexion y nos movemos a path remoto
    print("DIRECTORIO DE TRABAJO:\n")
    print(ftp.getcwd(), "\n")
    print("CONTENIDO DEL ARBOL:\n")
    for root,dirs, files in ftp.walk(ftp.getcwd()):     # caminamos por el arbol
        for x in files:
            print(ftp.path.join(root,x))
            ftp.remove(ftp.path.join(root, x))
    print("\nCONTENIDO DEL ARBOL TRAS EL BORRADO:\n")
    print(ftp.getcwd(),"->")
    for x in ftp.listdir(ftp.getcwd()):
        print(x)
    for root, dirs, files in ftp.walk(ftp.getcwd()):
        for x in dirs:
            print(ftp.path.join(root,x),"->")
            for y in ftp.listdir(ftp.path.join(root, x)):
                print(y)
    print()
    ftp.close()
    sys.stdout.close()

def borraftptotal(server, user, passwd, path):
    sys.stdout = open('vftpdel.log', 'w')
    print(getwelcome(), "\n")
    ftp = ftputil.FTPHost(server, user, passwd, session_factory=my_session_factory)
    ftp.chdir(path)
    print("DIRECTORIO DE TRABAJO:\n")
    print(ftp.getcwd(), "\n")
    print("CONTENIDO DEL ARBOL:\n")
    for root,dirs, files in ftp.walk(ftp.getcwd(), topdown=False):  # caminamos por el arbol al reves, de lo mas
        for x in files:                                             # profundo hacia los superiores
            print(ftp.path.join(root,x))                            # eliminamos ficheros
            ftp.remove(ftp.path.join(root, x))
        for x in dirs:                                              # eliminados los ficheros, eliminamos directorio
            print(ftp.path.join(root,x))
            ftp.rmdir(ftp.path.join(root,x))
    print("\nCONTENIDO DEL ARBOL TRAS EL BORRADO:\n")
    print(ftp.getcwd(), "->")
    for x in ftp.listdir(ftp.getcwd()):
        print(x)
    for root, dirs, files in ftp.walk(ftp.getcwd()):    # aseguramos q esta bien borrado
        for x in dirs:
            print(ftp.path.join(root, x), "->")
            for y in ftp.listdir(ftp.path.join(root, x)):
                print(y)
    print()
    ftp.close()
    sys.stdout.close()

def borraftp(server, user, passwd, path):
    sys.stdout = open('vftpdel.log', 'w')
    print(getwelcome(),"\n")
    ftp = ftputil.FTPHost(server, user, passwd, session_factory=my_session_factory)
    ftp.chdir(path)
    print("DIRECTORIO DE TRABAJO:\n")
    print(ftp.getcwd(),"\n")
    print("CONTENIDO DEL DIRECTORIO:")
    for files in ftp.listdir(ftp.getcwd()):
        try:
            str(files)
            print(files)
            ftp.remove(files)
        except ftputil.error.PermanentError:        # si es una carpeta, ignora
            pass
    print("CONTENIDO DEL DIRECTORIO TRAS EL BORRADO:")
    for x in ftp.listdir(ftp.getcwd()):
        print(x)
    ftp.close()
    sys.stdout.close()

def getwelcome():
    ftp = FTP_TLS()     # conectamos por ftplib para obtener el welcome y guardarlo en el log
    ftp.ssl_version = ssl.PROTOCOL_TLSv1_2  # obj ftp_tls y ssl
    ftp.connect(sys.argv[1], int(sys.argv[2]))
    ftp.login(sys.argv[3], sys.argv[4])
    ftp.prot_p()                # encriptamos conexion
    x = ftp.getwelcome()
    ftp.quit()
    return x            # devolvemos el welcome
# FIN FUNCIONES
opciones=["-r", "-s","-t"]

if len(sys.argv) < 7:           # si no estan todos los parametros, help ayudame!
    print("ERROR: Faltan parametros")
    print("USO: vftpdel servidor puerto usuario password directorio opcion")
    print("Ej.: vftpdel servidor.ftp 21 usuario password /ruta/a/borrar -r")
    print("\nOpciones validas: -r, -s, -t")
    print("-r: recursivo, borra todos los archivos de la ruta, ignorando subdirectorios")
    print("-s: simple, borra todos los archivos de la ruta, ignorando subdirectorios")
    print("-t: total, borra todos los archivos y subdirectorios de la ruta")
    print("\nLos resultados de la operacion se guardan en vftpdel.log")
    sys.exit()
elif sys.argv[6] not in opciones:   # si el comando esta mal te los recuerdo
    print("ERROR: opcion no reconocida.\nOpciones validas: -r, -s, -t")
    sys.exit()
elif sys.argv[6] == "-r":
    borraftprec(sys.argv[1],  sys.argv[3], sys.argv[4], sys.argv[5])
    sys.exit()
elif sys.argv[6] == "-s":
    borraftp(sys.argv[1], sys.argv[3], sys.argv[4], sys.argv[5])
    sys.exit()
elif sys.argv[6] == "-t":
    borraftptotal(sys.argv[1], sys.argv[3], sys.argv[4], sys.argv[5])
    sys.exit()

