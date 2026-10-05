from django import forms

from recruitments.models import Candidate


class CandidateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        self.fields["applied_role"].widget.attrs["class"] = "form-select"

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