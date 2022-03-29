import csv
import time
import requests
import json

json_file = "feed_parser/feed_json/cybercure_hashes.json"
#json_file = "feed_json/cybercure_hashes.json"

url = "https://api.cybercure.ai/feed/get_hash?type=csv"
hashes = []
add_title = "Malsilo potential domains"

def get_intel(url):
    with requests.Session() as s:
        download = s.get(url)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        print(my_list)
        for row in my_list:
            for x in row:
                hashes.append(x)

    print(hashes)

    create_json()

def create_json():
    report = []
    raw_ioc = []

    name = "cybercure_hashes"
    owner = "cybercure"
    provider_url = "http://www.cybercure.ai/"
    summary = "Cyber Cure established to share cyber intelligence with small and medium networks as well as with home users.\nCyber Cure offers several indicators that are being collected from the internet and provided by commercial vendors running honeypots and honeynets.\nYou can check the status page to see our current coverage of honeypot installations around the world at uptime.cybercure.ai Using Cyber Cure users can block and/or identify malware and threats, the data can be integrated with many popular vendors products and can be easily adjust to many others that supports the standards.\nCyber Cure Free is updated every several hours while Cyber Cure Premium is being updated every 10 minutes with new indicators and data.\n\nFP Rate Unknown."
    category = "Open Source"

    id = name
    epoch = int(time.time())
    title = add_title
    description = "Cyber Cure established to share cyber intelligence with small and medium networks as well as with home users.\nCyber Cure offers several indicators that are being collected from the internet and provided by commercial vendors running honeypots and honeynets.\nYou can check the status page to see our current coverage of honeypot installations around the world at uptime.cybercure.ai Using Cyber Cure users can block and/or identify malware and threats, the data can be integrated with many popular vendors products and can be easily adjust to many others that supports the standards.\nCyber Cure Free is updated every several hours while Cyber Cure Premium is being updated every 10 minutes with new indicators and data.\n\nFP Rate Unknown."
    severity = 5

    for x in range(len(hashes)):

        ioc = "hash:{}".format(hashes[x])
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