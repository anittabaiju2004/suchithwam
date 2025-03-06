from django.db import models

from adminapp.models import Ward  # Import the Ward model from adminapp
from django.db import models
from adminapp.models import Ward  # Import the Ward model from adminapp
from django.db import models
from adminapp.models import Ward  # Import the Ward model from adminapp
from django.db import models
from adminapp.models import Ward  # Import the Ward model from adminapp

from django.db import models
from adminapp.models import Ward  # Import the Ward model from adminapp

class tbl_register(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    pswd = models.CharField(max_length=100)
    place = models.CharField(max_length=100)  
    address = models.TextField(max_length=255) 
    phone = models.CharField(max_length=100)
    utype = models.CharField(max_length=100, default="user")
    # ForeignKey to the Ward model
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True)  # link to Ward model
    # Profile picture field
    profile_picture = models.ImageField(upload_to="profile_pics/", null=True, blank=True)
    # Longitude and Latitude with default value 0.0
    longitude = models.DecimalField(max_digits=11, decimal_places=7, default=0.0)
    latitude = models.DecimalField(max_digits=11, decimal_places=7, default=0.0)

    def __str__(self):
        return self.name



from django.db import models
from adminapp.models import tbl_category
from userapp.models import tbl_register  
from decimal import Decimal

class WasteSubmission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'), 
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('incompleted', 'Incompleted'),
    ]

    user = models.ForeignKey('tbl_register', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    categories = models.TextField()  # Store category IDs as a comma-separated string
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    kilo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Added kilo field
    description = models.TextField(null=True, blank=True)  # ✅ Added description field

    def __str__(self):
        return f"{self.user.name} - {self.date} ({self.get_status_display()})"

import uuid
from django.db import models
from decimal import Decimal

class Payment(models.Model):
    PAYMENT_OPTIONS = [
        ('cash', 'Cash'),
        ('card_payment', 'Card Payment'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('cash', 'Cash'),
        ('card_payment', 'Card Payment'),
    ]

    CASH_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
    ]

    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE)
    waste_submission = models.OneToOneField(WasteSubmission, on_delete=models.CASCADE, null=True, blank=True)
    payment_option = models.CharField(max_length=20, choices=PAYMENT_OPTIONS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cash_status = models.CharField(max_length=10, choices=CASH_STATUS_CHOICES, default='pending', null=True, blank=True)
    # Card Payment Details
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    name_of_card = models.CharField(max_length=255, null=True, blank=True)
    card_number = models.CharField(max_length=16, null=True, blank=True)
    expiry_date = models.CharField(max_length=5, null=True, blank=True)  # Format: MM/YY
    cvv = models.CharField(max_length=3, null=True, blank=True)

    def save(self, *args, **kwargs):
        # If waste_submission exists and has total_price, set it only if not manually updated
        if self.waste_submission and self.waste_submission.total_price and self.total_price == 0.00:
            self.total_price = self.waste_submission.total_price  

        if self.payment_option == 'cash':
            self.status = 'cash'
            
            # Preserve manually updated total_price & cash_status
            if self.total_price == 0.00:
                self.total_price = 0.00  

            if self.cash_status in [None, 'pending']:  
                self.cash_status = 'pending'  

            # Remove card payment details
            self.transaction_id = None
            self.name_of_card = None
            self.card_number = None
            self.expiry_date = None
            self.cvv = None

        elif self.payment_option == 'card_payment':
            self.status = 'card_payment'
            self.cash_status = None  # Not applicable for card payments
            
            # Only generate a transaction_id if it's empty
            if not self.transaction_id:
                self.transaction_id = str(uuid.uuid4())  

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.name} - {self.payment_option} - {self.status} - Cash Status: {self.cash_status or 'N/A'}"
