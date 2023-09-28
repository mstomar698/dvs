
from datetime import datetime as dt

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from railmadad.constants import update_global_variables
from railmadad.models import Main_Data_Upload
from s2analytica.common import log_time, getratelimit
from django_ratelimit.decorators import ratelimit
from s2analytica.settings import START_TIME, END_TIME, IST


@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def show_physical_coach_number(request):
    try:
        complain_list = []
        post = None
        start_date = None
        order = "desc"

        if request.method == "POST":
            user = User.objects.get(id=request.user.id)
            if user.groups.filter(name="Moderator").exists():
                post = True
                start_date = request.POST.get("start_date", "")
                # print(f"post_start_date: {start_date}")

                start = dt.strptime(start_date, "%Y-%m-%d")

                main_data = Main_Data_Upload.objects.filter(
                    registration_date__range=[
                        dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        f"{start_date} {END_TIME}+00:00",
                    ]
                )

                complain_list = list(main_data.values_list())
                # for complain in complain_list:
                #     for i, c in enumerate(complain):
                #         # print(f"c.{i} = {complain}")

                number_of_data = main_data.count()
            else:
                messages.error(
                    request, "You Cannot Update Coach Number, Only Moderator Can DO"
                )
                return redirect(request.path)
        else:
            start_date = request.GET.get("start_date", "")
            # print(f"Get_start_date: {start_date}")
            main_data = None
            if start_date:
                main_data = Main_Data_Upload.objects.filter(
                    registration_date__range=[
                        dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        f"{start_date} {END_TIME}+00:00",
                    ]
                )
                # # print(main_data)
                complain_list = list(main_data.values_list())
                # for complain in complain_list:
                #     for i, c in enumerate(complain):
                #         # print(f"c.{i} = {complain}")
                post = True

                number_of_data = main_data.count()

                sort_method_map = {
                    "coach-number": 12,
                    "reference": 3,
                    "train-number": 8,
                    "type": 15,
                    "sub-type": 16,
                    "disposal-time": 4,
                    "rating": 22,
                    "reg-date": 4,
                    "staff": 14,
                    "description": 8,
                }
                sort_method = request.GET.get("sort_method", "")
                order = "desc"
                if sort_method:
                    order = request.GET.get("order", "")
                    if order == "asc":
                        complain_list.sort(
                            key=lambda x: x[sort_method_map.get(sort_method)]
                        )
                        order = "desc"
                    elif order == "desc":
                        complain_list.sort(
                            key=lambda x: x[sort_method_map.get(sort_method)], reverse=True
                        )
                        order = "asc"

            else:
                post = False
                main_data = None
                number_of_data = None
                start_date = None

        context = {
            "order": order,
            "post": post,
            "start_date": start_date,
            "main_data": main_data,
            "number_of_data": number_of_data,
            "complains": complain_list,
        }
        return render(request, "railmadad/add_coach_number.html", context)
    except:
        return render(request,"error.html")

@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
@csrf_exempt
def add_physical_coach_number(request):
    try:
        if request.method == "POST":
            response = request.POST
            list_reponse = list(response)
            list_reponse.remove(list_reponse[0])
            list_reponse.remove(list_reponse[-1])
            for res in list_reponse:
                splitted_response = res.split("-")
                data_id = int(splitted_response[2])
                data_count = int(splitted_response[1])
                update_data = Main_Data_Upload.objects.get(id=data_id)

                if (
                    response[f"input-{data_count}-{data_id}"] == None
                    or response[f"input-{data_count}-{data_id}"] == ""
                    or response[f"input-{data_count}-{data_id}"] == " "
                ):
                    update_data.physical_coach_number = 0.0
                else:
                    update_data.physical_coach_number = int(
                        response[f"input-{data_count}-{data_id}"]
                    )
                update_data.save()
            update_global_variables()
            messages.success(request, "Successfully Updated Coach Number")
        # moving out of the if condition to make sure that the user is redirected to the page no matter what is the request type
        return redirect("/auth/show_physical_coach_number")
    except:
        return redirect("error.html")