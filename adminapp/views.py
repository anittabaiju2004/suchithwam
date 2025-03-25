from django.shortcuts import render

from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from .models import WasteThreshold



from django.shortcuts import render, redirect
from .models import WasteThreshold

from django.shortcuts import render
from userapp.models import WasteSubmission

from django.shortcuts import render, redirect
from django.db.models import Sum
from .models import  WasteThreshold

# def admin_index(request):
#     # Retrieve or create a threshold instance
#     threshold, created = WasteThreshold.objects.get_or_create(id=1)  # Ensuring a single threshold record

#     # Get status counts
#     status_counts = {
#         'Pending': WasteSubmission.objects.filter(status='pending').count(),
#         'Completed': WasteSubmission.objects.filter(status='completed').count(),
#         'Rejected': WasteSubmission.objects.filter(status='rejected').count(),
#     }

#     # Calculate total waste (sum of 'kilo' field)
#     total_waste = WasteSubmission.objects.aggregate(total=Sum('kilo'))['total'] or 0

#     # Check if total waste exceeds threshold
#     over_limit = total_waste > threshold.limit

#     if request.method == "POST":
#         new_limit = request.POST.get('limit')
#         if new_limit:
#             threshold.limit = float(new_limit)
#             threshold.save()
#         return redirect('admin_index')  # Redirect to refresh data

#     context = {
#         'status_counts': status_counts,
#         'total_waste': total_waste,
#         'threshold': threshold.limit,
#         'over_limit': over_limit
#     }
#     return render(request, 'admin_index.html', context)
from django.shortcuts import render, redirect
from django.db.models import Sum
from .models import WasteThreshold
from userapp.models import WasteSubmission

def admin_index(request):
    threshold, created = WasteThreshold.objects.get_or_create(id=1)  # Ensuring a single threshold record

    # Get status counts
    status_counts = {
        'Pending': WasteSubmission.objects.filter(status='pending').count(),
        'Completed': WasteSubmission.objects.filter(status='completed').count(),
        'Rejected': WasteSubmission.objects.filter(status='rejected').count(),
    }

    # Calculate total waste
    total_waste = WasteSubmission.objects.aggregate(total=Sum('kilo'))['total'] or 0
    over_limit = total_waste > threshold.limit

    if request.method == "POST":
        # Update Threshold
        new_limit = request.POST.get('limit')
        if new_limit:
            threshold.limit = float(new_limit)
            threshold.save()

        # Update Quotation
        new_quotation = request.POST.get('quotation')
        if new_quotation:
            threshold.quotation = float(new_quotation)

        # Update Status
        new_status = request.POST.get('status')
        if new_status == 'collected':
            WasteSubmission.objects.update(kilo=0)


        threshold.save()

        return redirect('admin_index')

    context = {
        'status_counts': status_counts,
        'total_waste': total_waste,
        'threshold': threshold.limit,
        'quotation': threshold.quotation,
        'status': threshold.status,
        'over_limit': over_limit
    }
    return render(request, 'admin_index.html', context)


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



from django.shortcuts import render, redirect, get_object_or_404
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

def list_categories(request):
    categories = tbl_category.objects.all()
    return render(request, 'categories_list.html', {'categories': categories})

def edit_category(request, category_id):
    category = get_object_or_404(tbl_category, id=category_id)
    
    if request.method == 'POST':
        category.name = request.POST.get('categoryName')
        
        if 'categoryImage' in request.FILES:
            category.image = request.FILES['categoryImage']
        
        category.save()
        return redirect('list_categories')
    
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
                return redirect("add_ward")  # Redirect to ward list after adding
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



# from userapp.models import WasteSubmissionDetail
from django.shortcuts import render, get_object_or_404
from .models import Ward
from userapp.models import WasteSubmission

def ward_request_details(request, ward_id):
    """Displays the waste submissions for a specific ward with all required details."""
    ward = get_object_or_404(Ward, id=ward_id)
    
    # Fetch waste submissions for this ward
    waste_submissions = WasteSubmission.objects.filter(user__ward=ward).order_by("-date")

    # Process each submission to split categories and kilograms
    for submission in waste_submissions:
        submission.category_list = submission.categories.split(",") if submission.categories else []
        # Add this line to split the kilograms into a list
    

    return render(request, "ward_request_details.html", {
        "ward": ward,
        "waste_submissions": waste_submissions,
    })
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Employee, Ward

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Employee, Ward

