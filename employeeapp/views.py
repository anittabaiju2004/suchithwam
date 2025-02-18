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
        # Ensure that employees can only view their own profile
        return Employee.objects.get(id=self.kwargs['employee_id'])  # Get the employee by ID in URL


class EmployeeProfileUpdateView(generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_object(self):
        return Employee.objects.get(id=self.kwargs['employee_id'])  # Get the employee by ID

# views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from adminapp.models import Employee
from userapp.models import WasteSubmission
from .serializers import WasteSubmissionUpdateSerializer, WasteSubmissionListSerializer

class AssignedTasksView(generics.ListAPIView):
    """
    API to list assigned tasks for a specific employee using employee ID
    """
    serializer_class = WasteSubmissionListSerializer

    def get_queryset(self):
        employee_id = self.request.query_params.get('employee_id')  # Get employee ID from request params
        if not employee_id:
            return WasteSubmission.objects.none()  # Return empty queryset if no employee ID provided
        
        employee = get_object_or_404(Employee, employee_id=employee_id)
        return WasteSubmission.objects.filter(status="assigned", user__ward__in=employee.ward.all())

class UpdateTaskStatusView(generics.UpdateAPIView):
    """
    API to update task status (incomplete or completed) using employee ID
    """
    serializer_class = WasteSubmissionUpdateSerializer

    def get_queryset(self):
        return WasteSubmission.objects.all()  # Allow updating any assigned submission

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_status = request.data.get("status")
        employee_id = request.data.get("employee_id")  # Get employee ID from request body

        if not employee_id:
            return Response({"error": "Employee ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate if the employee exists
        employee = get_object_or_404(Employee, employee_id=employee_id)

        # Validate if the employee belongs to the ward of the waste submission
        if employee.ward.filter(id=instance.user.ward.id).exists():
            if new_status not in ["complete", "incomplete"]:
                return Response({"error": "Invalid status update."}, status=status.HTTP_400_BAD_REQUEST)

            instance.status = new_status
            instance.save()
            return Response({"message": f"Task status updated to {new_status}"}, status=status.HTTP_200_OK)
        
        return Response({"error": "Employee not authorized to update this task"}, status=status.HTTP_403_FORBIDDEN)
