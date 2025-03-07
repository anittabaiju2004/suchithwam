
#userapp#
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import *
from userapp.views import MakePaymentView,UserPaymentHistoryView

from . import views
# Swagger Schema Configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Suchithwam App",
        default_version="v1",
        description="API documentation for Suchithwam App.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@yourapp.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# Router Configuration
router = DefaultRouter()
router.register(r"user_register", user_registerViewSet, basename="user_register"),
router.register(r'waste_submission', WasteSubmissionViewSet, basename='waste_submission'),
# router.register(r'profile', UserProfileViewSet, basename='user_profile')  # For viewing profile
router.register(r'profile/update', UserProfileUpdateViewSet, basename='update_user_profile')  # Update profile (ViewSet)
router.register(r'feedback', FeedbackViewSet, basename='feedback')



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

    # API Router
    path('', include(router.urls)),
    path('user_login/', LoginView.as_view(), name='user_login'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('user_wards/', WardListView.as_view(), name='user_wards'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('profile/<int:id>/', UserProfileView.as_view(), name='user_profile'),  
    path('make_payment/', MakePaymentView.as_view(), name='make_payment'),
    path('user/bookings/<int:user_id>/', UserBookingsView.as_view(), name='user-bookings'),
    path('reschedule/<int:submission_id>/', RescheduleWasteSubmissionView.as_view(), name='reschedule_waste'),
    path('update-payment/<int:waste_submission_id>/', UpdatePaymentView.as_view(), name='update-payment'),
     path('user/<int:user_id>/payments/', UserPaymentHistoryView.as_view(), name='user-payment-history'),
     

]

    
                 