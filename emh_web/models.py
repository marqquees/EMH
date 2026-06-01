from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

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
    id = models.AutoField(primary_key=True)
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
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=150)
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(140)])
    sex = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')])
    street = models.CharField(max_length=150)
    number = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)])
    floor = models.CharField(max_length=12, blank=True, null=True)
    municipality = models.CharField(max_length=30)
    district = models.CharField(max_length=20)
    postcode = models.CharField(max_length=10)
    enrolled_courses = models.ManyToManyField('Course', related_name='students', blank=True)

    def __str__(self):
        return self.full_name

class Account(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField()

    def __str__(self):
        return self.email