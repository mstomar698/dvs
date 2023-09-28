from urllib import response
from cmm.src.utitlity_functions.utitlities import CmmSickUtilities
from cmm.constants import CmmGlobals as GLOBAL
from cmm.src.data.DBQueries import DBQuery
from cmm.models import Cmm_Sick as Data
from django_ratelimit.decorators import ratelimit

from s2analytica.common import log_time, getratelimit

@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def sick_head_table_implementation(request):
    train_number = CmmSickUtilities.get_data('train_number')
    coach_number = CmmSickUtilities.get_data('coach_number')
    coach_type = CmmSickUtilities.get_data('coach_type')
    owning_rly = CmmSickUtilities.get_data('owning_rly')
    vehicle_type = CmmSickUtilities.get_data('vehicle_type')
    department = CmmSickUtilities.get_data('department')
    workshop = CmmSickUtilities.get_data('workshop')

    order = 'desc'
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
    result = [[], []]
    trains = []
    length = 0
    coach_nums = []
    sorting_method = 'desc'

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
        sorting_method = request.POST.get('sort-method')

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

        result = DBQuery.sick_Head_table_query(train_numbers, checked_coach_types, checked_coach_numbers, sick_heads, owning_rly, actual_coach_status,
                                               actual_department, actual_vehicle_type, workshops, problem_start, problem_end, placement_start, placement_end, fit_start, fit_end, coach_count, sorting_method)
        length = len(result)

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
        'problem_start': problem_start,
        'problem_end': problem_end,
        'placement_start': placement_start,
        'placement_end': placement_end,
        'fit_start': fit_start,
        'fit_end': fit_end,
        'method': request.method,
        'result': result,
        'length': length,
        'order': order,
        'sorting_method': sorting_method,
    }
    return context
