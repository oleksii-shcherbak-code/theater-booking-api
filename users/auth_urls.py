from django.urls import path

from users.auth_views import LoginView, RefreshView

urlpatterns = [
    path("login/", LoginView.as_view(), name="token_obtain_pair"),
    path("refresh/", RefreshView.as_view(), name="token_refresh"),
]
