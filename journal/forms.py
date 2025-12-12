from django import forms
from allauth.account.forms import SignupForm


class CustomSignupForm(SignupForm):
    """Custom signup form with only username and password fields."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Remove email field from the form
        if 'email' in self.fields:
            del self.fields['email']
        
        # Customize field labels and placeholders
        self.fields['username'].label = 'Username'
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Choose a username',
            'autocomplete': 'username',
        })
        
        self.fields['password1'].label = 'Password'
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Create a password',
            'autocomplete': 'new-password',
        })
        
        self.fields['password2'].label = 'Confirm Password'
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm your password',
            'autocomplete': 'new-password',
        })
        
        # Remove help texts
        for field_name in self.fields:
            self.fields[field_name].help_text = ''
    
    def clean(self):
        """Override clean to set email to empty string for PostgreSQL compatibility"""
        cleaned_data = super().clean()
        # PostgreSQL requires email to be NOT NULL
        # Set to empty string since we don't collect email
        cleaned_data['email'] = ''
        return cleaned_data
