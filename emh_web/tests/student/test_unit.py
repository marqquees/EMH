from django.core.exceptions import ValidationError
from django.test import TestCase
import re


def validade_student(data):
    """
    Valida os dados de um estudante, incluindo Nome Completo, Idade, NIF, Cartão de Cidadão, Morada e Código Postal.

    Args:
        data (dict): dicionário contendo os dados do estudante a serem validados.

    Raises:
        ValidationError: se algum dos campos não atender aos critérios de validação.
    """

    # Nome Completo
    full_name = data['full_name']
    if not data.get('full_name'):
        raise ValidationError("O Nome Completo é obrigatório.")
    if not isinstance(full_name, str):
        raise ValidationError("O Nome Completo deve ser uma string.")
    if len(full_name) < 2:
        raise ValidationError("O Nome Completo deve ter pelo menos 2 letras.")
    if len(full_name) > 150:
        raise ValidationError("O Nome Completo deve conter no máximo 150 caracteres.")

    # Idade
    age = data.get('age')
    if age is None:
        raise ValidationError("A Idade é obrigatória.")
    if not isinstance(age, int):
        raise ValidationError("A Idade deve ser um número inteiro.")
    if age < 1:
        raise ValidationError("A Idade deve ser um número inteiro maior que 0.")
    if age > 140:
        raise ValidationError("A Idade deve ser um número inteiro menor que 141.")

    # NIF
    if not data.get('nif'):
        raise ValidationError("O NIF é obrigatório.")
    if not re.fullmatch(r'^\d{9}$', str(data['nif'])):
        raise ValidationError("O NIF deve estar no formato válido.")

    # Cartão de Cidadão
    if not data.get('citizen_card_number'):
        raise ValidationError("O Cartão de Cidadão é obrigatório.")
    if not re.fullmatch(r'^\d{8}\s\d{1}\s[A-Z]{2}\d{1}$', str(data['citizen_card_number'])):
        raise ValidationError("O Cartão de Cidadão deve estar no formato válido.")

    # Rua
    if not data.get('street'):
        raise ValidationError("O nome da Rua é obrigatório.")
    if len(data['street']) > 150:
        raise ValidationError("O nome da Rua deve conter no máximo 150 caracteres.")

    # Número da Residência
    number = data['number']
    if data.get('number') is None:
        raise ValidationError("O Número da Residência é obrigatório.")
    if not isinstance(number, int):
        raise ValidationError("O Número da Residência deve ser um número inteiro.")
    if number < 1:
        raise ValidationError("O Número da Residência deve ser um número inteiro maior que 0.")
    if number > 10000:
        raise ValidationError("O Número da Residência deve ser um número inteiro menor que 10001.")

    # Piso
    floor = data.get('floor')
    if not floor:
        raise ValidationError("O número do Piso é obrigatório.")
    if floor and len(data['floor']) > 12:
        raise ValidationError("O número do Piso deve conter no máximo 12 caracteres.")

    # Município
    if data.get('municipality') and len(data['municipality']) > 26:
        raise ValidationError("O nome do Município deve conter no máximo 26 caracteres.")

    # Distrito
    if data.get('district') and len(data['district']) > 16:
        raise ValidationError("O nome do Distrito deve conter no máximo 16 caracteres.")

    # Código Postal
    if not data.get('postcode'):
        raise ValidationError("O Código Postal é obrigatório.")
    if not re.fullmatch(r'^\d{4}-\d{3}$', str(data['postcode'])):
        raise ValidationError("O Código Postal deve estar no formato válido.")


