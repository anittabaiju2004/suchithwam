from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import RecyclerLoginView# Import RecyclerLoginView,
from .views import WasteThresholdView ,RecyclerQuotationView 
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
    path('recycler_login/', RecyclerLoginView.as_view(), name='recycler_login'),
     path('waste-threshold/', WasteThresholdView.as_view(), name='waste_threshold'), 
     path('recycler/quotation/', RecyclerQuotationView.as_view(), name='recycler-quotation'),
]