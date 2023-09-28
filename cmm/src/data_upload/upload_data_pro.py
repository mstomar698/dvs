import os
import threading
import copy
import threading
import pytz
import warnings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import os, logging
from datetime import datetime as dt, timedelta
from dateutil.parser import parse as date_parse
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
from cmm.models import Cmm_Sick, Cmm_Warranty, Cmm_Warranty_New, Cmm_pro, Complaint_numbers, CsvFile, Failed_Assembly
from s2analytica.common import log_time, getratelimit

from s2analytica.settings import CMM__DRIVE_FOLDER_ID, EMAIL_HOST_USER, SERVICE_ACCOUNT_FILE
from s2analytica.utils.save import upload_file_to_drive, save_file_to_disk
from s2analytica.utils.email import SendEmail, create_sending_list
from cmm.src.utils.email import create_email_files, create_email_msg, create_email_subject
IST = pytz.timezone('Asia/Kolkata')
from django_ratelimit.decorators import ratelimit

@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required
@csrf_exempt
def upload_data_pro(request):
        if request.method == "POST":
            user = User.objects.get(id=request.user.id)
            if user.groups.filter(name="Moderator").exists():
                now = dt.now(IST)
                csv_data = request.FILES.get("csv")
                td = DataUploadPro(csv_data, user, now, request)
                td.start()
                messages.success(request, "Your data is Uploaded and is being processed. You will recieve an email once it is done.")
                return redirect(request.path)
            else:
                return redirect(request.path)
        # return render(request, "data_upload.html")
        return render(request, "cmm/data_upload_pro.html")
