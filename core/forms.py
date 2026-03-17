from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import ContactSubmission, Profile


def _apply_widget_classes(fields):
    for field in fields.values():
        if isinstance(field.widget, forms.CheckboxInput):
            css_class = "form-check-input"
        else:
            css_class = "form-control"
        field.widget.attrs.setdefault("class", css_class)


class AccessibleAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_widget_classes(self.fields)
        self.fields["username"].widget.attrs.setdefault("autocomplete", "username")
        self.fields["password"].widget.attrs.setdefault("autocomplete", "current-password")


class AccessibleUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_widget_classes(self.fields)
        self.fields["username"].widget.attrs.setdefault("autocomplete", "username")
        self.fields["email"].widget.attrs.setdefault("autocomplete", "email")
        self.fields["password1"].widget.attrs.setdefault("autocomplete", "new-password")
        self.fields["password2"].widget.attrs.setdefault("autocomplete", "new-password")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_widget_classes(self.fields)
        self.fields["email"].required = True


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "location", "avatar"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_widget_classes(self.fields)


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_widget_classes(self.fields)