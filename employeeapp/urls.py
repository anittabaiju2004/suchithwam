# urls.py
from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from employeeapp.views import *
# Swagger Schema Configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Suchithwam App",
        default_version="v1",
        description="API documentation for Suchithwam App.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@yourcompany.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[],
)

# Router Configuration (no need for DefaultRouter if only one endpoint)
router = DefaultRouter()

# URL Patterns
urlpatterns = [
    # Swagger Documentation
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    
    # Employee Login Endpoint
    path('login/', EmployeeLoginView.as_view(), name='employee_login'),
     path('profile/<str:employee_id>/', EmployeeProfileView.as_view(), name='view-profile'),

#    path('update-profile/<str:employee_id>/', UpdateProfileView.as_view(), name='update-profile'),
     path('employee/waste-submissions/<str:employee_id>/', EmployeeWasteSubmissionView.as_view(), name='employee-waste-submissions'),
      path('waste-submission/update/<int:submission_id>/', WasteSubmissionUpdateView.as_view(), name='waste-submission-update'),
      path('view-card-payment/<int:waste_submission_id>/', ViewCardPaymentDetails.as_view(), name='view-card-payment'),
      path('waste-submissions/completed/<str:employee_id>/', CompletedWasteSubmissionsView.as_view(), name='completed-waste-submissions'),
    path('waste-submissions/rejected/<str:employee_id>/', RejectedWasteSubmissionsView.as_view(), name='rejected-waste-submissions'),

    
]
    