class DataUploadPro(threading.Thread):
    def __init__(self, csv_data, user, time, request):
        self.csv_data = copy.deepcopy(csv_data)
        self.user = user
        now = dt.now()
        dt_string = now.strftime("%d-%m-%Y %H-%M-%S")
        ENV = os.getenv("ENV")
        self.drive_file_name = f'{ENV}-cmm_pro-{user}-{dt_string}-{csv_data.name}'
        self.local_file_name = csv_data.name
        self.now = time
        self.request = request
        threading.Thread.__init__(self)

    def run(self):
        CREATE_COACH_NUMBER = []
        DUPLICATE_COACH_NUMBER = []
        ERROR_COACH_NUMBER =[]
        developers_msg = ""
        public_url = ""
        convert_data = str(self.csv_data).split(" ")
        main_csv_data = "_".join(convert_data)
        ENV = os.getenv("ENV")
        save_file_to_disk(self.local_file_name, self.csv_data)
        print("File saved to disk")
        try:
            public_url = upload_file_to_drive(self.drive_file_name, self.local_file_name, SERVICE_ACCOUNT_FILE, CMM__DRIVE_FOLDER_ID)
            # save a reference of the url in the database
            csvfileurl = CsvFile.objects.create(csv_drive_url_path=public_url)
            csvfileurl.save()
        except:
            pass
        self.df = pd.read_csv(self.local_file_name , encoding = "ISO-8859-1") # adding encoding type to include special character in comments.
        os.remove(self.local_file_name)  
        coach_number = -1
        data_upload_count = 0 
        length = len(self.df)
        self.df["Built Year"] = self.df["Built Year"].fillna(0)
        for i in range(0, length):
            try:     
                if 'POH/SS2/SS3/DOC Date' in self.df.columns:
                    if self.df["POH/SS2/SS3/DOC Date"][i] == " " or type(self.df["POH/SS2/SS3/DOC Date"][i]) == float or not ( ('/' in self.df["POH/SS2/SS3/DOC Date"][i]) ^ ('-' in self.df["POH/SS2/SS3/DOC Date"][i])):
                        actual_POH_date = None
                    else:
                        # NOTE: Using date_parse in place of datetime and strptime to take dynamic data
                        split_date =  self.df["POH/SS2/SS3/DOC Date"][i]
                        actual_POH_date = date_parse(split_date, dayfirst=True)  
                elif 'POH/SS2/SS3/ DOC Date' in self.df.columns:
                    if self.df["POH/SS2/SS3/ DOC Date"][i] == " " or type(self.df["POH/SS2/SS3/ DOC Date"][i]) == float or not ( ('/' in self.df["POH/SS2/SS3/ DOC Date"][i]) ^ ('-' in self.df["POH/SS2/SS3/ DOC Date"][i])):
                        actual_POH_date = None
                    else:
                        # NOTE: Using date_parse in place of datetime and strptime to take dynamic data
                        split_date =  self.df["POH/SS2/SS3/ DOC Date"][i]
                        actual_POH_date = date_parse(split_date, dayfirst=True)  
                    

                if self.df["Return Date"][i] == " " or type(self.df["Return Date"][i]) == float or not (( '/' in self.df["Return Date"][i] )^ ('-' in self.df["Return Date"][i])):
                    actual_return_date = None
                else: 

                    split_date =self.df["Return Date"][i]
                    actual_return_date = date_parse(split_date, dayfirst=True) 
                
                if (
                self.df["POH/SS2/SS3 Workshop"][i] == " "
                    or type(self.df["POH/SS2/SS3 Workshop"][i]) == float
                ):
                    actual_POH_work = None
                else:
                    actual_POH_work= self.df["POH/SS2/SS3 Workshop"][i]


                if self.df["IOH/SS1 Date"][i] == " " or type(self.df["IOH/SS1 Date"][i]) == float or not ( ('/' in str(self.df["IOH/SS1 Date"][i])) ^ ('-' in str(self.df["IOH/SS1 Date"][i]))):
                    actual_IOH_date= None
                else :
                    split_date =  self.df["IOH/SS1 Date"][i]
                    actual_IOH_date = date_parse(split_date, dayfirst=True)  
                    

                if self.df["IOH/SS1 Location"][i] == " " or type(self.df["IOH/SS1 Location"][i]) == float:
                    actual_IOH_location= None
                else :
                    actual_IOH_location= self.df["IOH/SS1 Location"][i]
                
                if self.df["Expected IOH/SS1 Due Date"][i] == " " or type(self.df["Expected IOH/SS1 Due Date"][i]) == float or not ( ('/' in str(self.df["Expected IOH/SS1 Due Date"][i])) ^ ('-' in str(self.df["Expected IOH/SS1 Due Date"][i]))):
                    actual_expected_IOH_date= None
                else:
                    split_date = self.df["Expected IOH/SS1 Due Date"][i]
                    actual_expected_IOH_date = date_parse(split_date, dayfirst=True)
                    
                if self.df["Extended Return Date"][i] == " " or type(self.df["Extended Return Date"][i]) == float or not ( ('/' in str(self.df["Extended Return Date"][i])) ^ ('-' in str(self.df["Extended Return Date"][i]))):
                    actual_extend_return_date= None
                else:
                    split_date = self.df["Extended Return Date"][i]
                    actual_extend_return_date = date_parse(split_date, dayfirst=True)  
                        
                
                if self.df["Manufacture"][i] == " " or type(self.df["Manufacture"][i]) == float:
                    actual_manufacture= None
                else:
                    actual_manufacture= self.df["Manufacture"][i]

                if self.df["Nominated Workshop"][i] == " " or type(self.df["Nominated Workshop"][i]) == float:
                    actual_nominated_workshop= None
                else:
                    actual_nominated_workshop= self.df["Nominated Workshop"][i]

                if self.df["Built Year"][i] == "0" or self.df["Built Year"][i] == " " or type(self.df["Built Year"][i]) == float  :
                    built_year= None
                else:
                    # NOTE: Try catch for taking date speacially if none is also passed
                    # built_year= self.df["Built Year"][i]
                    try:
                        built_year = int(self.df["Built Year"][i])
                    except (ValueError, TypeError):
                        try:
                            date_obj = date_parse(self.df["Built Year"][i])
                            built_year = date_obj.year
                        except ValueError:
                            built_year = None
                
                if self.df["Base Depot"][i] == " " or type(self.df["Base Depot"][i]) == float:
                    actual_base_depot= None
                else:
                    actual_base_depot= self.df["Base Depot"][i]


                if self.df["Last Update Time"][i] == " " or type(self.df["Last Update Time"][i]) == float or not ( ('/' in str(self.df["Last Update Time"][i])) ^ ('-' in str(self.df["Last Update Time"][i]))): 
                    last_updated_time= None
                else:
                    split_date = self.df["Last Update Time"][i]
                    last_updated_time = date_parse(split_date, dayfirst=True) 

                try:
                    if type(float(self.df["Coach Number"][i])) == float:
                        coach_number = self.df["Coach Number"][i]
                    else:
                        coach_number = None
                except:
                    coach_number = None

                try:
                    if str(self.df["Updated By"][i]).isnumeric() and type(float(self.df["Updated By"][i])) == float:
                        last_updated_by = self.df["Updated By"][i]
                    else:
                        last_updated_by = None
                except:
                    last_updated_by = None
                
                if "Coach Category" in self.df:
                    actual_coach_category = self.df["Coach Category"][i]
                else:
                    actual_coach_category= None
                
                if "AC Flag" in self.df:
                    actual_AC_flag = self.df["AC Flag"][i]
                else:
                    actual_AC_flag = None
                
                if "Gauge" in self.df:
                    actual_gauge = self.df["Gauge"][i]
                else:
                    actual_gauge = None

                # if "/" in self.df["Sick Head"][i]:
                #     print("Sick Head: ", self.df["Sick Head"][i])
                #     self.df["Sick Head"][i] = self.df["Sick Head"][i].replace("/", "|")
                #     print("Converted Sick Head: ", self.df["Sick Head"][i])

                # if "&" in self.df["Sick Head"][i]:
                #     print("Sick Head: ", self.df["Sick Head"][i])
                #     self.df["Sick Head"][i] = self.df["Sick Head"][i].replace("&", "_and")
                #     print("Converted Sick Head: ", self.df["Sick Head"][i])

                main_data = Cmm_pro(
                    sl_no=i,
                    unique_id=None,
                    owning_rly=self.df["Owning Rly"][i],
                    coach_number=coach_number,
                    coach_type=self.df["Coach Type"][i],
                    coach_category= actual_coach_category, 
                    ac_flag=actual_AC_flag,
                    guage= actual_gauge,
                    POH_date =  actual_POH_date,
                    return_date =  actual_return_date,
                    POH_work = actual_POH_work,
                    IOH_date = actual_IOH_date,
                    IOH_location= actual_IOH_location,
                    expected_IOH_date = actual_expected_IOH_date,
                    extend_return_date = actual_extend_return_date,
                    manufacture = actual_manufacture,
                    nominated_workshop =  actual_nominated_workshop,
                    built_year = built_year,
                    base_depot = actual_base_depot,
                    main_depot = self.df["Maint. Depot"][i],
                    main_division = self.df["Maint. Division"][i],
                    main_railway = self.df["Maint. Railway"][i],
                    last_updated_time =  last_updated_time,
                    last_updated_by = last_updated_by,
                    
                )

                duplicate_data = Cmm_pro.objects.filter(
                    POH_date =  actual_POH_date, 
                    coach_number=coach_number,
                    owning_rly=self.df["Owning Rly"][i],
                    coach_type=self.df["Coach Type"][i],
                    guage= actual_gauge,
                    coach_category=actual_coach_category,
                    return_date =  actual_return_date,
                    POH_work = actual_POH_work,
                    IOH_date = actual_IOH_date,
                    IOH_location= actual_IOH_location,
                    manufacture = actual_manufacture, 
                    nominated_workshop =  actual_nominated_workshop,
                    ac_flag=actual_AC_flag,
                    main_depot=self.df["Maint. Depot"][i],
                    last_updated_time =  last_updated_time,
                    last_updated_by = last_updated_by,
                )
                data_upload_count=0

                if len(duplicate_data) >= 1:
                    DUPLICATE_COACH_NUMBER.append(coach_number)
                    print("This Data Will Not Upload")
                else:
                    main_data.save()
                    data_upload_count+=1
                    CREATE_COACH_NUMBER.append(coach_number)
                    print("data is Uploading")

            except Exception as ex:
                try:
                    if type(float(self.df["Coach Number"][i])) == float:
                        coach_number = self.df["Coach Number"][i]
                    else:
                        coach_number = None
                except:
                    coach_number = None
                print("error in uploading data")
                developers_msg = f"{developers_msg}\n{coach_number}: {ex}"
                ERROR_COACH_NUMBER.append(coach_number)

                logging.error(f"{coach_number} - {ex}")
                pass
        
        email_sub = create_email_subject("pro")
        email_msg = create_email_msg(
            ERROR_COACH_NUMBER=ERROR_COACH_NUMBER, 
            CREATE_COACH_NUMBER=CREATE_COACH_NUMBER, 
            DUPLICATE_COACH_NUMBER=DUPLICATE_COACH_NUMBER, 
            current_user=self.request.user.username,
            public_url=public_url, 
            DEV_MESSAGE=developers_msg, 
            type_of_datainvoked="pro"
            )
        email_files = create_email_files(
            ERROR_COACH_NUMBER=ERROR_COACH_NUMBER, 
            CREATE_COACH_NUMBER=CREATE_COACH_NUMBER, 
            DUPLICATE_COACH_NUMBER=DUPLICATE_COACH_NUMBER, 
        )
        email_list = create_sending_list(self.request.user.email)

        SendEmail(email_sub, email_msg, EMAIL_HOST_USER, email_list, email_files)

        # Cleanup temproary files
        for file_path in email_files:
            os.remove(file_path)
            
    #     if data_upload_count >=1:
    #         messages.success(request, "Data is Uploaded")
    #         return redirect(request.path)
    #         else:
    #            messages.error(request, "No New Data is Uploaded")
    #            return redirect(request.path) 
    #     else:
    #         messages.error(request, "You Cannot Upload Data")
    #         return redirect(request.path)

    # return render(request, "cmm/data_upload_pro.html")


