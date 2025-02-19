from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import tbl_register
from .serializers import userregisterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
# from your_app.models import tbl_register
# from your_app.serializers import userregisterSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import tbl_register
from .serializers import userregisterSerializer

class user_registerViewSet(ModelViewSet):
    queryset = tbl_register.objects.all()
    serializer_class = userregisterSerializer
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
                    "location": user.location
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
                    {"message": "Login successful", "user": user.name,"role":"user"},
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

# class WasteSubmissionViewSet(viewsets.ModelViewSet):
#     queryset = WasteSubmission.objects.all()
#     serializer_class = WasteSubmissionSerializer
#     http_method_names = ['get', 'post']

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
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

# from rest_framework import generics
# from .models import WasteSubmission
# from .serializers import WasteSubmissionSerializer
# from userapp.models import tbl_register

# class UserWasteSubmissionListView(generics.ListAPIView):
#     serializer_class = WasteSubmissionSerializer

#     def get_queryset(self):
#         user_id = self.kwargs.get('user_id')  # Get user_id from URL
#         if user_id and tbl_register.objects.filter(id=user_id).exists():
#             return WasteSubmission.objects.filter(user_id=user_id)
#         return WasteSubmission.objects.none()  # Return empty if user_id is invalid



from rest_framework import generics
from .models import tbl_register
from .serializers import userregisterSerializer

class UserProfileView(generics.RetrieveAPIView):
    queryset = tbl_register.objects.all()
    serializer_class = userregisterSerializer
    lookup_field = 'id'  # This will allow us to fetch users by ID



from rest_framework import generics
from .models import tbl_register
from .serializers import userregisterSerializer

class UserProfileUpdateView(generics.UpdateAPIView):
    queryset = tbl_register.objects.all()
    serializer_class = userregisterSerializer
    lookup_field = 'id'  # Fetch user by ID


from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from userapp.models import Payment
from userapp.serializers import PaymentSerializer


# class MakePaymentView(APIView):
#     def post(self, request):
#         serializer = PaymentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Payment successful", "data": serializer.data}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from userapp.models import WasteSubmission, Payment
class WasteOverviewView(APIView):
    def get(self, request, user_id):
        # Get all waste submissions for the given user
        waste_submissions = WasteSubmission.objects.filter(user_id=user_id)
        data = []

        # Loop through each waste submission and prepare the response data
        for waste_submission in waste_submissions:
            # Check if there's a payment for the waste submission and get the status
            payment = Payment.objects.filter(waste_submission=waste_submission).first()
            payment_status = payment.status if payment else "Not Paid"

            data.append({
                "waste_id": waste_submission.id,
                "date": waste_submission.date,
                "time": waste_submission.time,
                "status": waste_submission.get_status_display(),
                "payment_status": payment_status
            })

        return Response(data, status=status.HTTP_200_OK)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from userapp.models import WasteSubmission, Payment
from userapp.serializers import WasteSubmissionSerializer, PaymentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from userapp.models import WasteSubmission, Payment
from userapp.serializers import WasteSubmissionSerializer, PaymentSerializer
class WastePaymentDetailView(APIView):
    def get(self, request, user_id):
        # Get all waste submissions for the given user
        waste_submissions = WasteSubmission.objects.filter(user_id=user_id)
        data = []

        # Loop through each waste submission and prepare the response data
        for waste_submission in waste_submissions:
            # Serialize the waste submission data
            waste_data = WasteSubmissionSerializer(waste_submission).data
            # Check if there's a payment for the waste submission
            payment = Payment.objects.filter(waste_submission=waste_submission).first()
            # Serialize the payment data if it exists, else set it to None
            payment_data = PaymentSerializer(payment).data if payment else None
            
            data.append({
                "waste_submission": waste_data,
                "payment_details": payment_data
            })

        return Response(data, status=status.HTTP_200_OK)


# class WasteSubmissionViewSet(viewsets.ModelViewSet):
#     queryset = WasteSubmission.objects.all()
#     serializer_class = WasteSubmissionSerializer
#     http_method_names = ['get', 'post']

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class MakePaymentView(APIView):
#     def post(self, request):
#         serializer = PaymentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Payment successful", "data": serializer.data}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework import viewsets, status
from rest_framework.response import Response
from userapp.models import WasteSubmission
from userapp.serializers import WasteSubmissionSerializer
# from decimal import Decimal

# class WasteSubmissionViewSet(viewsets.ModelViewSet):
#     queryset = WasteSubmission.objects.all()
#     serializer_class = WasteSubmissionSerializer
#     http_method_names = ['post']

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             waste_submission = serializer.save()
#             waste_submission.refresh_from_db()
#             return Response(WasteSubmissionSerializer(waste_submission).data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class WasteSubmissionViewSet(viewsets.ModelViewSet):
    queryset = WasteSubmission.objects.all()
    serializer_class = WasteSubmissionSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # The total_price can be passed as null from the frontend
            waste_submission = serializer.save()
            waste_submission.refresh_from_db()
            return Response(WasteSubmissionSerializer(waste_submission).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from userapp.models import WasteSubmission

class WasteSubmissionEditView(APIView):
    """View to reschedule the date or time of a waste submission."""

    def get(self, request, waste_id):
        """Get the waste submission details with date in dd-mm-yyyy format."""
        try:
            waste_submission = WasteSubmission.objects.get(id=waste_id)
        except WasteSubmission.DoesNotExist:
            return Response({"error": "Waste submission not found."}, status=status.HTTP_404_NOT_FOUND)

        # Format the date to dd-mm-yyyy for the response
        waste_submission_data = {
            "waste_id": waste_submission.id,
            "date": waste_submission.date.strftime("%d-%m-%Y"),
            "time": waste_submission.time.strftime("%H:%M:%S") if waste_submission.time else None,
            "status": waste_submission.get_status_display(),
        }

        return Response(waste_submission_data, status=status.HTTP_200_OK)

    def put(self, request, waste_id):
        """Update the date, time, or both of a waste submission."""
        try:
            waste_submission = WasteSubmission.objects.get(id=waste_id)
        except WasteSubmission.DoesNotExist:
            return Response({"error": "Waste submission not found."}, status=status.HTTP_404_NOT_FOUND)

        date = request.data.get("date")
        time = request.data.get("time")

        if not date and not time:
            return Response({"error": "Provide at least a date or time to update."}, status=status.HTTP_400_BAD_REQUEST)

        # Parse the date if it exists
        if date:
            try:
                # Try to parse the date in dd-mm-yyyy format
                parsed_date = datetime.strptime(date, "%d-%m-%Y").date()
                waste_submission.date = parsed_date
            except ValueError:
                return Response({"error": "Invalid date format. Use dd-mm-yyyy."}, status=status.HTTP_400_BAD_REQUEST)

        if time:
            waste_submission.time = time

        waste_submission.save()
        return Response({"message": "Waste submission updated successfully!"}, status=status.HTTP_200_OK)



class WasteSubmissionDeleteView(APIView):
    """View to delete a waste submission."""

    def delete(self, request, waste_id):
        """Delete a waste submission by ID."""
        try:
            waste_submission = WasteSubmission.objects.get(id=waste_id)
        except WasteSubmission.DoesNotExist:
            return Response({"error": "Waste submission not found."}, status=status.HTTP_404_NOT_FOUND)

        waste_submission.delete()
        return Response({"message": "Waste submission deleted successfully!"}, status=status.HTTP_200_OK)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PaymentSerializer

class MakePaymentView(APIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"message": "Payment successful", "data": serializer.data}, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
