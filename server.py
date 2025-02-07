import socket
import ssl
import threading

host = "127.0.0.1"
port = 9999


def create_secure_socket():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)  # Use TLS (TLS 1.2 or TLS 1.3)
    context.set_ciphers("ECDHE-RSA-AES256-GCM-SHA384")  # Use a strong, common cipher
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")  # Use your certificate and private key
    return context


def handle_client(conn, address):
    print(f"Connection established with {address}")
    conn.send(str.encode("Welcome to the secure server.\n"))
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            command = data.decode("utf-8").strip()
            if command.lower() == "quit":
                break
            response = f"Received: {command}\n"
            conn.send(response.encode("utf-8"))
    finally:
        conn.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = create_secure_socket()
    secure_socket = context.wrap_socket(server_socket, server_side=True)

    secure_socket.bind((host, port))
    secure_socket.listen(5)
    print(f"Server listening on {host}:{port}...")

    try:
        while True:
            conn, address = secure_socket.accept()
            threading.Thread(target=handle_client, args=(conn, address)).start()
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        secure_socket.close()


if __name__ == "__main__":
    main()
