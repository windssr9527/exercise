import socket
import threading

socket_obj=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

socket_obj.bind(("127.0.0.1",8080))
#設定端口複用
socket_obj.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
socket_obj.listen(128)

def sockserver():
    print(threading.current_thread())
    sock, addr = socket_obj.accept()
    sockmore=threading.Thread(target=sockserver)
    sockmore.start()
    while True:
        recvcode=sock.recv(1024)
        print(recvcode.decode())
        #sock.send("服務端收到".encode())
        if recvcode.decode()=="88":
            sock.close()
            break

if __name__=="__main__":
    sock1=threading.Thread(target=sockserver)
    sock1.start()



