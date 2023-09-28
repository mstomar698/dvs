import operator
from django.shortcuts import render
from railmadad.models import Main_Data_Upload
from railmadad.constants import TRAIN_CATS
from railmadad.src.data.DBQuery import DBQuery
from railmadad.constants import rgd, rncc, dnr, pnbe, ppta, ipr, keu, mka, ara, other, color_code, all_type, critical_type
from datetime import datetime as dt, date
from django.db.models import Sum
from pytz import timezone
from django_ratelimit.decorators import ratelimit
from s2analytica.common import log_time, getratelimit  
from django.contrib.auth.decorators import login_required

import calendar


@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def disposal_time_coach_wise(request):
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
        

        if request.method == "POST":
            start_date = request.POST.get("start_date", "")
            end_date = request.POST.get("end_date", "")
            complain_category = request.POST.getlist("complain-category")
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
                int(start_month.year), int(start_month.month), int(start_month.day)
            )
            edate = date(int(end_month.year), int(end_month.month), int(end_month.day))

            checked=[]
            for tr in train_number:
                checked.append(int(tr))

            selected_physical_coach_number = []
            data = DBQuery.disposal_time_coach_wise(complain_type,train_number,start_date,end_date)
            for data in data:
                if data.physical_coach_number == float(0.0):
                    pass
                else:
                    selected_physical_coach_number.append(data.physical_coach_number)


            main_data=[]
            print(selected_physical_coach_number)
            for cn in selected_physical_coach_number:
                if(cn != None):
                    disposal_time = Main_Data_Upload.objects.filter(
                        physical_coach_number = float(cn)
                    )
                    query_count = len(disposal_time)
                    query_sum= disposal_time.aggregate(Sum('disposal_time')).get('disposal_time__sum')
                    avg_query = (query_sum)/(query_count)
                    if query_count == 0:
                        main_data.append(0)
                    else:
                        main_data.append('%.2f' % avg_query)
            make_dict = dict(zip(selected_physical_coach_number, main_data))
            a1_sorted_keys = dict(
                sorted(make_dict.items(), key=operator.itemgetter(1), reverse=True)
            )
            first_n = sorted(a1_sorted_keys, key=a1_sorted_keys.get, reverse=True)
            main_data_values=[]
            for fn in first_n:
                main_data_values.append(a1_sorted_keys[fn])

                        

        else:
            post=False

        if request.method != "POST":
            start_date = None
            end_date = None
            real_train_number = train_numbers
            checked=None
            check_type=None
            main_data = None
            dates = None
            train_number=None
            complain_type = critical_type
            complain_category = None
            main_data_values = None
            first_n = None
            dates = None
            main_data_values = None
            post = False
            current_time_get = dt.now(timezone("Asia/Kolkata"))
            print(current_time_get)
            if(current_time_get.day > calendar.monthrange(current_time_get.year, current_time_get.month - 1)[1]):
                default_start = dt(current_time_get.year, current_time_get.month - 1, calendar.monthrange(current_time_get.year, current_time_get.month - 1)[1], 0, 0)
            
            else:
                default_start = dt(current_time_get.year, current_time_get.month - 1, current_time_get.day, 0, 0)
            start_date = default_start.strftime('%Y-%m-%d')
            end_date = current_time_get.strftime('%Y-%m-%d')
            check_type=['rncc']
            # if "other" not in check_type:
            #     check_type.append("other")
            # if TRAIN_CATS[0] not in check_type:
            #     for tc in TRAIN_CATS:
            #         check_type.append(tc)
            # context = {
            #    "complain_type": all_type,
            #    "complain_category":complain_category ,
            #    "main_train":main_train,
            #    'check_type':check_type,
            #    'train_numbers':main_train,
            #    'all_type':all_type,
            #    'start_date':start_date,
            #    'end_date':end_date
            # }
            real_train_number=rncc
            # train_numbers=main_train
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
            'complain_type':complain_type,
            'critical_type':critical_type,
            'complain_category':complain_category,
            'trains_cat':TRAIN_CATS,
            'main_data':main_data_values,
            'physical_coach_number':first_n,
        }
        return render(request, 'railmadad/disposal_time_coach_wise.html',context)
    except:
        return render(request,"error.html")



