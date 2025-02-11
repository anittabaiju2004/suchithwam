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
        fields = ['id', 'name', 'image']


from rest_framework import serializers

from userapp.models import WasteSubmission,WasteSubmissionDetail  # Add this line

class WasteSubmissionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteSubmissionDetail
        fields = ['category', 'kilogram']

class WasteSubmissionSerializer(serializers.ModelSerializer):
    details = WasteSubmissionDetailSerializer(many=True)
    user = serializers.PrimaryKeyRelatedField(queryset=tbl_register.objects.all())
    class Meta:
        model = WasteSubmission
        fields = "__all__"

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        waste_submission = WasteSubmission.objects.create(**validated_data)
        for detail in details_data:
            WasteSubmissionDetail.objects.create(waste_submission=waste_submission, **detail)
        return waste_submission



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
