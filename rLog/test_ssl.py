import time
import socket
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(
    '/home/master/ssl.pem', "/home/master/creds/public.key"
)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind(("0.0.0.0", 9898))
    print("srv online")

    sock.listen()

    with context.wrap_socket(sock, server_side=True) as ssock:
        conn, addr = ssock.accept()
        print("cli conn")
        while True:
            conn.sendall(bytes("welcome", "utf8"))
            time.sleep(1)

print("done")