def register_employee(request):
    if request.method == "POST":
        employee_id = request.POST.get("employee_id")
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")  # Storing password as plain text
        image = request.FILES.get("image")
        ward_ids = request.POST.getlist("ward")  # Get multiple selected ward IDs

        if not image:
            messages.error(request, "Both Employee Image and Aadhar Image are required!")
        elif Employee.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
        else:
            # Get the selected wards from the database
            wards = Ward.objects.filter(id__in=ward_ids)
            
            employee = Employee.objects.create(
                employee_id=employee_id,
                name=name,
                email=email,
                phone=phone,
                password=password,  # Stored as plain text
                image=image,
            )
            # Add the selected wards to the employee
            employee.ward.set(wards)
            employee.save()

            messages.success(request, "Employee registered successfully!")
            return redirect("register_employee")

    wards = Ward.objects.all()
    return render(request, "register_employee.html", {"wards": wards})



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Employee, Ward

def list_employees(request):
    employees = Employee.objects.all()
    return render(request, "list_employees.html", {"employees": employees})


    
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Employee, Ward
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    wards = Ward.objects.all()
    selected_ward_ids = employee.ward.values_list('id', flat=True)  # Get selected ward IDs

    if request.method == "POST":
        # Update the employee's fields
        employee.employee_id = request.POST.get("employee_id")
        employee.name = request.POST.get("name")
        employee.email = request.POST.get("email")
        employee.phone = request.POST.get("phone")
        employee.password = request.POST.get("password")  # No hashing for simplicity
        
        # Handling file uploads for images
        if "image" in request.FILES:
            employee.image = request.FILES["image"]
        
        # Handle multiple selected wards
        ward_ids = request.POST.getlist("ward")
        wards_selected = Ward.objects.filter(id__in=ward_ids)
        employee.save()
        employee.ward.set(wards_selected)  # Save multiple wards
        employee.save()

        messages.success(request, "Employee details updated successfully!")
        return redirect("list_employees")

    return render(request, "edit_employee.html", {"employee": employee, "wards": wards, "selected_ward_ids": selected_ward_ids})

def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    messages.success(request, "Employee deleted successfully!")
    return redirect("list_employees")



from django.shortcuts import render
from userapp.models import Feedback

def admin_feedback_list(request):
    """View to display all feedbacks for the admin"""
    feedbacks = Feedback.objects.all()
    return render(request, 'admin_feedback_list.html', {'feedbacks': feedbacks})


from django.shortcuts import render, redirect
from .models import Recycler
from django.shortcuts import render, redirect, get_object_or_404
from .models import Recycler
from django.shortcuts import render, redirect, get_object_or_404
from .models import Recycler

def manage_recyclers(request):
    if request.method == "POST":
        recycler_id = request.POST.get("recycler_id")
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")  # Store securely in production
        phone = request.POST.get("phone")
        profile_pic = request.FILES.get("profile_pic")
        aadhar_number = request.POST.get("aadhar_number")
        panchayath_name = request.POST.get("panchayath_name")

        Recycler.objects.create(
            recycler_id=recycler_id,
            name=name,
            email=email,
            password=password,  # Store securely in production
            phone=phone,
            profile_pic=profile_pic,
            aadhar_number=aadhar_number,
            panchayath_name=panchayath_name,
        )

        return redirect('manage_recyclers')

    recyclers = Recycler.objects.all()
    return render(request, "manage_recyclers.html", {"recyclers": recyclers})

def edit_recycler(request, recycler_id):
    recycler = get_object_or_404(Recycler, id=recycler_id)

    if request.method == "POST":
        recycler.recycler_id = request.POST.get("recycler_id")
        recycler.name = request.POST.get("name")
        recycler.email = request.POST.get("email")
        recycler.password = request.POST.get("password")
        recycler.phone = request.POST.get("phone")
        recycler.aadhar_number = request.POST.get("aadhar_number")
        recycler.panchayath_name = request.POST.get("panchayath_name")

        if 'profile_pic' in request.FILES:
            recycler.profile_pic = request.FILES['profile_pic']

        recycler.save()
        return redirect('manage_recyclers')

    return render(request, "edit_recycler.html", {"recycler": recycler})

def delete_recycler(request, recycler_id):
    recycler = get_object_or_404(Recycler, id=recycler_id)
    
    if request.method == "POST":
        recycler.delete()
        return redirect('manage_recyclers')

