import socket
import os


def udp_client() -> None:
    host: str = 'localhost'
    port: int = 20000
    buffer_size: int = 4096
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server_address: tuple = (host, port)
        
        filename: str = input("Enter filename to download: ")
        server.sendto(filename.encode(), server_address)
        
        data, _ = server.recvfrom(buffer_size)
        filesize: int = int(data.decode())
        
        if filesize == -1:
            print("File not found on server")
            return
        
        print(f"Downloading file {filename} ({filesize} bytes)")
        
        received: int = 0
        with open(f"downloaded_{filename}", 'wb') as file:
            while received < filesize:
                try:
                    server.settimeout(2)
                    data, _ = server.recvfrom(buffer_size)
                    file.write(data)
                    received += len(data)
                except socket.timeout:
                    print("Timeout occurred, file transfer may be incomplete")
                    break
        
        print(f"File downloaded successfully (received {received} bytes)")


if __name__ == "__main__":
    udp_client()
