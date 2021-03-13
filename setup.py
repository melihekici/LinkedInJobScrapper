import os
import subprocess
import zipfile

os.system("pip install wordcloud urllib3 requests selenium beautifulsoup4")

command = "wmic datafile where name='C:\\\\Program Files (x86)\\\\Google\\\\Chrome\\\\Application\\\\chrome.exe' get Version /value"
command2 = "wmic datafile where name='C:\\\\Program Files (x86)\\\\Google\\\\Chrome\\\\Application\\\\chrome.exe' get Version /value"

import requests

def download_url(url, save_path, chunk_size=128):
    r=requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)

try:
    vers = subprocess.check_output(command)
    vers = int(str(vers).split("Version=")[1][0:2])
except:
    try:
        vers = subprocess.check_output(command2)
        vers = int(str(vers).split("Version=")[1][0:2])
    except:
        print("Can not find chrome. You need to download your chrome driver manually.")

if vers == 89:
    driver_link = "https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_win32.zip"
elif vers == 88:
    driver_link = "https://chromedriver.storage.googleapis.com/88.0.4324.96/chromedriver_win32.zip"
elif ver == 87:
    driver_link = "https://chromedriver.storage.googleapis.com/87.0.4280.88/chromedriver_win32.zip"

download_url(driver_link, "driver.zip")

with zipfile.ZipFile("driver.zip", "r") as zip_ref:
    zip_ref.extractall("./")

os.remove("driver.zip")

input("Kurulum Tamamlandı.\nÇıkmak için Enter'a basın.")