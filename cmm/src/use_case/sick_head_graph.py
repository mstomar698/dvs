from django.shortcuts import render
from cmm.src.utitlity_functions.utitlities import CmmSickUtilities
from cmm.constants import CmmGlobals as GLOBAL
from cmm.src.data.DBQueries import DBQuery
import numpy as np
from datetime import datetime as dt
from pytz import timezone
from django.contrib.auth.decorators import login_required

from s2analytica.common import log_time, getratelimit
from django_ratelimit.decorators import ratelimit

import calendar

@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required
def sick_head_graph_implementation(request):
    # data from db
        train_number = CmmSickUtilities.get_data('train_number')
        print(f'Train Numbers for render:{train_number}')
        coach_number = CmmSickUtilities.get_data('coach_number')
        coach_type = CmmSickUtilities.get_data('coach_type')
        owning_rly = CmmSickUtilities.get_data('owning_rly')
        vehicle_type = CmmSickUtilities.get_data('vehicle_type')
        department = CmmSickUtilities.get_data('department')
        sick_head = CmmSickUtilities.get_data('sick_head')
        

        
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
        trainss = []
        trains = []
        coach_nums = []
        sicks = []
        for train in train_number:
            trainss.append(str(train))
    
        for train_num in trainss:
            if train_num != 'nan' and train_num != None and train_num != 'None':
                    trains.append(float(train_num))

        for coach in coach_number:
            if coach != None:
                coach_nums.append(coach)
        
        for sick in sick_head:
            if sick != None:
                sicks.append(sick)

        coach_numbers = set(list(map(int, coach_nums)))
        actual_department = []
        actual_coach_status = []
        actual_vehicle_type = []

        if request.method == 'POST':
            # filter_data = CmmUtilities.get_filters_data(request)
            all = request.POST.getlist('all', '')
            # print(f"Workshops: {workshops}")
            problem_start = request.POST.get('problem-start', '')
            problem_end = request.POST.get('problem-end', '')
            placement_start = request.POST.get('placement-start', '')
            placement_end = request.POST.get('placement-end', '')
            fit_start = request.POST.get('fit-start', '')
            fit_end = request.POST.get('fit-end', '')
            coach_count = request.POST.get('coach-count')
            sort_method = request.POST.get('sort-method', '')
            # print(f"***Coach_count***: {coach_count}")
            # print(f"***Type***: {type(coach_count)}")
            # print(f"checked_coach_types: {checked_coach_types}")
            # sick_groups = request.POST.getlist('sick-groups', '')
            # print(f"Coach_numbers: {checked_coach_numbers}")

            train_numbers_str = request.POST.get("train-number-dropdown", "")
            if train_numbers_str != "":
                train_numbers = train_numbers_str.split(",")
            else:
                train_numbers = train_numbers_str

            sick_heads_str = request.POST.get("sick-head-dropdown", "")
            if sick_heads_str != "":
                sick_heads = sick_heads_str.split(",")
            else:
                sick_heads = sick_heads_str

            owning_rly_str = request.POST.get("owning-rly-dropdown", "")
            if owning_rly_str != "":
                owning_rly = owning_rly_str.split(",")
            else:
                owning_rly = owning_rly_str

            coach_status_str = request.POST.get("coach-status-dropdown", "")
            if coach_status_str != "":
                coach_status = coach_status_str.split(",")
            else:
                coach_status = coach_status_str

            department_str = request.POST.get("department-dropdown", "")
            if department_str != "":
                department = department_str.split(",")
            else:
                department = department_str

            vehicle_type_str = request.POST.get("vehicle-type-dropdown", "")
            if vehicle_type_str != "":
                vehicle_type = vehicle_type_str.split(",")
            else:
                vehicle_type = vehicle_type_str

            workshops_str = request.POST.get("workshops-dropdown", "")
            if workshops_str != "":
                workshops = workshops_str.split(",")
            else:
                workshops = workshops_str

            checked_coach_types_str = request.POST.get("coach-type-dropdown", "")
            if checked_coach_types_str != "":
                checked_coach_types = checked_coach_types_str.split(",")
            else:
                checked_coach_types = checked_coach_types_str

            checked_coach_numbers_str = request.POST.get("coach-number-dropdown", "")
            if checked_coach_numbers_str != "":
                checked_coach_numbers = checked_coach_numbers_str.split(",")
            else:
                checked_coach_numbers = checked_coach_numbers_str

            

            if 'both' in coach_status:
                actual_coach_status = ['FITAVL','SICKCH']
            else:
                actual_coach_status = coach_status
            if 'both' in department:
                actual_department = [ 'ELCDFT','MECDFT']
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
            print(f'Result: {result}')
        if request.method != 'POST':
            current_time_get=dt.now(timezone("Asia/kolkata"))
            print(current_time_get)

            if(current_time_get.day > calendar.monthrange(current_time_get.year, current_time_get.month - 1)[1]):
                default_start = dt(current_time_get.year, current_time_get.month - 1, calendar.monthrange(current_time_get.year, current_time_get.month - 1)[1], 0, 0)
            
            else:
                default_start = dt(current_time_get.year, current_time_get.month - 1, current_time_get.day, 0, 0)
            
            problem_start=default_start.strftime('%Y-%m-%d')
            problem_end= current_time_get.strftime('%Y-%m-%d')
            placement_start=default_start.strftime('%Y-%m-%d')
            placement_end= current_time_get.strftime('%Y-%m-%d')
            fit_start=default_start.strftime('%Y-%m-%d')
            fit_end=current_time_get.strftime('%Y-%m-%d')
            train_numbers= list(map(int, trains))
            checked_coach_numbers = sorted(coach_numbers)
            checked_coach_types=coach_type
            sick_heads=sicks
            owning_rly= GLOBAL.OWNING_RLY    
            workshops=GLOBAL.WORKSHOPS
            coach_count=coach_count
            sort_method= sort_method
            department=GLOBAL.DEPARTMENTS
            actual_department=department
            coach_status=GLOBAL.COACH_STATUS
            actual_coach_status=coach_status              
            vehicle_type=GLOBAL.VEHICLE_TYPE
            actual_vehicle_type=vehicle_type
            print(owning_rly)
            DBQuery.sick_Head_graph_query(train_numbers, checked_coach_types, checked_coach_numbers, sick_heads, owning_rly, actual_coach_status,
                                                actual_department, actual_vehicle_type, workshops, problem_start, problem_end, placement_start, placement_end, fit_start, fit_end, coach_count, sort_method)
        sicks = sorted(sicks, reverse = False)
        coach_type = sorted(coach_type,reverse=False)
        trains.sort()
        context = {
            'sick_head': sicks,
            'train_numbers': list(map(int, trains)),
            'coach_numbers': sorted(coach_numbers),
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
            "checked_train_numbers" : train_numbers,
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
            'length':length,
            'result': result[2],
            'sorting_method': sort_method,
            # 'checked_coach_type': filter_data['coach_type'],
            # 'checked_coach_number': filter_data['coach_number'],
            # 'checked_main_depot': filter_data['main_depot'],
        }
        return context
