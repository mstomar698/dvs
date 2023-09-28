import json
import copy
import os

import logging
import threading
import pytz
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

@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required
@csrf_exempt
def upload_data_warranty_complain(request):
    try:
        if request.method == "POST":
            user = User.objects.get(id=request.user.id)
            if user.groups.filter(name="Moderator").exists():
                now = dt.now(IST)
                csv_data = request.FILES.get("csv1")
                td = DataUploadWarranty(csv_data, user, now, request)
                td.start()
                messages.success(request, "Your data is Uploaded and is being processed. You will recieve an email once it is done.")
                return redirect(request.path)
            else:
                return redirect(request.path)
        return render(request, "cmm/data_upload_warranty.html")
    except:
        return render(request,"error.html")


class DataUploadWarranty(threading.Thread):
    def __init__(self, csv_data, user, time, request):
        try:
            self.csv_data = copy.deepcopy(csv_data)
            self.user = user
            now = dt.now(IST)
            dt_string = now.strftime("%d-%m-%Y %H-%M-%S")
            ENV = os.getenv("ENV")
            self.drive_file_name = f'{ENV}-cmm_warranty-{user}-{dt_string}-{csv_data.name}'
            self.local_file_name = csv_data.name
            self.now = time
            self.request = request
            threading.Thread.__init__(self)
        except:
            return render(request,"error.html")

    def run(self):
        try:
            CREATE_COACH_NUMBER = []
            DUPLICATE_COACH_NUMBER = []
            ERROR_COACH_NUMBER =[]
            developers_msg = ""
            public_url = None
            
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
            for i in range(0, length):
                try:
                    if self.df["Failure Date"][i] == " " or type(self.df["Failure Date"][i]) == float:
                        self.df["Failure Date"][i] = None
                    try:
                        factory_turnout_date = self.df["Factory Turnout Date"][i]
                    except Exception:
                        factory_turnout_date = None
                        
                    if (
                        self.df["Complaint Date"][i] == " "
                        or type(self.df["Complaint Date"][i]) == float
                    ):
                        self.df["Complaint Date"][i] = None

                    try:
                        closing_date_by_pu_workshop = self.df["Closing Date By PU/Workshop"][i]
                    except Exception:
                        closing_date_by_pu_workshop = None

                    try:
                        closing_date_by_depot = self.df["Closing Date By Depot"][i]
                    except:
                        closing_date_by_depot = None
                    try:
                        if type(float(self.df["Complaint Id"][i])) == float:
                            Complaint_Id = self.df["Complaint Id"][i]
                        else:
                            Complaint_Id = None
                    except:
                        Complaint_Id = None
                    try:
                        if type(float(self.df["Coach Number"][i])) == float:
                            coach_number = self.df["Coach Number"][i]
                        else:
                            coach_number = None
                    except:
                        coach_number = None

                    if (
                        self.df["Failure Date"][i] != " "
                        and type(self.df["Failure Date"][i]) != float
                    ):  
                        if "-" in self.df["Failure Date"][i]:
                            self.df["Failure Date"][i] = self.df["Failure Date"][i].replace("-", "/")

                        p = self.df["Failure Date"][i] 
                        r = dt.strptime(p,"%d/%m/%Y")
                        placement_datee= r.strftime('%Y-%m-%d')
                        self.df["Failure Date"][i] = placement_datee

                    else:
                        self.df["Failure Date"][i] = None

                    
                    if factory_turnout_date == None:
                        factory_turnout_date = None
                    else:
                        if "/" in  str(self.df["Factory Turnout Date"][i]):
                            self.df["Factory Turnout Date"][i] = self.df["Factory Turnout Date"][i].replace("/", "-")
                            p = dt.strptime(self.df["Factory Turnout Date"][i],"%d-%m-%Y")
                            placement_datee= p.strftime('%Y-%m-%d')
                            factory_turnout_date = placement_datee
                        else:
                            factory_turnout_date = None
                            
                    if (
                        self.df["Complaint Date"][i] != " "
                        and type(self.df["Complaint Date"][i]) != float
                    ):
                        if "-" in self.df["Complaint Date"][i]:
                            self.df["Complaint Date"][i] = self.df["Complaint Date"][i].replace("-", "/")

                        p = dt.strptime(self.df["Complaint Date"][i],"%d/%m/%Y")
                        placement_datee= p.strftime('%Y-%m-%d')
                        self.df["Complaint Date"][i] = placement_datee
                    else:
                        self.df["Complaint Date"][i] = None

                    if closing_date_by_pu_workshop == None:
                        closing_date_by_pu_workshop = None
                    else:
                        split_date = str(self.df["Closing Date By PU/Workshop"][i]).split("T")
                        placement_datee = f'{split_date[0]}'
                        try:
                            register_time = f'{split_date[1]}'
                            register_date = date_parse(
                                f"{placement_datee} {register_time}"
                            )
                            register_date_ac = register_date 
                            closing_date_by_pu_workshop = register_date_ac
                        except Exception:
                            closing_date_by_pu_workshop = None

                    if (
                        self.df["Closing Date By Depot"][i] != " "
                        and type(self.df["Closing Date By Depot"][i]) != float and self.df["Closing Date By Depot"][i] !=None
                    ):
                        split_date = self.df["Closing Date By Depot"][i].split("T")
                        placement_datee = f'{split_date[0]}'
                        register_time = f"{split_date[1]}"
                        register_date = date_parse(
                            f"{placement_datee} {register_time}"
                        )
                        n = 5.5
                        register_date_ac = register_date - timedelta(hours=n)
                        self.df["Closing Date By Depot"][i] = register_date_ac
                    else:
                        self.df["Closing Date By Depot"][i] = None

                    if (
                        closing_date_by_depot != " "
                        and type(closing_date_by_depot) != float and closing_date_by_depot !=None
                    ):
                        split_date = closing_date_by_depot.split("T")
                        placement_datee = f'{split_date[0]}'
                        register_time = f"{split_date[1]}"
                        register_date = date_parse(
                            f"{placement_datee} {register_time}"
                        )
                        n = 5.5
                        register_date_ac = register_date - timedelta(hours=n)
                        closing_date_by_depot = register_date_ac
                    else:
                        closing_date_by_depot = None


                    if "&" in self.df["Failed Assembly"][i]:
                        print("Failed Assembly: ", self.df["Failed Assembly"][i])
                        self.df["Failed Assembly"][i] = self.df["Failed Assembly"][i].replace("&", "_and_")
                        print("Converted Failed Assembly: ", self.df["Failed Assembly"][i])

                    if "'" in self.df["Failed Assembly"][i]:
                        print("Failed Assembly: ", self.df["Failed Assembly"][i])
                        self.df["Failed Assembly"][i] = self.df["Failed Assembly"][i].replace("'", "")
                        print("Converted Failed Assembly: ", self.df["Failed Assembly"][i])

                    main_data = Cmm_Warranty(
                        sl_no=i,
                        unique_id=None,
                        complaint_id = Complaint_Id,
                        owning_rly=self.df["Owning Rly"][i],
                        coach_number=coach_number,
                        coach_type=self.df["Coach Type"][i],
                        factory_tumont_date = factory_turnout_date ,
                        complain_by_depot=self.df["Complaint by Depot"][i],
                        complain_by_division = self.df["Complaint by Division"][i],
                        complain_by_zone = self.df["Complaint by Zone"][i],
                        failed_assembly = self.df["Failed Assembly"][i],
                        failure_description = self.df["Failure Description"][i],
                        assembly_manufacture = self.df["Assembly Manufacturere"][i],
                        failure_date = self.df["Failure Date"][i],
                        complain_date=self.df["Complaint Date"][i],
                        complain_status=self.df["Complaint Status"][i],
                        responsible_pu_workshop = self.df["Responsible PU/workshop"][i],
                        closing_date_pu_workshop=closing_date_by_pu_workshop,
                        remark_by_pu_workshop = self.df["Remarks By PU/Workshop"][i],
                        closing_date_by_depot = closing_date_by_depot,
                        remark_by_depot = self.df["Remarks By Depot"][i],
                        complaint_name=self.df["Complainant Name"][i],
                        designation=self.df["Designation"][i],
                        location=self.df["Location"][i],
                        mobile=self.df["Mobile No."][i],
                        email_id=self.df["Email Id"][i],
                        address=self.df["Address"][i],
                        city= self.df["City"][i],
                    )
                    data_upload_count=0

                    duplicate_data = Cmm_Warranty.objects.filter(
                        complaint_id = Complaint_Id,
                        coach_number=coach_number,
                        owning_rly=self.df["Owning Rly"][i],
                        coach_type=self.df["Coach Type"][i],
                    )
                    if duplicate_data:
                        print("This Data Will Not Upload")
                        DUPLICATE_COACH_NUMBER.append(coach_number)
                    else:
                        try:
                            print(type(factory_turnout_date), type(self.df["Failure Date"][i]), type(self.df["Complaint Date"][i]),closing_date_by_depot,type(closing_date_by_pu_workshop))
                            main_data.save()
                            data_upload_count+=1
                            CREATE_COACH_NUMBER.append(coach_number)
                            failed_assembly_count= Failed_Assembly.objects.filter(
                                failed_item= self.df["Failed Assembly"][i],
                            )
                            if (len(failed_assembly_count)==0):
                                failed_data= Failed_Assembly(
                                    failed_item= self.df["Failed Assembly"][i],
                                )
                                failed_data.save()
                                print("failed_assembly saved")
                            
                            complaint_id_count= Complaint_numbers.objects.filter(
                                    complaint_id= Complaint_Id,
                                )
                            if (len(complaint_id_count)==0):
                                complain_data= Complaint_numbers(
                                complaint_id=  Complaint_Id,
                                )
                                complain_data.save()
                                print("complain_data saved")
                            
                            print("data is Uploading")
                        except Exception:
                            print("Some Error Ocuured")
                        
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
            email_sub = create_email_subject("old warranty data")
            email_msg = create_email_msg(
                ERROR_COACH_NUMBER=ERROR_COACH_NUMBER, 
                CREATE_COACH_NUMBER=CREATE_COACH_NUMBER, 
                DUPLICATE_COACH_NUMBER=DUPLICATE_COACH_NUMBER, 
                current_user=self.request.user.username,
                public_url=public_url, 
                DEV_MESSAGE=developers_msg, 
                type_of_datainvoked="old warranty data"
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
        except:
            return 
