from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login
from .serializers import RecyclerLoginSerializer
from adminapp.models import Recycler
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from adminapp.models import Recycler
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RecyclerLoginView(APIView):
    """
    API endpoint for recycler login without password hashing.
    """

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "recycler_id": openapi.Schema(type=openapi.TYPE_STRING, description="Recycler ID"),
                "password": openapi.Schema(type=openapi.TYPE_STRING, description="Password")
            },
            required=["recycler_id", "password"]
        ),
        responses={
            200: openapi.Response("Login Successful", examples={"application/json": {"message": "Login successful", "recycler_id": "REC123", "name": "John Doe"}}),
            400: openapi.Response("Invalid Credentials", examples={"application/json": {"error": "Invalid Recycler ID or Password"}})
        },
    )
    def post(self, request):
        recycler_id = request.data.get("recycler_id")
        password = request.data.get("password")

        if not recycler_id or not password:
            return Response({"error": "Recycler ID and Password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if recycler exists
        try:
            recycler = Recycler.objects.get(recycler_id=recycler_id)

            # Check if password matches (plain text)
            if recycler.password == password:
                return Response({
                    "message": "Login successful",
                    "recycler_id": recycler.recycler_id,
                    "password":recycler.password,
                    "name": recycler.name
                }, status=status.HTTP_200_OK)

            return Response({"error": "Invalid Recycler ID or Password."}, status=status.HTTP_400_BAD_REQUEST)

        except Recycler.DoesNotExist:
            return Response({"error": "Invalid Recycler ID or Password."}, status=status.HTTP_400_BAD_REQUEST)


from django.db import models  
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny  # Both admin & recycler can access
from adminapp.models import WasteThreshold
from .serializers import WasteThresholdSerializer

class WasteThresholdView(APIView):
    permission_classes = [AllowAny]  # Both Admin & Recycler can access

    def get(self, request):
        threshold = WasteThreshold.objects.first()  # Assuming only one threshold exists

        if not threshold:
            return Response({"message": "Threshold not set"}, status=404)

        # Fetch the current waste amount (Assuming you store it somewhere)
        current_waste = self.get_current_waste()  # Implement this function as needed

        # Check if waste exceeds the limit
        if current_waste > threshold.limit:
            warning_message = f"⚠ Warning! Waste exceeds limit ({current_waste:.2f} kg). Max: {threshold.limit} kg."
            return Response({"limit": threshold.limit, "current_waste": current_waste, "warning": warning_message})

        return Response({"limit": threshold.limit, "current_waste": current_waste, "warning": None})

    def get_current_waste(self):
        # Implement logic to get the current waste amount
        # Example: Fetch from a model that tracks waste
        from userapp.models import WasteSubmission  # Assuming you have this model
        return WasteSubmission.objects.aggregate(models.Sum("kilo"))["kilo__sum"] or 0

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from adminapp.models import WasteThreshold
from .serializers import RecyclerQuotationSerializer

class RecyclerQuotationView(generics.RetrieveUpdateAPIView):
    queryset = WasteThreshold.objects.all()
    serializer_class = RecyclerQuotationSerializer

    def get_object(self):
        return WasteThreshold.objects.get(id=1)  # Ensuring a single threshold record

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Quotation and status updated successfully!"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)