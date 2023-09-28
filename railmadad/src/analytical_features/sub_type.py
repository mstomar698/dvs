
import calendar
from django.shortcuts import render
from railmadad.models import Main_Data_Upload
from railmadad.constants import TRAIN_CATS
from railmadad.src.data.DBQuery import DBQuery
from railmadad.constants import rgd, rncc, dnr, pnbe, ppta, ipr, keu, mka, ara, checked, all_type, critical_type
from datetime import datetime as dt, timedelta
from pytz import timezone

from django.contrib.auth.decorators import login_required
from django_ratelimit.decorators import ratelimit
from s2analytica.common import log_time, getratelimit

@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def sub_type(request, subtype):
    try:
        if subtype == "Luggage Left Behind|Unclaimed|Suspected Articles":
            subtypes = "Luggage Left Behind/Unclaimed/Suspected Articles"

        elif subtype == "Harassment|Extortion by Security Personnel|Railway personnel":
            subtypes = "Harassment/Extortion by Security Personnel/Railway personnel"

        elif subtype == "Tap leaking|Tap not working":
            subtypes = "Tap leaking/Tap not working"

        elif subtype == "Window|Seat Broken":
            subtypes = "Window/Seat Broken"

        elif subtype == "Window|Door locking problem":
            subtypes = "Window/Door locking problem"

        elif subtype == "Unauthorized person in Ladies|Disabled Coach|SLR|Reserve Coach":
            subtypes = "Unauthorized person in Ladies/Disabled Coach/SLR/Reserve Coach"

        elif subtype == "Jerks|Abnormal Sound":
            subtypes = "Jerks/Abnormal Sound"

        elif subtype == "Theft of Passengers Belongings|Snatching":
            subtypes = "Theft of Passengers Belongings/Snatching"

        elif subtype == "Nuisance by Hawkers|Beggar|Eunuch|Passenger":
            subtypes = "Nuisance by Hawkers/Beggar/Eunuch/Passenger"

        elif subtype == "Smoking|Drinking Alcohol|Narcotics":
            subtypes = "Smoking/Drinking Alcohol/Narcotics"

        elif subtype == "Passenger Missing|Not responding call":
            subtypes = "Passenger Missing/Not responding call"

        else:
            subtypes = subtype

        dates = []
        data_count = []

        trainsss = Main_Data_Upload.objects.all()
        main_trains = []
        for ttt in trainsss:
            main_trains.append(float(ttt.train_station))
        set_train = set(main_trains)
        main_train = list(set_train)
        ######
        #####

        check_type = []

        if request.method == "POST":
            post = True
            train_numbers = request.POST.getlist("train_number")
            start_date = request.POST.get("start_date", "")
            end_date = request.POST.get("end_date", "")
            for train in request.POST.getlist("train_number"):
                checked.append(int(train))

            check_type = request.POST.getlist("check-type")

            data_count,dates = DBQuery.sub_type_query( start_date, end_date, subtypes)

        else:
            start_date = None
            end_date = None
            post = False
            for i in range(0, 31):
                day = dt.now(timezone("Asia/Kolkata")) - timedelta(i)
                dates.append(
                    str(day.day)
                    + " "
                    + str(calendar.month_name[day.month])
                    + ","
                    + str(day.year)
                )
                sub_type_data = Main_Data_Upload.objects.filter(
                    sub_type=f"{subtypes}",
                    train_station__in=checked,
                    registration_date__day=day.day,
                    registration_date__month=day.month,
                    registration_date__year=day.year,
                )
                data_count.append(sub_type_data.count())
            dates.reverse()
            data_count.reverse()
        context = {
            "show": True,
            "data_count": data_count,
            "dates": dates,
            "subtype": subtype,
            "subtypes": subtypes,
            "start_date": start_date,
            "end_date": end_date,
            "main_train": main_train,
            "post": post,
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
            "all_type": all_type,
            "critical_type": critical_type,
            "checked": checked,
            "check_type": check_type,
        }
        return render(request, "railmadad/sub_type.html", context)
    except:
        return render(request,"error.html")