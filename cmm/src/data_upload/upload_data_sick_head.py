import json
import os
import threading
import pytz
import warnings
import copy
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
from django_ratelimit.decorators import ratelimit

IST = pytz.timezone('Asia/Kolkata')


@ratelimit(key='ip', rate=getratelimit)
@log_time
@login_required
@csrf_exempt
def upload_data_sick_head(request):
    try:
        if request.method == "POST":
            user = User.objects.get(id=request.user.id)
            if user.groups.filter(name="Moderator").exists():
                now = dt.now()
                csv_data = request.FILES.get("csv")
                dt_string = now.strftime("%d-%m-%Y %H-%M-%S")
                csv_data = request.FILES.get("csv")
                td = DataUploadSickHead(csv_data, user, now, request)
                td.start()
                messages.success(request, "Your data is Uploaded and is being processed. You will recieve an email once it is done.")
                return redirect(request.path)
            else:
                return redirect(request.path)
        # return render(request, "railmadad/data_upload.html")
        return render(request, "cmm/data_upload_sick_head.html")
    except:
        return render(request,"error.html")
class DataUploadSickHead(threading.Thread):
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
        try:
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
            print("file removed from disk")
            coach_number = -1
            data_upload_count = 0 
            length = len(self.df)
            self.df = self.df.fillna(" ")
            for i in range(0, length):
                try:
                    if self.df["Problem Date"][i] == " " or type(self.df["Problem Date"][i]) == float:
                        actual_problem_date = None

                    if (
                        self.df["Placement Date"][i] == " "
                        or type(self.df["Placement Date"][i]) == float
                    ):
                        actual_placement_date = None

                    if self.df["Fit Date"][i] == " " or type(self.df["Fit Date"][i]) == float:
                        actual_fit_date = None

                    if (
                        self.df["Problem Date"][i] != " "
                        and type(self.df["Problem Date"][i]) != float
                    ):
                        split_date = self.df["Problem Date"][i].split(" ")
                        if '/' in split_date[0]:
                            problem_datee = dt.strptime(
                                f"{split_date[0]}", "%d/%m/%Y"
                            ).strftime("%Y-%m-%d")
                        elif '-' in split_date[0]:
                            problem_datee = dt.strptime(split_date[0], "%d-%m-%Y").strftime("%Y-%m-%d")
                        register_time = f"{split_date[1]}"
                        register_date = date_parse(
                            f"{problem_datee} {register_time}"
                        )
                        n = 5.5
                        register_date_ac = register_date - timedelta(hours=n)
                        actual_problem_date = register_date_ac
                    else:
                        actual_problem_date = None

                    if (
                        self.df["Placement Date"][i] != " "
                        and type(self.df["Placement Date"][i]) != float
                    ):
                        split_date = self.df["Placement Date"][i].split(" ")
                        if '/' in split_date[0]:
                            placement_datee = dt.strptime(
                                f"{split_date[0]}", "%d/%m/%Y"
                            ).strftime("%Y-%m-%d")
                        elif '-' in split_date[0]:
                            placement_datee = dt.strptime(split_date[0], "%d-%m-%Y").strftime("%Y-%m-%d")
                        register_time = f"{split_date[1]}"
                        register_date = date_parse(
                            f"{placement_datee} {register_time}"
                        )
                        n = 5.5
                        register_date_ac = register_date - timedelta(hours=n)
                        actual_placement_date = register_date_ac

                    else:
                        actual_placement_date = None

                    if self.df["Fit Date"][i] != " " and type(self.df["Fit Date"][i]) != float:
                        split_date = self.df["Fit Date"][i].split(" ")
                        if '/' in split_date[0]:
                            fit_datee = dt.strptime(
                                f"{split_date[0]}", "%d/%m/%Y"
                            ).strftime("%Y-%m-%d")
                        elif '-' in split_date[0]:
                            fit_datee = dt.strptime(split_date[0], "%d-%m-%Y").strftime("%Y-%m-%d")
                        register_time = f"{split_date[1]}"
                        register_date = date_parse(
                            f"{fit_datee} {register_time}"
                        )
                        n = 5.5
                        register_date_ac = register_date - timedelta(hours=n)
                        actual_fit_date = register_date_ac
                    else:
                        actual_fit_date = None
                    
                    if (self.df["WorkShop"][i] == " " or self.df["WorkShop"][i]== None):
                        self.df["WorkShop"][i] = "None"
                        print("Changed Null data to None")

                    try:
                        if type(float(self.df["Train Number"][i])) == float:
                            train_number = self.df["Train Number"][i]
                        else:
                            train_number = None
                    except:
                        train_number = None

                    try:
                        if type(float(self.df["Coach Number"][i])) == float:
                            coach_number = self.df["Coach Number"][i]
                        else:
                            coach_number = None
                    except:
                        coach_number = None

                    if "/" in self.df["Sick Head / Failed Assembly"][i]:
                        print("Sick Head / Failed Assembly: ", self.df["Sick Head / Failed Assembly"][i])
                        self.df["Sick Head / Failed Assembly"][i] = self.df["Sick Head / Failed Assembly"][i].replace("/", "|")
                        print("Converted Sick Head / Failed Assembly: ", self.df["Sick Head / Failed Assembly"][i])

                    if "&" in self.df["Sick Head / Failed Assembly"][i]:
                        print("Sick Head / Failed Assembly: ", self.df["Sick Head / Failed Assembly"][i])
                        self.df["Sick Head / Failed Assembly"][i] = self.df["Sick Head / Failed Assembly"][i].replace("&", "_and")
                        print("Converted Sick Head / Failed Assembly: ", self.df["Sick Head / Failed Assembly"][i])


