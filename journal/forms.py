from django import forms
from allauth.account.forms import SignupForm


class CustomSignupForm(SignupForm):
    """Custom signup form with email and password fields (no username)."""
    
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email address',
            'autocomplete': 'email',
            'class': 'form-control',
        }),
        required=True,
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Remove username field completely
        if 'username' in self.fields:
            del self.fields['username']
        
        # Customize password fields
        self.fields['password1'].label = 'Password'
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Create a password',
            'autocomplete': 'new-password',
            'class': 'form-control',
        })
        
        self.fields['password2'].label = 'Confirm Password'
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm your password',
            'autocomplete': 'new-password',
            'class': 'form-control',
        })
        
        # Update email field attributes
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Enter your email address',
            'autocomplete': 'email',
            'class': 'form-control',
        })
        
        # Remove help texts
        for field_name in self.fields:
            self.fields[field_name].help_text = ''
    
    def save(self, request):
        """Save user with email as the primary identifier."""
        user = super().save(request)
        # Set username to email (for Django compatibility)
        if not user.username:
            user.username = user.email.split('@')[0]  # Use email prefix as username
            user.save()
        return user
