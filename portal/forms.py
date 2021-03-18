import django.forms as forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from portal.models import Profile


class LoginForm(forms.Form):
    login = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'login'})
    )
    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={'placeholder': 'hasło'})
    )


def username_unique(username):
    """
    Raises ValidationError if user object with provided username exists.

    :param username: string
    """
    if User.objects.filter(username=username):
        raise ValidationError("Użytkownik o takim loginie już istnieje!")


def email_unique(email):
    """
    Raises ValidationError if user object with provided email exists.

    :param email: string
    """
    if User.objects.filter(email=email):
        raise ValidationError("Użytkownik o takim emailu już istnieje!")


class SignupForm(forms.Form):
    BUILDINGS = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]

    username = forms.CharField(
        label="",
        validators=[username_unique],
        widget=forms.TextInput(attrs={'placeholder': 'login'})
    )
    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={'placeholder': 'hasło'})
    )
    first_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'imię'})
    )
    last_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'nazwisko'})
    )
    email = forms.EmailField(
        label="",
        validators=[email_unique],
        widget=forms.EmailInput(attrs={'placeholder': 'email'})
    )
    number = forms.IntegerField(
        label="",
        widget=forms.NumberInput(attrs={'placeholder': 'numer mieszkania', 'min': 1, 'max': 50})
    )
    building = forms.CharField(
        label="",
        widget=forms.Select(attrs={'placeholder': 'budynek'}, choices=BUILDINGS)
    )


class NoticeForm(forms.Form):
    topic = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Temat'})
    )
    content = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'placeholder': 'Treść'})
    )


class MessageForm(forms.Form):
    topic = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Temat'})
    )
    content = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'placeholder': 'Treść'})
    )
    recipient = forms.ModelChoiceField(
        label="Odbiorca:",
        queryset=Profile.objects.all(),
        required=False,
        empty_label="Wszyscy użytkownicy",
        initial=0
    )


class PollForm(forms.Form):
    name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Temat'})
    )
    description = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'placeholder': 'Opis'})
    )
    question = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Pytanie'})
    )


class VoteForm(forms.Form):
    VOTES = [('Za', 'Za'), ('Przeciw', 'Przeciw'), ('Wstrzymaj', 'Wstrzymaj')]

    vote = forms.CharField(
        label="",
        widget=forms.Select(attrs={'placeholder': 'Głos'}, choices=VOTES)
    )
