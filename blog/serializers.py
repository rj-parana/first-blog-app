from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import Post, User, Category, Comment, Reply


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'author', 'category', 'tag', 'thumbnail', 'image', 'text']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['comment', 'name', 'email', 'content']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "mobile", "city", "country", "password1", "password2"]


# class SignUpForm(UserCreationForm):

#     password1 = forms.CharField(widget=forms.PasswordInput())
#     password2 = forms.CharField(widget=forms.PasswordInput())

#     class Meta:
#         model = User
#         fields = ("first_name", "last_name", "username", "email", "mobile", "city", "country", "password1", "password2")


# class LogInForm(forms.Form):
    
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)