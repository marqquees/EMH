from django.contrib.auth.hashers import make_password
from django.shortcuts import render, get_object_or_404, redirect
from emh_web.models import Course, Teacher, Account
from .forms import StudentRegistration
from django.db import IntegrityError, transaction
from django.contrib import messages

def home(request):
    course = Course.objects.all()
    teacher = Teacher.objects.all()
    context = {'courses': course, 'teachers': teacher}
    return render(request, 'emh/home.html', context)


def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    context = {'course': course}
    return render(request, 'emh/course_detail.html', context)


def student_registration(request):
    if request.method == 'POST':
        form = StudentRegistration(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    user_email = form.cleaned_data.get('email')
                    user_password = form.cleaned_data.get('password')

                    new_account = Account.objects.create(email=user_email, password=make_password(user_password))

                    new_student = form.save(commit=False)
                    new_student.account = new_account
                    new_student.save()

                    selected_courses = request.POST.getlist('courses')
                    if selected_courses:
                        new_student.enrolled_courses.set(selected_courses)

                    messages.success(request,
                                     "🎉 Matrícula efetuada com sucesso! Bem-vindo a Escola de Música Harmonia.")

                    return redirect('home')
            except IntegrityError:
                form.add_error('email', "Email já existente. Por favor, use um email diferente.")
            except Exception as e:
                print(f"{e}")
                form.add_error(None, "Erro interno do sistema durante o salvamento.")
        else:
            pass
    else:
        form = StudentRegistration()

    context = {'courses': Course.objects.all(), 'form': form}
    return render(request, 'emh/student_registration.html', context)
