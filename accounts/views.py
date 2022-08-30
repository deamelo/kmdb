from rest_framework.views import APIView, Request, Response, status
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import APIException

from  django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

from .models import Account
from .permissions import IsCritic
from .serializers import AccountSerializer, LoginSerializer


class OwnerOnlyError(APIException):
    status_code = 403


class RegisterView(APIView):
    def post(self, request: Request) -> Response:
        serializer = AccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class ListAllUsersView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request: Request) -> Response:
        user = Account.objects.all()
        result_page = self.paginate_queryset(user, request, view=self)

        serializer = AccountSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)


class ListOneUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser | IsCritic ]

    def get(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(Account, id=user_id)

        serializer = AccountSerializer(user)

        if not request.user.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif request.user.is_superuser:
            return Response(serializer.data)
        elif user.is_critic and user.id == request.user.id:
            return Response(serializer.data)

        raise OwnerOnlyError({"detail": "You do not have permission to perform this action."})


class LoginView(APIView):
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        if not user:
            return Response(
                {"detail": "invalid credentials"}, status.HTTP_400_BAD_REQUEST
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key})
