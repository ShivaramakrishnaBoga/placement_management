from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, ApplicationField, Application, ApplicationResponse
from .forms import JobForm
from accounts.models import User
from django.http import HttpResponse
import openpyxl

@login_required
def create_job(request):

    if request.user.role not in ['ADMIN', 'OFFICER']:
        return redirect('landing')

    if request.method == 'POST':

        Job.objects.create(
            company_name=request.POST.get('company_name'),
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            branches=request.POST.get('branches'),
            salary_amount=request.POST.get('salary_amount') or None,
            salary_period=request.POST.get('salary_period'),
            job_tags=request.POST.get('job_tags'),
            card_color=request.POST.get('card_color'),
            image=request.FILES.get('company_logo'),
            created_by=request.user
        )

        return redirect('/dashboard/officer/')

    return render(request, 'jobs/create_job.html')

#Job List View


def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})



#Job Detail View
def job_detail(request, job_id):

    job = get_object_or_404(Job, id=job_id)

    already_applied = False

    if request.user.is_authenticated and request.user.role == 'STUDENT':
        already_applied = Application.objects.filter(
            job=job,
            student=request.user
        ).exists()

    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'fields': job.fields.all(),
        'already_applied': already_applied
    })


#Apply View (Dynamic Form Logic)
@login_required
def apply_job(request, job_id):

    job = get_object_or_404(Job, id=job_id)

    if request.user.role != 'STUDENT':
        return redirect('landing')

    if request.method == 'POST':

        application = Application.objects.create(
            job=job,
            student=request.user
        )

        for field in job.fields.all():
            value = request.POST.get(field.field_name)
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

@login_required
def export_excel(request, job_id):

    job = get_object_or_404(Job, id=job_id)

    applications = Application.objects.filter(job=job)

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Applications"

    headers = ['Student Name', 'Roll Number', 'Branch', 'Status']
    sheet.append(headers)

    for app in applications:
        sheet.append([
            app.student.username,
            app.student.roll_number,
            app.student.branch,
            app.status
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename={job.title}.xlsx'

    workbook.save(response)
    return response

@login_required
def export_student_responses(request, job_id):

    job = get_object_or_404(Job, id=job_id)
    applications = Application.objects.filter(job=job)

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Dynamic Responses"

    # Get dynamic fields
    dynamic_fields = job.fields.all()

    # Header row (ONLY dynamic fields)
    headers = [field.field_name for field in dynamic_fields]
    sheet.append(headers)

    # Fill rows
    for app in applications:

        row = []

        for field in dynamic_fields:
            response = ApplicationResponse.objects.filter(
                application=app,
                field=field
            ).first()

            if response:
                row.append(response.value)
            else:
                row.append("")

        sheet.append(row)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename={job.title}_dynamic_responses.xlsx'

    workbook.save(response)
    return response
