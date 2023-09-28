from django.http import HttpResponse
from django.shortcuts import render
from railmadad.models import Main_Data_Upload
from railmadad.constants import TRAIN_CATS
from railmadad.src.data.DBQuery import DBQuery
from railmadad.constants import rgd, rncc, dnr, pnbe, ppta, ipr, keu, mka, ara,other, coach_clean, bed_roll, security, medical_assis, punctuality, water_avail, electrical_equip,coach_maintain, miscellaneous, Corruption_Bribery, Catering_and_Vending_Services, Divyangjan_Facilities, Facilities_for_Women_with_Special_needs, all_type, critical_type, color_code
from datetime import datetime as dt
from django.contrib.auth.decorators import login_required
from pytz import timezone

from s2analytica.common import log_time, getratelimit
from django_ratelimit.decorators import ratelimit

import calendar

@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def mix_chart(request):
    try:

        total_entries = Main_Data_Upload.objects.count()
        staff_behave = []
        bottom_train = []
        trainsss = Main_Data_Upload.objects.all()
        main_trains = []
        for ttt in trainsss:
            main_trains.append(float(ttt.train_station))
        set_train = set(main_trains)
        main_train = list(set_train)
        checked = []
        
        if request.method == "POST":
            post = True
            complain_category = request.POST.getlist("complain-category")
            start_date = request.POST.get("start_date", "")
            end_date = request.POST.get("end_date", "")

            start_month = dt.strptime(start_date, "%Y-%m-%d")
            end_month = dt.strptime(end_date, "%Y-%m-%d")

            complain_type = request.POST.get("complain-dropdown").split(',')
            train_numbers_str = request.POST.get("train-number-dropdown", "")
            if train_numbers_str != "":
                train_number = train_numbers_str.split(",")
            else:
                train_number = train_numbers_str
            check_type = request.POST.get("category-dropdown").split(',')

            delta = end_month - start_month

            if delta.days <= -1:
                return HttpResponse("<h1>Please Enter valid Date Range</h1>")


            for train in train_number:
                checked.append(int(train))

            first_n = []
            main_sorted_data = DBQuery.train_wise_complain_mix_chart_main_data(complain_type,train_number,start_date,end_date)
            for m in main_sorted_data:
                first_n.append(int((m['train_station'])))
            
            DBQuery.clear_variables()

            for r in first_n:
                bottom_train.append(int(r))
                data1 = DBQuery.maximum_complain_train_clean_data(start_date,end_date,r)
                coach_clean.append(data1.count())
                    
                data2 =  DBQuery.maximum_complain_train_bed_data(start_date,end_date,r)
                bed_roll.append(data2.count())

                data3 = DBQuery.maximum_complain_train_security_data(start_date,end_date,r)
                security.append(data3.count())

                data4 = DBQuery.maximum_complain_train_medical_data(start_date,end_date,r)
                medical_assis.append(data4.count())

                data5 = DBQuery.maximum_complain_train_punctuality_data(start_date,end_date,r)
                punctuality.append(data5.count())

                data6 = DBQuery.maximum_complain_train_water_data(start_date,end_date,r)
                water_avail.append(data6.count())

                data7 = DBQuery.maximum_complain_train_electrical_data(start_date,end_date,r)
                electrical_equip.append(data7.count())

                data8 =  DBQuery.maximum_complain_train_maintain_data(start_date,end_date,r)
                coach_maintain.append(data8.count())

                data9 = DBQuery.maximum_complain_train_miscellaneous_data(start_date,end_date,r)
                miscellaneous.append(data9.count())

                data10 = DBQuery.maximum_complain_train_behave_data(start_date,end_date,r)
                staff_behave.append(data10.count())

                data11 = DBQuery.maximum_complain_train_corruption_data(start_date,end_date,r)
                Corruption_Bribery.append(data11.count())

                data12 =  DBQuery.maximum_complain_train_catering_vending_data(start_date,end_date,r)
                Catering_and_Vending_Services.append(data12.count())

                data13 =  DBQuery.maximum_complain_train_divyang_fascilities_data(start_date,end_date,r)
                Divyangjan_Facilities.append(data13.count())

                data14 =DBQuery.maximum_complain_train_women_sp_need_data(start_date,end_date,r)
                Facilities_for_Women_with_Special_needs.append(data14.count())
        else:
            train_count = None
        total =[]
        if request.method == "POST":
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
        if request.method != "POST":
            post = False
            complain_type = critical_type
            check_type = ["rncc"]
            complain_category=None
            show=False
            total=None
            train_count=None
            train_number = rncc

            # if "other" not in check_type:
            #     check_type.append("other")
            # if TRAIN_CATS[0] not in check_type:
            #     for tc in TRAIN_CATS:
            #         check_type.append(tc)

            current_time_get = dt.now(timezone("Asia/Kolkata"))

            if(current_time_get.day > calendar.monthrange(current_time_get.year, current_time_get.month - 1)[1]):
                default_start = dt(current_time_get.year, current_time_get.month - 1, calendar.monthrange(current_time_get.year, current_time_get.month - 1)[1], 0, 0)
            
            else:
                default_start = dt(current_time_get.year, current_time_get.month - 1, current_time_get.day, 0, 0)
            
            start_date = default_start.strftime('%Y-%m-%d')
            end_date = current_time_get.strftime('%Y-%m-%d')
        else:
            show=True
            train_count = len(train_number)

        context = {
            "bottom_train": bottom_train,
            "post": post,
            "train_count": train_count,
            "total": total,
            "all_type": all_type,
            "critical_type": critical_type,
            "color_code": color_code,
            "total_entries": total_entries,
            "start_date": start_date,
            "end_date": end_date,
            "color_code": color_code,
            "main_train": main_train,
            "checked": checked,
            "check_type": check_type,
            "complain_category": complain_category,
            "complain_type": complain_type,
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
            "trains_cat": TRAIN_CATS,
            'main_train':main_train,
            "train_numbers":train_number,
        }
        return render(request, "railmadad/mix_chart.html", context)
    except:
        return render(request,"error.html")








