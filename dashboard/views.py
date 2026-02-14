from django.shortcuts import render, redirect, get_object_or_404
from jobs.models import JobDrive as Job, Application
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from accounts.models import User
from django.contrib.auth.hashers import make_password
from students.models import StudentProfile
from django.db import transaction
from django.contrib import messages


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

    # Fetch profiles with user data efficiently
    students = StudentProfile.objects.select_related('user').all()

    return render(request, 'dashboard/manage_students.html', {
        'students': students
    })
#admin add student
@login_required
def add_student(request):
    if request.user.role != 'ADMIN':
        return redirect('landing')

    if request.method == 'POST':
        username = request.POST['username']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('/dashboard/add-student/')

        # If username is unique, create
        user = User.objects.create(
            username=username,
            email=request.POST['email'],
            # We don't need to duplicate roll/branch in User if we rely on Profile, 
            # but for consistency with legacy/other parts, we might. 
            # The USER prompt snippet REMOVED them from User.objects.create(). 
            # I will follow the user's snippet exactly.
            role='STUDENT'
        )

        user.set_password(request.POST['password'])
        user.save()

        StudentProfile.objects.create(
            user=user,
            roll_number=request.POST['roll_number'],
            branch=request.POST['branch'],
            year=2025
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
        student.save()
        
        # Update StudentProfile if exists
        if hasattr(student, 'student_profile'):
            student.student_profile.roll_number = request.POST['roll_number']
            student.student_profile.branch = request.POST['branch']
            student.student_profile.save()
            
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



from jobs.models import JobDrive as Job, Application

@login_required
def officer_dashboard(request):

    jobs = Job.objects.filter(created_by=request.user)

    total = Application.objects.filter(
        job__created_by=request.user
    ).count()

    selected = Application.objects.filter(
        job__created_by=request.user,
        status="Selected"
    ).count()

    rejected = Application.objects.filter(
        job__created_by=request.user,
        status="Rejected"
    ).count()

    applications = Application.objects.filter(job__created_by=request.user).order_by('-applied_at')

    return render(request, 'dashboard/officer_dashboard.html', {
        'jobs': jobs,
        'applications': applications, # Added applications to context
        'total': total,
        'selected': selected,
        'rejected': rejected,
    })

@login_required
def student_profile(request):

    if request.user.role != "STUDENT":
        return redirect("admin_dashboard")

    profile = getattr(request.user, "student_profile", None)

    context = {
        "profile": profile
    }

    return render(request, "dashboard/student_profile.html", context)

@login_required
def my_applications(request):

    if request.user.role != "STUDENT":
        return redirect("admin_dashboard")

    applications = Application.objects.filter(
        student=request.user
    ).select_related("job").order_by("-applied_at")

    return render(
        request,
        "dashboard/my_applications.html",
        {"applications": applications}
    )





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

from core.services.academic_import_service import import_academic_excel
from django.contrib import messages

@login_required
def upload_academic_master(request):
    if request.user.role != 'ADMIN':
        return redirect('admin_dashboard')

    if request.method == 'POST':
        excel_file = request.FILES.get('file')

        if not excel_file:
            messages.error(request, "Please upload a file.")
            return redirect('upload_academic_master')
        
        if not excel_file.name.endswith('.xlsx'):
             messages.error(request, "Please upload a valid .xlsx file.")
             return redirect('upload_academic_master')

        try:
            result = import_academic_excel(excel_file)
            messages.success(
                request,
                f"Updated: {result['updated']} | Created: {result['created']}"
            )
        except Exception as e:
            messages.error(request, f"Error processing file: {str(e)}")

        return redirect('upload_academic_master')

    return render(request, 'dashboard/upload_academic_master.html')


from django.core.paginator import Paginator

@login_required
def student_list(request):

    if request.user.role not in ["ADMIN", "OFFICER"]:
        return redirect("student_dashboard")

    students = StudentProfile.objects.filter(academic_verified=True)

    # Filters
    department = request.GET.get("department")
    cgpa_sort = request.GET.get("cgpa_sort")
    roll_sort = request.GET.get("roll_sort")

    if department and department != "all":
        students = students.filter(branch=department)

    if cgpa_sort == "asc":
        students = students.order_by("cgpa")
    elif cgpa_sort == "desc":
        students = students.order_by("-cgpa")

    if roll_sort == "asc":
        students = students.order_by("roll_number")
    elif roll_sort == "desc":
        students = students.order_by("-roll_number")

    # Pagination
    paginator = Paginator(students, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Get unique branches dynamically
    branches = StudentProfile.objects.values_list("branch", flat=True).distinct()

    context = {
        "page_obj": page_obj,
        "branches": branches,
        "selected_department": department,
        "cgpa_sort": cgpa_sort,
        "roll_sort": roll_sort,
    }

    return render(request, "dashboard/student_list.html", context)


