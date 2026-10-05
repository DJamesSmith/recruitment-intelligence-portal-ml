from django.urls import path
from accounts import views

urlpatterns: list[object] = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("verify-email/", views.verify_email, name="verify_email"),
]
