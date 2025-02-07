import socket
import ssl

host = "127.0.0.1"
port = 9999

def main():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)  # Use TLS (TLS 1.2 or TLS 1.3)
    context.set_ciphers("ECDHE-RSA-AES256-GCM-SHA384")  # Match the server's cipher
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE  # Disable certificate verification for testing

    client_socket = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))

    try:
        client_socket.connect((host, port))
        print("Connected to the secure server.")
        while True:
            command = input("Enter command (type 'quit' to exit): ")
            if command.lower() == "quit":
                client_socket.send(command.encode("utf-8"))
                break
            client_socket.send(command.encode("utf-8"))
            response = client_socket.recv(4096).decode("utf-8")
            print(response)
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
