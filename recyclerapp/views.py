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
                    "name": recycler.name
                }, status=status.HTTP_200_OK)

            return Response({"error": "Invalid Recycler ID or Password."}, status=status.HTTP_400_BAD_REQUEST)

        except Recycler.DoesNotExist:
            return Response({"error": "Invalid Recycler ID or Password."}, status=status.HTTP_400_BAD_REQUEST)
