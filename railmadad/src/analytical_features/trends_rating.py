
import calendar
from django.shortcuts import render
from railmadad.models import Main_Data_Upload
from railmadad.constants import TRAIN_CATS
from railmadad.src.data.DBQuery import DBQuery
from railmadad.constants import rgd, rncc, dnr, pnbe, ppta, ipr, keu, mka, ara,other, all_type, critical_type, COMPLAINS_TYPE, SUB_TYPES_DICT
from datetime import datetime as dt, timedelta
from pytz import timezone
from django.contrib.auth.decorators import login_required

from s2analytica.common import log_time, getratelimit
from django_ratelimit.decorators import ratelimit

import calendar
@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def trend_rating(request):
    try:
        # raise Exception("This is an example exception")
        trainsss = Main_Data_Upload.objects.all()
        main_trains = []
        for ttt in trainsss:
            main_trains.append(float(ttt.train_station))
        set_train = set(main_trains)
        main_train = list(set_train)

        checked = []
        check_type = []

        if request.method == "POST":
            post = True
            # train_numbers_old = request.POST.getlist("train_number", "")
            start_date = request.POST.get("start_date", "")
            # complain_type_old = request.POST.getlist("complain_type")
            complain_category = request.POST.getlist("complain-category")
            end_date = request.POST.get("end_date", "")
            merged = request.POST.get("merge", "")

            complain_type = request.POST.get("complain-dropdown").split(',')
            train_numbers_str = request.POST.get("train-number-dropdown", "")
            if train_numbers_str != "":
                train_numbers = train_numbers_str.split(",")
            else:
                train_numbers = train_numbers_str
            check_type = request.POST.get("category-dropdown").split(',')


            for train in train_numbers:
                checked.append(int(train))

            # check_type = request.POST.getlist("check-type")

            excel,satis,unsatis,nan,dates,merge =  DBQuery.trend_rating_if(start_date ,end_date,train_numbers, complain_type,merged)
        else:
            current_time_get = dt.now(timezone("Asia/Kolkata"))
            print(calendar.monthrange(current_time_get.year, current_time_get.month - 1)[1])

            if(current_time_get.day > calendar.monthrange(current_time_get.year, current_time_get.month - 1)[1]):
                default_start = dt(current_time_get.year, current_time_get.month - 1, calendar.monthrange(current_time_get.year, current_time_get.month - 1)[1], 0, 0)
            
            else:
                default_start = dt(current_time_get.year, current_time_get.month - 1, current_time_get.day, 0, 0)
            
            
            start_date = default_start.strftime('%Y-%m-%d')
            end_date = current_time_get.strftime('%Y-%m-%d')

            train_numbers = rncc
            complain_type = critical_type
            # merged = ""

            # excel,satis,unsatis,nan,dates,merge =  DBQuery.trend_rating_if(start_date ,end_date,train_numbers, complain_type,merged)
            nan = []
            excel = []
            unsatis = []
            satis = []
            dates = []
            post = False
            # for i in range(0, 31):
            #     current_time = dt.now(timezone("Asia/Kolkata"))
            #     day = (current_time - timedelta(days=i)).date()
            #     dates.append(
            #         str(day.day)
            #         + " "
            #         + str(calendar.month_name[day.month])
            #         + " "
            #         + str(day.year)
            #     )

            #     excel_data = Main_Data_Upload.objects.filter(
            #         registration_date__year=day.year,
            #         registration_date__month=day.month,
            #         registration_date__day=day.day,
            #         rating="Excellent",
            #     )
            #     excel.append(excel_data.count())

            #     satis_data = Main_Data_Upload.objects.filter(
            #         registration_date__year=day.year,
            #         registration_date__month=day.month,
            #         registration_date__day=day.day,
            #         rating="Satisfactory",
            #     )
            #     satis.append(satis_data.count())

            #     unsatis_data = Main_Data_Upload.objects.filter(
            #         registration_date__year=day.year,
            #         registration_date__month=day.month,
            #         registration_date__day=day.day,
            #         rating="Unsatisfactory",
            #     )
            #     unsatis.append(unsatis_data.count())

            #     nan_data = Main_Data_Upload.objects.filter(
            #         registration_date__year=day.year,
            #         registration_date__month=day.month,
            #         registration_date__day=day.day,
            #         rating="-1",
            #     )
            #     nan.append(nan_data.count())

            # dates.reverse()
            # satis.reverse()
            # excel.reverse()
            # unsatis.reverse()
            # nan.reverse()

        if request.method != "POST":
            
            complain_category = None
            post = False
            merge = False
            
            check_type = ['rncc']
            # if "other" not in check_type:
            #     check_type.append("other")
            # if TRAIN_CATS[0] not in check_type:
            #     for tc in TRAIN_CATS:
            #         check_type.append(tc)
                    
        context = {
            "show": True,
            "post": post,
            "dates": dates,
            "all_type": all_type,
            "critical_type": critical_type,
            "start_date": start_date,
            "end_date": end_date,
            "main_train": main_train,
            "rncc": rncc,
            "rgd": rgd,
            "dnr": dnr,
            "pnbe": pnbe,
            "ppta": ppta,
            "ipr": ipr,
            "keu": keu,
            "mka": mka,
            "ara": ara,
            "other": other,
            "trains_cat": TRAIN_CATS,
            "complain_type": complain_type,
            "complain_category": complain_category,
            "nan": nan,
            "excel": excel,
            "satis": satis,
            "unsatis": unsatis,
            "merge": merge,
            "trains_cat": TRAIN_CATS,
            "complain_types": COMPLAINS_TYPE,
            "sub_types": SUB_TYPES_DICT,
            "check_type": check_type,
            "checked": checked,
            "train_numbers" : train_numbers,
        }

        return render(request, "railmadad/trend_rating.html", context)
    except:
        return render(request,"error.html")