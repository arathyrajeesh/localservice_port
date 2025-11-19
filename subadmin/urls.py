from django.urls import path
from . import views

urlpatterns = [
    path('adminlogin', views.admin_login_view, name='admin_login'),
    path('adminhome', views.admin_home_view, name='admin_home'),

    path('subadmin/manage-worker/', views.manage_worker, name='manage_worker'),
    path('subadmin/worker-requests/', views.worker_requests, name='worker_requests'),
    path('subadmin/approve-worker/<int:worker_id>/', views.approve_worker, name='approve_worker'),
    path('subadmin/reject-worker/<int:worker_id>/', views.reject_worker, name='reject_worker'),

    path('manage_consumer', views.manage_consumer, name='manage_consumer'),
    path('subadmin/delete-consumer/<int:consumer_id>/', views.delete_consumer, name='delete_consumer'),
]
