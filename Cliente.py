import socket


def tcp_client(host='127.0.0.1', port=65432):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print(f"Conectado al servidor {host}:{port}")

        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(data.decode())

    except Exception as e:
        print(f"Error al conectar con el servidor: {e}")
    finally:
        client_socket.close()
        print("Conexión cerrada")


if __name__ == '__main__':
    tcp_client()
