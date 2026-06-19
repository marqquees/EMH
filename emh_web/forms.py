from .models import Student
from django import forms


class StudentRegistration(forms.ModelForm):
    """
    Formulário de registo de estudante.

    Args:
        forms.ModelForm: classe base para criar formulários a partir de modelos Django.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'exemplo@exemplo.pt'
        })
    )

    password = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '********'
        })
    )

    class Meta:
        model = Student
        fields = [
            'full_name', 'age', 'sex', 'nif', 'citizen_card_number', 'street',
            'number', 'floor', 'municipality', 'district', 'postcode'
        ]

        widgets = {
            'nif': forms.TextInput(attrs={'placeholder': '123456789'}),
            'citizen_card_number': forms.TextInput(attrs={'placeholder': '12345678 1 AA1'}),
            'floor': forms.TextInput(attrs={'placeholder': '1E, 2º, T1, etc.'}),
            'postcode': forms.TextInput(attrs={'placeholder': '1234-567'}),
        }

        error_messages = {
            'nif': {
                'unique': "NIF já existente. Por favor, use um NIF diferente."
            },
            'citizen_card_number': {
                'unique': "Número do Cartão de Cidadão já existente. Por favor, use um CC diferente."
            }
        }
