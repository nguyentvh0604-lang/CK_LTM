import socket
import threading

# Cấu hình Server
HOST = '127.0.0.1'
PORT = 5050
clients = {} 

def handle_client(client_socket, address):
    print(f"[NEW CONNECTION] {address} connected.")
    
    try:
        username = client_socket.recv(1024).decode('utf-8')
        clients[username] = client_socket
        print(f"[REGISTER] {username} đã gia nhập hệ thống.")

        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            # TODO: 
           
            
            print(f"[{username}] gửi tin: {data}")
            
            client_socket.send(f"Server đã nhận tin từ {username}".encode('utf-8'))

    except Exception as e:
        print(f"[ERROR] Lỗi với client {address}: {e}")
    finally:
        client_socket.close()
        # TODO: Xóa client khỏi danh sách khi ngắt kết nối

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] Server đang chạy trên {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()