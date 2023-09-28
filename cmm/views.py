import json
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
from cmm.src.use_case.sick_head_graph import sick_head_graph_implementation
from cmm.src.use_case.warranty_complain_graph import warranty_complain_graph_implementation,new_warranty_complain_graph_implementation 
from cmm.src.use_case.sick_head_table import sick_head_table_implementation
from cmm.src.use_case.coach_pro_table import coach_pro_table_implementation
from typing import List


from cmm.src.use_case.analytical_features.download_csv_cmm_PRO import download_data_csv_implementation_PRO,download_helper_implementation_PRO
from cmm.src.use_case.complain_type_implementation import (
    complain_type_implementation,
)
from cmm.src.use_case.complain_implementation import (complain_warranty_implementation,new_complain_warranty_implementation)
from cmm.src.use_case.coach_pro_query import (
    coach_pro_query_implentation,
)
from cmm.src.use_case.analytical_features.sick_head_multiple_implementation import sick_head_multiple_implementation
from cmm.src.use_case.analytical_features.download_csv_implementation import download_data_csv_implementation
from cmm.src.use_case.analytical_features.download_csv_implementation import (download_warranty_complain_data_csv_implementation,download_warranty_complain_data_new_csv_implementation,)
from cmm.src.use_case.analytical_features.download_csv_implementation import download_helper_implementation
from cmm.src.use_case.analytical_features.download_csv_implementation import (download_warranty_helper_implementation, download_warranty_helper_new_implementation,)
from s2analytica.common import log_time, getratelimit
from s2analytica.settings import CMM__DRIVE_FOLDER_ID, EMAIL_HOST_USER, SERVICE_ACCOUNT_FILE
from s2analytica.utils.save import upload_file_to_drive, save_file_to_disk
from s2analytica.utils.email import SendEmail, create_sending_list
from cmm.src.utils.email import create_email_files, create_email_msg, create_email_subject
from django_ratelimit.decorators import ratelimit

