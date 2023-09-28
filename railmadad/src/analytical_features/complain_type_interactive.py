from django.shortcuts import render
from railmadad.models import Main_Data_Upload
from railmadad.src.data.DBQuery import DBQuery
from s2analytica.common import log_time, getratelimit
from s2analytica.settings import START_TIME, END_TIME, IST
from django.contrib.auth.decorators import login_required
from datetime import datetime as dt
from django_ratelimit.decorators import ratelimit

@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def complain_type(request, complain, start_date, end_date):
    try:
        train_numbers_list = []
        complains_list = []
        complains_list = request.GET.get("complain_type").split("--")
        train_numbers_list = request.GET.get("train_number").split("-")
        res_count = 0
        physical_coach_number = request.GET.get("physical_coach_number")
        merging = False
        merge = []

        a = Main_Data_Upload.objects.filter(problem_type=" Coach - Cleanliness")

        if complain == "satisfactory-nan":
            merging = True
            merge = ["Satisfactory", "-1"]

        else:
            complain = complain

        complain_type = complain

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
        if len(complain.split("----")) == 1:
            splitted_complain = None
        else:
            splitted_complain = complain.split("----")[1]

        if " or " in complain:
            # print(complain)
            complain = complain.replace(" or ", "/")
            complains_list.append(complain)
            complains_list.remove(complains_list[0])
            complain_type = complains_list[0]
            # print(complain_type)

        if complain == "DISPOSAL_DATE_WISE":
            # print(start_date)
            if(len(start_date.split(" "))==2):
                date="00"
                month= start_date.split(" ")[0]
                year=start_date.split(" ")[1]
            if(len(start_date.split(" "))==3):
                date = start_date.split(" ")[0]
                month = start_date.split(" ")[1]
                year = start_date.split(" ")[2]
            datetime_object = dt.strptime(month, "%B")
            month_number = datetime_object.month
            if len(str(month_number)) == 1:
                actual_month_number = f"0{month_number}"
            else:
                actual_month_number = month_number

            actual_date = f"{year}-{actual_month_number}-{date}"
            # print(actual_date)
            problem_types= []
            problem_types = DBQuery.complain_type_interactive_disposal_date(train_numbers_list,actual_month_number,year,complains_list,date)
        elif complain == "DISPOSAL_TRAIN_WISE":
            problem_types = []
            problem_types = DBQuery.complain_type_interactive_disposal_train(train_numbers_list,complains_list,start_date,end_date)
        elif complain == "DISPOSAL_COACH_WISE":
            problem_types = []
            problem_types = DBQuery.complain_type_interactive_disposal_coach(request,complains_list,start_date,end_date)

        elif complain == "DISPOSAL_SUB_TYPE_WISE":
            # print(start_date)
            if(len(start_date.split(" "))==2):
                date="00"
                month= start_date.split(" ")[0]
                year=start_date.split(" ")[1]
            if(len(start_date.split(" "))==3):
                date = start_date.split(" ")[0]
                month = start_date.split(" ")[1]
                year = start_date.split(" ")[2]
            datetime_object = dt.strptime(month, "%B")
            month_number = datetime_object.month
            if len(str(month_number)) == 1:
                actual_month_number = f"0{month_number}"
            else:
                actual_month_number = month_number

            actual_date = f"{year}-{actual_month_number}-{date}"
            # print(actual_date)
            if len(str(month_number)) == 1:
                actual_month_number = f"0{month_number}"
            else:
                actual_month_number = month_number

            actual_date = f"{year}-{actual_month_number}-{date}"
            # print(actual_date)
            problem_types = []
            problem_types = DBQuery.complain_type_interactive_disposal_sub_type(request,train_numbers_list,actual_month_number,year,date)
        elif splitted_complain == "SUB_TYPE_ALL_COMPLAIN_TRAIN_WISE":
            problem_types = Main_Data_Upload.objects.values_list(
                "physical_coach_number",
                "train_station",
                "problem_type",
                "sub_type",
                "disposal_time",
                "rating",
                "registration_date",
                "complaint_discription",
                "staff_name",
                "reference_number",
                'staff_id',
                'remark',
                "rake_number",
                "closing_date",
            ).filter(
                sub_type=request.GET.get('sub_type'),
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    f"{end_date} {END_TIME}+00:00"
                ],
                train_station=complain.split("----")[0]
            )
            # print(problem_types)

        else:
            if request.GET.get('sub_type') != None and len(request.GET.get('sub_type')) >= 1:
                # print("hello")
                problem_types = Main_Data_Upload.objects.values_list(
                    "physical_coach_number",
                    "train_station",
                    "problem_type",
                    "sub_type",
                    "disposal_time",
                    "rating",
                    "registration_date",
                    "complaint_discription",
                    "staff_name",
                    "reference_number",
                    'staff_id',
                    'remark',
                    "rake_number",
                    "closing_date",
                ).filter(
                    sub_type=request.GET.get('sub_type'),
                    problem_type__in=request.GET.get("complain_type").split("--"),
                    train_station__in=train_numbers_list,
                    registration_date__range=[
                        dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        f"{end_date} {END_TIME}+00:00"
                    ]
                )
            else:
                if (start_date == "None" or end_date == "None" or train_numbers_list == [""] or complains_list == [""]):
                    print(start_date, end_date, train_numbers_list, complains_list)
                    if (
                        request.GET.get("physical_coach_number") == None
                        or request.GET.get("physical_coach_number") == ""
                        or request.GET.get("physical_coach_number") == "None"
                    ):
                        if(start_date != "None" and end_date != "None" ):
                            physical_coach_number == None
                            problem_types = Main_Data_Upload.objects.values_list(
                                "physical_coach_number",
                                "train_station",
                                "problem_type",
                                "sub_type",
                                "disposal_time",
                                "rating",
                                "registration_date",
                                "complaint_discription",
                                "staff_name",
                                "reference_number",
                                'staff_id',
                                'remark',
                                "rake_number",
                                "closing_date",
                            ).filter(
                                registration_date__range=[
                                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                                    f"{end_date} {END_TIME}+00:00"
                                ]
                            )
                        else:
                            physical_coach_number == None
                            problem_types = Main_Data_Upload.objects.values_list(
                                "physical_coach_number",
                                "train_station",
                                "problem_type",
                                "sub_type",
                                "disposal_time",
                                "rating",
                                "registration_date",
                                "complaint_discription",
                                "staff_name",
                                "reference_number",
                                'staff_id',
                                'remark',
                                "rake_number",
                                "closing_date",
                            ).filter(
                                registration_date__range=[
                                    f"2000-01-01 {START_TIME}+00:00",
                                    f"5000-01-01 {START_TIME}+00:00",
                                ]
                            )
                    else:
                        # print("one--2")
                        physical_coach_number = int(physical_coach_number)
                        problem_types = Main_Data_Upload.objects.values_list(
                            "physical_coach_number",
                            "train_station",
                            "problem_type",
                            "sub_type",
                            "disposal_time",
                            "rating",
                            "registration_date",
                            "complaint_discription",
                            "staff_name",
                            "reference_number",
                            'staff_id',
                            'remark',
                            "rake_number",
                            "closing_date",
                        ).filter(
                            registration_date__range=[
                                f"2000-01-01 {START_TIME}+00:00",
                                f"5000-01-01 {START_TIME}+00:00",
                            ],
                            problem_type__in=complains_list,
                            physical_coach_number=int(physical_coach_number),
                        )
                else:
                    if (request.GET.get("physical_coach_number") == None or request.GET.get("physical_coach_number") == "" or request.GET.get("physical_coach_number") == "None"):
                        if not len(complain.split("/")) >= 2:
                            # print("one--3")
                            # print(set(Main_Data_Upload.objects.values_list('problem_type')))

                            physical_coach_number = None
                            problem_types = Main_Data_Upload.objects.values_list(
                                "physical_coach_number",
                                "train_station",
                                "problem_type",
                                "sub_type",
                                "disposal_time",
                                "rating",
                                "registration_date",
                                "complaint_discription",
                                "staff_name",
                                "reference_number",
                                'staff_id',
                                'remark',
                                "rake_number",
                                "closing_date",
                            ).filter(
                                registration_date__range=[
                                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                                ],
                                problem_type__in=complains_list,
                                train_station__in=train_numbers_list,
                            )

                        elif (len(complain.split("/")) >= 2):
                            # print("one--4")
                            problem_types = Main_Data_Upload.objects.values_list(
                                "physical_coach_number",
                                "train_station",
                                "problem_type",
                                "sub_type",
                                "disposal_time",
                                "rating",
                                "registration_date",
                                "complaint_discription",
                                "staff_name",
                                "reference_number",
                                'staff_id',
                                'remark',
                                "rake_number",
                                "closing_date",
                            ).filter(
                                registration_date__range=[
                                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                                ],
                                sub_type=complain_type,
                                train_station__in=train_numbers_list,
                                problem_type=(request.GET.get(
                                    "complain_type").split("--")[0])
                            )

                    elif not complain_type in all_type:
                        # print("one--5")
                        problem_types = Main_Data_Upload.objects.values_list(
                            "physical_coach_number",
                            "train_station",
                            "problem_type",
                            "sub_type",
                            "disposal_time",
                            "rating",
                            "registration_date",
                            "complaint_discription",
                            "staff_name",
                            "reference_number",
                            'staff_id',
                            'remark',
                            "rake_number",
                            "closing_date",
                        ).filter(
                            registration_date__range=[
                                dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                                dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            ],
                            sub_type=complain_type,
                            problem_type=(request.GET.get(
                                "complain_type").split("--")[0]),
                            train_station__in=request.GET.get(
                                "train_number").split("-")
                        )
                    else:
                        physical_coach_number = int(physical_coach_number)
                        problem_types = Main_Data_Upload.objects.values_list(
                            "physical_coach_number",
                            "train_station",
                            "problem_type",
                            "sub_type",
                            "disposal_time",
                            "rating",
                            "registration_date",
                            "complaint_discription",
                            "staff_name",
                            "reference_number",
                            'staff_id',
                            'remark',
                            "rake_number",
                            "closing_date",
                        ).filter(
                            registration_date__range=[
                                dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                                dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            ],
                            problem_type__in=complains_list,
                            physical_coach_number=int(physical_coach_number),
                        )

        problem_type = []

        for p in problem_types:
            if complain_type == "satisfactory-nan":
                if merging and str(p[5]) in merge:
                    problem_type.append(p)
            elif str(int(p[1])) == complain_type:
                problem_type.append(p)

            elif complain_type == "All_data":
                problem_type.append(p)

            elif complain_type == str(p[3]):
                problem_type.append(p)

            elif complain_type == str(p[2]):
                problem_type.append(p)

            elif complain_type == str(p[5]):
                problem_type.append(p)

            elif complain_type == str(p[8]):
                problem_type.append(p)

            elif complain_type == str(p[4]):
                problem_type.append(p)

            elif complain_type == "DISPOSAL_DATE_WISE":
                problem_type.append(p)

            elif complain_type == "DISPOSAL_TRAIN_WISE":
                problem_type.append(p)

            elif complain_type == "DISPOSAL_COACH_WISE":
                problem_type.append(p)

            elif complain_type == "DISPOSAL_SUB_TYPE_WISE":
                problem_type.append(p)

            elif splitted_complain == "SUB_TYPE_ALL_COMPLAIN_TRAIN_WISE":
                # print("yes")
                problem_type.append(p)

            try:
                if complain_type == str(int(p[0])) and complain_type != str(-1):
                    problem_type.append(p)
            except:
                pass

            else:
                pass

        res_count = len(problem_type)

        sort_method_map = {
            "coach-number": 0,
            "train-number": 1,
            "type": 2,
            "sub-type": 3,
            "disposal-time": 4,
            "rating": 5,
            "reg-date": 6,
            "staff": 8,
            "description": 7,
            "reference-number": 9,
            "staff_id": 10,
            "rake_number": 12,
            "closing_date": 13,
        }
        sort_method = request.GET.get("sort_method", "")
        order = "desc"
        if sort_method:
            order = request.GET.get("order", "")
            if order == "asc":
                problem_type.sort(
                    key=lambda x: x[sort_method_map.get(sort_method)] if x[sort_method_map.get(sort_method)] else 999999)
                order = "desc"
            elif order == "desc":
                problem_type.sort(
                    key=lambda x: x[sort_method_map.get(sort_method)] if x[sort_method_map.get(sort_method)] else 000000 , reverse=True
                )
                order = "asc"

        # # print(sort_method)
        data = str(problem_type)
        data = data.replace("[", "").replace("]", "").replace("), (", ")---(")

        train_numbers_str = request.GET.get("train_number")
        complain_lists_str = request.GET.get("complain_type")
        context = {
            "data": data,
            "coach_num": physical_coach_number,
            "complain_type": complain_type,
            "res_count": res_count,
            "complain_list": complain_lists_str,
            "train_numbers_list": train_numbers_str,
            "problem_type": problem_type,
            "order": order,
            "end_date": end_date,
            "start_date": start_date,
        }

        return render(request, "railmadad/complain_type.html", context)
    except:
        return render(request,"error.html")