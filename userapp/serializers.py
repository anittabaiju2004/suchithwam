from rest_framework import serializers
from .models import tbl_register

class userregisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = tbl_register
        fields = '__all__'
from rest_framework import serializers
from adminapp.models import tbl_category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = tbl_category
        fields = ['id', 'name', 'image','price']

from datetime import datetime

from rest_framework import serializers
from userapp.models import WasteSubmissionDetail,WasteSubmission

class WasteSubmissionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteSubmissionDetail
        fields = ['category', 'kilogram']

# class WasteSubmissionSerializer(serializers.ModelSerializer):
#     details = WasteSubmissionDetailSerializer(many=True)
#     user = serializers.PrimaryKeyRelatedField(queryset=tbl_register.objects.all())

#     # Customizing the time format for display
#     time = serializers.TimeField(format="%H:%M:%S")

#     class Meta:
#         model = WasteSubmission
#         fields = "__all__"

#     def to_internal_value(self, data):
#         """
#         Override the default method to parse the date in DD-MM-YYYY format and time in hh:mm[:ss[.uuuuuu]] format.
#         """
#         if 'date' in data:
#             try:
#                 date = datetime.strptime(data['date'], "%d-%m-%Y").date()
#                 data['date'] = date
#             except ValueError:
#                 raise serializers.ValidationError({"date": "Date has wrong format. Use DD-MM-YYYY."})

#         if 'time' in data:
#             try:
#                 # Parsing time in hh:mm[:ss[.uuuuuu]] format
#                 # The optional seconds and microseconds will be handled correctly
#                 time = datetime.strptime(data['time'], "%H:%M:%S.%f" if '.' in data['time'] else "%H:%M:%S").time()
#                 data['time'] = time
#             except ValueError:
#                 raise serializers.ValidationError({"time": "Time has wrong format. Use hh:mm[:ss[.uuuuuu]]."})

#         return super().to_internal_value(data)

#     def to_representation(self, instance):
#         """
#         Override the default method to customize the date and time format in the response.
#         """
#         representation = super().to_representation(instance)

#         # Format the date as DD-MM-YYYY
#         if 'date' in representation:
#             representation['date'] = instance.date.strftime("%d-%m-%Y")

#         # Format the time as hh:mm:ss[.uuuuuu]
#         if 'time' in representation:
#             time_str = instance.time.strftime("%H:%M:%S")
#             # If microseconds exist, append them
#             if instance.time.microsecond > 0:
#                 time_str += f".{instance.time.microsecond:06d}"
#             representation['time'] = time_str

#         return representation

#     def create(self, validated_data):
#         details_data = validated_data.pop('details')
#         waste_submission = WasteSubmission.objects.create(**validated_data)
#         for detail in details_data:
#             WasteSubmissionDetail.objects.create(waste_submission=waste_submission, **detail)
#         return waste_submission

from datetime import datetime
from rest_framework import serializers
from userapp.models import WasteSubmission, WasteSubmissionDetail, tbl_register

class WasteSubmissionSerializer(serializers.ModelSerializer):
    details = WasteSubmissionDetailSerializer(many=True)
    user = serializers.PrimaryKeyRelatedField(queryset=tbl_register.objects.all())
    total_price = serializers.SerializerMethodField()  # Corrected to use a method field

    # Customizing the time format for display
    time = serializers.TimeField(format="%H:%M:%S")

    class Meta:
        model = WasteSubmission
        fields = "__all__"

    def get_total_price(self, obj):
        """Calculate and return the total price dynamically."""
        return obj.total_price()

    def to_internal_value(self, data):
        """
        Override the default method to parse the date in DD-MM-YYYY format 
        and time in hh:mm[:ss[.uuuuuu]] format.
        """
        if 'date' in data:
            try:
                date = datetime.strptime(data['date'], "%d-%m-%Y").date()
                data['date'] = date
            except ValueError:
                raise serializers.ValidationError({"date": "Date has wrong format. Use DD-MM-YYYY."})

        if 'time' in data:
            try:
                # Parsing time in hh:mm[:ss[.uuuuuu]] format
                time = datetime.strptime(data['time'], "%H:%M:%S.%f" if '.' in data['time'] else "%H:%M:%S").time()
                data['time'] = time
            except ValueError:
                raise serializers.ValidationError({"time": "Time has wrong format. Use hh:mm[:ss[.uuuuuu]]."})

        return super().to_internal_value(data)

from rest_framework import serializers
from adminapp.models import Ward

class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = '__all__'  # Includes all fields (ward_number, location)



from rest_framework import serializers
from userapp.models import Payment
from rest_framework import serializers
from userapp.models import Payment
import uuid


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

    def validate(self, data):
        payment_option = data.get('payment_option')

        if payment_option == 'card_payment':
            if not data.get('transaction_id'):
                data['transaction_id'] = str(uuid.uuid4())  # Auto-generate if missing
            
            required_fields = ['card_number', 'expiry_date', 'cvv', 'cardholder_name']
            for field in required_fields:
                if not data.get(field):
                    raise serializers.ValidationError({field: f"{field} is required for card payment."})

        return data
