import csv
import time
import requests
import json

json_file = "feed_parser/feed_json/abuse.ch_ssl.json"
url = "https://sslbl.abuse.ch/blacklist/sslipblacklist.csv"
ips = []
ports = []


def get_intel(url):
    with requests.Session() as s:
        download = s.get(url)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            if not "#" in str(row):
                ips.append(row[1])
                ports.append(row[2])
                print(row)

    create_json()

def create_json():
    report = []
    raw_ioc = []

    name = "abuse.ch_ssl"
    owner = "abuse.ch"
    provider_url = "https://sslbl.abuse.ch/"
    summary = "An open source Feed from abuse.ch, looking for SSLBL Botnet C2 IP Blacklist's. abuse.ch is a research project at the Bern University of Applied Sciences (BFH). It is the home of a couple of projects that are helping internet service providers and network operators protecting their infrastructure from malware. IT-Security researchers, vendors and law enforcement agencies rely on data from abuse.ch, trying to make the internet a safer place."
    category = "Open Source"

    id = name
    epoch = int(time.time())
    title = "abuse.ch SSLBL Botnet C2 IP Blacklist"
    description = "Looking for IPv4 and Port associated with SSLBL Botnet C2"
    severity = 5

    for x in range(len(ips)):

        ioc = "netconn_ipv4:{} AND netconn_port:{}".format(ips[x],ports[x])
        raw_ioc.append(ioc)
        report.append({"id":name+"_"+str(x),
                       "timestamp":epoch,
                       "tags": [name],
                       "title":title,
                       "description": description,
                       "severity":severity,
                       "iocs_v2":[{"id": name+"_"+str(x),
                                  "match_type": "query",
                                  "values": [ioc]
                                   }]})
    body = {
        "feedinfo": {
            "name": name,
            "owner": owner,
            "provider_url": provider_url,
            "summary": summary,
            "category": category,
        },
        "reports": report
    }

    with open(json_file, 'w+', encoding='utf-8') as d:
        json.dump(body, d, ensure_ascii=False, indent=4)
        d.close()

def main():
    get_intel(url)

if __name__ == "__main__":
    main()