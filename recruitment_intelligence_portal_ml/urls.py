from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('recruitments/', include('recruitments.urls')),
    path('interviews/', include('interviews.urls')),
    path('ingestion/', include('ingestion.urls')),
    path('ml-engine/', include('ml-engine.urls')),
    path('nlp-engine/', include('nlp-engine.urls')),
    path('dl-engine/', include('dl-engine.urls')),
]