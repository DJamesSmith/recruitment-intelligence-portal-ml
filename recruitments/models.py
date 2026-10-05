from django.conf import settings
from django.db import models

from accounts.validators import validate_phone_format
from recruitments.validators import validate_non_negative


class JobRole(models.Model):
    name: models.CharField = models.CharField(max_length=100, unique=True)
    description: models.TextField = models.TextField(blank=True)
    required_skills: models.TextField = models.TextField(blank=True)
    min_experience_months: models.PositiveIntegerField = models.PositiveIntegerField(default=0)
    is_active: models.BooleanField = models.BooleanField(default=True)

    class Meta:
        ordering: list[str] = ["name"]

    def __str__(self: "JobRole") -> str:
        return self.name


class Candidate(models.Model):
    class ScreeningStatus(models.TextChoices):
        PENDING: str = "PENDING", "Pending"
        SHORTLISTED: str = "SHORTLISTED", "Shortlisted"
        WAITLISTED: str = "WAITLISTED", "Waitlisted"
        REJECTED: str = "REJECTED", "Rejected"

    name: models.CharField = models.CharField(max_length=150)
    email: models.EmailField = models.EmailField(unique=True)
    phone: models.CharField = models.CharField(max_length=20, validators=[validate_phone_format])
    college: models.CharField = models.CharField(max_length=200)
    applied_role: models.ForeignKey = models.ForeignKey(JobRole, on_delete=models.PROTECT, related_name="candidates")
    skills: models.TextField = models.TextField(blank=True)
    experience_months: models.IntegerField = models.IntegerField(default=0, validators=[validate_non_negative])
    notice_period_days: models.IntegerField = models.IntegerField(default=0, validators=[validate_non_negative])
    expected_salary: models.DecimalField = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[validate_non_negative])
    resume_text: models.TextField = models.TextField(blank=True)
    portfolio_url: models.URLField = models.URLField(blank=True)
    resume_file: models.FileField = models.FileField(upload_to="resumes/", blank=True)
    profile_image: models.ImageField = models.ImageField(upload_to="images/", blank=True)
    historical_selection_status: models.CharField = models.CharField(max_length=50, blank=True)
    screening_status: models.CharField = models.CharField(max_length=20, choices=ScreeningStatus.choices, default=ScreeningStatus.PENDING)
    created_by: models.ForeignKey = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_candidates")
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: list[str] = ["-created_at"]
        indexes: list[models.Index] = [
            models.Index(fields=["email"]),
            models.Index(fields=["applied_role", "screening_status"])]

    def __str__(self: "Candidate") -> str:
        return f"{self.name} - {self.email}"


class ApplicationBatch(models.Model):
    class Status(models.TextChoices):
        PENDING: str = "PENDING", "Pending"
        PROCESSING: str = "PROCESSING", "Processing"
        COMPLETED: str = "COMPLETED", "Completed"
        FAILED: str = "FAILED", "Failed"

    uploaded_by: models.ForeignKey = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="application_batches")
    file_name: models.CharField = models.CharField(max_length=255)
    total_rows: models.PositiveIntegerField = models.PositiveIntegerField(default=0)
    accepted_rows: models.PositiveIntegerField = models.PositiveIntegerField(default=0)
    rejected_rows: models.PositiveIntegerField = models.PositiveIntegerField(default=0)
    status: models.CharField = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    error_message: models.TextField = models.TextField(blank=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: list[str] = ["-created_at"]

    def __str__(self: "ApplicationBatch") -> str:
        return self.file_name


class ScreeningResult(models.Model):
    candidate: models.OneToOneField = models.OneToOneField(Candidate, on_delete=models.CASCADE, related_name="screening_result")
    score: models.FloatField = models.FloatField(default=0)
    status: models.CharField = models.CharField(max_length=20, choices=Candidate.ScreeningStatus.choices)
    reason: models.TextField = models.TextField(blank=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: list[str] = ["-score"]

    def __str__(self: "ScreeningResult") -> str:
        return f"{self.candidate.name} - {self.score:.2f}"