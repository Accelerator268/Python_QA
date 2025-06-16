#!/bin/bash

#Создание случайного файла размером более 1 МБ в папке server
echo "Создание случайного файла в папке server..."
dd if=/dev/urandom of=server/random bs=1M count=2 status=none

#Запуск server.py в фоновом режиме
echo "Запуск сервер в фоновом режиме..."
python3 server/server.py &
SERVER_PID=$!
echo "Сервер запущен с PID $SERVER_PID"

# Время серверу на запуск
sleep 2

#Запуск client.py и передача ему имени файла
echo "Запуск клиента и передача имени файла..."
echo "random" | python3 client/client.py

#Сравнение файлов
echo "Сравнение исходного и полученного файлов..."
if cmp -s server/random client/downloaded_random; then
    echo "Файлы идентичны!"
    RESULT=0
else
    echo "Файлы различаются!"
    RESULT=1
fi

#Завершение процесса сервера
kill $SERVER_PID
wait $SERVER_PID 2>/dev/null
echo "Сервер остановлен"

exit $RESULT
