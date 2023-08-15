from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


User = get_user_model()

class CustomLoginForm(forms.ModelForm):
    email = forms.CharField(label='Email', max_length=254)

    class Meta:
        model = User
        fields = ['email', 'password']

    def clean(self):
        clean_data = super().clean()
        email = clean_data.get('email')
        password = clean_data.get('password')

        if email and password:
            if '@' in email:
                try:
                    user = User.objects.get(email=email)
                    clean_data['username'] = user.username
                except User.DoesNotExist:
                    raise ValidationError('Invalid email or password')
            else:
                clean_data['username'] = email

        return clean_data