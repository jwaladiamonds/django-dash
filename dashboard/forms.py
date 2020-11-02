
from accounts.models import User
from django import forms

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'bio', 'birthday', 'picture']
        widgets = {
            'picture': forms.ClearableFileInput(attrs={ 'class': 'form-control mb-3', 'placeholder': 'Profile Picture'}),
        }
