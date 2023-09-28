from cmm.src.utitlity_functions.warranty_utilities import CmmUtilitie, CmmUtilitie_new
from cmm.models import Failed_Assembly, Complaint_numbers
from cmm.src.data.DBQueries import DBQuery
from datetime import datetime as dt
from pytz import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from s2analytica.common import log_time, getratelimit
from django_ratelimit.decorators import ratelimit

import calendar

@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def warranty_complain_graph_implementation(request):
   
        # data from db
        coach_number = CmmUtilitie.get_data('coach_number')
        complaint_id = CmmUtilitie.get_data('complaint_id')
        failed_assembly = CmmUtilitie.get_data('failed_assembly')
        all = []
        complaint_ids = []
        failed_assemblys = []
        checked_coach_numbers = []
        coach_count = 0
        result = [[], [], []]
        length = 0
        sort_method = 'desc'
        complain_start = ''
        complain_end = ''
        failed_assembly_checked_data = []
        failed_assemblys_2=[]

        # print(f"workshop: ", workshop)
        complains = []
        coach_nums = []
        fails = []
        for complain in complaint_id:
            if complain != None:
                complains.append(complain)

        for coach in coach_number:
            if coach != None:
                coach_nums.append(coach)

        for fail in failed_assembly:
            if fail != None:
                fails.append(fail)
        coach_numbers = set(list(map(int, coach_nums)))

        failed_data= {} 
        failed_from_db= Failed_Assembly.objects.all()
        for i in failed_from_db:
            failed_data[i.failed_item]= i.id
        # print(failed_data)

        complain_data= {}

        complain_from_db= Complaint_numbers.objects.all()
        for i in complain_from_db:
            complain_data[i.complaint_id]= i.id
        # print(complain_data)



        if request.method == 'POST':
            all = request.POST.getlist('all', '')
            coach_count = request.POST.get('coach-count')
            sort_method = request.POST.get('sort-method', '')
            complain_start = request.POST.get('complain-start', '')
            complain_end = request.POST.get('complain-end', '')
            # print(failed_assemblys)


            checked_coach_numbers_str = request.POST.get("coach-number-dropdown", "")
            if checked_coach_numbers_str != "":
                checked_coach_numbers = checked_coach_numbers_str.split(",")
            else:
                checked_coach_numbers = checked_coach_numbers_str
            
            complaint_ids_str = request.POST.get("complain-id-dropdown", "")
            if complaint_ids_str != "":
                complaint_ids = complaint_ids_str.split(",")
            else:
                complaint_ids = complaint_ids_str

            failed_assemblys = request.POST.getlist('selectedValues', '') 
            failed_assemblys_2 = request.POST.getlist('selectedValues', '') 
            
            result = DBQuery.warranty_complain_graph_query(checked_coach_numbers, failed_assemblys,complaint_ids,complain_start, complain_end, coach_count, sort_method)
            length = len(result[2])
        failed_assemblys = sorted(failed_assemblys,reverse = False)
        fails = sorted(fails,key = str.casefold)
        if request.method != 'POST':
            current_time_get=dt.now(timezone("Asia/kolkata"))
            print(current_time_get)

            if(current_time_get.day > calendar.monthrange(current_time_get.year, current_time_get.month - 1)[1]):
                default_start = dt(current_time_get.year, current_time_get.month - 1, calendar.monthrange(current_time_get.year, current_time_get.month - 1)[1], 0, 0)
            
            else:
                default_start = dt(current_time_get.year, current_time_get.month - 1, current_time_get.day, 0, 0)
            
            checked_coach_numbers=sorted(coach_numbers)
            failed_assemblys=fails
            complaint_ids=list(map(int,complains))
            complain_start=default_start.strftime('%Y-%m-%d')
            complain_end=current_time_get.strftime('%Y-%m-%d')
            coach_count=coach_count
            sort_method= sort_method
            failed_assemblys_2=fails
            print(failed_assemblys)
            DBQuery.warranty_complain_graph_query(checked_coach_numbers, failed_assemblys,complaint_ids,complain_start, complain_end, coach_count, sort_method)
    

        checked_failed_data=[]
        for i in failed_assemblys:
            checked_failed_data.append(failed_data[i])
        
        # print(checked_failed_data)

        # print(complaint_ids)

        checked_complain_data=[]
        for i in complaint_ids:
            checked_complain_data.append(complain_data[float(i)])

        # print(checked_complain_data)

        failed_assembly_checked_data = []
        for i in failed_assemblys_2:
            if ("\r" in i):
                i = i.replace('\r', '')
                print("entered")
            failed_assembly_checked_data.append(i)
        
        complains.sort()
        context = {
            'failed_assembly': fails,
            'failed_data': failed_data,
            'complaint_ids': list(map(int,complains)),
            'coach_numbers': sorted(coach_numbers),
            'checked_complains': complaint_ids,
            'checked_complain_data': checked_complain_data,
            'checked_failed_assemblys': failed_assemblys,
            'checked_failed_data': checked_failed_data,
            'checked_all': all,
            'checked_coach_numbers': list(map(int, checked_coach_numbers)),
            'coach_count': coach_count,
            'complain_start': complain_start,
            'complain_end': complain_end,
            'method': request.method,
            'labels': result[0],
            'data': result[1],
            'length':length,
            'result': result[2],
            'sorting_method': sort_method,
            "failed_assembly_checked_data" : failed_assembly_checked_data
        }
        return context

