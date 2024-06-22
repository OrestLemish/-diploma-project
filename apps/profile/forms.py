from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.forms import ModelForm, EmailInput, PasswordInput
from django.utils.translation import gettext_lazy as _

from apps.profile.models import Profile

class RegisterForm(UserCreationForm):
    email = forms.CharField(widget=EmailInput)
    # phone = forms.IntegerField(widget=PhoneNumberInputWidget)

    # image = forms.ImageField(widget=ImageSelect,)

    class Meta:
        model = Profile
        fields = ["username", "email", "password1", "password2", ]

    # def clean_email(self):
    #     email_value = self.cleaned_data['email']
    #     email = self.Meta.model.objects.filter(email=email_value)
    #
    #     if email:
    #         raise ValidationError(_('email_already_exists'))
    #     if not validate_email(email_value):
    #         raise ValidationError(_('email_not_valid'))
    #
    #     return email_value

    # def clean_phone(self):
    #     phone_value = self.cleaned_data['phone']
    #     phone = self.Meta.model.objects.filter(phone=phone_value)
    #
    #     if phone:
    #         raise ValidationError(_('phone_already_exists'))
    #     if not validate_phone(str(phone_value)):
    #         raise ValidationError(_('phone_not_valid'))
    #
    #     return phone_value

    def clean_password(self):
        password = self.cleaned_data['password']
        password_confirm = self.data['password_confirm']
        if len(password) < 5:
            raise ValidationError(_('password_min_letters_5'))
        if password != password_confirm:
            raise ValidationError(_('passwords_do_not_match'))

        return password
