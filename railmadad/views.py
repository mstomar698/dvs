from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Main_Data_Upload, Train_Type
from datetime import datetime as dt, date
from s2analytica.settings import IST, START_TIME, END_TIME
from railmadad.constants import ALL_TYPES, TRAIN_CATS, CRITICAL_TYPES
from django.contrib import messages

# Create your views here.
@login_required
def train_wise_data(request):
    try:
        data_count = []
        checked = []
        check_type = []
        complain_category = []
        problem_type = Main_Data_Upload.objects.values_list("problem_type")
        train_numbers_list = Main_Data_Upload.objects.values_list("train_station")
        Type = []
        trainsss = Main_Data_Upload.objects.all()
        main_trains = []
        for ttt in trainsss:
            main_trains.append(float(ttt.train_station))
        set_train = set(main_trains)
        main_train = list(set_train)
        for s in problem_type:
            for t in s:
                Type.append(t)

        train = []
        for tr_numbers in train_numbers_list:
            train.append(tr_numbers)
        train_numbers = set(train)

        problem_type = set(Type)

        complain_type = []
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
        trains = []
        data_show = False
        start_date = None
        end_date = None
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

        ######################################################
        total = []
        if request.method == "POST":
            train_number = request.POST.getlist("train_number")
            start_date = request.POST.get("start_date", "")
            end_date = request.POST.get("end_date", "")
            complain_type = request.POST.getlist("complain_type")
            complain_category = request.POST.getlist("complain-category")
            check_type = request.POST.getlist("check-type")

            if "Coach - Cleanliness" in complain_type:
                total.append("Coach - Cleanliness")
            if "Bed Roll" in complain_type:
                total.append("Bed Roll")
            if "Water Availability" in complain_type:
                total.append("Water Availability")
            if "Coach - Maintenance" in complain_type:
                total.append("Coach - Maintenance")
            if "Electrical Equipment" in complain_type:
                total.append("Electrical Equipment")
            if "Staff Behaviour" in complain_type:
                total.append("Staff Behaviour")
            if "Miscellaneous" in complain_type:
                total.append("Miscellaneous")
            if "Security" in complain_type:
                total.append("Security")
            if "Catering and Vending Services" in complain_type:
                total.append("Catering and Vending Services")
            if "Divyangjan Facilities" in complain_type:
                total.append("Divyangjan Facilities")
            if "Medical Assistance" in complain_type:
                total.append("Medical Assistance")
            if "Punctuality" in complain_type:
                total.append("Punctuality")
            if "Facilities for Women with Special needs" in complain_type:
                total.append("Facilities for Women with Special needs")
            if "Corruption Bribery" in complain_type:
                total.append("Corruption Bribery")

            start_month = dt.strptime(start_date, "%Y-%m-%d")
            end_month = dt.strptime(end_date, "%Y-%m-%d")

            delta = end_month - start_month

            sdate = date(
                int(start_month.year), int(start_month.month), int(start_month.day)
            )
            edate = date(int(end_month.year), int(
                end_month.month), int(end_month.day))

            if delta.days <= -1:
                return HttpResponse("<h1>Please Enter valid Date Range</h1>")

            for t_r in train_number:
                trains.append(int(t_r))
                checked.append(int(t_r))

            for p_t in total:
                data = Main_Data_Upload.objects.filter(
                    train_station__in=trains,
                    problem_type=p_t,
                    registration_date__range=[
                        dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    ],
                )
                data_count.append(data.count())

            if sum(data_count) == 0:
                data_show = False
            else:
                data_show = True

            if request.method != "POST":
                start_date = None
                end_date = None
                post = False

        else:
            post = False

        context = {
            "problem_type": problem_type,
            "post": True,
            "data_count": data_count,
            "train": trains,
            "data_show": data_show,
            "train_number": train_numbers,
            "start_date": start_date,
            "end_date": end_date,
            "checked": checked,
            "check_type": check_type,
            "complain_category": complain_category,
            "main_trains": main_trains,
            "rgd": rgd,
            "rncc": rncc,
            "dnr": dnr,
            "pnbe": pnbe,
            "ppta": ppta,
            "ipr": ipr,
            "keu": keu,
            "mka": mka,
            "ara": ara,
            "trains_cat": TRAIN_CATS,
            "all_type": ALL_TYPES,
            "critical_type": CRITICAL_TYPES,
            "complain_type": complain_type,
        }

        return render(request, "railmadad/train_wise_data.html", context)
    except:
        return render(request,"error.html")

