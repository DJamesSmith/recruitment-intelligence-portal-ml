from django import forms

from accounts.models import User
from accounts.validators import validate_email_format, validate_phone_format


class RegistrationForm(forms.ModelForm):
    password1: forms.CharField = forms.CharField(widget=forms.PasswordInput)
    password2: forms.CharField = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model: type[User] = User
        fields: list[str] = [
            "email",
            "first_name",
            "last_name",
            "phone",
            "role",
        ]

    def clean_email(self: "RegistrationForm") -> str:
        email: str = self.cleaned_data["email"].strip().lower()
        validate_email_format(email)
        return email

    def clean_phone(self: "RegistrationForm") -> str:
        phone: str = self.cleaned_data["phone"].strip()
        validate_phone_format(phone)
        return phone

    def clean_role(self: "RegistrationForm") -> str:
        role: str = self.cleaned_data["role"]
        if role == User.Role.ADMIN:
            raise forms.ValidationError("Admin users must be created by an administrator.")
        return role

    def clean(self: "RegistrationForm") -> dict[str, object]:
        cleaned_data: dict[str, object] = super().clean()
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self: "RegistrationForm", commit: bool = True) -> User:
        user: User = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email: forms.EmailField = forms.EmailField()
    password: forms.CharField = forms.CharField(widget=forms.PasswordInput)