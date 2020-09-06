from django.db import models

from datetime import datetime
class Lot(models.Model):
    STATUS =(
        ('Available', 'Available'),
        ('Sold', 'Sold')
    )
    scrap_category = models.CharField(max_length=200,)
    purchased_date = models.DateTimeField(default=datetime.now, blank=True)
    quantity = models.FloatField(default=0.0)
    rate = models.FloatField(default=0.0)
    status= models.CharField(max_length=200,default='Available', choices=STATUS)
    description = models.TextField(blank=True)
    sold_at = models.FloatField(null=True, blank=True, default=None)

    

    @property
    def total(self):
        return self.quantity *self.rate 

    def __str__(self):
        return self.scrap_category



class Expenses(models.Model):
    CATEGORY=(
        ('Labour', 'Labour'),
        ('Personal', 'Personal'),
        ('Supplies', 'Supplies'),
        ('Business Purchases','Business Purchases'),
        ('Mall', 'Mall'),
        ('Warehouse','Warehouse'),
        ('Other', 'Other')
    )

    TYPE=(
        ('Cash','Cash'),
        ('Card', 'Card')
    )

    ENTRY=(
        ('Debited','Debited'),
        ('Credited', 'Credited'),
    )

    entry = models.CharField(max_length=200, default=None, choices=ENTRY)
    handler = models.CharField(max_length=200,default=None)
    date = models.DateTimeField(default=datetime.now, null=True)
    category = models.CharField(max_length=200,default='Other', choices=CATEGORY)
    amount = models.FloatField(null=True)
    type_of_transaction= models.CharField(max_length=200, default=None, choices=TYPE)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.handler