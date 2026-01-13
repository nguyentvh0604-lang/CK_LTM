# Chat Client–Server TCP (Python)

# Nhóm 4

## 1. Giới thiệu

Đây là ứng dụng chat đơn giản theo mô hình **Client – Server**, sử dụng giao thức **TCP Socket** trong Python.  
Ứng dụng cho phép nhiều client kết nối đồng thời đến server, hỗ trợ:

- Chat nhóm
- Chat riêng giữa các client
- Hiển thị thông báo hệ thống khi client vào/ra phòng chat
- Giao diện đồ họa sử dụng Tkinter đơn giản

---

## 2. Công nghệ sử dụng

- Ngôn ngữ: **Python 3**
- Thư viện:
  - `socket` – lập trình mạng TCP
  - `asyncio` – xử lý đa kết nối phía server
  - `threading` – xử lý luồng phía client
  - `tkinter` – giao diện đồ họa
  - `json` – đóng gói dữ liệu trao đổi giữa client và server

---

## 3. Kiến trúc hệ thống

### 3.1 Mô hình Client – Server

- **Server**:

  - Lắng nghe kết nối từ nhiều client
  - Quản lý danh sách client đang online
  - Phát tin nhắn chat nhóm
  - Chuyển tiếp tin nhắn riêng

- **Client**:
  - Kết nối đến server
  - Nhập nickname khi tham gia
  - Gửi và nhận tin nhắn
  - Hiển thị nội dung chat qua giao diện Tkinter

---

## 4. Chức năng chính

### 4.1 Phía Server

- Chấp nhận nhiều kết nối cùng lúc
- Yêu cầu client nhập nickname khi kết nối
- Kiểm tra trùng nickname
- Gửi thông báo hệ thống
- Chat nhóm (broadcast)
- Chat riêng giữa 2 client

### 4.2 Phía Client

- Nhập nickname khi tham gia phòng chat
- Gửi tin nhắn chat nhóm
- Gửi tin nhắn riêng theo cú pháp:

## 5. Cách chạy

### Đối với server:

- python server.py

### Đối với client:

- python client.py

## 6. Lệnh

/msg <ten> <noi dung> gửi riêng cho một người
/exit thoát khỏi đoạn chat
