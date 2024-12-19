# from datetime import datetime  
from django.utils import timezone  # Import this to use timezone.now()
from django.shortcuts import render,redirect,get_object_or_404
from .models import UserDetails
from .models import ComplaintDetails
from django.contrib import messages
from django.db import models

# Create your views here.
def welcome(request):
    return render(request, 'welcome.html')

def register(request):
    return render(request, 'register.html')

def complaint_page(request):
    return render(request, 'complaint.html')

def complaint_history(request):
    user = UserDetails.objects.get(username='student1')  
    complaints = ComplaintDetails.objects.filter(user=user)
    return render(request, 'complaint_history.html', {'complaints': complaints})

def complaint_log(request):
    return render(request, 'complaint_log.html')

def submit_complaint(request):
    if request.method == 'POST':
        executive_name = request.POST.get('executive_name')
        complaint_text = request.POST.get('complaint_text')
        user = UserDetails.objects.get(username='student1')
        ComplaintDetails.objects.create(
            user=user,
            executive_name=executive_name,
            complaint_text=complaint_text,
            status='new', 
            created_date=timezone.now(),
            last_updated=timezone.now(),
        )
        messages.success(request, 'Complaint submitted successfully!')
        return redirect('complaint_history')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('complaint')
    
def complaint_log(request):
    executive_name = request.user.username 
    complaints = ComplaintDetails.objects.filter(executive_name="Mary Martin")
    return render(request, 'complaint_log.html', {'complaints': complaints})


def complaint_detail(request, complaint_id):
    complaint = get_object_or_404(ComplaintDetails, id=complaint_id)

    # Handle status update if the form is submitted
    if request.method == 'POST':
        status = request.POST.get('status')
        if status:
            complaint.status = status
            complaint.last_updated = timezone.now()  # Set last_updated as a valid datetime object
            complaint.save()  # Save the updated complaint with the new last_updated value

        return redirect('complaint_detail', complaint_id=complaint.id)

    return render(request, 'complaint_detail.html', {'complaint': complaint})
    

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')  
        try:
            user = UserDetails.objects.get(username=username, password=password, user_type=user_type)
            
            if user.user_type == 'student':
                return redirect('complaint')  
            elif user.user_type == 'executive':
                return redirect('complaint_log')  
        except UserDetails.DoesNotExist:
            messages.error(request, 'Invalid username, password, or account type.')
            return redirect('welcome')

    return render(request, 'welcome.html')

def signup_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # New field for username
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if password and confirm password match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        # Ensure the email is unique
        if UserDetails.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('signup')

        if UserDetails.objects.filter(email=email).exists():
            messages.error(request, "Email is already taken.")
            return redirect('signup')

        # Create new user
        try:
            new_user = UserDetails.objects.create(
                username=username,  # Saving username
                email=email,
                password=password,  # Ideally, hash the password in production
                first_name=first_name,
                last_name=last_name,
                user_type='student'  # Always a student
            )
            new_user.save()
            messages.success(request, "Account successfully created.")
            return redirect('welcome')  # Redirect to login or welcome page after signup
        except ValidationError as e:
            messages.error(request, f"Error: {e}")
            return redirect('signup')

    return render(request, 'signup.html')
