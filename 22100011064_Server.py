import socket
import select
import threading
import time


HOST = '127.0.0.1'
PORT = 12345
BUFFER_SIZE = 1024

# TCP ve UDP socketleri oluştur
server_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_tcp.bind((HOST, PORT))
server_udp.bind((HOST, PORT))

server_tcp.listen()
print("[SERVER] Sunucu başlatıldı ve dinliyor")

# Kullanılacak listeler ve kuyruklar
inputs = [server_tcp, server_udp]
client_sockets = []
doktor_list = []
hasta_list = []
hasta_kuyrugu = {}
aktif_udp_gorusmeler = {}  # UDP hastalar için aktif görüşme bilgisi

doktor_sayisi = 0
hasta_sayisi = 0

# UDP için 10 saniye bekleyip cevap gelmezse sıradaki hastaya geçecek timeout fonk
def udp_timeout_kontrol(addr, conn_doktor, hasta_ad, doktor_ad):
    time.sleep(10)
    if addr in aktif_udp_gorusmeler:
        aktif_udp_gorusmeler.pop(addr)
        server_udp.sendto("Cevap vermediniz, bağlantınız kapatıldı.\n".encode(), addr)
        conn_doktor.sendall(f"{hasta_ad} 10 sn içinde cevap vermedi, sıradaki hasta çağrılıyor.\n".encode())
        print(f"[SERVER] {hasta_ad} cevap vermedi, sıradaki hasta çağrılıyor.\n")
        hasta_cagir(doktor_ad)

# Bağlantıları yöneten ve mesajları işleyen ana fonksiyon
def baglanti_yonet():
    global doktor_sayisi, hasta_sayisi
    while True:
        readable, _, _ = select.select(inputs + client_sockets, [], [])
        for sock in readable:
            if sock == server_tcp:
                conn, addr = server_tcp.accept()
                client_sockets.append(conn)

                if doktor_sayisi < 2:  # İlk 2 TCP bağlantısı doktor olacak
                    doktor_ad = f"Doktor{doktor_sayisi + 1}"
                    doktor_list.append((conn, doktor_ad))
                    hasta_kuyrugu[doktor_ad] = []
                    doktor_sayisi += 1
                    conn.sendall(f"Hoşgeldiniz {doktor_ad}\n".encode())
                    print(f"[SERVER] Yeni doktor bağlandı: {doktor_ad} {addr}\n")
                else:  # Sonraki TCP bağlantıları hasta olacak
                    hasta_ad = f"Hasta{hasta_sayisi + 1}"
                    hangi_doktor = doktor_list[hasta_sayisi % len(doktor_list)][1]
                    hasta_sayisi += 1
                    hasta_list.append((conn, hasta_ad, 'TCP'))
                    hasta_kuyrugu[hangi_doktor].append((conn, hasta_ad, 'TCP'))
                    conn.sendall(f"Hoşgeldiniz {hasta_ad}, {hangi_doktor} kuyruğuna eklendiniz.\n".encode())
                    print(f"[SERVER] Yeni hasta bağlandı (TCP): {hasta_ad} {addr}, {hangi_doktor} kuyruğuna eklendi.\n")
            elif sock == server_udp:
                data, addr = server_udp.recvfrom(BUFFER_SIZE)
                mesaj = data.decode().strip()
                if mesaj.startswith("Hasta bağlandı"):  # UDP hasta bağlanınca
                    hasta_ad = f"Hasta{hasta_sayisi + 1}"
                    hangi_doktor = doktor_list[hasta_sayisi % len(doktor_list)][1]
                    hasta_sayisi += 1
                    hasta_list.append((addr, hasta_ad, 'UDP'))
                    hasta_kuyrugu[hangi_doktor].append((addr, hasta_ad, 'UDP'))
                    server_udp.sendto(f"Hoşgeldiniz {hasta_ad}, {hangi_doktor} kuyruğuna eklendiniz.\n".encode(), addr)
                    print(f"[SERVER] Yeni hasta bağlandı (UDP): {hasta_ad} {addr}, {hangi_doktor} kuyruğuna eklendi.\n")
                elif mesaj == "evet":  # UDP hasta kabul cevabı verdi
                    if addr in aktif_udp_gorusmeler:
                        hasta_ad = aktif_udp_gorusmeler[addr][1]
                        print(f"[SERVER] UDP mesaj {addr} (Hasta: {hasta_ad}): {mesaj}\n")
                        conn_doktor, hasta_ad, doktor_ad = aktif_udp_gorusmeler.pop(addr)
                        server_udp.sendto(f"{doktor_ad} ile randevunuz başladı.\n".encode(), addr)
                        time.sleep(3)
                        server_udp.sendto("Geçmiş olsun! Bağlantınız sonlandırılıyor.\n".encode(), addr)
                        conn_doktor.sendall(f"{hasta_ad}, randevuyu kabul etti.\n".encode())
                        conn_doktor.sendall(f"{hasta_ad} ayrıldı.\n".encode())
                        print(f"[SERVER] {hasta_ad} → {doktor_ad} görüşme tamamlandı.\n")
                    else:
                        print(f"[SERVER] UDP {addr} için aktif görüşme kaydı bulunamadı.\n")
                else:
                    print(f"[SERVER] UDP {addr} bilinmeyen mesaj: {mesaj}\n")
            else:  # Gelen diğer TCP mesajları
                try:
                    data = sock.recv(BUFFER_SIZE)
                    if not data:
                        sock.close()
                        client_sockets.remove(sock)
                        continue
                    print(f"[SERVER] Gelen mesaj: {data.decode()}\n")
                except:
                    sock.close()
                    if sock in client_sockets:
                        client_sockets.remove(sock)

