from django.contrib.auth.decorators import login_required
from cmm.src.data.DBQueries import DBQuery
from cmm.models import Failed_Assembly, Complaint_numbers


@login_required
def complain_warranty_implementation(request, complain, complain_start, complain_end):
    if request.method =="GET":
    #   failed_data = request.GET.get("failed_assembly").split("---")
      failed_data = list(map(int, request.GET.get("failed_assembly").split("---")))
      complain_data = list(map(int, request.GET.get("complaint_id").split("-")))
    sort_method = request.GET.get("sort_method", "")
    order = request.GET.get("order", "")
    query = request.GET.get("query", "")
    search_param = request.GET.get("search_param", "")

    print(failed_data)

    failed_assembly_from_db = {}
    failed_from_db = Failed_Assembly.objects.all()
    for i in failed_from_db:
        failed_assembly_from_db[i.id] = i.failed_item

    print(failed_assembly_from_db)

    failed_assembly = []
    for i in failed_data:
        failed_assembly.append(failed_assembly_from_db[i])

    print(failed_assembly)

    print(complain_data)

    complain_data_from_db = {}
    complain_from_db = Complaint_numbers.objects.all()
    for i in complain_from_db:
        complain_data_from_db[i.id] = i.complaint_id

    print(complain_data_from_db)

    complaint_id = []
    for i in complain_data:
        complaint_id.append(complain_data_from_db[i])

    print(f"complaint_id: {complaint_id}")
    print(f"failed_assembly: {failed_assembly}")
    print(f"sort_method: {sort_method}")
    print(f"order: {order}")
    print(f"query: {query}")
    print(f"Seach_param: {search_param}")
    print("--------------------------------------------------------------")

    if sort_method == "" or sort_method == None:
        sort_method = "id"

    result = DBQuery.complain_warranty_query(
        request,
        complain,
        failed_assembly,
        complaint_id,
        sort_method,
        order,
        query,
        search_param,
        complain_start,
        complain_end
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
        "complaint_id": complaint_id,
        "complaint_data": complain_data,
        "failed_assembly": failed_assembly,
        "failed_data": failed_data,
        "complain": complain,
        'complain_start': complain_start,
        'complain_end': complain_end,
        "order": order,
        "sort_method": sort_method,
        'search_param': search_param,
        "query": query,
    }
    return context

@login_required
def new_complain_warranty_implementation(request, complain, complain_start, complain_end):
    if request.method == "GET":
        #   failed_assembly = request.GET.get("failed_assembly").split("---")
        failed_data = list(
            map(int, request.GET.get("failed_assembly").split("---")))
        complain_data = list(
            map(int, request.GET.get("complaint_id").split("-")))
    sort_method = request.GET.get("sort_method", "")
    order = request.GET.get("order", "")
    query = request.GET.get("query", "")
    search_param = request.GET.get("search_param", "")

    print(failed_data)

    failed_assembly_from_db = {}
    failed_from_db = Failed_Assembly.objects.all()
    for i in failed_from_db:
        failed_assembly_from_db[i.id] = i.failed_item

    print(failed_assembly_from_db)

    failed_assembly = []
    for i in failed_data:
        failed_assembly.append(failed_assembly_from_db[i])

    print(failed_assembly)

    print(complain_data)

    complain_data_from_db = {}
    complain_from_db = Complaint_numbers.objects.all()
    for i in complain_from_db:
        complain_data_from_db[i.id] = i.complaint_id

    print(complain_data_from_db)

    complaint_id = []
    for i in complain_data:
        complaint_id.append(complain_data_from_db[i])

    print(f"complaint_id: {complaint_id}")
    print(f"failed_assembly: {failed_assembly}")
    print(f"sort_method: {sort_method}")
    print(f"order: {order}")
    print(f"query: {query}")
    print(f"Seach_param: {search_param}")
    print("--------------------------------------------------------------")

    if sort_method == "" or sort_method == None:
        sort_method = "id"

    result = DBQuery.new_complain_warranty_query(
        request,
        complain,
        failed_assembly,
        complaint_id,
        sort_method,
        order,
        query,
        search_param,
        complain_start,
        complain_end
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
        "complaint_id": complaint_id,
        "complaint_data": complain_data,
        "failed_assembly": failed_assembly,
        "failed_data": failed_data,
        "complain": complain,
        'complain_start': complain_start,
        'complain_end': complain_end,
        "order": order,
        "sort_method": sort_method,
        'search_param': search_param,
        "query": query,
    }
    return context
