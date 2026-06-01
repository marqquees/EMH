from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('course/<int:course_id>', views.course_detail, name='course_detail'),
    path('enroll/', views.enroll_course, name='enroll_course'),
    path('portal/student/login/', views.portal_student_login, name='portal_student_login'),
]