import openpyxl
from students.models import StudentProfile
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

def import_academic_excel(file):
    workbook = openpyxl.load_workbook(file)
    sheet = workbook.active

    updated_students = 0
    created_profiles = 0  # Will remain 0 as per logic, but returned for consistency

    with transaction.atomic():
        for row in sheet.iter_rows(min_row=2, values_only=True):
            # Assuming row format: Roll Number, Name, Branch, Year, CGPA, Backlogs
            if not row or len(row) < 6:
                continue

            # Unpack first 6 columns
            roll, name, branch, year, cgpa, backlogs = row[:6]

            if not roll:
                continue
            
            # Ensure roll is string
            roll = str(roll).strip()

            try:
                # Match using StudentProfile.roll_number instead of User.username
                profile = StudentProfile.objects.get(roll_number=roll)
                
                # If found, update fields
                profile.branch = branch
                profile.year = year
                profile.cgpa = float(cgpa)
                profile.backlogs = int(backlogs)
                profile.academic_verified = True
                profile.save()
                
                updated_students += 1
                
            except StudentProfile.DoesNotExist:
                # If StudentProfile does not exist, skip that row
                continue

    return {
        "updated": updated_students,
        "created": created_profiles
    }
