from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from lfs.core.models import Country

from ups.client import PACKAGES as UPS_PACKAGES


class UPSConfiguration(models.Model):
    """
        Contains the UPS configuration for the current site
    """

    site = models.ForeignKey(Site)
    username = models.CharField(_('User name for UPS Account'), max_length=128)
    password = models.CharField(_('Password'), max_length=128)
    shipper_number = models.CharField(_('Shipper Number'), max_length=128)
    access_license = models.CharField(_('API Key'), max_length=128)

    default_packaging_type = models.CharField(
        _('Default package type'),
        max_length=2,
        choices=UPS_PACKAGES,
        default='02', #UPS Custom packaging
    )

    shipper_name = models.CharField(_('Company name'), max_length=256)
    shipper_address = models.CharField(_('Address'), max_length=256)
    shipper_city = models.CharField(_('City'), max_length=256)
    shipper_state = models.CharField(_('State'), max_length=128)
    shipper_zipcode = models.CharField(_('Zip code'), max_length=32)
    shipper_country = models.ForeignKey(Country, verbose_name=_("Country"))
