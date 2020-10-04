from rest_framework import serializers
from BlogApi.models import Post, Comment, UserBlog


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'text', 'published_date')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('text',)


class UserCreationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    class Meta:
        Model = UserBlog
        fields = ("username", "email", "password1", "password2")

