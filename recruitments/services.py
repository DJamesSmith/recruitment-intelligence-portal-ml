from collections.abc import Iterable
from django.db import transaction
from recruitments.models import Candidate, ScreeningResult


def skill_matches(candidate: Candidate) -> int:
    candidate_skills: set[str] = {
        skill.strip().lower()
        for skill in candidate.skills.split(",")
        if skill.strip()
    }
    role_skills: set[str] = {
        skill.strip().lower()
        for skill in candidate.applied_role.required_skills.split(",")
        if skill.strip()
    }
    return len(candidate_skills & role_skills)


def calculate_screening_score(candidate: Candidate) -> float:
    score: float = 0.0
    if candidate.experience_months >= candidate.applied_role.min_experience_months:
        score += 40.0
    score += min(skill_matches(candidate) * 15.0, 45.0)
    if candidate.notice_period_days <= 30:
        score += 10.0
    if candidate.resume_text.strip():
        score += 5.0
    return min(score, 100.0)


@transaction.atomic
def screen_candidate(candidate: Candidate) -> ScreeningResult:
    score: float = calculate_screening_score(candidate)
    if score >= 70:
        status: str = Candidate.ScreeningStatus.SHORTLISTED
    elif score >= 50:
        status = Candidate.ScreeningStatus.WAITLISTED
    else:
        status = Candidate.ScreeningStatus.REJECTED

    reason: str = f"Rule-based score: {score:.2f}"
    candidate.screening_status = status
    candidate.save(update_fields=["screening_status", "updated_at"])

    result: ScreeningResult
    result, _ = ScreeningResult.objects.update_or_create(
        candidate=candidate,
        defaults={"score": score, "status": status, "reason": reason},
    )
    return result


def screen_candidates(candidates: Iterable[Candidate]) -> int:
    count: int = 0
    for candidate in candidates:
        screen_candidate(candidate)
        count += 1
    return count