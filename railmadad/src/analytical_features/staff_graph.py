import operator
from django.http import HttpResponse
from django.shortcuts import render
from railmadad.models import Main_Data_Upload
from railmadad.constants import TRAIN_CATS
from railmadad.src.data.DBQuery import DBQuery
from railmadad.constants import rgd, rncc, dnr, pnbe, ppta, ipr, keu, mka, ara, other, all_type, critical_type, color_code
from datetime import datetime as dt, date
from s2analytica.common import log_time, getratelimit
from s2analytica.settings import START_TIME, END_TIME, IST
from django.contrib.auth.decorators import login_required
from pytz import timezone
from django_ratelimit.decorators import ratelimit

import calendar

@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def staff_graph(request):
    try:
        trainsss = Main_Data_Upload.objects.all()
        main_trains = []
        for ttt in trainsss:
            main_trains.append(float(ttt.train_station))
        set_train = set(main_trains)
        main_train = list(set_train)

        bottom_staff = []
        bottom_staff_count = []
        checked = []


        staff_name_main_data = Main_Data_Upload.objects.all()
        staff_name_list = []
        for stf_n in staff_name_main_data:
            staff_name_list.append(stf_n.staff_name)

        set_staff_name = set(staff_name_list)
        staff_name = list(set_staff_name)
        if None in staff_name:
            staff_name.remove(None)
        if "" in staff_name:
            staff_name.remove("")
        if "None" in staff_name:
            staff_name.remove("None")

        if request.method == "POST":
            post = True
            problem_type = request.POST.getlist("problem_type")
            staff_count = int(request.POST.get("staff_count"))
            start_date = request.POST.get("start_date", "")
            end_date = request.POST.get("end_date", "")
            complain_category = request.POST.getlist("complain-category")
            complains = request.POST.getlist("complain-type")
            

            complain_type = request.POST.get("complain-dropdown").split(',')
            train_numbers_str = request.POST.get("train-number-dropdown", "")
            if train_numbers_str != "":
                train_number = train_numbers_str.split(",")
            else:
                train_number = train_numbers_str
            check_type = request.POST.get("category-dropdown").split(',')

            start_month = dt.strptime(start_date, "%Y-%m-%d")
            end_month = dt.strptime(end_date, "%Y-%m-%d")

            delta = end_month - start_month

            sdate = date(
                int(start_month.year), int(start_month.month), int(start_month.day)
            )
            edate = date(int(end_month.year), int(end_month.month), int(end_month.day))

            for tn in request.POST.getlist("train_number"):
                checked.append(int(tn))

            if delta.days <= -1:
                return HttpResponse("<h1>Please Enter valid Date Range</h1>")

            data_count = []
            problem_type = Main_Data_Upload.objects.values_list("problem_type")
            train_numbers = Main_Data_Upload.objects.all()

            Type = []
            for s in problem_type:
                for t in s:
                    Type.append(t)

            problem_types = set(Type)

            for stf_n in staff_name:
                a = Main_Data_Upload.objects.filter(
                    train_station__in=train_number,
                    problem_type__in=problem_types,
                    staff_name=stf_n,
                    registration_date__range=[
                        dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    ],
                    registration_date__lte=end_date,
                )
                data_count.append(a.count())

            make_dict = dict(zip(staff_name, data_count))
            a1_sorted_keys = dict(
                sorted(make_dict.items(), key=operator.itemgetter(1), reverse=True)
            )
            # print(a1_sorted_keys)
            first_n = sorted(a1_sorted_keys, key=a1_sorted_keys.get, reverse=True)[
                :staff_count
            ]


            DBQuery.clear_variables()


            for r in first_n:
                bottom_staff.append(r)
                bottom_staff_count.append(make_dict[r])
                coach_clean = DBQuery.staff_graph_coach_clean_query( r, start_date, end_date, train_number)
                bed_roll = DBQuery.staff_graph_bed_query( r, start_date, end_date, train_number)
                security = DBQuery.staff_graph_security_query( r, start_date, end_date, train_number)
                medical_assis = DBQuery.staff_graph_medical_query( r, start_date, end_date, train_number)
                punctuality = DBQuery.staff_graph_punctuality_query( r, start_date, end_date, train_number)
                water_avail = DBQuery.staff_graph_water_query( r, start_date, end_date, train_number)
                electrical_equip = DBQuery.staff_graph_electrical_query( r, start_date, end_date, train_number)
                coach_maintain=  DBQuery.staff_graph_maintain_query( r, start_date, end_date, train_number)
                miscellaneous = DBQuery.staff_graph_miscellaneous_query( r, start_date, end_date, train_number)
                staff_behave = DBQuery.staff_graph_behave_query( r, start_date, end_date, train_number)
                Corruption_Bribery = DBQuery.staff_graph_corruption_query( r, start_date, end_date, train_number)
                Catering_and_Vending_Services= DBQuery.staff_graph_catering_query( r, start_date, end_date, train_number)
                Divyangjan_Facilities = DBQuery.staff_graph_divyang_query( r, start_date, end_date, train_number)
                Facilities_for_Women_with_Special_needs = DBQuery.staff_graph_women_query( r, start_date, end_date, train_number)

        else:
            staff_count = 10
            post = False
            data_count = 10
            train_number = main_train
            start_date = None
            end_date = None
            post = False
            complain_type = None
            check_type = None
            complain_category=None

        total = []
        if request.method != "POST":
            post=False
            current_time_get = dt.now(timezone("Asia/Kolkata"))
            print(current_time_get)
            if(current_time_get.day > calendar.monthrange(current_time_get.year, current_time_get.month - 1)[1]):
                default_start = dt(current_time_get.year, current_time_get.month - 1, calendar.monthrange(current_time_get.year, current_time_get.month - 1)[1], 0, 0)
            
            else:
                default_start = dt(current_time_get.year, current_time_get.month - 1, current_time_get.day, 0, 0)
            start_date = default_start.strftime('%Y-%m-%d')
            end_date = current_time_get.strftime('%Y-%m-%d')
            check_type=["rncc"]
            complain_type = critical_type
            # if "other" not in check_type:
            #     check_type.append("other")
            # if TRAIN_CATS[0] not in check_type:
            #     for tc in TRAIN_CATS:
            #         check_type.append(tc)
            train_number=rncc
                
        else:
            if "Coach - Cleanliness" in complain_type:
                total.append(coach_clean)
            if "Bed Roll" in complain_type:
                total.append(bed_roll)
            if "Water Availability" in complain_type:
                total.append(water_avail)
            if "Electrical Equipment" in complain_type:
                total.append(electrical_equip)
            if "Coach - Maintenance" in complain_type:
                total.append(coach_maintain)
            if "Security" in complain_type:
                total.append(security)
            if "Punctuality" in complain_type:
                total.append(punctuality)
            if "Medical Assistance" in complain_type:
                total.append(medical_assis)
            if "Miscellaneous" in complain_type:
                total.append(miscellaneous)
            if "Staff Behaviour" in complain_type:
                total.append(staff_behave)

            ### New Complain Type ########
            if "Corruption Bribery" in complain_type:
                total.append(Corruption_Bribery)

            if "Catering and Vending Services" in complain_type:
                total.append(Catering_and_Vending_Services)

            if "Divyangjan Facilities" in complain_type:
                total.append(Divyangjan_Facilities)

            if "Facilities for Women with Special needs" in complain_type:
                total.append(Facilities_for_Women_with_Special_needs)

            if len(total) == 0:
                show = False
            if len(total) >= 1:
                show = True

        context = {
            "all_type": all_type,
            "critical_type": critical_type,
            "rgd": rgd,
            "rncc": rncc,
            "dnr": dnr,
            "pnbe": pnbe,
            "ppta": ppta,
            "ipr": ipr,
            "keu": keu,
            "mka": mka,
            "ara": ara,
            "other" : other,
            "main_train": main_train,
            "bottom_staff_count": bottom_staff_count,
            "bottom_staff": bottom_staff,
            "total": total,
            "data_count": data_count,
            "color_code": color_code,
            "post": post,
            "complain_type": complain_type,
            "start_date": start_date,
            "end_date": end_date,
            "staff_count": staff_count,
            "checked": checked,
            "check_type": check_type,
            "complain_category": complain_category,
            "complain_type": complain_type,
            "train_number": train_number,
            "trains_cat": TRAIN_CATS,
            "train_numbers": train_number,
        }

        return render(request, "railmadad/staff_graph.html", context)
    except:
        return render(request,"error.html")
