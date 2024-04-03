from django.contrib.contenttypes.models import ContentType

from nautobot.core.celery import register_jobs
from nautobot.apps.jobs import Job, StringVar, IntegerVar, ObjectVar
from nautobot.dcim.models import Location, LocationType, Device, Manufacturer, DeviceType, Platform
from nautobot.extras.models import Status, Role
from nautobot_device_lifecycle_mgmt.models import CVELCM, SoftwareLCM

import requests
from bs4 import BeautifulSoup


class ProvisionCVE(Job):
    class Meta:
        name = "Provision CVEs"
        description = "Pull CVEs from the internet and propogate them into Nautobot."
        
    def run(self):
        
        #LocationType.objects.get_or_create(name="Campus")
        
        cve_name = "CVE-2024-20303"
        cve_published_date = "2024-04-02"
        cve_link = "https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-wlc-mdns-dos-4hv6pBGf"
        
        cve_name2 = "CVE-2024-203034"
        cve_published_date2 = "2024-04-02"
        cve_link2 = "https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-wlc-mdns-dos-4hv6pBGf2"

        cve = CVELCM(name=cve_name, published_date=cve_published_date, link=cve_link)
        cve2 = CVELCM(name=cve_name2, published_date=cve_published_date2, link=cve_link2)

        cve.validated_save()
        cve2.validated_save()

register_jobs(ProvisionCVE)
