import csv
import time
import requests
import json

json_file = "feed_parser/feed_json/Russia_Ukraine_IOCs.json"
#json_file = "feed_json/Russia_Ukraine_IOCs.json"

url = "https://raw.githubusercontent.com/Orange-Cyberdefense/russia-ukraine_IOCs/main/OCD-Datalake-russia-ukraine_IOCs-ALL.csv"
type = []
iocs = []
tags = []
base_tags = ["russia", "ukraine", "russia_ukraine_iocs"]

add_title = "Russia-Ukraine IOCs"
def remove_quotes(list1):
    return str(list1).replace('"','').replace('[','').replace(']','').replace(' ', '').replace("'","").split(",")
def get_intel(url):
    with requests.Session() as s:
        download = s.get(url)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            temp_tags = remove_quotes(row[6])
            type.append(row[0])
            iocs.append(row[1])
            for x in base_tags:
                temp_tags.append(x)
            tags.append(temp_tags)
            print(row)

    create_json()

def create_json():
    report = []
    raw_ioc = []

    name = "Russia_Ukraine_IOCs"
    owner = "Orange-Cyberdefense"
    provider_url = "https://github.com/Orange-Cyberdefense/russia-ukraine_IOCs"
    summary = "Orange Cyberdefense CERT share here IOCs related to war against Ukraine extracted from our Datalake Threat Intelligence platform. Those IOC are collected automatically and provided to you without any prior verification.\n\n FP Rate Unknown - but should be viable for alerting, pending potential tuning. Updated on-demand within the app."
    category = "Open Source"

    id = name
    epoch = int(time.time())
    title = add_title
    description = "Orange Cyberdefense CERT share here IOCs related to war against Ukraine extracted from our Datalake Threat Intelligence platform. Those IOC are collected automatically and provided to you without any prior verification.\n\n FP Rate Unknown - but should be viable for alerting, pending potential tuning. Updated on-demand within the app."
    severity = 7

    for x in range(len(type)):
        if type[x] == "domain":
            ioc = "netconn_domain:{}".format(iocs[x])
            raw_ioc.append(ioc)
            report.append({"id": name + "_" + str(x),
                           "timestamp": epoch,
                           "tags": tags[x],
                           "title": "Connections to {}".format(iocs[x]),
                           "description": description,
                           "severity": severity,
                           "iocs_v2": [{"id": name + "_" + str(x),
                                        "match_type": "query",
                                        "values": [ioc]
                                        }]})
        if type[x] == "file":
            ioc = "hash:{} OR filemod_hash:{}".format(iocs[x],iocs[x])
            raw_ioc.append(ioc)
            report.append({"id": name + "_" + str(x),
                           "timestamp": epoch,
                           "tags": tags[x],
                           "title": "Suspicious hash detected",
                           "description": description,
                           "severity": 9,
                           "iocs_v2": [{"id": name + "_" + str(x),
                                        "match_type": "query",
                                        "values": [ioc]
                                        }]})
        if type[x] == "fqdn":
            ioc = "netconn_domain:{}".format(iocs[x])
            raw_ioc.append(ioc)
            report.append({"id": name + "_" + str(x),
                           "timestamp": epoch,
                           "tags": tags[x],
                           "title": "Connections to {}".format(iocs[x]),
                           "description": description,
                           "severity": severity,
                           "iocs_v2": [{"id": name + "_" + str(x),
                                        "match_type": "query",
                                        "values": [ioc]
                                        }]})
        if type[x] == "ip":
            ioc = "netconn_ipv4:{}".format(iocs[x])
            raw_ioc.append(ioc)
            report.append({"id": name + "_" + str(x),
                           "timestamp": epoch,
                           "tags": tags[x],
                           "title": "Connections to suspicious IP: {}".format(iocs[x]),
                           "description": description,
                           "severity": 5,
                           "iocs_v2": [{"id": name + "_" + str(x),
                                        "match_type": "query",
                                        "values": [ioc]
                                        }]})
        else:
            pass

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