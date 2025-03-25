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
    longitude = models.DecimalField(max_digits=20, decimal_places=7, default=0.0)
    latitude = models.DecimalField(max_digits=20, decimal_places=7, default=0.0)

    def __str__(self):
        return self.name


from django.db import models
from adminapp.models import tbl_category
from userapp.models import tbl_register  
from decimal import Decimal
import uuid

# Waste Submission Model
class WasteSubmission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'), 
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('incompleted', 'Incompleted'),
    ]

    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    categories = models.TextField()  # Store category IDs as a comma-separated string
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    kilo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Added kilo field
    description = models.TextField(null=True, blank=True)  # Added description field

    def __str__(self):
        return f"{self.user.name} - {self.date} ({self.get_status_display()})"

from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from decimal import Decimal
import uuid
from userapp.models import tbl_register, WasteSubmission  # Adjust import as per your app structure

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
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    cash_status = models.CharField(max_length=10, choices=CASH_STATUS_CHOICES, default='pending', null=True, blank=True)

    # Card Payment Details
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    name_of_card = models.CharField(max_length=255, null=True, blank=True)
    
    card_number = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        validators=[
            MinLengthValidator(16, message="Card number must be exactly 16 digits."),
            RegexValidator(r'^\d{16}$', message="Card number must contain only digits.")
        ]
    )

    expiry_date = models.CharField(max_length=5, null=True, blank=True)  # Format: MM/YY
    
    cvv = models.CharField(
        max_length=3,
        null=True,
        blank=True,
        validators=[
            MinLengthValidator(3, message="CVV must be exactly 3 digits."),
            RegexValidator(r'^\d{3}$', message="CVV must contain only digits.")
        ]
    )

    def save(self, *args, **kwargs):
        if self.payment_option == 'cash':
            if not self.pk:  # Only reset total_price to 0.00 if this is a new cash payment
                self.total_price = Decimal('0.00')
            
            self.status = 'cash'
            self.cash_status = 'pending' if self.cash_status is None else self.cash_status

            # Remove card payment details if cash is selected
            self.transaction_id = None
            self.name_of_card = None
            self.card_number = None
            self.expiry_date = None
            self.cvv = None

        elif self.payment_option == 'card_payment':
            self.status = 'card_payment'
            self.cash_status = None  # Cash status not applicable for card payments
            
            # Set total price from waste submission if available
            if self.waste_submission and self.waste_submission.total_price:
                self.total_price = self.waste_submission.total_price  

            # Generate a transaction ID if it's empty
            if not self.transaction_id:
                self.transaction_id = str(uuid.uuid4())

            # Mark the waste submission as completed if payment is successful
            if self.waste_submission:
                self.waste_submission.status = 'pending'
                self.waste_submission.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.name} - {self.payment_option} - {self.status} - Cash Status: {self.cash_status or 'N/A'}"

from django.db import models

class Feedback(models.Model):
    user = models.ForeignKey('tbl_register', on_delete=models.CASCADE)  # Linking feedback to a user
    rate = models.PositiveIntegerField()  # Rating (out of 5)
    feedback = models.TextField()  # User's feedback text
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for feedback submission

    def __str__(self):
        return f"Feedback from {self.user.name} - {self.rate}/5"
