from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import tbl_register
# from userapp.serializers import userregisterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import tbl_register
# from .serializers import userregisterSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from .models import tbl_register
from userapp.serializers import UserRegisterSerializer
class user_registerViewSet(ModelViewSet):
    queryset = tbl_register.objects.all()
    serializer_class = UserRegisterSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():       
            user = serializer.save()
            return Response(
                {
                    "message": "Registration successful",
                    "role": "user",
                    "name": user.name,
                    "email": user.email,
                    "place": user.place,
                    "address": user.address,
                    "phone": user.phone,
                    "ward": user.ward.id if user.ward else None,
                    "profile_picture": f"/media/{user.profile_picture.name}" if user.profile_picture else None,  # Ensures '/media/' prefix
                    "longitude": user.longitude,  # Include longitude
                    "latitude": user.latitude,  # Include latitude
                },
                status=status.HTTP_201_CREATED
            )

        # Extract error messages
        error_messages = {field: errors[0] for field, errors in serializer.errors.items()}

        return Response(
            {"message": "Registration failed", "errors": error_messages},
            status=status.HTTP_400_BAD_REQUEST
        )



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import tbl_register

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import tbl_register

class LoginView(APIView):
    def post(self, request):
        # Retrieve email, phone, and password from the request data
        email = request.data.get('email')
        phone = request.data.get('phone')
        pswd = request.data.get('pswd')
        print(request.data)
        # Ensure either email or phone is provided, along with the password
        if not (email or phone) or not pswd:
            return Response(
                {"error": "Email or phone and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Fetch user by email or phone
            if email:  # Login with email
                user = tbl_register.objects.get(email=email)
            elif phone:  # Login with phone
                user = tbl_register.objects.get(phone=phone)

            # Check if the password matches
            if user.pswd == pswd:  # Direct comparison; use hashing in production
                return Response(
                    {"message": "Login successful", "user": user.name,"role":"user","userid":user.id},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Invalid email/phone or password."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except tbl_register.DoesNotExist:
            # Return the same error if the user doesn't exist
            return Response(
                {"error": "Invalid email/phone or password."},
                status=status.HTTP_400_BAD_REQUEST,
            )



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from adminapp.models import tbl_category
from .serializers import CategorySerializer

class CategoryListView(APIView):
    def get(self, request, format=None):
        categories = tbl_category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import WasteSubmission
from .serializers import WasteSubmissionSerializer
from userapp.models import tbl_register


from rest_framework import generics
from adminapp.models import Ward
from userapp.serializers import WardSerializer

class WardListView(generics.ListAPIView):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer

def delete_ward(request, user_id):
    user = get_object_or_404(tbl_register, id=user_id)
    user.delete()

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from userapp.models import tbl_register

@csrf_exempt
def delete_user(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(tbl_register, id=user_id)
        user.delete()
        return JsonResponse({'message': 'User deleted successfully!', 'status': 'success'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser  # Enables form upload in Swagger
from .models import tbl_register
from .serializers import UserRegisterSerializer
from rest_framework import generics, viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import tbl_register
# from .serializers import userregisterSeUserRegisterSerializerrializer
from rest_framework import generics, viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import tbl_register
from userapp.serializers import UserRegisterSerializer,UserProfileUpdateSerializer
class UserProfileView(generics.RetrieveAPIView):
    """
    API to retrieve user profile by ID (without ViewSet)
    """
    queryset = tbl_register.objects.all()
    serializer_class = UserRegisterSerializer
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if isinstance(response.data, dict):
            response.data.pop("pswd", None)  # Remove password field safely
        return response
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import tbl_register
from .serializers import UserProfileUpdateSerializer

class UserProfileUpdateViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):  
        """Retrieve user profile details"""
        try:
            user = tbl_register.objects.get(id=pk)
            serializer = UserProfileUpdateSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except tbl_register.DoesNotExist:
            return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):  
        """Update user profile details and profile picture"""
        try:
            user = tbl_register.objects.get(id=pk)
            data = request.data.copy()

            # Update text fields
            user.name = data.get('name', user.name)
            user.email = data.get('email', user.email)

            # Update profile picture if provided
            if 'profile_picture' in request.FILES:
                image = request.FILES['profile_picture']

                # Delete old profile picture if it exists
                if hasattr(user, 'profile_picture') and user.profile_picture:
                    default_storage.delete(user.profile_picture.name)

                # Save new profile picture
                image_path = default_storage.save(f"profile_pictures/{image.name}", ContentFile(image.read()))
                user.profile_picture = image_path  # Save the new image path

            user.save()
            serializer = UserProfileUpdateSerializer(user)
            return Response({'status': 'success', 'message': 'Profile updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)

        except tbl_register.DoesNotExist:
            return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from userapp.models import Payment
from userapp.serializers import PaymentSerializer




from rest_framework import viewsets, status
from rest_framework.response import Response
from userapp.models import WasteSubmission
from userapp.serializers import WasteSubmissionSerializer
from rest_framework.response import Response
from .models import WasteSubmission
from .serializers import WasteSubmissionSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import WasteSubmission
from .serializers import WasteSubmissionSerializer

class WasteSubmissionViewSet(viewsets.ModelViewSet):
    queryset = WasteSubmission.objects.all()
    serializer_class = WasteSubmissionSerializer
    http_method_names = ['post', 'get']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            waste_submission = serializer.save()
            waste_submission.refresh_from_db()
            return Response(WasteSubmissionSerializer(waste_submission).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .models import WasteSubmission
from .serializers import WasteSubmissionSerializer

from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from rest_framework.views import APIView
from .models import WasteSubmission
from .serializers import WasteSubmissionSerializer

class RescheduleWasteSubmissionView(APIView):
    """API to reschedule the date and/or time of an existing WasteSubmission"""
    http_method_names = ['put']  # Allows only PUT requests

    def put(self, request, submission_id):
        try:
            waste_submission = WasteSubmission.objects.get(id=submission_id)
        except WasteSubmission.DoesNotExist:
            return Response({'error': 'Waste submission not found.'}, status=status.HTTP_404_NOT_FOUND)

        new_date = request.data.get('date')
        new_time = request.data.get('time')

        if not new_date and not new_time:
            return Response({'error': 'Provide at least one field (date or time) for rescheduling.'}, status=status.HTTP_400_BAD_REQUEST)

        if new_date:
            try:
                waste_submission.date = datetime.strptime(new_date, "%d-%m-%Y").date()
            except ValueError:
                return Response({'error': 'Invalid date format. Use DD-MM-YYYY.'}, status=status.HTTP_400_BAD_REQUEST)

        if new_time:
            try:
                waste_submission.time = datetime.strptime(new_time, "%H:%M:%S").time()
            except ValueError:
                return Response({'error': 'Invalid time format. Use HH:MM:SS.'}, status=status.HTTP_400_BAD_REQUEST)

        waste_submission.save()

        # Serialize and filter response
        waste_submission_data = WasteSubmissionSerializer(waste_submission).data

        # Keep only required fields
        filtered_data = {
            "id": waste_submission_data["id"],
            "date": waste_submission_data["date"],
            "time": waste_submission_data["time"],
            "status": waste_submission_data["status"],
            "categories": waste_submission_data["categories"],
            "total_price": waste_submission_data["total_price"],
            "user": waste_submission_data["user"]
        }

        return Response(filtered_data, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PaymentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from .serializers import PaymentSerializer

class MakePaymentView(APIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                payment = serializer.save()
                return Response({
                    "message": "Payment successful",
                    "waste_submission": payment.waste_submission.id if payment.waste_submission else None,  # Ensure waste_submission is included
                    "data": PaymentSerializer(payment).data
                }, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import generics, serializers
from .models import WasteSubmission, Payment
from .serializers import WasteSubmissionSerializer,UserBookingsSerializer

class UserBookingsView(generics.ListAPIView):
    serializer_class = UserBookingsSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return WasteSubmission.objects.filter(user_id=user_id) if user_id else WasteSubmission.objects.none()



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Payment, WasteSubmission
from .serializers import PaymentSerializer

class UpdatePaymentView(APIView):
    def post(self, request, waste_submission_id):
        # Get the waste submission and payment objects
        waste_submission = get_object_or_404(WasteSubmission, id=waste_submission_id)
        payment = get_object_or_404(Payment, waste_submission=waste_submission)

        # Deserialize request data
        serializer = PaymentSerializer(payment, data=request.data, partial=True)

        if serializer.is_valid():
            # If payment is card payment, remove the description
            if request.data.get("payment_option") == "card_payment":
                waste_submission.status = "completed"
                waste_submission.description = None  # Remove description
                waste_submission.save()

            # Save payment
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from .serializers import PaymentSerializer
class UserPaymentHistoryView(generics.ListAPIView):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')  # Ensure this matches the URL parameter
        return Payment.objects.filter(user_id=user_id).order_by('id')  # Use 'user_id' correctly


from rest_framework import viewsets
from .models import Feedback
from .serializers import FeedbackSerializer

class FeedbackViewSet(viewsets.ModelViewSet):
    """ViewSet for managing feedback"""
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
