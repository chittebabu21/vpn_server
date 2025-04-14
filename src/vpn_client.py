import socket
import ssl
import os
import pathlib

def start_vpn_client(host, port):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    cert_path = pathlib.Path(base_dir, "certs", "server.crt")

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations(cert_path)

    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_socket.connect((host, port))
    conn = context.wrap_socket(raw_socket, server_hostname=host)

    try:
        conn.send(b"Hello, VPN Server!")
        data = conn.recv(1024)
        print(f"Received: {data}")
    finally:
        conn.close()