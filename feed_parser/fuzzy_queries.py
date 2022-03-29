import csv
import time
import json

csv_file = "raw_content/fuzzy_search_queries.csv"
json_file = "feed_json/Fuzzy_Search_Queries.json"

app = []
risk = []

def get_intel(csv_file):
    with open(csv_file) as csvfile:
        reader = csv.reader(csvfile)
        next(csvfile)
        for row in reader:
            print(row)
            app.append(row[0])
            risk.append(row[1])

        create_json()
def create_json():
    report = []

    name = "Fuzzy_Search_Queries"
    title = "fuzzy_search"
    owner = "Nicholas Comeau"
    provider_url = "https://github.com/ncomeau"
    summary = "This feed contains curated queries looking for potential masquerading, through leveraging Carbon Black's Fuzzy Searching capability to look for common applications where the name differs by 1 character from the expected name.\n\nThis feed was created with contributions from Nicholas Comeau, Jacob Barosin, and Kirk Hasty.\n\nFP rate should be minimal, but could vary based on envrionment."
    category = "Nicholas Comeau-Jacob Barosin-Kirk Hasty"

    epoch = int(time.time())
    description = "This feed contains curated queries looking for potential masquerading, through leveraging Carbon Black's Fuzzy Searching capability to look for common applications where the name differs by 1 character from the expected name.\n\nThis feed was created with contributions from Nicholas Comeau, Jacob Barosin, and Kirk Hasty.\n\nFP rate should be minimal, but could vary based on envrionment."

    for x in range(len(app)):

        ioc = "process_name:{}~1 AND NOT process_name:{}".format(app[x],app[x])
        report.append({"id":title+"_"+str(x),
                       "timestamp":epoch,
                       "tags": [app[x],"fuzzy","masquerading"],
                       "title":app[x] + " potential masquerading",
                       "description": description,
                       "severity":int(risk[x]),
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