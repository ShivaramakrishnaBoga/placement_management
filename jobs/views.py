from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

import openpyxl

from .models import Application, ApplicationField, ApplicationResponse, Job


@login_required
def create_job(request):
    if request.user.role not in ['ADMIN', 'OFFICER']:
        return redirect('landing')

    if request.method == 'POST':
        title = (request.POST.get('title') or '').strip()
        description = (request.POST.get('description') or '').strip()
        branches = (request.POST.get('branches') or '').strip() or 'All Branches'

        if not title or not description:
            messages.error(request, 'Title and description are required.')
            return render(request, 'jobs/create_job.html')

        job = Job.objects.create(
            company_name=request.POST.get('company_name') or '',
            title=title,
            description=description,
            branches=branches,
            posting_date=request.POST.get('posting_date') or None,
            application_deadline=request.POST.get('application_deadline') or None,
            employment_type=request.POST.get('employment_type') or '',
            salary_amount=request.POST.get('salary_amount') or None,
            salary_period=request.POST.get('salary_period') or '',
            job_tags=request.POST.get('job_tags') or '',
            card_color=request.POST.get('card_color') or '#FFE4D6',
            image=request.FILES.get('company_logo'),
            created_by=request.user,
        )

        field_names = request.POST.getlist('field_name[]')
        field_types = request.POST.getlist('field_type[]')
        field_indexes = request.POST.getlist('field_index[]')

        for index, raw_name in enumerate(field_names):
            field_name = (raw_name or '').strip()
            if not field_name:
                continue

            field_type = field_types[index] if index < len(field_types) else 'text'
            checkbox_name = f'field_required_{field_indexes[index]}' if index < len(field_indexes) else f'field_required_{index}'
            is_required = bool(request.POST.get(checkbox_name))
            ApplicationField.objects.create(
                job=job,
                field_name=field_name,
                field_type=field_type,
                is_required=is_required,
            )

        messages.success(request, 'Job created successfully.')
        return redirect('officer_dashboard')

    return render(request, 'jobs/create_job.html')


def job_list(request):
    jobs = Job.objects.all().order_by('-created_at')
    return render(request, 'jobs/job_list.html', {'jobs': jobs})


def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    already_applied = False
    if request.user.is_authenticated and request.user.role == 'STUDENT':
        already_applied = Application.objects.filter(job=job, student=request.user).exists()

    applications = Application.objects.filter(job=job).select_related('student')

    return render(
        request,
        'jobs/job_detail.html',
        {
            'job': job,
            'fields': job.fields.all(),
            'already_applied': already_applied,
            'applications': applications,
        },
    )


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.user.role != 'STUDENT':
        return redirect('landing')

    if job.is_deadline_passed:
        messages.error(request, 'Application deadline is over for this job.')
        return redirect('job_detail', job_id=job.id)

    if request.method == 'POST':
        if Application.objects.filter(job=job, student=request.user).exists():
            messages.info(request, 'You have already applied for this job.')
            return redirect('student_dashboard')

        try:
            application = Application.objects.create(job=job, student=request.user)
        except IntegrityError:
            messages.info(request, 'You have already applied for this job.')
            return redirect('student_dashboard')

        for field in job.fields.all():
            value = ''
            if field.field_type in ['file', 'multi_file']:
                files = request.FILES.getlist(field.field_name)
                value = ', '.join([uploaded.name for uploaded in files])
            else:
                value = request.POST.get(field.field_name, '').strip()

            if field.is_required and not value:
                application.delete()
                messages.error(request, f'{field.field_name} is required.')
                return redirect('job_detail', job_id=job.id)

            ApplicationResponse.objects.create(application=application, field=field, value=value)

        messages.success(request, 'Application submitted successfully.')
        return redirect('student_dashboard')

    return redirect('job_detail', job_id=job.id)


@login_required
def update_status(request, application_id):
    if request.user.role not in ['ADMIN', 'OFFICER']:
        return redirect('landing')

    application = get_object_or_404(Application, id=application_id)

    if request.user.role == 'OFFICER' and application.job.created_by_id != request.user.id:
        return redirect('landing')

    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Application.STATUS_CHOICES):
            application.status = status
            application.save()
            messages.success(request, 'Application status updated.')

    return redirect('job_detail', job_id=application.job_id)


@login_required
def export_excel(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.user.role not in ['ADMIN', 'OFFICER']:
        return redirect('landing')
    if request.user.role == 'OFFICER' and job.created_by_id != request.user.id:
        return redirect('landing')

    applications = Application.objects.filter(job=job)

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Applications'

    headers = ['Student Name', 'Roll Number', 'Branch', 'Status']
    sheet.append(headers)

    for app in applications:
        sheet.append([
            app.student.username,
            app.student.roll_number,
            app.student.branch,
            app.status,
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={job.title}.xlsx'

    workbook.save(response)
    return response


@login_required
def export_student_responses(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.user.role not in ['ADMIN', 'OFFICER']:
        return redirect('landing')
    if request.user.role == 'OFFICER' and job.created_by_id != request.user.id:
        return redirect('landing')

    applications = Application.objects.filter(job=job)

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Dynamic Responses'

    dynamic_fields = job.fields.all()

    headers = ['Student Name', 'Roll Number', 'Status'] + [field.field_name for field in dynamic_fields]
    sheet.append(headers)

    for app in applications:
        row = [app.student.username, app.student.roll_number, app.status]

        for field in dynamic_fields:
            response = ApplicationResponse.objects.filter(application=app, field=field).first()
            row.append(response.value if response else '')

        sheet.append(row)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={job.title}_dynamic_responses.xlsx'

    workbook.save(response)
    return response