# Doktor tarafından hasta çağırma işlemini yapan fonk
def hasta_cagir(doktor_ad):
    doktor_bul = [c for c, d in doktor_list if d == doktor_ad]
    if not doktor_bul:
        print(f"[SERVER] {doktor_ad} henüz bağlı değil!\n")
        return

    conn_doktor = doktor_bul[0]

    if hasta_kuyrugu.get(doktor_ad) and hasta_kuyrugu[doktor_ad]:
        conn_or_addr, hasta_ad, protokol = hasta_kuyrugu[doktor_ad].pop(0)

        conn_doktor.sendall(f"{hasta_ad} → {doktor_ad}\n".encode())

        if protokol == 'TCP':
            conn_or_addr.sendall(f"{doktor_ad} sizi çağırıyor. Kabul için 'evet' yazın.\n".encode())
            conn_or_addr.settimeout(10)
            try:
                cevap = conn_or_addr.recv(BUFFER_SIZE).decode().strip().lower()
                if cevap == "evet":
                    conn_doktor.sendall(f"{hasta_ad}, randevuyu kabul etti.\n".encode())
                    conn_or_addr.sendall(f"{doktor_ad} ile randevunuz başladı.\n".encode())
                    time.sleep(1)
                    conn_or_addr.sendall("Geçmiş olsun! Bağlantınız sonlandırılıyor.\n".encode())
                    conn_or_addr.close()
                    if conn_or_addr in client_sockets:
                        client_sockets.remove(conn_or_addr)
                    conn_doktor.sendall(f"{hasta_ad} ayrıldı.\n".encode())
                    print(f"[SERVER] {hasta_ad} → {doktor_ad} görüşme tamamlandı.\n")
                else:
                    print(f"[SERVER] {hasta_ad} randevuyu reddetti.\n")
            except socket.timeout:
                conn_doktor.sendall(f"{hasta_ad} 10 sn içinde cevap vermedi, sıradaki hasta çağrılıyor.\n".encode())
                print(f"[SERVER] {hasta_ad} cevap vermedi, sıradaki hasta çağrılıyor.\n")
                hasta_cagir(doktor_ad)
        else:  # UDP hasta çağırıldı
            server_udp.sendto(f"{doktor_ad} sizi çağırıyor. Kabul için 'evet' yazın.\n".encode(), conn_or_addr)
            aktif_udp_gorusmeler[conn_or_addr] = (conn_doktor, hasta_ad, doktor_ad)
            print(f"[SERVER] {hasta_ad} için UDP çağrı gönderildi, cevap bekleniyor.\n")
            threading.Thread(target=udp_timeout_kontrol, args=(conn_or_addr, conn_doktor, hasta_ad, doktor_ad), daemon=True).start()
    else:
        conn_doktor.sendall("Bekleyen hasta bulunmamaktadır.\n".encode())
        print(f"[SERVER] {doktor_ad} için bekleyen hasta yok.\n")

# Bağlantı yönetimi threadi başlatılıyor
threading.Thread(target=baglanti_yonet, daemon=True).start()

# Konsoldan doktor ismi girilip hasta çağrılıyor
while True:
    komut = input("Hasta çağırmak için 'Doktor1' veya 'Doktor2' yazın: ")
    if komut in hasta_kuyrugu:
        hasta_cagir(komut)
    else:
        print("[SERVER] Geçerli bir doktor adı girin.\n")
