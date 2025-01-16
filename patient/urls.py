from django.urls import path
from . import views


app_name='patient'
urlpatterns=[
    path('login/',views.Login,name='login'),
    path('signup/',views.Signup,name='signup'),
    path('booking/',views.Booking,name='booking'),
    path('',views.Home,name='home'),
    path('list/',views.List,name='list'),
    path('otp/',views.otp,name='otp'),
    path('resend-otp/', views.resend, name='resend'),
    path('About_us/',views.aboutus,name='aboutus'),
    path('contact_us/',views.contactus,name='contactus'),
    path('our_doctors/',views.doctors,name='doctors'),
    path('search_doctors/',views.search_doctors,name='search_doctors') ,
    path('logout/',views.logout,name='logout')  
    
]
