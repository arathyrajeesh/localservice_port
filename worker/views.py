from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .models import Worker, Service,Message
from .forms import WorkerUserForm, WorkerForm, ServiceForm
from consumer.models import Booking


def worker_signup_view(request):
    userform = WorkerUserForm()
    workerform = WorkerForm()

    if request.method == 'POST':
        userform = WorkerUserForm(request.POST)
        workerform = WorkerForm(request.POST)
        
        if userform.is_valid() and workerform.is_valid():
            # Create user and set password
            user = userform.save(commit=False)
            raw_password = userform.cleaned_data.get('password')
            user.set_password(raw_password)
            user.save()

            # Create worker profile
            worker = workerform.save(commit=False)
            worker.user = user
            worker.save()

            # Add user to 'WORKER' group
            worker_group, created = Group.objects.get_or_create(name='WORKER')
            worker_group.user_set.add(user)

            messages.info(request, "Signup successful! Please wait for Subadmin approval before logging in.")
            return redirect('workerlogin')

    context = {'userform': userform, 'workerform': workerform}
    return render(request, 'worker/worker_signup.html', context)



def worker_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                worker = Worker.objects.get(user=user)
                if worker.status == 'approved':
                    login(request, user)
                    return redirect('worker_dashboard')
                else:
                    messages.error(request, "Your account is pending Subadmin approval.")
            except Worker.DoesNotExist:
                messages.error(request, "Worker account not found.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'worker/workerlogin.html')


@login_required
def worker_dashboard_view(request):
    try:
        worker = Worker.objects.get(user=request.user)
        if worker.status != 'approved':
            messages.error(request, "Your account is not approved yet.")
            return redirect('workerlogin')
    except Worker.DoesNotExist:
        messages.error(request, "Worker profile not found.")
        return redirect('workerlogin')

    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.worker = request.user
            service.save()
            messages.success(request, "Service added successfully!")
            return redirect('worker_dashboard')
    else:
        form = ServiceForm()

    return render(request, 'worker/worker_dashboard.html', {'form': form})


@login_required
def view_services(request):
    try:
        worker = Worker.objects.get(user=request.user)
        if worker.status != 'approved':
            messages.error(request, "Access denied. Your account is not approved yet.")
            return redirect('workerlogin')
    except Worker.DoesNotExist:
        messages.error(request, "Worker profile not found.")
        return redirect('workerlogin')

    services = Service.objects.filter(worker=request.user)
    return render(request, 'worker/view_service.html', {'services': services})



def worker_bookings(request):
    bookings = Booking.objects.filter(service__worker=request.user).order_by('-created_at')
    return render(request, 'worker/worker_booking.html', {'bookings': bookings})


@login_required
def send_message_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == "POST":
        content = request.POST.get("message")
        messages.success(request, f"Message sent to {booking.consumer.username}: {content}")
        
    return redirect('worker_bookings') 


def send_message_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        content = request.POST.get('message')
        Message.objects.create(
            booking=booking,
            sender=request.user,
            receiver=booking.consumer,
            content=content
        )
        messages.success(request, "Message sent to the consumer.")
        
    return redirect('worker_bookings')