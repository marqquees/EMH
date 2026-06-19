from django.test import TestCase
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from emh_web.models import Account


class AccountIntegrationTest(TestCase):
    """
    Testes de integração para o modelo Account, garantindo que a validação e salvamento funcionam corretamente.

    Args:
        TestCase: classe base para testes de unidade e integração no Django.

    Methods:
        setUp: configura o ambiente de teste criando uma conta de exemplo.
        test_account_full_clean_and_save_workflow: testa o fluxo de trabalho de validação e salvamento de uma nova conta.
        test_account_invalid_password_regex: testa a validação de senhas com formato mal construído.
        test_account_invalid_email_regex: testa a validação de endereços de Correio Eletrónico com formato mal construído.
        test_account_unique_email_integrity: testa a integridade de unicidade do endereço de Correio Eletrónico,
            garantindo que não é possível criar contas duplicadas.
    """

    def setUp(self):
        """
        Configura o ambiente de teste criando uma conta de exemplo para testes de integração.
        """

        self.account = Account.objects.create(
            email='admin@exemplo.pt',
            password=make_password('SenhaSegura123!')
        )

    def test_account_full_clean_and_save_workflow(self):
        """
        Garante que o fluxo de trabalho de validação e salvamento funciona corretamente.

        Raises:
            ValidationError: Se a senha não cumprir os requisitos de segurança.
        """
        new_email = "professor@harmonia.pt"
        password_text_clear = "OutraSenhaSegura456@"

        new_account = Account(email=new_email, password=password_text_clear)

        try:
            new_account.full_clean()
        except ValidationError:
            self.fail("O modelo rejeitou uma senha que cumpre os requisitos de segurança.")

        new_account.password = make_password(password_text_clear)
        new_account.save()

        self.assertEqual(Account.objects.count(), 2)
        saved_account = Account.objects.get(email=new_email)

        self.assertTrue(check_password(password_text_clear, saved_account.password))

    def test_account_invalid_password_regex(self):
        """
        Garante que senhas com formato mal construído são bloqueadas antes de tocarem na base de dados.

        Raises:
            ValidationError: Se a senha não cumprir os requisitos de segurança.
        """
        invalid_password = [
            "senha",
            "senhasegura",
            "senha123456",
            "SenhaSegura1",
            "sen@12"
        ]

        for password in invalid_password:
            with self.subTest(password=password):
                account = Account(email="teste@exemplo.pt", password=password)

                with self.assertRaises(ValidationError) as context:
                    account.full_clean()

                self.assertIn('password', context.exception.message_dict)

    def test_account_invalid_email_regex(self):
        """
        Garante que o endereço de Correio Eletrónico com formato mal construído são bloqueados
        antes de tocarem na base de dados.

        Raises:
            ValidationError: Se o endereço de Correio Eletrónico não cumprir os requisitos de formato.
        """
        invalid_emails = [
            "emailsemarroba.pt",
            "email@semdominio",
            "@semnome.com",
            "joao silva@harmonia.pt"  # Contém espaços
        ]

        for email in invalid_emails:
            with self.subTest(email=email):
                account = Account(email=email, password="ValidPassword123!")

                with self.assertRaises(ValidationError) as context:
                    account.full_clean()

                self.assertIn('email', context.exception.message_dict)

    def test_account_unique_email_integrity(self):
        """
        Garante que o modelo de Conta bloqueia a criação de contas com endereços de Correio Eletrónico duplicados.
        """
        with self.assertRaises(IntegrityError):
            Account.objects.create(
                email='admin@exemplo.pt',
                password=make_password("UmaSenhaDiferente1!")
            )
