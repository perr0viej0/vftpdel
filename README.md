# vftpdel

Borra todos los archivos en un directorio de un servidor FTPS

- Uso: vfptdel servidor puerto usuario contraseña directorio

-----------------------------------------------
Si el servidor FTPS requiere que la sesion TLS se reutilice en cada "data connection" (como filezilla server), 
es necesario parchear la libreria ftplib.py (/usr/local/lib/python3.8/ftplib.py)

-> EN LINEA 790:
- conn = self.context.wrap_socket(conn, server_hostname=self.host)

Cambiarla por:
- conn = self.context.wrap_socket(conn, server_hostname=self.host, session=self.sock.session)
------------------------------------------------
# vftpdelV2

Borra archivos y/o directorios de un servidor FTPS

- Uso: vftpdelV2 servidor puerto usuario contraseña directorio opcion
- Opciones: 
- - -r: recursivo, borra todos los archivos de la ruta, ignorando subdirectorios
- - -s: simple, borra todos los archivos de la ruta, ignorando subdirectorios
- - -t: total, borra todos los archivos y subdirectorios de la ruta

Los resultados de la operacion se guardan en vftpdel.log

--------------------------------------------------
Requerimientos:
-
- ftplib parcheada
- ftputil 

Instalacion: pip3 install ftputil
