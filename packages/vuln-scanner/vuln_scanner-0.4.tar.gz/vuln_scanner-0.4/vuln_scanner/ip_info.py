import socket

def get_ip_from_domain(domain):
    """
    يحصل على عنوان IP من اسم النطاق (الدومين).
    :param domain: اسم النطاق المراد تحويله إلى IP.
    """
    try:
        ip_address = socket.gethostbyname(domain)
        print(f"اسم النطاق: {domain}")
        print(f"عنوان IP: {ip_address}")
        return ip_address
    except socket.gaierror:
        print(f"[!] لم يتم العثور على عنوان IP لهذا النطاق: {domain}")
    except Exception as e:
        print(f"[!] حدث خطأ أثناء محاولة الحصول على IP: {e}")
