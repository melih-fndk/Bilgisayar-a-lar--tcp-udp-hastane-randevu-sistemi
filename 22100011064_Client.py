import socket
import sys
import threading

# Bağlantı yapılacak sunucunun adres ve portu
HOST = '127.0.0.1'
PORT = 12345
BUFFER_SIZE = 1024

# Komut satırından gelen argümanlarla hangi tip (Doktor/Hasta) ve bağlantı tipi (TCP/UDP) belirleniyor
client_type = sys.argv[1]  # Doktor veya Hasta
connection_type = sys.argv[2]  # TCP veya UDP

# TCP bağlantısı için sunucudan gelen mesajları dinleyen fonksiyon
def mesaj_dinle_tcp(sock):
    while True:
        try:
            mesaj = sock.recv(BUFFER_SIZE).decode()
            if not mesaj:
                break
            print(f"[{client_type}] Gelen mesaj: {mesaj}")  
        except:
            break

# UDP bağlantısı için gelen mesajları dinleyen fonksiyon
def mesaj_dinle_udp(sock):
    while True:
        try:
            mesaj, _ = sock.recvfrom(BUFFER_SIZE)
            print(f"[{client_type}][UDP] Gelen mesaj: {mesaj.decode()}")  
        except:
            break

# TCP bağlantısı kurulursa yapılacak işlemler
if connection_type.upper() == "TCP":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))  # Sunucuya bağlan
    print(f"[{client_type}] TCP bağlantısı kuruldu.")
    client_socket.sendall(f"{client_type} bağlandı".encode())  # Bağlandığını sunucuya bildir

    # Gelen mesajları dinlemek thread
    dinleme_thread = threading.Thread(target=mesaj_dinle_tcp, args=(client_socket,))
    dinleme_thread.start()

    while True:
        giris = input()  
        client_socket.sendall(giris.encode()) 

# UDP bağlantısı kurulursa yapılacak işlemler
elif connection_type.upper() == "UDP":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(f"{client_type} bağlandı".encode(), (HOST, PORT))  # sunucuya bağlandı mesajı 
    print(f"[{client_type}] UDP mesaj gönderildi.")

    # Gelen UDP mesajlarını dinlemek için ayrı bir thread başlat
    dinleme_thread = threading.Thread(target=mesaj_dinle_udp, args=(client_socket,))
    dinleme_thread.start()

    while True:
        giris = input()  
        client_socket.sendto(giris.encode(), (HOST, PORT))  # Mesajı sunucuya gönder

else:
    print("[HATA] Bağlantı tipi hatalı. TCP veya UDP giriniz.")
