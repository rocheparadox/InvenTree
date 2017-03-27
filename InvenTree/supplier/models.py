from __future__ import unicode_literals

from django.db import models

from part.models import Part

class Supplier(models.Model):
    """ Represents a manufacturer or supplier
    """
    
    name = models.CharField(max_length=100)
    URL = models.URLField(blank=True)
    address = models.CharField(max_length=200,
                               blank=True)
    phone = models.CharField(max_length=50,
                             blank=True)
    email = models.EmailField(blank=True)
    contact = models.CharField(max_length=100,
                               blank=True)
    notes = models.CharField(max_length=500,
                             blank=True)
    
    def __str__(self):
        return self.name
    
class SupplierPart(models.Model):
    """ Represents a unique part as provided by a Supplier
    Each SupplierPart is identified by a MPN (Manufacturer Part Number)
    Each SupplierPart is also linked to a Part object
    - A Part may be available from multiple suppliers
    """
    
    supplier = models.ForeignKey(Supplier,
                                 on_delete=models.CASCADE)
    part = models.ForeignKey(Part,
                             on_delete=models.CASCADE)
    
    MPN = models.CharField(max_length=100)
    URL = models.URLField(blank=True)
    description = models.CharField(max_length=250,
                                   blank=True)
    
    def __str__(self):
        return "{mpn} - {supplier}".format(
            mpn = self.MPN,
            supplier = self.supplier.name)
    
    
class SupplierPriceBreak(models.Model):
    """ Represents a quantity price break for a SupplierPart
    - Suppliers can offer discounts at larger quantities
    - SupplierPart(s) may have zero-or-more associated SupplierPriceBreak(s)
    """
    
    part = models.ForeignKey(SupplierPart,
                             on_delete=models.CASCADE)
    quantity = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=3)
    currency = models.CharField(max_length=10,
                                blank=True)
    
    def __str__(self):
        return "{mpn} - {cost}{currency} @ {quan}".format(
            mpn = part.MPN,
            cost = self.cost,
            currency = self.currency if self.currency else '',
            quan = self.quantity)