


from django.shortcuts import redirect, render
from railmadad.constants import update_global_variables
from railmadad.models import Staff_Detail
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from s2analytica.common import log_time, getratelimit
from django_ratelimit.decorators import ratelimit

@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def create_staff(request):
    show_data = list(Staff_Detail.objects.all().values_list())
    if request.method == "POST":
        staff_id = request.POST.get("staff_id", "")
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        department = request.POST.get("department", "")
        if Staff_Detail.objects.filter(staff_id=staff_id):
            messages.error(request,'This Staff Id is Already Taken')
            return redirect(request.path)
        else:
            data = Staff_Detail(
            staff_id=staff_id,
            staff_first_name=first_name,
            staff_last_name=last_name,
            department=department)
            data.save()
        update_global_variables()
        messages.success(request, "Successully Created a Staff")
        return redirect(request.path)
    else:
        pass
    return render(request, "railmadad/create_staff.html", {"staff_data": show_data})