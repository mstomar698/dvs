from django.http import HttpResponse
from django.shortcuts import render
from railmadad.models import Main_Data_Upload
from railmadad.constants import TRAIN_CATS
from railmadad.src.data.DBQuery import DBQuery
from railmadad.constants import rgd, rncc, dnr, pnbe, ppta, ipr, keu, mka, ara, other, ALL_TYPES, CRITICAL_TYPES
from datetime import datetime as dt, date
from django.contrib.auth.decorators import login_required
from pytz import timezone
from django_ratelimit.decorators import ratelimit
from s2analytica.common import log_time, getratelimit

import calendar

@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def max_complain_coach(request):
    try:
        # raise Exception("This is an example exception")
        main_all = Main_Data_Upload.objects.all()
        main_trains = []
        for ttt in main_all:
            main_trains.append(float(ttt.train_station))
        set_train = set(main_trains)
        main_train = list(set_train)
        coach = []
        for m in main_all:
            if m.physical_coach_number == float(0.0):
                pass
            else:
                coach.append(m.physical_coach_number)

        coaches_set = set(coach)
        coaches = list(coaches_set)

        coach_clean = []
        bed_roll = []
        security = []
        medical_assis = []
        punctuality = []
        water_avail = []
        electrical_equip = []
        coach_maintain = []
        miscellaneous = []
        staff_behave = []
        total = []
        complain_category = []
        complain_type = []
        check_type = None
        checked = []
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

        if request.method == "POST":
            post = True
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

            for train in train_number:
                checked.append(int(train))

            delta = end_month - start_month

            sdate = date(
                int(start_month.year), int(start_month.month), int(start_month.day)
            )
            edate = date(int(end_month.year), int(end_month.month), int(end_month.day))

            if delta.days <= -1:
                return HttpResponse(
                    "<center><h1>Please Enter valid date Range</center></h1>"
                )

            # NOTE: Assigning All references to None to prevent from reference before assignment error
            c1 = None
            b1 = None
            m1 = None
            p1 = None
            w1 = None
            e1 = None
            c2 = None
            m2 = None
            s2 = None

            DBQuery.clear_variables()

            for t_r in coaches:
                coach_clean = DBQuery.maximum_complain_coach_clean_data(start_date,end_date,t_r,checked)
                bed_roll = DBQuery.maximum_complain_coach_bed_data(start_date,end_date,t_r,checked)
                security = DBQuery.maximum_complain_coach_security_data(start_date,end_date,t_r,checked)
                medical_assis = DBQuery.maximum_complain_coach_medical_data(start_date,end_date,t_r,checked)
                punctuality = DBQuery.maximum_complain_coach_punctuality_data(start_date,end_date,t_r,checked)
                water_avail = DBQuery.maximum_complain_coach_water_data(start_date,end_date,t_r,checked)
                electrical_equip = DBQuery.maximum_complain_coach_electrical_data(start_date,end_date,t_r,checked)
                coach_maintain = DBQuery.maximum_complain_coach_maintain_data(start_date,end_date,t_r,checked)
                miscellaneous = DBQuery.maximum_complain_coach_miscellaneous_data(start_date,end_date,t_r,checked)
                staff_behave = DBQuery.maximum_complain_coach_behave_data(start_date,end_date,t_r,checked)
        if request.method != "POST":
            if len(total) == 0:
                show = False
            if len(total) >= 1:
                show = True
            
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
            # if "other" not in check_type:
            #     check_type.append("other")
            # if TRAIN_CATS[0] not in check_type:
            #     for tc in TRAIN_CATS:
            #         check_type.append(tc)
            
            train_number= rncc
            complain_type = CRITICAL_TYPES
        
        else:
            coach_maintain.sort(key=lambda x: x[0])
            bed_roll.sort(key=lambda x: x[0])
            coach_clean.sort(key=lambda x: x[0])
            staff_behave.sort(key=lambda x: x[0])
            electrical_equip.sort(key=lambda x: x[0])
            water_avail.sort(key=lambda x: x[0])
            punctuality.sort(key=lambda x: x[0])
            security.sort(key=lambda x: x[0])
            medical_assis.sort(key=lambda x: x[0])
            miscellaneous.sort(key=lambda x: x[0])

            if "Coach - Maintenance" in complain_type:
                total.append(coach_maintain[-1])
            if "Bed Roll" in complain_type:
                total.append(bed_roll[-1])
            if "Staff Behaviour" in complain_type:
                total.append(staff_behave[-1])
            if "Electrical Equipment" in complain_type:
                total.append(electrical_equip[-1])
            if "Water Availability" in complain_type:
                total.append(water_avail[-1])
            if "Punctuality" in complain_type:
                total.append(punctuality[-1])
            if "Security" in complain_type:
                total.append(security[-1])
            if "Medical Assistance" in complain_type:
                total.append(medical_assis[-1])
            if "Miscellaneous" in complain_type:
                total.append(miscellaneous[-1])
            if "Coach - Cleanliness" in complain_type:
                total.append(coach_clean[-1])
            if len(total) == 0:
                show = False
            if len(total) >= 1:
                show = True

        context = {
            "post": post,
            "total": total,
            "show": show,
            "all_type": ALL_TYPES,
            "critical_type": CRITICAL_TYPES,
            "start_date": start_date,
            "end_date": end_date,
            "complain_type": complain_type,
            "complain_category": complain_category,
            "trains_cat": TRAIN_CATS,
            "main_train": main_train,
            "checked": checked,
            "check_type": check_type,
            "complain_type": complain_type,
            "complain_category": complain_category,
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
            "train_numbers":train_number
        }
        return render(request, "railmadad/max_complain_coach.html", context)
    except:
        return render(request,"error.html")