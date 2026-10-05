from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.validators import validate_phone_format


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN: str = "ADMIN", "Admin"
        HR: str = "HR", "HR"
        INTERVIEWER: str = "INTERVIEWER", "Interviewer"

    username: None = None
    email: models.EmailField = models.EmailField(unique=True)
    phone: models.CharField = models.CharField(max_length=20, blank=True, validators=[validate_phone_format])
    role: models.CharField = models.CharField(max_length=20, choices=Role.choices, default=Role.HR)
    is_email_verified: models.BooleanField = models.BooleanField(default=False)

    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: list[str] = []

    def __str__(self: "User") -> str:
        return self.email


class EmailOTP(models.Model):
    user: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE, related_name="email_otps")
    code: models.CharField = models.CharField(max_length=6)
    expires_at: models.DateTimeField = models.DateTimeField()
    is_used: models.BooleanField = models.BooleanField(default=False)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering: list[str] = ["-created_at"]

    def __str__(self: "User") -> str:
        return f"{self.user.email} - {self.code}"
