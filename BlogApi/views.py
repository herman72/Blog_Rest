from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.decorators import method_decorator
from rest_framework import status, mixins, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from BlogApi.models import Post, UserBlog
from django.shortcuts import render, redirect
from rest_framework.parsers import JSONParser
from BlogApi.serializers import PostSerializer, UserCreationSerializer, UserSerializer, LoginSerializer
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt


# class PostList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
class PostList(generics.GenericAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    @method_decorator(login_required(login_url='', redirect_field_name=''))
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = Post.objects.create(author=request.user, title=serializer.validated_data['title'],
                                       text=serializer.validated_data['text'])

            # serializer.author = request.data['author']
            post.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(generics.GenericAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Register(generics.GenericAPIView):
    serializer_class = UserCreationSerializer
    queryset = UserBlog.objects.all()

    # def get(self, request, format=None):
    #     serializer = UserCreationSerializer()
    #
    #     return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserCreationSerializer(data=request.data)

        if serializer.is_valid():
            user = UserBlog.objects.create(username=serializer.validated_data['username'])
            user.email = serializer.validated_data['email']
            user.password = make_password(serializer.validated_data['password1'])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(generics.ListAPIView):
    queryset = UserBlog.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = UserBlog.objects.all()
    serializer_class = UserSerializer


class UserLogin(generics.GenericAPIView):
    serializer_class = LoginSerializer
    queryset = UserBlog.objects.all()

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = UserBlog.objects.get(username=serializer.validated_data['username'])
            login(request, user)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:

            return Response(serializer.errors, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class Logout(generics.GenericAPIView):
    # @method_decorator(login_required(login_url='/login/?next=/logout', redirect_field_name=''))
    def get(self, request):
        logout(request)

        return Response(status=status.HTTP_202_ACCEPTED)

# @api_view(['GET', 'POST'])
# def post_list(request, format=None):
#     if request.method == 'GET':
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#
#         serializer = PostSerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def post_detail(request, pk, format=None):
#     try:
#         post = Post.objects.get(pk=pk)
#     except Post.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = PostSerializer(post, data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