@login_required
def bottom_train_data_pie(request):
    try:
        bottom_train = []
        bottom_data_count = []
        complain_type = []
        complain_category = []
        trainsss = Main_Data_Upload.objects.all()
        main_trains = []
        for ttt in trainsss:
            main_trains.append(float(ttt.train_station))
        set_train = set(main_trains)
        main_train = list(set_train)
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

        ######################################################

        checked = []
        check_type = None

        if request.method == "POST":
            post = True
            train_number = request.POST.getlist("train_number")
            start_date = request.POST.get("start_date", "")
            end_date = request.POST.get("end_date", "")
            check_type = request.POST.getlist("check-type")
            complain_type = request.POST.getlist("complain_type")
            complain_category = request.POST.getlist("complain-category")

            start_month = dt.strptime(start_date, "%Y-%m-%d")
            end_month = dt.strptime(end_date, "%Y-%m-%d")

            delta = end_month - start_month

            sdate = date(
                int(start_month.year), int(start_month.month), int(start_month.day)
            )
            edate = date(int(end_month.year), int(
                end_month.month), int(end_month.day))

            if delta.days <= -1:
                return HttpResponse("<h1>Please Enter valid Date Range</h1>")

            data_count = []
            problem_type = Main_Data_Upload.objects.values_list("problem_type")
            # train_numbers = Main_Data_Upload.objects.all()

            Type = []
            for s in problem_type:
                for t in s:
                    Type.append(t)

            # train_number = []
            str_train_number = []
            for t_n in train_number:
                str_train_number.append(str(t_n))
                checked.append(int(t_n))

            problem_types = set(Type)

            for tr_n in train_number:
                a = Main_Data_Upload.objects.filter(
                    problem_type__in=complain_type,
                    train_station=tr_n,
                    registration_date__range=[
                        dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    ],
                )
                data_count.append(a.count())

            make_dict = dict(zip(str_train_number, data_count))
            a1_sorted_keys = sorted(make_dict, key=make_dict.get, reverse=True)
            for r in a1_sorted_keys:
                bottom_train.append(int(float(r)))
                bottom_data_count.append(make_dict[r])

        else:
            train_count = 10
            post = False
            data_count = []
            start_date = None
            end_date = None
            post = False

        context = {
            "bottom_train": bottom_train,
            "post": post,
            "bottom_data_count": bottom_data_count,
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
            "trains_cat": TRAIN_CATS,
            "all_type": ALL_TYPES,
            "critical_type": CRITICAL_TYPES,
            "complain_type": complain_type,
            "complain_category": complain_category,
        }
        return render(request, "railmadad/bottom_train_data_pie.html", context)
    except:
        return render(request,"error.html")

@login_required
def bottom_train_data_bar(request):
    try:
        bottom_train = []
        bottom_data_count = []
        complain_type = []
        complain_category = []
        trainsss = Main_Data_Upload.objects.all()
        main_trains = []
        for ttt in trainsss:
            main_trains.append(float(ttt.train_station))
        set_train = set(main_trains)
        main_train = list(set_train)
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

        ######################################################

        checked = []
        check_type = None

        if request.method == "POST":
            post = True
            train_number = request.POST.getlist("train_number")
            start_date = request.POST.get("start_date", "")
            end_date = request.POST.get("end_date", "")
            check_type = request.POST.getlist("check-type")
            complain_type = request.POST.getlist("complain_type")
            complain_category = request.POST.getlist("complain-category")
            start_month = dt.strptime(start_date, "%Y-%m-%d")
            end_month = dt.strptime(end_date, "%Y-%m-%d")

            delta = end_month - start_month

            sdate = date(
                int(start_month.year), int(start_month.month), int(start_month.day)
            )
            edate = date(int(end_month.year), int(
                end_month.month), int(end_month.day))

            if delta.days <= -1:
                return HttpResponse("<h1>Please Enter valid Date Range</h1>")

            data_count = []
            problem_type = Main_Data_Upload.objects.values_list("problem_type")
            # train_numbers = Main_Data_Upload.objects.all()

            Type = []
            for s in problem_type:
                for t in s:
                    Type.append(t)

            # train_number = []
            str_train_number = []
            for t_n in train_number:
                str_train_number.append(str(t_n))
                checked.append(int(t_n))

            problem_types = set(Type)

            for tr_n in train_number:
                a = Main_Data_Upload.objects.filter(
                    problem_type__in=complain_type,
                    train_station=tr_n,
                    registration_date__range=[
                        dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    ],
                )
                data_count.append(a.count())

            make_dict = dict(zip(str_train_number, data_count))
            a1_sorted_keys = sorted(make_dict, key=make_dict.get, reverse=True)
            for r in a1_sorted_keys:
                bottom_train.append(int(float(r)))
                bottom_data_count.append(make_dict[r])

        else:
            train_count = 10
            post = False
            data_count = []
            problem_type = Main_Data_Upload.objects.values_list("problem_type")
            train_numbers = Main_Data_Upload.objects.all()

            Type = []
            for s in problem_type:
                for t in s:
                    Type.append(t)

            train_number = []
            str_train_number = []
            for t_n in train_numbers:
                train_number.append(t_n.train_station)
                str_train_number.append(str(t_n.train_station))

            problem_types = set(Type)

            for tr_n in train_number:
                a = Main_Data_Upload.objects.filter(
                    problem_type__in=complain_type, train_station=tr_n
                )
                data_count.append(a.count())

            make_dict = dict(zip(str_train_number, data_count))
            a1_sorted_keys = sorted(make_dict, key=make_dict.get, reverse=True)
            for r in a1_sorted_keys:
                bottom_train.append(int(float(r)))
                bottom_data_count.append(make_dict[r])

        if request.method != "POST":
            start_date = None
            end_date = None
            post = False
            real_train_count = train_count
        else:
            real_train_count = len(train_number)

        if real_train_count == 0:
            messages.error(
                request, "Please Select Any Train Number To See The Filtered Data"
            )
            return redirect(request.path)
        else:
            pass

        context = {
            "bottom_train": bottom_train[0:real_train_count],
            "post": post,
            "bottom_data_count": bottom_data_count[0:real_train_count],
            "train_count": real_train_count,
            "start_date": start_date,
            "end_date": end_date,
            "main_train": main_train,
            "check_type": check_type,
            "checked": checked,
            "rgd": rgd,
            "rncc": rncc,
            "dnr": dnr,
            "pnbe": pnbe,
            "ppta": ppta,
            "ipr": ipr,
            "keu": keu,
            "mka": mka,
            "ara": ara,
            "trains_cat": TRAIN_CATS,
            "all_type": ALL_TYPES,
            "critical_type": CRITICAL_TYPES,
            "complain_type": complain_type,
            "complain_category": complain_category,
        }
        return render(request, "railmadad/bottom_train_data_bar.html", context)

    except:
        return render(request,"error.html")

