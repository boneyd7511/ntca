from django.contrib.contenttypes.models import ContentType

#from nautobot.apps.jobs import Job, register_jobs
from nautobot.core.celery import register_jobs
from nautobot.apps.jobs import Job, StringVar, IntegerVar, ObjectVar
from nautobot.dcim.models import Location, LocationType, Device, Manufacturer, DeviceType
from nautobot.extras.models import Status, Role
from nautobot_device_lifecycle_mgmt.models import CVELCM


class ProvisionCVE(Job):
    class Meta:
        name = "Provision CVEs"
        description = "Pull CVEs from the internet and propogate them into Nautobot."

    def run(self):
        # Create the new location

        cve_name = "CVE-2024-20303"
        cve_published_date = "2024-04-02"
        cve_link = "https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-wlc-mdns-dos-4hv6pBGf"

        cve = CVELCM(name=cve_name, published_date=cve_published_date, link=cve_link)

        cve.validated_save()

register_jobs(ProvisionCVE)
