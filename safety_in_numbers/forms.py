from django import forms
from safety_in_numbers.models import SafetyInUser, Transit


class SafetyInUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    username = forms.CharField(max_length=150)
    email = forms.EmailField(max_length=254)
    telephone = forms.CharField(max_length=15, required=False)
    is_volunteer = forms.BooleanField(required=False)

    class Meta:
        model = SafetyInUser
        fields = ['first_name', 'last_name', 'username', 'email', 'telephone', 'is_volunteer']


class TransitForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    starting_address = forms.CharField(max_length=50)
    ending_address = forms.CharField(max_length=50)
    comments = forms.CharField(max_length=140)

    class Meta:
        model = Transit
        fields = ['date', 'time', 'starting_address', 'ending_address', 'comments']