# serializers.py
from rest_framework import serializers

class EmployeeLoginSerializer(serializers.Serializer):
    employee_id = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)
