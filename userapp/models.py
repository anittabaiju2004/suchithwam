from django.db import models

from adminapp.models import Ward  # Import the Ward model from adminapp

class tbl_register(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    pswd = models.CharField(max_length=100)
    place = models.CharField(max_length=100)  
    address = models.TextField(max_length=255) 
    phone = models.CharField(max_length=100)
    utype = models.CharField(max_length=100, default="user")
    
    # ForeignKey to the Ward model
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True)  # link to Ward model
    location = models.CharField(max_length=255, null=True, blank=True)  # Store location info if needed
    
    def __str__(self):
        return self.name



from django.db import models
from adminapp.models import tbl_category
from userapp.models import tbl_register



# class WasteSubmission(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('complete', 'Complete'),
#         ('incomplete', 'Incomplete'),
#     ]

#     user = models.ForeignKey(tbl_register, on_delete=models.CASCADE)
#     date = models.DateField()
#     time = models.TimeField()
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

#     def __str__(self):
#         return f"{self.user.name} - {self.date} ({self.get_status_display()})"
class WasteSubmission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('complete', 'Complete'),
        ('incomplete', 'Incomplete'),
    ]

    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def total_price(self):
        total = 0
        for detail in self.details.all():  # 'details' is the related name
            total += detail.calculate_price()  # Use the method in WasteSubmissionDetail
        return total

    def __str__(self):
        return f"{self.user.name} - {self.date} ({self.get_status_display()})"


class WasteSubmissionDetail(models.Model):
    waste_submission = models.ForeignKey(WasteSubmission, related_name='details', on_delete=models.CASCADE)
    category = models.ForeignKey(tbl_category, on_delete=models.CASCADE)
    kilogram = models.FloatField()

    def calculate_price(self):
        return self.category.price * self.kilogram

    def __str__(self):
        return f"{self.category.name} - {self.kilogram} kg"

class Payment(models.Model):
    PAYMENT_OPTIONS = [
        ('cash', 'Cash '),
        ('card_payment', 'Card Payment'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE)
    waste_submission = models.OneToOneField(WasteSubmission, on_delete=models.CASCADE)
    payment_option = models.CharField(max_length=20, choices=PAYMENT_OPTIONS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Card Payment Details
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    card_number = models.CharField(max_length=16, null=True, blank=True)
    expiry_date = models.CharField(max_length=5, null=True, blank=True)  # Format: MM/YY
    cvv = models.CharField(max_length=3, null=True, blank=True)
    cardholder_name = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = sum(detail.calculate_price() for detail in self.waste_submission.details.all())
        if self.payment_option == 'card_payment' and not self.transaction_id:
            self.transaction_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.name} - {self.payment_option} - {self.status}"
 


from django.db import models
import uuid
from userapp.models import tbl_register
from userapp.models import WasteSubmission


from django.db import models
import uuid
from userapp.models import tbl_register, WasteSubmission


# class Payment(models.Model):
#     PAYMENT_OPTIONS = [
#         ('cash_on_delivery', 'Cash on Delivery'),
#         ('card_payment', 'Card Payment'),
#     ]

#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('cash_on_delivery', 'Cash on Delivery'),
#         ('card_payment', 'Card Payment'),
#     ]

#     user = models.ForeignKey(tbl_register, on_delete=models.CASCADE)
#     waste = models.ForeignKey(WasteSubmission, on_delete=models.CASCADE)
#     payment_option = models.CharField(max_length=20, choices=PAYMENT_OPTIONS)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
#     amount = models.DecimalField(max_digits=10, decimal_places=2, default=50.00)

#     # Card Payment Details
#     transaction_id = models.CharField(max_length=255, null=True, blank=True)
#     card_number = models.CharField(max_length=16, null=True, blank=True)
#     expiry_date = models.CharField(max_length=5, null=True, blank=True)  # Format: MM/YY
#     cvv = models.CharField(max_length=3, null=True, blank=True)
#     cardholder_name = models.CharField(max_length=100, null=True, blank=True)

#     def save(self, *args, **kwargs):
#         if self.payment_option == 'card_payment':
#             if not self.transaction_id:
#                 self.transaction_id = str(uuid.uuid4())
#             self.status = 'card_payment'
#         elif self.payment_option == 'cash_on_delivery':
#             self.transaction_id = "" 
#             self.status = 'cash_on_delivery'
        
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.user.name} - {self.payment_option} - {self.status}"

