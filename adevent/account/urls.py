from django.urls import path, include
from . import views

app_name= 'account'
urlpatterns = [
    
    path('signup', views.sign_up, name="signup"),
    path('signup/submit', views.signup_submit, name="signup_submit"),
    path('signup/complete/<token>', views.sign_up_complete, name="signup_complete"),
]