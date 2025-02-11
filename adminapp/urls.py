from django.urls import path
from . import views 
urlpatterns = [
    path('admin_index/', views.admin_index, name='admin_index'), 
    path('',views.admin_login,name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('add_category/', views.add_category, name='add_category'),
    path('categories/', views.list_categories, name='list_categories'),
    path('categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
     path("add_ward/", views.add_ward, name="add_ward"),
     path("wards/", views.list_wards, name="list_wards"),
     path("edit-ward/<int:ward_id>/", views.edit_ward, name="edit_ward"),
     path('ward/delete/<int:ward_id>/', views.delete_ward, name='delete_ward'),
   path("requests/", views.ward_requests, name="ward_requests"),
    path("requests/<int:ward_id>/", views.ward_request_details, name="ward_request_details"),
]
