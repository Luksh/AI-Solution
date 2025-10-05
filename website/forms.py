from django import forms
from .models import ContactInquiry, Testimonial

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

class TestimonialForm(forms.ModelForm):
    """Form for customer testimonials"""
    class Meta:
        model = Testimonial
        fields = ['customer_name', 'company', 'position', 'testimonial', 'rating', 'image']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Company Name'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Job Title'}),
            'testimonial': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Share your experience with our AI solutions...', 'rows': 4}),
            'rating': forms.Select(choices=[(i, f'{i} Star{"s" if i != 1 else ""}') for i in range(1, 6)], attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
        labels = {
            'customer_name': 'Full Name',
            'company': 'Company',
            'position': 'Job Title',
            'testimonial': 'Your Experience',
            'rating': 'Rating',
            'image': 'Your Photo (Optional)',
        }

class LoginForm(forms.Form):
    """Form for admin login"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
