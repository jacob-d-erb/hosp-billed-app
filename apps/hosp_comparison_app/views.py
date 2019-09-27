from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum
from ..admin_app.models import Hospital, DRG, HospitalDRG

def comparison_link(request):
    context = {
        "list_hosp": Hospital.objects.all(),
        "drg_list": DRG.objects.all(),
    }
    return render(request, "hosp_comparison_app/comparison.html", context)

def comparison_route(request):
    label_array = []
    color_array = []
    data_array = []
    hospital_array = []
    currentDRG = DRG.objects.get(id=request.POST["drg_input"])

    for entry in [["hosp1_input", "#3e95cd"], ["hosp2_input", "#8e5ea2"], ["hosp3_input", "#3cba9f"], ["hosp4_input", "#e8c3b9"], ["hosp5_input", "#c45850"]]:
        if request.POST[entry[0]] != "" and request.POST["drg_input"] != "":
            label_array.append(Hospital.objects.get(id=request.POST[entry[0]]).name)
            color_array.append(entry[1])
            data_array.append(HospitalDRG.objects.get(hospital_id=Hospital.objects.get(id=request.POST[entry[0]]), drg_id=currentDRG).avg_allowed_charge)
            hospital_array.append(Hospital.objects.get(id=request.POST[entry[0]]))

    context= {
        "label_array": label_array,
        "color_array": color_array,
        "data_array": data_array,
        "hospital_array": hospital_array,
        "current_drg": currentDRG,
    }
    return render(request, "hosp_comparison_app/comparison_chart.html", context)

def spec_hosp_link(request):
    context = {
        "list_hosp": Hospital.objects.all(),
        "drg_list": DRG.objects.all(),
    }
    return render(request, "hosp_comparison_app/single_hosp.html", context)

def spec_hosp_route(request):
    label_array = []
    hosp_data_array = []
    avg_data_array = []
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
            if avg_count == 0:
                avg_count = 1
            avg_data_array.append(avg_total/avg_count)

    context= {
        "label_array": label_array,
        "hosp_data_array": hosp_data_array,
        "avg_data_array": avg_data_array,
        "current_hosp": currentHosp,
    }
    return render(request, "hosp_comparison_app/single_hosp_chart.html", context)

def spec_drg_link(request):
    return render(request, "hosp_comparison_app/comparison.html")