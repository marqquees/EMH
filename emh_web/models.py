from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator


class Topic(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=150)
    bio = models.TextField(max_length=500)
    training = models.TextField(max_length=200)
    avatar = models.ImageField(upload_to='img/avatar/teacher', blank=True, null=True)

    def __str__(self):
        return self.full_name


class Course(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duração em horas.")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    age_group = models.CharField(max_length=20)
    icon = models.CharField(max_length=5, default='♪')
    topic = models.ManyToManyField('Topic', related_name='courses', blank=True)
    teacher = models.ManyToManyField('Teacher', related_name='courses', blank=True)

    def __str__(self):
        return self.title


class Student(models.Model):
    """
    Modelo para representar um Estudante, incluindo Dados Pessoais, Morada e Cursos Inscritos.
    """

    # Dados Pessoais
    full_name = models.CharField(max_length=150, blank=False, null=False,
                                 validators=[RegexValidator(r'^.{2,}$',
                                                            message="O Nome Completo deve ter pelo menos 2 caracteres.")])
    age = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(1), MaxValueValidator(140)])
    sex = models.CharField(max_length=1, blank=False, null=False,
                           choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')])
    nif = models.CharField(unique=True, blank=False, null=False,
                           validators=[RegexValidator(r'^\d{9}$', message="O NIF deve estar no formato válido.")])
    citizen_card_number = models.CharField(unique=True, blank=False, null=False,
                                           validators=[RegexValidator(r'^\d{8}\s\d{1}\s[A-Z]{2}\d{1}$',
                                                                      message="O Cartão de Cidadão deve estar no formato válido.")])

    # Dados de Morada
    street = models.CharField(max_length=150, blank=False, null=False)
    number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10000)], blank=False, null=False)
    floor = models.CharField(max_length=12, blank=False, null=False)
    municipality = models.CharField(max_length=26, blank=True, null=True)
    district = models.CharField(max_length=16, blank=True, null=True)
    postcode = models.CharField(blank=False, null=False,
                                validators=[RegexValidator(r'^\d{4}-\d{3}$',
                                                           message="O código postal deve estar no formato válido.")])

    # Relacionamento com os Cursos Inscritos
    enrolled_courses = models.ManyToManyField('Course', related_name='students')
    # Relacionamento com a Conta de Acesso à Plataforma
    account = models.OneToOneField('Account', on_delete=models.CASCADE, related_name='student', null=True, blank=True)

    def __str__(self):
        return self.full_name


class Account(models.Model):
    """
    Modelo para representar uma Conta de Acesso à Plataforma, incluindo o Correio Eletrónico e Palavra-Passe.
    """
    email = models.EmailField(unique=True, blank=False, null=False,
                              validators=[RegexValidator(r'^[\w\.-]+@[\w\.-]+\.\w+$',
                                                         message="O Email deve estar em um formato válido.")])
    password = models.CharField(max_length=128, blank=False, null=False,
                                validators=[
                                    RegexValidator(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$',
                                                   message="A Palavra-Passe deve estar num formato válido.")])

    def __str__(self):
        return self.email
