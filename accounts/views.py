from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import CustomUser

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            # Auto login after signup
            user = authenticate(username=username, password=form.cleaned_data.get('password1'))
            if user:
                login(request, user)
                return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def dashboard_view(request):
    user = request.user
    context = {
        'user': user,
        'user_details': {
            'First Name': user.first_name,
            'Last Name': user.last_name,
            'Username': user.username,
            'Email': user.email,
            'User Type': user.get_user_type_display(),
            'Address': user.address_line1,
            'City': user.city,
            'State': user.state,
            'Pincode': user.pincode,
        }
    }
    
    if user.user_type == 'patient':
        return render(request, 'accounts/patient_dashboard.html', context)
    elif user.user_type == 'doctor':
        return render(request, 'accounts/doctor_dashboard.html', context)
    else:
        return render(request, 'accounts/dashboard.html', context)

def home_view(request):
    return render(request, 'accounts/home.html')