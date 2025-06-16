import socket
import os


def tcp_client() -> None:
    # Определение названия хоста и порта, к которым надо подключиться
    host: str = 'localhost'
    port: int = 20000

    #Устанавливаем, в какой папке будут происходить последующие процессы
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    #Подключение к серверу
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.connect((host, port))

        #Запрос файла
        filename: str = input("Enter filename to download: ")
        server.send(filename.encode())

        filesize: int = int(server.recv(1024).decode())

        #Проверка, есть ли файл на сервере
        if filesize == -1:
            print("File not found on server")
            return
        
        print(f"Downloading file {filename} ({filesize} bytes)")

        #Загрузка файла (точнее, копирование его с сервера)
        received: int = 0
        with open(f"downloaded_{filename}", 'wb') as file:
            while received < filesize:
                data: bytes = server.recv(4096)
                if not data:
                    break
                file.write(data)
                received += len(data)
        
        #Вывод сообщения о том, что файл успешно получен с обозначением его кол-ва полученных байтов
        print(f"File downloaded successfully (received {received} bytes)")


#Основное тело программы
if __name__ == "__main__":
    tcp_client()
