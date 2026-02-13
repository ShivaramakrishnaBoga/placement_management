from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import JobDrive, ApplicationField, Application, ApplicationResponse
from django.http import HttpResponse
from django.utils import timezone
import openpyxl


# ==============================
# CREATE JOB
# ==============================
@login_required
def create_job(request):

    if request.user.role not in ['ADMIN', 'OFFICER']:
        return redirect('landing')

    if request.method == 'POST':

        job = JobDrive.objects.create(
            company_name=request.POST.get('company_name'),
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            allowed_branches=request.POST.get('branches'),
            ctc=request.POST.get('salary_amount') or 0,
            # salary_period=request.POST.get('salary_period'), # Removed in model update
            # job_tags=request.POST.get('job_tags'), # Removed
            card_color=request.POST.get('card_color'),
            image=request.FILES.get('company_logo'),
            application_deadline=request.POST.get('application_deadline'),
            created_by=request.user
        )

        # SAVE DYNAMIC FIELDS
        labels = request.POST.getlist('field_label[]')
        types = request.POST.getlist('field_type[]')

        for label, field_type in zip(labels, types):
            if label.strip():
                ApplicationField.objects.create(
                    job=job,
                    field_name=label,
                    field_type=field_type
                )

        return redirect('/dashboard/officer/')

    return render(request, 'jobs/create_job.html')


# ==============================
# JOB LIST
# ==============================
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import JobDrive, Application

@login_required
def job_list(request):

    jobs = JobDrive.objects.all()

    # Add applied status info for students
    if request.user.role == "STUDENT":
        student_applications = Application.objects.filter(
            student=request.user
        )

        applied_job_ids = student_applications.values_list(
            'job_id',
            flat=True
        )

    else:
        applied_job_ids = []

    return render(request, 'jobs/job_list.html', {
        'jobs': jobs,
        'applied_job_ids': applied_job_ids,
        'now': timezone.now()
    })



# ==============================
# JOB DETAIL
# ==============================
@login_required
def job_detail(request, job_id):

    job = get_object_or_404(JobDrive, id=job_id)
    already_applied = False

    if request.user.role == 'STUDENT':

        # Check for existing application
        is_applied = Application.objects.filter(job=job, student=request.user).exists()
        
        if is_applied:
            application = Application.objects.get(job=job, student=request.user)
            # mark viewed
            if not application.viewed:
                application.viewed = True
                application.save()
            already_applied = True # Logic changed slightly from original get_or_create which was weird

    context = {
        'job': job,
        'fields': job.fields.all(),
        'already_applied': already_applied
    }
    if already_applied:
         context['application'] = Application.objects.get(job=job, student=request.user)

    return render(request, 'jobs/job_detail.html', context)


# ==============================
# APPLY JOB
# ==============================
@login_required
def apply_job(request, job_id):

    job = get_object_or_404(JobDrive, id=job_id)

    if job.application_deadline and timezone.now() > job.application_deadline:
        return render(request, 'jobs/job_closed.html', {'job': job})

    if request.user.role != 'STUDENT':
        return redirect('landing')

    if request.method == 'POST':

        application, created = Application.objects.get_or_create(
            job=job,
            student=request.user
        )

        application.status = "APPLIED" # Updated status choice uppercase
        application.save()

        # Clear old responses
        ApplicationResponse.objects.filter(application=application).delete()

        for field in job.fields.all():
    
            if field.field_type in ["file", "multiple_file"]:
                uploaded_file = request.FILES.get(field.field_name)
                value = uploaded_file.name if uploaded_file else ""
            else:
                value = request.POST.get(field.field_name, "")
    
            ApplicationResponse.objects.create(
                application=application,
                field=field,
                value=value
            )

        return redirect('/dashboard/student/')

    return render(request, 'jobs/apply_job.html', {
        'job': job,
        'fields': job.fields.all()
    })


# ==============================
# UPDATE STATUS
# ==============================
@login_required
def update_status(request, application_id):

    if request.user.role not in ['ADMIN', 'OFFICER']:
        return redirect('landing')

    application = get_object_or_404(Application, id=application_id)

    if request.method == 'POST':
        status = request.POST.get('status')
        application.status = status
        application.save()

    return redirect('/dashboard/officer/')


# ==============================
# EXPORT EXCEL (Basic)
# ==============================
@login_required
def export_excel(request, job_id):

    job = get_object_or_404(JobDrive, id=job_id)
    applications = Application.objects.filter(job=job)

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Applications"

    headers = ['Student Name', 'Roll Number', 'Branch', 'Status', 'Viewed']
    sheet.append(headers)

    for app in applications:
        sheet.append([
            app.student.username,
            app.student.roll_number, # This might fail if roll_number moved to profile, but existing User model had it. I should check User model. User model had it. I should prefer profile if I can, but standard User fields are safer for now.
            app.student.branch,
            app.status,
            "Yes" if app.viewed else "No"
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename={job.title}.xlsx'

    workbook.save(response)
    return response


# ==============================
# EXPORT DYNAMIC RESPONSES
# ==============================
@login_required
def export_student_responses(request, job_id):

    job = get_object_or_404(JobDrive, id=job_id)
    applications = Application.objects.filter(job=job)

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Dynamic Responses"

    dynamic_fields = job.fields.all()

    headers = [field.field_name for field in dynamic_fields]
    sheet.append(headers)

    for app in applications:
        row = []

        for field in dynamic_fields:
            response = ApplicationResponse.objects.filter(
                application=app,
                field=field
            ).first()

            row.append(response.value if response else "")

        sheet.append(row)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'{job.title}_dynamic_responses.xlsx'

    workbook.save(response)
    return response
