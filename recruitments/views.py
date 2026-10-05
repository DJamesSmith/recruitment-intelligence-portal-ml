from typing import Any

from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Max, Min, QuerySet, Sum
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from accounts.models import User
from recruitments.forms import CandidateForm
from recruitments.models import Candidate, JobRole, ScreeningResult
from recruitments.services import screen_candidate


@login_required
def candidate_list(request: HttpRequest) -> HttpResponse:
    candidates: QuerySet[Candidate] = Candidate.objects.select_related("applied_role")
    search: str = request.GET.get("q", "").strip()
    role: str = request.GET.get("role", "").strip()
    status: str = request.GET.get("status", "").strip()

    if search:
        candidates = candidates.filter(name__icontains=search) | candidates.filter(email__icontains=search) | candidates.filter(skills__icontains=search)
    if role.isdigit():
        candidates = candidates.filter(applied_role_id=int(role))
    if status:
        candidates = candidates.filter(screening_status=status)

    candidates = candidates.order_by("-created_at")[:10]
    return render(
        request,
        "recruitments/candidate_list.html",
        {"candidates": candidates, "roles": JobRole.objects.filter(is_active=True)})


@login_required
def candidate_detail(request: HttpRequest, pk: int) -> HttpResponse:
    candidate: Candidate = get_object_or_404(Candidate, pk=pk)
    return render(request, "recruitments/candidate_detail.html", { "candidate": candidate })


@role_required(User.Role.ADMIN, User.Role.HR)
def candidate_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form: CandidateForm = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            candidate: Candidate = form.save(commit=False)
            candidate.created_by = request.user
            candidate.save()
            return redirect("candidate_detail", pk=candidate.pk)
    else:
        form = CandidateForm()
    return render(request, "recruitments/candidate_form.html", { "form": form })


@role_required(User.Role.ADMIN, User.Role.HR)
def candidate_update(request: HttpRequest, pk: int) -> HttpResponse:
    candidate: Candidate = get_object_or_404(Candidate, pk=pk)
    form: CandidateForm = CandidateForm(request.POST or None, request.FILES or None, instance=candidate)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("candidate_detail", pk=pk)
    return render(request, "recruitments/candidate_form.html", { "form": form })


@role_required(User.Role.ADMIN, User.Role.HR)
def candidate_delete(request: HttpRequest, pk: int) -> HttpResponse:
    candidate: Candidate = get_object_or_404(Candidate, pk=pk)
    candidate.delete()
    return redirect("candidate_list")


@role_required(User.Role.ADMIN, User.Role.HR)
def screen_candidate_view(request: HttpRequest, pk: int) -> HttpResponse:
    candidate: Candidate = get_object_or_404(Candidate, pk=pk)
    result: ScreeningResult = screen_candidate(candidate)
    return render(request, "recruitments/screening_result.html", { "result": result })


@role_required(User.Role.ADMIN, User.Role.HR)
def dashboard_summary(request: HttpRequest) -> HttpResponse:
    summary: dict[str, object] = Candidate.objects.aggregate(
        total=Count("id"),
        total_salary=Sum("expected_salary"),
        minimum_salary=Min("expected_salary"),
        maximum_salary=Max("expected_salary"),
        average_salary=Avg("expected_salary"))
    statuses: list[dict[str, Any]] = list(
        Candidate.objects.values("screening_status")
        .annotate(count=Count("id"))
        .order_by("screening_status"))
    return render(request, "recruitments/dashboard.html", { "summary": summary, "statuses": statuses })