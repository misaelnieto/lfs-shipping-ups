from ups.client import UPSClient
from ups.model import Package, Address
from django.contrib.sites.models import get_current_site
from lfs.customer.utils import get_customer
from lfs.plugins import ShippingMethodPriceCalculator

from .model import UPSConfiguraton


class UPSPriceCalculator(ShippingMethodPriceCalculator):
    def _ups_config(self):
        site = get_current_site(self.request)
        return UPSConfiguraton.objects.get(site=site)

    def _get_quote(self):
        ups_cfg = self._ups_config()

        credentials = {
            'username': ups_cfg.username,
            'password': ups_cfg.password,
            'access_license': ups_cfg.access_license,
            'shipper_number': ups_cfg.shipper_number,
        }

        shipper = Address(
            name=ups_cfg.shipper_name, 
            address=ups_shipper_address,
            city=ups_cfg.shipper_city,
            state=ups_cfg.shipper_state,
            zip=ups_cfg.shipper_zip,
            country=ups_cfg.country.code
        )

        customer = get_customer(self.request)
        ship_address = customer.get_selected_shipping_address()
        recipient = Address(
            name=' '.join(ship_address.firstname, ship_address.lastname),
            address=' '.join(ship_address.line1, ship_address.line2),
            city=ship_address.city,
            state=ship_address.state,
            zip=ship_address.zip_code,
            country=ship_address.country.code
        )

        packages = [Package(2, 3, 4, 5)]
        ups = UPSClient(credentials)
        return ups.rate(
            packages=packages,
            packaging_type='2a',
            shipper=shipper,
            recipient=recipient
        )


    def get_price_net(self):
        #XXX No error handler :P
        response = self._get_quote()
        return response.['info'][0]['cost']

    def get_price_gross(self):
        return self.get_price_net() * ((100 + self.shipping_method.tax.rate) / 100)

    def get_tax(self):
        """
        Returns the total tax of the shipping method.
        """
        return self.get_price_gross() - self.get_price_net()

