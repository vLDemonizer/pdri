from django import forms
from ambiental.models import Project, CD, RatingElement, UserProfile

WDI = (      # Weighting Designation Options
    ('H', 'High-Priority'),
    ('P', 'Pro-Rated'),)
MVI = (      # Maturity Value Options
    ('1', 'Slow'),
    ('2', 'Kinda Slow'),
    ('3', 'Okay'),
    ('4', 'Fastish'),
    ('5', 'Fast'),
    ('N/A', 'Not Assigned'),)

class RatingElementForm(forms.Form):
    index = forms.CharField(
        label='Index',
        required=False,
        widget=forms.TextInput(attrs={'size': '1'}),
    )
    name = forms.CharField(
        label='Rating Element',
        required=False,
    )
    wd = forms.ChoiceField(
        label='Weighting Designation',
        choices=WDI,
        required=True,
        widget=forms.TextInput(attrs={'size': '3'}),
    )
    wf = forms.DecimalField(
        label='Weighting Factor',
        required=True,
        max_value=10.00,
        widget=forms.TextInput(attrs={'size': '3'}),
    )
    mv = forms.ChoiceField(
        label='Maturity Value',
        required=True,
        choices=MVI,
        widget=forms.TextInput(attrs={'size': '3'}),
    )
    score = forms.DecimalField(
        label='Score',
        required=True,
        max_value=99.00,
        widget=forms.TextInput(attrs={'size': '3'}),
    )
    comment = forms.CharField(
        label='Comment',
        required=False,
        widget=forms.Textarea(),
    )

class ProjectForm(forms.Form):
    name = forms.CharField(
        label="Project's Title",
        required=False,
        widget=forms.TextInput(attrs={'size': '10'}),
    )
    description = forms.CharField(
        label="Description",
        required=False,
        widget=forms.Textarea(),
        )

class UserProfileForm(forms.Form):
    username = forms.CharField(
        label="Username",
        required=True,
    )
    first_name = forms.CharField(
        label="First Name",
        required=False,
    )
    last_name = forms.CharField(
        label="Last Name",
        required=False,
    )
    password = forms.CharField(
        label="Password",
        required=True,
        widget=forms.PasswordInput(),
    )
    email = forms.EmailField(
        label="Email",
        required=True,
    )
    company = forms.CharField(
        label="Company",
        required=False,
    )

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        required=True,
    )
    password = forms.CharField(
        label="Password",
        required=True,
        widget=forms.PasswordInput(),
    )
