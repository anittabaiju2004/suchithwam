from django.db import models

class tbl_admin(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    pswd = models.CharField(max_length=100)

    def __str__(self):
        return self.email


from decimal import Decimal

class tbl_category(models.Model):
    name = models.TextField()
    image = models.ImageField(upload_to="category_products/")

    def __str__(self):
        return self.name


class Ward(models.Model):
    ward_number = models.IntegerField(unique=True)
    location = models.CharField(max_length=255)  # Stores "from-to" in one field

    def __str__(self):
        return f"Ward {self.ward_number}: {self.location}"


        
class Employee(models.Model):
    employee_id = models.CharField(max_length=20, unique=True)  # Unique Employee ID
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=255)  # Store hashed password in production
    image = models.ImageField(upload_to="employee_images/", null=True, blank=True)  # Optional image
    ward = models.ManyToManyField(Ward, related_name="employees")  # Changed to ManyToManyField

    def __str__(self):
        return f"{self.employee_id} - {self.name}"
