from django.shortcuts import render, get_object_or_404, redirect
from emh_web.models import Course, Teacher

def home(request):
    course = Course.objects.all()
    teacher = Teacher.objects.all()
    context = {'courses': course, 'teachers': teacher}
    return render(request, 'emh/home.html', context)

def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    context = {'course': course}
    return render(request, 'emh/course_detail.html', context)

def enroll_course(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Normalmente guardaria numa base de dados num model como 'Inscricao'
        # ou enviaria um email (ex: send_mail())
        print(f"Nova inscrição recebida: {name} ({email}) para o curso {course_id} - {message}")

        # messages permite adicionar um pop-up na interface
        # messages.success(request, 'A tua inscrição foi registada com sucesso!')

        # Após tratar de um POST, rederecione o utilizador
        if course_id:
            return redirect('course_detail', course_id=course_id)
        return redirect('home')

    # Caso aceda ao link diretamento (GET), voltamos à página inicial
    return redirect('home')

def portal_student_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Aqui normalmente validaria as credenciais do utilizador.
        print(f"Tentativa de login: {email} - {password}")

    return redirect('home')