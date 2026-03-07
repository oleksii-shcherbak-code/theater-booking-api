from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),

    # Plays domain
    path("api/", include("plays.urls")),

    # Schedule domain
    path("api/", include("schedule.urls")),
]
