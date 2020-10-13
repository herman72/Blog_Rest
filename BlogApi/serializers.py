from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from BlogApi.models import Post, Comment, UserBlog


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    comments = serializers.SlugRelatedField(many=True, slug_field='text', read_only=True)

    class Meta:
        model = Post
        fields = ['title', 'text', 'author', 'comments']
        # read_only_fields = ['author']


class CommentSerializer(serializers.ModelSerializer):
    author_comment = serializers.ReadOnlyField(source='author_comment.username')

    class Meta:
        model = Comment
        fields = ['text', 'author_comment']


class UserCreationSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(required=True)
    password1 = serializers.CharField(required=True, max_length=255, style={'input_type': 'password'})
    password2 = serializers.CharField(required=True, max_length=255, style={'input_type': 'password'})

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
        fields = ['username', 'email']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=255)
    password = serializers.CharField(required=True, max_length=255, style={'input_type': 'password'})

    def validate(self, data):

        try:
            user = UserBlog.objects.get(username=data['username'])

            if user.check_password(data['password']):
                return data
            else:

                raise serializers.ValidationError('Pass incorrect')

        except UserBlog.DoesNotExist:

            raise serializers.ValidationError("no user")