@login_required
def all_complain_train(request):
    try:
        train_numbers_list = Main_Data_Upload.objects.values_list("train_station")
        train = []
        complain_type = []
        complain_category = []

        for tr_numbers in train_numbers_list:
            train.append(tr_numbers)
        train_num = set(train)
        train_numbers = []
        for t_numbers in train_num:
            for tt in t_numbers:
                train_numbers.append(tt)

        trainsss = Main_Data_Upload.objects.all()
        main_trains = []
        for ttt in trainsss:
            main_trains.append(float(ttt.train_station))
        set_train = set(main_trains)
        main_train = list(set_train)
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

        ######################################################

        checked = []
        check_type = None

        if request.method == "POST":
            post = True
            train_number = request.POST.getlist("train_number")
            start_date = request.POST.get("start_date", "")
            end_date = request.POST.get("end_date", "")
            check_type = request.POST.getlist("check-type")
            complain_type = request.POST.getlist("complain_type")
            complain_category = request.POST.getlist("complain-category")
            start_month = dt.strptime(start_date, "%Y-%m-%d")
            end_month = dt.strptime(end_date, "%Y-%m-%d")

            delta = end_month - start_month

            sdate = date(
                int(start_month.year), int(start_month.month), int(start_month.day)
            )
            edate = date(int(end_month.year), int(
                end_month.month), int(end_month.day))

            ######
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

            ## New Complain Type ####
            Corruption_Bribery = []
            Catering_and_Vending_Services = []
            Divyangjan_Facilities = []
            Facilities_for_Women_with_Special_needs = []
            ##

            dates = []

            for t_n in train_number:
                checked.append(int(t_n))

            ########

            if delta.days <= -1:
                return HttpResponse(
                    "<center><h1>Please Enter Right Date Range</h1></center>"
                )

            else:
                for t_r in train_number:

                    coach_clean_data = Main_Data_Upload.objects.filter(
                        registration_date__range=[
                            dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        ],
                        train_station=t_r,
                        problem_type="Coach - Cleanliness",
                    )
                    coach_clean.append(coach_clean_data.count())

                    bed_data = Main_Data_Upload.objects.filter(
                        registration_date__range=[
                            dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        ],
                        train_station=t_r,
                        problem_type="Bed Roll",
                    )
                    bed_roll.append(bed_data.count())

                    security_data = Main_Data_Upload.objects.filter(
                        registration_date__range=[
                            dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        ],
                        train_station=t_r,
                        problem_type="Security",
                    )
                    security.append(security_data.count())

                    medical_data = Main_Data_Upload.objects.filter(
                        registration_date__range=[
                            dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        ],
                        train_station=t_r,
                        problem_type="Medical Assistance",
                    )
                    medical_assis.append(medical_data.count())

                    punctuality_data = Main_Data_Upload.objects.filter(
                        registration_date__range=[
                            dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        ],
                        train_station=t_r,
                        problem_type="Punctuality",
                    )
                    punctuality.append(punctuality_data.count())

                    water_data = Main_Data_Upload.objects.filter(
                        registration_date__range=[
                            dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        ],
                        train_station=t_r,
                        problem_type="Water Availability",
                    )
                    water_avail.append(water_data.count())

                    electrical_data = Main_Data_Upload.objects.filter(
                        registration_date__range=[
                            dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        ],
                        train_station=t_r,
                        problem_type="Electrical Equipment",
                    )
                    electrical_equip.append(electrical_data.count())

                    coach_maintain_data = Main_Data_Upload.objects.filter(
                        registration_date__range=[
                            dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        ],
                        train_station=t_r,
                        problem_type="Coach - Maintenance",
                    )
                    coach_maintain.append(coach_maintain_data.count())

                    miscellaneous_data = Main_Data_Upload.objects.filter(
                        registration_date__range=[
                            dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        ],
                        train_station=t_r,
                        problem_type="Miscellaneous",
                    )
                    miscellaneous.append(miscellaneous_data.count())

                    staff_behave_data = Main_Data_Upload.objects.filter(
                        registration_date__range=[
                            dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        ],
                        train_station=t_r,
                        problem_type="Staff Behaviour",
                    )
                    staff_behave.append(staff_behave_data.count())

                    data11 = Main_Data_Upload.objects.filter(
                        registration_date__range=[
                            dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        ],
                        train_station=t_r,
                        problem_type="Corruption Bribery",
                    )
                    Corruption_Bribery.append(data11.count())

                    data12 = Main_Data_Upload.objects.filter(
                        registration_date__range=[
                            dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        ],
                        train_station=t_r,
                        problem_type="Catering and Vending Services",
                    )
                    Catering_and_Vending_Services.append(data12.count())

                    data13 = Main_Data_Upload.objects.filter(
                        registration_date__range=[
                            dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        ],
                        train_station=t_r,
                        problem_type="Divyangjan Facilities",
                    )
                    Divyangjan_Facilities.append(data13.count())

                    data14 = Main_Data_Upload.objects.filter(
                        registration_date__range=[
                            dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        ],
                        train_station=t_r,
                        problem_type="Facilities for Women with Special needs",
                    )
                    Facilities_for_Women_with_Special_needs.append(data14.count())

        else:
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

            ## New Complain Type ####
            Corruption_Bribery = []
            Catering_and_Vending_Services = []
            Divyangjan_Facilities = []
            Facilities_for_Women_with_Special_needs = []
            ##

            dates = []
            post = False
            for t_r in train_numbers:
                coach_clean_data = Main_Data_Upload.objects.filter(
                    train_station=t_r, problem_type="Coach - Cleanliness"
                )
                coach_clean.append(coach_clean_data.count())

                bed_data = Main_Data_Upload.objects.filter(
                    train_station=t_r, problem_type="Bed Roll"
                )
                bed_roll.append(bed_data.count())

                security_data = Main_Data_Upload.objects.filter(
                    train_station=t_r, problem_type="Security"
                )
                security.append(security_data.count())

                medical_data = Main_Data_Upload.objects.filter(
                    train_station=t_r, problem_type="Medical Assistance"
                )
                medical_assis.append(medical_data.count())

                punctuality_data = Main_Data_Upload.objects.filter(
                    train_station=t_r, problem_type="Punctuality"
                )
                punctuality.append(punctuality_data.count())

                water_data = Main_Data_Upload.objects.filter(
                    train_station=t_r, problem_type="Water Availability"
                )
                water_avail.append(water_data.count())

                electrical_data = Main_Data_Upload.objects.filter(
                    train_station=t_r, problem_type="Electrical Equipment"
                )
                electrical_equip.append(electrical_data.count())

                medical_data = Main_Data_Upload.objects.filter(
                    train_station=t_r, problem_type="Medical Assistance"
                )
                medical_assis.append(medical_data.count())

                coach_maintain_data = Main_Data_Upload.objects.filter(
                    train_station=t_r, problem_type="Coach - Maintenance"
                )
                coach_maintain.append(coach_maintain_data.count())

                miscellaneous_data = Main_Data_Upload.objects.filter(
                    train_station=t_r, problem_type="Miscellaneous"
                )
                miscellaneous.append(miscellaneous_data.count())

                staff_behave_data = Main_Data_Upload.objects.filter(
                    train_station=t_r, problem_type="Staff Behaviour"
                )
                staff_behave.append(staff_behave_data.count())

                data11 = Main_Data_Upload.objects.filter(
                    train_station=t_r, problem_type="Corruption Bribery"
                )
                Corruption_Bribery.append(data11.count())

                data12 = Main_Data_Upload.objects.filter(
                    train_station=t_r, problem_type="Catering and Vending Services"
                )
                Catering_and_Vending_Services.append(data12.count())

                data13 = Main_Data_Upload.objects.filter(
                    train_station=t_r, problem_type="Divyangjan Facilities"
                )
                Divyangjan_Facilities.append(data13.count())

                data14 = Main_Data_Upload.objects.filter(
                    train_station=t_r,
                    problem_type="Facilities for Women with Special needs",
                )
                Facilities_for_Women_with_Special_needs.append(data14.count())

        total = []
        if request.method != "POST":
            total.append(coach_clean)
            total.append(bed_roll)
            total.append(security)
            total.append(punctuality)
            total.append(water_avail)
            total.append(electrical_equip)
            total.append(medical_assis)
            total.append(coach_maintain)
            total.append(miscellaneous)
            total.append(staff_behave)

            ## New Complain Type ####

            total.append(Corruption_Bribery)
            total.append(Catering_and_Vending_Services)
            total.append(Divyangjan_Facilities)
            total.append(Facilities_for_Women_with_Special_needs)
        else:
            if "Coach - Cleanliness" in complain_type:
                total.append(coach_clean)
            if "Bed Roll" in complain_type:
                total.append(bed_roll)
            if "Security" in complain_type:
                total.append(security)
            if "Punctuality" in complain_type:
                total.append(punctuality)
            if "Water Availability" in complain_type:
                total.append(water_avail)
            if "Electrical Equipment" in complain_type:
                total.append(electrical_equip)
            if "Medical Assistance" in complain_type:
                total.append(medical_assis)
            if "Coach - Maintenance" in complain_type:
                total.append(coach_maintain)
            if "Miscellaneous" in complain_type:
                total.append(miscellaneous)
            if "Staff Behaviour" in complain_type:
                total.append(staff_behave)
            if "Corruption Bribery" in complain_type:
                total.append(Corruption_Bribery)
            if "Catering and Vending Services" in complain_type:
                total.append(Catering_and_Vending_Services)
            if "Divyangjan Facilities" in complain_type:
                total.append(Divyangjan_Facilities)
            if "Facilities for Women with Special needs" in complain_type:
                total.append(Facilities_for_Women_with_Special_needs)

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

        # sub_type = Main_Data_Upload.objects.values_list('sub_type')
        # subtype = []
        # for s in sub_type:
        #     for st in s:
        #         subtype.append(st)

        # main_sub_type = []
        # for sub in subtype:
        #     main_sub_type.append(sub.split('/'))
        # for i in range(len(main_sub_type)):
        #     if len(main_sub_type[i]) >= 2:
        #         subtype[i] = " ".join(main_sub_type[i])

        # sts = (set(subtype))
        # demo_sub = set(sub_type)

        if request.method != "POST":
            start_date = None
            end_date = None
            post = False
            real_train_number = train_numbers
            complain_type = all_type
            complain_type.reverse()
        else:
            real_train_number = train_number
            complain_type.reverse()

        context = {
            "show": True,
            "post": post,
            "coach_clean": coach_clean,
            "bed_roll": bed_roll,
            "security": security,
            "medical_assis": medical_assis,
            "punctuality": punctuality,
            "water_avail": water_avail,
            "electrical_equip": electrical_equip,
            "coach_maintain": coach_maintain,
            "miscellaneous": miscellaneous,
            "staff_behave": staff_behave,
            "dates": dates,
            "total": total,
            # 'sub_type': sts,
            # 'demo_sub': demo_sub,
            "train_number": real_train_number,
            "start_date": start_date,
            "end_date": end_date,
            "main_train": main_train,
            "check_type": check_type,
            "checked": checked,
            "rgd": rgd,
            "rncc": rncc,
            "dnr": dnr,
            "pnbe": pnbe,
            "ppta": ppta,
            "ipr": ipr,
            "keu": keu,
            "mka": mka,
            "ara": ara,
            "trains_cat": TRAIN_CATS,
            "all_type": ALL_TYPES,
            "critical_type": CRITICAL_TYPES,
            "Corruption Bribery": Corruption_Bribery,
            "Catering and Vending Services": Catering_and_Vending_Services,
            "Divyangjan Facilities": Divyangjan_Facilities,
            "Facilities for Women with Special needs": Facilities_for_Women_with_Special_needs,
            "complain_type": complain_type,
            "complain_category": complain_category,
        }
        return render(request, "railmadad/all_complain_train.html", context)
    except:
        return render(request,"error.html")


