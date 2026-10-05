from django.urls import path
from recruitments import views

urlpatterns: list[object] = [
    path("candidates/", views.candidate_list, name="candidate_list"),
    path("candidates/add/", views.candidate_create, name="candidate_create"),
    path("candidates/<int:pk>/", views.candidate_detail, name="candidate_detail"),
    path("candidates/<int:pk>/edit/", views.candidate_update, name="candidate_update"),
    path("candidates/<int:pk>/delete/", views.candidate_delete, name="candidate_delete"),
    path("candidates/<int:pk>/screen/", views.screen_candidate_view, name="screen_candidate"),
    path("dashboard/", views.dashboard_summary, name="dashboard_summary"),
]