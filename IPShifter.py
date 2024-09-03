# -*- coding: utf-8 -*-

import time
import os
import subprocess
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_and_install_package(package_name, install_command):
    """
    Check if a package is installed. If not, install it.
    """
    try:
        subprocess.check_output(f'dpkg -s {package_name}', shell=True)
    except subprocess.CalledProcessError:
        logging.info(f'{package_name} is not installed.')
        subprocess.check_output('sudo apt update', shell=True)
        subprocess.check_output(install_command, shell=True)
        logging.info(f'{package_name} installed successfully.')

def install_python_packages():
    """
    Ensure required Python packages are installed.
    """
    try:
        import requests
    except ImportError:
        logging.info('python3 requests is not installed.')
        os.system('pip3 install requests requests[socks]')
        logging.info('python3 requests is installed.')

def check_and_install_tor():
    """
    Check if Tor is installed. If not, install it.
    """
    check_and_install_package('tor', 'sudo apt install tor -y')

def ma_ip():
    """
    Fetch the current external IP address using Tor proxy.
    """
    url = 'https://api.ipify.org?format=text'  # Alternative URL
    proxies = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }
    try:
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()  # Raise HTTPError for bad responses
        logging.info(f'Fetched IP: {response.text.strip()}')
        return response.text.strip()
    except requests.RequestException as e:
        logging.error(f'Error fetching IP: {e}')
        return None

def change_ip():
    """
    Reload Tor service and print the new IP address.
    """
    os.system("sudo service tor reload")
    new_ip = ma_ip()
    if new_ip:
        logging.info(f'Your IP has been changed to: {new_ip}')
    else:
        logging.error('Failed to retrieve new IP.')

def main():
    """
    Main function to handle installation, starting services, and IP changes.
    """
    # Check and install required packages
    check_and_install_package('python3-pip', 'sudo apt install python3-pip -y')
    install_python_packages()
    check_and_install_tor()

    # Start Tor service
    os.system("sudo service tor start")

    # Welcome message
    print('''\033[1;32;40m
          
  _____ _____   _____ _     _  __ _            
|_   _|  __ \ / ____| |   (_)/ _| |           
  | | | |__) | (___ | |__  _| |_| |_ ___ _ __ 
  | | |  ___/ \___ \| '_ \| |  _| __/ _ \ '__|
 _| |_| |     ____) | | | | | | | ||  __/ |   
|_____|_|    |_____/|_| |_|_|_|  \__\___|_|  
                V 0.1
from Devin
''')
    print("\033[1;40;31 \n")
    
    time.sleep(3)
    print("\033[1;32;40m Change your SOCKS proxy to 127.0.0.1:9050\n")

    # Get user input for IP change intervals and count
    try:
        interval = int(input("[+] Time to change IP in seconds [type=60] >> "))
        count = int(input("[+] How many times do you want to change your IP [type=1000] for infinite IP changes type [0] >> "))

        if count == 0:
            while True:
                time.sleep(interval)
                change_ip()
        else:
            for _ in range(count):
                time.sleep(interval)
                change_ip()
    except ValueError:
        logging.error('Invalid input. Please enter numeric values.')
    except KeyboardInterrupt:
        logging.info('IPShifte is closed.')

if __name__ == "__main__":
    main()
