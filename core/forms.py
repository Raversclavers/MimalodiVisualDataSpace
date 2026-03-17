from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import ContactSubmission, Profile


class AccessibleFormMixin:
    base_input_class = "form-control"

    def _set_base_widget_attrs(self):
        for name, field in self.fields.items():
            existing_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing_classes} {self.base_input_class}".strip()
            field.widget.attrs.setdefault("id", f"id_{name}")

    def _set_error_accessibility_attrs(self):
        for name, field in self.fields.items():
            if name in self.errors:
                field.widget.attrs["aria-invalid"] = "true"
                field.widget.attrs["aria-describedby"] = f"id_{name}-error"
            else:
                field.widget.attrs.pop("aria-invalid", None)
                field.widget.attrs.pop("aria-describedby", None)

    def full_clean(self):
        super().full_clean()
        self._set_error_accessibility_attrs()


class AccessibleAuthenticationForm(AccessibleFormMixin, AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"autocomplete": "username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_base_widget_attrs()


class AccessibleUserCreationForm(AccessibleFormMixin, UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.setdefault("autocomplete", "username")
        self.fields["password1"].widget.attrs.setdefault("autocomplete", "new-password")
        self.fields["password2"].widget.attrs.setdefault("autocomplete", "new-password")
        self._set_base_widget_attrs()


class UserUpdateForm(AccessibleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"autocomplete": "given-name"}),
            "last_name": forms.TextInput(attrs={"autocomplete": "family-name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_base_widget_attrs()


class ProfileUpdateForm(AccessibleFormMixin, forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "bio", "location"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 5}),
            "location": forms.TextInput(attrs={"autocomplete": "address-level2"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_base_widget_attrs()


class ContactForm(AccessibleFormMixin, forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@company.com", "autocomplete": "email"}),
            "subject": forms.TextInput(attrs={"placeholder": "What do you need help with?", "autocomplete": "off"}),
            "message": forms.Textarea(
                attrs={
                    "placeholder": "Tell me about your project, reporting challenge, or dashboard goals.",
                    "rows": 6,
                    "autocomplete": "off",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_base_widget_attrs()

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 2:
            raise forms.ValidationError("Please enter your full name.")
        return name

    def clean_subject(self):
        subject = self.cleaned_data["subject"].strip()
        if len(subject) < 4:
            raise forms.ValidationError("Please add a clear subject so I can prioritize your inquiry.")
        return subject

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 20:
            raise forms.ValidationError("Please include a bit more detail so I can respond usefully.")
        return message