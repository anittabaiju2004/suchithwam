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



    
from decimal import Decimal

from decimal import Decimal

class WasteSubmission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'), 
        ('complete', 'Complete'),
        ('incomplete', 'Incomplete'),
    ]

    user = models.ForeignKey('tbl_register', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Make this field nullable

    def __str__(self):
        return f"{self.user.name} - {self.date} ({self.get_status_display()})"

# class WasteSubmission(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('complete', 'Complete'),
#         ('incomplete', 'Incomplete'),
#     ]

#     user = models.ForeignKey('tbl_register', on_delete=models.CASCADE)
#     date = models.DateField()
#     time = models.TimeField()
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

#     def total_price(self):
#         # Sum the price of each category detail in the submission
#         total = Decimal(0)  # Use Decimal for precision
#         for detail in self.details.all():
#             total += detail.calculate_price()  # Add the price of each category for each detail
#         return total

#     def __str__(self):
#         return f"{self.user.name} - {self.date} ({self.get_status_display()})"

from decimal import Decimal
# class WasteSubmissionDetail(models.Model):
#     waste_submission = models.ForeignKey(WasteSubmission, related_name='details', on_delete=models.CASCADE)
#     category = models.ForeignKey('adminapp.tbl_category', on_delete=models.CASCADE)
#     kilogram = models.FloatField()

#     def calculate_price(self):
#         # Return the price of the current category for this detail, no summing with other categories
#         return self.category.price

#     def __str__(self):
#         return f"{self.category.name} - {self.kilogram} kg"
    

class WasteSubmissionDetail(models.Model):
    waste_submission = models.ForeignKey(WasteSubmission, related_name='details', on_delete=models.CASCADE)
    category = models.ForeignKey('adminapp.tbl_category', on_delete=models.CASCADE)
    kilogram = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # New field to store price

    def calculate_price(self):
        # Fetch and return the price from the category
        return self.category.price

    def save(self, *args, **kwargs):
        # Automatically set price based on category before saving
        if not self.price:  # Only set price if it's not already set
            self.price = self.category.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} - {self.kilogram} kg - Price: {self.price}"




import uuid
from decimal import Decimal
from django.db import models

class Payment(models.Model):
    PAYMENT_OPTIONS = [
        ('cash', 'Cash'),
        ('card_payment', 'Card Payment'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE)
    waste_submission = models.OneToOneField(WasteSubmission, on_delete=models.CASCADE, null=True, blank=True)
    name_of_card = models.CharField(max_length=255, null=True, blank=True)
    payment_option = models.CharField(max_length=20, choices=PAYMENT_OPTIONS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Card Payment Details
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    card_number = models.CharField(max_length=16, null=True, blank=True)
    expiry_date = models.CharField(max_length=5, null=True, blank=True)  # Format: MM/YY
    cvv = models.CharField(max_length=3, null=True, blank=True)

    def save(self, *args, **kwargs):
    # Ensure waste_submission is not None before accessing total_price
        if self.waste_submission and not self.price:
            if self.waste_submission.total_price is not None:
                self.price = self.waste_submission.total_price  # Access it as a field, not a method
            else:
                raise ValueError("Total price is not set for this WasteSubmission instance.")

    # Handle card payment details
        if self.payment_option == 'card_payment' and not self.transaction_id:
            self.transaction_id = str(uuid.uuid4())  # Generate a transaction ID if not provided

        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.user.name} - {self.payment_option} - {self.status}"

 


# from django.db import models
# import uuid
# from userapp.models import tbl_register
# from userapp.models import WasteSubmission


# from django.db import models
# import uuid
# from userapp.models import tbl_register, WasteSubmission


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

