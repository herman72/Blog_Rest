from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.decorators import method_decorator
from rest_framework import status, mixins, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from BlogApi.models import Post, UserBlog, Comment
from django.shortcuts import render, redirect
from rest_framework.parsers import JSONParser

from BlogApi.permissions import IsOwnerOrReadOnly
from BlogApi.serializers import PostSerializer, UserCreationSerializer, UserSerializer, LoginSerializer, \
    CommentSerializer, FollowSerializer
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt


class PostList(generics.GenericAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = Post.objects.create(author=request.user, title=serializer.validated_data['title'],
                                       text=serializer.validated_data['text'])

            post.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(generics.GenericAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

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

    def post(self, request, format=None):
        serializer = UserCreationSerializer(data=request.data)

        if serializer.is_valid():
            user = UserBlog.objects.create(username=serializer.validated_data['username'])
            user.email = serializer.validated_data['email']
            user.password = make_password(serializer.validated_data['password1'])
            user.save()
            return Response(status=status.HTTP_201_CREATED)
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
            return Response(status=status.HTTP_202_ACCEPTED)
        else:

            return Response(serializer.errors, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class Logout(generics.GenericAPIView):

    def get(self, request):
        logout(request)

        return Response(status=status.HTTP_202_ACCEPTED)


class AddComment(generics.GenericAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = CommentSerializer(post.comments, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = CommentSerializer(data=request.data)
        post = get_object_or_404(Post, pk=pk)
        if serializer.is_valid():
            comment = Comment.objects.create(author_comment=request.user, post=post)
            comment.text = serializer.validated_data['text']

            comment.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class FollowerList(generics.GenericAPIView):
    serializer_class = FollowSerializer
    queryset = UserBlog.objects.all()

    def get(self, request, pk):
        user = get_object_or_404(UserBlog, pk=pk)
        serializer = FollowSerializer(user)
        return Response(serializer.data)

    def post(self, request, pk):
        user = get_object_or_404(UserBlog, pk=pk)

        serializer = FollowSerializer(data=request.data)
        if request.user == user:
            if serializer.is_valid():
                user.following.add(serializer.validated_data['following'][0])
                user.save()
            else:
                Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):

        user = get_object_or_404(UserBlog, pk=pk)
        serializer = FollowSerializer(data=request.data)
        if request.user == user:
            if serializer.is_valid():
                user.following.remove(serializer.validated_data['following'][0])
                user.save()
            else:
                Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
