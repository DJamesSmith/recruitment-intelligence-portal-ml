from django import forms

from recruitments.models import Candidate


class CandidateForm(forms.ModelForm):
    class Meta:
        model: type[Candidate] = Candidate
        fields: list[str] = [
            "name",
            "email",
            "phone",
            "college",
            "applied_role",
            "skills",
            "experience_months",
            "notice_period_days",
            "expected_salary",
            "resume_text",
            "portfolio_url",
            "resume_file",
            "profile_image",
            "historical_selection_status",
        ]
