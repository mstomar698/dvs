
from django.shortcuts import render
from railmadad.models import Main_Data_Upload
from railmadad.constants import ALL_TYPES, COMPLAINS_TYPE, CRITICAL_TYPES, SUB_TYPES_DICT, TRAIN_CATS
from railmadad.src.data.DBQuery import DBQuery
from railmadad.constants import rgd, rncc, dnr, pnbe, ppta, ipr, keu, mka, ara,other, checked
from django.contrib.auth.decorators import login_required
from datetime import datetime as dt, date
from pytz import timezone

from s2analytica.common import log_time, getratelimit
from django_ratelimit.decorators import ratelimit

import calendar

@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def trend(request):
    try:
        # raise Exception("This is an example exception")
        trainsss = Main_Data_Upload.objects.all()
        main_trains = []
        for ttt in trainsss:
            main_trains.append(float(ttt.train_station))
        set_train = set(main_trains)
        main_train = list(set_train)
        ######

        if request.method == "POST":
            post = True
            start_date = request.POST.get("start_date", "")
            end_date = request.POST.get("end_date", "")
            show_chart = request.POST.get("show-chart", "")
            complain_type_list = request.POST.getlist("complain-type")
            sub_type_list = request.POST.getlist("sub-type")

            train_numbers_str = request.POST.get("train-number-dropdown", "")
            if train_numbers_str != "":
                train_numbers = train_numbers_str.split(",")
            else:
                train_numbers = train_numbers_str
            check_type = request.POST.get("category-dropdown").split(',')

            # print(sub_type_list)

            for i in range(len(sub_type_list)):
                if "|" in sub_type_list[i]:
                    sub_type_list[i] = sub_type_list[i].replace("|", "/")

            for train in request.POST.getlist("train_number"):
                checked.append(int(train))


            # selecting complain-type and its sub-type
            complain_type_val = request.POST.get("complain-type", "")
            sub_type_val = request.POST.get("sub-type", "")
            problem_data_graph ,sub_type_graph,dates = DBQuery.trend(start_date ,end_date,train_numbers, sub_type_list,complain_type_list)
            total = []
            complain = []
            total.append(sub_type_graph)
            total.append(problem_data_graph)
            # print("total: ", total)
            complain.append(sub_type_list[0])
            complain.append(complain_type_list[0])

        else:
            post = False


        sub_type = Main_Data_Upload.objects.values_list("sub_type")
        subtype = []
        for s in sub_type:
            for st in s:
                subtype.append(st)

        main_sub_type = []
        for sub in subtype:
            main_sub_type.append(sub.split("/"))
        for i in range(len(main_sub_type)):
            if len(main_sub_type[i]) >= 2:
                subtype[i] = " ".join(main_sub_type[i])

        sts = set(subtype)
        demo_sub = set(sub_type)

        if request.method != "POST":
            post = False
            current_time_get = dt.now(timezone("Asia/Kolkata"))
            print(current_time_get)
            if(current_time_get.day > calendar.monthrange(current_time_get.year, current_time_get.month - 1)[1]):
                default_start = dt(current_time_get.year, current_time_get.month - 1, calendar.monthrange(current_time_get.year, current_time_get.month - 1)[1], 0, 0)
            
            else:
                default_start = dt(current_time_get.year, current_time_get.month - 1, current_time_get.day, 0, 0)
            start_date = default_start.strftime('%Y-%m-%d')
            end_date = current_time_get.strftime('%Y-%m-%d')
            check_type=[]
            if "other" not in check_type:
                check_type.append("other")
            if TRAIN_CATS[0] not in check_type:
                for tc in TRAIN_CATS:
                    check_type.append(tc)

            context = {
                "post": post,
                "rncc": rncc,
                "rgd": rgd,
                "dnr": dnr,
                "pnbe": pnbe,
                "ppta": ppta,
                "ipr": ipr,
                "keu": keu,
                "mka": mka,
                "ara": ara,
                "other" : other,
                "main_train": main_train,
                "trains_cat": TRAIN_CATS,
                "complain_types": COMPLAINS_TYPE,
                "sub_types": SUB_TYPES_DICT,

                "train_numbers":main_train,
                "check_type":check_type,
                "start_date":start_date,
                "end_date":end_date,

                "complain_type_val": "Electrical Equipment",
                "sub_type_val": "Air Conditioner",
            }
        else:
            context = {
                "show": True,
                "post": post,
                "dates": dates,
                "total": total,
                "problem_data_graph": problem_data_graph,
                "sub_type_graph": sub_type_graph,
                "all_type": ALL_TYPES,
                "sub_type": sts,
                "demo_sub": demo_sub,
                "critical_type": CRITICAL_TYPES,
                "start_date": start_date,
                "end_date": end_date,
                "main_train": main_train,
                "checked": checked,
                "check_type": check_type,
                "rncc": rncc,
                "rgd": rgd,
                "dnr": dnr,
                "pnbe": pnbe,
                "ppta": ppta,
                "ipr": ipr,
                "keu": keu,
                "mka": mka,
                "ara": ara,
                "other" : other,
                "trains_cat": TRAIN_CATS,
                "complain_types": COMPLAINS_TYPE,
                "sub_types": SUB_TYPES_DICT,
                "show_chart": show_chart,
                "complain_type_val": complain_type_val,
                "sub_type_val": sub_type_val,
                "complain_type": complain_type_list,
                "sub_type_list": sub_type_list,
                "complain": complain,
                "train_numbers" : train_numbers,
            }

        return render(request, "railmadad/trends.html", context)
    except:
        return render(request, "error.html")
