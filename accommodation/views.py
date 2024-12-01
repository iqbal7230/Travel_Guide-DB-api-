from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password, check_password
from .models import Hotel
from .forms import HotelOwnerRegistrationForm, HotelOwnerLoginForm
from django.conf import settings


def hotel_owner_registration(request):
    if request.method == 'POST':
        form = HotelOwnerRegistrationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirm_password')
            if password != confirm_password:
                messages.error(request, "Passwords do not match!")
            else:
                hotel_owner = form.save(commit=False)
                hotel_owner.password = make_password(password)
                hotel_owner.save()
                messages.success(request, "Registration successful!")
                return redirect('login')  
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = HotelOwnerRegistrationForm()

    return render(request, 'hotel_owner_register.html', {'form': form, 'MEDIA_URL': settings.MEDIA_URL})


def hotel_owner_login(request):
    if request.method == "POST":
        form = HotelOwnerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                hotel_owner = Hotel.objects.get(email=email)   
                if check_password(password, hotel_owner.password):
                    request.session['hotel_owner_id'] = hotel_owner.id 
                    messages.success(request, "Login successful!")
                    return redirect('hotel_dashboard')
                else:
                    messages.error(request, "Invalid Password.")
            except hotel_owner.DoesNotExist:
                messages.error(request, "profile doesn't exists.")
        else:
            messages.error(request, "Errors in the form.")
    else:     
        form = HotelOwnerLoginForm()
    return render(request, 'hotel_owner_login.html', {'form':form, 'MEDIA_URL': settings.MEDIA_URL})


def contact_support(request):    
    return render(request, 'contact.html', {'MEDIA_URL': settings.MEDIA_URL})

def get_dashboard(request):
    return render(request, 'hotel_dashboard.html', {'MEDIA_URL': settings.MEDIA_URL})


