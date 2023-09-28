from django.contrib import messages
from django.http import HttpResponse
import csv
from cmm.src.utitlity_functions.utitlities import CmmSickUtilities
from cmm.src.utitlity_functions.warranty_utilities import CmmUtilitie, CmmUtilitie_new


from django.contrib import messages
import datetime
from django.http import HttpResponse
import csv
from cmm.src.utitlity_functions.utitlities import CmmSickUtilities
from cmm.constants import CmmGlobals as GLOBAL
from cmm.models import Cmm_Sick, Cmm_Warranty, Cmm_Warranty_New
from s2analytica.common import log_time, getratelimit
from django.contrib.auth.decorators import login_required

from s2analytica.settings import END_TIME, IST, START_TIME
from datetime import datetime as dt
from django_ratelimit.decorators import ratelimit

@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def download_data_csv_implementation(request):
    train_number = CmmSickUtilities.get_data('train_number')
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
       if train_num != 'nan' and train_num != None and train_num != 'None' and train_num != '0.0':
            trains.append(float(train_num))

    for coach in coach_number:
        if coach != None:
            coach_nums.append(coach)
    for sick in sick_head:
        if sick != None:
            sicks.append(sick)

    coach_numbers = set(list(map(int, coach_nums)))
    trains.sort()
    sicks = sorted(sicks, reverse = False)
    coach_type = sorted(coach_type,reverse=False)
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
            'labels': result[0],
            'data': result[1],
            'length':length,
            'result': result[2],
            'sorting_method': sort_method,
        }
    return context