# New Columns
                    if self.df["Sick Head / Failed Assembly Position"][i] is not None:
                        sick_head_failed_assembly_position = self.df["Sick Head / Failed Assembly Position"][i]
                    else: 
                        sick_head_failed_assembly_position = "-1"


                    if self.df["Sub Sick Head / Failed Sub Assembly"][i] is not None:
                        sub_sick_head_failed_sub_assembly = self.df["Sub Sick Head / Failed Sub Assembly"][i]
                    else: 
                        sub_sick_head_failed_sub_assembly = "-1"


                    if self.df["Sub Sick Head Position / Failed Sub Assembly Position"][i] is not None:
                        sub_sick_head_position_failed_sub_assembly_position = self.df["Sub Sick Head Position / Failed Sub Assembly Position"][i]
                    else: 
                        sub_sick_head_position_failed_sub_assembly_position = "-1"


                    if self.df["Failed Assembly Make"][i] is not None:
                        failed_assembly_make = self.df["Failed Assembly Make"][i]
                    else: 
                        failed_assembly_make = "-1"

                    if self.df["Failed Sub Assembly Make"][i] is not None:
                        failed_sub_assembly_make = self.df["Failed Sub Assembly Make"][i]
                    else: 
                        failed_sub_assembly_make = "-1"


                    if self.df["IOH Date"][i] == " " or type(self.df["IOH Date"][i]) == float or not ( ('/' in str(self.df["IOH Date"][i])) ^ ('-' in str(self.df["IOH Date"][i]))):
                        actual_IOH_date= None
                    else :
                        if "/" in self.df["IOH Date"][i]:
                            self.df["IOH Date"][i] = self.df["IOH Date"][i].replace("/", "-")

                        split_date =  self.df["IOH Date"][i].split(" ")
                        actual_IOH_date = dt.strptime(
                            f"{split_date[0]}", "%d-%m-%Y"
                        ).date()
                            
                    if self.df["POH Date"][i] == " " or type(self.df["POH Date"][i]) == float or not ( ('/' in str(self.df["POH Date"][i])) ^ ('-' in str(self.df["POH Date"][i]))):
                        actual_POH_date= None
                    else :
                        if "/" in self.df["POH Date"][i]:
                            self.df["POH Date"][i] = self.df["POH Date"][i].replace("/", "-")

                        split_date =  self.df["POH Date"][i].split(" ")
                        actual_POH_date = dt.strptime(
                            f"{split_date[0]}", "%d-%m-%Y"
                        ).date()
                        main_data = Cmm_Sick(
                        sl_no=i,
                        unique_id=None,
                        owning_rly=self.df["Owning Rly"][i],
                        coach_number=coach_number,
                        coach_type=self.df["Coach Type"][i],
                        sick_head=self.df["Sick Head / Failed Assembly"][i],
                        cause_of_sick_marking=self.df["Cause of Sick Marking"][i],
                        reported_defect=self.df["Reported Defect"][i],
                        work_done=self.df["Work Done"][i],
                        problem_date=actual_problem_date,
                        placement_date=actual_placement_date,
                        fit_date=actual_fit_date,
                        coach_status=self.df["Coach Status"][i],
                        department=self.df["Department"][i],
                        POH_date = actual_POH_date,
                        IOH_date = actual_IOH_date,
                        ac_flag=self.df["AC Flag"][i],
                        coach_category=self.df["Coach Category"][i],
                        vehicle_type=self.df["Vehicle Type"][i],
                        train_number=train_number,
                        main_depot=self.df["Maint. Depot"][i],
                        workshop=self.df["WorkShop"][i],
                        sick_head_failed_assembly_position=sick_head_failed_assembly_position,
                        sub_sick_head_failed_sub_assembly=sub_sick_head_failed_sub_assembly,
                        sub_sick_head_position_failed_sub_assembly_position=sub_sick_head_position_failed_sub_assembly_position,
                        failed_assembly_make=failed_assembly_make,
                        failed_sub_assembly_make=failed_sub_assembly_make
                    )
                    print("Data is in processsing")

                    duplicate_data = Cmm_Sick.objects.filter(
                        sick_head=self.df["Sick Head / Failed Assembly"][i],
                        coach_number=coach_number,
                        owning_rly=self.df["Owning Rly"][i],
                        coach_type=self.df["Coach Type"][i],
                        problem_date=actual_problem_date,
                        placement_date=actual_placement_date,
                        fit_date=actual_fit_date,
                        department=self.df["Department"][i],
                        train_number=train_number,
                        workshop=self.df["WorkShop"][i],
                        ac_flag=self.df["AC Flag"][i],
                        main_depot=self.df["Maint. Depot"][i],
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
                        print(f"error in uploading data: {ex}")
                        developers_msg = f"{developers_msg}\n{coach_number}: {ex}"
                        ERROR_COACH_NUMBER.append(coach_number)

                        logging.error(f"{coach_number} - {ex}")
                        pass
                
            email_sub = create_email_subject("sick head")
            email_msg = create_email_msg(
                ERROR_COACH_NUMBER=ERROR_COACH_NUMBER, 
                CREATE_COACH_NUMBER=CREATE_COACH_NUMBER, 
                DUPLICATE_COACH_NUMBER=DUPLICATE_COACH_NUMBER, 
                current_user=self.request.user.username,
                public_url=public_url, 
                DEV_MESSAGE=developers_msg, 
                type_of_datainvoked="sick head"
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
        except :
            return      
