from django.http import HttpResponse
from datetime import datetime as dt, date
from s2analytica.settings import IST, START_TIME, END_TIME
from railmadad.models import Main_Data_Upload
from railmadad.constants import *
from django.db.models import Count
import calendar
from pytz import timezone
from dateutil.rrule import rrule, MONTHLY
from datetime import date, timedelta
from django.db.models import Sum

class DBQuery:
    def clear_variables():
        coach_clean.clear()
        bed_roll.clear()
        security.clear()
        medical_assis.clear()
        punctuality.clear()
        water_avail.clear()
        electrical_equip.clear()
        coach_maintain.clear()
        miscellaneous.clear()
        Corruption_Bribery.clear()
        Catering_and_Vending_Services.clear()
        Divyangjan_Facilities.clear()
        Facilities_for_Women_with_Special_needs.clear()
        staff_behave.clear()
    
    
    def all_complain_sub_type_train(
        train_number,
        start_date,
        end_date ,
        check_type,
        start_month,
        end_month,
        subtype,
        t_r,
    ):

        sub_type_filter_data = Main_Data_Upload.objects.filter(
                                        registration_date__range=[
                                            dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                                            dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                                        ],
                                        sub_type=f"{subtype}",
                                        train_station=float(t_r),
                                    )
        return sub_type_filter_data
    
    def complain_type_interactive_disposal_date(
        train_numbers_list,
        actual_month_number,
        year ,
        complains_list,
        date
    ):
        if date =="00":
            problem_types = Main_Data_Upload.objects.values_list(
                "physical_coach_number",
                "train_station",
                "problem_type",
                "sub_type",
                "disposal_time",
                "rating",
                "registration_date",
                "complaint_discription",
                "staff_name",
                "reference_number",
                'staff_id',
                'remark',
                "rake_number",
                "closing_date",
            ).filter(
                problem_type__in=complains_list,
                train_station__in=train_numbers_list,
                # registration_date__day=date,
                registration_date__month=actual_month_number,
                registration_date__year=year,
            ) 
        else:    
            problem_types = Main_Data_Upload.objects.values_list(
                "physical_coach_number",
                "train_station",
                "problem_type",
                "sub_type",
                "disposal_time",
                "rating",
                "registration_date",
                "complaint_discription",
                "staff_name",
                "reference_number",
                'staff_id',
                'remark',
                "rake_number",
                "closing_date",
            ).filter(
                problem_type__in=complains_list,
                train_station__in=train_numbers_list,
                registration_date__day=date,
                registration_date__month=actual_month_number,
                registration_date__year=year,
            )
        return problem_types
    
    def complain_type_interactive_disposal_train(
        train_numbers_list,
        complains_list,
        start_date,
        end_date
    ):  
        problem_types = Main_Data_Upload.objects.values_list(
            "physical_coach_number",
            "train_station",
            "problem_type",
            "sub_type",
            "disposal_time",
            "rating",
            "registration_date",
            "complaint_discription",
            "staff_name",
            "reference_number",
            'staff_id',
            'remark',
            "rake_number",
            "closing_date",
        ).filter(
             problem_type__in=complains_list,
             train_station__in=train_numbers_list,
             registration_date__range=[
              dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                f"{end_date} {END_TIME}+00:00"
            ]
        )
        return problem_types
    def complain_type_interactive_disposal_coach(
        request,
        complains_list,
        start_date,
        end_date
    ):  
        problem_types = Main_Data_Upload.objects.values_list(
            "physical_coach_number",
            "train_station",
            "problem_type",
            "sub_type",
            "disposal_time",
            "rating",
            "registration_date",
            "complaint_discription",
            "staff_name",
            "reference_number",
            'staff_id',
            'remark',
            "rake_number",
            "closing_date",
        ).filter(
            problem_type__in=request.GET.get("complain_type").split("--"),
            physical_coach_number=request.GET.get("physical_coach_number"),
            registration_date__range=[
                dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                f"{end_date} {END_TIME}+00:00"
            ]
        )
        return problem_types
    def complain_type_interactive_disposal_sub_type(
        request,
        train_numbers_list,
        actual_month_number,
        year,
        date
    ):  
        if date=="00":
            problem_types = Main_Data_Upload.objects.values_list(
                "physical_coach_number",
                "train_station",
                "problem_type",
                "sub_type",
                "disposal_time",
                "rating",
                "registration_date",
                "complaint_discription",
                "staff_name",
                "reference_number",
                'staff_id',
                'remark',
                "rake_number",
                "closing_date",
            ).filter(
                sub_type=request.GET.get("sub_type"),
                train_station__in=train_numbers_list,
                # registration_date__day=date,
                registration_date__month=actual_month_number,
                registration_date__year=year,
            )
        else:
             problem_types = Main_Data_Upload.objects.values_list(
            "physical_coach_number",
            "train_station",
            "problem_type",
            "sub_type",
            "disposal_time",
            "rating",
            "registration_date",
            "complaint_discription",
            "staff_name",
            "reference_number",
            'staff_id',
            'remark',
            "rake_number",
            "closing_date",
        ).filter(
            sub_type=request.GET.get("sub_type"),
            train_station__in=train_numbers_list,
            registration_date__day=date,
            registration_date__month=actual_month_number,
            registration_date__year=year,
        )
        return problem_types
    def disposal_time_coach_wise(
        complain_type,
        train_number,
        start_date,
        end_date    
    ):
        data = Main_Data_Upload.objects.filter(
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    f"{end_date} {END_TIME}+00:00"
                ],
                problem_type__in = complain_type,
                train_station__in = train_number
                )
        return data
    # def disposal_time_date_wise(
    #         i,
    #     sub_type,
    #     train_number,  
    #     day, 
    #     start_month,
    #     end_month,
        
    # ): 
    #     sdate = date(
    #         int(start_month.year), int(start_month.month), int(start_month.day)
    #     )
    #     day = sdate + timedelta(days=i)
    #     disposal_time = Main_Data_Upload.objects.filter(
    #                 registration_date__day=day.day,
    #                 registration_date__month=day.month,
    #                 registration_date__year=day.year,
    #                 sub_type = str(sub_type),
    #                 train_station__in = train_number
    #             )
    #     return disposal_time
    def disposal_time_train_wise(
        start_date,
        end_date,  
        complain_type ,
         tr  
    ):
        disposal_time = Main_Data_Upload.objects.filter(
                registration_date__range=[
                                        dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                                        f"{end_date} {END_TIME}+00:00"
                                    ],
                problem_type__in = complain_type,
                train_station = float(tr)
            )
        return disposal_time
    def maximum_complain_coach_clean_data(
        start_date,
        end_date,
        t_r, 
        checked
    ):
        coach_clean_data = Main_Data_Upload.objects.filter(
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                physical_coach_number=t_r,
                train_station__in= checked,
                problem_type="Coach - Cleanliness",
            )
        if len(coach_clean_data) > 0:
                temp_train = []
                for i in range(len(coach_clean_data)):
                    temp_train.append(coach_clean_data[i].train_station)
                    try:
                        c1 = (int(coach_clean_data.count()), int(t_r), "Coach - Cleanliness", temp_train)
                    except Exception as e:
                        print(f"Error in coach_clean_data: {e}")
                        c1 = None 
        else:
                try:
                    c1 = (int(coach_clean_data.count()), int(t_r), "Coach - Cleanliness")
                except Exception as e:
                    print(f"Error in coach_clean_data from else: {e}")
                    c1 = None  

        if c1 is not None:
                coach_clean.append(list(c1))

        return coach_clean
    
    def maximum_complain_coach_bed_data(
        start_date,
        end_date,
        t_r, 
        checked
    ):
        bed_data = Main_Data_Upload.objects.filter(
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                physical_coach_number=t_r,
                train_station__in= checked,
                problem_type="Bed Roll",
            )
        if len(bed_data) > 0:
                temp_train = []
                for i in range(len(bed_data)):
                    temp_train.append(bed_data[i].train_station)
                try:
                    b1 = (int(bed_data.count()), int(t_r), "Bed Roll", temp_train)
                except Exception as e:
                    print(f"Error in bed_data: {e}")
                    b1 = None
        else:
                try:
                    b1 = (int(bed_data.count()), int(t_r), "Bed Roll")
                except Exception as e:
                    print(f"Error in bed_data from else: {e}")
                    b1 = None

        if b1 is not None:
                bed_roll.append(list(b1))
        return bed_roll
    
    def maximum_complain_coach_security_data(
        start_date,
        end_date,
        t_r, 
        checked
    ):
        security_data = Main_Data_Upload.objects.filter(
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                physical_coach_number=t_r,
                train_station__in= checked,
                problem_type="Security",
            )
        if len(security_data) > 0:
                temp_train = []
                for i in range(len(security_data)):
                    temp_train.append(security_data[i].train_station)
                try:
                    s1 = (int(security_data.count()), int(t_r), "Security", temp_train)
                except Exception as e:
                    print(f"Error in security_data: {e}")
                    s1 = None
        else:
                try:
                    s1 = (int(security_data.count()), int(t_r), "Security")
                except Exception as e:
                    print(f"Error in security_data from else: {e}")
                    s1 = None

        if s1 is not None:
                security.append(list(s1))
        return security
    def maximum_complain_coach_medical_data(
        start_date,
        end_date,
        t_r, 
        checked
    ):
        medical_data = Main_Data_Upload.objects.filter(
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                physical_coach_number=t_r,
                train_station__in= checked,
                problem_type="Medical Assistance",
            )
        if len(medical_data) > 0:
                temp_train = []
                for i in range(len(medical_data)):
                    temp_train.append(medical_data[i].train_station)
                try:
                    m1 = (int(medical_data.count()), int(t_r), "Medical Assistance", temp_train)
                except Exception as e:
                    print(f"Error in medical_data: {e}")
                    m1 = None
        else:
                try:
                    m1 = (int(medical_data.count()), int(t_r), "Medical Assistance")
                except Exception as e:
                    print(f"Error in medical_data from else: {e}")
                    m1 = None

        if m1 is not None:
                medical_assis.append(list(m1))
        return medical_assis
    
    def maximum_complain_coach_punctuality_data(
        start_date,
        end_date,
        t_r, 
        checked
    ):
        punctuality_data = Main_Data_Upload.objects.filter(
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                physical_coach_number=t_r,
                train_station__in= checked,
                problem_type="Punctuality",
            )
        if len(punctuality_data) > 0:
                temp_train = []
                for i in range(len(punctuality_data)):
                    temp_train.append(punctuality_data[i].train_station)
                try:
                    p1 = (int(punctuality_data.count()), int(t_r), "Punctuality", temp_train)
                except Exception as e:
                    print(f"Error in punctuality_data: {e}")
                    p1 = None
        else:
                try:
                    p1 = (int(punctuality_data.count()), int(t_r), "Punctuality")
                except Exception as e:
                    print(f"Error in punctuality_data from else: {e}")
                    p1 = None

        if p1 is not None:
                punctuality.append(list(p1))
        
        return punctuality
    def maximum_complain_coach_water_data(
        start_date,
        end_date,
        t_r, 
        checked
    ): 
        water_data = Main_Data_Upload.objects.filter(
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                physical_coach_number=t_r,
                train_station__in= checked,
                problem_type="Water Availability",
            )
        if len(water_data) > 0:
                temp_train = []
                for i in range(len(water_data)):
                    temp_train.append(water_data[i].train_station)
                try:
                    w1 = (int(water_data.count()), int(t_r), "Water Availability", temp_train)
                except Exception as e:
                    print(f"Error in water_data: {e}")
                    w1 = None
        else:
                try:
                    w1 = (int(water_data.count()), int(t_r), "Water Availability")
                except Exception as e:
                    print(f"Error in water_data from else: {e}")
                    w1 = None

        if w1 is not None:
                water_avail.append(list(w1))
        return  water_avail 
    def maximum_complain_coach_electrical_data(
        start_date,
        end_date,
        t_r, 
        checked
    ): 
        electrical_data = Main_Data_Upload.objects.filter(
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                physical_coach_number=t_r,
                train_station__in= checked,
                problem_type="Electrical Equipment",
            )
        if len(electrical_data) > 0:
                temp_train = []
                for i in range(len(electrical_data)):
                    temp_train.append(electrical_data[i].train_station)
                try:
                    e1 = (int(electrical_data.count()), int(t_r), "Electrical Equipment", temp_train)
                except Exception as e:
                    print(f"Error in electrical_data: {e}")
                    e1 = None
        else:
                try:
                    e1 = (int(electrical_data.count()), int(t_r), "Electrical Equipment")
                except Exception as e:
                    print(f"Error in electrical_data from else: {e}")
                    e1 = None    

        if e1 is not None:
                electrical_equip.append(list(e1)) 
        return electrical_equip
    def maximum_complain_coach_maintain_data(
        start_date,
        end_date,
        t_r, 
        checked
    ):
        coach_maintain_data = Main_Data_Upload.objects.filter(
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                physical_coach_number=t_r,
                train_station__in= checked,
                problem_type="Coach - Maintenance",
            )
        if len(coach_maintain_data) > 0:
                temp_train = []
                for i in range(0, len(coach_maintain_data)):
                    temp_train.append(coach_maintain_data[i].train_station)
                try:
                    c2 = (int(coach_maintain_data.count()), int(t_r), "Coach - Maintenance", temp_train)
                except Exception as e:
                    print(f"Error in coach_maintain_data: {e}")
                    c2 = None        
        else:
                try:
                    c2 = (int(coach_maintain_data.count()), int(t_r), "Coach - Maintenance")
                except Exception as e:
                    print(f"Error in coach_maintain_data from else: {e}")
                    c2 = None    
            
        if c2 is not None:                     
                coach_maintain.append(list(c2))
        return coach_maintain
    def maximum_complain_coach_miscellaneous_data(
        start_date,
        end_date,
        t_r, 
        checked
    ):
        miscellaneous_data = Main_Data_Upload.objects.filter(
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                physical_coach_number=t_r,
                train_station__in= checked,
                problem_type="Miscellaneous",
            )
        if len(miscellaneous_data) > 0:
                temp_train = []
                for i in range(0, len(miscellaneous_data)):
                    temp_train.append(miscellaneous_data[i].train_station)
                try:
                    m2 = (int(miscellaneous_data.count()), int(t_r), "Miscellaneous", temp_train)
                except Exception as e:
                    print(f"Error in miscellaneous_data: {e}")
                    m2 = None
        else:
                try:
                    m2 = (int(miscellaneous_data.count()), int(t_r), "Miscellaneous")
                except Exception as e:
                    print(f"Error in miscellaneous_data from else: {e}")
                    m2 = None

        if m2 is not None:
                miscellaneous.append(list(m2))
        return miscellaneous
    def maximum_complain_coach_behave_data(
        start_date,
        end_date,
        t_r, 
        checked
    ): 
        staff_behave_data = Main_Data_Upload.objects.filter(
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                physical_coach_number=t_r,
                train_station__in= checked,
                problem_type="Staff Behaviour",
            )
        if len(staff_behave_data) > 0:
                temp_train = []
                for i in range(0, len(staff_behave_data)):
                    temp_train.append(staff_behave_data[i].train_station)
                try:
                    s2 = (int(staff_behave_data.count()), int(t_r), "Staff Behaviour", temp_train)
                except Exception as e:
                    print(f"Error in staff_behave_data: {e}")
                    s2 = None
        else:
                try:
                    s2 = (int(staff_behave_data.count()), int(t_r), "Staff Behaviour")
                except Exception as e:
                    print(f"Error in staff_behave_data from else: {e}")
                    s2 = None

        if s2 is not None:
                staff_behave.append(list(s2))
        return staff_behave
    def maximum_complain_train_clean_data(
        start_date,
        end_date,
        t_r, 
    ):
        coach_clean_data =Main_Data_Upload.objects.filter(
             registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                train_station=t_r,
                problem_type="Coach - Cleanliness",
            )
        return coach_clean_data
    
    def maximum_complain_train_bed_data(
        start_date,
        end_date,
        t_r, 
    ):
        bed_data = Main_Data_Upload.objects.filter(
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                train_station=t_r,
                problem_type="Bed Roll",
            )
        return bed_data
    
    def maximum_complain_train_security_data(
        start_date,
        end_date,
        t_r, 
    ):
        security_data = Main_Data_Upload.objects.filter(
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                train_station=t_r,
                problem_type="Security",
            )
        return security_data
    def maximum_complain_train_medical_data(
        start_date,
        end_date,
        t_r, 
    ):
        medical_data = Main_Data_Upload.objects.filter(
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                train_station=t_r,
                problem_type="Medical Assistance",
            )
        return medical_data
    
    def maximum_complain_train_punctuality_data(
        start_date,
        end_date,
        t_r, 
    ):
        punctuality_data = Main_Data_Upload.objects.filter(
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                train_station=t_r,
                problem_type="Punctuality",
            )    
        return punctuality_data
    def maximum_complain_train_water_data(
        start_date,
        end_date,
        t_r, 
    ): 
        water_data = Main_Data_Upload.objects.filter(
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                train_station=t_r,
                problem_type="Water Availability",
            )
        return  water_data
    def maximum_complain_train_electrical_data(
        start_date,
        end_date,
        t_r, 
    ): 
        electrical_data = Main_Data_Upload.objects.filter(
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                train_station=t_r,
                problem_type="Electrical Equipment",
            )
        return electrical_data
    def maximum_complain_train_maintain_data(
        start_date,
        end_date,
        t_r, 
    ):
        coach_maintain_data = Main_Data_Upload.objects.filter(
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                train_station=t_r,
                problem_type="Coach - Maintenance",
            )
        return coach_maintain_data
    def maximum_complain_train_miscellaneous_data(
        start_date,
        end_date,
        t_r, 
    ):
        miscellaneous_data = Main_Data_Upload.objects.filter(
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                train_station=t_r,
                problem_type="Miscellaneous",
            )
        return miscellaneous_data
    def maximum_complain_train_behave_data(
        start_date,
        end_date,
        t_r, 
    ): 
        staff_behave_data = Main_Data_Upload.objects.filter(
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                train_station=t_r,
                problem_type="Staff Behaviour",
            )
        return staff_behave_data
    def maximum_complain_train_corruption_data(
        start_date,
        end_date,
        t_r, 
    ): 
        corruption_data = Main_Data_Upload.objects.filter(
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                train_station=t_r,
                problem_type="Corruption Bribery",
            )
        return corruption_data
    def maximum_complain_train_catering_vending_data(
        start_date,
        end_date,
        t_r, 
    ): 
        catering_vending = Main_Data_Upload.objects.filter(
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                train_station=t_r,
                problem_type="Catering & Vending Services",
            )
        return catering_vending
    def maximum_complain_train_divyang_fascilities_data(
        start_date,
        end_date,
        t_r, 
    ): 
        divyang_fascilities = Main_Data_Upload.objects.filter(
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                train_station=t_r,
                problem_type="Divyangjan Facilities",
            )
        return divyang_fascilities
    def maximum_complain_train_women_sp_need_data(
        start_date,
        end_date,
        t_r, 
    ): 
        women_sp_need = Main_Data_Upload.objects.filter(
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                train_station=t_r,
                problem_type="Facilities for Women with Special needs  ",
            )
        return women_sp_need 
    def physical_coach_number_wise_complain_mix_main_data(
        complain_type, 
        all_coaches_lists,     
        start_date,
        end_date,
    ): 
        main_sorted_data = Main_Data_Upload.objects.values("physical_coach_number").filter(
                                                            problem_type__in=complain_type,
                                                            physical_coach_number__in=all_coaches_lists,
                                                            registration_date__range=[
                                                                dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                                                                dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                                                            ],).annotate(count=Count('physical_coach_number')).order_by("-count")
        return main_sorted_data 
    def physical_coach_number_wise_complain_mix_clean_data(
        r,    
        start_date,
        end_date,
    ): 
        data1 = Main_Data_Upload.objects.filter(
                physical_coach_number=float(r),
                problem_type='Coach - Cleanliness',
                registration_date__range=[
                            dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            f"{end_date} {END_TIME}+00:00"],
            )
        coach_clean.append(data1.count())
        return coach_clean
    def physical_coach_number_wise_complain_mix_bed_data(
        r,  
        start_date,
        end_date,
    ): 
        data = Main_Data_Upload.objects.filter(
                physical_coach_number=float(r),
                problem_type="Bed Roll",
                registration_date__range=[
                            dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            f"{end_date} {END_TIME}+00:00"],
            )
        bed_roll.append(data.count())
        return bed_roll
    def physical_coach_number_wise_complain_mix_security_data(
        r,  
        start_date,
        end_date,
    ): 
        data = Main_Data_Upload.objects.filter(
                physical_coach_number=float(r),
                problem_type="Security",
                registration_date__range=[
                            dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            f"{end_date} {END_TIME}+00:00"],
            )
        security.append(data.count())
        return security
    def physical_coach_number_wise_complain_mix_medical_data(
        r,  
        start_date,
        end_date,
    ): 
        data = Main_Data_Upload.objects.filter(
                physical_coach_number=float(r),
                problem_type="Medical Assistance",
                registration_date__range=[
                            dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            f"{end_date} {END_TIME}+00:00"],
            )
        medical_assis.append(data.count())
        return medical_assis
    
    def physical_coach_number_wise_complain_mix_punctuality_data(
        r,  
        start_date,
        end_date,
    ): 
        data = Main_Data_Upload.objects.filter(
                physical_coach_number=float(r),
                problem_type="Punctuality",
                registration_date__range=[
                            dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            f"{end_date} {END_TIME}+00:00"],
            )
        punctuality.append(data.count())
        return punctuality
    
    def physical_coach_number_wise_complain_mix_water_data(
        r,  
        start_date,
        end_date,
    ): 
        data = Main_Data_Upload.objects.filter(
                physical_coach_number=float(r),
                problem_type="Water Availability",
                registration_date__range=[
                            dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            f"{end_date} {END_TIME}+00:00"],
            )
        water_avail.append(data.count())
        return water_avail
    
    def physical_coach_number_wise_complain_mix_electrical_data(
        r,  
        start_date,
        end_date,
    ): 
        data = Main_Data_Upload.objects.filter(
                physical_coach_number=float(r),
                problem_type="Electrical Equipment",
                registration_date__range=[
                            dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            f"{end_date} {END_TIME}+00:00"],
            )
        electrical_equip.append(data.count())
        return electrical_equip
    
    def physical_coach_number_wise_complain_mix_coach_maintain_data(
        r,  
        start_date,
        end_date,
    ): 
        data = Main_Data_Upload.objects.filter(
                physical_coach_number=float(r),
                problem_type="Coach - Maintenance",
                registration_date__range=[
                            dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            f"{end_date} {END_TIME}+00:00"],
            )
        coach_maintain.append(data.count())
        return coach_maintain
    
    def physical_coach_number_wise_complain_mix_miscellaneous_data(
        r,  
        start_date,
        end_date,
    ): 
        data = Main_Data_Upload.objects.filter(
                physical_coach_number=float(r),
                problem_type="Miscellaneous",
                registration_date__range=[
                            dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            f"{end_date} {END_TIME}+00:00"],
            )
        miscellaneous.append(data.count())
        return miscellaneous
    
    def physical_coach_number_wise_complain_mix_behave_data(
        r,  
        start_date,
        end_date,
    ): 
        data = Main_Data_Upload.objects.filter(
                physical_coach_number=float(r),
                problem_type="Staff Behaviour",
                registration_date__range=[
                            dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            f"{end_date} {END_TIME}+00:00"],
            )
        staff_behave.append(data.count())
        return staff_behave
    
    def physical_coach_number_wise_complain_mix_Corruption_Bribery_data(
        r,  
        start_date,
        end_date,
    ): 
        data11 = Main_Data_Upload.objects.filter(
                physical_coach_number=float(r),
                problem_type="Corruption Bribery",
                registration_date__range=[
                            dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            f"{end_date} {END_TIME}+00:00"],
            )
        Corruption_Bribery.append(data11.count())
        return Corruption_Bribery
    
    def physical_coach_number_wise_complain_mix_catering_data(
        r,  
        start_date,
        end_date,
    ): 
        data = Main_Data_Upload.objects.filter(
                physical_coach_number=float(r),
                problem_type="Catering and Vending Services",
                registration_date__range=[
                            dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            f"{end_date} {END_TIME}+00:00"],
            )
        Catering_and_Vending_Services.append(data.count())
        return Catering_and_Vending_Services
    
    def physical_coach_number_wise_complain_mix_divyang_data(
        r,  
        start_date,
        end_date,
    ): 
        data = Main_Data_Upload.objects.filter(
                physical_coach_number=float(r),
                problem_type="Divyangjan Facilities",
                registration_date__range=[
                            dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            f"{end_date} {END_TIME}+00:00"],
            )
        Divyangjan_Facilities.append(data.count())
        return Divyangjan_Facilities
    
    def physical_coach_number_wise_complain_mix_women_data(
        r,  
        start_date,
        end_date,
    ): 
        data = Main_Data_Upload.objects.filter(
                physical_coach_number=float(r),
                problem_type="Facilities for Women with Special needs",
                registration_date__range=[
                            dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            f"{end_date} {END_TIME}+00:00"],
            )
        Facilities_for_Women_with_Special_needs.append(data.count())
        return Facilities_for_Women_with_Special_needs
    
    def train_wise_complain_mix_chart_main_data(
        complain_type,
        train_number,  
        start_date,
        end_date,
    ): 
        main_sorted_data = Main_Data_Upload.objects.values("train_station").filter(
                                                            problem_type__in=complain_type,
                                                            train_station__in=train_number,
                                                            registration_date__range=[
                                                                dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                                                                dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                                                            ],).annotate(count=Count('train_station')).order_by("-count")
        return main_sorted_data
    
    def rating_chart_with_percentage_data_complain_type(
        main_trains,
        complain_type, 
        start_date,
        end_date,
    ): 
        dataa = Main_Data_Upload.objects.filter(
                train_station__in=main_trains,
                problem_type__in=complain_type,
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
            )
        return dataa
    
    def rating_chart_with_percentage_data_with_no_complain_type(
        main_trains,
        start_date,
        end_date,
    ): 
        dataa = Main_Data_Upload.objects.filter(
                train_station__in=main_trains,
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
            )
        return dataa
    
    def trend(
           start_date ,
           end_date,
           train_numbers, 
           sub_type_list,
           complain_type_list,  
    ):
        start_month = dt.strptime(start_date, "%Y-%m-%d")
        end_month = dt.strptime(end_date, "%Y-%m-%d")

        delta = end_month - start_month
        sdate = date(
                int(start_month.year), int(start_month.month), int(start_month.day)
            )
        edate = date(int(end_month.year), int(end_month.month), int(end_month.day))
        problem_data_graph = []
        sub_type_graph = []
        dates = []
        if delta.days <= -1:
                return HttpResponse(
                    "<center><h1>Please Enter Right Date Range</h1></center>"
                )
        elif delta.days <= 149:
                for i in range(delta.days + 1):
                    day = sdate + timedelta(days=i)
                    dates.append(
                        str(day.day)
                        + " "
                        + str(calendar.month_name[day.month])
                        + ","
                        + str(day.year)
                    )

                    problem_data_data = Main_Data_Upload.objects.filter(
                        train_station__in=train_numbers,
                        registration_date__year=day.year,
                        registration_date__month=day.month,
                        registration_date__day=day.day,
                        problem_type__in=complain_type_list,
                    )
                    problem_data_graph.append(problem_data_data.count())

                    sub_type_data = Main_Data_Upload.objects.filter(
                        train_station__in=train_numbers,
                        registration_date__year=day.year,
                        registration_date__month=day.month,
                        registration_date__day=day.day,
                        sub_type__in=sub_type_list,
                        problem_type__in=complain_type_list,
                    )
                    sub_type_graph.append(sub_type_data.count())

        elif delta.days >= 150:
                strt_dt = sdate
                end_dt = edate
                datess = [dt for dt in rrule(MONTHLY, dtstart=strt_dt, until=end_dt)]
                for d in datess:
                    dates.append(calendar.month_name[int(d.month)] + "," + str(d.year))

                    problem_data = Main_Data_Upload.objects.filter(
                        train_station__in=train_numbers,
                        registration_date__year=d.year,
                        registration_date__month=d.month,
                        problem_type__in=complain_type_list,
                    )

                    problem_data_graph.append(problem_data.count())

                    sub_type_data = Main_Data_Upload.objects.filter(
                        train_station__in=train_numbers,
                        registration_date__year=d.year,
                        registration_date__month=d.month,
                        sub_type__in=sub_type_list,
                        problem_type__in=complain_type_list,
                    )
                    sub_type_graph.append(sub_type_data.count())
    
        return problem_data_graph, sub_type_graph,dates
    
    def trend_rating_if(
           start_date ,
           end_date,
           train_numbers, 
           complain_type,
           merged,  
    ):  
        if merged == " " or merged == "":
            merge = False
        else:
            merge = True
        start_month = dt.strptime(start_date, "%Y-%m-%d")
        end_month = dt.strptime(end_date, "%Y-%m-%d")

        delta = end_month - start_month
        sdate = date(
                int(start_month.year), int(start_month.month), int(start_month.day)
            )
        edate = date(int(end_month.year), int(end_month.month), int(end_month.day))
        nan = []
        excel = []
        unsatis = []
        satis = []
        dates = []
        if delta.days <= -1:
            return HttpResponse(
                "<center><h1>Please Enter Right Date Range</h1></center>"
            )

        elif delta.days <= 320:
            for i in range(delta.days + 1):
                day = sdate + timedelta(days=i)
                dates.append(
                    str(day.day)
                    + " "
                    + str(calendar.month_name[day.month])
                    +" "
                    + str(day.year)
                )

                excel_data = Main_Data_Upload.objects.filter(
                    train_station__in=train_numbers,
                    registration_date__year=day.year,
                    registration_date__month=day.month,
                    registration_date__day=day.day,
                    problem_type__in=complain_type,
                    rating="Excellent",
                )
                
                excel.append(excel_data.count())

                satis_data = Main_Data_Upload.objects.filter(
                    train_station__in=train_numbers,
                    registration_date__year=day.year,
                    registration_date__month=day.month,
                    registration_date__day=day.day,
                    problem_type__in=complain_type,
                    rating="Satisfactory",
                )
                satis.append(satis_data.count())

                unsatis_data = Main_Data_Upload.objects.filter(
                    train_station__in=train_numbers,
                    registration_date__year=day.year,
                    registration_date__month=day.month,
                    registration_date__day=day.day,
                    problem_type__in=complain_type,
                    rating="Unsatisfactory",
                )
                unsatis.append(unsatis_data.count())

                nan_data = Main_Data_Upload.objects.filter(
                    train_station__in=train_numbers,
                    registration_date__year=day.year,
                    registration_date__month=day.month,
                    registration_date__day=day.day,
                    problem_type__in=complain_type,
                    rating="-1",
                )
                
                nan.append(nan_data.count())

            merge_data = []
            if merge:
                for i in range(0, len(satis)):
                    merge_data.append(satis[i] + nan[i])
                satis = merge_data
            else:
                pass

        elif delta.days >= 321:
            strt_dt = sdate
            end_dt = edate
            datess = [dt for dt in rrule(MONTHLY, dtstart=strt_dt, until=end_dt)]
            for d in datess:
                dates.append(calendar.month_name[int(d.month)] + str(d.year))
                excel_data = Main_Data_Upload.objects.filter(
                    train_station__in=train_numbers,
                    registration_date__year=d.year,
                    registration_date__month=d.month,
                    problem_type__in=complain_type,
                    rating="Excellent",
                )
                excel.append(excel_data.count())

                satis_data = Main_Data_Upload.objects.filter(
                    train_station__in=train_numbers,
                    registration_date__year=d.year,
                    registration_date__month=d.month,
                    problem_type__in=complain_type,
                    rating="Satisfactory",
                )
                satis.append(satis_data.count())

                unsatis_data = Main_Data_Upload.objects.filter(
                    train_station__in=train_numbers,
                    registration_date__year=d.year,
                    registration_date__month=d.month,
                    problem_type__in=complain_type,
                    rating="Unsatisfactory",
                )
                unsatis.append(unsatis_data.count())

                nan_data = Main_Data_Upload.objects.filter(
                    train_station__in=train_numbers,
                    registration_date__year=d.year,
                    registration_date__month=d.month,
                    problem_type__in=complain_type,
                    rating="-1",
                )
                nan.append(nan_data.count())
            merge_data = []
            if merge:
                for i in range(0, len(satis)):
                    merge_data.append(satis[i] + nan[i])
                satis = merge_data
            else:
                pass
        return excel,satis,unsatis,nan,dates,merge
    
    def trend_rating_else(): 
        nan = []
        excel = []
        unsatis = []
        satis = []
        dates = []
        dates = []
        post = False
        for i in range(0, 31):
            tz = timezone('Asia/Kolkata')
            day = dt.now(tz) - timedelta(i)
            (
                str(day.day)
                + " "
                + str(calendar.month_name[day.month])
                + " "
                + str(day.year)
            )

            excel_data = Main_Data_Upload.objects.filter(
                registration_date__year=day.year,
                registration_date__month=day.month,
                registration_date__day=day.day,
                rating="Excellent",
            )
            excel.append(excel_data.count())

            satis_data = Main_Data_Upload.objects.filter(
                registration_date__year=day.year,
                registration_date__month=day.month,
                registration_date__day=day.day,
                rating="Satisfactory",
            )
            satis.append(satis_data.count())

            unsatis_data = Main_Data_Upload.objects.filter(
                registration_date__year=day.year,
                registration_date__month=day.month,
                registration_date__day=day.day,
                rating="Unsatisfactory",
            )
            unsatis.append(unsatis_data.count())

            nan_data = Main_Data_Upload.objects.filter(
                registration_date__year=day.year,
                registration_date__month=day.month,
                registration_date__day=day.day,
                rating="-1",
            )
            nan.append(nan_data.count())

        dates.reverse()
        satis.reverse()
        excel.reverse()
        unsatis.reverse()
        nan.reverse()

        return dates,satis,excel,unsatis,nan
    def train_sumary_table(
       start_date,
       end_date,
       complain_type,
       train_number, 
       i,
       d        
    ):
        data = Main_Data_Upload.objects.filter(
                            registration_date__range=[
                            dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        ],
                        problem_type=complain_type[i],
                        train_station=train_number[d]).count()
        return data
    

    def staff_graph_coach_clean_query(
      r,
      start_date,
      end_date,
      train_number,        
    ):
        data1 = Main_Data_Upload.objects.filter(
                staff_name=r,
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                train_station__in=train_number,
                problem_type="Coach - Cleanliness",
            )
        coach_clean.append(data1.count())
        return coach_clean

    def staff_graph_bed_query(
      r,
      start_date,
      end_date,
      train_number,        
    ):
        data2 = Main_Data_Upload.objects.filter(
                staff_name=r,
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                train_station__in=train_number,
                problem_type="Bed Roll",
            )
        bed_roll.append(data2.count())
        return bed_roll   
    
    def staff_graph_security_query(
      r,
      start_date,
      end_date,
      train_number,        
    ):
        data = Main_Data_Upload.objects.filter(
                staff_name=r,
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                train_station__in=train_number,
                problem_type="Security",
            )
        security.append(data.count())
        return security   
    
    def staff_graph_medical_query(
      r,
      start_date,
      end_date,
      train_number,        
    ):
        data4 = Main_Data_Upload.objects.filter(
                staff_name=r,
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                train_station__in=train_number,
                problem_type="Medical Assistance",
            )
        medical_assis.append(data4.count())
        return medical_assis  
    
    def staff_graph_punctuality_query(
      r,
      start_date,
      end_date,
      train_number,        
    ):
        data5 = Main_Data_Upload.objects.filter(
                staff_name=r,
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                train_station__in=train_number,
                problem_type="Punctuality",
            )
        punctuality.append(data5.count())
        return punctuality  
    
    def staff_graph_water_query(
      r,
      start_date,
      end_date,
      train_number,        
    ):
        data6 = Main_Data_Upload.objects.filter(
                staff_name=r,
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                train_station__in=train_number,
                problem_type="Water Availability",
            )
        water_avail.append(data6.count())
        return water_avail
    
    def staff_graph_electrical_query(
      r,
      start_date,
      end_date,
      train_number,        
    ):
        data7 = Main_Data_Upload.objects.filter(
                staff_name=r,
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                train_station__in=train_number,
                problem_type="Electrical Equipment",
            )
        electrical_equip.append(data7.count())
        return electrical_equip
    
    def staff_graph_maintain_query(
      r,
      start_date,
      end_date,
      train_number,        
    ):
        data8 = Main_Data_Upload.objects.filter(
                staff_name=r,
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                train_station__in=train_number,
                problem_type="Coach - Maintenance",
            )
        coach_maintain.append(data8.count())
        return coach_maintain
    
    def staff_graph_miscellaneous_query(
      r,
      start_date,
      end_date,
      train_number,        
    ):
        data9 = Main_Data_Upload.objects.filter(
                staff_name=r,
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                train_station__in=train_number,
                problem_type="Miscellaneous",
            )
        miscellaneous.append(data9.count())
        return miscellaneous
    
    def staff_graph_behave_query(
      r,
      start_date,
      end_date,
      train_number,        
    ):
        data10 = Main_Data_Upload.objects.filter(
                staff_name=r,
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                train_station__in=train_number,
                problem_type="Staff Behaviour",
            )
        staff_behave.append(data10.count())
        return staff_behave
    

    def staff_graph_corruption_query(
      r,
      start_date,
      end_date,
      train_number,        
    ):
        data11 = Main_Data_Upload.objects.filter(
                staff_name=r,
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                train_station__in=train_number,
                problem_type="Corruption Bribery",
            )
        Corruption_Bribery.append(data11.count())
        return Corruption_Bribery
    
    def staff_graph_catering_query(
      r,
      start_date,
      end_date,
      train_number,        
    ):
        data12 = Main_Data_Upload.objects.filter(
                staff_name=r,
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                train_station__in=train_number,
                problem_type="Catering and Vending Services",
            )
        Catering_and_Vending_Services.append(data12.count())
        return Catering_and_Vending_Services
    
    def staff_graph_divyang_query(
      r,
      start_date,
      end_date,
      train_number,        
    ):
        data13 = Main_Data_Upload.objects.filter(
                staff_name=r,
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                train_station__in=train_number,
                problem_type="Divyangjan Facilities",
            )
        Divyangjan_Facilities.append(data13.count())
        return Divyangjan_Facilities
    
    def staff_graph_women_query(
      r,
      start_date,
      end_date,
      train_number,        
    ):
        data14 = Main_Data_Upload.objects.filter(
                staff_name=r,
                registration_date__range=[
                    dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                train_station__in=train_number,
                problem_type="Facilities for Women with Special needs",
            )
        Facilities_for_Women_with_Special_needs.append(data14.count())
        return Facilities_for_Women_with_Special_needs
    
    def sub_type_query(
         start_date,
         end_date,
         subtypes,
    ):  
        dates = []
        data_count = []
        start_month = dt.strptime(start_date, "%Y-%m-%d")
        end_month = dt.strptime(end_date, "%Y-%m-%d")

        delta = end_month - start_month

        sdate = date(
            int(start_month.year), int(start_month.month), int(start_month.day)
        )
        edate = date(int(end_month.year), int(end_month.month), int(end_month.day))

        if delta.days <= 45:
            for i in range(delta.days + 1):
                day = sdate + timedelta(days=i)
                dates.append(
                    str(day.day)
                    + " "
                    + str(calendar.month_name[day.month])
                    + ","
                    + str(day.year)
                )
                sub_type_data = Main_Data_Upload.objects.filter(
                    sub_type=f"{subtypes}",
                    train_station__in=checked,
                    registration_date__day=day.day,
                    registration_date__month=day.month,
                    registration_date__year=day.year,
                )
                data_count.append(sub_type_data.count())
        elif delta.days <= -1:
            return HttpResponse("<h1>Please Enter valid Date Range</h1>")
        elif delta.days >= 46:
            strt_dt = sdate
            end_dt = edate
            datess = [dt for dt in rrule(MONTHLY, dtstart=strt_dt, until=end_dt)]
            for d in datess:
                dates.append(calendar.month_name[int(d.month)] + "," + str(d.year))
                sub_type_data = Main_Data_Upload.objects.filter(
                    train_station__in=checked,
                    sub_type=f"{subtypes}",
                    registration_date__month=d.month,
                    registration_date__year=d.year,
                )
                data_count.append(sub_type_data.count()) 
        return data_count,dates
    
    def disposal_time_date_wise_query(
          start_date,
           end_date,
            train_number,
            complain_type,
    ):
        start_month = dt.strptime(start_date, "%Y-%m-%d")
        end_month = dt.strptime(end_date, "%Y-%m-%d")

        delta = end_month - start_month

        sdate = date(
            int(start_month.year), int(start_month.month), int(start_month.day)
        )
        edate = date(int(end_month.year), int(end_month.month), int(end_month.day))


        dates=[]
        main_data=[]
        if delta.days <= -1:
            return HttpResponse("<h1>Please Enter valid Date Range</h1>")
        elif delta.days <= 420:
            for i in range(delta.days + 1):
                day = sdate + timedelta(days=i)
                dates.append(
                    str(day.day)
                    + " "
                    + str(calendar.month_name[day.month])
                    + " "
                    + str(day.year)
                )

                disposal_time = Main_Data_Upload.objects.filter(
                    registration_date__day=day.day,
                    registration_date__month=day.month,
                    registration_date__year=day.year,
                    problem_type__in = complain_type,
                    train_station__in = train_number
                )
                query_count = len(disposal_time)
                query_sum= disposal_time.aggregate(Sum('disposal_time')).get('disposal_time__sum')
                if query_sum == None or query_sum == "None":
                    query_sum = 0
                    query_count = 1
                else:
                    query_sum = float(query_sum)
                    query_count = query_count
                avg_query = query_sum/query_count
                main_data.append('%.2f' % avg_query)
        else:
            strt_dt = sdate
            end_dt = edate
            datess = [dt for dt in rrule(MONTHLY, dtstart=strt_dt, until=end_dt)]
            for d in datess:
                dates.append(
                    str(calendar.month_name[d.month])
                    + " "
                    + str(d.year)
                )

                disposal_time = Main_Data_Upload.objects.filter(
                    registration_date__month=d.month,
                    registration_date__year=d.year,
                    problem_type__in = complain_type,
                    train_station__in = train_number
                )
                query_count = len(disposal_time)
                query_sum= disposal_time.aggregate(Sum('disposal_time')).get('disposal_time__sum')
                if query_sum is None or query_sum == "None":
                    query_sum = 0
                    query_count = 1
                else:
                    query_sum = float(query_sum)
                    query_count = query_count
                avg_query = query_sum / query_count
                if query_count == 0:
                    main_data.append(0)
                else:
                    main_data.append('%.2f' % avg_query)    
        checked=[]
        for tr in train_number:
            checked.append(int(tr))

        return dates, main_data, checked
    

    def disposal_time_sub_type_wise_query(
          start_date,
           end_date,
            train_number,
            sub_type,
    ):  
        start_month = dt.strptime(start_date, "%Y-%m-%d")
        end_month = dt.strptime(end_date, "%Y-%m-%d")
        delta = end_month - start_month

        sdate = date(
            int(start_month.year), int(start_month.month), int(start_month.day)
        )
        edate = date(int(end_month.year), int(end_month.month), int(end_month.day))


        dates=[]
        main_data=[]
        if delta.days <= -1:
                return HttpResponse("<h1>Please Enter valid Date Range</h1>")
        elif delta.days <= 420:
            for i in range(delta.days + 1):
                day = sdate + timedelta(days=i)
                dates.append(
                    str(day.day)
                    + " "
                    + str(calendar.month_name[day.month])
                    + " "
                    + str(day.year)
                )

                disposal_time = Main_Data_Upload.objects.filter(
                    registration_date__day=day.day,
                    registration_date__month=day.month,
                    registration_date__year=day.year,
                    sub_type = str(sub_type),
                    train_station__in = train_number
                )
                query_count = len(disposal_time)
                query_sum= disposal_time.aggregate(Sum('disposal_time')).get('disposal_time__sum')
                if query_sum == None or query_sum == "None":
                    query_sum = 0
                    query_count = 1
                else:
                    query_sum = float(query_sum)
                    query_count = query_count
                avg_query = query_sum/query_count
                main_data.append('%.2f' % avg_query)

        else:
            strt_dt = sdate
            end_dt = edate
            datess = [dt for dt in rrule(MONTHLY, dtstart=strt_dt, until=end_dt)]
            for day in datess:  
                #NOTE: Here, we are traversing months in place of days
                dates.append(
                    str(calendar.month_name[day.month])
                    + " "
                    + str(day.year)
                )

                disposal_time = Main_Data_Upload.objects.filter(
                    registration_date__month=day.month,
                    registration_date__year=day.year,
                    sub_type=str(sub_type),
                    train_station__in=train_number
                )
                query_count = len(disposal_time)
                query_sum = disposal_time.aggregate(Sum('disposal_time')).get('disposal_time__sum')
                if query_sum is None or query_sum == "None":
                    query_sum = 0
                    query_count = 1
                else:
                    query_sum = float(query_sum)
                    query_count = query_count
                avg_query = query_sum / query_count
                if query_count == 0:
                    main_data.append(0)
                else:
                    main_data.append('%.2f' % avg_query)
        
        checked=[]
        for tr in train_number:
            checked.append(int(tr))

        return dates,main_data,checked
    
    def complain_type_absolute_query(
              train_numbers,
              complain_type,
              start_date,
              end_date):
        data_filter = Main_Data_Upload.objects.filter(
            train_station__in=train_numbers,
            problem_type__in=complain_type,
            registration_date__range=[
                dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
            ],
        )
        return data_filter
    
    def coach_summary_table_query(
         d,i,start_date,
          end_date,
          complain_type,
         physical_coach_number_list
    ):
        data = Main_Data_Upload.objects.filter(
                            registration_date__range=[
                            dt.strptime(f"{start_date} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                            dt.strptime(f"{end_date} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                        ],
                        problem_type=complain_type[i],physical_coach_number=physical_coach_number_list[d]).count()
        return data