def download_helper_implementation(request):
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


    actual_department = []
    actual_coach_status = []
    actual_vehicle_type = []

    if request.method == 'POST':
        all = request.POST.getlist('all', '')
        problem_start = request.POST.get('problem-start', '')
        problem_end = request.POST.get('problem-end', '')
        placement_start = request.POST.get('placement-start', '')
        placement_end = request.POST.get('placement-end', '')
        fit_start = request.POST.get('fit-start', '')
        fit_end = request.POST.get('fit-end', '')

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

        data = []
        

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

        start = datetime.datetime.strptime(problem_start, "%Y-%m-%d")
        end = datetime.datetime.strptime(problem_end, "%Y-%m-%d")
        delta = end - start

        if delta.days <= -1:
            print("problem start date is greater than problem end date")    
            messages.error(request, "Please select valid date range. i.e., start date can not be greater than end date.")
        else:
            print(f"Should download now")
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="Cmm_Sick_from_{problem_start}_{problem_end}.csv"'
            writer = csv.writer(response)
            writer.writerow([
                        'Owning Rly',
                        'Coach Number',
                        'Coach Type',
                        'Sick Head',
                        'Cause of Sick Marking',
                        'Reported Defect',
                        'Work Done',
                        'Problem Date',
                        'Placement Date',
                        'Fit Date',
                        'Coach Status',
                        'Department',
                        'POH Date',
                        'IOH Date',
                        'AC Flag',
                        'Coach Category',
                        'Vehicle Type',
                        'Train Number',
                        'Maint. Depot',
                        'WorkShop',
                        'Created at',
                        'Created by',
                        'Updated at',
                        'Updated by'
                    ])

            # data = DbUtility.download_csv_query(train_numbers, sick_heads, owning_rly, actual_coach_status, actual_department, actual_vehicle_type, workshops, problem_start, problem_end, checked_coach_types, checked_coach_numbers)
            data = Cmm_Sick.objects.all().values_list(
                'owning_rly',
                'coach_number',
                'coach_type',
                'sick_head',
                'cause_of_sick_marking',
                'reported_defect',
                'work_done',
                'problem_date',
                'placement_date',
                'fit_date',
                'coach_status',
                'department',
                'POH_date',
                'IOH_date',
                'ac_flag',
                'coach_category',
                'vehicle_type',
                'train_number',
                'main_depot',
                'workshop',
                'created_at',
                'created_by',
                'updated_at',
                ).filter(
                train_number__in=train_numbers,
                sick_head__in=sick_heads,
                owning_rly__in=owning_rly,
                coach_status__in=actual_coach_status,
                department__in=actual_department,
                vehicle_type__in=actual_vehicle_type,
                coach_type__in=checked_coach_types,
                coach_number__in=checked_coach_numbers,
                workshop__in=workshops,
                problem_date__range=[
                    dt.strptime(f"{problem_start} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{problem_end} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST)],
                )
            
        for entry in data:
            writer.writerow(entry)
        return response


def download_warranty_complain_data_csv_implementation(request):
    complaint_id = CmmUtilitie.get_data('complaint_id')
    coach_number = CmmUtilitie.get_data('coach_number')
    failed_assembly = CmmUtilitie.get_data('failed_assembly')
    complaint_ids = []
    failed_assemblys = []
    all = []
    checked_coach_types = []
    checked_coach_numbers = []
    coach_count = 0
    result = [[], [], []]
    length = 0
    sort_method = 'desc'

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

    coach_numbers = sorted(set(list(map(int, coach_nums))))
    fails = sorted(fails,key = str.casefold)
    complains.sort()
    context = {
            'failed_assembly': fails,
            'complaint_ids': list(map(int, complains)),
            'coach_numbers': coach_numbers,
            'checked_complains': list(map(int, complaint_ids)),
            'checked_failed_assembly': failed_assembly,
            'checked_all': all,
            'checked_coach_numbers': list(map(int, checked_coach_numbers)),
            'coach_count': coach_count,
            'method': request.method,
            'labels': result[0],
            'data': result[1],
            'length':length,
            'result': result[2],
            'sorting_method': sort_method,
        }
    return context





def download_warranty_helper_implementation(request):
    complaint_ids = []
    failed_assembly = []
    sort_method = 'desc'
    all = []
    checked_coach_numbers = []
    coach_count = 0
    result = [[], [], []]
    length = 0


    if request.method == 'POST':
        all = request.POST.getlist('all', '')
        coach_count = request.POST.get('coach-count')
        sort_method = request.POST.get('sort-method', '')

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

        failed_assembly = request.POST.getlist('selectedValues', '') 

        

        print(f"Should download now")
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="Cmm_warranty_data.csv"'
        writer = csv.writer(response)
        writer.writerow([
                        'complaint Id ',
                        'Owning Rly',
                        'Coach Number',
                        'Coach Type',
                        'Factory Turnout Date',
                        'Complain By Depot',
                        'Complain By Division',
                        'Complain By Zone',
                        'Failed Assembly',
                        'Failure Description',
                        'Assembly Manufacture',
                        'Failure Date',
                        'Complain Date',
                        'Complain Status',
                        'Responsible PU/Workshop ',
                        'Closing Date By PU/Workshop',
                        'Remark By PU/Workshop ',
                        'Closing Date By Depot ',
                        'Remark By Depot ',
                        'Complainant Name',
                        'Designation ',
                        'Location ',
                        'Mobile ',
                        'Email id',
                        'Address',
                        'City',
                        'Created at',
                        'Created by',
                        'Updated at',
                        'Updated by'
                    ])

            # data = DbUtility.download_csv_query(train_numbers, sick_heads, owning_rly, actual_coach_status, actual_department, actual_vehicle_type, workshops, problem_start, problem_end, checked_coach_types, checked_coach_numbers)
        data = Cmm_Warranty.objects.all().values_list(
                'complaint_id',
                'owning_rly',
                'coach_number',
                'coach_type',
                'factory_tumont_date',
                'complain_by_depot',
                'complain_by_division',
                'complain_by_zone',
                'failed_assembly',
                'failure_description',
                'assembly_manufacture',
                'failure_date',
                'complain_date',
                'complain_status',
                'responsible_pu_workshop',
                'closing_date_pu_workshop',
                'remark_by_pu_workshop',
                'closing_date_by_depot',
                'remark_by_depot',
                'complaint_name',
                'designation',
                'location',
                'mobile',
                'email_id',
                'address',
                'city',
                'created_at',
                'created_by',
                'updated_at',
                ).filter(
                complaint_id__in=complaint_ids,
                failed_assembly__in=failed_assembly,
                coach_number__in=checked_coach_numbers,
                )
        if sort_method == "asc":
            data= data.order_by('complaint_id')
        elif sort_method == "desc":
            data= data.order_by('-complaint_id')    
        for entry in data:
            writer.writerow(entry)
        return response
# def download_data_csv(request):
#     coach_clean = []
#     bed_roll = []
#     security = []
#     medical_assis = []
#     punctuality = []
#     water_avail = []
#     electrical_equip = []
#     coach_maintain = []
#     miscellaneous = []
#     total_entries = Main_Data_Upload.objects.count()
#     staff_behave = []
#     complain_category = ""
#     complains = []
#     train_cats = TRAIN_CATS

#     ### new complain Type ####
#     Corruption_Bribery = []
#     Catering_and_Vending_Services = []
#     Divyangjan_Facilities = []
#     Facilities_for_Women_with_Special_needs = []

#     # train checkbox status arrays ######################
#     rncc = []
#     rgd = []
#     dnr = []
#     pnbe = []
#     ppta = []
#     ipr = []
#     keu = []
#     mka = []
#     ara = []
#     # checkbox status data objects #######################
#     train_type_rncc = Train_Type.objects.filter(Type="RNCC")
#     train_type_rgd = Train_Type.objects.filter(Type="RGD")
#     train_type_dnr = Train_Type.objects.filter(Type="DNR")
#     train_type_pnbe = Train_Type.objects.filter(Type="PNBE")
#     train_type_ppta = Train_Type.objects.filter(Type="PPTA")
#     train_type_ipr = Train_Type.objects.filter(Type="IPR")
#     train_type_keu = Train_Type.objects.filter(Type="KEU")
#     train_type_mka = Train_Type.objects.filter(Type="MKA")
#     train_type_ara = Train_Type.objects.filter(Type="ARA")
#     # train checkbox status loops to append into arrays ##
#     for rncc_train in train_type_rncc:
#         rncc.append(rncc_train.train_number)

#     for rgd_train in train_type_rgd:
#         rgd.append(rgd_train.train_number)

#     for dnr_train in train_type_dnr:
#         dnr.append(dnr_train.train_number)

#     for pnbe_train in train_type_pnbe:
#         pnbe.append(pnbe_train.train_number)

#     for ppta_train in train_type_ppta:
#         ppta.append(ppta_train.train_number)

#     for ipr_train in train_type_ipr:
#         ipr.append(ipr_train.train_number)

#     for keu_train in train_type_keu:
#         keu.append(keu_train.train_number)

#     for mka_train in train_type_mka:
#         mka.append(mka_train.train_number)

#     for ara_train in train_type_ara:
#         ara.append(ara_train.train_number)

#     ######################################################

#     trainsss = Main_Data_Upload.objects.all()
#     main_trains = []
#     for ttt in trainsss:
#         main_trains.append(float(ttt.train_station))
#     set_train = set(main_trains)
#     main_train = list(set_train)
#     ######
#     bottom_staff = []
#     bottom_staff_count = []
#     checked = []

#     color_code = [
#         "#FF3838",
#         "#FFB3B3",
#         "#006441",
#         "#FF8300",
#         "#EEFF70",
#         "#00FF83",
#         "#00E8FF",
#         "#4200FF",
#         "#BD00FF",
#         "#747474",
#         "#1D0249",
#         "#5F0037",
#         "#D33737",
#         "#00766B",
#     ]

#     all_type = [
#         "Coach - Cleanliness",
#         "Bed Roll",
#         "Security",
#         "Punctuality",
#         "Water Availability",
#         "Electrical Equipment",
#         "Medical Assistance",
#         "Coach - Maintenance",
#         "Miscellaneous",
#         "Staff Behaviour",
#         "Corruption Bribery",
#         "Catering and Vending Services",
#         "Divyangjan Facilities",
#         "Facilities for Women with Special needs",
#     ]

#     critical_type = [
#         "Coach - Cleanliness",
#         "Bed Roll",
#         "Water Availability",
#         "Electrical Equipment",
#         "Coach - Maintenance",
#     ]

                
#     if request.method == "POST":
#         post = True
#         problem_type = request.POST.getlist("problem_type")
#         train_number = request.POST.getlist("train_number")
#         complain_type = request.POST.getlist("complain_type")
#         start_date = request.POST.get("start_date", "")
#         end_date = request.POST.get("end_date", "")
#         complain_category = request.POST.getlist("complain-category")
#         complains = request.POST.getlist("complain-type")
#         check_type = request.POST.getlist("check-type")

#         start_month = datetime.datetime.strptime(start_date, "%Y-%m-%d")
#         end_month = datetime.datetime.strptime(end_date, "%Y-%m-%d")

#         delta = end_month - start_month

#         sdate = date(
#             int(start_month.year), int(start_month.month), int(start_month.day)
#         )
#         edate = date(int(end_month.year), int(end_month.month), int(end_month.day))

#         for tn in request.POST.getlist("train_number"):
#             checked.append(int(tn))

#         if delta.days <= -1:
#             return HttpResponse("<h1>Please Enter valid Date Range</h1>")
#         else:
#             response = HttpResponse(content_type='text/csv')
#             response['Content-Disposition'] = f'attachment; filename="Rail_madad_data_from_{start_date}_{end_date}.csv"'
#             writer = csv.writer(response)
#             writer.writerow(['Reference No.','registration_date','closing_date','disposal_time',
#                             'mode','train_number',
#                             'station_name','channel','Type',
#                             'coach_number','rake_number','staff_name',
#                             'staff_id','department','problem_type','sub_type',
#                             'commodity','zone','div','dept','breach','rating','status',
#                             'complaint_discription','remark','number_of_time_forwarded',
#                             'pnr_utc_number','coach_type','feedback_remark','upcoming_station','mobile_number_or_email',
#                             'physical_coach_number','train_name','created_at','updated_at','created_by','updated_by'
#                             ])

#             users = Main_Data_Upload.objects.all().values_list(
#                             'reference_no','registration_date','closing_date','disposal_time',
#                             'mode','train_station',
#                             'station_name','channel','Type',
#                             'coach_number','rake_number','staff_name',
#                             'staff_id','department','problem_type','sub_type',
#                             'commodity','zone','div','dept','breach','rating','status',
#                             'complaint_discription','remark','number_of_time_forwarded',
#                             'pnr_utc_number','coach_type','feedback_remark','upcoming_station','mobile_number_or_email',
#                             'physical_coach_number','train_name','created_at','updated_at','created_by','updated_by'
#                             ).filter(
#                                 registration_date__range=[f"{start_date} 00:00:00+00:00",f"{end_date} 23:59:00+00:00"],
#                                 problem_type__in=complain_type,
#                                 train_station__in=train_number)
#             for user in users:
#                 writer.writerow(user)

#             return response
#     if request.method != "POST":
#         post=False
#         start_date=None
#         end_date = None
#         train_number = None
#         check_type=None
#     context = {
#         "all_type": all_type,
#         "critical_type": critical_type,
#         "rgd": rgd,
#         "rncc": rncc,
#         "dnr": dnr,
#         "pnbe": pnbe,
#         "ppta": ppta,
#         "ipr": ipr,
#         "keu": keu,
#         "mka": mka,
#         "ara": ara,
#         "main_train": main_train,
#         "post": post,
#         "start_date": start_date,
#         "end_date": end_date,
#         "checked": checked,
#         "check_type": check_type,
#         "complain_category": complain_category,
#         "train_number": train_number,
#         "trains_cat": train_cats,
#         }
#     return render(request, 'download_data.html',context)


def download_warranty_complain_data_new_csv_implementation(request):
    complaint_id = CmmUtilitie_new.get_data('complaint_id')
    coach_number = CmmUtilitie_new.get_data('coach_number')
    failed_assembly = CmmUtilitie_new.get_data('failed_assembly')
    complaint_ids = []
    failed_assemblys = []
    all = []
    checked_coach_types = []
    checked_coach_numbers = []
    coach_count = 0
    result = [[], [], []]
    length = 0
    sort_method = 'desc'

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

    coach_numbers = sorted(set(list(map(int, coach_nums))))
    fails = sorted(fails,key = str.casefold)
    complains.sort()
    context = {
            'failed_assembly': fails,
            'complaint_ids': list(map(int, complains)),
            'coach_numbers': coach_numbers,
            'checked_complains': list(map(int, complaint_ids)),
            'checked_failed_assembly': failed_assembly,
            'checked_all': all,
            'checked_coach_numbers': list(map(int, checked_coach_numbers)),
            'coach_count': coach_count,
            'method': request.method,
            'labels': result[0],
            'data': result[1],
            'length':length,
            'result': result[2],
            'sorting_method': sort_method,
        }
    return context





def download_warranty_helper_new_implementation(request):
    complaint_ids = []
    failed_assembly = []
    sort_method = 'desc'
    all = []
    checked_coach_numbers = []
    coach_count = 0
    result = [[], [], []]
    length = 0


    if request.method == 'POST':
        all = request.POST.getlist('all', '')
        coach_count = request.POST.get('coach-count')
        sort_method = request.POST.get('sort-method', '')

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

        failed_assembly = request.POST.getlist('selectedValues', '') 


        print(f"Should download now")
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="Cmm_warranty_data_new.csv"'
        writer = csv.writer(response)
        writer.writerow([
                        'Complaint Id',
                        'Complaint by Zone',
                        'Complaint by Division',
                        'Complaint by Depot',
                        'Consignee Code',
                        'Complaint To',
                        'Owning Rly.',
                        'Coach Number',
                        'Coach Type',
                        'Failed Assembly',
                        'Assembly Manufacturer',
                        'Assembly SrNo',
                        'Assembly PlNo',
                        'Assembly Mfg.Date',
                        'Failure Date',
                        'Failure Desc.',
                        'Complaint Date',
                        'Complaint Status',
                        'Depot Remarks',
                        'Div. Remarks ',
                        'PU/WS Remarks',
                        'UDM Remarks',
                        'UDM Date',
                        'PU/WS Date',
                        'Div. Date',
                        'Complaint By Mobile No.',
                        'Created at',
                        'Created by',
                        'Updated at',
                        'Updated by'
                    ])

            # data = DbUtility.download_csv_query(train_numbers, sick_heads, owning_rly, actual_coach_status, actual_department, actual_vehicle_type, workshops, problem_start, problem_end, checked_coach_types, checked_coach_numbers)
        data = Cmm_Warranty_New.objects.all().values_list(
                'complaint_id',
                'complain_by_zone',
                'complain_by_division',
                'complain_by_depot',
                'consignee_code',
                'complaint_to',
                'owning_rly',
                'coach_number',
                'coach_type',
                'failed_assembly',
                'assembly_manufacture',
                'assembly_srno',
                'assembly_plno',
                'assembly_mfg_date',
                'failure_date',
                'failure_description',
                'complain_date',
                'complain_status',
                'depot_remarks',
                'div_remarks',
                'pu_ws_remarks',
                'udm_remarks',
                'udm_date',
                'pu_ws_date',
                'div_date',
                'complain_by_mobile',
                'created_at',
                'created_by',
                'updated_at',
                ).filter(
                complaint_id__in=complaint_ids,
                failed_assembly__in=failed_assembly,
                coach_number__in=checked_coach_numbers,
                )
        if sort_method == "asc":
            data= data.order_by('complaint_id')
        elif sort_method == "desc":
            data= data.order_by('-complaint_id')    
        for entry in data:
            writer.writerow(entry)
        return response