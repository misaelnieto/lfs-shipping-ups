from django.conf import settings

UPS_USERNAME = getattr(settings, 'UPS_PUBLIC_FOLDER')
UPS_PASSWORD = getattr(settings, 'UPS_PASSWORD')
UPS_ACCESS_LICENSE = getattr(settings, 'UPS_ACCESS_LICENSE')
UPS_SHIPPER_NUMBER = getattr(settings, 'UPS_SHIPPER_NUMBER')
