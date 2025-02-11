from django.shortcuts import render

from django.shortcuts import render, redirect

def admin_index(request):
    if not request.session.get("admin_logged_in"):
        return redirect("admin_login")  # Redirect if not logged in
    
    return render(request, "admin_index.html")

def admin_logout(request):
    request.session.flush()  # Clear session
    messages.success(request, "You have been logged out.")
    return redirect("admin_login")


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import tbl_admin  # Import the admin model

def admin_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if the email and password match the admin credentials
        if email == "admin@gmail.com" and password == "admin":
            request.session["admin_logged_in"] = True  # Store login session
            messages.success(request, "Login successful!")
            return redirect("admin_index")  # Redirect to admin dashboard

        else:
            messages.error(request, "Invalid email or password. Please try again.")
    
    return render(request, "admin_login.html")  # Render login page



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import tbl_category

def add_category(request):
    if request.method == "POST":
        category_name = request.POST.get("categoryName")
        category_image = request.FILES.get("categoryImage")

        if category_name and category_image:
            tbl_category.objects.create(name=category_name, image=category_image)
            messages.success(request, "Category added successfully!")
            return redirect("add_category")
        else:
            messages.error(request, "Please fill out all fields.")

    return render(request, "add_category.html")


from django.shortcuts import render, redirect, get_object_or_404
from .models import tbl_category

def list_categories(request):
    categories = tbl_category.objects.all()
    return render(request, 'categories_list.html', {'categories': categories})
from django.shortcuts import render, get_object_or_404, redirect
from .models import tbl_category

def edit_category(request, category_id):
    category = get_object_or_404(tbl_category, id=category_id)
    
    if request.method == 'POST':
        category.name = request.POST.get('categoryName')
        
        if 'categoryImage' in request.FILES:
            category.image = request.FILES['categoryImage']
        
        category.save()
        return redirect('list_categories')  # Ensure 'list_categories' is a valid URL name
    
    return render(request, 'edit_category.html', {'category': category})


def delete_category(request, category_id):
    category = get_object_or_404(tbl_category, id=category_id)
    category.delete()
    return redirect('list_categories')



from django.shortcuts import render, redirect
from .models import Ward

def add_ward(request):
    if request.method == "POST":
        ward_number = request.POST.get("ward_number")
        location = request.POST.get("location")

        if ward_number and location:
            # Check if the ward number is unique
            if not Ward.objects.filter(ward_number=ward_number).exists():
                Ward.objects.create(ward_number=ward_number, location=location)
                return redirect("list_wards")  # Redirect to ward list after adding
            else:
                error_message = "Ward number already exists."
                return render(request, "add_ward.html", {"error_message": error_message})

    return render(request, "add_ward.html")



from django.shortcuts import render, get_object_or_404, redirect
from .models import Ward

def edit_ward(request, ward_id):
    ward = get_object_or_404(Ward, id=ward_id)

    if request.method == "POST":
        ward_number = request.POST.get("ward_number")
        location = request.POST.get("location")

        if ward_number and location:
            # Ensure the ward number remains unique
            if Ward.objects.exclude(id=ward_id).filter(ward_number=ward_number).exists():
                error_message = "Ward number already exists."
                return render(request, "edit_ward.html", {"ward": ward, "error_message": error_message})

            ward.ward_number = ward_number
            ward.location = location
            ward.save()
            return redirect("list_wards")  # Redirect after updating

    return render(request, "edit_ward.html", {"ward": ward})


from django.shortcuts import render
from .models import Ward

def list_wards(request):
    wards = Ward.objects.all().order_by("ward_number")  # Order by ward number
    return render(request, "list_wards.html", {"wards": wards})


def delete_ward(request, ward_id):
    ward = get_object_or_404(Ward, id=ward_id)
    ward.delete()
    return redirect('list_wards')

from django.shortcuts import render
from userapp.models import tbl_register, WasteSubmission
from django.shortcuts import render
from userapp.models import tbl_register, WasteSubmission
# views.py
from django.shortcuts import render
from adminapp.models import Ward



from django.shortcuts import render, get_object_or_404
from .models import Ward
from userapp.models import WasteSubmission

def ward_requests(request):
    """Displays the list of wards."""
    wards = Ward.objects.all().order_by("ward_number")
    return render(request, "ward_requests.html", {"wards": wards})
from django.shortcuts import render, get_object_or_404
from .models import Ward
from userapp.models import WasteSubmission, WasteSubmissionDetail
from django.shortcuts import render, get_object_or_404
from .models import Ward
from userapp.models import WasteSubmission, WasteSubmissionDetail

def ward_request_details(request, ward_id):
    """Displays the waste submissions for a specific ward."""
    ward = get_object_or_404(Ward, id=ward_id)
    
    # Fetch waste submissions for this ward
    waste_submissions = WasteSubmission.objects.filter(user__ward=ward).order_by("-date")
    
    # Fetch submission details with category and kilograms
    waste_submission_details = WasteSubmissionDetail.objects.filter(waste_submission__in=waste_submissions)

    return render(request, "ward_request_details.html", {
        "ward": ward,
        "waste_submissions": waste_submissions,
        "waste_submission_details": waste_submission_details,
    })
