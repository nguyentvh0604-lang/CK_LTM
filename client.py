import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog
import json

HOST = '127.0.0.1'
PORT = 5050

class ChatClient:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chat App")
        
        self.text_area = scrolledtext.ScrolledText(self.root, state='disabled')
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.input_area = tk.Entry(self.root)
        self.input_area.pack(padx=10, pady=10, fill=tk.X)
        self.input_area.bind("<Return>", lambda e: self.send_message())

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))

        threading.Thread(target=self.receive, daemon=True).start()
        self.root.mainloop()

    def receive(self):
        while True:
            try:
                message_raw = self.client.recv(1024).decode('utf-8')
                if message_raw == "NICK_REQUEST":
                    if not hasattr(self, 'nickname'):
                        self.nickname = simpledialog.askstring("Nickname", "Name:")
                    self.client.send(self.nickname.encode('utf-8'))
                else:
                    msg_obj = json.loads(message_raw)
                    self.display_message(msg_obj)
            except:
                break

    def send_message(self):
        raw_text = self.input_area.get()
        if not raw_text: return
        
        if raw_text.startswith("/msg "):
            try:
                parts = raw_text.split(" ", 2)
                packet = {"type": "private", "sender": self.nickname, "receiver": parts[1], "content": parts[2]}
            except: return
        else:
            packet = {"type": "group", "sender": self.nickname, "content": raw_text}
        
        self.client.send(json.dumps(packet).encode('utf-8'))
        self.input_area.delete(0, tk.END)

    def display_message(self, msg_obj):
        self.text_area.config(state='normal')
        m_type = msg_obj.get("type")
        sender = msg_obj.get("sender", "System")
        content = msg_obj.get("content")

        if m_type == "private":
            self.text_area.insert(tk.END, f"[PM] {sender}: {content}\n", "p")
        elif m_type == "system":
            self.text_area.insert(tk.END, f"! {content}\n", "s")
        else:
            self.text_area.insert(tk.END, f"{sender}: {content}\n")
            
        self.text_area.tag_config("p", foreground="purple")
        self.text_area.tag_config("s", foreground="grey")
        self.text_area.yview(tk.END)
        self.text_area.config(state='disabled')

if __name__ == "__main__":
    ChatClient()