logging.basicConfig(filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')


def redircte(request):
    return redirect("/login")


##############################################################################################





##############################################
################# Main Data ###############
##############################################


@log_time
@login_required # type: ignore
@ratelimit(key='ip', rate=getratelimit)
@csrf_exempt
def upload_data_rncc_pro(request):
    try:
        if request.method == "POST":
            user = User.objects.get(id=request.user.id)
            if user.groups.filter(name="Moderator").exists():
                now = dt.now()
                dt_string = now.strftime("%d-%m-%Y %H-%M-%S")
                csv_data = request.FILES.get("csv")
                convert_data = str(csv_data).split(" ")
                main_csv_data = "_".join(convert_data)
                ENV = os.getenv("ENV")
                drive_file_name = f'{ENV}-cmm_rncc_pro-{user}-{dt_string}-{csv_data.name}'
                local_file_name = csv_data.name
                save_file_to_disk(local_file_name, csv_data)
                print("File saved to disk")
                try:
                            public_url = upload_file_to_drive(drive_file_name, local_file_name, SERVICE_ACCOUNT_FILE, CMM__DRIVE_FOLDER_ID)
                        # save a reference of the url in the database
                            csvfileurl = CsvFile.objects.create(csv_drive_url_path=public_url)
                            csvfileurl.save()
                except:
                            pass
                df = pd.read_csv(local_file_name , encoding = "ISO-8859-1") # adding encoding type to include special character in comments.

                os.remove(local_file_name)

                # data = CsvFile(csv_data=csv_data).save()
                # try:
                length = len(df)
                
                # except:
                # messages.error(
                #     request,
                #     'Uploaded should be only in Csv format and name of file should only contain space ex:- "file 1.csv","this file.csv" not any special characters including "-","_","!"--->this should not be name of file ex:-this(file).csv',
                # )
                # return redirect(request.path)
                # try:

                # print( df)
                # df.to_json(r'app/df.json')
                for i in range(0, length):
                    print(df)   
                
        return render(request, "cmm/data_upload_rncc_pro.html")
    except:
        return render(request,"error.html")


@log_time
@login_required # type: ignore
@ratelimit(key='ip', rate=getratelimit)
def sick_head_graph(request):
    try:
        context = sick_head_graph_implementation(request)
        return render(request, "cmm/sick_head_graph.html", context)
    except:
        return render(request,"error.html")


@log_time
@login_required # type: ignore
@ratelimit(key='ip', rate=getratelimit)
def sick_head_table(request):
    try:
        context = sick_head_table_implementation(request)
        return render(request, "cmm/sick_heads_table.html", context)
    except:
        return render(request,"error.html")

@log_time
@login_required # type: ignore
@ratelimit(key='ip', rate=getratelimit)
def coach_pro_table(request):
    try:
        count=-1
        context = coach_pro_table_implementation(request)
        count = context['length']
        if count >=1:
            messages.success(request, "Coach Number is found")    
        
        return render(request, "cmm/coach_pro_table.html", context)
    except:
        return render(request,"error.html")

@log_time
@login_required # type: ignore
@ratelimit(key='ip', rate=getratelimit)
def trend_rating(request):
    try:
      return render(request, "cmm/trend_rating.html")
    except:
        return render(request,"error.html")

 

@log_time
@login_required # type: ignore
@ratelimit(key='ip', rate=getratelimit)
def complain_type(request, complain, problem_start, problem_end):
    try:
        context = complain_type_implementation(
            request, complain, problem_start, problem_end
        )
        sort_order = request.GET.get("order", "")
        if request.GET.get("sort_method") != None:
            if sort_order == "":
                sort_order = "ascending"
            else:
                sort_order = "descending"
            messages.success(
                request,
                f"Sorted data with respect to {context['sort_method']} in {sort_order} order.",
            )
        return render(request, "cmm/complain_type.html", context)
    except:
        return render(request,"error.html")

@log_time
@login_required # type: ignore
@ratelimit(key='ip', rate=getratelimit)
def complain_warranty(request, complain, complain_start, complain_end):
    try:
        context = complain_warranty_implementation(
            request, complain, complain_start, complain_end
        )
        sort_order = request.GET.get("order", "")
        if request.GET.get("sort_method") != None:
            if sort_order == "":
                sort_order = "ascending"
            else:
                sort_order = "descending"
            messages.success(
                request,
                f"Sorted data with respect to {context['sort_method']} in {sort_order} order.",
            )
        return render(request, "cmm/complain_warranty.html", context)
    except:
        return render(request,"error.html")

@log_time
@login_required # type: ignore
@ratelimit(key='ip', rate=getratelimit)
def new_complain_warranty(request, complain, complain_start, complain_end):
    try:
        context = new_complain_warranty_implementation(
            request, complain,complain_start, complain_end
        )
        sort_order = request.GET.get("order", "")
        if request.GET.get("sort_method") != None:
            if sort_order == "":
                sort_order = "ascending"
            else:
                sort_order = "descending"
            messages.success(
                request,
                f"Sorted data with respect to {context['sort_method']} in {sort_order} order.",
            )
        return render(request, "cmm/new_complain_warranty.html", context)
    except:
        return render(request,"error.html")

@log_time
@login_required # type: ignore
@ratelimit(key='ip', rate=getratelimit)
def coach_pro_query(request, coach_number_id):
    try:
        context = coach_pro_query_implentation(
            request, coach_number_id
        )
        sort_order = request.GET.get("order", "")
        if request.GET.get("sort_method") != None:
            if sort_order == "":
                sort_order = "ascending"
            else:
                sort_order = "descending"
            messages.success(
                request,
                f"Sorted data with respect to {context['sort_method']} in {sort_order} order.",
            )
        return render(request, "cmm/coach_pro_query.html", context)
    except:
        return render(request,"error.html")

@log_time
@login_required # type: ignore
@ratelimit(key='ip', rate=getratelimit)
def sick_head_multiple(request):
    try:
        context = sick_head_multiple_implementation(request)
    except:
        return render(request,"error.html")


@log_time
@login_required # type: ignore
@ratelimit(key='ip', rate=getratelimit)
def warranty_complain_graph(request):
    try:
        context = warranty_complain_graph_implementation(request)
        return render(request, "cmm/warranty_complain_graph.html", context)
    except:
        return render(request,"error.html")

@log_time
@login_required # type: ignore
@ratelimit(key='ip', rate=getratelimit)
def new_warranty_complain_graph(request):
    try:
        context = new_warranty_complain_graph_implementation(request)
        return render(request, "cmm/new_warranty_complain_graph.html", context)
    except:
        return render(request,"error.html")


#####################
@log_time
@login_required # type: ignore
@ratelimit(key='ip', rate=getratelimit)
def download_sick_head_data_csv(request):
    try:
        context = download_data_csv_implementation(request)
        return render(request, "cmm/download_csv.html", context)
    except:
         return render(request,"error.html")
    
@log_time
@login_required # type: ignore
@ratelimit(key='ip', rate=getratelimit)
def download_helper(request):
    try:
        response = download_helper_implementation(request)
        return response
    except:
        return render(request,"error.html")


@log_time
@login_required # type: ignore
@ratelimit(key='ip', rate=getratelimit)
def download_data_csv_PRO(request):
    try:
        context = download_data_csv_implementation_PRO(request)
        return render(request, "cmm/download_csv_PRO.html", context)
    except:
        return render(request,"error.html")
    

@log_time
@login_required # type: ignore
@ratelimit(key='ip', rate=getratelimit)    
def download_helper_PRO(request):
    try:
        response = download_helper_implementation_PRO(request)
        return response
    except:
        return render(request,"error.html")




@log_time
@login_required # type: ignore
@ratelimit(key='ip', rate=getratelimit)
def download_warranty_complain_data_csv(request):
    try:
        context =  download_warranty_complain_data_csv_implementation(request)
        return render(request, "cmm/components_warranty/download_warranty_csv.html", context)
    except:
        return render(request,"error.html")



@log_time
@login_required # type: ignore
@ratelimit(key='ip', rate=getratelimit)
def download_warranty_helper(request):
    try:
        response = download_warranty_helper_implementation(request)
        return response
    except:
        return render(request,"error.html")

@log_time
@login_required # type: ignore
@ratelimit(key='ip', rate=getratelimit)
def download_warranty_complain_data_new_csv(request):
    try:
        context =  download_warranty_complain_data_new_csv_implementation(request)
        return render(request, "cmm/components_warranty/download_warranty_new_csv.html", context)
    except:
        return render(request,"error.html")

@log_time
@login_required # type: ignore
@ratelimit(key='ip', rate=getratelimit)
def download_warranty_helper_new(request):
    try:
        response = download_warranty_helper_new_implementation(request)
        return response
    except:
        return render(request,"error.html")
    
@log_time
@login_required # type: ignore
@ratelimit(key='ip', rate=getratelimit)
def complain(request, complain):
    try:
        context = complain_implementation(
            request, complain
        )
        sort_order = request.GET.get("order", "")
        if request.GET.get("sort_method") != None:
            if sort_order == "":
                sort_order = "ascending"
            else:
                sort_order = "descending"
            messages.success(
                request,
                f"Sorted data with respect to {context['sort_method']} in {sort_order} order.",
            )
        return render(request, "cmm/complain_warranty.html", context)
    except:
        return render(request,"error.html")

####################
data = json.load(open('./secretes.json'))
# def save_file_to_disk(local_file_name, file,request):
#     try:
#         with open(local_file_name, "wb+") as destination:
#             for chunk in file.chunks():
#                 destination.write(chunk)
#     except:
#         return render(request,"error.html")

    
# def sending_email_msg(ERROR_COACH_NUMBER: List[int], CREATE_COACH_NUMBER: List[int],
#                       DUPLICATE_COACH_NUMBER: List[int], current_user: str ,currentUserEmail: str, devMessage: str, toDev: bool, to_mail: List[str], public_url: str) -> None:
#         current_env = os.getenv("ENV")

#         if current_env is None:
#             current_env = "LOCAL"
#         HOST_USER = data.get(f"GMAIL_{current_env}", {}).get("GMAIL_USER")
#         if not toDev:
#             total_rows = len(ERROR_COACH_NUMBER) + len(CREATE_COACH_NUMBER) + len(DUPLICATE_COACH_NUMBER)
#             SUBJECT = f"Data Uploaded in RailMadad {current_env.capitalize()}"
#             to_mail.append(currentUserEmail)

#             # Get the first 10 items from the list and join them with commas. If the list is longer than 10, add "..." at the end.
#             error_value = ', '.join(str(item) for item in ERROR_COACH_NUMBER[:10]) + '...' if len(ERROR_COACH_NUMBER) > 10 else ', '.join(str(item) for item in ERROR_COACH_NUMBER)

#             if len(error_value) == 0:
#                 error_value = "0"
#             create_value = ', '.join(str(item) for item in CREATE_COACH_NUMBER[:10]) + '...' if len(CREATE_COACH_NUMBER) > 10 else ', '.join(str(item) for item in CREATE_COACH_NUMBER)
#             if len(create_value) == 0:
#                 create_value = "0"
#             update_value = ', '.join(str(item) for item in DUPLICATE_COACH_NUMBER[:10]) + '...' if len(DUPLICATE_COACH_NUMBER) > 10 else ', '.join(str(item) for item in DUPLICATE_COACH_NUMBER)
#             if len(update_value) == 0:
#                 update_value = "0"

#             MESSAGE = f"""
#     Number of rows in the input file is: {total_rows}, out of which:
#     Number of Issues while loading/updated data: {len(ERROR_COACH_NUMBER)}
#     Number of Data Loaded: {len(CREATE_COACH_NUMBER)}
#     Number of Data Updated: {len(DUPLICATE_COACH_NUMBER)}

#     DATA LOAD is invoked by {current_user}

#     Uploaded File : {public_url}

#     Issues while loading/updated data: {error_value}

#     Data Loaded: {create_value}

#     Duplicate Data: {update_value}

#     You have received this email because you were in the mailing list of Cmm.
#     """
            
#             if HOST_USER:
#                 SendEmail(SUBJECT, MESSAGE, HOST_USER, to_mail, files)

#             for file_path in files:
#                 try:
#                     os.remove(file_path)
#                 except OSError as e:
#                     print(f"Error occurred while removing file: {file_path}. Error: {e}")
#         else:
#             SUBJECT = f"DEV MESSAGE"
#             MESSAGE = f"""
#             DEVELOPER MAIL
            
#             {devMessage}

#             You have received this email because you were in the mailing list of cmm.
#             """
#             SendEmail(SUBJECT, MESSAGE, HOST_USER, ["atul.nitt@gmail.com", "kraj.krishna11@gmail.com"], [])
 

# def SendEmail( Subject:str, Message:str, HOST_USER:str, to_mail:list, Files:list ,request): # type: ignore
#     try:
#         from django.conf import settings
#         HOST_USER:str = settings.DEFAULT_FROM_EMAIL
#         from django.core.mail import EmailMessage
#         try:
#             email:EmailMessage = EmailMessage(
#                 Subject,
#                 Message,
#                 HOST_USER,
#                 to_mail
#             )
#             print("Sending email...")
#             for file in Files:
#                 email.attach_file(file)
#             email.send(fail_silently=False)
#             print("Email sent successfully!")
#         except Exception as e:
#             print("An error occurred while sending email:")
#             print(str(e))
#     except:
#         return render(request,"error.html")

