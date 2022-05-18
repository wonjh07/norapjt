from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django import forms

# 수정 필요

class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
    password = None

    username = forms.CharField(
        label ="이름",
        widget=forms.TextInput(
            attrs={
                'class': "input"
            }
        )
    )

    email = forms.CharField(
        label ="EMAIL",
        widget=forms.TextInput(
            attrs={
                'class': "input"
            }
        )
    )

    nickname = forms.CharField(
        label ="닉네임",
        widget=forms.TextInput(
            attrs={
                'class': "input"
            }
        )
    )
    class Meta:
        model = get_user_model() 
        fields = ('username', 'nickname','email')


class CustomUserCreationform(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'nickname', 'email', 'password1', 'password2')