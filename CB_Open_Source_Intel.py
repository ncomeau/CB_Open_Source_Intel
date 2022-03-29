import json
import os
from os import listdir
from os.path import isfile, join
import time
import configparser

from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.tab import MDTabsBase
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.button import MDFlatButton,MDRoundFlatIconButton, MDFillRoundFlatIconButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.label import MDLabel
from kivymd.uix.tooltip import MDTooltip
from kivymd.uix.list import OneLineAvatarIconListItem
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.filemanager import MDFileManager


import requests

### Lists for storing and dedouping ###
final_api_key = []
final_api_id = []
final_org_key = []
url_base = "https://defense-prod05.conferdeploy.net"
nav_dedoup = []
nav_dedoup2 = []
nav_dedoup3 = []
nav_dedoup_home = []
cbr_active = []
cbr_active_nav = []

# Simple formatting function for Feed parsing & Cred Upload Input
def feed_format(list1):
    return str(list1).replace(".json", "")
def no_quotes(list1):
    return str(list1).replace("'","").replace('"','')
### Classes for App Objects ###
class ContentNavigationDrawer(BoxLayout):
    pass

class MyScreenManager(ScreenManager):
    pass

class Tab(FloatLayout,MDTabsBase):
    pass

class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()

class ActiveCBR(MDRelativeLayout):
    text = StringProperty()
    secondary_text = StringProperty()
    icon = StringProperty()

class GetInfoBtn(MDRelativeLayout):
    text = StringProperty()
    secondary_text = StringProperty()
    icon = StringProperty()

class InfoUpdateDeleteBtn(MDRelativeLayout):
    text = StringProperty()
    secondary_text = StringProperty()
    icon = StringProperty()

class InfoDeleteBtn(MDRelativeLayout):
    text = StringProperty()
    secondary_text = StringProperty()
    icon = StringProperty()

class InfoDeleteCreditBtn(MDRelativeLayout):
    text = StringProperty()
    secondary_text = StringProperty()
    icon = StringProperty()
    def props(self, name):
        if "Rob_Eberhardt" in name:
            Snackbar(text="Feed Author Credit: Rob Eberhardt").open()
        elif "fuzzy" in name:
            Snackbar(text="Feed Author Credit: Nicholas Comeau, Jacob Barosin, & Kirk Hasty").open()
        elif "nick_comeau" in name:
            Snackbar(text="Feed Author Credit: Nicholas Comeau").open()
        elif "patrick_mayer" in name:
            Snackbar(text="Feed Author Credit: Patrick Mayer").open()

class ImportBtn(MDRelativeLayout):
    text = StringProperty()
    secondary_text = StringProperty()
    icon = StringProperty()

class ImportCreditBtn(MDRelativeLayout):
    text = StringProperty()
    secondary_text = StringProperty()
    icon = StringProperty()
    def props(self, name):
        if "Rob_Eberhardt" in name:
            Snackbar(text="Feed Author Credit: Rob Eberhardt").open()
        elif "fuzzy" in name:
            Snackbar(text="Feed Author Credit: Nicholas Comeau, Jacob Barosin, & Kirk Hasty").open()
        elif "nick_comeau" in name:
            Snackbar(text="Feed Author Credit: Nicholas Comeau").open()
        elif "patrick_mayer" in name:
            Snackbar(text="Feed Author Credit: Patrick Mayer").open()


class FeedBtn(MDRelativeLayout):
    text = StringProperty()
    secondary_text = StringProperty()
    icon = StringProperty()

class WatchlistBtn(MDRelativeLayout):
    text = StringProperty()
    secondary_text = StringProperty()
    icon = StringProperty()

class TooltipMDIconButton(MDIconButton, MDTooltip):
    pass

class CBRBtn(MDRelativeLayout):
    pass

class NoCBR(MDRelativeLayout):
    pass

class CBRNav(MDRelativeLayout):
    pass

class Item(OneLineAvatarIconListItem):
    left_icon = StringProperty()

### APP PAGES & API FUNCTIONS ###
class Home(Screen):
    def __init__(self, name, sm):
        """
        Init the sub-class and Screen super class.
        :param name:
        :param sm:
        """
        super().__init__() # Python3
        self.sm = sm
    def initWindow(self):

        if len(cbr_active) != 0:
            self.ids.layout.add_widget(CBRBtn())
            self.initNav()
            #self.basic_nav.ids.nav_content.ids.container.add_widget(CBRNav())
            #cbr_active_nav.append("active")

        else:
            self.ids.layout.add_widget(NoCBR())
            self.initNav()

    def initNav(self):
        if len(nav_dedoup_home) == 0:
            self.basic_nav = Builder.load_file("pages/nav_drawer.kv")
            self.add_widget(self.basic_nav)
            nav_dedoup_home.append("added")

    def cleanup(self):
        self.ids.layout.clear_widgets()
        #nav_dedoup_home.clear()

class LoginWindow(Screen):
    dialog = None
    api_key = ObjectProperty(None)
    api_id = ObjectProperty(None)
    org_key = ObjectProperty(None)

    def __init__(self, name, sm):
        """
        Init the sub-class and Screen super class.
        :param name:
        :param sm:
        """
        super().__init__() # Python3
        self.sm = sm
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path
        )
    def file_manager_open(self):
        self.file_manager.show('credentials/')  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''

        self.exit_manager()

        config = configparser.ConfigParser()
        config.read(os.path.expanduser(path))

        self.ids.api_key.ids.text_field.text = no_quotes(config['creds']['api_key'])
        self.api_id.text = no_quotes(config['creds']['api_id'])
        self.org_key.text = no_quotes(config['creds']['org_key'])

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()
    def initWindow(self):
        final_org_key.clear()
        final_api_key.clear()
        final_api_id.clear()

        self.ids.api_key.ids.text_field.text = ''
        self.api_id.text = ''
        self.org_key.text = ''

    def loginBtn(self):

        #print(self.ids.api_key.ids.text_field.text)
        print(len(self.ids.api_key.ids.text_field.text))

        #print(self.api_id.text)
        print(len(self.api_id.text))

        #print(self.org_key.text)
        print(len(self.org_key.text))
        if len(self.ids.api_key.ids.text_field.text) == 24 and len(self.api_id.text) == 10 and len(self.org_key.text) == 8:
            final_api_key.append(self.ids.api_key.ids.text_field.text)
            final_api_id.append(self.api_id.text)
            final_org_key.append(self.org_key.text)

            self.correct_show_alert_dialog()

        else:
            self.incorrect_show_alert_dialog()


    def correct_show_alert_dialog(self):
        self.dialog = MDDialog(
            text="Excellent!\n\nPlease ensure the API Key provided is type 'Custom', with the proper permissions, or else you will experience errors on the following page.",
            buttons=[
                MDFlatButton(
                    text="BACK",
                    theme_text_color="Custom",
                    on_press=lambda x: self.close_correct_popup2()
                ),
                MDFlatButton(
                    text="CONTINUE",
                    theme_text_color="Custom",
                    on_press=lambda x: self.close_correct_popup()
                ),
            ],
        )
        self.dialog.open()

    def incorrect_show_alert_dialog(self):
        self.dialog = MDDialog(
            text="It seems as though either your API Key, API ID, or Org Key are the wrong length. Perhaps a typo, or trailing blank space.\n\nPlease revise and try again.",
            buttons=[
                MDFlatButton(
                    text="EXIT",
                    theme_text_color="Custom",
                    on_press=lambda x: self.close_incorrect_popup()
                ),
            ],
        )
        self.dialog.open()

    def close_incorrect_popup(self):
        self.dialog.dismiss(force=True)
        self.ids.api_key.ids.text_field.text = ''
        self.api_id.text = ''
        self.org_key.text = ''

    def close_correct_popup(self):
        self.dialog.dismiss(force=True)
        self.sm.current = "home"

    def close_correct_popup2(self):
        self.dialog.dismiss(force=True)

