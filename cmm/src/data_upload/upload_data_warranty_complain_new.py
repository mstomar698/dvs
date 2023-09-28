import json
import copy
import os

import logging
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
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate=getratelimit)
@log_time
@login_required
@csrf_exempt
def upload_data_warranty_complain_new(request):
    try:
        if request.method == "POST":
            user = User.objects.get(id=request.user.id)
            if user.groups.filter(name="Moderator").exists():
                now = dt.now()
                csv_data = request.FILES.get("csv1")
                td = DataUploadWarrantyNew(csv_data, user, now, request)
                td.start()
                messages.success(request, "Your data is Uploaded and is being processed. You will recieve an email once it is done.")
                return redirect(request.path)
            else:
                return redirect(request.path)
        return render(request, "cmm/data_upload_warranty_new.html")
    except:
        return render(request,"error.html")

class DataUploadWarrantyNew(threading.Thread):
    def __init__(self, csv_data, user, time, request):
        self.csv_data = copy.deepcopy(csv_data)
        self.user = user
        now = dt.now()
        dt_string = now.strftime("%d-%m-%Y %H-%M-%S")
        ENV = os.getenv("ENV")
        self.drive_file_name = f'{ENV}-cmm_new_warranty-{user}-{dt_string}-{csv_data.name}'
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
            public_url = None
            
            convert_data = str(self.csv_data).split(" ")
            ENV = os.getenv("ENV")
            main_csv_data = "_".join(convert_data) 
            

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
            print("length", length)
            for i in range(0, length):
                try:
                    if self.df["Failure Date"][i] == " " or type(self.df["Failure Date"][i]) == float:
                        self.df["Failure Date"][i] = None
                    try:
                        udm_date = self.df["UDM Date"][i]
                    except Exception:
                        udm_date = None
                    
                    try:
                        pu_ws_date = self.df["PU/WS Date"][i]
                    except Exception:
                        pu_ws_date = None
                    
                    try:
                        div_date = self.df["Div. Date"][i]
                    except Exception:
                        div_date = None
                        
                    if (
                        self.df["Complaint Date"][i] == " "
                        or type(self.df["Complaint Date"][i]) == float
                    ):
                        self.df["Complaint Date"][i] = None

                    try:
                        assembly_mfg_date = self.df["Assembly Mfg.Date"][i]
                    except Exception:
                        assembly_mfg_date = None

                    
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

                    if (
                        self.df["UDM Date"][i] != " "
                        and type(self.df["UDM Date"][i]) != float
                    ):  
                        if "-" in self.df["UDM Date"][i]:
                            self.df["UDM Date"][i] = self.df["UDM Date"][i].replace("-", "/")

                        p = self.df["UDM Date"][i]
                        r = dt.strptime(p,"%d/%m/%Y")
                        placement_datee= r.strftime('%Y-%m-%d')
                        self.df["UDM Date"][i] = placement_datee

                    else:
                        self.df["UDM Date"][i] = None

                    if (
                        self.df["PU/WS Date"][i] != " "
                        and type(self.df["PU/WS Date"][i]) != float
                    ):  
                        if "-" in self.df["PU/WS Date"][i]:
                            self.df["PU/WS Date"][i] = self.df["PU/WS Date"][i].replace("-", "/")

                        p = self.df["PU/WS Date"][i]
                        r = dt.strptime(p,"%d/%m/%Y")
                        placement_datee= r.strftime('%Y-%m-%d')
                        self.df["PU/WS Date"][i] = placement_datee

                    else:
                        self.df["PU/WS Date"][i] = None


                    if (
                        self.df["Div. Date"][i]!= " "
                        and type(self.df["Div. Date"][i]) != float
                    ):  
                        if "-" in self.df["Div. Date"][i]:
                            self.df["Div. Date"][i] = self.df["Div. Date"][i].replace("-", "/")

                        p = self.df["Div. Date"][i]
                        r = dt.strptime(p,"%d/%m/%Y")
                        placement_datee= r.strftime('%Y-%m-%d')
                        div_date = placement_datee

                    else:
                        div_date = None
                    
                    if (
                        self.df["Assembly Mfg.Date"][i] != " "
                        and type(self.df["Assembly Mfg.Date"][i]) != float
                    ):  
                        if "-" in self.df["Assembly Mfg.Date"][i]:
                            self.df["Assembly Mfg.Date"][i] = self.df["Assembly Mfg.Date"][i].replace("-", "/")

                        p = self.df["Assembly Mfg.Date"][i]
                        r = dt.strptime(p,"%d/%m/%Y")
                        placement_datee= r.strftime('%Y-%m-%d')
                        self.df["Assembly Mfg.Date"][i] = placement_datee

                    else:
                        self.df["Assembly Mfg.Date"][i] = None
                
                            
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
                    
                    if (
                        self.df["Consignee Code"][i] != " "
                        and type(self.df["Consignee Code"][i]) != float
                    ):
                        consignee_code= self.df["Consignee Code"][i]
                    else:
                        consignee_code = None

                    if (
                        self.df["Assembly PlNo"][i] != " "
                        and type(self.df["Assembly PlNo"][i]) != float
                    ):
                        assembly_plno = self.df["Assembly PlNo"][i]
                    else:
                        assembly_plno = None

                    # if (
                    #    self.df["Assembly SrNo"][i] != " "
                    #     and type(self.df["Assembly SrNo"][i]) != float
                    # ):
                    #     assembly_srno= self.df["Assembly SrNo"][i]
                    # else:
                    #     assembly_srno = None


                    if "&" in self.df["Failed Assembly"][i]:
                        print("Failed Assembly: ", self.df["Failed Assembly"][i])
                        self.df["Failed Assembly"][i] = self.df["Failed Assembly"][i].replace("&", "_and_")
                        print("Converted Failed Assembly: ", self.df["Failed Assembly"][i])

                    if "'" in self.df["Failed Assembly"][i]:
                        print("Failed Assembly: ", self.df["Failed Assembly"][i])
                        self.df["Failed Assembly"][i] = self.df["Failed Assembly"][i].replace("'", "")
                        print("Converted Failed Assembly: ", self.df["Failed Assembly"][i])

                    main_data = Cmm_Warranty_New(
                        sl_no=i,
                        unique_id=None,
                        complaint_id = Complaint_Id,
                        complain_by_zone = self.df["Complaint by Zone"][i],
                        complain_by_division = self.df["Complaint by Division"][i],
                        complain_by_depot =  self.df["Complaint by Depot"][i],
                        consignee_code=  consignee_code,
                        complaint_to =  self.df["Complaint To"][i],
                        owning_rly =  self.df["Owning Rly."][i],
                        coach_number = self.df["Coach Number"][i],
                        coach_type =  self.df["Coach Type"][i],
                        failed_assembly =  self.df["Failed Assembly"][i],
                        assembly_manufacture =  self.df["Assembly Manufacturer"][i],
                        assembly_srno=  self.df["Assembly SrNo"][i],
                        assembly_plno= assembly_plno,
                        assembly_mfg_date =  self.df["Assembly Mfg.Date"][i],
                        failure_date =  self.df["Failure Date"][i],
                        failure_description =  self.df["Failure Desc."][i],
                        complain_date =  self.df["Complaint Date"][i],
                        complain_status =  self.df["Complaint Status"][i],
                        depot_remarks =  self.df["Depot Remarks"][i],
                        div_remarks = self.df["Div. Remarks"][i],
                        pu_ws_remarks =  self.df["PU/WS Remarks"][i],
                        udm_remarks =  self.df["UDM Remarks"][i],
                        udm_date =  self.df["UDM Date"][i],
                        pu_ws_date =   self.df["PU/WS Date"][i],
                        div_date =  div_date, 
                        complain_by_mobile =  self.df["Complaint By Mobile No."][i],
                    )

                    duplicate_data = Cmm_Warranty_New.objects.filter(
                        complaint_id = Complaint_Id,
                        coach_number=coach_number,
                        owning_rly=self.df["Owning Rly."][i],
                        coach_type=self.df["Coach Type"][i],
                    )
                    data_upload_count=0
                    if duplicate_data:
                        print("This Data Will Not Upload")
                        DUPLICATE_COACH_NUMBER.append(coach_number)
                    else:
                        try:
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
            email_sub = create_email_subject("new warranty data")
            email_msg = create_email_msg(
                ERROR_COACH_NUMBER=ERROR_COACH_NUMBER, 
                CREATE_COACH_NUMBER=CREATE_COACH_NUMBER, 
                DUPLICATE_COACH_NUMBER=DUPLICATE_COACH_NUMBER, 
                current_user=self.request.user.username,
                public_url=public_url, 
                DEV_MESSAGE=developers_msg, 
                type_of_datainvoked="new warranty data"
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
    
