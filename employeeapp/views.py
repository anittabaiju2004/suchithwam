# views.py
from rest_framework import status, generics
from rest_framework.response import Response
from employeeapp.serializers import EmployeeLoginSerializer
from adminapp.models import Employee

class EmployeeLoginView(generics.GenericAPIView):
    serializer_class = EmployeeLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            employee_id = serializer.validated_data['employee_id']
            password = serializer.validated_data['password']

            try:
                employee = Employee.objects.get(employee_id=employee_id)
                # Check if password matches (Assuming password is stored as plain text)
                if employee.password == password:
                    return Response({'detail': 'Login successful','role':'Employee','id':employee_id}, status=status.HTTP_200_OK)
                else:
                    return Response({'detail': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
            except Employee.DoesNotExist:
                return Response({'detail': 'Employee not found'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# views.py
from rest_framework import generics
from adminapp.models import Employee
from .serializers import EmployeeSerializer
class EmployeeProfileView(generics.RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_object(self):
        return Employee.objects.get(employee_id=self.kwargs['employee_id'])  # Get employee by employee_id


class EmployeeProfileUpdateView(generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_object(self):
        return Employee.objects.get(id=self.kwargs['employee_id'])  # Get the employee by ID




        
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from userapp.models import WasteSubmission
from adminapp.models import Employee
from userapp.models import Payment  # Assuming Payment model is in payments app
from employeeapp.serializers import WasteSubmissionListSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from userapp.models import WasteSubmission
from adminapp.models import Employee
from userapp.models import Payment
from employeeapp.serializers import WasteSubmissionListSerializer

class EmployeeWasteSubmissionView(APIView):
    def get(self, request, employee_id):
        try:
            employee = Employee.objects.get(employee_id=employee_id)
            waste_submissions = WasteSubmission.objects.filter(user__ward__in=employee.ward.all())

            if not waste_submissions.exists():
                return Response({"message": "No waste submissions found"}, status=status.HTTP_200_OK)

            response_data = []
            for submission in waste_submissions:
                print(f"Waste Submission ID: {submission.id}")  # ✅ Debugging: Print waste submission ID
                
                payment = Payment.objects.filter(waste_submission=submission).first()
                payment_status = payment.status if payment else None
                cash_status = payment.cash_status if payment else None
                total_price = payment.total_price if payment_status == 'card_payment' else None

                response_data.append({
                    "id": submission.id,
                    "name": submission.user.name,
                    "address": submission.user.address,
                    "ward_number": submission.user.ward.ward_number if submission.user.ward else None,
                    "ward": submission.user.ward.location if submission.user.ward else None,
                    "phone": submission.user.phone,
                    "location": f"{submission.user.latitude}, {submission.user.longitude}",
                    "date": submission.date,
                    "time": submission.time,
                    "categories": submission.categories,
                    "kilo": submission.kilo,
                    "total_price": total_price,
                    "payment_status": payment_status,
                    "cash_status": cash_status,
                    "employee_id": employee_id
                })

            return Response(response_data, status=status.HTTP_200_OK)

        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from userapp.models import WasteSubmission
from userapp.models import Payment
from employeeapp.serializers import WasteSubmissionUpdateSerializer
from decimal import Decimal

from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from decimal import Decimal
from userapp.models import WasteSubmission, Payment
from decimal import Decimal
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from userapp.models import WasteSubmission, Payment
class WasteSubmissionUpdateView(APIView):
    def put(self, request, submission_id):
        # Get the waste submission object
        waste_submission = get_object_or_404(WasteSubmission, id=submission_id)
        print(f"Waste Submission ID: {waste_submission.id}")  # Debugging: Print waste submission ID

        # Fetch the associated payment record
        payment = Payment.objects.filter(waste_submission=waste_submission).first()

        # Extract data from request
        kilo = request.data.get("kilo")
        total_price = request.data.get("total_price")
        description = request.data.get("description")  # ✅ Get the description

        print(f"Received Data - Kilo: {kilo}, Total Price: {total_price}, Description: {description}")

        # Update kilo (weight)
        if kilo:
            waste_submission.kilo = Decimal(kilo)  # Ensure proper decimal conversion

        # Update description
        if description is not None:
            waste_submission.description = description

        if payment:
            print(f"Payment Found - ID: {payment.id}, Option: {payment.payment_option}")

            if payment.payment_option == "cash":
                print(f"Total Price Before Update: {payment.total_price}")

                if total_price == "0.00":  # If total price is zero, reject the submission
                    waste_submission.status = "rejected"
                    payment.cash_status = "unpaid"
                    payment.total_price = Decimal(total_price)
                    print(f"Updating Payment - Rejected, New Cash Status: {payment.cash_status}")
                else:  # Otherwise, process as completed
                    payment.total_price = Decimal(total_price)  # Convert safely
                    waste_submission.status = "completed"
                    payment.cash_status = "paid"
                    print(f"Updating Payment - New Cash Status: {payment.cash_status}, Total Price: {payment.total_price}")

            elif payment.payment_option == "card_payment":
                waste_submission.status = "completed"
                print("Payment is via Card. Marking submission as Completed.")

            # Save both models
            payment.save()
            waste_submission.save()

            print(f"Waste Submission Status After Save: {waste_submission.status}")
            print(f"Payment Cash Status After Save: {payment.cash_status}")
        else:
            print("No Payment Record Found for this Waste Submission.")

        # Return response
        return Response({
            "message": "Waste submission updated successfully",
            "waste_submission": {
                "id": waste_submission.id,
                "status": waste_submission.status,
                "kilo": str(waste_submission.kilo),
                "description": waste_submission.description,
                "total_price": str(waste_submission.total_price)
            },
            "payment": {
                "id": payment.id if payment else None,
                "cash_status": payment.cash_status if payment else None,
                "total_price": str(payment.total_price) if payment else None,
            }
        }, status=status.HTTP_200_OK)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from userapp.models import Payment, WasteSubmission
from userapp.serializers import PaymentSerializer

class ViewCardPaymentDetails(APIView):
    def get(self, request, waste_submission_id):
        # Fetch the waste submission
        waste_submission = get_object_or_404(WasteSubmission, id=waste_submission_id)

        # Fetch payment details for the given waste submission
        payment = get_object_or_404(Payment, waste_submission=waste_submission, payment_option="card_payment")

        # Serialize the payment data
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from userapp.models import WasteSubmission
from adminapp.models import Employee
from employeeapp.serializers import EmployeeWasteSubmissionStatusSerializer

class CompletedWasteSubmissionsView(APIView):
    def get(self, request, employee_id):
        try:
            employee = Employee.objects.get(employee_id=employee_id)
            completed_submissions = WasteSubmission.objects.filter(
                user__ward__in=employee.ward.all(), status="completed"
            )

            if not completed_submissions.exists():
                return Response({"message": "No completed waste submissions found"}, status=status.HTTP_200_OK)

            serializer = EmployeeWasteSubmissionStatusSerializer(completed_submissions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)


class RejectedWasteSubmissionsView(APIView):
    def get(self, request, employee_id):
        try:
            employee = Employee.objects.get(employee_id=employee_id)
            rejected_submissions = WasteSubmission.objects.filter(
                user__ward__in=employee.ward.all(), status="rejected"
            )

            if not rejected_submissions.exists():
                return Response({"message": "No rejected waste submissions found"}, status=status.HTTP_200_OK)

            serializer = EmployeeWasteSubmissionStatusSerializer(rejected_submissions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)