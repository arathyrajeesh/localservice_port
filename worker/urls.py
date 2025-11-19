from django.urls import path
from django.contrib.auth.views import LoginView
from .import views

urlpatterns = [
    path('workerlogin',LoginView.as_view(template_name='worker/workerlogin.html'),name='workerlogin'),
    path('worker-signup',views.worker_signup_view,name='worker-signup'),
    path('accounts/profile/',views.worker_dashboard_view,name='worker_dashboard'),
    path('my-services/', views.view_services, name='view_services'),
    path('workerlogin/', views.worker_login_view, name='workerlogin'),
    path('bookings/', views.worker_bookings, name='worker_bookings'),
    path('send-message/<int:booking_id>/', views.send_message_view, name='send_message'),
]
