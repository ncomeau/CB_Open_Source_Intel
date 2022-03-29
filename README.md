# CB_Open_Source_Intel

CB Open-Source Intel is a tool created by Nicholas Comeau, for the intent of allowing easy import of a curated list of custom Threat Intel, to further enhance the robust capabilities of VMware Carbon Black's Enterprise EDR tool.

The intended use for this tool is predominately intel, but can be used in prospect or customer orgs as well.

Instructions for setup can be found below, as well as a full breakdown of the feeds associated, and the tool's core capabilities. It is worth noting, that if you are unable to setup the app on your own, for whatever reason, you can reach out to me (Nicholas Comeau) on Slack, provide the proper credentials, and I can add the Threat Intel Feeds of your choice for you!

A huge shoutout to those who have contributed to the feeds available, as well as the testing and development of the tool:

* Rob Eberhardt
* Jacob Barosin
* Patrick Mayer
* Mitchell Krane
* Karlee Lange
* Chris & Stacia Gelineau


**_Note:_** MacOS is the recommended OS, since it was developed on a Mac, and the UI is designed to render optimally on a Mac. However, recent updates to support Windows and Linux have been made on the ```win_linux``` branch - see [setup instructions](https://github.com/ncomeau/CB_Open_Source_Intel#setup-process) below for full details
## Videos

* **Short**_(ish)_ **Demo:**
    * https://www.youtube.com/watch?v=HGWENc_Gy-8
* **Full Demo:**
    * https://www.youtube.com/watch?v=NQAKKx-aI0o
# Updates
### Feature Additions
* 3/23/22 - ***Import Creds:***
   * Added additional module on the home page to allow for cred import
   * Process:
      * Select the new "Upload Creds" button - this will open a filechooser option which will open to the new "Credentials" directory
      * Import the desired creds text file - the same file will show you the required format
      * You may store multiple different credentials files - but one can house 1 set of credentials per file
      * Once selected it should auto-populate your creds in the applicable fields, and you should be able to hit submit, and be good to go!

### Feed Additions
* 3/24/22 - ***Russia-Ukraine IOCs Feed added:***
   * Roughly 3k IOCs, containing Domains, IPs, FQDNs, and Hashs that have been associated with the Russia-Ukraine conflict - from Orange Cyberdefense's github page
   * See feed description [below](https://github.com/ncomeau/CB_Open_Source_Intel#russia-ukraine-iocs)

### Bug Fixes/Cleanup
* 3/23/22 - ***Sanitize:***
   * Removed IOC from Mayer's Magic Queries that is FP prone
* 3/24/22 - ***Warning pop-up:***
   * Added a short pop-up window on the "Available Feeds" tab, which will notify the users that importing feeds can take up to ~15-30 seconds, and not to be alarmed if it appears as though the app is briefly is frozen, that is expected.  

### OS Support
* 3/24/22 - ***Windows & Linux Support:***
   * Alerted UI elements that rendered poorly on Windows & Linux, to be optimized for those respective platforms
   * See the [setup instructions](https://github.com/ncomeau/CB_Open_Source_Intel#setup-process) below for full details
   * Essentially, on install, simply reference the ```win_linux``` branch for those respective OSes

# Index

* [Updates](https://github.com/ncomeau/CB_Open_Source_Intel#updates)
* [Tool Overview](https://github.com/ncomeau/CB_Open_Source_Intel#tool-overview)
* [Setup & Install](https://github.com/ncomeau/CB_Open_Source_Intel#setup--install)
   * _[Requirements](https://github.com/ncomeau/CB_Open_Source_Intel#requirements)_
   * _[Setup Process](https://github.com/ncomeau/CB_Open_Source_Intel#setup-process)_
* [Feed Breakdown](https://github.com/ncomeau/CB_Open_Source_Intel#feed-breakdown)
   *  [CB TSO Custom Feeds](https://github.com/ncomeau/CB_Open_Source_Intel#cb-tso-custom-feeds)
      *  _[Suspicious Chrome Extensions](https://github.com/ncomeau/CB_Open_Source_Intel#suspicious-chrome-extensions)_
      *  _[Fuzzy Search Queries](https://github.com/ncomeau/CB_Open_Source_Intel#fuzzy-search-queries)_
      *  _[PCI DSS FIM](https://github.com/ncomeau/CB_Open_Source_Intel#pci-dss-fim)_
      *  _[Threat Hunting V2](https://github.com/ncomeau/CB_Open_Source_Intel#threat-hunting-v2)_
      *  _[SE Queries V2](https://github.com/ncomeau/CB_Open_Source_Intel#se-query-feed-v2)_
      *  _[Mayer's Magic Queries](https://github.com/ncomeau/CB_Open_Source_Intel#mayers-magic-queries)_
   *  [Open Source Feeds](https://github.com/ncomeau/CB_Open_Source_Intel#open-source-feeds)
      * _[Russia-Ukraine IOCs](https://github.com/ncomeau/CB_Open_Source_Intel#russia-ukraine-iocs)_
      * _[IPSUM Levels 5-8](https://github.com/ncomeau/CB_Open_Source_Intel#ipsum-levels-5-8)_
      * _[Abuse.ch Freodo Tracker](https://github.com/ncomeau/CB_Open_Source_Intel#abusech-freodo)_
      * _[Abuse.ch SSL BL](https://github.com/ncomeau/CB_Open_Source_Intel#abusech-ssl-bl)_
      * _[Cyber Cure Hashes](https://github.com/ncomeau/CB_Open_Source_Intel#cyber-cure-hashes)_
      * _[Malsilo IPv4](https://github.com/ncomeau/CB_Open_Source_Intel#malsilo-ipv4)_
      * _[Malsilo Domain](https://github.com/ncomeau/CB_Open_Source_Intel#malsilo-domain)_

* [CBR to EEDR Query Converter](https://github.com/ncomeau/CB_Open_Source_Intel#cbr-to-eedr-query-converter)

# Tool Overview

CB Open Source Intel is comprised of 3 core components;

* **Custom Threat Intel Import**
    * This component of the tool is far and away the focal point of the app.
    * This module encapsulates a combination of an open-source 3rd party threat intel, mostly from [MISP](https://www.misp-project.org/feeds/), as well as internal threat intel provided by a few individual contributors on the VMware Carbon Black team.
    * All of this is wrapped in a simple GUI, to allow for ease of importing this robust threat intel with a mere click of a button.
      * _**Note:** All of the Reports/IOCs are added, and tagged, as well. Thus, if you merely want to leverage the tool to import the intel, listed below, and then mix & match the reports/IOCs themselves into your very own custom Watch List, be my guest!_

* **Watchlist Management**
   * While the focal point of the tool is most certainly the importing of Threat Intel, I figured that being able to manage said imported threat intel might prove handy as well - enter Watchlist Management!
      * _For those of you unfamiliar with EEDR, a "Feed" is a collection of threat intelligence. However, when you enable a "Feed", either for alerting or overlay on the data in your unique environment, it then becomes a "Watchlist". Not all "Watchlists" come from "Feeds", as you can have custom created "Watchlists" - which is denoted by the "tools" icon in the app._
   * Given the above; not only does the app allow you to import the Threat Intel Feed, but you can enable those Threat Intel Feeds, as Watchlists, in your environment, directly from the app - as well as control the ability to enable and/or alert on ALL Threat Intel and Watchlists, available in your EEDR environment!

* **CBR to EEDR Query Converter**
   * Lastly, this is an optional module, whereby patrons of EDR (formerly CB Response/CBR) looking to migrate to EEDR, can very simply leverage the query converter API, report creation API, and Watchlist Creation API, with a simple push of a button - to convert any supported custom Watchlist you might have, into the EEDR equivalent!
      * _Full credit for this idea goes to Mitchell Krane - as well as several ideas for improvement to incorporate into a V2_

# Setup & Install

### Requirements
* Python 3+
   *  If an older version of python is being utilized - the app may run fine, but the threat intel update script will likely fail
   *  If desired, look within the CB_Open_Source_Intel.py script --> The "Feed" Class --> The "update_feed" function (around line 620)
* Kivy & KivyMD
   * This is the actual app GUI framework itself
* Pip/pip3
  * This is only required for pulling the correct kivy framework
* Only supported for orgs on Prod05
   * Could work on other backends, if the ```url_base``` variable in the CB_Open_Source_Intel.py script was updated (around line 32)
   * However, it has only been tested on Prod05
*  _(Optional/Recommended)_ Pycharm
   * As noted, this is optional - but recommended, should you want to make any alterations

**_Note:_** MacOS is the recommended OS, since it was developed on a Mac, and the UI is designed to render optimally on a Mac. However, recent updates to support Windows and Linux have been made on the ```win_linux``` branch - see [setup instructions](https://github.com/ncomeau/CB_Open_Source_Intel#setup-process) below for full details
### Setup Process
* Clone the full repo to your desired local location:
   *  <b><ins>For MacOS</ins></b>
      * ```git clone https://github.com/ncomeau/CB_Open_Source_Intel.git```
   *  <b><ins>For Windows or Linux</ins></b>
      * ```git clone -b win_linux https://github.com/ncomeau/CB_Open_Source_Intel.git```

* Install pip - if you don't already have it
  * ```curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py```
    * Could also be ```curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python get-pip.py``` depending on your python version/os

* Install Kivy (KivyMD is part of the git clone of this repo)  
   *  ```pip3 install "kivy[base]"```
       *  This may also be ```pip install "kivy[base]"``` depending on your pip version
   * **_Note:_** This has been tested and verified for Ubuntu and MacOS - However, Windows and other linux distros should work as expected, but not verified. For additional info on installation of kivy, see below:
     *  [Installing Kivy](https://kivy.org/doc/stable/gettingstarted/installation.html)

* In your CBC UI - create a API Key to utilize for the app:
   * In your console **\[Settings > API Access > Add API Key\]**
      * Access Level Type = "Custom"
      * Custom Access Level = A profile that has _at least_ all capabilities for "Custom Detections" field
   *  Your unique org_key can be found on \[Settings > API Access\] in the top left of the page
   *  See [Dev Rel Auth Docs](https://developer.carbonblack.com/reference/carbon-black-cloud/authentication/)

* Run the following command **from the dir where the script resides**:
  * ```python3 CB_Open_Source_Intel.py```
    * (Could also be ```python CB_Open_Source_Intel.py``` depending on python version/os)

* Input your EEDR API Creds & Org Key in the applicable fields within the app OR add your creds to the template file in the 'credentials' directory and easily upload from within the app, and you should be good to go!

# Feed Breakdown
Below you will find breakdowns on all feeds available for import - broken into feeds created by the CB Community, and those pulled from open source threat intel providers.
## CB TSO Custom Feeds
This is a compliation of threat intel feeds inspired or created by the Techincal Sales Org community, namely; myself (Nick Comeau), Rob Eberhardt, Patrick Mayer, Jake Barosin, and Kirk Hasty. These feeds span various topics, and can be utilized for a wide array of use-cases. Below you will find a description surrounding each feeds contents, and recommended alerting vs enabling viability.

<h3 align="center"><ins>Suspicious Chrome Extensions</ins></h3>

| Category   | Contents | Image |
| ---      | ---       | --- |
| **Author:** | Nick Comeau | |
| **Feed Description:** | This feed contains curated queries looking for the registry and file mods associated with malicious, or suspect, Chrome Extensions. Chrome Extensions are an often over-looked aspect of security, but can pose a significant threat. This remains a gap for most endpoint security solutions, as they do not have visibility into the Chrome Extensions themselves, rather than the process of Chrome. However, EEDR's robust visibility can identify Chrome Extension IDs being loaded, through looking at the associated registry and file modification events they generate. All that remains is overlaying intel on the robust data provided - enter the Suspicious Chrome Extensions Threat Intel Feed! | <img src="https://github.com/ncomeau/CB_Open_Source_Intel/blob/main/credit/nick_comeau_chrome_atlas.png" width="82"> |
| **Alerting:** |  This feed should be minimally false positive prone, and should be viable for alerting.| |

 * These Chrome Extensions are not definitively malicious, but have been reported by multiple security vendors and evangilists as potentially malicious, or have excessive permissions associated which could lead to exploitation for malintent.
 * Each of these Chrome Extensions have been checked against Duo's open-source project, [crxcavator](https://crxcavator.io/), to validate the potential threat.

<h3 align="center"><ins>Fuzzy Search Queries</ins></h3>

| Category     | Contents | Image |
| ---      | ---       | --- |
| **Author:** | Nicholas Comeau | |
| **Feed Description:** | This feed contains curated queries looking for potential masquerading, through leveraging Carbon Black's Fuzzy Searching capability to look for applications which look like common processes, but the name differs by 1 character from the expected name. Imagine trying to figure out if the powershell instance you are seeing running in task manager is actually powershell.exe, or if it has a capital "I" instead of a lower-case "l". Well worry no longer - this threat intel feed, combined with the robust data EEDR gathers, and the powerful "fuzzy searching" capability it provides, allows you to quickly and easily cut through the noise, and see what processes are real, and which are imposters!  | <img src="https://github.com/ncomeau/CB_Open_Source_Intel/blob/main/credit/nick_comeau_fuzzy_search.png" width="82"> |
| **Alerting:** | This feed should be minimally false positive prone, and should be viable for alerting. Obviously, this can vary per environment, and if there is a false positive, it should manifest quickly, and you can simply disable that specific report and/or edit the IOC to exclude the specified process generating the FP.| |

 * This feed was created with contributions from Jacob Barosin and Kirk Hasty.


<h3 align="center"><ins>PCI DSS FIM</ins></h3>

| Category     | Contents | Image |
| ---      | ---       | --- |
| **Author:** | Rob Eberhardt | |
| **Feed Description:** | This feed is a collection of critical Windows files that should be monitored for modification under PCI DSS requirement 11.5.  Please note that this feed is not provided by Carbon Black, and is simply a starting point for monitoring Windows file modifications per the PCI DSS spec.  Please consult with your QSA for potential exclusions or additions. | <img src="https://github.com/ncomeau/CB_Open_Source_Intel/blob/main/logos/PCI_DSS_Rob_Eberhardt.png" width="82"> |
| **Alerting:** | Do not alert - simply enable for overlay and context.  | |

<h3 align="center"><ins>Threat Hunting V2</ins></h3>

| Category     | Contents | Image |
| ---      | ---       | --- |
| **Author:** | Rob Eberhardt | |
| **Feed Description:** | Do you want to become a threat hunting pro, but are not sure where to start? Well fear not, admin, for Rob's threat-hunting building blocks can take you from a threat-zero to a threat-hero! _(Ok, I'll even admit that was lame, I wrote this except - Rob wrote the not lame part; all of the Feed contents.)_ | <img src="https://github.com/ncomeau/CB_Open_Source_Intel/blob/main/credit/Rob_Eberhardt.jpeg" width="82"> |
| **Alerting:** | Do not alert - simply enable for overlay and context, to leverage as a starting point for threathunting. | |

<h3 align="center"><ins>SE Query Feed V2</ins></h3>

| Category     | Contents | Image |
| ---      | ---       | --- |
| **Author:** | Rob Eberhardt | |
| **Feed Description:** | This feed is comprised of an amalgamation of queries generated by the Carbon Black SE community. These queries have a wide range of applicability, looking for everything from notepad spawning child processes, to executions from the temp directory with a high volume of netconns. The expertise of the SE community can be seen within this feed, and can be a great starting point for identifying anomalous behavior within your environment. | <img src="https://github.com/ncomeau/CB_Open_Source_Intel/blob/main/credit/Rob_Eberhardt.jpeg" width="82"> |
| **Alerting:** | The alerting fidelity of this feed can vary. It is recommended to initially enable this feed, and tune accordingly prior to alerting. | |

<h3 align="center"><ins>Mayer's Magic Queries</ins></h3>

| Category     | Contents | Image |
| ---      | ---       | --- |
| **Author:** | Patrick Mayer | |
| **Feed Description:** | This feed is comprised of curated queries provided by EEDR Wizard Patrick Mayer, on the Carbon Black SE team. This feed contains queries ranging from threat-hunting building blocks, to more high fidelity malicious activity IOCs. All Reports/IOCs are tagged based on category of query, and the name of the report, for custom WL generation based on the core query content. | <img src="https://github.com/ncomeau/CB_Open_Source_Intel/blob/main/credit/patrick_mayer_wizard.png" width="82"> |
| **Alerting:** | The vast majority of these queries would be viable for alerting. However, there are several which are intended for threat hunting building blocks, and some which may be false positive prone based on the environment. That said; it is recommended to simply enable at first, and then progress towards alerting after some minor tuning relative to your unique environment. | |



_If you have some swanky threat intel you wish to add, and have me create a hilarious thumbnail of your face, please reach out to me directly on Slack (Nicholas Comeau)_

## Open Source Feeds

<h3 align="center"><ins>Russia-Ukraine IOCs</ins></h3>

| Category     | Contents | Image |
| ---      | ---       | --- |
| **Author:** | https://github.com/Orange-Cyberdefense/russia-ukraine_IOCs | |
| **Feed Description:** | Orange Cyberdefense CERT share here IOCs related to war against Ukraine extracted from our Datalake Threat Intelligence platform. Those IOC are collected automatically and provided to you without any prior verification. Updated on-demand in the app, by pulling from the source IOCs listed in the 'author' section.| <img src="https://github.com/ncomeau/CB_Open_Source_Intel/blob/main/logos/ukraine.png" width="82"> |
| **Alerting:** | FP Rate unknown - but should be viable for alerting. Minor tuning may be advised. | |

<h3 align="center"><ins>IPSUM Levels 5-8</ins></h3>

| Category     | Contents | Image |
| ---      | ---       | --- |
| **Author:** | https://github.com/stamparm/ipsum | |
| **Feed Description:** | IPsum is a threat intelligence feed based on 30+ different publicly available lists of suspicious and/or malicious IP addresses. The "levels" simply indicate the number of these publically available feeds that the IP address in question. For instance; IPSUM Level 6 means that the IPs on this list have been seen on _at least_ 6 publically available threat intel feeds. Thus, there will be some redundancy between feeds, and the higher "level" the higher confidence of the feed. The raw feeds that this feed derives from are updated on a daily basis, and can be updated on-demand within the EEDR Feed Manager app.| <img src="https://github.com/ncomeau/CB_Open_Source_Intel/blob/main/logos/misp.png" width="82"> |
| **Alerting:** | Alerting recommended, the higher the "level" the less likely FP prone it will be. | |

<h3 align="center"><ins>Abuse.ch Freodo</ins></h3>

| Category     | Contents | Image |
| ---      | ---       | --- |
| **Author:** | https://feodotracker.abuse.ch/blocklist/ | |
| **Feed Description:** | Feodo Tracker is a project of abuse.ch with the goal of sharing botnet C&C servers (IPV4 & Port) associated with Dridex, Emotet (aka Heodo), TrickBot, QakBot (aka QuakBot / Qbot) and BazarLoader (aka BazarBackdoor). It offers various blocklists, helping network owners to protect their users from Dridex and Emotet/Heodo. Updated on-demand in the app.| <img src="https://github.com/ncomeau/CB_Open_Source_Intel/blob/main/logos/abuse.png" width="82"> |
| **Alerting:** | FP Rate unknown - butshould be viable for alerting. Minor tuning may be advised. | |

<h3 align="center"><ins>Abuse.ch SSL BL</ins></h3>

| Category     | Contents | Image |
| ---      | ---       | --- |
| **Author:** | https://sslbl.abuse.ch/ | |
| **Feed Description:** | An open source Feed from abuse.ch, looking for SSLBL Botnet C2 IP Blacklist's. The SSL Blacklist (SSLBL) is a project of abuse.ch with the goal of detecting malicious SSL connections, by identifying and blacklisting SSL certificates used by botnet C&C servers. In addition, SSLBL identifies JA3 fingerprints that helps you to detect & block malware botnet C&C communication on the TCP layer. abuse.ch is a research project at the Bern University of Applied Sciences (BFH). Updated on-demand in the app. | <img src="https://github.com/ncomeau/CB_Open_Source_Intel/blob/main/logos/abuse.png" width="82"> |
| **Alerting:** | FP Rate unknown - but should be viable for alerting. Minor tuning may be advised. | |


<h3 align="center"><ins>Cyber Cure Hashes</ins></h3>

| Category     | Contents | Image |
| ---      | ---       | --- |
| **Author:** | http://www.cybercure.ai/ | |
| **Feed Description:** | Cyber Cure established to share cyber intelligence with small and medium networks as well as with home users. Cyber Cure offers several indicators that are being collected from the internet and provided by commercial vendors running honeypots and honeynets. Using Cyber Cure, users can block and/or identify malware and threats, the data can be integrated with many popular vendors products and can be easily adjust to many others that supports the standards. The Cyber Cure Feed is updated on demand in the app. | <img src="https://github.com/ncomeau/CB_Open_Source_Intel/blob/main/logos/cybercure.jpg" width="82"> |
| **Alerting:** | FP Rate unknown - but should be viable for alerting, given the 1-to-1 hash match. | |


<h3 align="center"><ins>Malsilo IPv4</ins></h3>

| Category     | Contents | Image |
| ---      | ---       | --- |
| **Author:** | https://malsilo.gitlab.io/ | |
| **Feed Description:** | Malsilo is an open source threat intel feed used in a variety of threat intel platforms. The following feed contains ips (v4) and their associated ports that have been observed in correlation with known attacks. These attacks can be found in the 'tags' section of the report. Updated on-demand in the app. | <img src="https://github.com/ncomeau/CB_Open_Source_Intel/blob/main/logos/misp.png" width="82"> |
| **Alerting:** | FP Rate unknown - butshould be viable for alerting. Minor tuning may be advised. | |

<h3 align="center"><ins>Malsilo Domain</ins></h3>

| Category     | Contents | Image |
| ---      | ---       | --- |
| **Author:** | https://malsilo.gitlab.io/ | |
| **Feed Description:** | Malsilo is an open source threat intel feed used in a variety of threat intel platforms. The following feed contains domains that have been observed in correlation with known attacks. These attacks can be found in the 'tags' section of the report. Updated on-demand in the app. | <img src="https://github.com/ncomeau/CB_Open_Source_Intel/blob/main/logos/misp.png" width="82"> |
| **Alerting:** |  FP Rate unknown - butshould be viable for alerting. Minor tuning may be advised. | |


# CBR to EEDR Query Converter

As noted above, this is an optional module, which can be toggled on during the login screen. When toggled on, this will dynamically update the UI to create a new page, for enabling conversion of a legacy EDR (formerly Carbon Black Response/CBR) to the EEDR equivalent.

* On this page, you have 2 options:
   * Convert a single CBR query into it's its EEDR equivalent, and create a Watch List for this specific Report/IOC
   * Convert a single CBR query into it's its EEDR equivalent, and append the Report/IOC to a specifed custom Watch List
      * _It is under future consideration to add a third option, for bulk uploading CBR queries for conversion, but not currently available_

It is important to note, that although custom error handling was adding into this module, the efficacy of conversion is still predicated on the [Legacy Query Conversion API](https://developer.carbonblack.com/reference/carbon-black-cloud/cb-threathunter/latest/feed-api/#create-a-new-private-feed), and as such, there are limitations. However, it is meant to encapsulate a simple method to leverage that API route, and turn it into immediate tangible output, through combination with the Report creation, and Watch List creation APIs.

Once again; full credit for the idea behind this module goes to Mitchell Krane!
