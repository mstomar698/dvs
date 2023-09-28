import operator
from datetime import date, datetime
from django_ratelimit.decorators import ratelimit
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from railmadad.models import Main_Data_Upload
from railmadad.src.data.DBQuery import DBQuery
from railmadad.constants import rncc, rgd, all_type, ara, ipr, dnr, pnbe, ppta, keu, mka, color_code, TRAIN_CATS,other
from s2analytica.common import log_time, getratelimit
from pytz import timezone

from s2analytica.settings import START_TIME, END_TIME, IST
from django_ratelimit.decorators import ratelimit

@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def all_sub_complain_train(request, subtype):
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
        ##########################################

        subtypes = subtype

        ######################################################

        if request.method == "POST":
            # train_number = request.POST.getlist("train_number")
            start_date = request.POST.getlist("start_date", "")[0]
            end_date = request.POST.getlist("end_date", "")[0]
            
            # check_type = request.POST.getlist("check-type")
            start_month = datetime.strptime(start_date, "%Y-%m-%d")
            end_month = datetime.strptime(end_date, "%Y-%m-%d")
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

            if delta.days <= -1:
                return HttpResponse("<h1>Please Enter valid Date Range</h1>")
            
            checked=[]
            for tr in train_number:
                checked.append(int(tr))

            str_train_number = []
            for t_n in train_number:
                str_train_number.append(str(t_n))


            sub_type_data_count = []
            for t_r in checked:
                sub_type_filter_data = DBQuery.all_complain_sub_type_train(
                                            train_number,start_date,end_date ,check_type,start_month,end_month,subtype,t_r )
                sub_type_data_count.append(sub_type_filter_data.count())

            make_dict = dict(zip(checked, sub_type_data_count))
            a1_sorted_keys = dict(
                sorted(make_dict.items(), key=operator.itemgetter(1), reverse=True)
            )
            first_n = sorted(a1_sorted_keys, key=a1_sorted_keys.get, reverse=True)

            # print(first_n)

            if len(train_number) == 0:
                for t_r in first_n:
                    sub_type_data = sub_type_filter_data = DBQuery.all_complain_sub_type_train(
                                            train_number,start_date,end_date ,check_type,start_month,end_month,subtype,t_r )
                    data_count.append(sub_type_data.count())
            else:
                for t_r in first_n:
                    sub_type_data = sub_type_filter_data = DBQuery.all_complain_sub_type_train(
                                            train_number,start_date,end_date ,check_type,start_month,end_month,subtype,t_r )
                    data_count.append(sub_type_data.count())

        else:
            post=False

        if request.method != "POST":
            current_time_get = datetime.now(timezone("Asia/Kolkata"))
            default_start = datetime(current_time_get.year, current_time_get.month - 1, current_time_get.day, 0, 0)
            start_date = default_start.strftime('%Y-%m-%d')
            end_date = current_time_get.strftime('%Y-%m-%d')
            real_train_number = rncc
            checked=None
            check_type = ['rncc']
            train_number=None
            first_n = None
        else:
            real_train_number = train_number
            post = True
        context = {
            "post": post,
            "show": True,
            "data_count": data_count,
            "subtype": subtype,
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
            'first_n':first_n
        }
        return render(request, "railmadad/all_sub_complain_train.html", context)
    except:
        return render(request,"error.html")
