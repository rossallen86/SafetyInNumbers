from django import forms
from safety_in_numbers.models import SafetyInUser, Transit


class SafetyInUserForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name ', max_length=30, required=False)
    last_name = forms.CharField(label='Last Name ', max_length=150, required=False)
    username = forms.CharField(label='Username ', max_length=150)
    email = forms.EmailField(label='Email ', max_length=90)
    telephone = forms.CharField(label='Telephone ', max_length=15, required=False)
    is_volunteer = forms.BooleanField(label='Is Volunteer ', required=False)

    class Meta:
        model = SafetyInUser
        fields = ['first_name', 'last_name', 'username', 'email', 'telephone', 'is_volunteer']


class TransitForm(forms.ModelForm):
    date = forms.DateField(label='Date ', widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(label='Time ', widget=forms.TimeInput(attrs={'type': 'time'}))
    starting_address = forms.CharField(label='Start Address', max_length=50)
    ending_address = forms.CharField(label='End Address', max_length=50)
    comments = forms.CharField(label='Comments', max_length=140)

    class Meta:
        model = Transit
        fields = ['date', 'time', 'starting_address', 'ending_address', 'comments']


class EmailForm(forms.Form):
    from_email = forms.EmailField(max_length=90, disabled=True, required=False)
    to_email = forms.EmailField(max_length=90)
    subject = forms.CharField(max_length=50)
    body = forms.CharField(max_length=500, widget=forms.Textarea())