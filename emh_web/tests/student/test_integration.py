from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.test import TestCase, TransactionTestCase

from emh_web.models import Student, Course, Account, Teacher, Topic


class StudentRegistrationViewIntegrationTest(TransactionTestCase):
    """
    Testa a integração da view de registo de estudante, incluindo a criação da conta,
    persistência dos dados do estudante e associação ao curso selecionado.

    Args:
        TransactionTestCase: classe base para testes de integração no Django,
            fornecendo um ambiente de teste isolado e controlado, permitindo a persistência de dados entre testes.

    Methods:
        setUp: configura o ambiente de teste, criando um professor, um tópico e um curso para os testes de integração.
        test_integration_registration_success: testa a integração do fluxo completo de registo de estudante,
            garantindo que a criação da conta, persistência dos dados do estudante e associação ao curso selecionado ocorrem corretamente.
        test_integration_registration_success_no_course: testa a integração do fluxo completo de registo de estudante
            sem selecionar nenhum curso, garantindo que a criação da conta e persistência dos dados do estudante
            ocorrem corretamente.
        test_integration_registration_duplicate_email: testa a integração do fluxo de registo de estudante com um Correio Eletrónico duplicado,
            garantindo que a validação falha corretamente e que o estudante não é criado.
        test_integration_registration_invalid_nif: testa a integração do fluxo de registo de estudante com um NIF duplicado,
            garantindo que a validação falha corretamente e que o estudante não é criado.
    """

    def setUp(self):
        """
        Configura o ambiente de teste, criando um professor, um tópico e um curso para os testes de integração.
        """

        self.teacher = Teacher.objects.create(
            full_name='Anabela Ferreira',
            bio='Professora de Piano com mais de 20 anos de experiência, '
                'especializada em música clássica e contemporânea.',
            training='Licenciatura em Música, Mestrado em Educação Musical.'
        )

        self.topic = Topic.objects.create(
            name='Técnica Instrumental',
            description='Aprenda a dominar o seu instrumento com técnicas avançadas e práticas recomendadas.'
        )

        self.course = Course.objects.create(
            title='Piano Clássico',
            description='Do repertório barroco ao romântico. '
                        'Técnica rigorosa e expressividade musical com professores especializados.',
            duration=3000,
            price=4000.00,
            age_group='A partir dos 12 anos',
            icon='♪'
        )

        self.course.teacher.add(self.teacher)
        self.course.topic.add(self.topic)

        self.url = reverse('student_registration')

        self.valid_student_data = {
            'email': 'novo.aluno@exemplo.pt',
            'password': 'senhaSegura123',
            'full_name': 'João Silva',
            'age': 30,
            'sex': 'M',
            'nif': '123456789',
            'citizen_card_number': '12345678 1 AA1',
            'street': 'Rua das Flores',
            'number': 123,
            'floor': '2A',
            'municipality': 'Lisboa',
            'district': 'Lisboa',
            'postcode': '1000-001',
            'courses': [self.course.id]
        }

    def test_integration_registration_success(self):
        """
        Testa a integração do fluxo completo de registo de estudante, incluindo a criação da conta,
        persistência dos dados do estudante e associação ao curso selecionado.

        Raises:
            AssertionError: se a validação falhar para dados válidos, o que não deveria acontecer.
        """
        response = self.client.post(self.url, data=self.valid_student_data)

        self.assertRedirects(response, reverse('home'))

        self.assertEqual(Account.objects.count(), 1)
        account = Account.objects.first()
        self.assertEqual(account.email, 'novo.aluno@exemplo.pt')
        self.assertTrue(check_password('senhaSegura123', account.password))

        self.assertEqual(Student.objects.count(), 1)
        student = Student.objects.first()

        self.assertEqual(student.full_name, 'João Silva')
        self.assertEqual(student.age, 30)
        self.assertEqual(student.sex, 'M')
        self.assertEqual(student.nif, '123456789')
        self.assertEqual(student.citizen_card_number, '12345678 1 AA1')
        self.assertEqual(student.street, 'Rua das Flores')
        self.assertEqual(student.number, 123)
        self.assertEqual(student.floor, '2A')
        self.assertEqual(student.municipality, 'Lisboa')
        self.assertEqual(student.district, 'Lisboa')
        self.assertEqual(student.postcode, '1000-001')
        self.assertEqual(student.account, account)
        self.assertIn(self.course, student.enrolled_courses.all())

    def test_integration_registration_success_no_course(self):
        """
        Testa a integração do fluxo completo de registo de estudante sem selecionar nenhum curso,
        garantindo que a criação da conta e persistência dos dados do estudante ocorrem corretamente.

        Raises:
            AssertionError: se a validação falhar para dados válidos, o que não deveria acontecer.
        """

        student_data_no_course = self.valid_student_data.copy()
        student_data_no_course.pop('courses', None)

        response = self.client.post(self.url, data=student_data_no_course)

        self.assertRedirects(response, reverse('home'))

        self.assertEqual(Account.objects.count(), 1)
        account = Account.objects.first()
        self.assertEqual(account.email, 'novo.aluno@exemplo.pt')
        self.assertTrue(check_password('senhaSegura123', account.password))

        self.assertEqual(Student.objects.count(), 1)
        student = Student.objects.first()

        self.assertEqual(student.full_name, 'João Silva')
        self.assertEqual(student.age, 30)
        self.assertEqual(student.sex, 'M')
        self.assertEqual(student.nif, '123456789')
        self.assertEqual(student.citizen_card_number, '12345678 1 AA1')
        self.assertEqual(student.street, 'Rua das Flores')
        self.assertEqual(student.number, 123)
        self.assertEqual(student.floor, '2A')
        self.assertEqual(student.municipality, 'Lisboa')
        self.assertEqual(student.district, 'Lisboa')
        self.assertEqual(student.postcode, '1000-001')
        self.assertEqual(student.account, account)

        student = Student.objects.first()
        self.assertEqual(student.enrolled_courses.count(), 0)

    def test_integration_registration_duplicate_email(self):
        """
        Testa a integração do fluxo de registo de estudante com um Correio Eletrónico duplicado,
        garantindo que a validação falha corretamente e que o estudante não é criado.

        Raises:
            AssertionError: se a validação não falhar para um Correio Eletrónico duplicado, o que não deveria acontecer.
        """

        Account.objects.create(email='novo.aluno@exemplo.pt', password='senhaSegura123')

        response = self.client.post(self.url, data=self.valid_student_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context['form'],
            'email',
            "Email já existente. Por favor, use um email diferente."
        )

        self.assertEqual(Student.objects.count(), 0)

    def test_integration_registration_invalid_nif(self):
        """
        Testa a integração do fluxo de registo de estudante com um NIF duplicado,
        garantindo que a validação falha corretamente e que o estudante não é criado.

        Raises:
            AssertionError: se a validação não falhar para um NIF duplicado, o que não deveria acontecer.
        """

        Student.objects.create(
            full_name='João Silva',
            age=30,
            sex='M',
            nif='123456789',
            citizen_card_number='87654321 2 BB2',
            street='Rua das Flores',
            number=123,
            floor='2A',
            municipality='Lisboa',
            district='Lisboa',
            postcode='1000-001'
        )

        response = self.client.post(self.url, data=self.valid_student_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context['form'],
            'nif',
            "NIF já existente. Por favor, use um NIF diferente."
        )


