import requests
import json
import sys
import urllib3
import apiconf
import time
import argparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Argparse section
parser = argparse.ArgumentParser()
parser.add_argument("-ip", help="Example 172.31.0.100", required=True)
args = parser.parse_args()
template_ip = args.ip

# Globals
baseurl = 'https://' + template_ip + ':443' # Connecting to vfw instance API
retr_path = "/retrieve"
config_path = "/configure"
save_path = "/config-file"
headers = {}
apireq = apiconf.apireq

def main():

        eth_list = get_interfaces()
        if len(eth_list) > 0:
                for eth in eth_list:
                        deleted = delete_hwid(eth)
                        
        if deleted == True:
             save_config() 
                                             
# Get interfaces and append them to a list
def get_interfaces():
        with requests.Session() as s:
                apireq['data'] = '{"op": "showConfig", "path": ["interfaces", "ethernet"]}' 
                try: 
                        response = s.post(baseurl + retr_path, headers=headers, data=apireq, verify=False)
                        jsonResponse = json.loads(response.text)
                except requests.exceptions.HTTPError as e:
                        print (e.response.text)
                if jsonResponse['success']:
                        eth_list = []
                        for eth in jsonResponse['data']['ethernet']:
                                eth_list.append(eth)
                else: 
                        sys.exit(2)

                return eth_list

# Delete hw id from interfaces
def delete_hwid(eth):
        deleted = False
        with requests.Session() as s:
                # Set new hostname
                apireq['data'] = '{"op": "delete", "path": ["interfaces", "ethernet","' + eth +'", "hw-id"]}'
                try: 
                        response = s.post(baseurl + config_path, headers=headers, data=apireq, verify=False)
                        jsonResponse = json.loads(response.text)
                except requests.exceptions.HTTPError as e:
                        print (e.response.text)
                if jsonResponse['success']:
                        print("HW-ID deleted for", eth)
                        deleted = True
                else:
                        print("nothing deleted exiting..")
                        sys.exit(2)
        return deleted

#  Save config to file.
def save_config():
         with requests.Session() as s:            
                # Save config to mem(file)
                apireq['data'] = '{"op": "save", "file": "/config/config.boot"}'
                try: 
                        response = s.post(baseurl + save_path, headers=headers, data=apireq, verify=False)
                        jsonResponse = json.loads(response.text)
                except requests.exceptions.HTTPError as e:
                        print (e.response.text)
                if jsonResponse['success']:
                        print(jsonResponse['data'])
                else:
                        sys.exit(2)

main()




