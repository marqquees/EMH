from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.test import TestCase

from emh_web.models import Student


class StudentModelTest(TestCase):
    """
    Testes unitários para o modelo Student, garantindo a validação correta dos campos e a integridade dos dados.
    Cada teste verifica um aspeto específico do modelo, como a criação de um Estudante com dados válidos,
    a validação de formatos para NIF e Cartão de Cidadão, e a restrição de campos como Rua, Número, Piso,
    Município, Distrito e Código Postal.

    Args:
        TestCase: classe base para criar casos de teste unitários no Django.

    Methods:
        setUp: configura o ambiente de teste, garantindo que o banco de dados esteja limpo antes de cada teste.
        test_model_student_creation: testa a criação inicial de um Estudante com dados válidos.
        test_model_validate_full_name: testa a criação de um Estudante com um Nome Completo inválido,
            garantindo que o campo seja obrigatório, que seja do tipo 'string' e que tenha entre 2 e 150 caracteres.
        test_model_validate_age: testa a criação de um Estudante com uma Idade inválida,
            garantindo que o campo seja obrigatório e que esteja dentro do intervalo permitido [1..140].
        test_model_validate_nif: testa a criação de um Estudante com um NIF inválido,
            garantindo que o campo seja obrigatório, tenha exatamente 9 dígitos e seja único.
        test_model_validate_citizen_card: testa a criação de um Estudante com um Cartão de Cidadão inválido,
            garantindo que o campo seja obrigatório, tenha o formato correto e seja único.
        test_model_validate_street: testa a criação de um Estudante com o nome da Rua inválido,
            garantindo que o campo seja obrigatório, seja do tipo 'string' e tenha no máximo 150 caracteres.
        test_model_validate_number: testa a criação de um Estudante com um Número de Residência inválido,
            garantindo que o campo seja obrigatório e esteja dentro do intervalo permitido [1..10000].
        test_model_validate_floor: testa a criação de um Estudante com um Piso inválido,
            garantindo que o campo seja do tipo 'string' e tenha no máximo 12 caracteres.
        test_model_validate_municipality: testa a criação de um Estudante com um Município inválido,
            garantindo que o campo seja do tipo 'string' e tenha no máximo 26 caracteres.
        test_model_validate_district: testa a criação de um Estudante com um Distrito inválido,
            garantindo que o campo seja do tipo 'string' e tenha no máximo 16 caracteres.
        test_model_validate_postcode: testa a criação de um Estudante com um Código Postal inválido,
            garantindo que o campo seja obrigatório, seja do tipo 'string' e esteja no formato correto '1234-567'.
    """

    def setUp(self):
        """
        Configura o ambiente de teste, garantindo que o banco de dados esteja limpo antes de cada teste.
        """

        self.valid_student_data = {
            'full_name': 'Maria Oliveira',
            'age': 25,
            'sex': 'F',
            'nif': '123456789',
            'citizen_card_number': '12345678 1 AA1',
            'street': 'Rua das Flores',
            'number': 10,
            'floor': '2E',
            'municipality': 'Maia',
            'district': 'Porto',
            'postcode': '1234-567'
        }
        self.student = Student.objects.create(**self.valid_student_data)

    def test_model_student_creation(self):
        """
        Testa a criação inicial de um Estudante com dados válidos.
        """

        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(self.student.full_name, "Maria Oliveira")
        self.assertEqual(self.student.age, 25)
        self.assertEqual(self.student.sex, "F")
        self.assertEqual(self.student.nif, "123456789")
        self.assertEqual(self.student.citizen_card_number, "12345678 1 AA1")
        self.assertEqual(self.student.street, "Rua das Flores")
        self.assertEqual(self.student.number, 10)
        self.assertEqual(self.student.floor, "2E")
        self.assertEqual(self.student.municipality, "Maia")
        self.assertEqual(self.student.district, "Porto")
        self.assertEqual(self.student.postcode, "1234-567")

    def test_model_validate_full_name(self):
        """
        Testa a criação de um Estudante com um Nome Completo inválido, garantindo que o campo seja obrigatório,
        que seja do tipo 'string' e que tenha entre 2 e 150 caracteres.

        Raises:
            ValidationError: se o Nome Completo for vazio, não for uma 'string' ou
            estiver fora do intervalo permitido [2..150].
        """

        # Nome Completo vazio.
        with self.assertRaises(ValidationError):
            student = Student(**(self.valid_student_data | {'full_name': None}))
            student.full_clean()

        # Nome Completo não é uma 'string'.
        with self.assertRaises(ValidationError):
            student = Student(**(self.valid_student_data | {'full_name': 12345}))
            student.full_clean()

        # Nome Completo com apenas uma letra.
        with self.assertRaises(ValidationError):
            student = Student(**(self.valid_student_data | {'full_name': 'A'}))
            student.full_clean()

        # Nome Completo com mais de 150 caracteres.
        with self.assertRaises(ValidationError):
            student = Student(**(self.valid_student_data | {'full_name': 'A' * 151}))
            student.full_clean()

    def test_model_validate_age(self):
        """
        Testa a criação de um Estudante com uma Idade inválida, garantindo que o campo seja obrigatório e
        que esteja dentro do intervalo permitido [1..140].

        Raises:
            ValidationError: se a Idade for vazia ou estiver fora do intervalo permitido [1..140].
        """

        # Idade vazia.
        with self.assertRaises(ValidationError):
            student = Student(**(self.valid_student_data | {'age': None}))
            student.full_clean()

        # Idade menor que 1.
        with self.assertRaises(ValidationError):
            student = Student(**(self.valid_student_data | {'age': 0}))
            student.full_clean()

        # Idade maior que 140.
        with self.assertRaises(ValidationError):
            student = Student(**(self.valid_student_data | {'age': 141}))
            student.full_clean()

    def test_model_validate_nif(self):
        """
        Testa a criação de um Estudante com um NIF inválido, garantindo que o campo seja obrigatório,
        tenha exatamente 9 dígitos e seja único.

        Raises:
            ValidationError: se o NIF for vazio ou não tiver exatamente 9 dígitos.
            IntegrityError: se o NIF já existir na base de dados.
        """

        # NIF vazio.
        with self.assertRaises(ValidationError):
            student = Student(**(self.valid_student_data | {'nif': None}))
            student.full_clean()

        # NIF com formato inválido.
        with self.assertRaises(ValidationError):
            student = Student(**(self.valid_student_data | {'nif': '12345678'}))
            student.full_clean()

        # Duplicação do NIF.
        with self.assertRaises(IntegrityError):
            Student.objects.create(**(self.valid_student_data | {
                'full_name': 'João Silva',
                'citizen_card_number': '87654321 1 BB1'
            }))

    def test_model_validate_citizen_card(self):
        """
        Testa a criação de um Estudante com um Cartão de Cidadão inválido, garantindo que o campo seja obrigatório,
        tenha o formato correto e seja único.

        Raises:
            ValidationError: se o Cartão de Cidadão for vazio ou não estiver no formato correto.
            IntegrityError: se o Cartão de Cidadão já existir na base de dados
        """

        # Cartão de Cidadão vazio.
        with self.assertRaises(ValidationError):
            student = Student(**(self.valid_student_data | {'citizen_card_number': None}))
            student.full_clean()

        # Cartão de Cidadão com formato inválido.
        with self.assertRaises(ValidationError):
            student = Student(**(self.valid_student_data | {'citizen_card_number': '12345678 1 AA'}))
            student.full_clean()

        # Duplicação do Cartão de Cidadão.
        with self.assertRaises(IntegrityError):
            Student.objects.create(**(self.valid_student_data | {
                'full_name': 'João Silva',
                'nif': '987654321'
            }))

    def test_model_validate_street(self):
        """
        Testa a criação de um Estudante com o nome da Rua inválido, garantindo que o campo seja obrigatório,
        seja do tipo 'string' e tenha no máximo 150 caracteres.

        Raises:
            ValidationError: se o nome da Rua for vazio, não for uma 'string' ou tiver mais de 150 caracteres.
        """

        # Nome da Rua vazia.
        with self.assertRaises(ValidationError):
            student = Student(**(self.valid_student_data | {'street': None}))
            student.full_clean()

        # Nome da Rua não é uma 'string'.
        with self.assertRaises(ValidationError):
            student = Student(**(self.valid_student_data | {'street': 12345}))
            student.full_clean()

        # Teste de nome da Rua com mais de 150 caracteres.
        with self.assertRaises(ValidationError):
            student = Student(**(self.valid_student_data | {'street': 'R' * 151}))
            student.full_clean()

    def test_model_validate_number(self):
        """
        Testa a criação de um Estudante com um Número de Residência inválido, garantindo que o campo seja obrigatório
        e esteja dentro do intervalo permitido [1..10000].

        Raises:
            ValidationError: se o Número de Residência for vazio ou estiver fora do intervalo permitido [1..10000].
        """

        # Numero da Residência vazio.
        with self.assertRaises(ValidationError):
            student = Student(**(self.valid_student_data | {'number': None}))
            student.full_clean()

        # Número de residência menor que 1.
        with self.assertRaises(ValidationError):
            student = Student(**(self.valid_student_data | {'number': 0}))
            student.full_clean()

        # Número de residência maior que 10000.
        with self.assertRaises(ValidationError):
            student = Student(**(self.valid_student_data | {'number': 10001}))
            student.full_clean()

    def test_model_validate_floor(self):
        """
        Testa a criação de um Estudante com um Piso inválido, garantindo que o campo seja do tipo 'string' e
        tenha no máximo 12 caracteres.

        Raises:
            ValidationError: se o Piso não for uma 'string' ou tiver mais de 12 caracteres.
        """

        # Nome do Piso vazio.
        with self.assertRaises(ValidationError):
            student = Student(**(self.valid_student_data | {'floor': None}))
            student.full_clean()

        # Piso não é uma 'string'.
        with self.assertRaises(ValidationError):
            student = Student(**(self.valid_student_data | {'floor': 12345}))
            student.full_clean()

        # Nome do Piso com mais de 12 caracteres.
        with self.assertRaises(ValidationError):
            student = Student(**(self.valid_student_data | {'floor': 'P' * 13}))
            student.full_clean()

    def test_model_validate_municipality(self):
        """
        Testa a criação de um Estudante com um Município inválido, garantindo que o campo seja do tipo 'string' e
        tenha no máximo 26 caracteres.

        Raises:
            ValidationError: se o nome do Município não for uma 'string' ou tiver mais de 26 caracteres.
        """

        # Nome do Município vazio.
        with self.assertRaises(ValidationError):
            student = Student(**(self.valid_student_data | {'municipality': None}))
            student.full_clean()

        # Nome do Município não é uma 'string'.
        with self.assertRaises(ValidationError):
            student = Student(**(self.valid_student_data | {'municipality': 12345}))
            student.full_clean()

        # Nome do Município com mais de 26 caracteres.
        with self.assertRaises(ValidationError):
            student = Student(**(self.valid_student_data | {'municipality': 'M' * 27}))
            student.full_clean()

    def test_model_validate_district(self):
        """
        Testa a criação de um Estudante com um Distrito inválido, garantindo que o campo seja do tipo 'string' e
        tenha no máximo 16 caracteres.

        Raises:
            ValidationError: se o nome do Distrito não for uma 'string' ou tiver mais de 16 caracteres.
        """

        # Nome do Distrito vazio.
        with self.assertRaises(ValidationError):
            student = Student(**(self.valid_student_data | {'district': None}))
            student.full_clean()

        # Nome do Distrito não é uma 'string'.
        with self.assertRaises(ValidationError):
            student = Student(**(self.valid_student_data | {'district': 12345}))
            student.full_clean()

        # Nome do Distrito com mais de 16 caracteres.
        with self.assertRaises(ValidationError):
            student = Student(**(self.valid_student_data | {'district': 'D' * 17}))
            student.full_clean()

    def test_model_validate_postcode(self):
        """
        Testa a criação de um Estudante com um Código Postal inválido, garantindo que o campo seja obrigatório,
        seja do tipo 'string' e esteja no formato correto '1234-567'.

        Raises:
            ValidationError: se o Código Postal for vazio, não for uma 'string' ou não estiver no formato correto '1234-567'.
        """

        # Código Postal vazio.
        with self.assertRaises(ValidationError):
            student = Student(**(self.valid_student_data | {'postcode': None}))
            student.full_clean()

        # Código Postal não é uma 'string'.
        with self.assertRaises(ValidationError):
            student = Student(**(self.valid_student_data | {'postcode': 1234567}))
            student.full_clean()

        # Código Postal com formato inválido.
        with self.assertRaises(ValidationError):
            student = Student(**(self.valid_student_data | {'postcode': '1234567'}))
            student.full_clean()
