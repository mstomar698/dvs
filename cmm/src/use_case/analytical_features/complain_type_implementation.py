from django.contrib.auth.decorators import login_required
from cmm.src.data.DBQueries import DBQuery
from django_ratelimit.decorators import ratelimit

from s2analytica.common import log_time, getratelimit

@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def complain_type_implementation(request, complain, problem_start, problem_end):
    train_number = list(map(int, request.GET.get("train_number").split("-")))
    sick_heads = request.GET.get("sick_heads").split("---")
    owning_rly = request.GET.get("owning_rly").split("-")
    coach_status = request.GET.get("coach_status")
    departments = request.GET.get("departments")
    vehicle_type = request.GET.get("vehicle_type")
    workshops = request.GET.get("workshops").split("-")
    coach_type = request.GET.get("coach_type").split("-")
    sort_method = request.GET.get("sort_method", "")
    order = request.GET.get("order", "")
    query = request.GET.get("query", "")
    search_param = request.GET.get("search_param", "")

    print(f"train_number: {train_number}")
    print(f"coach_type: {coach_type}")
    print(f"sick_heads: {sick_heads}")
    print(f"owning_rly: {owning_rly}")
    print(f"coach_status: {coach_status}")
    print(f"departments: {departments}")
    print(f"vehicle_type: {vehicle_type}")
    print(f"workshops: {workshops}")
    print(f"sort_method: {sort_method}")
    print(f"order: {order}")
    print(f"query: {query}")
    print(f"Seach_param: {search_param}")
    print("--------------------------------------------------------------")

    if sort_method == "" or sort_method == None:
        sort_method = "id"

    result = DBQuery.complain_type_query(
        request,
        problem_start,
        problem_end,
        complain,
        coach_type,
        train_number,
        owning_rly,
        coach_status,
        departments,
        vehicle_type,
        workshops,
        sick_heads,
        sort_method,
        order,
        query,
        search_param
    )

    # search query text in all database columns

    res_count = result.count()

    if order == "":
        order = "-"
    elif order == "-":
        order = ""

    context = {
        "data": result,
        "res_count": res_count,
        "train_number": train_number,
        "coach_type": coach_type,
        "sick_heads": sick_heads,
        "owning_rly": owning_rly,
        "coach_status": coach_status,
        "departments": departments,
        'coach_type': coach_type,
        "vehicle_type": vehicle_type,
        "workshops": workshops,
        "problem_start": problem_start,
        "problem_end": problem_end,
        "complain": complain,
        "order": order,
        "sort_method": sort_method,
        'search_param': search_param,
        "query": query,
    }

    return context
