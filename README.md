# 💬 Multi-Client Command-Line Chat Server in Python

A robust client-server chat application built with Python's native `socket` and `threading` libraries, demonstrating core networking concepts.

This project implements a **multi-client chatroom** where users can connect to a central server via a **command-line interface** to send and receive messages in real-time. It operates over **TCP** for reliable, connection-oriented communication.

---

## 📖 Abstract

This project aims to develop a robust client-server chat application that allows multiple users to connect to a central server and communicate in a shared public chatroom. The application is built using Python's native `socket` and `threading` libraries, operating over the **Transmission Control Protocol (TCP)** for reliable, connection-oriented communication.

The **server** is responsible for accepting incoming client connections, receiving messages, and broadcasting them to all other connected clients.  
Each **client** runs a separate application that connects to the server, allowing the user to send messages and receive messages from others in real time.

This project serves as a practical demonstration of fundamental networking concepts including:
- Socket programming  
- Client-server architecture  
- Concurrency  
- Protocol handling

---

## ✨ Core Features

- ✅ **Multi-Client Support** — The server uses threading to handle multiple simultaneous client connections without blocking.  
- ⚡ **Real-Time Messaging** — Messages are broadcast instantly to all connected users.  
- 🧠 **Reliable Communication** — Utilizes TCP protocol to ensure messages are delivered in order and without errors.  
- 👥 **Dynamic User Management** — Gracefully handles users joining and leaving the chatroom, notifying all other participants.  
- 💻 **Command-Line Interface** — A clean, simple, and intuitive interface for sending and receiving messages.  
- 🌐 **Cross-Platform** — Runs on any system with Python 3 installed (Windows, macOS, Linux).

---

## 🏗️ System Architecture

The application follows a **classic Client-Server Architecture**.

### 🖥️ Server (`server.py`)
- Acts as the **central hub**.  
- Binds to a specific IP and port, listens for incoming connections.  
- Manages all communication.  
- When a message is received from one client, it **broadcasts** it to every other connected client.

### 💻 Client (`client.py`)
- The application that each user runs.  
- Connects to the server, then spawns two threads:
  - One for sending user input to the server.
  - Another for continuously listening for incoming messages from the server.

---

## 🛠️ Technical Stack

- **Programming Language**: Python 3  
- **Core Libraries**:
  - [`socket`](https://docs.python.org/3/library/socket.html): For low-level network communication.
  - [`threading`](https://docs.python.org/3/library/threading.html): For concurrent client connections and non-blocking operations.

---

## 🚀 How to Run

### ✅ Prerequisites
- Python 3 must be installed on your system.  
  [Download Python](https://www.python.org/downloads/)

---

### 🧭 Instructions

#### 1. Clone the Repository
```bash
git clone https://github.com/Arun2895/python-multiclient-chat.git
cd python-multiclient-chat

