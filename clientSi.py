import socket
import threading

HOST = input("Nhập IP server: ")
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

username = ""

def receive():
    global username
    while True:
        try:
            msg = client.recv(1024).decode("utf-8")

            if msg == "USERNAME":
                username = input("Nhập tên của bạn: ")
                client.send(username.encode("utf-8"))
            else:
                print(msg)
        except:
            print("Mất kết nối tới server!")
            client.close()
            break

def write():
    while True:
        msg = input("")
        if msg.lower() == "/quit":
            client.send(msg.encode("utf-8"))
            client.close()
            break
        client.send(msg.encode("utf-8"))

thread_recv = threading.Thread(target=receive)
thread_recv.start()

thread_write = threading.Thread(target=write)
thread_write.start()