@login_required
def min_complain_train(request):
    try:
        main_all = Main_Data_Upload.objects.all()
        train_numbers = []
        for m in main_all:
            train_numbers.append(m.train_station)
        all_type = [
            "Coach - Cleanliness",
            "Bed Roll",
            "Security",
            "Medical Assistance",
            "Punctuality",
            "Water Availability",
            "Electrical Equipment",
            "Coach - Maintenance",
            "Miscellaneous",
            "Staff Behaviour",
        ]
        critical_type = [
            "Coach - Cleanliness",
            "Bed Roll",
            "Water Availability",
            "Electrical Equipment",
            "Coach - Maintenance",
        ]
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
        total = []
        checked = []
        complain_type = []
        check_type = []
        complain_category = []
        trainsss = Main_Data_Upload.objects.all()
        main_trains = []
        for ttt in trainsss:
            main_trains.append(float(ttt.train_station))
        set_train = set(main_trains)
        main_train = list(set_train)
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

        ######################################################

        if request.method == "POST":
            post = True
            train_number = request.POST.getlist("train_number")
            complain_type = request.POST.getlist("complain_type")
            start_date = request.POST.get("start_date", "")
            end_date = request.POST.get("end_date", "")
            check_type = request.POST.getlist("check-type")
            complain_category = request.POST.getlist("complain-category")
            start_month = dt.strptime(start_date, "%Y-%m-%d")
            end_month = dt.strptime(end_date, "%Y-%m-%d")
            for train in train_number:
                checked.append(int(train))

            delta = end_month - start_month

            sdate = date(
                int(start_month.year), int(start_month.month), int(start_month.day)
            )
            edate = date(int(end_month.year), int(
                end_month.month), int(end_month.day))

            for train in train_number:
                checked.append(int(train))

            if delta.days <= -1:
                return HttpResponse(
                    "<center><h1>Please Enter valid date Range</center></h1>"
                )

            for t_r in train_number:
                coach_clean_data = Main_Data_Upload.objects.filter(
                    registration_date__range=[
                        dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    ],
                    train_station=t_r,
                    problem_type="Coach - Cleanliness",
                )
                c1 = (int(coach_clean_data.count()),
                    int(t_r), "Coach - Cleanliness")
                coach_clean.append(list(c1))

                bed_data = Main_Data_Upload.objects.filter(
                    registration_date__range=[
                        dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    ],
                    train_station=t_r,
                    problem_type="Bed Roll",
                )
                b1 = (int(bed_data.count()), int(t_r), "Bed Roll")
                bed_roll.append(list(b1))

                security_data = Main_Data_Upload.objects.filter(
                    registration_date__range=[
                        dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    ],
                    train_station=t_r,
                    problem_type="Security",
                )
                s1 = (int(security_data.count()), int(t_r), "Security")
                security.append(list(s1))

                medical_data = Main_Data_Upload.objects.filter(
                    registration_date__range=[
                        dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    ],
                    train_station=t_r,
                    problem_type="Medical Assistance",
                )
                m1 = (int(medical_data.count()), int(t_r), "Medical Assistance")
                medical_assis.append(list(m1))

                punctuality_data = Main_Data_Upload.objects.filter(
                    registration_date__range=[
                        dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    ],
                    train_station=t_r,
                    problem_type="Punctuality",
                )
                p1 = (int(punctuality_data.count()), int(t_r), "Punctuality")
                punctuality.append(list(p1))

                water_data = Main_Data_Upload.objects.filter(
                    registration_date__range=[
                        dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    ],
                    train_station=t_r,
                    problem_type="Water Availability",
                )
                w1 = (int(water_data.count()), int(t_r), "Water Availability")
                water_avail.append(list(w1))

                electrical_data = Main_Data_Upload.objects.filter(
                    registration_date__range=[
                        dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    ],
                    train_station=t_r,
                    problem_type="Electrical Equipment",
                )
                e1 = (int(electrical_data.count()),
                    int(t_r), "Electrical Equipment")
                electrical_equip.append(list(e1))

                coach_maintain_data = Main_Data_Upload.objects.filter(
                    registration_date__range=[
                        dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    ],
                    train_station=t_r,
                    problem_type="Coach - Maintenance",
                )
                c2 = (int(coach_maintain_data.count()),
                    int(t_r), "Coach - Maintenance")
                coach_maintain.append(list(c2))

                miscellaneous_data = Main_Data_Upload.objects.filter(
                    registration_date__range=[
                        dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    ],
                    train_station=t_r,
                    problem_type="Miscellaneous",
                )
                m2 = (int(miscellaneous_data.count()), int(t_r), "Miscellaneous")
                miscellaneous.append(list(m1))

                staff_behave_data = Main_Data_Upload.objects.filter(
                    registration_date__range=[
                        dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    ],
                    train_station=t_r,
                    problem_type="Staff Behaviour",
                )
                s2 = (int(staff_behave_data.count()), int(t_r), "Staff Behaviour")
                staff_behave.append(list(s2))
        else:
            for t_r in train_numbers:
                coach_clean_data = Main_Data_Upload.objects.filter(
                    train_station=t_r, problem_type="Coach - Cleanliness"
                )
                c1 = (int(coach_clean_data.count()),
                    int(t_r), "Coach - Cleanliness")
                coach_clean.append(list(c1))

                bed_data = Main_Data_Upload.objects.filter(
                    train_station=t_r, problem_type="Bed Roll"
                )
                b1 = (int(bed_data.count()), int(t_r), "Bed Roll")
                bed_roll.append(list(b1))

                security_data = Main_Data_Upload.objects.filter(
                    train_station=t_r, problem_type="Security"
                )
                s1 = (int(security_data.count()), int(t_r), "Security")
                security.append(list(s1))

                medical_data = Main_Data_Upload.objects.filter(
                    train_station=t_r, problem_type="Medical Assistance"
                )
                m1 = (int(medical_data.count()), int(t_r), "Medical Assistance")
                medical_assis.append(list(m1))

                punctuality_data = Main_Data_Upload.objects.filter(
                    train_station=t_r, problem_type="Punctuality"
                )
                p1 = (int(punctuality_data.count()), int(t_r), "Punctuality")
                punctuality.append(list(p1))

                water_data = Main_Data_Upload.objects.filter(
                    train_station=t_r, problem_type="Water Availability"
                )
                w1 = (int(water_data.count()), int(t_r), "Water Availability")
                water_avail.append(list(w1))

                electrical_data = Main_Data_Upload.objects.filter(
                    train_station=t_r, problem_type="Electrical Equipment"
                )
                e1 = (int(electrical_data.count()),
                    int(t_r), "Electrical Equipment")
                electrical_equip.append(list(e1))

                coach_maintain_data = Main_Data_Upload.objects.filter(
                    train_station=t_r, problem_type="Coach - Maintenance"
                )
                c2 = (int(coach_maintain_data.count()),
                    int(t_r), "Coach - Maintenance")
                coach_maintain.append(list(c2))

                miscellaneous_data = Main_Data_Upload.objects.filter(
                    train_station=t_r, problem_type="Miscellaneous"
                )
                m2 = (int(miscellaneous_data.count()), int(t_r), "Miscellaneous")
                miscellaneous.append(list(m1))

                staff_behave_data = Main_Data_Upload.objects.filter(
                    train_station=t_r, problem_type="Staff Behaviour"
                )
                s2 = (int(staff_behave_data.count()), int(t_r), "Staff Behaviour")
                staff_behave.append(list(s2))

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

        if request.method != "POST":
            for cm in coach_maintain:
                if cm[0] != 0:
                    total.append(cm)
                    break

            for b in bed_roll:
                if b[0] != 0:
                    total.append(b)
                    break

            for st in staff_behave:
                if st[0] != 0:
                    total.append(st)
                    break

            for ee in electrical_equip:
                if ee[0] != 0:
                    total.append(ee)
                    break

            for wta in water_avail:
                if wta[0] != 0:
                    total.append(wta)
                    break

            for punc in punctuality:
                if punc[0] != 0:
                    total.append(punc)
                    break

            for secure in security:
                if secure[0] != 0:
                    total.append(secure)
                    break

            for mda in medical_assis:
                if mda[0] != 0:
                    total.append(mda)
                    break

            for mis in miscellaneous:
                if mis[0] != 0:
                    total.append(mis)
                    break

            for cc in coach_clean:
                if cc[0] != 0:
                    total.append(cc)
                    break

            if len(total) == 0:
                show = False
            if len(total) >= 1:
                show = True
        else:
            if "Coach - Maintenance" in complain_type:
                for cm in coach_maintain:
                    if cm[0] != 0:
                        total.append(cm)
                        break
            if "Bed Roll" in complain_type:
                for b in bed_roll:
                    if b[0] != 0:
                        total.append(b)
                        break
            if "Staff Behaviour" in complain_type:
                for st in staff_behave:
                    if st[0] != 0:
                        total.append(st)
                        break
            if "Electrical Equipment" in complain_type:
                for ee in electrical_equip:
                    if ee[0] != 0:
                        total.append(ee)
                        break
            if "Water Availability" in complain_type:
                for wta in water_avail:
                    if wta[0] != 0:
                        total.append(wta)
                        break
            if "Punctuality" in complain_type:
                for punc in punctuality:
                    if punc[0] != 0:
                        total.append(punc)
                        break
            if "Security" in complain_type:
                for secure in security:
                    if secure[0] != 0:
                        total.append(secure)
                        break
            if "Medical Assistance" in complain_type:
                for mda in medical_assis:
                    if mda[0] != 0:
                        total.append(mda)
                        break
            if "Miscellaneous" in complain_type:
                for mis in miscellaneous:
                    if mis[0] != 0:
                        total.append(mis)
                        break
            if "Coach - Cleanliness" in complain_type:
                for cc in coach_clean:
                    if cc[0] != 0:
                        total.append(cc)
                        break
            if len(total) == 0:
                show = False
            if len(total) >= 1:
                show = True

        if request.method != "POST":
            start_date = "2000-01-01"
            end_date = "5000-01-01"
            post = False
        context = {
            "post": post,
            "total": total,
            "show": show,
            "all_type": ALL_TYPES,
            "critical_type": CRITICAL_TYPES,
            "start_date": start_date,
            "end_date": end_date,
            "rgd": rgd,
            "rncc": rncc,
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
            "trains_cat": TRAIN_CATS,
        }
        return render(request, "railmadad/min_complain_train.html", context)
    except:
        return render(request,"errorhtml")

