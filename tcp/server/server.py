import socket
import os


def tcp_server() -> None:
    host: str = 'localhost'
    port: int = 20000

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen(1)
        print(f"TCP Server listening on {host}:{port}")

        while True:
            conn, address = server.accept()
            address = ':'.join([str(i) for i in address])
            print(f"Request from {address}")

            try:
                filename = conn.recv(1024).decode()
                if not filename:
                    continue

                print(f"Client requested file: {filename}\nSending...")

                if os.path.exists(filename):
                    filesize: int = os.path.getsize(filename)
                    conn.send(str(filesize).encode())

                    with open(filename, 'rb') as file:
                        while True:
                            data: bytes = file.read(4096)
                            if not data:
                                break
                            conn.send(data)
                    print(f"Finished sending to {address}")
                else:
                    conn.send(b"-1")
                    print(f"File not found\nFailed sending to {address}")

            except Exception as exception:
                print(f"Error: {exception}")

            finally:
                conn.close()


if __name__ == "__main__":
    tcp_server()
