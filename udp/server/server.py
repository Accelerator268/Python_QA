import socket
import os


def udp_server() -> None:
    host: str = 'localhost'
    port: int = 20000
    buffer_size: int = 4096
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((host, port))
        print(f"UDP Server listening on {host}:{port}")
        
        while True:
            try:
                data, address = server.recvfrom(buffer_size)
                filename: str = data.decode()
                print(f"Client {address} requested file: {filename}")
                
                if os.path.exists(filename):
                    print(f"Client requested file: {filename}\nSending...")

                    filesize: int = os.path.getsize(filename)
                    server.sendto(str(filesize).encode(), address)
                    
                    with open(filename, 'rb') as file:
                        while True:
                            chunk: bytes = file.read(buffer_size)
                            if not chunk:
                                break
                            server.sendto(chunk, address)
                    print(f"File {filename} sent successfully to {address}")
                else:
                    server.sendto(b"-1", address)
                    print(f"File {filename} not found")
                    
            except Exception as exception:
                print(f"Error: {exception}")


if __name__ == "__main__":
    udp_server()
