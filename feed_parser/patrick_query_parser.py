import csv
import time
import json

csv_file = "raw_content/Patricks_Queries_v3.csv"
json_file = "feed_json/Mayers_Magic_Queries.json"
names = []
queries = []
risks = []
tags = []
names1 = []
queries1 = []
risks1 = []
tags1 = []
# Simple formatting function for Feed parsing
def query_format(list1):
    return str(list1).replace("\n", "").replace(" or ", " OR ").replace(" and ", " AND ")

# Issue with a query between 1-10
# Issue with queries with \"
# Issue with queries - not anything else...since no ioc_v2 works

# 19-40 is good
# 40-50 is bad
# 50+ is good

def get_intel(csv_file):
    with open(csv_file) as csvfile:
        reader = csv.reader(csvfile)
        next(csvfile)
        for row in reader:
            names.append(row[0])
            queries.append(query_format(row[1]))
            risks.append(row[2])
            tags.append(row[3])



        create_json()

def create_json():
    report = []

    name = "Mayers_Magic_Queries"
    title = "mayers_magic_queries"
    owner = "Patrick Mayer"
    provider_url = "https://github.com/carbonblack/community"
    summary = "This feed is comprised of curated queries provided by Patrick Mayer, on the Carbon Black SE team. This feed contains queries ranging from threat-hunting building blocks, to more high fidelity malicious activity IOCs. All Reports/IOCs are tagged based on category of query, and the name of the report, for custom WL generation based on the core query content.\n\nThis feed would likely require tuning of some of the more threat-hunting-centric queries before being viable for alerting. Enabling for overlay context and tuning recommended."
    category = "Patrick Mayer"

    epoch = int(time.time())
    description = "This feed is comprised of curated queries provided by Patrick Mayer, on the Carbon Black SE team. This feed contains queries ranging from threat-hunting building blocks, to more high fidelity malicious activity IOCs. All Reports/IOCs are tagged based on category of query, and the name of the report, for custom WL generation based on the core query content.\n\nThis feed would likely require tuning of some of the more threat-hunting-centric queries before being viable for alerting. Enabling for overlay context and tuning recommended."

    for x in range(len(names)):

        ioc = "{}".format(queries[x])
        report.append({"id":title+"_"+str(x),
                       "timestamp":epoch,
                       "tags": [name,names[x], tags[x]],
                       "title":names[x],
                       "description": description,
                       "severity":int(risks[x]),
                       "iocs_v2":[{"id": name+"_"+str(epoch)+str(x),
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