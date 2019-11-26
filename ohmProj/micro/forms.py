from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.core.mail import send_mail
from django.forms import TextInput
from .models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    telephone = forms.CharField(max_length=10)

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'telephone', 'password1', 'password2']

class OTPAuthenticationForm(AuthenticationForm):
    otp = forms.CharField(required=False, widget=forms.PasswordInput)

    def clean(self):
        # Allow Django to detect can user log in
        super(OTPAuthenticationForm, self).clean()

        # If we got this far, we know that user can log in.
        if self.request.session.has_key('_otp'):
            if self.request.session['_otp'] != self.cleaned_data['otp']:
                raise forms.ValidationError("Invalid OTP.")
            del self.request.session['_otp']
        else:
            # There is no OTP so create one and send it by email
            otp = "1234"
            send_mail(
                subject="Your OTP Password",
                message="Your OTP password is %s" % otp,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[self.user_cache.email]
            )
            self.request.session['_otp'] = otp
            # Now we trick form to be invalid
            raise forms.ValidationError("Enter OTP you received via e-mail")