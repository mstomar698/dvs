from django.http import HttpResponse
from django.shortcuts import render
from railmadad.models import Main_Data_Upload, Train_Type
from railmadad.constants import other
from railmadad.src.data.DBQuery import DBQuery

from datetime import datetime as dt, date
from s2analytica.common import log_time, getratelimit
from s2analytica.settings import START_TIME, END_TIME, IST
from django.contrib.auth.decorators import login_required
from pytz import timezone
from django_ratelimit.decorators import ratelimit

import calendar

@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def mix_coach_graph(request):
    try:
        bottom_train = []
        bottom_data_count = []
        trainsss = Main_Data_Upload.objects.all()
        main_trains = []
        for ttt in trainsss:
            main_trains.append(float(ttt.train_station))
        set_train = set(main_trains)
        main_train = list(set_train)
        checked = []

        all_type = [
            "Coach - Cleanliness",
            "Bed Roll",
            "Security",
            "Punctuality",
            "Water Availability",
            "Electrical Equipment",
            "Medical Assistance",
            "Coach - Maintenance",
            "Miscellaneous",
            "Staff Behaviour",
            "Corruption Bribery",
            "Catering and Vending Services",
            "Divyangjan Facilities",
            "Facilities for Women with Special needs",
        ]

        TRAIN_CATS = ["all", "rncc", "rgd", "dnr", "pnbe", "ppta", "ipr", "keu", "mka", "ara"]

        critical_type = [
            "Coach - Cleanliness",
            "Bed Roll",
            "Water Availability",
            "Electrical Equipment",
            "Coach - Maintenance",
        ]

        color_code = [
            "#FF3838",
            "#FFB3B3",
            "#006441",
            "#FF8300",
            "#EEFF70",
            "#00FF83",
            "#00E8FF",
            "#4200FF",
            "#BD00FF",
            "#747474",
            "#1D0249",
            "#5F0037",
            "#D33737",
            "#00766B",
        ]
        coach_clean = []
        bed_roll = []
        security = []
        medical_assis = []
        punctuality = []
        water_avail = []
        electrical_equip = []
        coach_maintain = []
        miscellaneous = []

        ### new complain Type ####
        Corruption_Bribery = []
        Catering_and_Vending_Services = []
        Divyangjan_Facilities = []
        Facilities_for_Women_with_Special_needs = []

        total_entries = Main_Data_Upload.objects.count()
        staff_behave = []
        # train checkbox status arrays ######################
        rncc = []
        rgd = []
        dnr = []
        pnbe = []
        ppta = []
        ipr = []
        keu = []
        mka = []
        ara = []
        # checkbox status data objects #######################
        train_type_rncc = Train_Type.objects.filter(Type="RNCC")
        train_type_rgd = Train_Type.objects.filter(Type="RGD")
        train_type_dnr = Train_Type.objects.filter(Type="DNR")
        train_type_pnbe = Train_Type.objects.filter(Type="PNBE")
        train_type_ppta = Train_Type.objects.filter(Type="PPTA")
        train_type_ipr = Train_Type.objects.filter(Type="IPR")
        train_type_keu = Train_Type.objects.filter(Type="KEU")
        train_type_mka = Train_Type.objects.filter(Type="MKA")
        train_type_ara = Train_Type.objects.filter(Type="ARA")
        # train checkbox status loops to append into arrays ##
        for rncc_train in train_type_rncc:
            rncc.append(rncc_train.train_number)

        for rgd_train in train_type_rgd:
            rgd.append(rgd_train.train_number)

        for dnr_train in train_type_dnr:
            dnr.append(dnr_train.train_number)

        for pnbe_train in train_type_pnbe:
            pnbe.append(pnbe_train.train_number)

        for ppta_train in train_type_ppta:
            ppta.append(ppta_train.train_number)

        for ipr_train in train_type_ipr:
            ipr.append(ipr_train.train_number)

        for keu_train in train_type_keu:
            keu.append(keu_train.train_number)

        for mka_train in train_type_mka:
            mka.append(mka_train.train_number)

        for ara_train in train_type_ara:
            ara.append(ara_train.train_number)

        if request.method == "POST":
            post = True
            complain_category = request.POST.getlist("complain-category")
            start_date = request.POST.get("start_date", "")
            end_date = request.POST.get("end_date", "")
            count =  int(request.POST.get('staff_count',''))

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

            if delta.days <= -1:
                return HttpResponse("<h1>Please Enter valid Date Range</h1>")

            data_count = []

            # print(train_number)
            # print(train_number)

            problem_type = Main_Data_Upload.objects.values_list("problem_type")
            all_data_main_data_upload = set(Main_Data_Upload.objects.filter(train_station__in=train_number,problem_type__in=complain_type,registration_date__range=[dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),f"{end_date} {END_TIME}+00:00"]))


            str_train_number = []
            for t_n in train_number:
                str_train_number.append(str(t_n))

            for train in train_number:
                checked.append(int(train))

            
            all_coaches_set=[]
            for mn in all_data_main_data_upload:
                if mn.physical_coach_number == float(0.0):
                    pass
                else:
                    all_coaches_set.append(str(mn.physical_coach_number))

            all_coaches_list = set(all_coaches_set)
            all_coaches_lists = list(all_coaches_list)

            main_sorted_data = []
            try: 
                main_sorted_data = DBQuery.physical_coach_number_wise_complain_mix_main_data(complain_type, all_coaches_lists,start_date, end_date)
            except Exception as e:
                pass

            first_n = []
            for m in main_sorted_data:
                try:
                    first_n.append(int(m['physical_coach_number']))
                except Exception as e:
                    pass

            DBQuery.clear_variables()
            
            for r in first_n:
                bottom_train.append(int(r))
                coach_clean = DBQuery.physical_coach_number_wise_complain_mix_clean_data(r,start_date, end_date)

                bed_roll =  DBQuery.physical_coach_number_wise_complain_mix_bed_data(r,start_date, end_date)

                security = DBQuery.physical_coach_number_wise_complain_mix_security_data(r,start_date, end_date)

                medical_assis = DBQuery.physical_coach_number_wise_complain_mix_medical_data(r,start_date, end_date)

                punctuality = DBQuery.physical_coach_number_wise_complain_mix_punctuality_data(r,start_date, end_date)

                water_avail = DBQuery.physical_coach_number_wise_complain_mix_water_data(r,start_date, end_date)

                electrical_equip = DBQuery.physical_coach_number_wise_complain_mix_electrical_data(r,start_date, end_date)

                coach_maintain = DBQuery.physical_coach_number_wise_complain_mix_coach_maintain_data(r,start_date, end_date)

                miscellaneous = DBQuery.physical_coach_number_wise_complain_mix_miscellaneous_data(r,start_date, end_date)

                staff_behave =  DBQuery.physical_coach_number_wise_complain_mix_behave_data(r,start_date, end_date)

                Corruption_Bribery = DBQuery.physical_coach_number_wise_complain_mix_Corruption_Bribery_data(r,start_date, end_date)

                Catering_and_Vending_Services = DBQuery.physical_coach_number_wise_complain_mix_catering_data(r,start_date, end_date)

                Divyangjan_Facilities = DBQuery.physical_coach_number_wise_complain_mix_divyang_data(r,start_date, end_date)
                
                Facilities_for_Women_with_Special_needs = DBQuery.physical_coach_number_wise_complain_mix_women_data(r,start_date, end_date)
            # print(bottom_train)
        else:
            train_count = None
        total =[]
        if request.method == "POST":
            if "Coach - Cleanliness" in complain_type:
                total.append(coach_clean)
            if "Bed Roll" in complain_type:
                total.append(bed_roll)
            if "Water Availability" in complain_type:
                total.append(water_avail)
            if "Electrical Equipment" in complain_type:
                total.append(electrical_equip)
            if "Coach - Maintenance" in complain_type:
                total.append(coach_maintain)
            if "Security" in complain_type:
                total.append(security)
            if "Punctuality" in complain_type:
                total.append(punctuality)
            if "Medical Assistance" in complain_type:
                total.append(medical_assis)
            if "Miscellaneous" in complain_type:
                total.append(miscellaneous)
            if "Staff Behaviour" in complain_type:
                total.append(staff_behave)

            ### New Complain Type ########
            if "Corruption Bribery" in complain_type:
                total.append(Corruption_Bribery)

            if "Catering and Vending Services" in complain_type:
                total.append(Catering_and_Vending_Services)

            if "Divyangjan Facilities" in complain_type:
                total.append(Divyangjan_Facilities)

            if "Facilities for Women with Special needs" in complain_type:
                total.append(Facilities_for_Women_with_Special_needs)

            if len(total) == 0:
                show = False
            if len(total) >= 1:
                show = True
        if request.method != "POST":
            post = False
            count = None
            complain_type = critical_type
            check_type = ['rncc']
            complain_category=None
            all_coaches_lists = None
            train_number = rncc

            # if "other" not in check_type:
            #     check_type.append("other")
            # if TRAIN_CATS[0] not in check_type:
            #     for tc in TRAIN_CATS:
            #         check_type.append(tc)

            current_time_get = dt.now(timezone("Asia/Kolkata"))
            
            if(current_time_get.day > calendar.monthrange(current_time_get.year, current_time_get.month - 1)[1]):
                default_start = dt(current_time_get.year, current_time_get.month - 1, calendar.monthrange(current_time_get.year, current_time_get.month - 1)[1], 0, 0)
            
            else:
                default_start = dt(current_time_get.year, current_time_get.month - 1, current_time_get.day, 0, 0)
            
            start_date = default_start.strftime('%Y-%m-%d')
            end_date = current_time_get.strftime('%Y-%m-%d')
        else:
            train_count = len(train_number)

        context = {
            "bottom_train": bottom_train,
            "post": post,
            "train_count": train_count,
            "total": total,
            "all_type": all_type,
            "critical_type": critical_type,
            "color_code": color_code,
            "total_entries": total_entries,
            "start_date": start_date,
            "end_date": end_date,
            "color_code": color_code,
            "main_train": main_train,
            "checked": checked,
            "check_type": check_type,
            "complain_category": complain_category,
            "complain_type": complain_type,
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
            'staff_count':count,
            'all_coaches_lists':all_coaches_lists,
            "train_numbers" : train_number
        }
        print(train_number)
        return render(request, 'railmadad/mix_coach_graph.html',context)
    except:
        return render(request,"error.html")