from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User, DonorProfile, PatientRequest
from .models import BloodInventory  
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets
from .models import User


class DonorSignUpForm(UserCreationForm):
    blood_type = forms.ChoiceField(
        choices=BloodInventory.BLOOD_TYPE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
        )
    blood_units = forms.IntegerField(
        min_value=1,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    @transaction.atomic
    def save(self, commit=True):
        try:
            user = super().save(commit=False)
            user.user_type = 'DONOR'
            if commit:
                user.save()
                donor_profile = DonorProfile.objects.create(
                    user=user,
                    blood_type=self.cleaned_data.get('blood_type'),
                    blood_units=self.cleaned_data.get('blood_units'),
                    status='PENDING'
                )
            return user
        except Exception as e:
            # If there's an error, rollback the transaction
            print(f"Error creating donor: {str(e)}")
            raise
    
    def clean(self):
        cleaned_data = super().clean()
        blood_type = cleaned_data.get('blood_type')
        blood_units = cleaned_data.get('blood_units')

        if not blood_type:
            raise forms.ValidationError('Blood type is required.')
        
        if not blood_units:
            raise forms.ValidationError('Blood units is required.')
        
        if blood_units and blood_units < 1:
            raise forms.ValidationError('Blood units must be at least 1.')

        return cleaned_data



class PatientSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'PATIENT'
        if commit:
            user.save()
        return user

class AuthoritySignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'AUTHORITY'
        if commit:
            user.save()
        return user

class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = PatientRequest
        fields = ['blood_type', 'units_required']