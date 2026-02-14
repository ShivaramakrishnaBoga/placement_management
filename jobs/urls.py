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

    # Guidance
    path('guidance/', views.guidance_list, name='guidance_list'),
    path('guidance/<int:job_id>/', views.guidance_detail, name='guidance_detail'),
    path('guidance/create/<int:job_id>/', views.create_guidance, name='create_guidance'),
    path('guidance/update/<int:job_id>/', views.update_round_status, name='update_round_status'),
    path('guidance/export/<int:job_id>/', views.export_job_guidance_data, name='export_job_guidance_data'),


]
