from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Tell us your email address so we can verify it.")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")
