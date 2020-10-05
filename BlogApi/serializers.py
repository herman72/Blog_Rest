from rest_framework import serializers
from BlogApi.models import Post, Comment, UserBlog


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'text')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('text', 'post')


class UserCreationSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(required=True)
    password1 = serializers.CharField(required=True, max_length=255)
    password2 = serializers.CharField(required=True, max_length=255)

    class Meta:
        Model = UserBlog
        fields = ("username", "email", "password1", "password2")
