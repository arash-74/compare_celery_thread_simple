from django import forms

from compare.models import User


class SignInForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')


class ResetForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput)
