from django.contrib.sites.models import get_current_site

from lfs.cart.utils import get_cart
from lfs.customer.utils import get_customer
from lfs.plugins import ShippingMethodPriceCalculator

from ups.client import UPSClient
from ups.model import Package, Address

from .models import UPSConfiguration


class UPSPriceCalculator(ShippingMethodPriceCalculator):
    #Cache price
    _price = None

    def _ups_config(self):
        site = get_current_site(self.request)
        return UPSConfiguration.objects.get(site=site)

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
            address=ups_cfg.shipper_address,
            city=ups_cfg.shipper_city,
            state=ups_cfg.shipper_state,
            zip=ups_cfg.shipper_zipcode,
            country=ups_cfg.shipper_country.code
        )

        customer = get_customer(self.request)
        ship_address = customer.get_selected_shipping_address()
        recipient = Address(
            name=' '.join([ship_address.firstname, ship_address.lastname]),
            address=' '.join([ship_address.line1, ship_address.line2]),
            city=ship_address.city,
            state=ship_address.state,
            zip=ship_address.zip_code,
            country=ship_address.country.code
        )

        cart = get_cart(self.request)

        #weight, length, width, height
        product_info = [0, 0, 0, 0] 
        for line_item in cart.get_items():
            product_info[0] += line_item.product.weight
            product_info[1] += line_item.product.length
            product_info[2] += line_item.product.width
            product_info[3] += line_item.product.height

        quote = 0.0
        if all(product_info):
            packages = [Package(*product_info)]
            ups = UPSClient(credentials, weight_unit='KGS', dimension_unit='CM', currency_code='USD')
            response = ups.rate(
                packages=packages,
                packaging_type=ups_cfg.default_packaging_type,
                shipper=shipper,
                recipient=recipient
            )
            quote = float(response['info'][0]['cost'])

        return quote

    def get_price_net(self):
        return self.get_price_gross()

    def get_price_gross(self):
        #XXX No error handler :P
        # return self.get_price_net() * ((100 + self.shipping_method.tax.rate) / 100)
        if self._price is None:
            self._price = self._get_quote()
        return self._price

    def get_tax(self):
        #How do I calculate taxes?
        return 0.0