from datetime import datetime as dt
from json import dumps

import pandas as pd
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from railmadad.constants import update_global_variables
from railmadad.models import Main_Data_Upload, Staff_Detail, CsvFile
from s2analytica.common import log_time, getratelimit
from s2analytica.settings import BASE_DIR
from s2analytica.settings import START_TIME, END_TIME, IST
from django_ratelimit.decorators import ratelimit

@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def show_staff_name(request):

    staff_ids = list(Staff_Detail.objects.values("staff_id"))
    # convert staff_ids into list
    staff_dict = {}

    for staff in set(Staff_Detail.objects.all()):
        staff_dict[str(staff.staff_id)] = [
            staff.staff_id,
            staff.staff_first_name,
            staff.staff_last_name,
            staff.department,
        ]

    staff_json = dumps(staff_dict)

    staff_ids = [i["staff_id"] for i in staff_ids]
    staff_ids = list(set(staff_ids))
    staff_ids.sort()
    complain_list = []
    post = None
    start_date = None
    order = "asc"
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        if user.groups.filter(name="Moderator").exists():
            post = True
            start_date = request.POST.get("start_date", "")

            start = dt.strptime(start_date, "%Y-%m-%d")

            main_data = Main_Data_Upload.objects.filter(
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    f"{start_date} {END_TIME}+00:00",
                ]
            )

            complain_list = list(main_data.values_list())
            number_of_data = main_data.count()
        else:
            messages.error(
                request, "You Cannot Update Staff Name, Only Moderator Can DO"
            )
            return redirect(request.path)
    else:
        start_date = request.GET.get("start_date", "")

        main_data = None
        if start_date:
            main_data = Main_Data_Upload.objects.filter(
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    f"{start_date} {END_TIME}+00:00",
                ]
            )
            complain_list = list(main_data.values_list())
            post = True
            number_of_data = main_data.count()
            sort_method_map = {
                "coach-number": 12,
                "reference": 3,
                "train-number": 8,
                "type": 15,
                "sub-type": 16,
                "disposal-time": 4,
                "rating": 22,
                "reg-date": 4,
                "staff": 14,
                "description": 8,
            }
            sort_method = request.GET.get("sort_method", "")
            order = "desc"
            if sort_method:
                order = request.GET.get("order", "")
                if order == "asc":
                    complain_list.sort(
                        key=lambda x: x[sort_method_map.get(sort_method)]
                    )
                    order = "desc"
                elif order == "desc":
                    complain_list.sort(
                        key=lambda x: x[sort_method_map.get(sort_method)], reverse=True
                    )
                    order = "asc"
        else:
            post = False
            main_data = None
            number_of_data = None
            start_date = None

    all_staff_detail = Staff_Detail.objects.all()
    all_staff_id = []
    for all_s in all_staff_detail:
        all_staff_id.append(all_s.staff_id)

    staff_data = Main_Data_Upload.objects.filter(staff_id__in=all_staff_id)
    staff_detail = {}
    for s in staff_data:
        # print(s.staff_name)
        reference_number = int(s.reference_number)
        first_name = s.staff_name.split(" ")[0]
        last_name = s.staff_name.split(" ")[1]
        staff_detail[reference_number] = [
            s.staff_id, first_name, last_name, s.department]
    # # print(staff_detail)

    ref_number_staff = list(staff_detail.keys())
    value_staff = list(staff_detail.values())

    try:
        for s in staff_data:
            reference_number = int(s.reference_number)
            first_name = s.staff_name.split(" ")[0]
            last_name = s.staff_name.split(" ")[1]
            staff_detail[reference_number] = [
                s.staff_id,
                first_name,
                last_name,
                s.department,
            ]
            ref_number_staff = list(staff_detail.keys())
            value_staff = list(staff_detail.values())
    except:
        messages.error(request, "Staff Name Not Found")
        return redirect(request.path)

    context = {
        "order": order,
        "post": post,
        "start_date": start_date,
        "main_data": main_data,
        "number_of_data": number_of_data,
        "complains": complain_list,
        "staff_ids": staff_ids,
        "staff_json": staff_json,
        'staff_data': staff_data,
        'staff_detail': staff_detail,
        'ref_number_staff': ref_number_staff,
        'values_staff': value_staff
    }

    return render(request, "railmadad/add_staff_name.html", context)


@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
@csrf_exempt
def add_staff_name(request):
    try :
        if request.method == "POST":
            user = User.objects.get(id=request.user.id)
            if user.groups.filter(name="Moderator").exists():
                response = request.POST
                ids = request.POST.getlist('staff_id')
                fnames = request.POST.getlist('fres')
                lnames = request.POST.getlist('lres')
                depts = request.POST.getlist('dres')
                data_ids = request.POST.getlist('data_id')
                ref_number = request.POST.getlist('ref_number')

                for i, id in enumerate(ids):
                    staff = Staff_Detail.objects.get(staff_id=id)
                    data = Main_Data_Upload.objects.get(
                        reference_number=ref_number[i])
                    data.staff_id = id
                    data.department = depts[i]
                    data.staff_name = fnames[i] + " " + lnames[i]
                    data.save()
                update_global_variables()
                messages.success(request, "Successfully Updated Staff Name")
                return redirect("/auth/show_staff_name")
            else:
                messages.error(request, 'You Cannot Upload Data')
                return redirect('/auth/show_staff_name')
        else:
            pass
    except:
        return render(request, 'error.html')

@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def add_staff_csv(request):

    # Fix csvfile here
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        if user.groups.filter(name="Moderator").exists():
            csv_data = request.FILES.get("csv")
            convert_data = str(csv_data).split(" ")
            main_csv_data = "_".join(convert_data)
            data = CsvFile(csv_data=csv_data).save()
            df = pd.read_csv(
                str(BASE_DIR) + "/media/data/railway/" + str(main_csv_data)
            )
            length = len(df)
            for i in range(0, length):
                ref_number_numpy = df["Ref. No."][i]
                ref_number = float(ref_number_numpy)
                try:
                    staff_name = df["Escort staff"][i]
                except KeyError as e:
                    staff_name = df["Escorting staff"][i]

                if Main_Data_Upload.objects.filter(reference_number=ref_number):
                    data = Main_Data_Upload.objects.get(
                        reference_number=ref_number)
                    data.staff_name = staff_name
                    data.save()
                else:
                    pass
                messages.success(request, "Succesfully Updated")
                return render(request.path)
        else:
            messages.error(
                request, "You Don't Have Access So,You Cannot Update The Staff Name"
            )
            return redirect(request.path)
    return render(request, "railmadad/add_staff_csv.html")
