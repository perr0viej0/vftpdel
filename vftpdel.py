#!/usr/bin/python3
# vftpdel - borra todos los archivos de un directorio en un servidor ftps
# uso: vftpdel server puerto user password ruta
from ftplib import FTP_TLS
import ssl
import sys

DEBUG = False
# FUNCIONES

def borraftp(server, port, user, passwd, path):
    sys.stdout = open('vftpdel.log', 'w')   # sacamos stdout a fichero
    ftp = FTP_TLS()
    ftp.ssl_version = ssl.PROTOCOL_TLSv1_2  # obj ftp_tls y ssl
    if DEBUG:
        ftp.debugging = 2
    ftp.connect(server, port)
    ftp.login(user, passwd)
    ftp.prot_p()            # encriptamos conexion
    ftp.cwd(path)           # subimos a path
    print("DIRECTORIO DE TRABAJO:\n")
    print(ftp.pwd(),"\n")
    print("LISTA DE ARCHIVOS A ELIMINAR\n")
    print(ftp.retrlines('LIST'))        # listamos

    for cosas in ftp.nlst():
        try:
            ftp.delete(cosas)       # eliminalo
        except Exception:
            pass                    # excepto si es dir
    print("\nCONTENIDO DEL DIRECTORIO DESPUES DE ELIMINAR\n")
    print(ftp.retrlines('LIST'))
    ftp.quit()
    sys.stdout.close()      # lo ultimo es cerrar stdout, pq si no dara error al intentar escribir en un fichero cerrado
# FIN FUNCIONES

if len(sys.argv) < 6:
    print("ERROR: Faltan parametros")
    print("USO: vftpdel servidor puerto usuario password directorio")
    print("Ej.: vftpdel servidor.ftp 21 usuario password /ruta/a/borrar")
    sys.exit()
else:
    borraftp(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5])
    sys.exit()