from rest_framework import serializers
from .models import tbl_register
from rest_framework import serializers
from .models import tbl_register
class userregisterSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = tbl_register
        fields = '__all__'

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return f"media/{obj.profile_picture.name}"
        return None


from rest_framework import serializers
from adminapp.models import tbl_category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = tbl_category
        fields = ['id', 'name', 'image']

from rest_framework import serializers
from adminapp.models import Ward

class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = '__all__'  # Includes all fields (ward_number, location)

from rest_framework import serializers
from userapp.models import WasteSubmission, tbl_register
from adminapp.models import tbl_category

from rest_framework import serializers
from .models import WasteSubmission
from decimal import Decimal

from rest_framework import serializers
from .models import WasteSubmission

class WasteSubmissionSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%d-%m-%Y", input_formats=["%d-%m-%Y"])
    time = serializers.TimeField(format="%H:%M:%S", input_formats=["%H:%M:%S"])
    
    class Meta:
        model = WasteSubmission
        fields = '__all__'

    def create(self, validated_data):
        validated_data['total_price'] = Decimal('50.00')  # Ensure total_price is always 50
        return WasteSubmission.objects.create(**validated_data)


from rest_framework import serializers
import uuid 
from .models import Payment
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

    def validate(self, data):
        payment_option = data.get('payment_option')

        if payment_option == 'card_payment':
            required_fields = ['card_number', 'expiry_date', 'cvv', 'name_of_card']
            for field in required_fields:
                if not data.get(field):
                    raise serializers.ValidationError({field: f"{field} is required for card payment."})

            if not data.get('transaction_id'):
                data['transaction_id'] = str(uuid.uuid4())

        return data

    def create(self, validated_data):
        # Set the default status as "pending"
        validated_data['status'] = 'pending'
        return Payment.objects.create(**validated_data)

from rest_framework import generics, serializers
from django.urls import path
from .models import WasteSubmission, Payment
from .serializers import WasteSubmissionSerializer

class UserBookingsSerializer(serializers.ModelSerializer):
    waste = serializers.SerializerMethodField()
    payment_status = serializers.SerializerMethodField()

    class Meta:
        model = WasteSubmission
        fields = ['id', 'date', 'time', 'waste', 'status', 'user_id', 'payment_status','total_price']

    def get_waste(self, obj):
        return obj.categories.split(',') if obj.categories else []
    
    
    def get_payment_status(self, obj):
        payment = Payment.objects.filter(waste_submission=obj).first()
        return payment.status if payment else 'Not Paid'