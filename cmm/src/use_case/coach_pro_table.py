from cmm.src.utitlity_functions.utitlities import CmmProUtilities
from cmm.src.data.DBQueries import DBQuery
from django_ratelimit.decorators import ratelimit
from django.contrib.auth.decorators import login_required

from s2analytica.common import log_time, getratelimit

@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def coach_pro_table_implementation(request):
    # data from db

    coach_number = CmmProUtilities.get_data('coach_number')

    all = []

    checked_coach_numbers = []

    coach_number_box = 0
    result = [[]]
    length = 0
    sort_method = 'desc'

    # print(f"workshop: ", workshop)
    # trains = []
    coach_nums = []
    # coach_cats = []

    # for train in train_number:
    #     if train != None:
    #         trains.append(train)

    for coach in coach_number:
        if coach != None:
            coach_nums.append(coach)

    # for coach in coach_category:
    #     if coach != None:
    #         coach_cats.append(coach)

    coach_numbers = set(list(map(int, coach_nums)))
    # actual_department = []
    # actual_coach_status = []
    # actual_vehicle_type = []

    if request.method == 'POST':
        # filter_data = CmmUtilities.get_filters_data(request)

        all = request.POST.getlist('all', '')

        coach_number_box = request.POST.get('coach_number_box')
        sort_method = request.POST.get('sort-method', '')

        checked_coach_numbers_str = request.POST.get(
            "coach-number-dropdown", "")
        if checked_coach_numbers_str != "":
            checked_coach_numbers = checked_coach_numbers_str.split(",")
        else:
            checked_coach_numbers = checked_coach_numbers_str

        # if 'both' in coach_status:
        #     actual_coach_status = ['SICKCH', 'FITAVL']
        # else:
        #     actual_coach_status = coach_status
        # if 'both' in department:
        #     actual_department = ['MECDFT', 'ELCDFT']
        # else:
        #     actual_department = department
        # if 'both' in vehicle_type:
        #     actual_vehicle_type = ['OCV', 'PCV']
        # else:
        #     actual_vehicle_type = vehicle_type
        # print(f"filter_data: ", filter_data)

        result = DBQuery.coach_pro_table_query(
            checked_coach_numbers, coach_number_box, sort_method)
        length = len(result)
    print(coach_number_box)
    if request.method != 'POST':
        checked_coach_numbers = sorted(coach_numbers)
        coach_number_box = coach_number_box
        sort_method = 'desc'
        DBQuery.coach_pro_table_query(
            checked_coach_numbers, coach_number_box, sort_method)
    context = {

        'coach_numbers': sorted(coach_numbers),

        'checked_coach_numbers': list(map(int, checked_coach_numbers)),
        'coach_number_box': coach_number_box,
        'checked_all': all,
        'method': request.method,
        'result': result,
        'length': length,
        # 'order': order,
        'sorting_method': sort_method,
    }
    return context
