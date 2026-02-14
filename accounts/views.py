from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import StudentSignupForm
from .models import User

from students.models import StudentProfile
from django.db import transaction

def student_signup(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save(commit=False)
                user.role = 'STUDENT'
                
                # We can clear these from User if we want strict non-duplication, 
                # but form validation might rely on them. 
                # For now let's just ensure StudentProfile is created.
                user.save()

                # Create Student Profile
                if not hasattr(user, 'student_profile'):
                    StudentProfile.objects.create(
                        user=user,
                        roll_number=form.cleaned_data.get('roll_number'),
                        branch=form.cleaned_data.get('branch'),
                        year=2025,  # Default year as it's mandatory
                        cgpa=0.0,
                        backlogs=0,
                        academic_verified=False
                    )
            
            return redirect('login')
    else:
        form = StudentSignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        print("AUTH USER:", user)

        if user:
            login(request, user)
            print("LOGGED USER ROLE:", user.role)

            if user.role == 'ADMIN':
                return redirect('/dashboard/admin/')
            elif user.role == 'OFFICER':
                return redirect('/dashboard/officer/')
            else:
                return redirect('/dashboard/student/')

    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('landing')
