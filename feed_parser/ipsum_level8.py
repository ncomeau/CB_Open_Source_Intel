import csv
import time
import requests
import json

json_file = "feed_parser/feed_json/ipsum_level8.json"
#json_file = "feed_json/ipsum_level8.json"

url = "https://raw.githubusercontent.com/stamparm/ipsum/master/levels/8.txt"
ips = []
add_title = "Level 8 - NO REPORTED False Positives"

def get_intel(url):
    with requests.Session() as s:
        download = s.get(url)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            ips.append(row[0])
            print(row)

    create_json()

def create_json():
    report = []
    raw_ioc = []

    name = "ipsum_level8"
    owner = "ipsum"
    provider_url = "https://github.com/stamparm/ipsum"
    summary = "NO REPORTED FP - Highest Confidence\n\nIPsum is a threat intelligence feed based on 30+ different publicly available lists of suspicious and/or malicious IP addresses. All lists are automatically retrieved and parsed on a daily (24h) basis and the final result is pushed to this repository. List is made of IP addresses together with a total number of (black)list occurrence (for each). Greater the number, lesser the chance of false positive detection and/or dropping in (inbound) monitored traffic. Also, list is sorted from most (problematic) to least occurent IP addresses."
    category = "Open Source"

    id = name
    epoch = int(time.time())
    title = add_title
    description = "IPsum is a threat intelligence feed based on 30+ different publicly available lists of suspicious and/or malicious IP addresses. All lists are automatically retrieved and parsed on a daily (24h) basis and the final result is pushed to this repository. List is made of IP addresses together with a total number of (black)list occurrence (for each). Greater the number, lesser the chance of false positive detection and/or dropping in (inbound) monitored traffic. Also, list is sorted from most (problematic) to least occurent IP addresses."
    severity = 8

    for x in range(len(ips)):

        ioc = "netconn_ipv4:{}".format(ips[x])
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