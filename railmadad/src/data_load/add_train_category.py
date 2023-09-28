from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from railmadad.models import Main_Data_Upload, Train_Type
from railmadad.constants import TRAIN_CATS, update_global_variables
from s2analytica.common import log_time, getratelimit
from django_ratelimit.decorators import ratelimit

@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def add_train_cat(request):
    data = Main_Data_Upload.objects.all()
    trains = []
    for md in data:
        trains.append(md.train_station)
    set_train = set(trains)
    main_train = list(set_train)

    train_cat = Train_Type.objects.all()
    train_asso = []
    for tc in train_cat:
        train_asso.append(tc.train_number)

    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        if user.groups.filter(name="Moderator").exists():
            for m_t in main_train:
                train_type = request.POST.get(f"type-{m_t}")
                if train_type == None:
                    pass
                else:
                    split_train_number = train_type.split("-")
                    train_number_int = int(float(split_train_number[1]))
                    train_type_str = split_train_number[0]
                    if train_type_str == "DEL":
                        train_1 = Train_Type.objects.get(train_number=train_number_int)
                        train_1.delete()
                        # print("Deleted Successfully")
                    else:
                        train_1 = Train_Type.objects.get(train_number=train_number_int)
                        train_1.Type = split_train_number[0]
                        train_1.save()
                        # print("updated Successfully")

                train_type_2 = request.POST.get(f"type-2-{m_t}")
                if train_type_2 == None or train_type_2 == "" or train_type_2 == " ":
                    pass
                else:
                    split_train_number = train_type_2.split("-")
                    train_number_int = int(float(split_train_number[1]))
                    train_type_str = split_train_number[0]
                    train = Train_Type(
                        train_number=train_number_int, Type=train_type_str
                    )
                    train.save()
            update_global_variables()
                    # print("Successfully Created New")

            messages.success(request, "Successfully Updated")
            return redirect(request.path)

        else:
            messages.error(
                request, "You Cannot Update Train Category, You Are not Moderator"
            )
            return redirect(request.path)

        return redirect(request.path)

    context = {
        "main_train": main_train,
        "train_asso": train_asso,
        "train_cat": train_cat,
        "categories": TRAIN_CATS,
    }
    return render(request, "railmadad/add_train_cat.html", context)

    