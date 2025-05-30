from flask import Flask, request
from datetime import datetime
import os
import requests

app = Flask(__name__)

def check_ip_details(ip):
    api_key = 'YOUR_API_KEY'
    url = f'https://ipqualityscore.com/api/json/ip/{api_key}/{ip}'
    response = requests.get(url)
    return response.json()

def detect_device_type(user_agent):
    ua = user_agent.lower()
    if 'tablet' in ua or 'ipad' in ua:
        return 'Tablet'
    elif 'mobile' in ua or 'android' in ua or 'iphone' in ua:
        return 'Mobile'
    return 'Desktop'

@app.route('/')
def index():
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        visitor_ip = x_forwarded_for.split(',')[0].strip()
    else:
        visitor_ip = request.remote_addr

    user_agent = request.headers.get('User-Agent', 'Unknown')
    referer = request.headers.get('Referer', 'None')
    cookies = request.headers.get('Cookie', 'None')
    access_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    device_type = detect_device_type(user_agent)

    log_entry = (
        f"Time: {access_time}\n"
        f"IP: {visitor_ip}\n"
        f"Device Type: {device_type}\n"
        f"User-Agent: {user_agent}\n"
        f"Referer: {referer}\n"
        f"Cookies: {cookies}\n"
        f"X-Forwarded-For: {x_forwarded_for if x_forwarded_for else 'None'}\n\n"
    )

    print(log_entry)

    with open("ip_log.txt", "a") as f:
        f.write(log_entry)

    return "Шо ты голова."
