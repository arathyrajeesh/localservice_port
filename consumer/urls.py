from django.contrib import admin
from django.urls import path
from . import views  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),  
    path('login/',views.login_view,name='login'),
    path('signup/', views.signup_view, name='signup'), 
    path('consumer/',views.consumer_login_view,name='consumer_login'),
    path('consumersignup/',views.consumer_signup_view,name='consumer_signup'),
    path('consumerhome',views.consumer_home_view,name='consumer_home'),
    path('consumer/home/', views.consumer_service_view, name='consumer_home'),
    path('book/<int:service_id>/', views.book_service, name='book_service'),
    path('search/',views.search_view,name='search'),
    path('addedservice',views.added_service_view,name='addservice'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),

]
