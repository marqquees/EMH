from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from emh_web.models import Account


class AccountModelTest(TestCase):
    """
    Testes Unitários para o Modelo de Conta, incluindo a criação de contas e validação dos campos de Correio Eletrónico e
    Palavra-Passe.

    Args:
        TestCase: classe base para criar casos de teste unitários no Django.

    Methods:
        setUp: configura os dados de teste antes de cada teste ser executado.
        test_model_account_creation: verifica se uma conta é criada corretamente com dados válidos.
        test_model_validate_email: testa cenários de validação do campo Correio Eletrónico,
            incluindo correio eletrónico vazio, formato inválido e duplicação.
        test_model_account_invalid_password: testa cenários de validação do campo Palavra-Passe,
            incluindo palavra-passe vazia e formato inválido.
    """

    def setUp(self):
        """
        Configura o ambiente de teste, garantindo que o banco de dados esteja limpo antes de cada teste.
        """

        self.valid_account_data = {
            'email': 'josé.moreira@exemplo.com',
            'password': 'SenhaSegura123!'
        }
        # Cria um objeto Account na base de dados.
        self.account = Account.objects.create(**self.valid_account_data)

    def test_model_account_creation(self):
        """
        Testa a criação inicial de uma Conta com dados válidos.
        """

        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(self.account.email, "josé.moreira@exemplo.com")
        self.assertEqual(self.account.password, "SenhaSegura123!")

    def test_model_validate_email(self):
        """
        Testa a validação do campo Correio Eletrónico, incluindo casos de Correio Eletrónico vazio,
        formato inválido e duplicação.

        Raises:
            ValidationError: se o Correio Eletrónico for inválido ou vazio.
            IntegrityError: se houver uma tentativa de criar uma Conta com um Correio Eletrónico já existente.
        """

        # Email vazio.
        with self.assertRaises(ValidationError):
            account = Account(**(self.valid_account_data | {'email': None}))
            account.full_clean()

        # Email com formato inválido.
        with self.assertRaises(ValidationError):
            account = Account(**(self.valid_account_data | {'email': 'invalid-format-email'}))
            account.full_clean()

        # Duplicação de Email.
        with self.assertRaises(IntegrityError):
            Account.objects.create(**self.valid_account_data)

    def test_model_account_invalid_password(self):
        """
        Testa a validação do campo Palavra-Passe, incluindo casos de Palavra-Passe vazia e formato inválido.

        Raises:
            ValidationError: se a Palavra-Passe for inválida ou vazia.
        """

        # Palavra-Passe vazia.
        with self.assertRaises(ValidationError):
            account = Account(**(self.valid_account_data | {'password': None}))
            account.full_clean()

        # Palavra-Passe com o formato inválido.
        with self.assertRaises(ValidationError):
            account = Account(**(self.valid_account_data | {'password': 'short'}))
            account.full_clean()
