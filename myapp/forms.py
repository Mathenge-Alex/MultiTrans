from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model

)

User = get_user_model()



class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email Address')
    email2 = forms.EmailField(label='Re-Enter Email Address')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password'
        ]

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            raise forms.ValidationError("Your Emails Didn't Match")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError(
                "Email address Has Already Been Taken")
        return super(UserRegisterForm, self).clean(*args, **kwargs)


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user has not been authenticated')
            if not user.check_password(password):
                raise forms.ValidationError('You Have Entered an Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is inactive')
        return super(UserLoginForm, self).clean(*args, **kwargs)

