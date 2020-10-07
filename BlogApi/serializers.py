from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from BlogApi.models import Post, Comment, UserBlog


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'text']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text', 'post']


class UserCreationSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(required=True)
    password1 = serializers.CharField(required=True, max_length=255)
    password2 = serializers.CharField(required=True, max_length=255)

    class Meta:
        model = UserBlog
        fields = ['username', 'email', 'password1', 'password2']

    def validate(self, data):

        if data['password1'] != data['password2']:
            raise serializers.ValidationError("no same pass")
        else:
            return data


class UserSerializer(serializers.ModelSerializer):
    # posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())

    class Meta:
        model = UserBlog
        fields = [ 'username']
