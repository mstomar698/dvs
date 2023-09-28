import csv
from django.shortcuts import render
from railmadad.models import Main_Data_Upload
from railmadad.constants import TRAIN_CATS
from railmadad.constants import rgd, rncc, dnr, pnbe, ppta, ipr, keu, mka, ara, all_type, critical_type
from s2analytica.common import log_time, getratelimit
from s2analytica.settings import IST, START_TIME, END_TIME
from datetime import datetime as dt, date
from django.http import HttpResponse
import matplotlib
from django_ratelimit.decorators import ratelimit
matplotlib.use("Agg")
from django.contrib.auth.decorators import login_required

@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def download_data_csv(request):

    trainsss = Main_Data_Upload.objects.all()
    main_trains = []
    for ttt in trainsss:
        main_trains.append(float(ttt.train_station))
    set_train = set(main_trains)
    main_train = list(set_train)
    ######
    bottom_staff = []
    bottom_staff_count = []
    checked = []
    if request.method == "POST":
        post = True
        problem_type = request.POST.getlist("problem_type")
        start_date = request.POST.get("start_date", "")
        end_date = request.POST.get("end_date", "")
        complain_category = request.POST.getlist("complain-category")
        complains = request.POST.getlist("complain-type")
        # owning_zone='not_storing_data'
        # current_user_id = 'not_storing_data'
        # current_user_phone_number = 'not_storing_data'
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
        edate = date(int(end_month.year), int(
            end_month.month), int(end_month.day))

        for tn in request.POST.getlist("train_number"):
            checked.append(int(tn))

        if delta.days <= -1:
            return HttpResponse("<h1>Please Enter valid Date Range</h1>")
        else:
            response = HttpResponse(content_type='text/csv')
            response[
                'Content-Disposition'] = f'attachment; filename="Rail_madad_data_from_{start_date}_{end_date}.csv"'
            writer = csv.writer(response)
            writer.writerow(['S. No.', 'Ref. No.', 'Registration Date', 'Closing Date', 'Disposal Time',
                            'Train/Station', 'Coach type', 'Coach no', 'Rake no', 'Escot staff',
                             'Type', 'Sub Type', 'Zone','Div', 'Dept', 
                             'Breach', 'Rating', 'Status', 'Complaint Description', 'Remarks',
                             'No. of times forwarded', 'PNR/UTS No', 'Coach Type', 'Coach No.', 'Feedback Remarks',
                             'Upcoming Station', 'Mobile No./Email Id',
                             'created_at', 'updated_at', 'created_by', 'updated_by'
                             ])
					
            users = Main_Data_Upload.objects.all().values_list(
                'sl_number', 'reference_number', 'registration_date', 'closing_date', 'disposal_time',
                'train_station', 'train_coach_type', 'physical_coach_number', 'rake_number', 'staff_name',
                'problem_type', 'sub_type', 'zone', 'div', 'dept',
                'breach','rating', 'status', 'complaint_discription', 'remark',
                'number_of_time_forwarded', 'pnr_utc_number', 'physical_coach_type', 'train_coach_number', 'feedback_remark',
                'upcoming_station', 'mobile_number_or_email',
                'created_at', 'updated_at', 'created_by', 'updated_by'
            ).filter(
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST), f"{end_date} {END_TIME}+00:00"],
                problem_type__in=complain_type,
                train_station__in=train_number)
            formated_users = list(users)
            for formated_user in formated_users:
                list_formated_user = list(formated_user)
                list_formated_user[2] = list_formated_user[2].strftime(
                    "%d-%m-%y %H:%M")
                list_formated_user[3] = list_formated_user[3].strftime(
                    "%d-%m-%y %H:%M")

                writer.writerow(list_formated_user)
            return response

    if request.method != "POST":
        post = False
        start_date = None
        end_date = None
        train_number = None
        check_type = None
        complain_category = None
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
        "post": post,
        "start_date": start_date,
        "end_date": end_date,
        "checked": checked,
        "check_type": check_type,
        "complain_category": complain_category,
        "train_number": train_number,
        "trains_cat": TRAIN_CATS,
    }
    return render(request, 'railmadad/download_data.html', context)