class Feeds(Screen):
    dialog = None

    def __init__(self, name, sm):
        """
        Init the sub-class and Screen super class.
        :param name:
        :param sm:
        """
        super().__init__() # Python3
        self.sm = sm

    def initNav(self):
        if len(nav_dedoup) == 0:
            self.basic_nav = Builder.load_file("pages/nav_drawer.kv")
            self.add_widget(self.basic_nav)
            nav_dedoup.append("added")


    def initWindow(self):
        all_feeds = []
        all_feeds_ids = []
        enabled_feeds = []
        dedoup = []

        self.header = {
            "Content-Type": "application/json",
            "X-Auth-Token": final_api_key[0] + "/" + final_api_id[0],
            "org_key": final_org_key[0]
        }
        pub_feeds = "/threathunter/feedmgr/v2/orgs/{}/feeds?include_public=true".format(final_org_key[0])
        get_pub_feeds = url_base+pub_feeds

        r = requests.get(url=get_pub_feeds, headers=self.header)
        r1 = r.json()
        print(r1)

        self.ids.container.add_widget(MDLabel(
            text="This page contains all imported and OOTB Threat Intel Feeds",
            halign="center",
            theme_text_color="Custom",
            text_color= (1, 0, 0, 0.5)
        ))
        self.ids.avail_container.add_widget(MDLabel(
            text="This page contains all available Threat Intel Feeds for Import",
            halign="center",
            theme_text_color="Custom",
            text_color= (1, 0, 0, 0.5)
        ))

        for x in r1['results']:
            all_feeds_ids.append(x['id'])

            if x not in all_feeds:

                if x['owner'] == "Carbon Black":

                    if "ATT&CK" in x['name']:
                        if x['id'] not in dedoup:
                            logo = "logos/mitre.png"
                            self.ids.container.add_widget(GetInfoBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                            dedoup.append(x['id'])

                    if "Cybercom" in x['name']:
                        if x['id'] not in dedoup:
                            logo = "logos/uscyber.jpeg"
                            self.ids.container.add_widget(GetInfoBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                            dedoup.append(x['id'])

                    elif x['id'] not in dedoup:
                        logo = "logos/cb.png"
                        dedoup.append(x['id'])
                        self.ids.container.add_widget(GetInfoBtn(
                            text=x['name'],
                        secondary_text=x['id'],
                        icon=logo))

                if x['owner'] == "TOR":
                    if x['id'] not in dedoup:
                        logo = "logos/tor.png"
                        dedoup.append(x['id'])
                        self.ids.container.add_widget(GetInfoBtn(
                            text=x['name'],
                            secondary_text=x['id'],
                            icon=logo))

                if x['owner'] == "Facebook ThreatExchange":
                    if x['id'] not in dedoup:
                        logo = "logos/fb.png"
                        dedoup.append(x['id'])
                        self.ids.container.add_widget(GetInfoBtn(
                            text=x['name'],
                            secondary_text=x['id'],
                            icon=logo))

                if x['owner'] == "AlienVault":
                    if x['id'] not in dedoup:
                        logo = "logos/av.png"
                        dedoup.append(x['id'])
                        self.ids.container.add_widget(GetInfoBtn(
                            text=x['name'],
                            secondary_text=x['id'],
                            icon=logo))

                elif x['owner'] != None:
                    if x['id'] not in dedoup:
                        if x['category'] == 'Open Source':
                            if "abuse" in x['name']:
                                logo = "logos/abuse.png"
                                dedoup.append(x['id'])
                                self.ids.container.add_widget(InfoUpdateDeleteBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                            elif "cybercure" in x['name']:
                                logo = "logos/cybercure.jpg"
                                dedoup.append(x['id'])
                                self.ids.container.add_widget(InfoUpdateDeleteBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                            elif "Ukraine" in x['name']:
                                logo = "logos/ukraine.png"
                                dedoup.append(x['id'])
                                self.ids.container.add_widget(InfoUpdateDeleteBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                            else:
                                logo = "logos/misp.png"
                                dedoup.append(x['id'])
                                self.ids.container.add_widget(InfoUpdateDeleteBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                        else:
                            if "Rob Eberhardt" in x['category']:
                                if "PCI_DSS_FIM" in x['name']:
                                    dedoup.append(x['id'])
                                    self.ids.container.add_widget(InfoDeleteCreditBtn(
                                        text=x['name'],
                                        secondary_text=x['id'],
                                        icon="logos/PCI_DSS_Rob_Eberhardt.png",
                                    ))
                                else:
                                    dedoup.append(x['id'])
                                    self.ids.container.add_widget(InfoDeleteCreditBtn(
                                        text=x['name'],
                                        secondary_text=x['id'],
                                        icon="credit/Rob_Eberhardt.jpeg",
                                    ))
                            elif "Nicholas Comeau" in x['category']:
                                if "Chrome" in x['name']:
                                    dedoup.append(x['id'])
                                    self.ids.container.add_widget(InfoDeleteCreditBtn(
                                        text=x['name'],
                                        secondary_text=x['id'],
                                        icon="credit/nick_comeau_chrome_atlas.png",
                                    ))
                                if "Fuzzy" in x['name']:
                                    dedoup.append(x['id'])
                                    self.ids.container.add_widget(InfoDeleteCreditBtn(
                                        text=x['name'],
                                        secondary_text=x['id'],
                                        icon="credit/nick_comeau_fuzzy_search.png",
                                    ))
                                if "Linux" in x['name']:
                                    self.ids.container.add_widget(InfoDeleteCreditBtn(
                                        text=x['name'],
                                        secondary_text=x['id'],
                                        icon="credit/nick_comeau_linux.png",
                                    ))
                            elif "Patrick Mayer" in x['category']:
                                dedoup.append(x['id'])
                                self.ids.container.add_widget(InfoDeleteCreditBtn(
                                    text=x['name'],
                                    secondary_text=x['id'],
                                    icon="credit/patrick_mayer_wizard.png",
                                ))
                            else:
                                dedoup.append(x['id'])
                                self.ids.container.add_widget(InfoDeleteBtn(
                                    text=x['name'],
                                    secondary_text=x['id'],
                                    icon="tools"))
                all_feeds.append(x)
                enabled_feeds.append(x['name'])
        self.ids.container.add_widget(OneLineListItem(text=""))
        self.ids.container.add_widget(OneLineListItem(text=""))

        ### Check Unused Feeds ###
        path = "feed_parser/feed_json"
        onlyfiles = [f for f in listdir('feed_parser/feed_json') if isfile(join('feed_parser/feed_json', f))]

        for f in sorted(onlyfiles):
            if feed_format(f) not in enabled_feeds:
                print(f)

                with open(path+"/"+f) as a:
                    b = json.load(a)
                    x = b['feedinfo']
                    if x['category'] == 'Open Source':
                        if "abuse" in x['name']:
                            logo = "logos/abuse.png"
                            self.ids.avail_container.add_widget(ImportBtn(
                                text=x['name'],
                                secondary_text = path+"/"+f,
                                icon=logo))
                        elif "cybercure" in x['name']:
                            logo = "logos/cybercure.jpg"
                            self.ids.avail_container.add_widget(ImportBtn(
                                text=x['name'],
                                secondary_text = path+"/"+f,
                                icon=logo))
                        elif "Ukraine" in x['name']:
                            logo = "logos/ukraine.png"
                            self.ids.avail_container.add_widget(ImportBtn(
                                text=x['name'],
                                secondary_text = path+"/"+f,
                                icon=logo))
                        else:
                            logo = "logos/misp.png"
                            self.ids.avail_container.add_widget(ImportBtn(
                                text=x['name'],
                                secondary_text = path+"/"+f,
                                icon=logo))
                    else:
                        if "Rob Eberhardt" in x['category']:
                            if "PCI_DSS_FIM" in x['name']:
                                self.ids.avail_container.add_widget(ImportCreditBtn(
                                    text=x['name'],
                                    secondary_text = path+"/"+f,
                                    icon="logos/PCI_DSS_Rob_Eberhardt.png"))
                            else:
                                self.ids.avail_container.add_widget(ImportCreditBtn(
                                    text=x['name'],
                                    secondary_text = path+"/"+f,
                                    icon="credit/Rob_Eberhardt.jpeg"))

                        elif "Nicholas Comeau" in x['category']:
                            if "Chrome" in x['name']:
                                self.ids.avail_container.add_widget(ImportCreditBtn(
                                    text=x['name'],
                                    secondary_text=path+"/"+f,
                                    icon="credit/nick_comeau_chrome_atlas.png",
                                ))
                            if "Fuzzy" in x['name']:
                                self.ids.avail_container.add_widget(ImportCreditBtn(
                                    text=x['name'],
                                    secondary_text=path + "/" + f,
                                    icon="credit/nick_comeau_fuzzy_search.png",
                                ))
                            if "Linux" in x['name']:
                                self.ids.avail_container.add_widget(ImportCreditBtn(
                                    text=x['name'],
                                    secondary_text=path + "/" + f,
                                    icon="credit/nick_comeau_linux.png",
                                ))
                        elif "Patrick Mayer" in x['category']:
                            self.ids.avail_container.add_widget(ImportCreditBtn(
                                text=x['name'],
                                secondary_text=path + "/" + f,
                                icon="credit/patrick_mayer_wizard.png",
                            ))
                        else:
                            self.ids.avail_container.add_widget(ImportBtn(
                                text=x['name'],
                                secondary_text = path+"/"+f,
                                icon="tools"))

                    a.close()
        self.ids.avail_container.add_widget(OneLineListItem(text=""))
        self.ids.avail_container.add_widget(OneLineListItem(text=""))

    ### IMPORT NOTICE ###
    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        '''
        Called when switching tabs.
        :param tab_text: text or name icon of tab;
        '''
        if tab_text == "Available Threat Intel":
            self.dialog = MDDialog(
                title="Important Information",
                text="When importing a feed, it can take up to ~15-45 seconds, depending on the size of the feed contents.\n\nDuring that time, the app may look like it is frozen, but it is not, it is simply working on your request in the background, so please be patient!",
            )
            self.dialog.open()

    #### IMPORT FEED ####
    def import_feed(self,path, name):
        create_route = "/threathunter/feedmgr/v2/orgs/{}/feeds".format(final_org_key[0])
        create_url = url_base+create_route

        with open(path) as a:
            body = json.load(a)
            r = requests.post(url=create_url, headers=self.header, json=body)
            print(r)
            a.close()
            if r.status_code == 200:
                self.ids.container.clear_widgets()
                self.ids.avail_container.clear_widgets()
                self.initWindow()
                Snackbar(text="{} Feed successfully Imported!".format(name)).open()
            else:
                Snackbar(text="Unable to import feed {}.".format(name)).open()


    #### GET FEED INFO ####
    def get_info_file(self,path):
        with open(path) as a:
            b = json.load(a)
            self.show_info(b)
            a.close()

    def get_info(self, id):


        specific_feed= "/threathunter/feedmgr/v2/orgs/{}/feeds/{}".format(final_org_key[0],id)
        specific_feed_url = url_base+specific_feed

        r = requests.get(url=specific_feed_url, headers=self.header)
        data = r.json()
        self.show_info(data)

    def show_info(self, data):
        num_iocs = []
        for x in range(len(data['reports'])):
            for y in data['reports'][x]['iocs_v2'][0]['values']:
                num_iocs.append(y)

        feed_info = MDDialog(title=data['feedinfo']['name'],
                          text="Summary: {}\n\nNumber of Reports: {}\n\nNumber of IOCs: {}".format(data['feedinfo']['summary'],len(data['reports']),len(num_iocs)))
        feed_info.open()

    #### DELETE FEED ####
    def delete_confirm(self,id,name):

        self.dialog = MDDialog(
            title="Are you sure you want to delete this feed?",
            text="NOTE: If this is a feed you imported via CB Open Source Threat Intel Mgr you will be available for import afterwards.",
            buttons=[
                MDFlatButton(
                    text="CONFIRM",
                    theme_text_color="Custom",
                    text_color=(1,0,0.3,1),
                    on_press=lambda x: self.delete_feed(id, name)
                ),
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    on_press=lambda x: self.delete_feed_cancel()
                ),
            ],
        )
        self.dialog.open()

    def delete_feed_cancel(self):
        self.dialog.dismiss(force=True)

    def delete_feed(self,id,name):

        delete_url = url_base + "/threathunter/feedmgr/v2/orgs/{}/feeds/{}".format(final_org_key[0],id)
        r = requests.delete(url=delete_url, headers=self.header)
        print(r.status_code)
        if r.status_code == 204:
            self.dialog.dismiss(force=True)
            self.ids.container.clear_widgets()
            self.ids.avail_container.clear_widgets()
            self.initWindow()
            Snackbar(text="{} Feed successfully deleted!".format(name)).open()
        else:
            Snackbar(text="Hmmm, there seems to be an issue deleting Feed {}".format(name)).open()


    #### UPDATE FEED ####
    def update_feed(self,id, name):
        update_route = "/threathunter/feedmgr/v2/orgs/{}/feeds/{}/reports".format(final_org_key[0],id)
        update_url = url_base+update_route

        # Running helper script to update the feed json
        os.system("python3 feed_parser/{}.py".format(name))

        # Defining the import for the updated json
        path = "feed_parser/feed_json/{}.json".format(name)

        with open(path) as a:
            body = json.load(a)
            r = requests.post(url=update_url, headers=self.header, json=body)
            print(r.status_code)
            if r.status_code == 200:
                Snackbar(text="{} Feed successfully Updated!".format(name)).open()
            else:
                Snackbar(text="{} Feed was unable to update.".format(name)).open()
            a.close()

class Watchlists(Screen):
    dialog = None
    def __init__(self, name, sm):
        """
        Init the sub-class and Screen super class.
        :param name:
        :param sm:
        """
        super().__init__() # Python3
        self.sm = sm

    def initNav(self):
        if len(nav_dedoup2) == 0:
            self.basic_nav = Builder.load_file("pages/nav_drawer.kv")
            self.add_widget(self.basic_nav)
            nav_dedoup2.append("added")

    def initWindow(self):
        all_wl = []
        all_wl_name = []
        all_wl_ids = []
        enabled_feeds = []
        dedoup = []

        self.header = {
            "Content-Type": "application/json",
            "X-Auth-Token": final_api_key[0] + "/" + final_api_id[0],
            "org_key": final_org_key[0]
        }

        wl_route = "/threathunter/watchlistmgr/v3/orgs/{}/watchlists".format(final_org_key[0])
        get_all_wl = url_base+wl_route

        pub_feeds = "/threathunter/feedmgr/v2/orgs/{}/feeds?include_public=true".format(final_org_key[0])
        get_pub_feeds = url_base + pub_feeds

        r = requests.get(url=get_all_wl, headers=self.header)
        print(r.status_code)
        r1 = r.json()
        for x in r1['results']:
            if x['name'] not in str(all_wl_name):
                all_wl.append(x)
                all_wl_ids.append(x['id'])
                all_wl_name.append(x['name'])

        r = requests.get(url=get_pub_feeds, headers=self.header)
        print(r.status_code)
        r1 = r.json()

        for x in r1['results']:
            if x['name'] not in str(all_wl_name):

                if x['owner'] == "Carbon Black":

                    if "ATT&CK" in x['name']:
                        if x['id'] not in dedoup:
                            logo = "logos/mitre.png"
                            self.ids.not_enabled.add_widget(FeedBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                            dedoup.append(x['id'])

                    if "Cybercom" in x['name']:
                        if x['id'] not in dedoup:
                            logo = "logos/uscyber.jpeg"
                            self.ids.not_enabled.add_widget(FeedBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                            dedoup.append(x['id'])

                    elif x['id'] not in dedoup:
                        logo = "logos/cb.png"
                        dedoup.append(x['id'])
                        self.ids.not_enabled.add_widget(FeedBtn(
                            text=x['name'],
                        secondary_text=x['id'],
                        icon=logo))

                if x['owner'] == "TOR":
                    if x['id'] not in dedoup:
                        logo = "logos/tor.png"
                        dedoup.append(x['id'])
                        self.ids.not_enabled.add_widget(FeedBtn(
                            text=x['name'],
                            secondary_text=x['id'],
                            icon=logo))

                if x['owner'] == "Facebook ThreatExchange":
                    if x['id'] not in dedoup:
                        logo = "logos/fb.png"
                        dedoup.append(x['id'])
                        self.ids.not_enabled.add_widget(FeedBtn(
                            text=x['name'],
                            secondary_text=x['id'],
                            icon=logo))

                if x['owner'] == "AlienVault":
                    if x['id'] not in dedoup:
                        logo = "logos/av.png"
                        dedoup.append(x['id'])
                        self.ids.not_enabled.add_widget(FeedBtn(
                            text=x['name'],
                            secondary_text=x['id'],
                            icon=logo))

                elif x['owner'] != None:
                    if x['id'] not in dedoup:
                        if x['category'] == 'Open Source':
                            if "abuse" in x['name']:
                                logo = "logos/abuse.png"
                                dedoup.append(x['id'])
                                self.ids.not_enabled.add_widget(FeedBtn(
                                    text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                            elif "cybercure" in x['name']:
                                logo = "logos/cybercure.jpg"
                                dedoup.append(x['id'])
                                self.ids.not_enabled.add_widget(FeedBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                            elif "Ukraine" in x['name']:
                                logo = "logos/ukraine.png"
                                dedoup.append(x['id'])
                                self.ids.not_enabled.add_widget(FeedBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                            else:
                                logo = "logos/misp.png"
                                dedoup.append(x['id'])
                                self.ids.not_enabled.add_widget(FeedBtn(
                                    text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                        else:
                            if "Rob Eberhardt" in x['category']:
                                if "PCI_DSS_FIM" in x['name']:
                                    dedoup.append(x['id'])
                                    self.ids.not_enabled.add_widget(FeedBtn(
                                        text=x['name'],
                                        secondary_text=x['id'],
                                        icon="logos/PCI_DSS_Rob_Eberhardt.png",
                                    ))
                                else:
                                    dedoup.append(x['id'])
                                    self.ids.not_enabled.add_widget(FeedBtn(
                                        text=x['name'],
                                        secondary_text=x['id'],
                                        icon="credit/Rob_Eberhardt.jpeg",
                                    ))
                            if "Nicholas Comeau" in x['category']:
                                if "Chrome" in x['name']:
                                    dedoup.append(x['id'])
                                    self.ids.not_enabled.add_widget(FeedBtn(
                                        text=x['name'],
                                        secondary_text=x['id'],
                                        icon="credit/nick_comeau_chrome_atlas.png",
                                    ))
                                elif "Fuzzy" in x['name']:
                                    dedoup.append(x['id'])
                                    self.ids.not_enabled.add_widget(FeedBtn(
                                        text=x['name'],
                                        secondary_text=x['id'],
                                        icon="credit/nick_comeau_fuzzy_search.png",
                                    ))
                                elif "Linux" in x['name']:
                                    dedoup.append(x['id'])
                                    self.ids.not_enabled.add_widget(FeedBtn(
                                        text=x['name'],
                                        secondary_text=x['id'],
                                        icon="credit/nick_comeau_linux.png",
                                    ))
                            if "Patrick Mayer" in x['category']:
                                dedoup.append(x['id'])
                                self.ids.not_enabled.add_widget(FeedBtn(
                                    text=x['name'],
                                    secondary_text=x['id'],
                                    icon="credit/patrick_mayer_wizard.png",
                                ))
                            else:
                                if x['id'] not in dedoup:
                                    dedoup.append(x['id'])
                                    self.ids.not_enabled.add_widget(FeedBtn(
                                        text=x['name'],
                                        secondary_text=x['id'],
                                        icon="tools"))

    def initWl(self):
        disabled_wls = []
        enabled_wls = []
        alerted_wls = []
        dedoup = []
        wl_route = "/threathunter/watchlistmgr/v3/orgs/{}/watchlists".format(final_org_key[0])
        get_all_wl = url_base+wl_route

        r = requests.get(url=get_all_wl, headers=self.header)
        print(r.status_code)
        r1 = r.json()

        for x in r1['results']:
            if x['tags_enabled'] == False:
                disabled_wls.append(x)
                if "TOR" in x['name']:
                    if x['id'] not in dedoup:
                        logo = "logos/tor.png"
                        dedoup.append(x['id'])
                        self.ids.not_enabled.add_widget(WatchlistBtn(
                            text=x['name'],
                            secondary_text=x['id'],
                            icon=logo))
                if "AlienVault" in x['name']:
                    if x['id'] not in dedoup:
                        logo = "logos/av.png"
                        dedoup.append(x['id'])
                        self.ids.not_enabled.add_widget(WatchlistBtn(
                            text=x['name'],
                            secondary_text=x['id'],
                            icon=logo))
                if "Facebook ThreatExchange" in x['name']:
                    if x['id'] not in dedoup:
                        logo = "logos/fb.png"
                        dedoup.append(x['id'])
                        self.ids.not_enabled.add_widget(WatchlistBtn(
                            text=x['name'],
                            secondary_text=x['id'],
                            icon=logo))
                if "ATT&CK" in x['name']:
                    if x['id'] not in dedoup:
                        logo = "logos/mitre.png"
                        self.ids.not_enabled.add_widget(WatchlistBtn(
                            text=x['name'],
                            secondary_text=x['id'],
                            icon=logo))
                        dedoup.append(x['id'])

                if "Cybercom" in x['name']:
                    if x['id'] not in dedoup:
                        logo = "logos/uscyber.jpeg"
                        self.ids.not_enabled.add_widget(WatchlistBtn(
                            text=x['name'],
                            secondary_text=x['id'],
                            icon=logo))
                        dedoup.append(x['id'])

                if "Carbon Black" in x['name']:
                    if x['id'] not in dedoup:
                        logo = "logos/cb.png"
                        dedoup.append(x['id'])
                        self.ids.not_enabled.add_widget(WatchlistBtn(
                            text=x['name'],
                            secondary_text=x['id'],
                            icon=logo))
                if "AMSI Threat Intelligence" in x['name']:
                    if x['id'] not in dedoup:
                        logo = "logos/cb.png"
                        dedoup.append(x['id'])
                        self.ids.not_enabled.add_widget(WatchlistBtn(
                            text=x['name'],
                            secondary_text=x['id'],
                            icon=logo))

                if "abuse" in x['name']:
                    if x['id'] not in dedoup:
                        logo = "logos/abuse.png"
                        dedoup.append(x['id'])
                        self.ids.not_enabled.add_widget(WatchlistBtn(
                            text=x['name'],
                            secondary_text=x['id'],
                            icon=logo))
                if "ipsum" in x['name']:
                    if x['id'] not in dedoup:
                        logo = "logos/misp.png"
                        dedoup.append(x['id'])
                        self.ids.not_enabled.add_widget(WatchlistBtn(
                            text=x['name'],
                            secondary_text=x['id'],
                            icon=logo))
                if "Ukraine" in x['name']:
                    if x['id'] not in dedoup:
                        logo = "logos/ukraine.png"
                        dedoup.append(x['id'])
                        self.ids.not_enabled.add_widget(WatchlistBtn(
                            text=x['name'],
                            secondary_text=x['id'],
                            icon=logo))
                ### Custom CB Intel ###
                if x['name'] == "PCI_DSS_FIM":
                    if x['id'] not in dedoup:
                        logo = "logos/PCI_DSS_Rob_Eberhardt.png"
                        dedoup.append(x['id'])
                        self.ids.not_enabled.add_widget(WatchlistBtn(
                            text=x['name'],
                            secondary_text=x['id'],
                            icon=logo))
                if x['name'] == "Threat_Hunting_Feed_v2":
                    if x['id'] not in dedoup:
                        logo = "credit/Rob_Eberhardt.jpeg"
                        dedoup.append(x['id'])
                        self.ids.not_enabled.add_widget(WatchlistBtn(
                            text=x['name'],
                            secondary_text=x['id'],
                            icon=logo))
                if x['name'] == "SE_Query_Feed_v2":
                    if x['id'] not in dedoup:
                        logo = "credit/Rob_Eberhardt.jpeg"
                        dedoup.append(x['id'])
                        self.ids.not_enabled.add_widget(WatchlistBtn(
                            text=x['name'],
                            secondary_text=x['id'],
                            icon=logo))
                if x['name'] == "Suspicious_Chrome_Extensions":
                    if x['id'] not in dedoup:
                        logo = "credit/nick_comeau_chrome_atlas.png"
                        dedoup.append(x['id'])
                        self.ids.not_enabled.add_widget(WatchlistBtn(
                            text=x['name'],
                            secondary_text=x['id'],
                            icon=logo))
                if x['name'] == "Fuzzy_Search_Queries":
                    if x['id'] not in dedoup:
                        logo = "credit/nick_comeau_fuzzy_search.png"
                        dedoup.append(x['id'])
                        self.ids.not_enabled.add_widget(WatchlistBtn(
                            text=x['name'],
                            secondary_text=x['id'],
                            icon=logo))
                if x['name'] == "Linux_Queries":
                    if x['id'] not in dedoup:
                        logo = "credit/nick_comeau_linux.png"
                        dedoup.append(x['id'])
                        self.ids.not_enabled.add_widget(WatchlistBtn(
                            text=x['name'],
                            secondary_text=x['id'],
                            icon=logo))
                if x['name'] == "Mayers_Magic_Queries":
                    if x['id'] not in dedoup:
                        logo = "credit/patrick_mayer_wizard.png"
                        dedoup.append(x['id'])
                        self.ids.not_enabled.add_widget(WatchlistBtn(
                            text=x['name'],
                            secondary_text=x['id'],
                            icon=logo))
                else:
                    if x['id'] not in dedoup:
                        dedoup.append(x['id'])
                        self.ids.not_enabled.add_widget(WatchlistBtn(
                            text=x['name'],
                            secondary_text=x['id'],
                            icon="tools"))

            if x['tags_enabled'] == True:
                if x['alerts_enabled'] == False:
                    enabled_wls.append(x)
                    if "TOR" in x['name']:
                        if x['id'] not in dedoup:
                            logo = "logos/tor.png"
                            dedoup.append(x['id'])
                            self.ids.enabled.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                    if "AlienVault" in x['name']:
                        if x['id'] not in dedoup:
                            logo = "logos/av.png"
                            dedoup.append(x['id'])
                            self.ids.enabled.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                    if "Facebook ThreatExchange" in x['name']:
                        if x['id'] not in dedoup:
                            logo = "logos/fb.png"
                            dedoup.append(x['id'])
                            self.ids.enabled.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                    if "ATT&CK" in x['name']:
                        if x['id'] not in dedoup:
                            logo = "logos/mitre.png"
                            self.ids.enabled.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                            dedoup.append(x['id'])

                    if "Cybercom" in x['name']:
                        if x['id'] not in dedoup:
                            logo = "logos/uscyber.jpeg"
                            self.ids.enabled.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                            dedoup.append(x['id'])

                    if "Carbon Black" in x['name']:
                        if x['id'] not in dedoup:
                            logo = "logos/cb.png"
                            dedoup.append(x['id'])
                            self.ids.enabled.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                    if "AMSI Threat Intelligence" in x['name']:
                        if x['id'] not in dedoup:
                            logo = "logos/cb.png"
                            dedoup.append(x['id'])
                            self.ids.enabled.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                    if "abuse" in x['name']:
                        if x['id'] not in dedoup:
                            logo = "logos/abuse.png"
                            dedoup.append(x['id'])
                            self.ids.enabled.add_widget(WatchlistBtn(
                                text=x['name'],
                                    secondary_text=x['id'],
                                    icon=logo))
                    if "ipsum" in x['name']:
                        if x['id'] not in dedoup:
                            logo = "logos/misp.png"
                            dedoup.append(x['id'])
                            self.ids.enabled.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                    if "Ukraine" in x['name']:
                        if x['id'] not in dedoup:
                            logo = "logos/ukraine.png"
                            dedoup.append(x['id'])
                            self.ids.enabled.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))

                    ### Custom CB Intel ###
                    if x['name'] == "PCI_DSS_FIM":
                        if x['id'] not in dedoup:
                            logo = "logos/PCI_DSS_Rob_Eberhardt.png"
                            dedoup.append(x['id'])
                            self.ids.enabled.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                    if x['name'] == "Threat_Hunting_Feed_v2":
                        if x['id'] not in dedoup:
                            logo = "credit/Rob_Eberhardt.jpeg"
                            dedoup.append(x['id'])
                            self.ids.enabled.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                    if x['name'] == "SE_Query_Feed_v2":
                        if x['id'] not in dedoup:
                            logo = "credit/Rob_Eberhardt.jpeg"
                            dedoup.append(x['id'])
                            self.ids.enabled.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                    if x['name'] == "Suspicious_Chrome_Extensions":
                        if x['id'] not in dedoup:
                            logo = "credit/nick_comeau_chrome_atlas.png"
                            dedoup.append(x['id'])
                            self.ids.enabled.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                    if x['name'] == "Fuzzy_Search_Queries":
                        if x['id'] not in dedoup:
                            logo = "credit/nick_comeau_fuzzy_search.png"
                            dedoup.append(x['id'])
                            self.ids.enabled.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                    if x['name'] == "Linux_Queries":
                        if x['id'] not in dedoup:
                            logo = "credit/nick_comeau_linux.png"
                            dedoup.append(x['id'])
                            self.ids.enabled.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                    if x['name'] == "Mayers_Magic_Queries":
                        if x['id'] not in dedoup:
                            logo = "credit/patrick_mayer_wizard.png"
                            dedoup.append(x['id'])
                            self.ids.enabled.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                    else:
                        if x['id'] not in dedoup:
                            dedoup.append(x['id'])
                            self.ids.enabled.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon="tools"))

                if x['alerts_enabled'] == True:
                    alerted_wls.append(x)
                    if "TOR" in x['name']:
                        if x['id'] not in dedoup:
                            logo = "logos/tor.png"
                            dedoup.append(x['id'])
                            self.ids.alerted.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                    if "AlienVault" in x['name']:
                        if x['id'] not in dedoup:
                            logo = "logos/av.png"
                            dedoup.append(x['id'])
                            self.ids.alerted.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                    if "Facebook ThreatExchange" in x['name']:
                        if x['id'] not in dedoup:
                            logo = "logos/fb.png"
                            dedoup.append(x['id'])
                            self.ids.alerted.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                    if "ATT&CK" in x['name']:
                        if x['id'] not in dedoup:
                            logo = "logos/mitre.png"
                            self.ids.alerted.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                            dedoup.append(x['id'])

                    if "Cybercom" in x['name']:
                        if x['id'] not in dedoup:
                            logo = "logos/uscyber.jpeg"
                            self.ids.alerted.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                            dedoup.append(x['id'])

                    if "Carbon Black" in x['name']:
                        if x['id'] not in dedoup:
                            logo = "logos/cb.png"
                            dedoup.append(x['id'])
                            self.ids.alerted.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                    if "AMSI Threat Intelligence" in x['name']:
                        if x['id'] not in dedoup:
                            logo = "logos/cb.png"
                            dedoup.append(x['id'])
                            self.ids.alerted.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                    if "abuse" in x['name']:
                        if x['id'] not in dedoup:
                            logo = "logos/abuse.png"
                            dedoup.append(x['id'])
                            self.ids.alerted.add_widget(WatchlistBtn(
                                text=x['name'],
                                    secondary_text=x['id'],
                                    icon=logo))
                    if "ipsum" in x['name']:
                        if x['id'] not in dedoup:
                            logo = "logos/misp.png"
                            dedoup.append(x['id'])
                            self.ids.alerted.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                    if "Ukraine" in x['name']:
                        if x['id'] not in dedoup:
                            logo = "logos/ukraine.png"
                            dedoup.append(x['id'])
                            self.ids.alerted.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))

                    ### Custom CB Intel ###
                    if x['name'] == "PCI_DSS_FIM":
                        if x['id'] not in dedoup:
                            logo = "logos/PCI_DSS_Rob_Eberhardt.png"
                            dedoup.append(x['id'])
                            self.ids.alerted.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                    if x['name'] == "Threat_Hunting_Feed_v2":
                        if x['id'] not in dedoup:
                            logo = "credit/Rob_Eberhardt.jpeg"
                            dedoup.append(x['id'])
                            self.ids.alerted.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                    if x['name'] == "SE_Query_Feed_v2":
                        if x['id'] not in dedoup:
                            logo = "credit/Rob_Eberhardt.jpeg"
                            dedoup.append(x['id'])
                            self.ids.alerted.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                    if x['name'] == "Suspicious_Chrome_Extensions":
                        if x['id'] not in dedoup:
                            logo = "credit/nick_comeau_chrome_atlas.png"
                            dedoup.append(x['id'])
                            self.ids.alerted.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                    if x['name'] == "Fuzzy_Search_Queries":
                        if x['id'] not in dedoup:
                            logo = "credit/nick_comeau_fuzzy_search.png"
                            dedoup.append(x['id'])
                            self.ids.alerted.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                    if x['name'] == "Linux_Queries":
                        if x['id'] not in dedoup:
                            logo = "credit/nick_comeau_linux.png"
                            dedoup.append(x['id'])
                            self.ids.alerted.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))

                    if x['name'] == "Mayers_Magic_Queries":
                        if x['id'] not in dedoup:
                            logo = "credit/patrick_mayer_wizard.png"
                            dedoup.append(x['id'])
                            self.ids.alerted.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon=logo))
                    else:
                        if x['id'] not in dedoup:
                            dedoup.append(x['id'])
                            self.ids.alerted.add_widget(WatchlistBtn(
                                text=x['name'],
                                secondary_text=x['id'],
                                icon="tools"))

        # Adding Bottom Blank Widgets for ease of viewing
        self.ids.not_enabled.add_widget(OneLineListItem(text=""))
        self.ids.not_enabled.add_widget(OneLineListItem(text=""))
        self.ids.enabled.add_widget(OneLineListItem(text=""))
        self.ids.enabled.add_widget(OneLineListItem(text=""))
        self.ids.alerted.add_widget(OneLineListItem(text=""))
        self.ids.alerted.add_widget(OneLineListItem(text=""))

    def decider(self,id,name):
        not_supported = ["ATT&CK Framework", "Carbon Black Early Access Indicators", "Carbon Black Endpoint Suspicious Indicators", "Carbon Black Endpoint Visibility",]

        info_route = "/threathunter/watchlistmgr/v3/orgs/{}/watchlists/{}".format(final_org_key[0],id)
        info_url = url_base+info_route

        r = requests.get(url=info_url, headers=self.header)
        data = r.json()

        if data['name'] in not_supported:
            if data['tags_enabled'] == False:
                self.enable_not_supported_wl(id,name)
            if data['tags_enabled'] == True:
                self.disable_not_supported_wl(id,name)

        else:
            if data['tags_enabled'] == False:
                self.manage_disabled_wl(id,name)
            if data['tags_enabled'] == True:
                if data['alerts_enabled'] == False:
                    self.manage_enabled_wl(id,name)
                if data['alerts_enabled'] == True:
                    self.manage_alerted_wl(id,name)

    def get_info(self, id):
        print("------------")
        print(id)

        specific_feed= "/threathunter/feedmgr/v2/orgs/{}/feeds/{}".format(final_org_key[0],id)
        specific_feed_url = url_base+specific_feed

        r = requests.get(url=specific_feed_url, headers=self.header)
        data = r.json()
        self.show_info(data)

    def show_info(self, data):
        num_iocs = []
        for x in range(len(data['reports'])):
            for y in data['reports'][x]['iocs_v2'][0]['values']:
                num_iocs.append(y)

        feed_info = MDDialog(title=data['feedinfo']['name'],
                          text="Summary: {}\n\nNumber of Reports: {}\n\nNumber of IOCs: {}".format(data['feedinfo']['summary'],len(data['reports']),len(num_iocs)))
        feed_info.open()

    def get_wl_info(self,id):
        info_route = "/threathunter/watchlistmgr/v3/orgs/{}/watchlists/{}".format(final_org_key[0],id)
        info_url = url_base+info_route

        r = requests.get(url=info_url, headers=self.header)
        data = r.json()
        self.show_wl_info(data)

    def show_wl_info(self, data):

        feed_info = MDDialog(title=data['name'],
                          text="Summary: {}\n\nEnabled: {}\nAlerting: {}".format(data['description'],data['tags_enabled'], data['alerts_enabled']))
        feed_info.open()

    def manage_disabled_feed(self,id,name):

        self.dialog = MDDialog(
            title="What action would you like to take for {}?".format(name),
            text="ENABLE: Enabling a WL will allow for the associated threat intel to be overlaid on all data, and hits can be viewed on the [Enforce > Watchlists] Page.\n\nALERT: Alerting on a WL will allow for the associated threat intel to generate alerts, which will propagate on the 'Alerts' page.\n\n\nAlerting is only recommended for high-confidence indicators. If you are uncertain, the recommendation is to simply enable for now.",
            buttons=[
                MDFillRoundFlatIconButton(
                    text="Enable & Alert",
                    theme_text_color="Custom",
                    icon= "alert-circle-check-outline",
                    on_press=lambda x: self.enable_alert_feed(id,name)
                ),
                MDRoundFlatIconButton(
                    text="Enable",
                    theme_text_color="Custom",
                    icon="eye-check-outline",
                    on_press=lambda x: self.enable_feed(id,name)
                ),
                MDRoundFlatIconButton(
                    text="Cancel",
                    theme_text_color="Custom",
                    icon="cancel",
                    text_color=(1, 0, 0.3, 1),
                    on_press=lambda x: self.manage_wl_cancel()
                ),
            ],
        )
        self.dialog.open()

    def enable_feed(self,id,name):
        specific_feed= "/threathunter/feedmgr/v2/orgs/{}/feeds/{}".format(final_org_key[0],id)
        specific_feed_url = url_base+specific_feed

        r = requests.get(url=specific_feed_url, headers=self.header)
        data = r.json()
        description = data['feedinfo']['summary']


        enable_route = "/threathunter/watchlistmgr/v3/orgs/{}/watchlists".format(final_org_key[0])
        enable_url = url_base+enable_route

        body = {
            "name": name,
            "description": description,
            "tags_enabled": True,
            "alerts_enabled": False,
            "classifier": {
                "key": "feed_id",
                "value": id
            }
        }

        r1 = requests.post(url=enable_url,headers=self.header,json=body)
        print(r1)

        if r1.status_code == 200:
            self.dialog.dismiss(force=True)
            self.ids.not_enabled.clear_widgets()
            self.ids.enabled.clear_widgets()
            self.ids.alerted.clear_widgets()
            self.initWindow()
            self.initWl()
            Snackbar(text="{} Feed successfully enabled as a Watchlist!".format(name)).open()
        else:
            Snackbar(text="{} Feed failed to be enabled.".format(name)).open()

    def enable_alert_feed(self,id,name):
        specific_feed= "/threathunter/feedmgr/v2/orgs/{}/feeds/{}".format(final_org_key[0],id)
        specific_feed_url = url_base+specific_feed

        r = requests.get(url=specific_feed_url, headers=self.header)
        data = r.json()
        description = data['feedinfo']['summary']


        enable_route = "/threathunter/watchlistmgr/v3/orgs/{}/watchlists".format(final_org_key[0])
        enable_url = url_base+enable_route

        body = {
            "name": name,
            "description": description,
            "tags_enabled": True,
            "alerts_enabled": True,
            "classifier": {
                "key": "feed_id",
                "value": id
            }
        }
        r1 = requests.post(url=enable_url,headers=self.header,json=body)
        print(r1)

        if r1.status_code == 200:
            self.dialog.dismiss(force=True)
            self.ids.not_enabled.clear_widgets()
            self.ids.enabled.clear_widgets()
            self.ids.alerted.clear_widgets()
            self.initWindow()
            self.initWl()
            Snackbar(text="{} Feed successfully enabled as a Watchlist, and alerts turned on!".format(name)).open()
        else:
            Snackbar(text="{} Feed failed to be enabled.".format(name)).open()

    def manage_disabled_wl(self,id,name):

        self.dialog = MDDialog(
            title="What action would you like to take for {}?".format(name),
            text="ENABLE: Enabling a WL will allow for the associated threat intel to be overlaid on all data, and hits can be viewed on the [Enforce > Watchlists] Page.\n\nALERT: Alerting on a WL will allow for the associated threat intel to generate alerts, which will propagate on the 'Alerts' page.\n\n\nAlerting is only recommended for high-confidence indicators. If you are uncertain, the recommendation is to simply enable for now.",
            buttons=[
                MDFillRoundFlatIconButton(
                    text="Enable & Alert",
                    theme_text_color="Custom",
                    icon= "alert-circle-check-outline",
                    on_press=lambda x: self.enable_both(id,name)
                ),
                MDRoundFlatIconButton(
                    text="Enable",
                    theme_text_color="Custom",
                    icon="eye-check-outline",
                    on_press=lambda x: self.enable_wl(id,name)
                ),
                MDRoundFlatIconButton(
                    text="Cancel",
                    theme_text_color="Custom",
                    icon="cancel",
                    text_color=(1, 0, 0.3, 1),
                    on_press=lambda x: self.manage_wl_cancel()
                ),
            ],
        )
        self.dialog.open()

    def manage_enabled_wl(self,id,name):

        self.dialog = MDDialog(
            title="What action would you like to take for {}?".format(name),
            text="ENABLE: Enabling a WL will allow for the associated threat intel to be overlaid on all data, and hits can be viewed on the [Enforce > Watchlists] Page.\n\nALERT: Alerting on a WL will allow for the associated threat intel to generate alerts, which will propagate on the 'Alerts' page.\n\n\nAlerting is only recommended for high-confidence indicators. If you are uncertain, the recommendation is to simply enable for now.",
            buttons=[
                MDFillRoundFlatIconButton(
                    text="Alert",
                    theme_text_color="Custom",
                    icon="alert-circle-check-outline",
                    on_press=lambda x: self.enable_alert_wl(id,name)
                ),
                MDRoundFlatIconButton(
                    text="Disable WL",
                    theme_text_color="Custom",
                    icon="eye-off-outline",
                    on_press=lambda x: self.disable_wl(id,name)
                ),
                MDRoundFlatIconButton(
                    text="Cancel",
                    theme_text_color="Custom",
                    icon="cancel",
                    text_color=(1, 0, 0.3, 1),
                    on_press=lambda x: self.manage_wl_cancel()
                ),
            ],
        )
        self.dialog.open()

    def manage_alerted_wl(self,id,name):

        self.dialog = MDDialog(
            title="What action would you like to take for {}?".format(name),
            text="ENABLE: Enabling a WL will allow for the associated threat intel to be overlaid on all data, and hits can be viewed on the [Enforce > Watchlists] Page.\n\nALERT: Alerting on a WL will allow for the associated threat intel to generate alerts, which will propagate on the 'Alerts' page.\n\n\nAlerting is only recommended for high-confidence indicators. If you are uncertain, the recommendation is to simply enable for now.",
            buttons=[
                MDFillRoundFlatIconButton(
                    text="Disable Alerts",
                    theme_text_color="Custom",
                    icon="alert-remove-outline",
                    on_press=lambda x: self.disable_alert_wl(id,name)
                ),
                MDRoundFlatIconButton(
                    text="Disable WL",
                    theme_text_color="Custom",
                    icon="eye-off-outline",
                    on_press=lambda x: self.disable_both(id,name)
                ),
                MDRoundFlatIconButton(
                    text="Cancel",
                    theme_text_color="Custom",
                    icon="cancel",
                    text_color=(1, 0, 0.3, 1),
                    on_press=lambda x: self.manage_wl_cancel()
                ),
            ],
        )
        self.dialog.open()

    def enable_not_supported_wl(self,id,name):
        self.dialog = MDDialog(
            title="What action would you like to take for {}?".format(name),
            text="ENABLE: Enabling a WL will allow for the associated threat intel to be overlaid on all data, and hits can be viewed on the [Enforce > Watchlists] Page.\n\nALERT: Alerting is NOT SUPPORTED for this specific feed.",
            buttons=[
                MDRoundFlatIconButton(
                    text="Enable",
                    theme_text_color="Custom",
                    icon="eye-check-outline",
                    on_press=lambda x: self.enable_wl(id,name)
                ),
                MDRoundFlatIconButton(
                    text="Cancel",
                    theme_text_color="Custom",
                    icon="cancel",
                    text_color=(1, 0, 0.3, 1),
                    on_press=lambda x: self.manage_wl_cancel()
                ),
            ],
        )
        self.dialog.open()

    def disable_not_supported_wl(self,id,name):

        self.dialog = MDDialog(
            title="What action would you like to take for {}?".format(name),
            text="ENABLE: Enabling a WL will allow for the associated threat intel to be overlaid on all data, and hits can be viewed on the [Enforce > Watchlists] Page.\n\nALERT: Alerting is NOT SUPPORTED for this specific feed.",
            buttons=[
                MDRoundFlatIconButton(
                    text="Disable",
                    theme_text_color="Custom",
                    icon="eye-off-outline",
                    on_press=lambda x: self.disable_wl(id,name)
                ),
                MDRoundFlatIconButton(
                    text="Cancel",
                    theme_text_color="Custom",
                    icon="cancel",
                    text_color=(1, 0, 0.3, 1),
                    on_press=lambda x: self.manage_wl_cancel()
                ),
            ],
        )
        self.dialog.open()

    def manage_wl_cancel(self):
        self.dialog.dismiss(force=True)

    def enable_wl(self,id,name):
        enable_route = "/threathunter/watchlistmgr/v3/orgs/{}/watchlists/{}/tag".format(final_org_key[0],id)
        enable_url = url_base+enable_route

        body = {"tag": True}

        r = requests.put(url=enable_url, headers=self.header, json=body)
        print(r)
        if r.status_code == 200:
            self.dialog.dismiss(force=True)
            self.ids.not_enabled.clear_widgets()
            self.ids.enabled.clear_widgets()
            self.ids.alerted.clear_widgets()
            self.initWindow()
            self.initWl()
            Snackbar(text="{} Watchlist successfully Enabled!".format(name)).open()
        else:
            Snackbar(text="There was an issue enabling {}.".format(name)).open()

    def disable_wl(self,id,name):
        disable_route = "/threathunter/watchlistmgr/v3/orgs/{}/watchlists/{}/tag".format(final_org_key[0],id)
        disable_url = url_base+disable_route

        r = requests.delete(url=disable_url, headers=self.header)
        print(r)
        if r.status_code == 204:
            self.dialog.dismiss(force=True)
            self.ids.not_enabled.clear_widgets()
            self.ids.enabled.clear_widgets()
            self.ids.alerted.clear_widgets()
            self.initWindow()
            self.initWl()
            Snackbar(text="{} Watchlist successfully Disabled!".format(name)).open()
        else:
            Snackbar(text="There was an issue disabling {}.".format(name)).open()

    def enable_alert_wl(self,id,name):
        alert_route = "/threathunter/watchlistmgr/v3/orgs/{}/watchlists/{}/alert".format(final_org_key[0],id)
        alert_url = url_base+alert_route

        body = {"alert": True}

        r = requests.put(url=alert_url, headers=self.header, json=body)
        print(r)
        if r.status_code == 200:
            self.dialog.dismiss(force=True)
            self.ids.not_enabled.clear_widgets()
            self.ids.enabled.clear_widgets()
            self.ids.alerted.clear_widgets()
            self.initWindow()
            self.initWl()
            Snackbar(text="{} Watchlist Alerting successfully Enabled!".format(name)).open()
        else:
            Snackbar(text="There was an issue alerting on {}.".format(name)).open()

    def disable_alert_wl(self,id,name):
        disable_route = "/threathunter/watchlistmgr/v3/orgs/{}/watchlists/{}/alert".format(final_org_key[0],id)
        disable_url = url_base+disable_route

        r = requests.delete(url=disable_url, headers=self.header)

        print(r)
        self.dialog.dismiss(force=True)
        self.ids.not_enabled.clear_widgets()
        self.ids.enabled.clear_widgets()
        self.ids.alerted.clear_widgets()
        self.initWindow()
        self.initWl()
        Snackbar(text="{} Watchlist alerting successfully disabled!".format(name)).open()

    def enable_both(self,id,name):
        self.enable_wl(id,name)
        self.enable_alert_wl(id,name)

    def disable_both(self,id,name):
        self.disable_alert_wl(id,name)
        self.disable_wl(id,name)

class Converter(Screen):
    def __init__(self, name, sm):
        """
        Init the sub-class and Screen super class.
        :param name:
        :param sm:
        """
        super().__init__() # Python3
        self.sm = sm
        self.set_wl_id = []
        self.alerting = []

    def initNav(self):
        if len(nav_dedoup3) == 0:
            self.basic_nav = Builder.load_file("pages/nav_drawer.kv")
            self.add_widget(self.basic_nav)
            nav_dedoup3.append("added")

    def initWindow(self):

        current_wls = []
        self.current_wls_name = []
        self.current_wls_ids = []


        self.alerting.clear()
        self.set_wl_id.clear()

        self.header = {
            "Content-Type": "application/json",
            "X-Auth-Token": final_api_key[0] + "/" + final_api_id[0],
            "org_key": final_org_key[0]
        }

        wl_route = "/threathunter/watchlistmgr/v3/orgs/{}/watchlists".format(final_org_key[0])
        get_wls_url = url_base+wl_route

        r = requests.get(url=get_wls_url, headers=self.header)
        print(r)
        r1 = r.json()
        try:
            for x in r1['results']:
                if x['classifier'] == None:
                    current_wls.append(x)
                    self.current_wls_name.append(x['name'])
                    self.current_wls_ids.append(x['id'])
        except:
            pass


        menu_items = [
            {
                "viewclass": "Item",
                "left_icon": "tools",
                "height": dp(56),
                "text": "{}".format(i['name']),
                "on_release": lambda x="{}".format(i['name']): self.set_item(x),
            } for i in current_wls]

        self.menu = MDDropdownMenu(
            caller=self.ids.menu,
            items=menu_items,
            position="bottom",
            width_mult=7,
        )

    def set_item(self, text__item):
        self.set_wl_id.clear()

        self.ids.menu.text = text__item

        for x in range(len(self.current_wls_name)):
            print(self.current_wls_name[x])
            print(text__item)
            if self.current_wls_name[x] == text__item:
                self.set_wl_id.append(self.current_wls_ids[x])

        print(self.set_wl_id)

        self.menu.dismiss()
    def enable_alerting(self, checkbox, value):
        if value:
            print("Alerting Enabled")
            self.alerting.append("enabled")
        else:
            print("Alerting Disabled")
            self.alerting.clear()

    def add_wl(self):
        self.set_wl_id.clear()

        wl = self.ids.new_wl.text
        name = self.ids.new_name.text
        description = self.ids.new_description.text
        severity = int(self.ids.new_severity.text)
        query = self.ids.new_query.text

        self.convert_legacy(wl,severity,name,description,query)


    def add_report(self):
        wl = self.set_wl_id[0]

        name = self.ids.name.text
        description = self.ids.description.text
        severity = int(self.ids.severity.text)

        query = self.ids.query.text

        self.convert_legacy(wl,severity,name,description,query)

    def convert_legacy(self, wl,severity,name, description, query):


        convert_route = "/threathunter/feedmgr/v2/query/translate"
        convert_url = url_base+convert_route

        body = {"query": query}

        r = requests.post(url=convert_url, headers=self.header, json=body)
        print(r)
        if r.status_code == 200:
            r1 = r.json()
            print(r1)
            final_query = r1['query']
            self.create_report(wl,severity,name,description,final_query)

        else:
            self.convert_error()

    def create_report(self,wl,severity,name,description,final_query):

        create_report_route = "/threathunter/watchlistmgr/v3/orgs/{}/reports".format(final_org_key[0])
        create_report_url = url_base+create_report_route

        body = {
            "title": name,
            "description": description,
            "timestamp": int(time.time()),
            "severity": severity,
            "iocs_v2": [
                {"id": str(int(time.time())),
                                "match_type": "query",
                                "values": [final_query]
                                }
            ],
        }

        r = requests.post(url=create_report_url, headers=self.header, json=body)
        print(r)

        if r.status_code == 200:
            print("Successfully created report")
            r1 = r.json()
            report_id = r1['id']
            if len(self.set_wl_id) > 0:
                self.add_report_to_wl(report_id)
            else:
                self.create_wl(wl,report_id,name)

        else:
            self.report_creation_error()

    def create_wl(self, wl,report_id,name):
        wl_route = "/threathunter/watchlistmgr/v3/orgs/{}/watchlists".format(final_org_key[0])
        create_wl_url = url_base + wl_route
        if len(self.alerting) > 0:
            body = {
                "name": wl,
                "description": "Custom WL",
                "tags_enabled": True,
                "alerts_enabled": True,
                "report_ids": [report_id],
                "classifier": None
            }

            r = requests.post(url=create_wl_url, headers=self.header, json=body)
            print(r)
            print(body)
            if r.status_code == 200:
                Snackbar(text="Successfully created WL {} with report {}".format(wl,name)).open()
                self.ids.new_wl.text = ""
                self.ids.new_name.text = ""
                self.ids.new_description.text = ""
                self.ids.new_query.text = ""
                self.ids.new_severity.text = str(5)
                self.ids.alert_toggle.active = False
                self.initWindow()
            else:
                self.wl_creation_error()
        else:
            body = {
                "name": wl,
                "description": "Custom WL",
                "tags_enabled": True,
                "alerts_enabled": False,
                "report_ids": [report_id],
                "classifier": None
            }

            r = requests.post(url=create_wl_url, headers=self.header, json=body)
            print(r)
            print(body)
            if r.status_code == 200:
                Snackbar(text="Successfully created WL {} with report {}".format(wl, name)).open()
                self.ids.new_wl.text = ""
                self.ids.new_name.text = ""
                self.ids.new_description.text = ""
                self.ids.new_query.text = ""
                self.ids.new_severity.text = str(5)
            else:
                self.wl_creation_error()


    def add_report_to_wl(self,report_id):
        wl_id = self.set_wl_id
        wl_route = "/threathunter/watchlistmgr/v3/orgs/{}/watchlists/{}".format(final_org_key[0],wl_id[0])
        wl_url = url_base+wl_route

        r = requests.get(url=wl_url, headers=self.header)
        print(r)
        if r.status_code == 200:
            r1 = r.json()
            print(r1)
            report_ids = r1['report_ids']
            report_ids.append(report_id)
            body = {
                "name": r1['name'],
                "description": r1['description'],
                "tags_enabled": r1['tags_enabled'],
                "alerts_enabled": r1['alerts_enabled'],
                "report_ids": report_ids,
                "classifier": None
            }
            r2 = requests.put(url=wl_url, headers=self.header, json=body)
            print(r2)
            if r2.status_code == 200:
                Snackbar(text="Successfully added report to specified Watchlist").open()
                self.ids.menu.text = ""
                self.ids.name.text = ""
                self.ids.description.text = ""
                self.ids.query.text = ""
                self.ids.severity.text = str(5)
            else:
                self.report_addition_error()

        else:
            self.report_addition_error()

    def wl_creation_error(self):

        self.dialog = MDDialog(
            title="Report Creation Error",
            text="Hmmm...the query converted successfully, the report was created successfully, but creating the WL and/or adding the report to the new WL seems to have failed. Please check your inputs to ensure you have all the required fields.\n\nIf this issue persists, you can always manually create the desired WL and add the to said WL, as the report will be searchable in the console under:\n\n[Enforce > Watchlists > Add Watchlist > Build Tab]"
        )
        self.dialog.open()
    def report_addition_error(self):

        self.dialog = MDDialog(
            title="Report Creation Error",
            text="Hmmm...the query converted successfully, the report was created successfully, but adding it to the desired WL seems to have failed. Please check your inputs to ensure you have all the required fields.\n\nIf this issue persists, you can always manually add it to the desired WL, as the report will be searchable in the console under:\n\n[Enforce > Watchlists > Add Watchlist > Build Tab]"
        )
        self.dialog.open()


    def report_creation_error(self):

        self.dialog = MDDialog(
            title = "Report Creation Error",
            text = "Hmmm...the query converted successfully, but the report creation failed. Please check your inputs to ensure you have all the required fields. Perhaps special characters in the name or description may be causing issues."
        )
        self.dialog.open()

    def convert_error(self):

        self.dialog = MDDialog(
            title = "Query Conversion Error",
            text= "We're sorry, there was an error attempting to convert your CBR query to EEDR syntax.\n\nPlease check your query, however it is possible that this query is simply not compatable. Possible causes:\n\n    - Malformed Query\n    - Unsupported Field\n      - (i.e. a CBR field used in the query not supported by EEDR)\n    - Other:\n      - Invalid Cred/Permissions\n      - Sytanctical conversion error (i.e.'\\n' in python conversion)\n      - Internal server/general error"
        )
        self.dialog.open()

        self.ids.query.text = ''

    def add_alert_severity(self):
        if int(self.ids.severity.text) < 10:
            severity = int(self.ids.severity.text) + 1
            self.ids.severity.text = str(severity)
    def minus_alert_severity(self):
        if int(self.ids.severity.text) > 1:
            severity = int(self.ids.severity.text) - 1
            self.ids.severity.text = str(severity)

    def add_new_alert_severity(self):
        if int(self.ids.new_severity.text) < 10:
            severity = int(self.ids.new_severity.text) + 1
            self.ids.new_severity.text = str(severity)
    def minus_new_alert_severity(self):
        if int(self.ids.new_severity.text) > 1:
            severity = int(self.ids.new_severity.text) - 1
            self.ids.new_severity.text = str(severity)

    def cleanup(self):
        self.set_wl_id.clear()
        self.alerting.clear()


### MAIN APP ###
class CB_Open_Source_Intel(MDApp):
    def build(self):
        self.sm = MyScreenManager()

        lw = Builder.load_file('pages/login.kv')
        loginScreen = LoginWindow(name="login", sm=self.sm)
        self.sm.add_widget(loginScreen)

        hs = Builder.load_file('pages/home.kv')
        home = Home(name="home", sm=self.sm)
        self.sm.add_widget(home)

        cs = Builder.load_file('pages/feeds.kv')
        self.feeds = Feeds(name="feeds", sm=self.sm)
        self.sm.add_widget(self.feeds)

        wl = Builder.load_file('pages/watchlists.kv')
        self.watchlists = Watchlists(name="watchlists", sm=self.sm)
        self.sm.add_widget(self.watchlists)

        cv = Builder.load_file('pages/converter.kv')
        converter = Converter(name="converter", sm=self.sm)
        self.sm.add_widget(converter)


        self.sm.current = "login"

        return self.sm

    def on_checkbox_active(self, checkbox, value):
        if value:
            print('CBR Converter Enabled')
            cbr_active.append("true")
        else:
            print('CBR Converter Disabled')
            cbr_active.clear()


CB_Open_Source_Intel().run()
