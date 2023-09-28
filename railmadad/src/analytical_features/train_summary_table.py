from django.http import HttpResponse
from django.shortcuts import render
from railmadad.models import Main_Data_Upload
from railmadad.constants import TRAIN_CATS
from railmadad.src.data.DBQuery import DBQuery
from railmadad.constants import rgd, rncc, dnr, pnbe, ppta, ipr, keu, mka, ara, other, color_code, all_type, critical_type
from datetime import date, datetime as dt
from pytz import timezone
from django.contrib.auth.decorators import login_required

import calendar


@login_required
def train_summary_table(request):
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

        if request.method == "POST":
            post = True
            problem_type = request.POST.getlist("problem_type")
            start_date = request.POST.get("start_date", "")
            end_date = request.POST.get("end_date", "")
            complain_category = request.POST.getlist("complain-category")
            complains = request.POST.getlist("complain-type")

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

            sdate = date(
                int(start_month.year), int(
                    start_month.month), int(start_month.day)
            )
            edate = date(int(end_month.year), int(
                end_month.month), int(end_month.day))

            for tn in request.POST.getlist("train_number"):
                checked.append(int(tn))

            if delta.days <= -1:
                return HttpResponse("<h1>Please Enter valid Date Range</h1>")

            else:
                datas = []
                total = []
                for d in range(len(train_number)):
                    for i in range(len(complain_type)):
                        data = DBQuery.train_sumary_table(
                            start_date, end_date, complain_type, train_number, i, d)
                        datas.append(data)
                for k in range(len(train_number)):
                    total.append(datas[k*len(complain_type)                                 :len(complain_type)*(k+1)])

                total_complain = []
                for t in total:
                    total_complain.append(sum(t))

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
                "other": other,
                "main_train": main_train,
                "bottom_staff_count": bottom_staff_count,
                "bottom_staff": bottom_staff,
                "color_code": color_code,
                "post": post,
                "complain_type": complain_type,
                "start_date": start_date,
                "end_date": end_date,
                "checked": checked,
                "check_type": check_type,
                "complain_category": complain_category,
                "train_number": train_number,
                "trains_cat": TRAIN_CATS,
                'total': total,
                'total_complain': total_complain,
                "train_numbers": train_number
            }

        else:
            current_time_get = dt.now(timezone("Asia/Kolkata"))
            print(current_time_get)

            if(current_time_get.day > calendar.monthrange(current_time_get.year, current_time_get.month - 1)[1]):
                default_start = dt(current_time_get.year, current_time_get.month - 1, calendar.monthrange(current_time_get.year, current_time_get.month - 1)[1], 0, 0)
            
            else:
                default_start = dt(current_time_get.year, current_time_get.month - 1, current_time_get.day, 0, 0)
                
            start_date = default_start.strftime('%Y-%m-%d')
            end_date = current_time_get.strftime('%Y-%m-%d')
            check_type = ["rncc"]
            train_number = rncc
            complain_type = critical_type
            # if "other" not in check_type:
            #     check_type.append("other")
            # if TRAIN_CATS[0] not in check_type:
            #     for tc in TRAIN_CATS:
            #        check_type.append(tc)
            post = False
            context = {
                'post': post,
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
                "other": other,
                "main_train": main_train,
                "checked": checked,
                "complain_category": None,
                "train_numbers": train_number,
                "trains_cat": TRAIN_CATS,
                "start_date": start_date,
                "end_date": end_date,
                "check_type": check_type,
                "complain_type": complain_type
            }

        return render(request, 'railmadad/train_summary_table.html', context)
    except:
        return render(request, "error.html")
