from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from .models import CustomUser, Review


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(
        required=True,
        max_length=11,
        min_length=11,
        validators=[
            RegexValidator(
                regex=r"^\d{11}$",
                message="Введите номер телефона в формате 11 цифр без букв и символов.",
            )
        ],
        widget=forms.TextInput(
            attrs={
                "maxlength": 11,
                "inputmode": "numeric",
                "pattern": r"\d{11}",
                "placeholder": "79991234567",
            }
        ),
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'password1', 'password2']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, f"{i} звезд") for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Ваш отзыв...'})
        }