# @login_required
# @csrf_exempt
# def upload_data_rncc_pro(request):
#     if request.method == "POST":
#         user = User.objects.get(id=request.user.id)
#         if user.groups.filter(name="Moderator").exists():
#             now = dt.now()
#             dt_string = now.strftime("%d-%m-%Y %H-%M-%S")
#             csv_data = request.FILES.get("csv")
#             convert_data = str(csv_data).split(" ")
#             main_csv_data = "_".join(convert_data)
#             ENV = os.getenv("ENV")
#             drive_file_name = f'{ENV}-cmm_rncc_pro-{user}-{dt_string}-{csv_data.name}'
#             local_file_name = csv_data.name
#             save_file_to_disk(local_file_name, csv_data)
#             print("File saved to disk")
#             try:
#                         public_url = upload_file_to_drive(drive_file_name, local_file_name, SERVICE_ACCOUNT_FILE, CMM__DRIVE_FOLDER_ID)
#                      # save a reference of the url in the database
#                         csvfileurl = CsvFile.objects.create(csv_drive_url_path=public_url)
#                         csvfileurl.save()
#             except:
#                         pass
#             self.df = pd.read_csv(local_file_name , encoding = "ISO-8859-1") # adding encoding type to include special character in comments.

#             os.remove(local_file_name)

#             # data = CsvFile(csv_data=csv_data).save()
#             # try:
#             length = len(self.df)
            
#             # except:
#             # messages.error(
#             #     request,
#             #     'Uploaded should be only in Csv format and name of file should only contain space ex:- "file 1.csv","this file.csv" not any special characters including "-","_","!"--->this should not be name of file ex:-this(file).csv',
#             # )
#             # return redirect(request.path)
#             # try:

#             # print( self.df)
#             # self.df.to_json(r'app/self.df.json')
#             for i in range(0, length):
#                 print(self.df)   
             
#     return render(request, "cmm/data_upload_rncc_pro.html")