from django import forms
from django.contrib.auth import get_user_model

from task_manager.models import Position


class WorkerUpdateForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        )
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First name",
                "class": "form-control"
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last name",
                "class": "form-control"
            }
        )
    )
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        widget=forms.Select(
            attrs={
                "placeholder": "Last name",
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "first_name", "last_name", "position")
    #
    # def save(self, commit=True):
    #     user = super(WorkerUpdateForm, self).save(commit=False)
    #     password = self.cleaned_data["password"]
    #
    #     if password:
    #         user.set_password(password)
    #     if commit:
    #         user.save()
    #     return user
