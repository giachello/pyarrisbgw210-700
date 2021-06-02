import bs4

from bs4 import BeautifulSoup
import httpx

import requests

def get_devices():
    devices_page = requests.get("http://192.168.1.254/cgi-bin/devices.ha")

    soup = BeautifulSoup(devices_page.content, "html.parser")

    table = soup.find(class_="table100")
    rows = table.find_all('tr')

    devices = list()
    device = dict()

    for row in rows:
        header = row.find("th")
        cell = row.find("td")
        if (header is None):
            devices.append(device)
            device = dict()
        else:
            h = header.get_text().strip("\n")
            c = cell.get_text().strip("\n")
            device[h]= c
            if (h == "IPv4 Address / Name"):
                device["IPv4 Address"] = c.split("/")[0].strip("\n ")
                device["Name"] = c.split("/")[1].strip("\n ")

    devices.append(device)

    return devices


def get_statistics():
    statistics_page = requests.get("http://192.168.1.254/cgi-bin/lanstatistics.ha")

    soup = BeautifulSoup(statistics_page.content, "html.parser")

    table = soup.find(class_="table100 grid")
    rows = table.find_all('tr')

    headers = rows[0].find_all("th")
    header_names = list()
    for h in headers:
        header_names.append(h.get_text().strip())

    statistics = list()

    for row in rows:
        cells = row.find_all("td")
        i = 0
        statistic = dict()
        for c in cells:
            statistic[header_names[i]] = c.get_text().strip()
            i = i + 1
        if len(statistic)>0: 
            statistics.append(statistic)

    return statistics

devices = get_devices()

for d in devices:
    print(d["MAC Address"]+" "+d["Name"])

print()

statistics = get_statistics()

for s in statistics:
    print(s["MAC Address"]+" "+s["Receive Bytes"])

print()

for s in statistics:
    print(s["MAC Address"]+" "+next((l for l in devices if l['MAC Address'] == s["MAC Address"]), None)["Name"] + " " + s["Receive Bytes"])

