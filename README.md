# Bilgisayar Ağları TCP/UDP Hastane Randevu Sistemi

## Proje Hakkında

Bu proje, Bilgisayar Ağları dersi kapsamında Python programlama dili kullanılarak geliştirilmiş istemci-sunucu tabanlı bir hastane randevu sistemidir.

Sistem, TCP ve UDP haberleşme protokollerini kullanarak doktor ve hasta arasındaki iletişimi simüle etmektedir. Projede çoklu istemci desteği, kuyruk yönetimi, zaman aşımı (timeout) kontrolü ve çok iş parçacıklı (multithreaded) yapı kullanılmıştır.

Amaç, TCP ve UDP protokollerinin çalışma mantığını uygulamalı olarak göstermek ve istemci-sunucu mimarisini gerçek bir senaryo üzerinden modellemektir.

---

## Proje Özellikleri

* TCP bağlantı desteği
* UDP bağlantı desteği
* İstemci-Sunucu mimarisi
* Çoklu istemci yönetimi
* Doktor-Hasta eşleştirme sistemi
* Hasta kuyruk yönetimi
* Timeout mekanizması
* Thread kullanımı
* Socket programlama uygulaması

---

## Kullanılan Teknolojiler

* Python 3
* Socket Programming
* TCP Protocol
* UDP Protocol
* Threading
* Select Modülü

---

## Sistem Yapısı

Sistemde iki farklı kullanıcı tipi bulunmaktadır:

### Doktor

* Sunucuya TCP bağlantısı ile bağlanır.
* Hastaları sırayla çağırabilir.
* Gelen hasta taleplerini yönetir.

### Hasta

* TCP veya UDP üzerinden bağlanabilir.
* Sistemde uygun doktor kuyruğuna eklenir.
* Doktor tarafından çağrıldığında randevuyu kabul edebilir.

---

## Dosya Yapısı

```text
bilgisayar-ağları-tcp-udp-hastane-randevu-sistemi
│
├── 22100011064_Server.py
├── 22100011064_Client.py
└── README.md
```

### Dosya Açıklamaları

| Dosya                 | Açıklama                  |
| --------------------- | ------------------------- |
| 22100011064_Server.py | Sunucu tarafı uygulaması  |
| 22100011064_Client.py | İstemci tarafı uygulaması |
| README.md             | Proje dokümantasyonu      |

---

## Çalıştırma Adımları

### 1. Sunucuyu Başlatma

```bash
python 22100011064_Server.py
```

Sunucu başarıyla çalıştığında aşağıdaki mesaj görüntülenir:

```text
[SERVER] Sunucu başlatıldı ve dinliyor
```

---

### 2. Doktor Bağlantısı

Doktor istemcisi TCP kullanarak bağlanır.

```bash
python 22100011064_Client.py Doktor TCP
```

---

### 3. TCP Hasta Bağlantısı

```bash
python 22100011064_Client.py Hasta TCP
```

---

### 4. UDP Hasta Bağlantısı

```bash
python 22100011064_Client.py Hasta UDP
```

---

## Çalışma Mantığı

1. Sunucu başlatılır.
2. İlk iki TCP bağlantısı doktor olarak sisteme eklenir.
3. Daha sonra bağlanan kullanıcılar hasta olarak kabul edilir.
4. Hastalar doktor kuyruklarına sırayla dağıtılır.
5. Doktor istediği zaman sıradaki hastayı çağırabilir.
6. Hasta çağrıyı kabul ettiğinde görüşme başlatılır.
7. Hasta belirlenen süre içerisinde cevap vermezse sistem sıradaki hastaya geçer.
8. Görüşme tamamlandıktan sonra bağlantı sonlandırılır.

---

## Öğrenilen Konular

Bu proje kapsamında aşağıdaki ağ programlama kavramları uygulanmıştır:

* TCP Haberleşmesi
* UDP Haberleşmesi
* Socket Programlama
* Client-Server Mimarisi
* Multithreading
* Select Kullanımı
* Timeout Yönetimi
* Kuyruk Yapıları
* Eşzamanlı Bağlantı Yönetimi

---

## Proje Amacı

Bu çalışmanın amacı;

* TCP ve UDP protokollerini uygulamalı olarak öğrenmek,
* Ağ programlama becerilerini geliştirmek,
* İstemci-sunucu mimarisini gerçek bir senaryo üzerinde uygulamak,
* Çoklu istemci yönetimini gerçekleştirmektir.

---

## Ders Bilgisi

**Ders:** Bilgisayar Ağları

**Proje Türü:** Dönem Ödevi

**Konu:** TCP/UDP Tabanlı Hastane Randevu Sistemi

---

## Geliştirici

Melih Fındık

Necmettin Erbakan Üniversitesi

Bilgisayar Mühendisliği
