from django.contrib.contenttypes.models import ContentType

from nautobot.core.celery import register_jobs
from nautobot.apps.jobs import Job, StringVar, IntegerVar, ObjectVar
from nautobot.dcim.models import Location, LocationType, Device, Manufacturer, DeviceType, Platform
from nautobot.extras.models import Status, Role
from nautobot_device_lifecycle_mgmt.models import CVELCM, SoftwareLCM

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import requests
import os
import json


class ProvisionCVE(Job):
    class Meta:
        name = "Provision CVEs"
        description = "Pull CVEs from the internet and propogate them into Nautobot."

    cves = []
    cves_id = []
    cve_file_name = "cve_file.json"

    def scrape_webpage(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless") 
        chrome_options.add_argument("--window-size=1920x1080")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://sec.cloudapps.cisco.com/security/center/publicationListing.x")
        driver.implicitly_wait(5)
        time.sleep(7)
        page_source = driver.page_source
        driver.quit()

        soup = BeautifulSoup(page_source, "html.parser")
        data = soup.find_all("span", class_="ng-binding")

        for i in range(0,len(data)):
            if data[i].text.startswith("CVE") and data[i].text not in self.cves:
                self.cves.append(data[i].text)
            elif data[i].text.startswith("cisco-sa") and data[i].text not in self.cves_id:
                self.cves_id.append(data[i].text)

    def download_file(self, url, filename):
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Open a new file in binary write mode and write the content of the response
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"File downloaded successfully: {filename}")
        else:
            print(f"Failed to download file: {url}")

    def extract_service_packs(self, data, target_product_family):
        service_packs = []

        if isinstance(data, dict):
            # Check if the current node represents a branch
            if 'name' in data and data.get('category') == 'product_family' and data.get('name') == target_product_family:
                # Extract service packs directly under the target product family
                if 'branches' in data:
                    for branch in data['branches']:
                        if branch.get('category') == 'product_version' and 'branches' in branch:
                            for sub_branch in branch['branches']:
                                if sub_branch.get('category') == 'service_pack' and 'name' in sub_branch:
                                    # Append the service pack name to the list
                                    service_packs.append(sub_branch['name'])
            else:
                # Recursively search deeper if the current node has nested branches
                if 'branches' in data:
                    for branch in data['branches']:
                        service_packs.extend(self.extract_service_packs(branch, target_product_family))

        return service_packs
        
    def run(self):
        
        self.scrape_webpage()
        
        #If CVE is not already in nautobot
        cve_url = "https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/" + self.cves_id[0] + "/csaf/" + self.cves_id[0]+ ".json"
        self.download_file(cve_url, self.cve_file_name)
        
        # Load JSON data from the file
        with open(self.cve_file_name, 'r', encoding='utf-8') as file:
            json_data = json.load(file)

        # Extract service packs under the specified product family
        ios_service_packs = self.extract_service_packs(json_data['product_tree'], 'IOS')
        ios_xe_service_packs = self.extract_service_packs(json_data['product_tree'], 'Cisco IOS XE Software')

        # Print the extracted service pack names
        if ios_service_packs:
            print(f"Service Packs under IOS:")
            for sp in ios_service_packs:
                print(sp)
        else:
            print(f"No service packs found under IOS product family.")

        if ios_xe_service_packs:
            print(f"Service Packs under IOS-XE:")
            for sp in ios_xe_service_packs:
                print(sp)
        else:
            print(f"No service packs found under IOS-XE product family.")
        
        #LocationType.objects.get_or_create(name="Campus")
        
        cve_name = "CVE-2024-20303"
        cve_published_date = "2024-04-02"
        cve_link = "https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-wlc-mdns-dos-4hv6pBGf"

        cve = CVELCM(name=cve_name, published_date=cve_published_date, link=cve_link)
        cve.validated_save()
     

register_jobs(ProvisionCVE)
