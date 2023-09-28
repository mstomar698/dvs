from django.contrib.auth.decorators import login_required
from cmm.src.data.DBQueries import DBQuery
from django_ratelimit.decorators import ratelimit

from s2analytica.common import log_time, getratelimit

@log_time
@login_required # type: ignore
@ratelimit(key='ip', rate=getratelimit)
def coach_pro_query_implentation(request, coach_number_id):

    sort_method = request.GET.get("sort_method", "")
    order = request.GET.get("order", "")
    query = request.GET.get("query", "")
    search_param = request.GET.get("search_param", "")

    print(f"sort_method: {sort_method}")
    print(f"order: {order}")
    print(f"query: {query}")
    print(f"Seach_param: {search_param}")
    print("--------------------------------------------------------------")

    if sort_method == "" or sort_method == None:
        sort_method = "id"

    result = DBQuery.coach_pro_queries(
        request,

        coach_number_id,

        sort_method,
        order,
        query,
        search_param
    )

    print(result)

    # search query text in all database columns

    res_count = result.count()
    print(res_count)

    if order == "":
        order = "-"
    elif order == "-":
        order = ""

    context = {
        "data": result,

        "coach_number_id": coach_number_id,
        "order": order,
        "sort_method": sort_method,
        'search_param': search_param,
        "query": query,
    }

    return context
