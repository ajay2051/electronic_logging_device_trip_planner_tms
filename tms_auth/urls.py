from django.urls import path

from tms_auth.views.create_users import CreateUserView
from tms_auth.views.forgot_password import ForgotPasswordConfirmView, ForgotPasswordView
from tms_auth.views.user_login import UserLoginView
from tms_auth.views.verify_users import verify_user_account

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('create_users/', CreateUserView.as_view(), name='create_users'),

    path('verify_users/<int:user_id>/<str:token>/', verify_user_account, name='verify_users'),

    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("forgot-password-confirm/<int:user_id>/<str:token>/", ForgotPasswordConfirmView.as_view(), name="forgot-password-confirm", ),

]
