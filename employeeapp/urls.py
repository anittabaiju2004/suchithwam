# urls.py
from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import EmployeeLoginView,EmployeeProfileUpdateView,EmployeeProfileView,AssignedTasksView,UpdateTaskStatusView

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
    # path('update-profile/<int:employee_id>/', EmployeeProfileUpdateView.as_view(), name='update-profile'),
    path('profile/<int:employee_id>/', EmployeeProfileView.as_view(), name='view-profile'),
    path('update-profile/<int:employee_id>/', EmployeeProfileUpdateView.as_view(), name='update-profile'),
     path('employee/tasks/', AssignedTasksView.as_view(), name='assigned-tasks'),
    path('employee/tasks/<int:pk>/update/', UpdateTaskStatusView.as_view(), name='update-task-status'),
]
    