class StudentDataUnitTest(TestCase):
    """
    Testes unitários para validar os dados de um Estudante.
    Cada teste verifica se a função de validação de dados do Estudante deteta corretamente os erros em campos específicos,
    como Nome Completo, Idade, NIF, Cartão de Cidadão, Morada e Código Postal.

    Args:
        TestCase: classe base para criar casos de teste unitários no Django.

    Methods:
        setUp: configura os dados de teste antes de cada teste ser executado.
        test_unit_data_validate_success: verifica se os dados válidos passam pela validação sem erros.
        test_unit_validate_full_name: testa a validação do campo Nome Completo.
        test_unit_validate_age: testa a validação do campo Idade.
        test_unit_validate_nif: testa a validação do campo NIF.
        test_unit_validate_citizen_card: testa a validação do campo Cartão de Cidadão.
        test_unit_validate_street: testa a validação do campo Rua.
        test_unit_validate_number: testa a validação do campo Número da Residência.
        test_unit_validate_floor: testa a validação do campo Piso.
        test_unit_validate_municipality: testa a validação do campo Município.
        test_unit_validate_district: testa a validação do campo Distrito.
        test_unit_validate_postcode: testa a validação do campo Código Postal.
    """

    def setUp(self):
        """
        Configura os dados de teste para os testes unitários de validação de dados do Estudante.
        """

        self.valid_student_data = {
            'full_name': 'João Silva',
            'age': 25,
            'sex': 'M',
            'nif': '123456789',
            'citizen_card_number': '12345678 1 AA1',
            'street': 'Rua das Flores',
            'number': 123,
            'floor': '2E',
            'municipality': 'Maia',
            'district': 'Porto',
            'postcode': '1234-567'
        }

    def test_unit_data_validate_success(self):
        """
        Testa a função de validação de dados do Estudante com um conjunto de dados válidos.

        Raises:
            ValidationError: se a função de validação falhar em dados válidos.
        """

        try:
            validade_student(self.valid_student_data)
        except ValidationError as e:
            self.fail(f"A função de validação falhou em dados válidos. "
                      f"\nErro: {e}")

    def test_unit_validate_full_name(self):
        """
        Testa o erro quando o Nome Completo é vazio, não é uma 'string',
        tem menos de 2 caracteres ou mais de 150 caracteres.

        Raises:
            ValidationError: se a função de validação não detetar o erro de Nome Completo vazio, não for uma 'string' ou
            estiver com cumprimento fora do intervalo [2..150].
        """

        # Nome Completo vazio.
        with self.assertRaisesRegex(ValidationError, r"O Nome Completo é obrigatório."):
            validade_student(self.valid_student_data | {'full_name': None})

        # Nome Completo não é uma 'string'.
        with self.assertRaisesRegex(ValidationError, r"O Nome Completo deve ser uma string."):
            validade_student(self.valid_student_data | {'full_name': 123})

        # Nome Completo com apenas uma letra.
        with self.assertRaisesRegex(ValidationError, r"O Nome Completo deve ter pelo menos 2 letras."):
            validade_student(self.valid_student_data | {'full_name': 'A'})

        # Nome Completo com mais de 150 caracteres.
        with self.assertRaisesRegex(ValidationError, r"O Nome Completo deve conter no máximo 150 caracteres."):
            validade_student(self.valid_student_data | {'full_name': 'A' * 151})

    def test_unit_validate_age(self):
        """
        Testa o erro quando a Idade é vazia, não é um número inteiro ou está fora do intervalo [1, 140].

        Raises:
            ValidationError: se a função de validação não detetar o erro de Idade vazia,
            não numérica ou fora do intervalo.
        """

        # Idade vazia.
        with self.assertRaisesRegex(ValidationError, r"A Idade é obrigatória."):
            validade_student(self.valid_student_data | {'age': None})

        # Idade não é um número inteiro.
        with self.assertRaisesRegex(ValidationError, r"A Idade deve ser um número inteiro."):
            validade_student(self.valid_student_data | {'age': 'twenty-five'})

        # Idade menor que 1.
        with self.assertRaisesRegex(ValidationError, r"A Idade deve ser um número inteiro maior que 0."):
            validade_student(self.valid_student_data | {'age': 0})

        # Idade maior que 140.
        with self.assertRaisesRegex(ValidationError, r"A Idade deve ser um número inteiro menor que 141."):
            validade_student(self.valid_student_data | {'age': 141})

    def test_unit_validate_nif(self):
        """
        Testa o erro quando o NIF é vazio ou não segue o padrão de 9 dígitos.

        Raises:
            ValidationError: se a função de validação não detetar o erro de NIF vazio ou fora do padrão.
        """

        # NIF vazio.
        with self.assertRaisesRegex(ValidationError, r"O NIF é obrigatório."):
            validade_student(self.valid_student_data | {'nif': None})

        # NIF inválido.
        with self.assertRaisesRegex(ValidationError, r"O NIF deve estar no formato válido."):
            validade_student(self.valid_student_data | {'nif': '12345'})

    def test_unit_validate_citizen_card(self):
        """
        Testa o erro quando o Cartão de Cidadão é vazio ou não segue o formato '12345678 1 AA1'.

        Raises:
            ValidationError: se a função de validação não detetar o erro de Cartão de Cidadão vazio ou com formato incorreto.
        """

        # Cartão de Cidadão vazio.
        with self.assertRaisesRegex(ValidationError, r"O Cartão de Cidadão é obrigatório."):
            validade_student(self.valid_student_data | {'citizen_card_number': None})

        # Formato incorreto do Cartão de Cidadão.
        with self.assertRaisesRegex(ValidationError, r"O Cartão de Cidadão deve estar no formato válido."):
            validade_student(self.valid_student_data | {'citizen_card_number': '12345678 1 A1A'})

    def test_unit_validate_street(self):
        """
        Testa o erro quando o nome da Rua é vazio ou tem mais de 150 caracteres.
        
        Raises:
            ValidationError: se a função de validação não detetar o erro de nome da Rua vazio ou com o cumprimento inválido.
        """

        # Nome da Rua vazio.
        with self.assertRaisesRegex(ValidationError, r"O nome da Rua é obrigatório."):
            validade_student(self.valid_student_data | {'street': None})

        # Nome da Rua com mais de 150 caracteres.
        with self.assertRaisesRegex(ValidationError, r"O nome da Rua deve conter no máximo 150 caracteres."):
            validade_student(self.valid_student_data | {'street': 'A' * 151})

    def test_unit_validate_number(self):
        """
        Testa o erro quando o Número da Residência é vazio, não é um número inteiro ou está fora do intervalo [1, 10000].

        Raises:
            ValidationError: se a função de validação não detetar o erro de Número da Residência vazio,
            não numérico ou fora do intervalo.
        """

        # Número da Residência vazio.
        with self.assertRaisesRegex(ValidationError, r"O Número da Residência é obrigatório."):
            validade_student(self.valid_student_data | {'number': None})

        # Número da Residência não é um número inteiro.
        with self.assertRaisesRegex(ValidationError, r"O Número da Residência deve ser um número inteiro."):
            validade_student(self.valid_student_data | {'number': 'one hundred'})

        # Número da Residência menor que 1.
        with self.assertRaisesRegex(ValidationError,
                                    r"O Número da Residência deve ser um número inteiro maior que 0."):
            validade_student(self.valid_student_data | {'number': 0})

        # Número da Residência maior que 10000.
        with self.assertRaisesRegex(ValidationError,
                                    r"O Número da Residência deve ser um número inteiro menor que 10001."):
            validade_student(self.valid_student_data | {'number': 10001})

    def test_unit_validate_floor(self):
        """
        Testa o erro quando o número do Piso é vazio ou tem mais de 12 caracteres.

        Raises:
            ValidationError: se a função de validação não detetar o erro de número do Piso vazio ou com o cumprimento inválido.
        """

        # Número do Piso vazio.
        with self.assertRaisesRegex(ValidationError, r"O número do Piso é obrigatório."):
            validade_student(self.valid_student_data | {'floor': None})

        # Número do Piso com mais de 12 caracteres.
        with self.assertRaisesRegex(ValidationError, r"O número do Piso deve conter no máximo 12 caracteres."):
            validade_student(self.valid_student_data | {'floor': 'A' * 13})

    def test_unit_validate_municipality(self):
        """
        Testa o erro quando o nome do Município tem mais de 26 caracteres.

        Raises:
            ValidationError: se a função de validação não detetar o erro de nome do Município com o cumprimento inválido.
        """

        # Nome do Município com mais de 26 caracteres.
        with self.assertRaisesRegex(ValidationError,
                                    r"O nome do Município deve conter no máximo 26 caracteres."):
            validade_student(self.valid_student_data | {'municipality': 'A' * 27})

    def test_unit_validate_district(self):
        """
        Testa o erro quando o nome do Distrito tem mais de 16 caracteres.

        Raises:
            ValidationError: se a função de validação não detetar o erro de nome do Distrito com o cumprimento inválido.
        """

        # Nome do Distrito com mais de 16 caracteres.
        with self.assertRaisesRegex(ValidationError,
                                    r"O nome do Distrito deve conter no máximo 16 caracteres."):
            validade_student(self.valid_student_data | {'district': 'A' * 17})

    def test_unit_validate_postcode(self):
        """
        Testa o erro quando o Código Postal é vazio ou não segue o formato '1234-567'.

        Raises:
            ValidationError: se a função de validação não detetar o erro de Código Postal vazio ou com formato incorreto.
        """

        # Código Postal vazio.
        with self.assertRaisesRegex(ValidationError, r"O Código Postal é obrigatório."):
            validade_student(self.valid_student_data | {'postcode': None})

        # Código Postal com formato inválido.
        with self.assertRaisesRegex(ValidationError, r"O Código Postal deve estar no formato válido."):
            validade_student(self.valid_student_data | {'postcode': '1234567'})
