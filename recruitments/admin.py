from django.contrib import admin
from recruitments.models import ApplicationBatch, Candidate, JobRole, ScreeningResult


@admin.register(JobRole)
class JobRoleAdmin(admin.ModelAdmin):
    list_display: tuple = ("name", "min_experience_months", "is_active")
    list_filter: tuple = ("is_active",)
    search_fields: tuple = ("name", "required_skills")
    fieldsets: tuple = (
        ("Role", {"fields": ("name", "description", "required_skills")}),
        ("Requirements", {"fields": ("min_experience_months", "is_active")}),)


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display: tuple = (
        "name",
        "email",
        "applied_role",
        "experience_months",
        "screening_status",
        "created_at",)
    list_filter: tuple = ("screening_status", "applied_role")
    search_fields: tuple = ("name", "email", "skills", "college")
    ordering: tuple = ("-created_at",)


@admin.register(ApplicationBatch)
class ApplicationBatchAdmin(admin.ModelAdmin):
    list_display: tuple = (
        "file_name",
        "uploaded_by",
        "status",
        "total_rows",
        "accepted_rows",
        "rejected_rows",
        "created_at",
    )
    list_filter: tuple = ("status",)
    search_fields: tuple = ("file_name", "uploaded_by__email")


@admin.register(ScreeningResult)
class ScreeningResultAdmin(admin.ModelAdmin):
    list_display: tuple = ("candidate", "score", "status", "created_at")
    list_filter: tuple = ("status",)
    search_fields: tuple = ("candidate__name", "candidate__email")