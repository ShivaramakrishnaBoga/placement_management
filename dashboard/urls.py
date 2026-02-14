from django.urls import path
from . import views

urlpatterns = [
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('officer/', views.officer_dashboard, name='officer_dashboard'),
    path('student/', views.student_dashboard, name='student_dashboard'),

    path('manage-students/', views.manage_students, name='manage_students'),
    path('add-student/', views.add_student, name='add_student'),
    path('edit-student/<int:user_id>/', views.edit_student, name='edit_student'),
    path('delete-student/<int:user_id>/', views.delete_student, name='delete_student'),

    path('manage-officers/', views.manage_officers, name='manage_officers'),
    path('add-officer/', views.add_officer, name='add_officer'),
    path('edit-officer/<int:user_id>/', views.edit_officer, name='edit_officer'),
    path('delete-officer/<int:user_id>/', views.delete_officer, name='delete_officer'),

    path('upload-academic-master/', views.upload_academic_master, name='upload_academic_master'),
    path('students/', views.student_list, name='student_list'),
    path('profile/', views.student_profile, name='student_profile'),
    path('my-applications/', views.my_applications, name='my_applications'),
]
