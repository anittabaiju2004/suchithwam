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