@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def new_warranty_complain_graph_implementation(request):
    # try:
        # data from db
        coach_number = CmmUtilitie_new.get_data('coach_number')
        complaint_id = CmmUtilitie_new.get_data('complaint_id')
        failed_assembly = CmmUtilitie_new.get_data('failed_assembly')
        all = []
        complaint_ids = []
        failed_assemblys = []
        checked_coach_numbers = []
        coach_count = 0
        complain_start = ''
        complain_end = ''
        result = [[], [], []]
        length = 0
        sort_method = 'desc'
        failed_assembly_checked_data = []
        failed_assemblys_2=[]
        

        # print(f"workshop: ", workshop)
        complains = []
        coach_nums = []
        fails = []
        for complain in complaint_id:
            if complain != None:
                complains.append(complain)

        for coach in coach_number:
            if coach != None:
                coach_nums.append(coach)

        # print(failed_assembly)

        for fail in failed_assembly:
            if fail != None:
                fails.append(fail)
        coach_numbers = set(list(map(int, coach_nums)))

        failed_data= {} 
        failed_from_db= Failed_Assembly.objects.all()
        for i in failed_from_db:
            if ("\n" in i.failed_item):
                i.failed_item = i.failed_item.replace("\n", '')
            failed_data[i.failed_item]= i.id
        # print(failed_data)

        complain_data= {}

        complain_from_db= Complaint_numbers.objects.all()
        for i in complain_from_db:
            complain_data[i.complaint_id]= i.id
        # print(complain_data)

        if request.method == 'POST':
            # filter_data = CmmUtilities_new.get_filters_data(request)
            all = request.POST.getlist('all', '')
            coach_count = request.POST.get('coach-count')
            sort_method = request.POST.get('sort-method', '')
            complain_start = request.POST.get('complain-start', '')
            complain_end = request.POST.get('complain-end', '')
            print("new_warrranty graph implementation")
            

            checked_coach_numbers_str = request.POST.get("coach-number-dropdown", "")
            if checked_coach_numbers_str != "":
                checked_coach_numbers = checked_coach_numbers_str.split(",")
            else:
                checked_coach_numbers = checked_coach_numbers_str
            
            complaint_ids_str = request.POST.get("complain-id-dropdown", "")
            if complaint_ids_str != "":
                complaint_ids = complaint_ids_str.split(",")
            else:
                complaint_ids = complaint_ids_str
            failed_assemblys = request.POST.getlist('selectedValues', '') 
            failed_assemblys_2 = request.POST.getlist('selectedValues', '') 
            result = DBQuery.new_warranty_complain_graph_query(checked_coach_numbers, failed_assemblys,complaint_ids,complain_start, complain_end, coach_count, sort_method)
            length = len(result[2])
        failed_assemblys = sorted(failed_assemblys,reverse = False)
        fails = sorted(fails,key = str.casefold)


        if request.method != 'POST':
            current_time_get=dt.now(timezone("Asia/kolkata"))
            print(current_time_get)
            if(current_time_get.day > calendar.monthrange(current_time_get.year, current_time_get.month - 1)[1]):
                default_start = dt(current_time_get.year, current_time_get.month - 1, calendar.monthrange(current_time_get.year, current_time_get.month - 1)[1], 0, 0)
            
            else:
                default_start = dt(current_time_get.year, current_time_get.month - 1, current_time_get.day, 0, 0)
            checked_coach_numbers=sorted(coach_numbers)
            failed_assemblys=fails
            complaint_ids=list(map(int,complains))
            complain_start=default_start.strftime('%Y-%m-%d')
            complain_end=current_time_get.strftime('%Y-%m-%d')
            print(failed_assemblys)
            coach_count=coach_count
            sort_method= sort_method
            failed_assemblys_2 = fails


        checked_failed_data=[]
        for i in failed_assemblys:
            if ("\r\n" in i):
                i = i.replace('\r\n', '')
            elif ("\n" in i):
                i = i.replace('\n', '')
            checked_failed_data.append(failed_data[i])

        # print(complaint_ids)

        checked_complain_data=[]
        for i in complaint_ids:
            checked_complain_data.append(complain_data[float(i)])

        # print(checked_complain_data)
        failed_assembly_checked_data = []
        for i in failed_assemblys_2:
            if ("\r" in i):
                i = i.replace('\r', '')
            failed_assembly_checked_data.append(i)
            
            



        complains.sort()
        context = {
            'failed_assembly': fails,
            'failed_data': failed_data,
            'complaint_ids': list(map(int,complains)),
            'coach_numbers': sorted(coach_numbers),
            'checked_complains': complaint_ids,
            'checked_complain_data': checked_complain_data,
            'checked_failed_assemblys': failed_assemblys,
            'checked_failed_data': checked_failed_data,
            'checked_all': all,
            'checked_coach_numbers': list(map(int, checked_coach_numbers)),
            'coach_count': coach_count,
            'complain_start': complain_start,
            'complain_end': complain_end,
            'method': request.method,
            'labels': result[0],
            'data': result[1],
            'length':length,
            'result': result[2],
            'sorting_method': sort_method,
            "failed_assembly_checked_data" : failed_assembly_checked_data
        }
        return context
    # except:
    #     return render(request,"error.html")