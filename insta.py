import requests
import json
import re
import urllib3
import csv
from datetime import datetime

urllib3.disable_warnings()

ascii_art = r"""
░▀█▀░█▀▀░░░█▀█░█▀▀░▀█▀░█▀█░▀█▀░░
░░█░░█░█░░░█░█░▀▀█░░█░░█░█░░█░░░
░▀▀▀░▀▀▀░░░▀▀▀░▀▀▀░▀▀▀░▀░▀░░▀░░░
      Made By @0xVileness
"""

def obtener_info_osint(username, guardar_csv=True):
    url = "https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/"
    data = {'email_or_username': username}
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Instagram-Ajax': '1',
        'X-Csrftoken': 'DUMMYTOKEN',
        'Referer': 'https://www.instagram.com/accounts/password/reset/',
    }

    response = requests.post(url, headers=headers, data=data, verify=False)
    result = {
        'user': username,
        'Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status_code': response.status_code,
        'correo_visible': '',
        'domain': '',
        'tipo': '',
        'alert': '',
    }

    if response.status_code == 200:
        try:
            res_json = response.json()
            if 'contact_point' in res_json:
                correo_oculto = res_json['contact_point']
                result['correo_visible'] = correo_oculto

                match = re.search(r'@(\w+\.\w+)', correo_oculto)
                if match:
                    domain = match.group(1)
                    result['domain'] = domain

                    if "gmail.com" in domain:
                        result['tipo'] = "Gmail"
                    elif "hotmail.com" in domain:
                        result['tipo'] = "Hotmail"
                    elif "yahoo.com" in domain:
                        result['tipo'] = "Yahoo"
                    elif "outlook.com" in domain:
                        result['tipo'] = "Outlook"
                    elif "protonmail.com" in domain or "proton.me" in domain:
                        result['tipo'] = "ProtonMail"
                    else:
                        result['tipo'] = "Another"
                else:
                    result['tipo'] = "Indeterminado"
                result['alert'] = "All OK"
            else:
                result['alert'] = "No mail was obtained."
        except Exception as e:
            result['alert'] = f"Error JSON: {str(e)}"
    else:
        result['alert'] = f"Error HTTP: {response.status_code}"

    print(f"\n[INFO OSINT] User: {username}")
    print(f"- Code HTTP: {result['status_code']}")
    print(f"- Mail parcial: {result['correo_visible']}")
    print(f"- Domain: {result['domain']}")
    print(f"- Tipo: {result['tipo']}")
    print(f"- Alert: {result['alert']}")

    if guardar_csv:
        with open('resultados_osint.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=result.keys())
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(result)

if __name__ == "__main__":
    print(ascii_art)
    usuario = input(" Enter The Instagram User for Osint: ").strip()
    obtener_info_osint(usuario, guardar_csv=True)
