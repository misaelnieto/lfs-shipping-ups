What is it?
===========

LFS Plugin to add support for UPS Quotes

See project wiki for more details: https://bitbucket.org/pigletto/lfs-carousel/wiki/Home

Basic usage
===========

Add your application to the PYTHONPATH.

Add the class ``UPSPriceCalculator`` to the
``LFS_SHIPPING_METHOD_PRICE_CALCULATORS`` setting. Example::
    
    LFS_SHIPPING_METHOD_PRICE_CALCULATORS = [
        ["lfs.shipping.GrossShippingMethodPriceCalculator", _(u'Price includes tax')],
        ["lfs.shipping.NetShippingMethodPriceCalculator", _(u'Price excludes tax')],
        ["lfs_ups.UPSPriceCalculator", _(u'UPS')],
    ]


Add the shipping_ups app to ``settings.INSTALLED_APPS``::


If your are using models (which is completely up to you), add the application
to settings.INSTALLED_APPS and sync your database.

Add a new shipping method and select your UPS from the
``price_calculator`` field.

Save the shipping method.