class StudentRegistrationIntegrationTest(TestCase):
    """
    Testa a integração do modelo Student com a lógica de validação e persistência de dados,
    garantindo que as regras de unicidade para NIF e Cartão de Cidadão
    sejam corretamente aplicadas durante o processo de registo.

    Args:
        TestCase: classe base para testes de integração no Django, fornecendo um ambiente de teste isolado e controlado.

    Methods:
        setUp: configura o ambiente de teste,
            criando um utilizador de teste e um estudante inicial para os testes de integração.
        test_integration_unicity_nif: testa a integração do modelo Student para garantir que o campo NIF é único,
            verificando se a validação falha corretamente quando um NIF duplicado é utilizado.
        test_integration_unicity_citizen_card_number: testa a integração do modelo Student para garantir que o campo Citizen Card Number é único,
            verificando se a validação falha corretamente quando um Cartão de Cidadão duplicado é utilizado.
        test_integration_test_valid_data: testa a integração do fluxo completo, incluindo a persistência de dados válidos,
            garantindo que a validação passa sem erros para um conjunto de dados corretamente formatados e únicos.
    """

    def setUp(self):
        """
        Configura a secção e um utilizador de teste para os testes de integração.
        """

        self.base_student_data = Student.objects.create(
            full_name="João Silva",
            age=30,
            sex="M",
            nif="123456789",
            citizen_card_number="12345678 1 AA1",
            street="Rua das Flores",
            number=123,
            floor="2A",
            municipality="Lisboa",
            district="Lisboa",
            postcode="1000-001"
        )

    def test_integration_unicity_nif(self):
        """
        Testa a integração do modelo Student para garantir que o campo NIF é único.

        Raises:
            ValidationError: se a validação falhar para dados válidos, o que não deveria acontecer.
        """

        valid_student_data = {
            'full_name': "Maria Santos",
            'age': 25,
            'sex': "F",
            # Mesmo NIF do estudante anterior.
            'nif': 123456789,
            'citizen_card_number': "87654321 2 BB2",
            'street': "Avenida Central",
            'number': 456,
            'floor': "3B",
            'municipality': "Porto",
            'district': "Porto",
            'postcode': "2000-002"
        }

        student = Student(**valid_student_data)

        with self.assertRaises(ValidationError) as context:
            student.full_clean()

        self.assertIn("nif", context.exception.message_dict)

    def test_integration_unicity_citizen_card_number(self):
        """
        Testa a integração do modelo Student para garantir que o campo Citizen Card Number é único.

        Raises:
            ValidationError: se a validação falhar para dados válidos, o que não deveria acontecer.
        """

        invalid_student_data = {
            'full_name': "Carlos Pereira",
            'age': 35,
            'sex': "M",
            'nif': 192837465,
            # Mesmo Citizen Card Number do estudante anterior.
            'citizen_card_number': "12345678 1 AA1",
            'street': "Avenida das Estrelas",
            'number': 321,
            'floor': "4D",
            'municipality': "Braga",
            'district': "Braga",
            'postcode': "4700-003"
        }

        student = Student(**invalid_student_data)

        with self.assertRaises(ValidationError) as context:
            student.full_clean()

        self.assertIn("citizen_card_number", context.exception.message_dict)

    def test_integration_valid_data(self):
        """
        Testa a integração do fluxo completo, incluindo a persistência de dados válidos.

        Raises:
            ValidationError: se a validação falhar para dados válidos, o que não deveria acontecer.
        """

        valid_student_data = {
            'full_name': "Sofia Almeida",
            'age': 22,
            'sex': "F",
            'nif': 555666777,
            'citizen_card_number': "55566677 3 CC3",
            'street': "Rua das Acácias",
            'number': 654,
            'floor': "5E",
            'municipality': "Faro",
            'district': "Faro",
            'postcode': "8000-003"
        }

        student = Student(**valid_student_data)

        try:
            student.full_clean()
        except ValidationError:
            self.fail("A validação falhou para dados válidos")
