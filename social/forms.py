from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile, Post, Comment


class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create password'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile

        fields = [
            'bio',
            'profile_photo',
            'location'
            ]

        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write something about yourself'
            }),
            'profile_photo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'id': 'profilePhotoInput'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your location'
            }),
        }


class PostForm(forms.ModelForm):

    class Meta:
        model = Post

        fields = [
            'content',
            'post_image',
        ]

        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'What is on your mind?'
            }),
            'post_image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment

        fields = [
            'text'
        ]

        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Write a comment...'
            }),
        }

class EditPostForm(forms.ModelForm):

    class Meta:
        model = Post

        fields = [
            'content',
            'post_image'
        ]

        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Edit your post...'
            }),
            'image': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional image URL'
            }),
        }