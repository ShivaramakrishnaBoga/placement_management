from students.models import StudentProfile

def check_student_eligibility(student_profile, job):
    """
    Returns:
    {
        "eligible": True/False,
        "reasons": [list of reasons]
    }
    """

    reasons = []

    # If profile not verified
    if not student_profile or not student_profile.academic_verified:
        reasons.append("Academic data not verified.")
        return {"eligible": False, "reasons": reasons}

    # Branch check
    if job.eligible_branches and job.eligible_branches != "All":
        # Split by comma and strip
        allowed_branches = [b.strip().upper() for b in job.eligible_branches.split(",")]
        # Ensure student branch is compared correctly (case insensitive or matched)
        if student_profile.branch.upper() not in allowed_branches:
            reasons.append(f"Your branch ({student_profile.branch}) is not eligible.")

    # CGPA check
    if job.cgpa_required and job.min_cgpa is not None:
        if student_profile.cgpa < job.min_cgpa:
            reasons.append(
                f"Minimum CGPA required is {job.min_cgpa}. Your CGPA is {student_profile.cgpa}."
            )

    # Backlogs check
    if job.backlogs_required and job.max_backlogs is not None:
        if student_profile.backlogs > job.max_backlogs:
            reasons.append(
                f"Maximum allowed backlogs is {job.max_backlogs}. You have {student_profile.backlogs}."
            )

    return {
        "eligible": len(reasons) == 0,
        "reasons": reasons
    }
