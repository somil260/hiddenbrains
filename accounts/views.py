import uuid


from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.core.mail import EmailMessage
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework import generics, mixins

from .models import ResetPasswordModel
from .serializers import LoginSerializer, SignupSerializer,\
    SetPasswordSerializer, ResetPasswordSerializer


class Login(APIView):
    template_name = 'accounts/login.html'
    serializer_class = LoginSerializer

    def get(self, request):
        return Response({'serializer': self.serializer_class()})

    def post(self, request):
        response_data = dict()
        password = request.POST.get('password')
        username = request.POST.get('username')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if request.accepted_renderer.format == 'html':
                return HttpResponseRedirect('/')
            response_data['token'] = user.auth_token.key
            return Response(response_data, status=status.HTTP_200_OK)
        response_data['error'] = "Username or password not matched"
        return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)


class Signup(APIView):
    template_name = 'accounts/signup.html'
    serializer_class = SignupSerializer

    def get(self, request):
        return Response({'serializer': self.serializer_class()})

    def post(self, request):
        response_data = dict()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = EmailMessage('welcome', 'You have sign up successfully',
                                   to=[request.POST.get('email')],
                                   from_email=getattr(settings, DEFAULT_EMAIL_FROM))

            return Login().post(request)
        response_data['error'] = serializer.errors
        return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)


class SetPassword(APIView):
    template_name = 'accounts/setpassword.html'
    serializer_class = SetPasswordSerializer

    def get(self, request, user_id=None):
        return Response({'serializer': self.serializer_class()})

    def post(self, request, user_id=None):
        user = User.objects.get(id=user_id)
        serializer = SetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            if user.check_password(serializer.data['old_password']):
                user.set_password(serializer.data['new_password'])
                user.save()

                if request.accepted_renderer.format == 'html':
                    return HttpResponseRedirect('/')
                return Response({'status': 'password set'})
            else:
                return Response({'status': 'old password Not matched'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(APIView):
    template_name = 'accounts/resetpassword.html'
    serializer_class = ResetPasswordSerializer

    def get(self, request, *args, **kwargs):
        # import pdb;pdb.set_trace()
        if kwargs.get('user_id'):
            return Response({'serializer': self.serializer_class(
                            context={'user_id': kwargs.get('user_id'),
                                     'uid': str(kwargs.get('uid'))})},
                            template_name='accounts/resetpassword_template.html')

        return Response({'serializer': self.serializer_class()})

    def post(self, request, *args, **kwargs):
        user = User.objects.filter(email=request.POST.get('email'))
        if user.exists():
            resetpw_obj = ResetPasswordModel.objects.create(user=user.first())
            message = EmailMessage('change password',
                                   request.build_absolute_uri()+str(resetpw_obj.user.id) +
                                   '/'+str(resetpw_obj.uid)+'/',
                                   to=[resetpw_obj.user.email],
                                   from_email=getattr(settings, 'DEFAULT_EMAIL_FROM'))
            return Response({'status': 'password set'})
        else:
            user = User.objects.filter(id=kwargs.get('user_id'))
            rpm_obj = ResetPasswordModel.objects.filter(user__id=kwargs.get('user_id'),
                                                                         uid=kwargs.get('uid'))
            serializer = ResetPasswordSerializer(data=request.data)
            if serializer.is_valid() and rpm_obj.exists():
                user.first().set_password(serializer.data['new_password'])
                user.first().save()
                return Response({'status': 'password set'})
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)


def index(request):
    return render(request, 'accounts/index.html')
