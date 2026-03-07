from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["auth"])
class LoginView(TokenObtainPairView):
    schema = AutoSchema()


@extend_schema(tags=["auth"])
class RefreshView(TokenRefreshView):
    schema = AutoSchema()
