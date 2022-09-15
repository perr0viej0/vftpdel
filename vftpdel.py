#!/usr/bin/python3
# vftpdel - borra todos los archivos de un directorio en un servidor ftps
# uso: vftpdel server puerto user password ruta
from ftplib import FTP_TLS
import ssl
import sys

# FUNCIONES

def borraftp(server, port, user, passwd, path):
    sys.stdout = open('vftpdel.log', 'w')
    ftp = FTP_TLS()
    ftp.ssl_version = ssl.PROTOCOL_TLSv1_2
    #ftp.debugging = 2
    ftp.connect(server, port)
    ftp.login(user, passwd)
    ftp.prot_p()
    ftp.cwd(path)
    print("LISTA DE ARCHIVOS A ELIMINAR\n")
    print(ftp.retrlines('LIST'))
    for cosas in ftp.nlst():
        try:
            ftp.delete(cosas)
        except Exception:
            ftp.cwd(cosas)
            for x in ftp.nlst():
                ftp.delete(x)
            ftp.sendcmd('CDUP')
            ftp.rmd(cosas)
    print("\nCONTENIDO DEL DIRECTORIO DESPUES DE ELIMINAR\n")
    print(ftp.retrlines('LIST'))
    sys.stdout.close()
    ftp.quit()

# FIN FUNCIONES

if len(sys.argv) < 6:
    print("ERROR: Faltan parametros")
    print("USO: vftpdel servidor puerto usuario password directorio")
    print("Ej.: vftpdel servidor.ftp 21 usuario password /ruta/a/borrar")
    sys.exit()
else:

    borraftp(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5])
    sys.exit()