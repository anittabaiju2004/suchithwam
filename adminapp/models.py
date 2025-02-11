from django.db import models

class tbl_admin(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    pswd = models.CharField(max_length=100)

    def __str__(self):
        return self.email



from django.db import models

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
