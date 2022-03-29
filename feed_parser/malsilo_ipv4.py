import csv
import time
import requests
import json

json_file = "feed_parser/feed_json/malsilo_ipv4.json"
#json_file = "feed_json/malsilo_ipv4.json"

url = "https://malsilo.gitlab.io/feeds/dumps/ip_list.txt"
ips = []
ports = []
tags = []
add_title = "Malsilo potential malicious ips and ports"

def get_intel(url):
    with requests.Session() as s:
        download = s.get(url)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            if not "#" in str(row):
                if len(row) != 0:
                    temp_tags = ["malsilo_ipv4"]
                    split_test = row[2].split(":")
                    ips.append(split_test[0])
                    ports.append(split_test[1])
                    temp_tags.append(row[3])
                    tags.append(temp_tags)

        print(len(ips))
        print(len(ports))
        print(len(tags))
        print(tags)

    create_json()

def create_json():
    report = []
    raw_ioc = []

    name = "malsilo_ipv4"
    owner = "malsilo"
    provider_url = "https://malsilo.gitlab.io/"
    summary = "Malsilo is an open source threat intel feed used in a variety of threat intel platforms. The following feed contains ips (v4) and their associated ports that have been observed in correlation with known attacks. These attacks can be found in the 'tags' section of the report.\n\nFP Rate Unknown."
    category = "Open Source"

    id = name
    epoch = int(time.time())
    title = add_title
    description = "Malsilo is an open source threat intel feed used in a variety of threat intel platforms. The following feed contains ips (v4) and their associated ports that have been observed in correlation with known attacks. These attacks can be found in the 'tags' section of the report.\n\nFP Rate Unknown."
    severity = 5

    for x in range(len(ips)):

        ioc = "netconn_ipv4:{} AND netconn_port:{}".format(ips[x],ports[x])
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