import socket
import ssl

host = ""
port = 9898

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations("/home/leon/ssl.pem")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
ssock = context.wrap_socket(sock, server_hostname=host)
ssock.setblocking(True)
ssock.connect((host, 9898))
print("connected")
while True:
    msg = ssock.recv(1024)
    print(msg)
print("done")
