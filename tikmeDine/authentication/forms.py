# authentication/forms.py
from django import forms
from .models import Employee

class EmployeeCreationForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('username', 'email', 'first_name', 'last_name')

class SetupSecurityQuestionsForm(forms.Form):
    security_answer_1 = forms.CharField(
        label="What is your childhood’s nickname?",
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Type your answer here...'})
    )
    security_answer_2 = forms.CharField(
        label="What is your grandmother’s maiden name?",
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Type your answer here...'})
    )
    security_answer_3 = forms.CharField(
        label="What is your favorite sport?",
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Type your answer here...'})
    )


class SetupPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput,
        help_text="Password must be at least 8 characters and include a mix of letters, numbers, and symbols."
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password"
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        # Add additional password validation here (e.g., length, complexity)
        return cleaned_data
