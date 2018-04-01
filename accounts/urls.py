from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import Login, Signup, index, SetPassword, ResetPassword


urlpatterns = [
    path('', index, name='index'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('signup/', Signup.as_view(), name='signup'),
    path('setpassword/<int:user_id>/', SetPassword.as_view(), name='setpassword'),
    path('resetpassword/',ResetPassword.as_view(), name='resetpassword'),
    path('resetpassword/<int:user_id>/<uuid:uid>/',
         ResetPassword.as_view(), name='resetpassword_template'),
]
