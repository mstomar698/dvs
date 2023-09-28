from django.http import HttpResponse
from django.shortcuts import render
from railmadad.models import Main_Data_Upload
from railmadad.constants import TRAIN_CATS
from railmadad.src.data.DBQuery import DBQuery
from railmadad.constants import rgd, rncc, dnr, pnbe, ppta, ipr, keu, mka, ara,other, ALL_TYPES, CRITICAL_TYPES
from datetime import datetime as dt, date
from django.contrib.auth.decorators import login_required
from pytz import timezone
from django_ratelimit.decorators import ratelimit
from s2analytica.common import log_time, getratelimit

import calendar

@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def max_complain_train(request):
    try:
        main_all = Main_Data_Upload.objects.all()
        train_numbers = []
        for m in main_all:
            train_numbers.append(m.train_station)
        train_numbers = list(Main_Data_Upload.objects.all().values_list('train_station',flat=True))
        # all_type = [
        #     "Coach - Cleanliness",
        #     "Bed Roll",
        #     "Security",
        #     "Medical Assistance",
        #     "Punctuality",
        #     "Water Availability",
        #     "Electrical Equipment",
        #     "Coach - Maintenance",
        #     "Miscellaneous",
        #     "Staff Behaviour",
        # ]
        # critical_type = [
        #     "Coach - Cleanliness",
        #     "Bed Roll",
        #     "Water Availability",
        #     "Electrical Equipment",
        #     "Coach - Maintenance",
        # ]
        train_numbers = set(train_numbers)
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
        corruption = []
        catering = []
        divyang = []
        women = []
        total = []
        checked = []
        # train checkbox status arrays ######################
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

        ######################################################
        check_type = []
        complain_category = []
        complain_type = []
        train_count = None
        trainsss = Main_Data_Upload.objects.all()
        main_trains = []
        for ttt in trainsss:
            main_trains.append(float(ttt.train_station))
        set_train = set(main_trains)
        main_train = list(set_train)

        if request.method == "POST":
            post = True
            start_date = request.POST.get("start_date", "")
            end_date = request.POST.get("end_date", "")
            complain_category = request.POST.getlist("complain-category")
            train_count = request.POST.get(
                "staff_count"
            )  # because of comp using staff_count
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

            for tn in train_number:
                checked.append(int(tn))

            if delta.days <= -1:
                return HttpResponse(
                    "<center><h1>Please Enter valid date Range</center></h1>"
                )

            for t_r in train_number:
                coach_clean_data = DBQuery.maximum_complain_train_clean_data(start_date,end_date,t_r)
                c1 = (int(coach_clean_data.count()), int(t_r), "Coach - Cleanliness")
                coach_clean.append(list(c1))

                bed_data = DBQuery.maximum_complain_train_bed_data(start_date,end_date,t_r)
                b1 = (int(bed_data.count()), int(t_r), "Bed Roll")
                bed_roll.append(list(b1))

                security_data =  DBQuery.maximum_complain_train_security_data(start_date,end_date,t_r)
                s1 = (int(security_data.count()), int(t_r), "Security")
                security.append(list(s1))

                medical_data = DBQuery.maximum_complain_train_medical_data(start_date,end_date,t_r)
                m1 = (int(medical_data.count()), int(t_r), "Medical Assistance")
                medical_assis.append(list(m1))

                punctuality_data = DBQuery.maximum_complain_train_punctuality_data(start_date,end_date,t_r)
                p1 = (int(punctuality_data.count()), int(t_r), "Punctuality")
                punctuality.append(list(p1))

                water_data = DBQuery.maximum_complain_train_water_data(start_date,end_date,t_r)
                w1 = (int(water_data.count()), int(t_r), "Water Availability")
                water_avail.append(list(w1))

                electrical_data = DBQuery.maximum_complain_train_electrical_data(start_date,end_date,t_r)
                e1 = (int(electrical_data.count()), int(t_r), "Electrical Equipment")
                electrical_equip.append(list(e1))

                coach_maintain_data = DBQuery.maximum_complain_train_maintain_data(start_date,end_date,t_r)
                c2 = (int(coach_maintain_data.count()), int(t_r), "Coach - Maintenance")
                coach_maintain.append(list(c2))

                miscellaneous_data = DBQuery.maximum_complain_train_miscellaneous_data(start_date,end_date,t_r)
                m2 = (int(miscellaneous_data.count()), int(t_r), "Miscellaneous")
                miscellaneous.append(list(m1))

                staff_behave_data = DBQuery.maximum_complain_train_behave_data(start_date,end_date,t_r)
                s2 = (int(staff_behave_data.count()), int(t_r), "Staff Behaviour")
                staff_behave.append(list(s2))

                corruption_data = DBQuery.maximum_complain_train_corruption_data(start_date,end_date,t_r)
                c3 = (int(corruption_data.count()), int(t_r), "Corruption Bribery")
                corruption.append(list(c3))
                
                catering_vending = DBQuery.maximum_complain_train_catering_vending_data(start_date,end_date,t_r)
                c4 = (
                    int(catering_vending.count()),
                    int(t_r),
                    "Catering and Vending Services",
                )
                catering.append(list(c4))

                divyang_fascilities = DBQuery.maximum_complain_train_divyang_fascilities_data(start_date,end_date,t_r)

                d1 = (int(divyang_fascilities.count()), int(t_r), "Divyangjan Facilities")
                divyang.append(list(d1))

                women_sp_need = DBQuery.maximum_complain_train_women_sp_need_data(start_date,end_date,t_r)
                wn1 = (
                    int(women_sp_need.count()),
                    int(t_r),
                    "Fascilities for Women with Special needs",
                )

                women.append(list(wn1))
        else:
            pass

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
        corruption.sort(key=lambda x: x[0])
        catering.sort(key=lambda x: x[0])
        divyang.sort(key=lambda x: x[0])
        women.sort(key=lambda x: x[0])

        if request.method == "POST":
            post = True
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
            if "Corruption Bribery" in complain_type:
                total.append(corruption[-1])
            if "Catering and Vending Services" in complain_type:
                total.append(catering[-1])
            if "Divyangjan Facilities" in complain_type:
                total.append(divyang[-1])
            if "Facilities for Women with Special needs" in complain_type:
                total.append(women[-1])

            if len(total) == 0:
                show = False
            if len(total) >= 1:
                show = True
        else:
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
            train_number=rncc

        context = {
            "post": post,
            "total": total,
            "all_type": ALL_TYPES,
            "critical_type": CRITICAL_TYPES,
            "start_date": start_date,
            "end_date": end_date,
            "main_train": main_train,
            "checked": checked,
            "check_type": check_type,
            "complain_category": complain_category,
            "complain_type": complain_type,
            "staff_count": train_count,
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
            "train_numbers": train_number
        }
        return render(request, "railmadad/max_complain_train.html", context)
    except:
        return render(request,"error.html")