@login_required
def min_complain_coach(request):
    try:
        main_all = Main_Data_Upload.objects.all()
        coach = []
        for m in main_all:
            if m.physical_coach_number == float(0.0):
                pass
            else:
                coach.append(m.physical_coach_number)
        all_type = [
            "Coach - Cleanliness",
            "Bed Roll",
            "Security",
            "Medical Assistance",
            "Punctuality",
            "Water Availability",
            "Electrical Equipment",
            "Coach - Maintenance",
            "Miscellaneous",
            "Staff Behaviour",
        ]
        critical_type = [
            "Coach - Cleanliness",
            "Bed Roll",
            "Water Availability",
            "Electrical Equipment",
            "Coach - Maintenance",
        ]

        coaches_set = set(coach)
        coaches = list(coaches_set)

        train_number = []
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
        checked = []
        check_type = []
        complain_category = []
        complain_type = []

        trainsss = Main_Data_Upload.objects.all()
        main_trains = []
        for ttt in trainsss:
            main_trains.append(float(ttt.train_station))
        set_train = set(main_trains)
        main_train = list(set_train)
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

        ######################################################

        if request.method == "POST":
            post = True
            complain_type = request.POST.getlist("complain_type")
            start_date = request.POST.get("start_date", "")
            end_date = request.POST.get("end_date", "")
            train_number = request.POST.getlist("train_number")
            check_type = request.POST.getlist("check-type")
            complain_category = request.POST.getlist("complain-category")
            start_month = dt.strptime(start_date, "%Y-%m-%d")
            end_month = dt.strptime(end_date, "%Y-%m-%d")

            delta = end_month - start_month

            for train in train_number:
                checked.append(int(train))

            sdate = date(
                int(start_month.year), int(start_month.month), int(start_month.day)
            )
            edate = date(int(end_month.year), int(
                end_month.month), int(end_month.day))

            if delta.days <= -1:
                return HttpResponse(
                    "<center><h1>Please Enter valid date Range</center></h1>"
                )

            for t_r in coaches:
                coach_clean_data = Main_Data_Upload.objects.filter(
                    registration_date__range=[
                        dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    ],
                    physical_coach_number=t_r,
                    problem_type="Coach - Cleanliness",
                )
                c1 = (int(coach_clean_data.count()),
                    int(t_r), "Coach - Cleanliness")
                coach_clean.append(list(c1))

                bed_data = Main_Data_Upload.objects.filter(
                    registration_date__range=[
                        dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    ],
                    physical_coach_number=t_r,
                    problem_type="Bed Roll",
                )
                b1 = (int(bed_data.count()), int(t_r), "Bed Roll")
                bed_roll.append(list(b1))

                security_data = Main_Data_Upload.objects.filter(
                    registration_date__range=[
                        dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    ],
                    physical_coach_number=t_r,
                    problem_type="Security",
                )
                s1 = (int(security_data.count()), int(t_r), "Security")
                security.append(list(s1))

                medical_data = Main_Data_Upload.objects.filter(
                    registration_date__range=[
                        dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    ],
                    physical_coach_number=t_r,
                    problem_type="Medical Assistance",
                )
                m1 = (int(medical_data.count()), int(t_r), "Medical Assistance")
                medical_assis.append(list(m1))

                punctuality_data = Main_Data_Upload.objects.filter(
                    registration_date__range=[
                        dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    ],
                    physical_coach_number=t_r,
                    problem_type="Punctuality",
                )
                p1 = (int(punctuality_data.count()), int(t_r), "Punctuality")
                punctuality.append(list(p1))

                water_data = Main_Data_Upload.objects.filter(
                    registration_date__range=[
                        dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    ],
                    physical_coach_number=t_r,
                    problem_type="Water Availability",
                )
                w1 = (int(water_data.count()), int(t_r), "Water Availability")
                water_avail.append(list(w1))

                electrical_data = Main_Data_Upload.objects.filter(
                    registration_date__range=[
                        dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    ],
                    physical_coach_number=t_r,
                    problem_type="Electrical Equipment",
                )
                e1 = (int(electrical_data.count()),
                    int(t_r), "Electrical Equipment")
                electrical_equip.append(list(e1))

                coach_maintain_data = Main_Data_Upload.objects.filter(
                    registration_date__range=[
                        dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    ],
                    physical_coach_number=t_r,
                    problem_type="Coach - Maintenance",
                )
                c2 = (int(coach_maintain_data.count()),
                    int(t_r), "Coach - Maintenance")
                coach_maintain.append(list(c2))

                miscellaneous_data = Main_Data_Upload.objects.filter(
                    registration_date__range=[
                        dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    ],
                    physical_coach_number=t_r,
                    problem_type="Miscellaneous",
                )
                m2 = (int(miscellaneous_data.count()), int(t_r), "Miscellaneous")
                miscellaneous.append(list(m1))

                staff_behave_data = Main_Data_Upload.objects.filter(
                    registration_date__range=[
                        dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    ],
                    physical_coach_number=t_r,
                    problem_type="Staff Behaviour",
                )
                s2 = (int(staff_behave_data.count()), int(t_r), "Staff Behaviour")
                staff_behave.append(list(s2))
        else:
            for t_r in coaches:
                coach_clean_data = Main_Data_Upload.objects.filter(
                    physical_coach_number=t_r, problem_type="Coach - Cleanliness"
                )
                c1 = (int(coach_clean_data.count()),
                    int(t_r), "Coach - Cleanliness")
                coach_clean.append(list(c1))

                bed_data = Main_Data_Upload.objects.filter(
                    physical_coach_number=t_r, problem_type="Bed Roll"
                )
                b1 = (int(bed_data.count()), int(t_r), "Bed Roll")
                bed_roll.append(list(b1))

                security_data = Main_Data_Upload.objects.filter(
                    physical_coach_number=t_r, problem_type="Security"
                )
                s1 = (int(security_data.count()), int(t_r), "Security")
                security.append(list(s1))

                medical_data = Main_Data_Upload.objects.filter(
                    physical_coach_number=t_r, problem_type="Medical Assistance"
                )
                m1 = (int(medical_data.count()), int(t_r), "Medical Assistance")
                medical_assis.append(list(m1))

                punctuality_data = Main_Data_Upload.objects.filter(
                    physical_coach_number=t_r, problem_type="Punctuality"
                )
                p1 = (int(punctuality_data.count()), int(t_r), "Punctuality")
                punctuality.append(list(p1))

                water_data = Main_Data_Upload.objects.filter(
                    physical_coach_number=t_r, problem_type="Water Availability"
                )
                w1 = (int(water_data.count()), int(t_r), "Water Availability")
                water_avail.append(list(w1))

                electrical_data = Main_Data_Upload.objects.filter(
                    physical_coach_number=t_r, problem_type="Electrical Equipment"
                )
                e1 = (int(electrical_data.count()),
                    int(t_r), "Electrical Equipment")
                electrical_equip.append(list(e1))

                coach_maintain_data = Main_Data_Upload.objects.filter(
                    physical_coach_number=t_r, problem_type="Coach - Maintenance"
                )
                c2 = (int(coach_maintain_data.count()),
                    int(t_r), "Coach - Maintenance")
                coach_maintain.append(list(c2))

                miscellaneous_data = Main_Data_Upload.objects.filter(
                    physical_coach_number=t_r, problem_type="Miscellaneous"
                )
                m2 = (int(miscellaneous_data.count()), int(t_r), "Miscellaneous")
                miscellaneous.append(list(m1))

                staff_behave_data = Main_Data_Upload.objects.filter(
                    physical_coach_number=t_r, problem_type="Staff Behaviour"
                )
                s2 = (int(staff_behave_data.count()), int(t_r), "Staff Behaviour")
                staff_behave.append(list(s2))

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

        if request.method != "POST":
            for cm in coach_maintain:
                if cm[0] != 0:
                    total.append(cm)
                    break

            for b in bed_roll:
                if b[0] != 0:
                    total.append(b)
                    break

            for st in staff_behave:
                if st[0] != 0:
                    total.append(st)
                    break

            for ee in electrical_equip:
                if ee[0] != 0:
                    total.append(ee)
                    break

            for wta in water_avail:
                if wta[0] != 0:
                    total.append(wta)
                    break

            for punc in punctuality:
                if punc[0] != 0:
                    total.append(punc)
                    break

            for secure in security:
                if secure[0] != 0:
                    total.append(secure)
                    break

            for mda in medical_assis:
                if mda[0] != 0:
                    total.append(mda)
                    break

            for mis in miscellaneous:
                if mis[0] != 0:
                    total.append(mis)
                    break

            for cc in coach_clean:
                if cc[0] != 0:
                    total.append(cc)
                    break

            if len(total) == 0:
                show = False
            if len(total) >= 1:
                show = True
        else:
            if "Coach - Maintenance" in complain_type:
                for cm in coach_maintain:
                    if cm[0] != 0:
                        total.append(cm)
                        break
            if "Bed Roll" in complain_type:
                for b in bed_roll:
                    if b[0] != 0:
                        total.append(b)
                        break
            if "Staff Behaviour" in complain_type:
                for st in staff_behave:
                    if st[0] != 0:
                        total.append(st)
                        break
            if "Electrical Equipment" in complain_type:
                for ee in electrical_equip:
                    if ee[0] != 0:
                        total.append(ee)
                        break
            if "Water Availability" in complain_type:
                for wta in water_avail:
                    if wta[0] != 0:
                        total.append(wta)
                        break
            if "Punctuality" in complain_type:
                for punc in punctuality:
                    if punc[0] != 0:
                        total.append(punc)
                        break
            if "Security" in complain_type:
                for secure in security:
                    if secure[0] != 0:
                        total.append(secure)
                        break
            if "Medical Assistance" in complain_type:
                for mda in medical_assis:
                    if mda[0] != 0:
                        total.append(mda)
                        break
            if "Miscellaneous" in complain_type:
                for mis in miscellaneous:
                    if mis[0] != 0:
                        total.append(mis)
                        break
            if "Coach - Cleanliness" in complain_type:
                for cc in coach_clean:
                    if cc[0] != 0:
                        total.append(cc)
                        break
            if len(total) == 0:
                show = False
            if len(total) >= 1:
                show = True
        if request.method != "POST":
            start_date = None
            end_date = None
            post = False

        context = {
            "post": post,
            "total": total,
            "show": show,
            "all_type": all_type,
            "critical_type": critical_type,
            "start_date": start_date,
            "end_date": end_date,
            "rncc": rncc,
            "rgd": rgd,
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
            "trains_cat": TRAIN_CATS,
            "all_type": ALL_TYPES,
            "critical_type": CRITICAL_TYPES,
        }
        return render(request, "railmadad/min_complain_coach.html", context)
    except:
        return render (request,"error.html")