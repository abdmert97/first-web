from django import forms
from django.contrib.auth.models import User
from basic_app.models import UserInfo, Player, Team

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password')

class PlayerForm(forms.ModelForm):
    student_id = forms.CharField(min_length=7, max_length=7,required=True)
    class Meta:
        model = Player
        exclude = ['team',]


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        exclude = ['admin_usr',]