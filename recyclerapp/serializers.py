from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from adminapp.models import Recycler

class RecyclerLoginSerializer(serializers.Serializer):
    recycler_id = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        recycler_id = data.get("recycler_id")
        password = data.get("password")

        try:
            recycler = Recycler.objects.get(recycler_id=recycler_id)
        except Recycler.DoesNotExist:
            raise serializers.ValidationError("Invalid Recycler ID or Password.")

        if not check_password(password, recycler.password):  # Ensure password is hashed in DB
            raise serializers.ValidationError("Invalid Recycler ID or Password.")

        data["recycler"] = recycler
        return data



from rest_framework import serializers
from adminapp.models import WasteThreshold

class WasteThresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteThreshold
        fields = ['limit', 'updated_at']
from rest_framework import serializers
from adminapp.models import WasteThreshold
from userapp.models import WasteSubmission  # For resetting kilo values
from decimal import Decimal

class RecyclerQuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteThreshold
        fields = ['quotation', 'status']

    def update(self, instance, validated_data):
        if validated_data.get('status') == 'collected':
            # Reset kilo value for all submissions instead of deleting them
            WasteSubmission.objects.update(kilo=Decimal('0.00'))

        return super().update(instance, validated_data)
