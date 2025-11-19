from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from .models import ConsumerProfile,Booking
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from worker import models as wmodel
from consumer import models as cmodel

def home_view(request):
    return render(request, 'home.html')

def login_view(request):
    return render(request,'login.html')

def signup_view(request):
    return render(request,'signup.html')

def consumer_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('consumer_home')  
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('consumer_login')

    return render(request, 'consumerlogin.html')

def consumer_signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        location = request.POST['location']
        phone = request.POST['phone']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('consumer_signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('consumer_signup')

        user = User.objects.create_user(username=username, password=password)
        ConsumerProfile.objects.create(user=user, location=location, phone=phone)

        messages.success(request, "Account created successfully. Please log in.")
        return redirect('consumer_login')

    return render(request, 'consumersignup.html')


def consumer_home_view(request):
    return render(request, 'consumerhome.html')


def consumer_service_view(request):
    services = wmodel.Service.objects.all()
    return render(request, 'consumerhome.html', {
        'services': services,
        'user': request.user
    })

def book_service(request, service_id):
    service = get_object_or_404(wmodel.Service, id=service_id)

    if request.method == 'POST':
        service_date = request.POST.get('date')
        cmodel.Booking.objects.create(
            consumer=request.user,
            service=service,
            date=service_date
        )
        messages.success(request, 'Booking confirmed!')
        return redirect('consumer_home')

    return render(request, 'book_service.html', {'service': service})




# def search_view(request):
#     query=request.GET['query']
#     services=wmodel.Service.objects.all().filter(title=query)
#     if 'service_ids' in request.COOKIES:
#         service_ids=request.COOKIES['service_ids']
#         counter=service_ids.split('|')
#         service_count_in_cart=len(set(counter))
#     else:
#         service_count_in_cart=0
        
#     word='searched result :'
    
#     if request.user.is_authenticated:
#         return render(request,'consumerhome.html',{'services':services,'word':word,'service_count_in_cart':service_count_in_cart})
#     return render(request,'consumerhome.html',{'services':services,'word':word,'service_count_in_cart':service_count_in_cart})



def search_view(request):
    query = request.GET.get('query', '')
    services = wmodel.Service.objects.filter(title__icontains=query)

    word = f"Search results for '{query}':"

    return render(request, 'consumerhome.html', {
        'services': services,
        'word': word
    })

def added_service_view(request):
    bookings = Booking.objects.filter(consumer=request.user)

    booking_data = []
    for booking in bookings:
        messages = wmodel.Message.objects.filter(booking=booking).order_by('-timestamp')
        booking_data.append({'booking': booking, 'messages': messages})

    return render(request, 'added_service.html', {'booking_data': booking_data})


def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, consumer=request.user)
    booking.delete()
    return redirect('addservice')



