import re
from django.test import TestCase
from django.core.exceptions import ValidationError


def validate_account(data):
    """
    Valida os dados de uma conta, incluindo o Correio Eletrónico e a Palavra-Passe.

    Args:
        data (dict): dicionário contendo os dados da conta a ser validada.

    Raises:
        ValidationError: se algum dos campos não atender aos critérios de validação.
    """

    # Email
    if not data.get('email'):
        raise ValidationError("O Email é obrigatório.")
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', str(data['email'])):
        raise ValidationError("O Email deve estar em um formato válido.")

    # Password
    if not data.get('password'):
        raise ValidationError("A Password é obrigatória.")
    if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', str(data['password'])):
        raise ValidationError("A Palavra-Passe deve estar num formato válido.")


class AccountDataUnitTest(TestCase):
    """
    Testes Unitários para a Validação de Dados de Conta, incluindo Correio Eletrónico e Palavra-Passe.
    Esses testes verificam se a função de validação de conta lida corretamente com dados válidos e inválidos,
    garantindo que os critérios de formatação e segurança sejam atendidos.

    Args:
        TestCase: classe base para criar casos de teste unitários no Django.

    Methods:
        setUp: configura os dados de teste antes de cada teste ser executado.
        test_unit_data_validate_success: verifica se os dados de conta válidos passam pela validação sem erros.
        test_unit_email_validation: testa cenários de validação do correio eletrónico,
            incluindo correio eletrónico vazio e formato inválido.
        test_unit_password_validation: testa cenários de validação de palavra-passe, incluindo palavra-passe vazia e
            formato inválido.
    """

    def setUp(self):
        """
        Configura os dados de teste para os testes unitários de validação de conta.
        """

        self.valid_account_data = {
            'email': 'joao.silva@gmail.pt',
            'password': 'Password123!'
        }

    def test_unit_data_validate_success(self):
        """
        Testa a função de validação dos Dados de Acesso ao sistema com dados válidos.

        Raises:
            ValidationError: se a função de validação lançar um erro para dados válidos.
        """

        try:
            validate_account(self.valid_account_data)
        except ValidationError as e:
            self.fail(f"A função de validação falhou em dados válidos. "
                      f"\nErro: {e}")

    def test_unit_email_validation(self):
        """
        Testa a validação do campo de Correio Eletrónico.

        Raises:
            ValidationError: se o campo de Correio Eletrónico estiver vazio ou num formato inválido.
        """

        # Email vazio.
        with self.assertRaisesRegex(ValidationError, r"O Email é obrigatório."):
            validate_account(self.valid_account_data | {'email': None})

        # Email inválido.
        with self.assertRaisesRegex(ValidationError, re.escape(r"O Email deve estar em um formato válido.")):
            validate_account(self.valid_account_data | {'email': 'jose.ribeiro@gmail'})

    def test_unit_password_validation(self):
        """
        Testa a validação do campo de Palavra-Passe.

        Raises:
            ValidationError: se o campo de Palavra-Passe estiver vazio ou num formato inválido.
        """

        # Password vazia.
        with self.assertRaisesRegex(ValidationError, r"A Password é obrigatória."):
            validate_account(self.valid_account_data | {'password': None})

        # Password inválida.
        with self.assertRaisesRegex(ValidationError, r"A Palavra-Passe deve estar num formato válido."):
            validate_account(self.valid_account_data | {'password': 'pass'})
