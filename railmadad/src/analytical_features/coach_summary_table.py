from django.http import HttpResponse
from django.shortcuts import render
from railmadad.models import Main_Data_Upload
from railmadad.constants import TRAIN_CATS
from railmadad.constants import rgd, rncc, dnr, pnbe, ppta, ipr, keu, mka, ara, color_code, all_type, critical_type
from datetime import datetime as dt, date
from django.contrib.auth.decorators import login_required
from pytz import timezone
from s2analytica.common import log_time, getratelimit
from s2analytica.settings import START_TIME, END_TIME, IST
from django_ratelimit.decorators import ratelimit
import calendar

@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def coach_summary_table(request):
    try:
        trainsss = Main_Data_Upload.objects.all()
        main_trains = []
        for ttt in trainsss:
            main_trains.append(float(ttt.train_station))
        set_train = set(main_trains)
        main_train = list(set_train)

        bottom_staff = []
        bottom_staff_count = []
        checked = []

        # all_physical_coach_number = []
        set_physical_coach_number = set()
        all_data = Main_Data_Upload.objects.all()
        for ad in all_data:
            # print(ad)
            if not ad or not ad.physical_coach_number:
                # print("here")
                pass
            else:
                # NOTE: int() argument must be a string, a bytes-like object or a number, not 'NoneType'
                # if ad.physical_coach_number is not None:
                try:
                    # print("p ",ad.physical_coach_number)
                    set_physical_coach_number.add(
                        int(ad.physical_coach_number))
                except Exception as e:
                    # print(e)
                    # print(e)
                    pass
        #  = set(all_physical_coach_number)
        physical_coach_number = list(set_physical_coach_number)
        # print(physical_coach_number)
        if request.method == "POST":
            post = True
            problem_type = request.POST.getlist("problem_type")
            start_date = request.POST.get("start_date", "")
            end_date = request.POST.get("end_date", "")
            complain_category = request.POST.getlist("complain-category")
            complains = request.POST.getlist("complain-type")
            check_type = request.POST.getlist("check-type")

            select_checkbox = request.POST.get("check-type-select-all")
            # print(select_checkbox)

            if select_checkbox == "value_checked":
                select_all = True
            else:
                select_all = False

            complain_type = request.POST.get("complain-dropdown").split(',')
            physical_coach_number_list_str = request.POST.get(
                "coach-number-dropdown", "")
            if physical_coach_number_list_str != "":
                physical_coach_number_list = physical_coach_number_list_str.split(
                    ",")
            else:
                physical_coach_number_list = physical_coach_number_list_str

            # print(select_all)

            start_month = dt.strptime(start_date, "%Y-%m-%d")
            end_month = dt.strptime(end_date, "%Y-%m-%d")

            delta = end_month - start_month

            sdate = date(
                int(start_month.year), int(
                    start_month.month), int(start_month.day)
            )
            edate = date(int(end_month.year), int(
                end_month.month), int(end_month.day))

            for cn in request.POST.getlist("physical_coach_number"):
                checked.append(int(cn))

            if delta.days <= -1:
                return HttpResponse("<h1>Please Enter valid Date Range</h1>")

            else:
                datas = []
                total = []
                for d in range(len(physical_coach_number_list)):
                    for i in range(len(complain_type)):
                        data = Main_Data_Upload.objects.filter(
                            registration_date__range=[
                                dt.strptime(
                                    f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                                dt.strptime(f"{end_date} {END_TIME}",
                                            '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            ],
                            problem_type=complain_type[i], physical_coach_number=physical_coach_number_list[d]).count()
                        # print(data)
                        datas.append(data)
                for k in range(len(physical_coach_number_list)):
                    total.append(datas[k*len(complain_type)                                 :len(complain_type)*(k+1)])

                total_complain = []
                for t in total:
                    total_complain.append(sum(t))

            context = {
                "all_type": all_type,
                "critical_type": critical_type,
                "rgd": rgd,
                "rncc": rncc,
                "dnr": dnr,
                "pnbe": pnbe,
                "ppta": ppta,
                "ipr": ipr,
                "keu": keu,
                "mka": mka,
                "ara": ara,
                "main_train": main_train,
                "bottom_staff_count": bottom_staff_count,
                "bottom_staff": bottom_staff,
                "color_code": color_code,
                "post": post,
                "complain_type": complain_type,
                "start_date": start_date,
                "end_date": end_date,
                "checked": checked,
                "check_type": check_type,
                "complain_category": complain_category,
                "trains_cat": TRAIN_CATS,
                'total': total,
                'total_complain': total_complain,
                'physical_coach_number': physical_coach_number,
                'select_all': select_all,
                'physical_coach_number_list': physical_coach_number_list
            }

            # # itterate through dictionary
            # for _, j in context.items():
            #     print(_,type(j))
            # if len(j) == 0:
            #     print(_, j)
            # print(total_complain)
        else:
            current_time_get = dt.now(timezone("Asia/Kolkata"))
            print(current_time_get)

            if(current_time_get.day > calendar.monthrange(current_time_get.year, current_time_get.month - 1)[1]):
                default_start = dt(current_time_get.year, current_time_get.month - 1, calendar.monthrange(current_time_get.year, current_time_get.month - 1)[1], 0, 0)
            
            else:
                default_start = dt(current_time_get.year, current_time_get.month - 1, current_time_get.day, 0, 0)
                
            start_date = default_start.strftime('%Y-%m-%d')
            end_date = current_time_get.strftime('%Y-%m-%d')
            # physical_coach_number_list=physical_coach_number_list
            # total_complain=total_complain
            post = False
            complain_type = critical_type
            context = {
                'post': post,
                "all_type": all_type,
                "critical_type": critical_type,
                "rgd": rgd,
                "rncc": rncc,
                "dnr": dnr,
                "pnbe": pnbe,
                "ppta": ppta,
                "ipr": ipr,
                "keu": keu,
                "mka": mka,
                "ara": ara,
                "main_train": main_train,
                "checked": checked,
                "complain_category": None,
                "trains_cat": TRAIN_CATS,
                'physical_coach_number': physical_coach_number,
                'physical_coach_number_list': physical_coach_number,
                "complain_type": complain_type,
                "start_date": start_date,
                "end_date": end_date,

            }
        return render(request, 'railmadad/coach_summary_table.html', context)
    except:
        return render(request, "error.html")
