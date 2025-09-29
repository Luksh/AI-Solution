from django import forms
from .models import ContactInquiry

class ContactForm(forms.ModelForm):
    """Form for contact inquiries"""
    class Meta:
        model = ContactInquiry
        fields = ['name', 'email', 'phone', 'company_name', 'country', 'job_title', 'job_details']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone Number'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Company Name'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Country'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Job Title'}),
            'job_details': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Please describe your job requirements', 'rows': 5}),
        }

class LoginForm(forms.Form):
    """Form for admin login"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
