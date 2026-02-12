from django.shortcuts import render, redirect, get_object_or_404
from jobs.models import Job, Application
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from accounts.models import User
from django.contrib.auth.hashers import make_password


@login_required
def admin_dashboard(request):

    if request.user.role != 'ADMIN':
        return redirect('landing')

    jobs = Job.objects.all()
    applications = Application.objects.all()

    total = applications.count()
    selected = applications.filter(status='Selected').count()
    rejected = applications.filter(status='Rejected').count()

    students_count = User.objects.filter(role='STUDENT').count()
    officers_count = User.objects.filter(role='OFFICER').count()

    return render(request, 'dashboard/admin_dashboard.html', {
        'jobs': jobs,
        'applications': applications,
        'total': total,
        'selected': selected,
        'rejected': rejected,
        'students_count': students_count,
        'officers_count': officers_count,
    })

#manage students

@login_required
def manage_students(request):

    if request.user.role != 'ADMIN':
        return redirect('landing')

    students = User.objects.filter(role='STUDENT')

    return render(request, 'dashboard/manage_students.html', {
        'students': students
    })
#admin add student
@login_required
def add_student(request):

    if request.user.role != 'ADMIN':
        return redirect('landing')

    if request.method == 'POST':
        User.objects.create(
            username=request.POST['username'],
            email=request.POST['email'],
            roll_number=request.POST['roll_number'],
            branch=request.POST['branch'],
            role='STUDENT',
            password=make_password(request.POST['password'])
        )
        return redirect('/dashboard/manage-students/')

    return render(request, 'dashboard/add_student.html')

#admin edit student
@login_required
def edit_student(request, user_id):

    if request.user.role != 'ADMIN':
        return redirect('landing')

    student = get_object_or_404(User, id=user_id, role='STUDENT')

    if request.method == 'POST':
        student.username = request.POST['username']
        student.email = request.POST['email']
        student.roll_number = request.POST['roll_number']
        student.branch = request.POST['branch']
        student.save()
        return redirect('/dashboard/manage-students/')

    return render(request, 'dashboard/edit_student.html', {
        'student': student
    })


#admin delete student
@login_required
def delete_student(request, user_id):

    student = get_object_or_404(User, id=user_id, role='STUDENT')
    student.delete()
    return redirect('/dashboard/manage-students/')

#manage officers
@login_required
def manage_officers(request):

    officers = User.objects.filter(role='OFFICER')

    return render(request, 'dashboard/manage_officers.html', {
        'officers': officers
    })

#admin add officer
@login_required
def add_officer(request):

    if request.method == 'POST':
        User.objects.create(
            username=request.POST['username'],
            email=request.POST['email'],
            role='OFFICER',
            password=make_password(request.POST['password'])
        )
        return redirect('/dashboard/manage-officers/')

    return render(request, 'dashboard/add_officer.html')

#admin edit officer
@login_required
def edit_officer(request, user_id):

    if request.user.role != 'ADMIN':
        return redirect('landing')

    officer = get_object_or_404(User, id=user_id, role='OFFICER')

    if request.method == 'POST':
        officer.username = request.POST['username']
        officer.email = request.POST['email']
        officer.save()
        return redirect('/dashboard/manage-officers/')

    return render(request, 'dashboard/edit_officer.html', {
        'officer': officer
    })
#admin delete officer
@login_required
def delete_officer(request, user_id):

    officer = get_object_or_404(User, id=user_id, role='OFFICER')
    officer.delete()
    return redirect('/dashboard/manage-officers/')



@login_required
def officer_dashboard(request):

    jobs = Job.objects.filter(created_by=request.user)

    applications = Application.objects.filter(job__in=jobs)

    total = applications.count()
    selected = applications.filter(status='Selected').count()
    rejected = applications.filter(status='Rejected').count()

    return render(request, 'dashboard/officer_dashboard.html', {
        'jobs': jobs,
        'applications': applications,
        'total': total,
        'selected': selected,
        'rejected': rejected
    })




@login_required
def student_dashboard(request):

    applications = Application.objects.filter(student=request.user)

    if request.method == 'POST':
        app_id = request.POST.get('application_id')
        result = request.POST.get('result')

        app = Application.objects.get(id=app_id, student=request.user)
        app.status = result
        app.save()

    return render(request, 'dashboard/student_dashboard.html', {
        'applications': applications
    })

