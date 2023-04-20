from django.db import models

# Create your models here.


class order_data(models.Model):

    sopnumbe = models.CharField(
        db_column="SOPNUMBE", primary_key=True, max_length=21
    )  # Field name made lowercase.
    cstnmbr = models.CharField(db_column="cstnmbr", max_length=21)
    originalshipdate = models.DateTimeField(db_column="OriginalShipDate")
    product = models.CharField(
        db_column="internalproductname", max_length=21, blank=False
    )
    tons = models.DecimalField(max_digits=7, decimal_places=2)
    projectedshipdate = models.DateTimeField(
        db_column="ProjectedShipDate"
    )  # Field name made lowercase.
    requesteddeliverydate = models.DateTimeField(
        db_column="RequestedDeliveryDate"
    )  # Field name made lowercase.
    truckingconfirmed = models.BooleanField(db_column="TruckingConfirmed")
    shippingcontact = models.TextField(db_column="shippingcontact", blank=True)
    correspondencenotes = models.TextField(
        db_column="CorrespondenceNotes", blank=True
    )  # Field name made lowercase. This field type is a guess.
    shipped = models.BooleanField(db_column="Shipped")

    class Meta:
        managed = False
        db_table = "order_data"
        # unique_together = (('sopnumbe', 'soptype'),)
