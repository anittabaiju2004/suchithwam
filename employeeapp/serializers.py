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
class WasteSubmissionListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_address = serializers.CharField(source='user.address', read_only=True)
    user_phone = serializers.CharField(source='user.phone', read_only=True)
    ward = serializers.CharField(source='user.ward', read_only=True)  # Assuming ward is related to the user
    location = serializers.CharField(source='user.location', read_only=True)  # Assuming location is related to the user
    category_name = serializers.CharField(source='details.category.name', read_only=True)

    class Meta:
        model = WasteSubmission
        fields = ['id', 'user_name', 'user_address', 'user_phone', 'ward', 'location', 'date', 'time', 'total_price', 'category_name', 'description']  # ✅ Added description field
