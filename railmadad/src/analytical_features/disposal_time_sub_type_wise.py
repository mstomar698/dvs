from django.shortcuts import render
from railmadad.models import Main_Data_Upload
from railmadad.constants import TRAIN_CATS
from railmadad.src.data.DBQuery import DBQuery
from railmadad.constants import SUB_TYPE_FOR_DISPOSAL_TIME, rgd, rncc, dnr, pnbe, ppta, ipr, keu, mka, ara, other, color_code, all_type
from pytz import timezone
from datetime import datetime as dt, date
from django_ratelimit.decorators import ratelimit
from s2analytica.common import log_time, getratelimit
from django.contrib.auth.decorators import login_required

import calendar

@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def disposal_time_sub_type_wise(request):
    try:
        train_numbers_list = Main_Data_Upload.objects.values_list("train_station")
        train = []
        for tr_numbers in train_numbers_list:
            train.append(tr_numbers)
        train_num = set(train)
        train_numbers = []
        data_count = []
        for t_numbers in train_num:
            for tt in t_numbers:
                train_numbers.append(tt)

        trainsss = Main_Data_Upload.objects.all()
        main_trains = []
        for ttt in trainsss:
            main_trains.append(float(ttt.train_station))
        set_train = set(main_trains)
        main_train = list(set_train)

        ##### Exported From Common Variable

        if request.method == "POST":
            start_date = request.POST.get("start_date", "")
            end_date = request.POST.get("end_date", "")
            sub_type=request.POST.get('sub_type','')

            train_numbers_str = request.POST.get("train-number-dropdown", "")
            if train_numbers_str != "":
                train_number = train_numbers_str.split(",")
            else:
                train_number = train_numbers_str
            check_type = request.POST.get("category-dropdown").split(',')

            dates,main_data,checked = DBQuery.disposal_time_sub_type_wise_query(start_date,end_date,train_number,sub_type)
        else:
            post=False

        if request.method != "POST":
            start_date = None
            end_date = None
            real_train_number = rncc
            checked=None
            check_type=None
            train_number=None
            main_data = None
            sub_type='Lights'
            dates = None
            complain_category=None
            current_time_get = dt.now(timezone("Asia/Kolkata"))
            print(current_time_get)
            if(current_time_get.day > calendar.monthrange(current_time_get.year, current_time_get.month - 1)[1]):
                default_start = dt(current_time_get.year, current_time_get.month - 1, calendar.monthrange(current_time_get.year, current_time_get.month - 1)[1], 0, 0)
            
            else:
                default_start = dt(current_time_get.year, current_time_get.month - 1, current_time_get.day, 0, 0)
            start_date = default_start.strftime('%Y-%m-%d')
            end_date = current_time_get.strftime('%Y-%m-%d')
            check_type=["rncc"]
            # if "other" not in check_type:
            #     check_type.append("other")
            # if TRAIN_CATS[0] not in check_type:
            #     for tc in TRAIN_CATS:
            #         check_type.append(tc)
        else:
            real_train_number = train_number
            post = True

        context = {
            "post": post,
            "show": True,
            "data_count": data_count,
            "train_numbers": real_train_number,
            "start_date": start_date,
            "end_date": end_date,
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
            "main_train": main_train,
            'color_code':color_code,
            'all_type':all_type,
            'checked':checked,
            'check_type':check_type,
            'train_number':train_number,
            'trains_cat':TRAIN_CATS,
            'main_data':main_data,
            'dates':dates,
            'selected_sub_type':sub_type,
            'sub_type':SUB_TYPE_FOR_DISPOSAL_TIME
        }
        return render(request, 'railmadad/disposal_time_sub_type.html',context)
    except:
        return render(request,"error.html")

