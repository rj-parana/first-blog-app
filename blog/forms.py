from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, User, Category, Comment, Reply

choices = Category.objects.all().values_list('name','name') 
choice_list = []

for item in choices:
    choice_list.append(item)

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'author', 'category', 'tag', 'thumbnail', 'image', 'text')


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('name', 'email', 'content')

class ReplyForm(forms.ModelForm):

    class Meta:
        model = Reply
        fields = ('comment', 'name', 'email', 'content')
    

class SignUpForm(UserCreationForm):
    
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "mobile", "city", "country", "password1", "password2")


class LogInForm(forms.Form):
    
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)