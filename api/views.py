from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {"message": "Hello, World!"}
        return Response(content)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        if user.is_teacher:
            return Response(
                {"token": token.key, "user_id": user.pk, "usertype": "teacher"}
            )
        elif user.is_student:
            return Response(
                {"token": token.key, "user_id": user.pk, "usertype": "student"}
            )
        return Response({"token": token.key, "user_id": user.pk, "usertype": None})

