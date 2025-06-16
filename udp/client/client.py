import socket
import os


def udp_client() -> None:
    #Определение названия хоста и порта, к которым надо подключиться
    host: str = 'localhost'
    port: int = 20000
    buffer_size: int = 4096
    
    #Устанавливаем, в какой папке будут происходить последующие процессы
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    #Подключение к серверу
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server_address: tuple = (host, port)
        
        #Запрос файла
        filename: str = input("Enter filename to download: ")
        server.sendto(filename.encode(), server_address)
        
        #Получение размера файла
        data, _ = server.recvfrom(buffer_size)
        filesize: int = int(data.decode())
        
        #Проверка, есть ли файл на сервере
        if filesize == -1:
            print("File not found on server")
            return
        
        print(f"Downloading file {filename} ({filesize} bytes)")
        
        #Загрузка файла (точнее, копирование его с сервера)
        received: int = 0
        with open(f"downloaded_{filename}", 'wb') as file:
            while received < filesize:
                try:
                    # Устанавливаем таймаут для ожидания следующих пакетов
                    server.settimeout(2)
                    data, _ = server.recvfrom(buffer_size)
                    file.write(data)
                    received += len(data)
                except socket.timeout:
                    print("Timeout occurred, file transfer may be incomplete")
                    break
        
        #Вывод сообщения о том, что файл успешно получен с обозначением его кол-ва полученных байтов
        print(f"File downloaded successfully (received {received} bytes)")

#Основное тело программы
if __name__ == "__main__":
    udp_client()
    
