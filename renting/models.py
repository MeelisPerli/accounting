from django.db import models


# The Rental model represents a rental property.
class Rental(models.Model):
    rental_id = models.AutoField(primary_key=True)  # The unique ID of the rental property.
    address = models.CharField(max_length=255)  # The address of the rental property.
    room_nr = models.IntegerField()  # The number of rooms in the rental property.
    description = models.TextField()  # A description of the rental property.
    
    def __str__(self):
        return str(self.address) + ", room: " + str(self.room_nr)   # or any other field that you want to display

# The Deposit model represents a deposit made by a renter.
class Deposit(models.Model):
    STATUS_CHOICES = [
        ("HOLDING", 'Holding'),
        ("PAID_BACK", 'Paid back'),
        ("PARTIAL_PAID_BACK", 'Partial paid back'),
        ("COVERED_RENT", 'Covered rent')
    ]

    deposit_id = models.AutoField(primary_key=True)  # The unique ID of the deposit.
    deposit_amount = models.DecimalField(max_digits=7, decimal_places=2)  # The amount of the deposit.
    deposit_date = models.DateField()  # The date the deposit was made.
    referral_id = models.CharField(max_length=32, db_index=True)  # The ID of the referral associated with the deposit.
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="HOLDING")  # The status of the deposit.
    paid_back_date = models.DateField(null=True)  # The date the deposit was paid back. This can be null if the deposit hasn't been paid back yet.
    return_referral_id = models.IntegerField(null=True)  # The ID of the referral associated with the return of the deposit. This can be null if the deposit hasn't been returned yet.
    
# The Renter model represents a person who is renting a property.
class Renter(models.Model):
    renter_id = models.AutoField(primary_key=True)  # The unique ID of the renter.
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    deposit = models.ForeignKey(Deposit, on_delete=models.CASCADE)
    renter_name = models.CharField(max_length=255)  # The name of the renter.
    monthly_rent = models.DecimalField(max_digits=7, decimal_places=2)  # The monthly rent amount.
    monthly_communals = models.DecimalField(max_digits=7, decimal_places=2)  # The monthly communal charges.
    begin_date = models.DateField()  # The date the renter started renting.
    end_date = models.DateField(null=True)  # The date the renter stopped renting. This can be null if the renter is still renting.
