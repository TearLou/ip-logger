from flask import Flask, request
from datetime import datetime
import pytz
import requests
import os

app = Flask(__name__)

moscow_tz = pytz.timezone("Europe/Moscow")
access_time = datetime.now(moscow_tz).strftime('%Y-%m-%d %H:%M:%S')

def check_ip_details(ip):
    api_key = '4NCSuXALgoQMCfExLttNTPQVnyD2h3cf'
    url = f'https://ipqualityscore.com/api/json/ip/{api_key}/{ip}'
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Определение типа устройства
def detect_device_type(user_agent):
    ua = user_agent.lower()
    if 'tablet' in ua or 'ipad' in ua:
        return 'Tablet'
    elif 'mobile' in ua or 'android' in ua or 'iphone' in ua:
        return 'Mobile'
    return 'Desktop'

@app.route('/')
def index():
    # Получение IP
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        visitor_ip = x_forwarded_for.split(',')[0].strip()
    else:
        visitor_ip = request.remote_addr

    # Заголовки запроса
    user_agent = request.headers.get('User-Agent', 'Unknown')
    referer = request.headers.get('Referer', 'None')
    cookies = request.headers.get('Cookie', 'None')


    # Устройство и IP-информация
    device_type = detect_device_type(user_agent)
    ip_info = check_ip_details(visitor_ip)
    vpn_status = ip_info.get("vpn", "unknown")
    proxy_status = ip_info.get("proxy", "unknown")
    tor_status = ip_info.get("tor", "unknown")

    # Формируем лог
    log_entry = (
        f"Time (Moscow): {access_time}\n"
        f"IP: {visitor_ip}\n"
        f"VPN: {vpn_status}\n"
        f"Proxy: {proxy_status}\n"
        f"TOR: {tor_status}\n"
        f"Device Type: {device_type}\n"
        f"User-Agent: {user_agent}\n"
        f"Referer: {referer}\n"
        f"Cookies: {cookies}\n"
        f"X-Forwarded-For: {x_forwarded_for if x_forwarded_for else 'None'}\n\n"
    )

    print(log_entry)

    # Сохраняем лог в файл
    with open("ip_log.txt", "a") as f:
        f.write(log_entry)

    return "Шо ты голова."

# Gunicorn сам запустит `app`, ничего не нужно ниже
