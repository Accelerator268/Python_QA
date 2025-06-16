import socket
import os


def tcp_client() -> None:
    host: str = 'localhost'
    port: int = 20000

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.connect((host, port))

        filename: str = input("Enter filename to download: ")
        server.send(filename.encode())

        filesize: int = int(server.recv(1024).decode())

        if filesize == -1:
            print("File not found on server")
            return
        
        print(f"Downloading file {filename} ({filesize} bytes)")

        received: int = 0
        with open(f"downloaded_{filename}", 'wb') as file:
            while received < filesize:
                data: bytes = server.recv(4096)
                if not data:
                    break
                file.write(data)
                received += len(data)

        print(f"File downloaded successfully (received {received} bytes)")


if __name__ == "__main__":
    tcp_client()
