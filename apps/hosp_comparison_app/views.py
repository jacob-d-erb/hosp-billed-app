from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum
from ..admin_app.models import Hospital, DRG, HospitalDRG


def comparison_link(request):
    hosp_name_array = []
    hosp_id_array = []

    all_hospitals = Hospital.objects.all().order_by('name')

    for item in all_hospitals:
        hosp_name_array.append(item.name)
        hosp_id_array.append(item.id)

    context = {
        "list_hosp": all_hospitals,
        "hosp_name_array": hosp_name_array,
        "hosp_id_array": hosp_id_array,
        "drg_list": DRG.objects.all(),
    }

    return render(request, "hosp_comparison_app/comparison.html", context)


def comparison_route(request):
    abbreviated_array = []
    label_array = []
    color_array = []
    data_array = []
    cases_array = []
    hospital_array = []
    
    any_notes_flag = 0

    currentDRG = DRG.objects.get(id=request.POST["drg_input"])

    for entry in [["hosp1_input", "#3e95cd"], ["hosp2_input", "#8e5ea2"], ["hosp3_input", "#3cba9f"], ["hosp4_input", "#e8c3b9"], ["hosp5_input", "#c45850"]]:
        if request.POST[entry[0]] != "" and request.POST["drg_input"] != "":
            original_name = Hospital.objects.get(id=request.POST[entry[0]]).name
            abbreviated_name = ""
            for word in original_name.split():
                abbreviated_name = abbreviated_name + word[0].upper()
            abbreviated_array.append(abbreviated_name)
            label_array.append(original_name)
            color_array.append(entry[1])
            data_array.append(HospitalDRG.objects.get(hospital_id=Hospital.objects.get(id=request.POST[entry[0]]), drg_id=currentDRG).avg_allowed_charge)
            cases_array.append(HospitalDRG.objects.get(hospital_id=Hospital.objects.get(id=request.POST[entry[0]]), drg_id=currentDRG).cases)
            hospital_array.append(Hospital.objects.get(id=request.POST[entry[0]]))
            if Hospital.objects.get(id=request.POST[entry[0]]).comment != "":
                any_notes_flag = 1

    context = {
        "abbreviated_array": abbreviated_array,
        "label_array": label_array,
        "color_array": color_array,
        "data_array": data_array,
        "cases_array": cases_array,
        "hospital_array": hospital_array,
        "current_drg": currentDRG,
        "any_notes_flag": any_notes_flag,
    }
    return render(request, "hosp_comparison_app/comparison_chart.html", context)


def spec_hosp_link(request):
    DRG_name_array = []
    DRG_id_array = []
    DRG_description_array = []

    all_DRGs = DRG.objects.all().order_by('id')

    for item in all_DRGs:
        DRG_name_array.append(item.ms_drg)
        DRG_description_array.append(item.drg_description)
        DRG_id_array.append(item.id)
        
    context = {
        "list_hosp": Hospital.objects.all().order_by('name'),
        "DRG_name_array": DRG_name_array,
        "DRG_description_array": DRG_description_array,
        "DRG_id_array": DRG_id_array,
        "DRG_list": all_DRGs,
    }

    return render(request, "hosp_comparison_app/single_hosp.html", context)


def spec_hosp_route(request):
    label_array = []
    hosp_data_array = []
    avg_data_array = []
    cases_array = []
    avg_count_array = []
    currentHosp = Hospital.objects.get(id=request.POST["hosp_input"])

    for entry in ["drg1_input", "drg2_input", "drg3_input", "drg4_input", "drg5_input"]:
        if request.POST[entry] != "" and request.POST["hosp_input"] != "":
            label_array.append(DRG.objects.get(id=request.POST[entry]).ms_drg)
            hosp_data_array.append(HospitalDRG.objects.get(hospital_id=currentHosp, drg_id=DRG.objects.get(id=request.POST[entry])).avg_allowed_charge)
            avg_count = HospitalDRG.objects.filter(hospital_id__state=currentHosp.state, drg_id=DRG.objects.get(id=request.POST[entry])).exclude(hospital_id=currentHosp).exclude(avg_allowed_charge=0).count()
            avg_sum_set = HospitalDRG.objects.filter(hospital_id__state=currentHosp.state, drg_id=DRG.objects.get(id=request.POST[entry])).exclude(hospital_id=currentHosp)
            avg_total = 0
            for obj in avg_sum_set:
                avg_total = avg_total + obj.avg_allowed_charge
            avg_count_array.append(avg_count)
            if avg_count == 0:
                avg_count = 1
            avg_data_array.append(avg_total/avg_count)
            cases_array.append(HospitalDRG.objects.get(hospital_id=currentHosp, drg_id=DRG.objects.get(id=request.POST[entry])).cases)
    
    abbreviation = ""
    for word in currentHosp.name.split():
        abbreviation = abbreviation + word[0].upper()

    context= {
        "label_array": label_array,
        "hosp_data_array": hosp_data_array,
        "avg_data_array": avg_data_array,
        "cases_array": cases_array,
        "avg_count_array": avg_count_array,
        "current_hosp": currentHosp,
        "hosp_abbreviation": abbreviation
    }
    return render(request, "hosp_comparison_app/single_hosp_chart.html", context)


def about_link(request):
    return render(request, "hosp_comparison_app/about.html")


def spec_drg_link(request):
    context = {  
        "drg_list": DRG.objects.all(),
    }

    return render(request, "hosp_comparison_app/single_drg.html", context)


def spec_drg_route(request):
    long_array = []
    lat_array = []
    cost_array = []
    bed_array = []
    name_array = []

    filteredHospitals = HospitalDRG.objects.filter(drg_id=DRG.objects.get(id=request.POST["drg_input"])).exclude(avg_allowed_charge=0)

    for obj in filteredHospitals:
        cost_array.append(obj.avg_allowed_charge)
        long_array.append(obj.hospital_id.longitude)
        lat_array.append(obj.hospital_id.latitude)
        bed_array.append(obj.hospital_id.beds)
        name_array.append(obj.hospital_id.name)

    context= {
        "long_array": long_array,
        "lat_array": lat_array,
        "cost_array": cost_array,
        "bed_array": bed_array,
        "name_array": name_array,
        "max_cost": max(cost_array),
        "min_cost": min(cost_array),
    }

    return render(request, "hosp_comparison_app/single_drg_chart.html", context)