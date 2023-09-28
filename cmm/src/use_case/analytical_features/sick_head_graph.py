from cmm.src.utitlity_functions.utitlities import CmmSickUtilities
from cmm.src.data.DBQueries import DBQuery
from cmm.src.utitlity_functions.utitlities import CmmSickUtilities
from cmm.src.utitlity_functions.utitlities import CmmSickUtilities
from cmm.constants import CmmGlobals as GLOBAL
from django_ratelimit.decorators import ratelimit

from s2analytica.common import log_time, getratelimit



@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def sick_head_graph_implementation(request):
    # data from db
    train_number = CmmSickUtilities.get_data('train_number')
    coach_number = CmmSickUtilities.get_data('coach_number')
    coach_type = CmmSickUtilities.get_data('coach_type')
    owning_rly = CmmSickUtilities.get_data('owning_rly')
    vehicle_type = CmmSickUtilities.get_data('vehicle_type')
    department = CmmSickUtilities.get_data('department')
    workshop = CmmSickUtilities.get_data('workshop')

    train_numbers = []
    sick_heads = []
    all = []
    owning_rly = []
    coach_status = []
    department = []
    vehicle_type = []
    workshops = []
    problem_start = ''
    problem_end = ''
    placement_start = ''
    placement_end = ''
    fit_start = ''
    fit_end = ''
    checked_coach_types = []
    checked_coach_numbers = []
    coach_count = 0
    result = [[], [], []]
    length = 0
    sort_method = 'desc'

    # print(f"workshop: ", workshop)
    trains = []
    coach_nums = []
    for train in train_number:
        if train != None:
            trains.append(train)

    for coach in coach_number:
        if coach != None:
            coach_nums.append(coach)

    coach_numbers = set(list(map(int, coach_nums)))
    actual_department = []
    actual_coach_status = []
    actual_vehicle_type = []

    if request.method == 'POST':
        # filter_data = CmmUtilities.get_filters_data(request)
        train_numbers = request.POST.getlist('train-numbers', '')
        sick_heads = request.POST.getlist('sick-heads', '')
        all = request.POST.getlist('all', '')
        owning_rly = request.POST.getlist('owning-rly', '')
        coach_status = request.POST.getlist('coach-status', '')
        department = request.POST.getlist('department', '')
        vehicle_type = request.POST.getlist('vehicle-type')
        workshops = request.POST.getlist('workshops', '')
        problem_start = request.POST.get('problem-start', '')
        problem_end = request.POST.get('problem-end', '')
        placement_start = request.POST.get('placement-start', '')
        placement_end = request.POST.get('placement-end', '')
        fit_start = request.POST.get('fit-start', '')
        fit_end = request.POST.get('fit-end', '')
        checked_coach_types = request.POST.getlist('coach-type', '')
        checked_coach_numbers = request.POST.getlist('coach-number', '')
        coach_count = request.POST.get('coach-count')
        sort_method = request.POST.get('sort-method', '')
        # print(f"***Coach_count***: {coach_count}")
        # print(f"***Type***: {type(coach_count)}")
        # print(f"checked_coach_types: {checked_coach_types}")
        # sick_groups = request.POST.getlist('sick-groups', '')
        # print(f"Coach_numbers: {checked_coach_numbers}")

        if 'both' in coach_status:
            actual_coach_status = ['SICKCH', 'FITAVL']
        else:
            actual_coach_status = coach_status
        if 'both' in department:
            actual_department = ['MECDFT', 'ELCDFT']
        else:
            actual_department = department
        if 'both' in vehicle_type:
            actual_vehicle_type = ['OCV', 'PCV']
        else:
            actual_vehicle_type = vehicle_type
        # print(f"filter_data: ", filter_data)

        result = DBQuery.sick_Head_graph_query(train_numbers, checked_coach_types, checked_coach_numbers, sick_heads, owning_rly, actual_coach_status,
                                               actual_department, actual_vehicle_type, workshops, problem_start, problem_end, placement_start, placement_end, fit_start, fit_end, coach_count, sort_method)
        length = len(result[2])

    context = {
        'sick_head': GLOBAL.SICK_HEAD,
        'train_numbers': list(map(int, trains)),
        'coach_numbers': coach_numbers,
        'coach_type': coach_type,
        'coach_status': GLOBAL.COACH_STATUS,
        'owning_rly': GLOBAL.OWNING_RLY,
        'vehicle_type': GLOBAL.VEHICLE_TYPE,
        'departments': GLOBAL.DEPARTMENTS,
        'main_depot': GLOBAL.MAIN_DEPOT,
        'workshops': GLOBAL.WORKSHOPS,
        'checked_trains': list(map(int, train_numbers)),
        # 'checked_sick_battery_group': GLOBAL.SICK_BATTERY_GROUP,
        # 'chekcked_sick_wheel_group': GLOBAL.SICK_WHEEL_GROUP,
        # 'checkded_others_group': GLOBAL.SICK_OTHER_GROUP,
        'checked_sick_heads': sick_heads,
        'checked_all': all,
        'checked_owning_rly': owning_rly,
        'checked_coach_status': coach_status,
        'checked_department': department,
        'checked_vehicle_type': vehicle_type,
        'checked_workshops': workshops,
        'checked_coach_type': checked_coach_types,
        'checked_coach_numbers': list(map(int, checked_coach_numbers)),
        'coach_count': coach_count,
        # 'checked_sick_groups': sick_groups,
        'problem_start': problem_start,
        'problem_end': problem_end,
        'placement_start': placement_start,
        'placement_end': placement_end,
        'fit_start': fit_start,
        'fit_end': fit_end,
        'method': request.method,
        'labels': result[0],
        'data': result[1],
        'length': length,
        'result': result[2],
        'sorting_method': sort_method,
        # 'checked_coach_type': filter_data['coach_type'],
        # 'checked_coach_number': filter_data['coach_number'],
        # 'checked_main_depot': filter_data['main_depot'],
    }

    return context
