from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_job, name='create_job'),
    path('list/', views.job_list, name='job_list'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),
    path('<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('update-status/<int:application_id>/', views.update_status, name='update_status'),
    path('export/<int:job_id>/', views.export_excel, name='export_excel'),
    path('export-responses/<int:job_id>/', views.export_student_responses, name='export_student_responses'),


]
