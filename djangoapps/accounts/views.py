import json
import jwt

from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework import status, exceptions

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_exempt


class UserInfoView(views.APIView):

    # permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        user = self.request.user
        """
        auth = get_authorization_header(self.request).split()
        print "auth" , auth
        if not auth or auth[0].lower() != b'token':
            return Response({"Error": "Incorrect token"})

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header'
            raise exceptions.AuthenticationFailed(msg)

        """
        data = {
            "data": {
                "roles": []
            }
        }

        if user.is_superuser:
            data["data"]["roles"].append("admin")

        return Response(data)


class UserLoginView(views.APIView):

    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        if not request.data:
            return Response({'Error': "Please provide username/password"}, status="400")

        username = request.data['username']
        password = request.data['password']

        #user = authenticate(username=username, password=password)
        user = None
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'Error': "Invalid username"}, status="200")

        if not user.check_password(password):
            return Response({'Error': "Invalid password"}, status="200")
        #if user is not None:
        #    return Response({'Error': "Invalid username/password"}, status="200")
        if not user.is_active:
            return Response({'Error': "User not active"}, status="200")
        # login(request, user)

        """
        try:
            #user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'Error': "Invalid username"}, status="200")

        if user:
            if not user.check_password(password):
                return Response({'Error': "Invalid password"}, status="200")
        """

        payload = {
            'id': user.id,
            'email': user.email,
        }
        jwt_token = {'token': jwt.encode(payload, "SECRET_KEY")}

        return Response(
            {"data": jwt_token},
            status=200,
            content_type="application/json"
            )
        """
        else:
            return Response(
                {'Error': "Invalid credentials"},
                status=400,
                content_type="application/json"
            )
        """

