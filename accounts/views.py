from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from accounts.forms import LoginForm, RegistrationForm
from accounts.models import User
from accounts.services import create_token, create_verification_code, verify_code


def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form: RegistrationForm = RegistrationForm(request.POST)
        if form.is_valid():
            user: User = form.save()
            create_verification_code(user)
            return redirect("verify_email")
    else:
        form = RegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form: LoginForm = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].lower()
            password = form.cleaned_data["password"]
            user: User | None = authenticate(request, email=email, password=password)
            if user is not None:
                if user.role == User.Role.HR and not user.is_email_verified:
                    form.add_error(None, "Email verification required.")
                else:
                    login(request, user)
                    request.session["jwt"] = create_token(user)
                    return redirect("candidate_list")
            else:
                form.add_error(None, "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("login")


def verify_email(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        email = str(request.POST.get("email", "")).strip().lower()
        code = str(request.POST.get("code", "")).strip()
        try:
            user: User = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if user is not None and verify_code(user, code):
            return redirect("login")
        return render(request, "accounts/verify_email.html", {"error": "Invalid or expired code."})
    return render(request, "accounts/verify_email.html")
