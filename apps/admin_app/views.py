from django.shortcuts import render, redirect
from django.contrib import messages
import datetime
import bcrypt
from .models import User, Hospital, DRG, HospitalDRG


def admin_dashboard_link(request):
    if "curr_user_id" not in request.session:
        return redirect("/")
    context = {
        "list_hosp": Hospital.objects.all().order_by('name')
    }
    return render(request, "admin_app/admin_dashboard.html", context)

def login_route(request):
    request.session.flush()
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    if bcrypt.checkpw(request.POST["admin_password_input"].encode(), User.objects.get(email=request.POST["admin_email_input"]).password_hash.encode()):
        request.session["curr_user_id"] = User.objects.get(email=request.POST["admin_email_input"]).id
        request.session["curr_user_name"] = User.objects.get(email=request.POST["admin_email_input"]).first_name
        return redirect("/admin")
    else:
        messages.error(request, "Email and password combination not valid.")
        return redirect("/")

def logout_route(request):
    request.session.flush()
    return redirect("/")

def update_drg_route(request):
    DRG.objects.all().delete()
    text_file = request.FILES["drg_definition"]
    if not text_file.name.endswith('.txt'):
        messages.error(request,'File is not Text file')
    
    file_data = text_file.read().decode("utf-8")
    lines = file_data.split("\n")
    line_number = 0

    for line in lines:
        line_number = line_number + 1
        try:
            fields = line.split("\t")
            if len(fields[0]) != 3:
                messages.error(request,"Invalid DRG in line " + str(line_number) + ".")
            if len(fields[1]) < 3:
                messages.error(request,"Invalid DRG description in line " + str(line_number) + ". Description must be at least 10 characters.")
            DRG.objects.create(
                ms_drg=fields[0],
                drg_description=fields[1]
            )
        except:
            messages.error(request,"Line skipped while uploading DRG file. See line " + str(line_number)  + ".")

    return redirect("/admin")

def add_hospital_route(request):
    try: 
        text_file = request.FILES["hosp_drg_input"]
    except:
        messages.error(request,"Please enter a Text file.")
        messages.error(request,"Hospital not added.")
        return redirect("/admin")

    errors = Hospital.objects.hospital_validator(request.POST, text_file)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        messages.error(request,"Hospital not added.")
        return redirect("/admin")
    
    try:
        newHosp = Hospital.objects.create(
            name=request.POST["hosp_name_input"],
            beds=float(request.POST["hosp_bed_input"]),
            longitude=float(request.POST["hosp_long_input"]),
            latitude=float(request.POST["hosp_lat_input"]),
            source=request.POST["hosp_source_input"],
            state=request.POST["hosp_state_input"],
            comment=request.POST["hosp_comment_input"]
        )
    except:
        messages.error(request,"Error creating hospital. Hospital not created.")
        return redirect("/admin")

    file_data = text_file.read().decode("utf-8")
    lines = file_data.split("\n")
    line_number = 0

    for line in lines:
        line_number = line_number + 1
        try:
            fields = line.split("\t")
            if len(fields[0]) != 3:
                messages.error(request,"Invalid DRG in line " + str(line_number) + ".")
            if len(fields[1]) < 2:
                messages.error(request,"Invalid billed charge in line " + str(line_number) + ". Please review.")
            currentDRG = DRG.objects.get(ms_drg=fields[0])
            HospitalDRG.objects.create(
                hospital_id=newHosp,
                drg_id=currentDRG,
                avg_allowed_charge=float(fields[1]),
                cases=float(fields[2])
            )
        except:
            messages.error(request,"Line skipped while adding DRG for hospital. See line " + str(line_number)  + ".")
    
    unused_DRGs = DRG.objects.exclude(coding_hospitals=newHosp)

    for drg in unused_DRGs:
        HospitalDRG.objects.create(
            hospital_id=newHosp,
            drg_id=drg,
            avg_allowed_charge=0,
            cases=0
        )
        messages.error(request,"DRG " + str(drg.ms_drg)  + " was not found in Hospital pricing file. Set to 0.")

    return redirect("/admin")

def remove_hospital_route(request):
    try:
        Hospital.objects.get(id=request.POST["remove_hosp_name_input"]).delete()
    except:
        messages.error(request,"Hospital removal failed.")
    
    return redirect("/admin")

# def ping_sources_route(request):
#     pass