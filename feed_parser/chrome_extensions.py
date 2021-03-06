import csv
import time
import requests
import json

csv_file = "raw_content/suspect_chrome_extensions.csv"
json_file = "feed_json/Suspicious_Chrome_Extensions.json"

names = []
ids = []
risks = []

def get_intel(csv_file):
    with open(csv_file) as csvfile:
        reader = csv.reader(csvfile)
        next(csvfile)
        for row in reader:
            names.append(row[0])
            ids.append(row[1])
            risks.append(row[2])

        create_json()

def create_json():
    report = []

    name = "Suspicious_Chrome_Extensions"
    title = "suspicious_chrome_extensions"
    owner = "Nicholas Comeau"
    provider_url = "https://github.com/ncomeau"
    summary = "This feed contains curated queries looking for the registry and file mods associated with malicious, or suspect, Chrome Extensions. These Chrome Extensions are not definitively malicious, but have been reported by multiple security vendors and evangilists as potentially malicious, or have excessive permissions associated which could lead to exploitation for malintent. Please visit https://crxcavator.io/ to further validate permissions and risk associated with a specific Chrome Extension.\n\nThis feed was created by Nicholas Comeau, for the intended use to enrich data generated by Carbon Black Enterprise EDR. The risk scores are arbitary, but derived from perceived threat, based on crxacavtor risk scores and associated permissions.\n\nFalse positive rate unknown, but expected to be minimal."
    category = "Nicholas Comeau"

    epoch = int(time.time())
    description = "This feed contains curated queries looking for the registry and file mods associated with malicious, or suspect, Chrome Extensions. These Chrome Extensions are not definitively malicious, but have been reported by multiple security vendors and evangilists as potentially malicious, or have excessive permissions associated which could lead to exploitation for malintent. Please visit https://crxcavator.io/ to further validate permissions and risk associated with a specific Chrome Extension.\n\nThis feed was created by Nicholas Comeau, for the intended use to enrich data generated by Carbon Black Enterprise EDR. The risk scores are arbitary, but derived from perceived threat, based on crxacavtor risk scores and associated permissions.\n\nFalse positive rate unknown, but expected to be minimal."

    for x in range(len(names)):

        ioc = "process_name:chrome.exe AND (regmod_name:*{}* OR filemod_name:*{}*)".format(ids[x],ids[x])
        report.append({"id":title+"_"+str(x),
                       "timestamp":epoch,
                       "tags": [name,"chrome",names[x]],
                       "title":names[x],
                       "description": description,
                       "severity":int(risks[x]),
                       "iocs_v2":[{"id": title+"_"+str(x),
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
    get_intel(csv_file)

if __name__ == "__main__":
    main()