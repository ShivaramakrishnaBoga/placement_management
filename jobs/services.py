from decimal import Decimal

def check_eligibility(student_profile, job_drive):
    """
    Checks if a student is eligible for a job drive.
    Returns (is_eligible, reasons_list)
    """
    reasons = []
    is_eligible = True

    # Check CGPA
    if student_profile.cgpa < job_drive.min_cgpa:
        is_eligible = False
        reasons.append(f"CGPA {student_profile.cgpa} is less than minimum required {job_drive.min_cgpa}")

    # Check Backlogs
    if student_profile.active_backlogs > job_drive.max_backlogs:
        is_eligible = False
        reasons.append(f"Active backlogs {student_profile.active_backlogs} exceeds limit {job_drive.max_backlogs}")

    # Check Branch
    # allowed_branches is a comma separated string
    allowed_branches = [b.strip().upper() for b in job_drive.allowed_branches.split(',')]
    if student_profile.branch.upper() not in allowed_branches:
        is_eligible = False
        reasons.append(f"Branch {student_profile.branch} is not allowed. Allowed: {job_drive.allowed_branches}")

    # Check Year
    # eligible_batches is a comma separated string
    if job_drive.eligible_batches:
        allowed_years = [y.strip() for y in job_drive.eligible_batches.split(',')]
        if str(student_profile.year) not in allowed_years:
            is_eligible = False
            reasons.append(f"Year {student_profile.year} is not eligible. Allowed: {job_drive.eligible_batches}")

    # Check Placement Policy (Dream/Super Dream)
    # This requires checking student's current offers.
    # To implement this, we need to access existing offers.
    # We will assume this check is done separately or we pass current offers here.
    # For now, simplistic check.
    
    if student_profile.is_placed:
        # Check if upgrade logic applies
        # If current offer is Normal and this is Dream -> Allowed
        # If current offer is Dream and this is Super Dream -> Allowed
        # Else -> Blocked
        pass # To be implemented with Offer integration

    return is_eligible, reasons
