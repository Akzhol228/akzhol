from django import forms
from .models import SolutionProposal

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import CityProblem

class CityProblemForm(forms.ModelForm):
    class Meta:
        model = CityProblem
        fields = ['category', 'title', 'description', 'location', 'collected_amount', 'total_amount']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'collected_amount': forms.TextInput(attrs={'class': 'form-control'}),
            'total_amount': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SolutionProposalForm(forms.ModelForm):
    class Meta:
        model = SolutionProposal
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Опишите свое решение...'}),
        }

class VoteForm(forms.Form):
    solution_id = forms.IntegerField(widget=forms.HiddenInput())
    vote_type = forms.ChoiceField(choices=[('1', 'Upvote'), ('-1', 'Downvote')], widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        self.fields['vote_type'].widget.attrs.update({'class': 'form-check-input'})



class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

from .models import Donation

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['name', 'phone_number', 'amount']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }