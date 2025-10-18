# client_gui.py
import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext

# --- Configuration ---
HOST = '127.0.0.1'
PORT = 55555

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Client")
        self.root.geometry("400x500")

        # --- Nickname Dialog ---
        self.nickname = simpledialog.askstring("Nickname", "Please choose a nickname", parent=root)
        if not self.nickname:
            root.destroy()
            return
            
        self.client = None
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # --- GUI Elements ---
        
        # Frame for the chat display
        self.chat_frame = tk.Frame(root)
        self.scrollbar = tk.Scrollbar(self.chat_frame)
        
        # Chat display area
        self.chat_box = scrolledtext.ScrolledText(self.chat_frame, height=20, width=50, yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.chat_box.config(state=tk.DISABLED) # Make it read-only
        self.chat_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Frame for message entry
        self.entry_frame = tk.Frame(root)
        self.msg_entry = tk.Entry(self.entry_frame, width=40)
        self.msg_entry.bind("<Return>", self.send_message) # Bind Enter key
        self.send_button = tk.Button(self.entry_frame, text="Send", command=self.send_message)
        
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.send_button.pack(side=tk.RIGHT, padx=5)
        self.entry_frame.pack(pady=10, padx=10, fill=tk.X)

        # --- Network Connection ---
        self.start_network_thread()

    def start_network_thread(self):
        """Initializes the network connection and starts the receiving thread."""
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((HOST, PORT))
            
            # Start a thread to listen for messages
            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.daemon = True # Thread dies when main app closes
            self.receive_thread.start()
            
        except ConnectionRefusedError:
            self.insert_message("[SYSTEM] Cannot connect to the server. Is it running?")
        except Exception as e:
            self.insert_message(f"[SYSTEM] Connection error: {e}")

    def receive_messages(self):
        """Handles receiving messages from the server."""
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('utf-8'))
                elif not message:
                    # Server closed connection
                    self.insert_message("[SYSTEM] Server has closed the connection.")
                    break
                else:
                    # Display the message in the chat box
                    self.insert_message(message)
            except (ConnectionResetError, ConnectionAbortedError):
                self.insert_message("[SYSTEM] Disconnected from server.")
                break
            except Exception as e:
                self.insert_message(f"[SYSTEM] An error occurred: {e}")
                self.client.close()
                break

    def send_message(self, event=None):
        """Handles sending a message to the server."""
        message_content = self.msg_entry.get()
        if message_content and self.client:
            message = f"{self.nickname}: {message_content}"
            try:
                self.client.send(message.encode('utf-8'))
                self.msg_entry.delete(0, tk.END) # Clear the entry box
            except Exception as e:
                self.insert_message(f"[SYSTEM] Failed to send message: {e}")

    def insert_message(self, message):
        """Inserts a message into the chat box (thread-safe)."""
        # We must modify the GUI from the main thread
        # This simple lambda function is scheduled to run in the main GUI loop
        self.root.after(0, lambda: self._insert_to_chatbox(message))

    def _insert_to_chatbox(self, message):
        """Helper function to modify the chat box."""
        if self.chat_box:
            self.chat_box.config(state=tk.NORMAL)
            self.chat_box.insert(tk.END, message + "\n")
            self.chat_box.config(state=tk.DISABLED)
            self.chat_box.see(tk.END) # Auto-scroll to the bottom

    def on_closing(self, event=None):
        """Handles the event when the user closes the GUI window."""
        if self.client:
            self.client.close()
        self.root.destroy()

# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClient(root)
    root.mainloop()
