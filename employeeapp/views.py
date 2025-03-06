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
class EmployeeWasteSubmissionView(APIView):
    def get(self, request, employee_id):
        try:
            employee = Employee.objects.get(employee_id=employee_id)
            waste_submissions = WasteSubmission.objects.filter(user__ward__in=employee.ward.all())

            if not waste_submissions.exists():
                return Response({"message": "No waste submissions found"}, status=status.HTTP_200_OK)

            response_data = []
            for submission in waste_submissions:
                payment = Payment.objects.filter(waste_submission=submission).first()
                payment_status = payment.status if payment else None
                cash_status = payment.cash_status if payment else None
                total_price = payment.total_price if payment_status == 'card_payment' else None

                response_data.append({
                    "id": submission.id,
                    "name": submission.user.name,
                    "address": submission.user.address,
                    "ward_number": submission.user.ward.ward_number if submission.user.ward else None,  # Added ward_number
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
                    "employee_id":employee_id
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
# class WasteSubmissionUpdateView(APIView):
#     def patch(self, request, submission_id):
#         waste_submission = get_object_or_404(WasteSubmission, id=submission_id)
#         payment = Payment.objects.filter(waste_submission=waste_submission).first()

#         kilo = request.data.get("kilo")
#         total_price = request.data.get("total_price")

#         # Update kilo (weight)
#         if kilo:
#             waste_submission.kilo = kilo

#         if payment and payment.payment_option == "cash":
#             if total_price:
#                 payment.total_price = Decimal(total_price)  # Ensure correct decimal value
#                 waste_submission.status = "completed"
#                 payment.cash_status = "paid"
#             else:
#                 waste_submission.status = "rejected"
#                 payment.cash_status = "unpaid"

#             payment.save()  # Ensure payment table is updated

#         waste_submission.save()  # Ensure waste submission table is updated

#         return Response({"message": "Waste submission updated successfully"}, status=status.HTTP_200_OK)


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
class WasteSubmissionUpdateView(APIView):
    def patch(self, request, submission_id):
        waste_submission = get_object_or_404(WasteSubmission, id=submission_id)
        payment = Payment.objects.filter(waste_submission=waste_submission).first()

        kilo = request.data.get("kilo")
        total_price = request.data.get("total_price")
        description = request.data.get("description")  # ✅ Get the description from request data

        print(f"Received Data - Kilo: {kilo} Total Price: {total_price} Description: {description}")

        # Update kilo (weight)
        if kilo:
            waste_submission.kilo = kilo

        # ✅ Update description
        if description:
            waste_submission.description = description

        if payment:
            print(f"Payment Found - ID: {payment.id} Option: {payment.payment_option}")

            if payment.payment_option == "cash":
                if total_price:
                    payment.total_price = Decimal(total_price)  # Ensure correct decimal value
                    waste_submission.status = "completed"
                    payment.cash_status = "paid"
                else:
                    waste_submission.status = "rejected"
                    payment.cash_status = "unpaid"

                payment.save()  # Ensure payment table is updated
                print(f"Updating Payment - Cash Status: {payment.cash_status} Total Price: {payment.total_price}")

        waste_submission.save()  # ✅ Ensure waste submission table is updated, including description
        print(f"Waste Submission Updated Successfully - Status: {waste_submission.status} Description: {waste_submission.description}")

        return Response({"message": "Waste submission updated successfully"}, status=status.HTTP_200_OK)


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
