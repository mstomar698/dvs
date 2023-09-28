from django.http import HttpResponse
from django.shortcuts import render
from railmadad.models import Main_Data_Upload
from railmadad.constants import TRAIN_CATS
from railmadad.src.data.DBQuery import DBQuery
from railmadad.constants import rgd, rncc, dnr, pnbe, ppta, ipr, keu, mka, ara, other, CRITICAL_TYPES, ALL_TYPES
from django.contrib.auth.decorators import login_required
from datetime import datetime as dt
from pytz import timezone

from s2analytica.common import log_time, getratelimit
from django_ratelimit.decorators import ratelimit

import calendar


@log_time
@ratelimit(key='ip', rate='30/m')
@login_required
def dashboard(request):
    try:
        main_data = []
        trainsss = Main_Data_Upload.objects.all()
        main_trains = []
        for ttt in trainsss:
            main_trains.append(float(ttt.train_station))
        main_train_set = set(main_trains)
        main_train = list(main_train_set)
        complain_type = []
        complain_category = []

        # rncc = []
        # rgd = []
        # dnr = []
        # pnbe = []
        # ppta = []
        # ipr = []
        # keu = []
        # mka = []
        # ara = []
        # # checkbox status data objects #######################
        # train_type_rncc = Train_Type.objects.filter(Type="RNCC")
        # train_type_rgd = Train_Type.objects.filter(Type="RGD")
        # train_type_dnr = Train_Type.objects.filter(Type="DNR")
        # train_type_pnbe = Train_Type.objects.filter(Type="PNBE")
        # train_type_ppta = Train_Type.objects.filter(Type="PPTA")
        # train_type_ipr = Train_Type.objects.filter(Type="IPR")
        # train_type_keu = Train_Type.objects.filter(Type="KEU")
        # train_type_mka = Train_Type.objects.filter(Type="MKA")
        # train_type_ara = Train_Type.objects.filter(Type="ARA")
        # # train checkbox status loops to append into arrays ##
        # for rncc_train in train_type_rncc:
        #     rncc.append(rncc_train.train_number)

        # for rgd_train in train_type_rgd:
        #     rgd.append(rgd_train.train_number)

        # for dnr_train in train_type_dnr:
        #     dnr.append(dnr_train.train_number)

        # for pnbe_train in train_type_pnbe:
        #     pnbe.append(pnbe_train.train_number)

        # for ppta_train in train_type_ppta:
        #     ppta.append(ppta_train.train_number)

        # for ipr_train in train_type_ipr:
        #     ipr.append(ipr_train.train_number)

        # for keu_train in train_type_keu:
        #     keu.append(keu_train.train_number)

        # for mka_train in train_type_mka:
        #     mka.append(mka_train.train_number)

        # for ara_train in train_type_ara:
        #     ara.append(ara_train.train_number)

        # ######################################################

        checked = []
        check_type = None
        ########

        if request.method == "POST":
            post = True
            start_date = request.POST.get("start_date", "")
            end_date = request.POST.get("end_date", "")
            complain_category = request.POST.getlist("complain-category", "")

            start_month = dt.strptime(start_date, "%Y-%m-%d")
            end_month = dt.strptime(end_date, "%Y-%m-%d")
            delta = end_month - start_month

            complain_type = request.POST.get("complain-dropdown").split(',')
            train_numbers_str = request.POST.get("train-number-dropdown", "")
            if train_numbers_str != "":
                train_numbers = train_numbers_str.split(",")
            else:
                train_numbers = train_numbers_str
            check_type = request.POST.get("category-dropdown").split(',')

            for train_number in train_numbers:
                checked.append(int(train_number))

            if delta.days <= -1:
                return HttpResponse("<h1>Please Enter Valid Date Range</h1>")

            data_filter = DBQuery.complain_type_absolute_query(train_numbers,complain_type,start_date,end_date)
            for f_d in data_filter:
                main_data.append(f_d.problem_type)
            data = set(main_data)

            occur = []
            for ff in data:
                occur.append(main_data.count(ff))

            if len(occur) == 0:
                show = False
            else:
                show = True

        else:
            post = False
            #### Full Main data ############
            data =[]
            # full_data = Main_Data_Upload.objects.all()
            # for f_d in full_data:
            #     main_data.append(f_d.problem_type)
            # data = set(main_data)

            ############## Set Data ######################
            occur = []
            show = False
            # for ff in data:
            #     occur.append(main_data.count(ff))

            # if len(occur) == 0:
            #     show = False
            # else:
            #     show = True

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
            check_type=["rncc"]
            complain_type = CRITICAL_TYPES
            # if "other" not in check_type:
            #     check_type.append("other")
            # if TRAIN_CATS[0] not in check_type:
            #     for tc in TRAIN_CATS:
            #         check_type.append(tc)
            
            train_numbers = rncc
        context = {
            "show": show,
            "post": post,
            "main_data": main_data,
            "data": data,
            "occur": occur,
            "start_date": start_date,
            "end_date": end_date,
            "main_train": main_train,
            "checked": checked,
            "check_type": check_type,
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
            "all_type": ALL_TYPES,
            "critical_type": CRITICAL_TYPES,
            "complain_type": complain_type,
            "complain_category": complain_category,
            "train_numbers" : train_numbers,
        }
        return render(request, "railmadad/dashboard.html", context)
    except:
        return render(request,"error.html")
