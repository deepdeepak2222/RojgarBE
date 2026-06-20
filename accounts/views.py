"""Signup + current-user endpoints. Login/refresh use SimpleJWT's own views."""
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from core.scoping import get_current_client

from .serializers import SignupSerializer


def _tokens_for(user) -> dict:
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


def _client_payload(client) -> dict:
    return {"id": client.id, "name": client.name}


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        body = {**_tokens_for(result["user"]), "client": _client_payload(result["client"])}
        return Response(body, status=status.HTTP_201_CREATED)


class MeView(APIView):
    def get(self, request):
        client = get_current_client(request.user)
        return Response(
            {
                "phone": request.user.username,
                "email": request.user.email,
                "client": _client_payload(client),
            }
        )
