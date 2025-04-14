import socket
import ssl
import os
import pathlib

def start_vpn_server(host, port):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    cert_path = pathlib.Path(base_dir, "certs", "server.crt")
    key_path = pathlib.Path(base_dir, "certs", "server.key")

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=cert_path, keyfile=key_path)

    bindsocket = socket.socket()
    bindsocket.bind((host, port))
    bindsocket.listen(5)

    print(f"VPN server listening on {host}:{port}")

    while True:
        newsocket, fromaddr = bindsocket.accept()
        print(f"Client connected from {fromaddr}")

        conn = context.wrap_socket(newsocket, server_side=True)

        try:
            data = conn.recv(1024)
            print(f"Received from {fromaddr}: {data}")

            if data:
                conn.sendall(b"Hello, VPN Client")
        except Exception as e:
            print(f"Exception: {e}")
        finally:
            try:
                conn.shutdown(socket.SHUT_RDWR)
            except OSError as e:
                print(f"OSError: {e}")

            conn.close()