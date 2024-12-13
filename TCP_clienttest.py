import socket

socket_obj=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

socket_obj.connect(("127.0.0.1",8080))

while True:
    sendstr=input("請輸入文字:")

    socket_obj.send(sendstr.encode())

    returncode=socket_obj.recv(1024)

    print(returncode.decode())

    if sendstr=="88":
        break

socket_obj.close()