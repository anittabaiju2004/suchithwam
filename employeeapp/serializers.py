# serializers.py
from rest_framework import serializers

class EmployeeLoginSerializer(serializers.Serializer):
    employee_id = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)


# serializers.py
from rest_framework import serializers
from adminapp.models import Employee, Ward
from rest_framework import serializers
# from .models import Employee, Ward
class EmployeeSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['employee_id', 'name', 'email', 'phone', 'password', 'image']
        extra_kwargs = {
            'employee_id': {'required': False},
            'name': {'required': False},
            'email': {'required': False},
            'phone': {'required': False},
            'password': {'required': False},
            'image': {'required': False},
        }

    def get_image(self, obj):
        if obj.image:
            return f"media/{obj.image.name}"
        return None





# serializers.py

from rest_framework import serializers
from userapp.models import WasteSubmission
class WasteSubmissionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteSubmission
        fields = ['status', 'kilo', 'description']  # ✅ Added description field

from rest_framework import serializers
from userapp.models import WasteSubmission
from rest_framework import serializers
from adminapp.models import tbl_category
from userapp.models import WasteSubmission

class WasteSubmissionListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_address = serializers.CharField(source='user.address', read_only=True)
    user_phone = serializers.CharField(source='user.phone', read_only=True)
    ward = serializers.CharField(source='user.ward.name', read_only=True)  
    location = serializers.CharField(source='user.location', read_only=True)
    category_names = serializers.SerializerMethodField()  # ✅ Fetch category names
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    description = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = WasteSubmission
        fields = ['id', 'user_name', 'user_address', 'user_phone', 'ward', 'location', 'date', 'time', 'total_price', 'category_names', 'description']

    def get_category_names(self, obj):
        if obj.categories:
            category_names = [name.strip() for name in obj.categories.split(",")]
            categories = tbl_category.objects.filter(name__in=category_names).values_list("name", flat=True)
            return list(categories)
        return []



class EmployeeWasteSubmissionStatusSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    ward = serializers.CharField(source='user.ward.name', read_only=True)
    ward_no = serializers.CharField(source='user.ward.ward_no', read_only=True)
    user_address = serializers.CharField(source='user.address', read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    category_names = serializers.SerializerMethodField()  # ✅ Fetch category names

    class Meta:
        model = WasteSubmission
        fields = ['id', 'user_name', 'ward', 'user_address', 'ward_no', 'date', 'time', 'status', 'description', 'category_names', 'total_price']

    def get_category_names(self, obj):
        if obj.categories:
            category_names = [name.strip() for name in obj.categories.split(",")]
            categories = tbl_category.objects.filter(name__in=category_names).values_list("name", flat=True)
            return list(categories)
        return []


