import csv
import time
import requests
import json

json_file = "feed_parser/feed_json/abuse.ch_feodo.json"
url = "https://feodotracker.abuse.ch/downloads/ipblocklist.csv"
ips = []
ports = []
tags = []

def get_intel(url):
    with requests.Session() as s:
        download = s.get(url)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            if not "#" in str(row):
                if "dst_ip" not in str(row):
                    temp_tags = ["abuse.ch_feodo"]
                    ips.append(row[1])
                    ports.append(row[2])
                    temp_tags.append(row[5])
                    tags.append(temp_tags)
                    print(row)

    create_json()

def create_json():
    report = []
    raw_ioc = []

    name = "abuse.ch_feodo"
    owner = "abuse.ch"
    provider_url = "https://feodotracker.abuse.ch/blocklist/"
    summary = "Feodo Tracker is a project of abuse.ch with the goal of sharing botnet C&C servers associated with Dridex, Emotet (aka Heodo), TrickBot, QakBot (aka QuakBot / Qbot) and BazarLoader (aka BazarBackdoor). It offers various blocklists, helping network owners to protect their users from Dridex and Emotet/Heodo."
    category = "Open Source"

    id = name
    epoch = int(time.time())
    title = "abuse.ch Feodo Tracker Botnet C2 IP Blocklist"
    description = "Looking for IPv4 and Port botnet C&C servers associated with Dridex, Emotet (aka Heodo), TrickBot, QakBot (aka QuakBot / Qbot) and BazarLoader (aka BazarBackdoor)"
    severity = 5

    for x in range(len(ips)):

        ioc = "netconn_ipv4:{} AND netconn_port:{}".format(ips[x],ports[x])
        raw_ioc.append(ioc)
        report.append({"id":name+"_"+str(x),
                       "timestamp":epoch,
                       "tags": tags[x],
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