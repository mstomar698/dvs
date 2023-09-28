from django.http import HttpResponse
from django.shortcuts import render
from railmadad.models import Main_Data_Upload
from railmadad.constants import TRAIN_CATS
from railmadad.src.data.DBQuery import DBQuery
from railmadad.constants import rgd, rncc, dnr, pnbe, ppta, ipr, keu, mka, ara, other, ALL_TYPES, CRITICAL_TYPES
from datetime import datetime as dt
from django.contrib.auth.decorators import login_required
from pytz import timezone

from s2analytica.common import log_time, getratelimit
from django_ratelimit.decorators import ratelimit

import calendar

@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def rating(request):
    try:
        train_numbers_list = Main_Data_Upload.objects.values_list("train_station")
        train = []
        complain_type = []
        complain_category = []
        for tr_numbers in train_numbers_list:
            train.append(tr_numbers)
        train_numbers = set(train)

        trainsss = Main_Data_Upload.objects.all()
        main_trains = []
        for ttt in trainsss:
            main_trains.append(float(ttt.train_station))


        ######################################################

        checked = []

        ########

        ########## Bar Graph rating ###############
        if request.method == "POST":
            
            start_date = request.POST.get("start_date", "")
            end_date = request.POST.get("end_date", "")
            merge = request.POST.get("merge-to-satis", "")
            for train in request.POST.getlist("train_number"):
                checked.append(int(train))

            # print(f"complain_type : {complain_type}")
            complain_category = request.POST.getlist("complain-category")


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

            months = []

            unsatis = []
            satis = []
            excel = []
            nan = []

            trains_num = []
            for t_r in train_numbers:
                trains_num.append(t_r)

            if delta.days <= -1:
                return HttpResponse("<h1>Please Enter Valid Date Range</h1>")

            if len(train_number) == 0:
                main_trains = main_trains
            else:
                main_trains = train_number

            dataa = DBQuery.rating_chart_with_percentage_data_complain_type(main_trains,complain_type, start_date,end_date)
            data = []
            for dd in dataa:
                data.append(dd.rating)
            unsatis.append(data.count("Unsatisfactory"))
            satis.append(data.count("Satisfactory"))
            if merge == "True":
                satis.append(data.count("-1"))
            nan.append(data.count("-1"))
            excel.append(data.count("Excellent"))

            print(nan)
            total = []
            total.append(sum(unsatis))
            total.append(sum(satis))
            total.append(sum(excel))
            total.append(sum(nan))

            # months.append(calendar.month_name[i])

            if sum(excel) == 0 and sum(nan) == 0 and sum(unsatis) == 0 and sum(satis) == 0:
                show = False
            else:
                show = True

            context = {
                "show": True,
                "post": True,
                "months": months,
                "unsatis": unsatis,
                "satis": satis,
                "excel": excel,
                "nan": nan,
                "train_number": train_numbers,
                "start_date": start_date,
                "end_date": end_date,
                "rncc": rncc,
                "rgd": rgd,
                "total": total,
                "checked": checked,
                "check_type": check_type,
                "dnr": dnr,
                "pnbe": pnbe,
                "ppta": ppta,
                "ipr": ipr,
                "keu": keu,
                "mka": mka,
                "ara": ara,
                "other" : other,
                "trains_cat": TRAIN_CATS,
                "merge": merge,
                "all_type": ALL_TYPES,
                "critical_type": CRITICAL_TYPES,
                "complain_type": complain_type,
                "complain_category": complain_category,
                "train_numbers" : train_number,
            }

        else:
            rating_data = []
            main_rating_data = []

            current_time_get = dt.now(timezone("Asia/Kolkata"))
            end_date = current_time_get.strftime('%Y-%m-%d')

            if(current_time_get.day > calendar.monthrange(current_time_get.year, current_time_get.month - 1)[1]):
                default_start = dt(current_time_get.year, current_time_get.month - 1, calendar.monthrange(current_time_get.year, current_time_get.month - 1)[1], 0, 0)
            
            else:
                default_start = dt(current_time_get.year, current_time_get.month - 1, current_time_get.day, 0, 0)

            start_date = default_start.strftime('%Y-%m-%d')
            post = False
            complain_type = CRITICAL_TYPES
            train_number = rncc

            # full_rating_data = DBQuery.rating_chart_with_percentage_data_complain_type(main_trains,complain_type, start_date,end_date)
            # for f_d in full_rating_data:
            #     main_rating_data.append(f_d.rating)

            unsatis = []
            satis = []
            nan = []
            excel = []

            # unsatis.append(main_rating_data.count("Unsatisfactory"))
            # satis.append(main_rating_data.count("Satisfactory"))
            # nan.append(main_rating_data.count("-1"))
            # excel.append(main_rating_data.count("Excellent"))

            total = []
            # total.append(sum(unsatis))
            # total.append(sum(satis))
            # total.append(sum(excel))
            # total.append(sum(nan))

            # if sum(excel) == 0 and sum(nan) == 0 and sum(unsatis) == 0 and sum(satis) == 0:
            #     show = False
            # else:
            #     show = True

            # start_date = None
            # end_date = None

            check_type_get = ['rncc']
            # if "other" not in check_type_get:
            #     check_type_get.append("other")
            # if TRAIN_CATS[0] not in check_type_get:
            #     for tc in TRAIN_CATS:
            #         check_type_get.append(tc)

            context = {
                "show": False,
                "post": False,
                "unsatis": unsatis,
                "satis": satis,
                "excel": excel,
                "nan": nan,
                "train_number": train_numbers,
                "checked": checked,
                "total": total,
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
                "start_date": start_date,
                "end_date": end_date,
                "all_type": ALL_TYPES,
                "critical_type": CRITICAL_TYPES,
                "complain_type": complain_type,
                "complain_category": complain_category,
                "train_numbers" : train_number,
                "check_type": check_type_get,
            }
        return render(request, "railmadad/rating.html", context)
    except:
        return render(request,"error.html")
