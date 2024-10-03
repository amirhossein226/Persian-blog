from django import forms
from account.models import Profile
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label='رمز عبور'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label='تکرار رمز عبور'
    )

    class Meta:
        model = UserModel
        fields = [
            'first_name',
            'last_name',
            'email',
            'username'
        ]

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError(
                'هر دو فیلد مربوط به رمز عبور باید مقادیر یکسانی داشته باشند.')
        return cd['password2']

    # since users are able to login with both username and email, we check to see if the user with same email already exists or not
    # the uniqueness for username already is handling by django(by default) then there is no need to check existence of username
    def clean_email(self):
        cd = self.cleaned_data
        user = UserModel.objects.filter(email=cd['email']).exists()
        if user:
            raise forms.ValidationError(
                'در حال حاضر حسابی کاربری با همین ایمیل موجود می باشد.')
        return cd['email']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]
    # the users are able to change their information's which which their account is created with them,
    # because of this, we don't allow them to define the same email as another user's email when they
    # want to change their information

    def clean_email(self):
        email = self.cleaned_data['email']
        duplicate = UserModel.objects.filter(
            email=email
        ).exclude(
            id=self.instance.id
        ).exists()

        if duplicate:
            raise forms.ValidationError(
                'ایمیلی با همین آدرس، موجود می باشد.')

        return email


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'photo'
        ]
