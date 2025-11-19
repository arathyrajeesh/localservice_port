from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from consumer import models as cmodel
from worker.models import Worker


def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_home')
        else:
            messages.error(request, "Access denied. Invalid credentials or not a subadmin.")
            return redirect('admin_login')

    return render(request, 'subadmin/adminlogin.html')


@login_required(login_url='admin_login')
def admin_home_view(request):
    if request.user.is_staff:
        return render(request, 'subadmin/adminhome.html')
    else:
        messages.error(request, "Access denied.")
        return redirect('admin_login')


@login_required(login_url='admin_login')
def manage_worker(request):
    if request.user.is_staff:
        approved_workers = Worker.objects.filter(status='approved')
        return render(request, 'subadmin/manage_worker.html', {'workers': approved_workers})
    else:
        messages.error(request, "Access denied.")
        return redirect('admin_login')



@login_required(login_url='admin_login')
def worker_requests(request):
    if request.user.is_staff:
        pending_workers = Worker.objects.filter(status='pending')
        return render(request, 'subadmin/worker_request.html', {'workers': pending_workers})
    else:
        messages.error(request, "Access denied.")
        return redirect('admin_login')


@login_required(login_url='admin_login')
def approve_worker(request, worker_id):
    if request.user.is_staff:
        worker = get_object_or_404(Worker, id=worker_id)
        worker.status = 'approved'
        worker.save()
        messages.success(request, "Worker approved successfully.")
    return redirect('worker_requests')


@login_required(login_url='admin_login')
def reject_worker(request, worker_id):
    if request.user.is_staff:
        worker = get_object_or_404(Worker, id=worker_id)
        worker.status = 'rejected'
        worker.save()
        messages.success(request, "Worker rejected.")
    return redirect('worker_requests')


@login_required(login_url='admin_login')
def manage_consumer(request):
    if request.user.is_staff:
        consumers = cmodel.ConsumerProfile.objects.all()
        return render(request, 'subadmin/manage_consumer.html', {'consumers': consumers})
    else:
        messages.error(request, "Access denied.")
        return redirect('admin_login')


@require_POST
@login_required(login_url='admin_login')
def delete_consumer(request, consumer_id):
    if request.user.is_staff:
        consumer = get_object_or_404(cmodel.ConsumerProfile, id=consumer_id)
        user = consumer.user
        consumer.delete()
        user.delete()
        messages.success(request, "Consumer deleted.")
    return redirect('manage_consumer')
