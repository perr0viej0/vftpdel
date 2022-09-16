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