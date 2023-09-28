from django.http import HttpResponse
import csv
from cmm.src.utitlity_functions.utitlities import CmmProUtilities
from cmm.models import Cmm_pro
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from s2analytica.common import log_time, getratelimit
from django_ratelimit.decorators import ratelimit

@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def download_data_csv_implementation_PRO(request):
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

@log_time
def download_helper_implementation_PRO(request):
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
     

    if request.method == 'POST':
        # filter_data = CmmUtilities.get_filters_data(request)
         
        
        all = request.POST.getlist('all', '')
         
        # checked_coach_numbers = request.POST.getlist('coach-number', '')
        coach_number_box = request.POST.get('coach_number_box')
        sort_method = request.POST.get('sort-method', '')

        

        checked_coach_numbers_str = request.POST.get("coach-number-dropdown", "")
        if checked_coach_numbers_str != "":
            checked_coach_numbers = checked_coach_numbers_str.split(",")
        else:
            checked_coach_numbers = checked_coach_numbers_str


        print(f"Should download now")
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="Cmm_pro.csv"'
        writer = csv.writer(response)
        writer.writerow([
                        'Owning Rly',
                        'Coach Number',
                        'Coach Type',
                        'Coach Category',
                        'AC Flag',
                        'Gauge',
                        'POH/SS2/SS3/ DOC Date',
                        'Return Date',
                        'POH/SS2/SS3 Workshop',
                        'IOH/SS1 Date',
                        'IOH/SS1 Location',
                        'Expected IOH/SS1 Due Date',
                        'Extended Return Date',
                        'Manufacture',
                        'Nominated Workshop',
                        'Built Year',
                        'Base Depot',
                        'Maint. Depot',
                        'Maint. Division',
                        'Maint. Railway',
                        'Last Update Time',
                        'Updated By'

                    ])

        result_dict = {}
        print(coach_number_box)
        print("`````````````````````````````````````")
        print(checked_coach_numbers)
        print("``````````````````````````````````")
        if len(checked_coach_numbers) == 0 and not coach_number_box:
            data = []
        else:
            if coach_number_box:
                print("helloooooo")
                data = Cmm_pro.objects.all().values_list(
                    'owning_rly',
                    'coach_number',
                    'coach_type', 
                    'coach_category',  
                    'ac_flag',
                    'guage',
                    'POH_date',  
                    'return_date',  
                    'POH_work', 
                    'IOH_date', 
                    'IOH_location', 
                    'expected_IOH_date',  
                    'extend_return_date',
                    'manufacture', 
                    'nominated_workshop', 
                    'built_year', 
                    'base_depot', 
                    'main_depot', 
                    'main_division', 
                    'main_railway', 
                    'last_updated_time', 
                    'last_updated_by', 
                    ).filter(
                    Q(coach_number__in=checked_coach_numbers)|
                    Q(coach_number= coach_number_box)
                    )
            
            else:
                print("hello")
                data = Cmm_pro.objects.all().values_list(
                    'owning_rly',
                    'coach_number',
                    'coach_type', 
                    'coach_category',  
                    'ac_flag',
                    'guage',
                    'POH_date',  
                    'return_date',  
                    'POH_work', 
                    'IOH_date', 
                    'IOH_location', 
                    'expected_IOH_date',  
                    'extend_return_date',
                    'manufacture', 
                    'nominated_workshop', 
                    'built_year', 
                    'base_depot', 
                    'main_depot', 
                    'main_division', 
                    'main_railway', 
                    'last_updated_time', 
                    'last_updated_by', 
                    ).filter(
                    Q(coach_number__in=checked_coach_numbers)
                    )

            if sort_method == "asc":
                data= data.order_by('coach_number')
            elif sort_method == "desc":
                data= data.order_by('-coach_number')
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
