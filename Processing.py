import requests
from bs4 import BeautifulSoup
import os
from concurrent.futures import ThreadPoolExecutor
from handle_error import *

ask = input("give me the list: ")

def chek_file_stop(file):
    my_path = os.getcwd()
    list_file = os.listdir(my_path)
    
    if "stop.txt" in list_file:
        with open("stop.txt", "r") as tp:
            first_line = int(tp.readline().strip())
        
        with open(file, 'r') as fp:
            lines = fp.readlines()  # قراءة جميع السطور إلى قائمة
            
            # طباعة السطر الذي يبدأ منه
            print(f"Starting from line: {first_line}")
            
            # إرجاع السطور من السطر المحدد حتى النهاية
            return lines[first_line:], first_line
    else:
        with open(file, 'r') as fp:
            return fp.readlines(), 0

requests.urllib3.disable_warnings()

def check_upload_form(url, start_line):
    global ask
    try:
        null, _ = chek_file_stop(ask)
        for i, line in enumerate(null, start=start_line):
            print(f"{i}: {line.strip()}")
            save(i, 10)
           
            response = requests.get(url.rstrip(), timeout=10, allow_redirects=False, verify=False)
            soup = BeautifulSoup(response.content, 'html.parser')
            file_inputs = soup.find_all('input', {'type': 'file'})

            if file_inputs:
                print("it works.")
                with open("upload.txt", "a") as f:
                    print(url.rstrip(), file=f)
            else:
                print("not working")
    except Exception as e:
        print(f"Error: {e}")

urls, start_line = chek_file_stop(ask)
input_threads = int(input("how many threads do you want:"))
pool = ThreadPoolExecutor(input_threads)

for url in urls:
    pool.submit(check_upload_form, url, start_line)
